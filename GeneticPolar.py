import copy
import json
import math
import pandas as pd
import numpy as np
import warnings
import pygad

from PolarChecker import getError
from RemoveBadData import BestTrustAdjustedData, TeamBasedData, getBestData, getMarkovianRatings, getTrustAdjustedData

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


# @jit(target_backend='cuda')


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
    AMatrix = pd.DataFrame(Alist)
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
    nn = pygad.GA()
    return getError(XMatrix, realData)