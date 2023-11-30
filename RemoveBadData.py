import pandas as pd


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


def getError(combination: dict, TBAMatch: pd.Series) -> float:
    error = 0
    total = 0
    errorPercent = 1.0
    data = []
    for team in combination:
        data.append(flatten_dict(combination[team]["data"]))
    addedData = data[0]
    for field in addedData:
        addedData[field] = data[0][field] + data[1][field] + data[2][field]
        total += abs(TBAMatch[field])
        error += abs(TBAMatch[field] - addedData[field])
    if (total > 0):
        errorPercent = error/total
    return errorPercent

def throwAwayBadData(TBAData: pd.DataFrame, scoutingData: list):
    retval = []
    TBADict = TBAData.to_dict("records")
    j = 0
    for game in TBADict:
        j += 1
        entries = []
        teamEntries = {}
        teams = []
        for entry in scoutingData:
            if type(entry["metadata"]) == dict:
                if entry["metadata"]["match_number"] == game["match_number"]:
                    for i in range(3):
                        if game["station" + str(i + 1)] == entry["metadata"]["team_number"]:
                            entries.append(entry)
                            if not teams.__contains__(entry["metadata"]["team_number"]):
                                teams.append(entry["metadata"]["team_number"])
                            break
        for entry in entries:
            teamEntries[entry["metadata"]["team_number"]] = []
        for entry in entries:
            teamEntries[entry["metadata"]["team_number"]].append(entry)
        combinations = []
        if len(teams) == 3:
            for team0 in teamEntries[teams[0]]:
                for team1 in teamEntries[teams[1]]:
                    for team2 in teamEntries[teams[2]]:
                        combinations.append(
                            {teams[0]: team0, teams[1]: team1, teams[2]: team2}
                        )
            combinationError = []
            for i in range(len(combinations)):
                combinationError.append(getError(combinations[i], game))
            returnCombination = combinations[combinationError.index(min(combinationError))]
            # combinationTrust = [1-combinationError[i] for i in range(len(combinationError))]
            # for i in range(len(combinations)):
            #     for entry in combinations[i]:
            #         for field in combinations[i][entry]:
            #             returnCombination[entry][field] = 0
            #     for entry in combinations[i]:
            #         for field in combinations[i][entry]:
            #             if not type(combinations[i][entry][field]) == dict:
            #                 returnCombination[entry][field] += combinationTrust[i]*combinations[i][entry][field]
            # for entry in returnCombination:
            #     for field in returnCombination[entry]:
            #         if not(sum(combinationTrust) == 0):
            #             returnCombination[entry][field] /= sum(combinationTrust)
            for entry in returnCombination:
                if not retval.__contains__(entry):
                    retval.append(returnCombination[entry])
        else:
            for entry in entries:
                if not retval.__contains__(entry):
                    retval.append(entry)
    return retval
