import copy
import json
import math
import pandas as pd
import numpy as np
import warnings
import pygad

from PolarChecker import getError
from RemoveBadData import (
    BestTrustAdjustedData,
    TeamBasedData,
    getBestData,
    getMarkovianRatings,
    getTrustAdjustedData,
)

warnings.filterwarnings("ignore")


def flatten_dict(dd, separator="_", prefix=""):
    return (
        {
            prefix + separator + k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in flatten_dict(vv, separator, kk).items()
        }
        if isinstance(dd, dict)
        else {prefix: dd}
    )


def getPiecesScored(match: dict, communityStr: str, allianceStr: str) -> list:
    hco = getPieceScored(match, communityStr, allianceStr, "T", "Cone")
    hcu = getPieceScored(match, communityStr, allianceStr, "T", "Cube")
    mco = getPieceScored(match, communityStr, allianceStr, "M", "Cone")
    mcu = getPieceScored(match, communityStr, allianceStr, "M", "Cube")
    lco = getPieceScored(match, communityStr, allianceStr, "B", "Cone")
    lcu = getPieceScored(match, communityStr, allianceStr, "B", "Cube")
    lp = lcu + lco
    return [hco, hcu, mco, mcu, lp]


def getPieceScored(
    match: dict,
    communityStr: str,
    allianceStr: str,
    row: str,
    piece: str,
) -> int:
    retval = 0
    for spot in match["score_breakdown"][allianceStr][communityStr][row]:
        if spot[:4] == piece:
            retval += 1
    return retval


def analyzeData(m_data: list):
    realData = m_data[0]
    data = m_data[1]
    oprMatchList = []
    # Isolating Data Related to OPR
    blankOprEntry = {
        "auto_hco": 0,
        "auto_hcu": 0,
        "auto_mco": 0,
        "auto_mcu": 0,
        "auto_lp": 0,
        "teleop_hco": 0,
        "teleop_hcu": 0,
        "teleop_mco": 0,
        "teleop_mcu": 0,
        "teleop_lp": 0,
        "station1": 0,
        "station2": 0,
        "station3": 0,
        "match_number": 0,
        "allianceStr": "",
    }
    for row in data:
        for j in range(2):
            if j == 1:
                allianceStr = "red"
            else:
                allianceStr = "blue"
            oprMatchEntry = copy.deepcopy(blankOprEntry)
            oprMatchEntry["allianceStr"] = allianceStr
            oprMatchEntry["match_number"] = row["match_number"]
            for k in range(3):
                oprMatchEntry["station" + str(k + 1)] = row["alliances"][allianceStr][
                    "team_keys"
                ][k][3:]
            piecesScored = getPiecesScored(row, "autoCommunity", allianceStr)
            oprMatchEntry["auto_hco"] = piecesScored[0]
            oprMatchEntry["auto_hcu"] = piecesScored[1]
            oprMatchEntry["auto_mco"] = piecesScored[2]
            oprMatchEntry["auto_mcu"] = piecesScored[3]
            oprMatchEntry["auto_lp"] = piecesScored[4]
            piecesScored = getPiecesScored(row, "teleopCommunity", allianceStr)
            oprMatchEntry["teleop_hco"] = piecesScored[0]
            oprMatchEntry["teleop_hcu"] = piecesScored[1]
            oprMatchEntry["teleop_mco"] = piecesScored[2]
            oprMatchEntry["teleop_mcu"] = piecesScored[3]
            oprMatchEntry["teleop_lp"] = piecesScored[4]
            oprMatchList.append(copy.deepcopy(oprMatchEntry))
    oprMatchDataFrame = pd.DataFrame(oprMatchList)
    teams = []
    for k in range(3):
        for matchTeam in oprMatchDataFrame["station" + str(k + 1)]:
            exists = False
            for team in teams:
                if matchTeam == team:
                    exists = True
            if not exists:
                teams.append(matchTeam)
    teams.sort()
    # TBA Data for Y Matrix
    YKeys = [
        "auto_hco",
        "auto_hcu",
        "auto_mco",
        "auto_mcu",
        "auto_lp",
        "teleop_hco",
        "teleop_hcu",
        "teleop_mco",
        "teleop_mcu",
        "teleop_lp",
    ]

    scoutingBaseData = m_data[2]
    errorData = []
    numEntries = len(scoutingBaseData)
    j = numEntries
    # TBA Data
    YMatrix = pd.DataFrame(None, columns=YKeys)
    # YMatrix = oprMatchDataFrame[YKeys]
    # matchTeamMatrix = oprMatchDataFrame[["station1", "station2", "station3"]]
    blankAEntry = {}
    for team in teams:
        blankAEntry[team] = 0
    Alist = []
    # for game in matchTeamMatrix.values.tolist():
    #     AEntry = copy.deepcopy(blankAEntry)
    #     for team in game:
    #         AEntry[team] = 1
    #     Alist.append(AEntry)
    # Fitting Scouting Data to Matrices A and Y
    scoutingData = copy.deepcopy(scoutingBaseData[:j])
    teamMatchesList = copy.deepcopy(blankAEntry)
    # Throw out bad scouting data
    scoutingDataFunction = TeamBasedData
    print(scoutingDataFunction.__name__)
    scoutingData = scoutingDataFunction(oprMatchDataFrame, scoutingData)
    for team in teams:
        teamMatches = []
        for entry in scoutingData:
            for k in range(2):
                if k == 0:
                    allianceStr = "blue"
                else:
                    allianceStr = "red"
                if type(entry["metadata"]) == dict:
                    if entry["metadata"]["team_number"] == team:
                        if not teamMatches.__contains__(
                            entry["metadata"]["match_number"]
                        ):
                            teamMatches.append(entry["metadata"]["match_number"])
        teamMatchesList[team] = teamMatches
    teamIdx = -1
    for team in teams:
        teamIdx += 1
        teamYEntry = [0 for k in range(len(YKeys))]
        for teamMatch in teamMatchesList[team]:
            numEntries = 0
            for entry in scoutingData:
                if type(entry["metadata"]) == dict:
                    if (
                        entry["metadata"]["team_number"] == team
                        and entry["metadata"]["match_number"] == teamMatch
                    ):
                        numEntries += 1
            for entry in scoutingData:
                if type(entry["metadata"]) == dict:
                    if (
                        entry["metadata"]["team_number"] == team
                        and entry["metadata"]["match_number"] == teamMatch
                    ):
                        data = flatten_dict(entry["data"])
                        newY = [data[key] for key in YKeys]
                        teamYEntry = [
                            teamYEntry[i]
                            + (newY[i] / len(teamMatchesList[team]) / numEntries)
                            for i in range(len(teamYEntry))
                        ]
        YMatrix.loc[len(YMatrix)] = teamYEntry
        teamAEntry = copy.deepcopy(blankAEntry)
        teamAEntry[team] = 1
        Alist.append(teamAEntry)
    # Compiling data into matrices
    AMatrix = pd.DataFrame(Alist, columns=teams)
    APseudoInverse = np.linalg.pinv(AMatrix[teams])
    # Multivariate Regression
    XMatrix = pd.DataFrame(APseudoInverse @ YMatrix)
    XMatrix["team_number"] = teams
    cols = XMatrix.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    XMatrix = XMatrix[cols]
    # errorData.append(getError(XMatrix, realData))
    # errorDataFrame = pd.DataFrame(errorData, columns=["Average Error"])
    # Run Genetic Algorithm
    functionInputs = [AMatrix, YMatrix.loc[:, YMatrix.columns != "MatchNumber"]]
    desiredError = 0

    def fitness_func(ga_instance: pygad.GA, solution, solution_idx):
        fitness = 0
        error = 0.0
        solutionMatrix = pd.DataFrame(
            [
                solution[x : x + len(XMatrix.columns) - 1]
                for x in range(0, len(solution), len(XMatrix.columns) - 1)
            ]
        )

        for i in range(len(functionInputs[0])):
            aseries = functionInputs[0].iloc[i]
            yseries = functionInputs[1].iloc[i]
            matchTeams = []
            for a, b in aseries.items():
                if b == 1:
                    matchTeams.append(a)
            blankList = []
            for a, b in yseries.items():
                blankList.append(0)
            solutionSeries = pd.Series(blankList, index=yseries.axes)
            for matchTeam in matchTeams:
                solutionSeries += pd.Series(solutionMatrix.iloc[teams.index(matchTeam)])
            errorlist = [
                abs(solutionSeries[i] - yseries[i]) for i in range(len(yseries - 1))
            ]
            for num in errorlist:
                error += num
        if error != 0:
            fitness = 1 / error
        return fitness

    numGenerations = 50
    numParentsMating = 8
    sol_per_pop = 8
    num_genes = len(XMatrix) * (len(XMatrix.columns) - 1)
    fitness_batch_size = 1
    init_range_low = 0
    init_range_high = 15

    parent_selection_type = "rank"
    keep_parents = 1

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    def on_start(ga_instance):
        print("on_start()")

    def on_fitness(ga_instance, population_fitness):
        print("on_fitness()")

    def on_parents(ga_instance, selected_parents):
        print("on_parents()")

    def on_crossover(ga_instance, offspring_crossover):
        print("on_crossover()")

    def on_mutation(ga_instance, offspring_mutation):
        print("on_mutation()")

    def on_generation(ga_instance):
        print("on_generation()")

    def on_stop(ga_instance, last_population_fitness):
        print("on_stop()")

    ga_instance = pygad.GA(
        num_generations=numGenerations,
        num_parents_mating=numParentsMating,
        fitness_func=fitness_func,
        fitness_batch_size=fitness_batch_size,
        sol_per_pop=sol_per_pop,
        num_genes=num_genes,
        init_range_low=init_range_low,
        init_range_high=init_range_high,
        parent_selection_type=parent_selection_type,
        keep_parents=keep_parents,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes,
        on_start=on_start,
        on_fitness=on_fitness,
        on_parents=on_parents,
        on_crossover=on_crossover,
        on_mutation=on_mutation,
        on_generation=on_generation,
        on_stop=on_stop,
    )
    ga_instance.run()
    # ga_instance.plot_fitness()
    # solution, solution_fitness, solution_idx = ga_instance.best_solution()
    # print(solution_fitness)
    # XMatrix = pd.DataFrame(solution, columns=XMatrix.columns)
    return getError(XMatrix, realData)