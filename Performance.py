import random
import pandas as pd
import numpy as np
import json

from Robot import dockingAutoRobots, randomRobot


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def combinePlacements(placementList: list) -> list:
    retval = []
    for i in range(3):
        retval.append([])
        for j in range(9):
            retval[i].append("None")
    for placements in placementList:
        for i in range(len(placements)):
            for j in range(len(placements[0])):
                if retval[i][j] == "None":
                    retval[i][j] = placements[i][j]
                else:
                    rand = random.random()
                    if rand < 0.5:
                        retval[i][j] = placements[i][j]
    return retval


def getAutoPlacements(bots: list, middleBot: int, alliance: str) -> list:
    retval = bots[0].getAutos().getMiddle().getPlacements(alliance, middleBot + 1)
    rand = random.random()
    feederBot = (middleBot + 1) % 3
    if rand < 0.5:
        bumpBot = feederBot
        feederBot += 1
        feederBot %= 3
    else:
        bumpBot = feederBot + 1
        bumpBot %= 3
    retval = combinePlacements(
        [
            retval,
            bots[bumpBot].getAutos().getBump().getPlacements(alliance, bumpBot + 1),
            bots[feederBot]
            .getAutos()
            .getFeeder()
            .getPlacements(alliance, feederBot + 1),
        ]
    )
    return retval


teamsCSV = pd.read_csv("Teams.csv")
numTeams = 0
robots = []
TBAMatchesJson = []
for team in teamsCSV["Team"]:
    robots.append(randomRobot(team))
    numTeams += 1
matchCSV = pd.read_csv("Matches.csv")
numMatches = 0
for matchNumber in matchCSV["Match Number"]:
    numMatches += 1
for matchNumber in matchCSV["Match Number"]:
    matchJSONFile = open("Match.json")
    TBAMatchJson = json.load(matchJSONFile)
    # ActualMatchJson = json.load()
    matchRobots = []
    for i in range(6):
        matchRobots.append(None)
    r1 = matchCSV["R1"][matchNumber - 1]
    r2 = matchCSV["R2"][matchNumber - 1]
    r3 = matchCSV["R3"][matchNumber - 1]
    b1 = matchCSV["B1"][matchNumber - 1]
    b2 = matchCSV["B2"][matchNumber - 1]
    b3 = matchCSV["B3"][matchNumber - 1]
    # Metadata
    TBAMatchJson["alliances"]["blue"]["team_keys"][0] = "frc" + str(b1)
    TBAMatchJson["alliances"]["red"]["team_keys"][0] = "frc" + str(r1)
    TBAMatchJson["alliances"]["blue"]["team_keys"][1] = "frc" + str(b2)
    TBAMatchJson["alliances"]["red"]["team_keys"][1] = "frc" + str(r2)
    TBAMatchJson["alliances"]["blue"]["team_keys"][2] = "frc" + str(b3)
    TBAMatchJson["alliances"]["red"]["team_keys"][2] = "frc" + str(r3)
    TBAMatchJson["key"] = "2023fake_qm" + str(matchNumber)
    TBAMatchJson["match_number"] = matchNumber
    for robot in robots:
        if robot.getTeam() == r1:
            matchRobots[0] = robot
        elif robot.getTeam() == r2:
            matchRobots[1] = robot
        elif robot.getTeam() == r3:
            matchRobots[2] = robot
        elif robot.getTeam() == b1:
            matchRobots[3] = robot
        elif robot.getTeam() == b2:
            matchRobots[4] = robot
        elif robot.getTeam() == b3:
            matchRobots[5] = robot
    blueBots = matchRobots[3:]
    redBots = matchRobots[:3]
    # Autonomous Docking
    autoDockRobots = dockingAutoRobots(matchRobots)
    allianceIdx = 0
    for string in autoDockRobots:
        if allianceIdx == 0:
            if string == "r1":
                dock = matchRobots[0].getAutoDock()
                if dock != 0:
                    TBAMatchJson["score_breakdown"]["red"][
                        "autoChargeStationRobot1"
                    ] = "Docked"
                    TBAMatchJson["score_breakdown"]["red"]["autoDocked"] = True
                if dock == 8:
                    TBAMatchJson["score_breakdown"]["red"][
                        "autoBridgeState"
                    ] = "NotLevel"
                TBAMatchJson["score_breakdown"]["red"]["autoChargeStationPoints"] = dock
            elif string == "r2":
                dock = matchRobots[1].getAutoDock()
                if dock != 0:
                    TBAMatchJson["score_breakdown"]["red"][
                        "autoChargeStationRobot2"
                    ] = "Docked"
                    TBAMatchJson["score_breakdown"]["red"]["autoDocked"] = True
                if dock == 8:
                    TBAMatchJson["score_breakdown"]["red"][
                        "autoBridgeState"
                    ] = "NotLevel"
                TBAMatchJson["score_breakdown"]["red"]["autoChargeStationPoints"] = dock
            elif string == "r3":
                dock = matchRobots[2].getAutoDock()
                if dock != 0:
                    TBAMatchJson["score_breakdown"]["red"][
                        "autoChargeStationRobot3"
                    ] = "Docked"
                    TBAMatchJson["score_breakdown"]["red"]["autoDocked"] = True
                if dock == 8:
                    TBAMatchJson["score_breakdown"]["red"][
                        "autoBridgeState"
                    ] = "NotLevel"
                TBAMatchJson["score_breakdown"]["red"]["autoChargeStationPoints"] = dock
        else:
            if string == "b1":
                dock = matchRobots[3].getAutoDock()
                if dock != 0:
                    TBAMatchJson["score_breakdown"]["blue"][
                        "autoChargeStationRobot1"
                    ] = "Docked"
                    TBAMatchJson["score_breakdown"]["blue"]["autoDocked"] = True
                if dock == 8:
                    TBAMatchJson["score_breakdown"]["blue"][
                        "autoBridgeState"
                    ] = "NotLevel"
                TBAMatchJson["score_breakdown"]["blue"][
                    "autoChargeStationPoints"
                ] = dock
            elif string == "b2":
                dock = matchRobots[4].getAutoDock()
                if dock != 0:
                    TBAMatchJson["score_breakdown"]["blue"][
                        "autoChargeStationRobot2"
                    ] = "Docked"
                    TBAMatchJson["score_breakdown"]["blue"]["autoDocked"] = True
                if dock == 8:
                    TBAMatchJson["score_breakdown"]["blue"][
                        "autoBridgeState"
                    ] = "NotLevel"
                TBAMatchJson["score_breakdown"]["blue"][
                    "autoChargeStationPoints"
                ] = dock
            elif string == "b3":
                dock = matchRobots[5].getAutoDock()
                if dock != 0:
                    TBAMatchJson["score_breakdown"]["blue"][
                        "autoChargeStationRobot3"
                    ] = "Docked"
                    TBAMatchJson["score_breakdown"]["blue"]["autoDocked"] = True
                if dock == 8:
                    TBAMatchJson["score_breakdown"]["blue"][
                        "autoBridgeState"
                    ] = "NotLevel"
                TBAMatchJson["score_breakdown"]["blue"][
                    "autoChargeStationPoints"
                ] = dock
        allianceIdx += 1
    # Auto Scoring
    if autoDockRobots[1][-1] == "1":
        blueAutoDockIdx = 0
    elif autoDockRobots[1][-1] == "2":
        blueAutoDockIdx = 2
    else:
        blueAutoDockIdx = 3
    blueScoring = getAutoPlacements(blueBots, blueAutoDockIdx, "blue")
    if autoDockRobots[0][-1] == "1":
        redAutoDockIdx = 0
    elif autoDockRobots[0][-1] == "2":
        redAutoDockIdx = 2
    else:
        redAutoDockIdx = 3
    redScoring = getAutoPlacements(redBots, redAutoDockIdx, "red")
    TBAMatchesJson.append(TBAMatchJson)
# print(TBAMatchesJson)
TBAOutput = open("TBAOutput.json", "w")
json.dump(TBAMatchesJson, TBAOutput, cls=NpEncoder)
