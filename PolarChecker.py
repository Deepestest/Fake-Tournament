import copy
import json

import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def getPiecesScored(match: dict, communityStr: str, driverStation: str) -> list:
    if driverStation[0] == "r":
        allianceStr = "red"
    else:
        allianceStr = "blue"
    hco = getPieceScored(match, communityStr, allianceStr, driverStation, "T", "Cone")
    hcu = getPieceScored(match, communityStr, allianceStr, driverStation, "T", "Cube")
    mco = getPieceScored(match, communityStr, allianceStr, driverStation, "M", "Cone")
    mcu = getPieceScored(match, communityStr, allianceStr, driverStation, "M", "Cube")
    lco = getPieceScored(match, communityStr, allianceStr, driverStation, "B", "Cone")
    lcu = getPieceScored(match, communityStr, allianceStr, driverStation, "B", "Cube")
    lp = lcu + lco
    return [hco, hcu, mco, mcu, lp]


def getPieceScored(
    match: dict,
    communityStr: str,
    allianceStr: str,
    driverStation: str,
    row: str,
    piece: str,
) -> int:
    retval = 0
    for spot in match["score_breakdown"][allianceStr][communityStr][row]:
        if spot[4:] == driverStation:
            if spot[:4] == piece:
                retval += 1
    return retval


def addValues(teamData: dict, newData: list, teleop: bool) -> pd.Series:
    retval = copy.deepcopy(teamData)
    if teleop:
        communityStr = "teleop"
    else:
        communityStr = "auto"
    retval[communityStr + "_hco"] += newData[0]
    retval[communityStr + "_hcu"] += newData[1]
    retval[communityStr + "_mco"] += newData[2]
    retval[communityStr + "_mcu"] += newData[3]
    retval[communityStr + "_lp"] += newData[4]
    return retval


def getError(polarData: pd.DataFrame, realData: list) -> list:
    teams = []
    for game in realData:
        for i in range(2):
            if i == 1:
                allianceStr = "red"
            else:
                allianceStr = "blue"
            for x in game["alliances"][allianceStr]["team_keys"]:
                matchTeam = x[3:]
                exists = False
                for team in teams:
                    if matchTeam == team:
                        exists = True
                if not exists:
                    teams.append(matchTeam)
    teams.sort()
    blankTeamData = {
        "team_number": 0,
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
        "numMatches": 0,
    }
    teamDataList = []

    for team in teams:
        teamData = copy.deepcopy(blankTeamData)
        teamData["team_number"] = team
        for game in realData:
            for i in range(2):
                if i == 1:
                    allianceStr = "red"
                else:
                    allianceStr = "blue"
                if game["alliances"][allianceStr]["team_keys"].__contains__(
                    "frc" + str(team)
                ):
                    driverStation = allianceStr[0] + str(
                        game["alliances"][allianceStr]["team_keys"].index(
                            "frc" + str(team)
                        )
                        + 1
                    )
                    autoScoring = getPiecesScored(game, "autoCommunity", driverStation)
                    teleopScoring = getPiecesScored(
                        game, "teleopCommunity", driverStation
                    )
                    teamData = addValues(teamData, autoScoring, False)
                    teamData = addValues(teamData, teleopScoring, True)
                    teamData["numMatches"] +=1
        teamDataList.append(teamData)
    for teamData in teamDataList:
        teamData["auto_hco"] /= teamData["numMatches"]
        teamData["auto_hcu"] /= teamData["numMatches"]
        teamData["auto_mco"] /= teamData["numMatches"]
        teamData["auto_mcu"] /= teamData["numMatches"]
        teamData["auto_lp"] /= teamData["numMatches"]
        teamData["teleop_hco"] /= teamData["numMatches"]
        teamData["teleop_hcu"] /= teamData["numMatches"]
        teamData["teleop_mco"] /= teamData["numMatches"]
        teamData["teleop_mcu"] /= teamData["numMatches"]
        teamData["teleop_lp"] /= teamData["numMatches"]
    teamDataFrame = pd.DataFrame(teamDataList)
    importantKeys = [
        "team_number",
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
    actualData = teamDataFrame[importantKeys]
    actualData.to_csv("PolarChecker.csv")
    errorKeys = importantKeys[1:]
    errorData = copy.deepcopy(polarData)
    for i in range(len(polarData)):
        for errorKey in errorKeys:
            errorData[errorKey][i] = abs(
                polarData[errorKey][i] - actualData[errorKey][i]
            )
    errorData = errorData[errorKeys]
    return sum(errorData.mean())
