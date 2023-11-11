import copy
import json
import pandas as pd
import numpy as np
import warnings

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


dataFile = open("TBAOutput.json")
data = json.load(dataFile)
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
}
for row in data:
    for i in range(2):
        if i == 1:
            allianceStr = "red"
        else:
            allianceStr = "blue"
        oprMatchEntry = copy.deepcopy(blankOprEntry)
        oprMatchEntry["station1"] = row["alliances"][allianceStr]["team_keys"][0][3:]
        oprMatchEntry["station2"] = row["alliances"][allianceStr]["team_keys"][1][3:]
        oprMatchEntry["station3"] = row["alliances"][allianceStr]["team_keys"][2][3:]
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
for i in range(3):
    for matchTeam in oprMatchDataFrame["station" + str(i + 1)]:
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
YMatrix = oprMatchDataFrame[YKeys]

# TBA Data for A Matrix
matchTeamMatrix = oprMatchDataFrame[["station1", "station2", "station3"]]
blankAEntry = {}
for team in teams:
    blankAEntry[team] = 0
Alist = []
for game in matchTeamMatrix.values.tolist():
    AEntry = copy.deepcopy(blankAEntry)
    for team in game:
        AEntry[team] = 1
    Alist.append(AEntry)

# Fitting Scouting Data to Matrices A and Y
# scoutingDataFile = open("ScoutingOutput.json")
# scoutingData = json.load(scoutingDataFile)
# for entry in scoutingData:
#     AEntry = copy.deepcopy(blankAEntry)
#     AEntry[entry["metadata"]["team_number"]] = 1
#     Alist.append(AEntry)
#     data = flatten_dict(entry["data"])
#     YEntry = [data[key] for key in YKeys]
#     YMatrix.loc[len(YMatrix.index)] = YEntry
AMatrix = pd.DataFrame(Alist)
APseudoInverse = np.linalg.pinv(AMatrix)

# Multivariate Regression
XMatrix = pd.DataFrame(APseudoInverse @ YMatrix)
XMatrix["team_number"] = teams
cols = XMatrix.columns.tolist()
cols = cols[-1:] + cols[:-1]
XMatrix = XMatrix[cols]
AMatrix.to_csv("AMatrix.csv")
YMatrix.to_csv("YMatrix.csv")
XMatrix.to_csv("PolarOutput.csv")
