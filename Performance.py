import csv
import json
from numpy import *
from Robot import *

def combinePlacements(placementList:list) -> list:
    retval = []
    for i in range(3):
        retval.append([])
        for j in range(9):
            retval[i].append("None")
    for placements in placementList:
        for i in range(len(placements)):
            for j in range(len(placements[0])):
                if (retval[i][j] == "None"):
                    retval[i][j] = placements[i][j]
                else:
                    rand = random.random()
                    if (rand < 0.5):
                        retval[i][j] = placements[i][j]
    return retval

def getAutoPlacements(bots:list, dockingBotIdx:int) -> list:
    retval = bots[0].getAutos().getMiddle().getPlacements()
    rand = random.random()
    feederBot  = (dockingBotIdx + 1) % 3
    if (rand < 0.5):
        bumpBot = feederBot
        feederBot += 1
        feederBot %= 3
    else:
        bumpBot = feederBot + 1
        bumpBot %= 3
    retval = combinePlacements([retval, bots[bumpBot].getAutos().getBump().getPlacements(), bots[feederBot].getAutos().getFeeder().getPlacements()])
    return retval

matchJSONFile = open("Match.json")
with open("Teams.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.dialect = csv.excel()
    numTeams = 0
    robots = []
    for row in reader:
        team = row['Team']
        robots.append(randomRobot(team))
        numTeams +=1
matchesJson = []
with open("Matches.csv", newline='') as csvfile:
    matchReader = csv.DictReader(csvfile)
    matchReader.dialect = csv.excel()
numMatches = 0
for row in matchReader:
    numMatches+=1
for row in matchReader:
    TBAMatchJson = json.load(matchJSONFile)
    ActualMatchJson = json.load()
    matchRobots = []
    for i in range(6):
        matchRobots.append(None)
    r1 = row["R1"]
    r2 = row["R2"]
    r3 = row["R3"]
    b1 = row["B1"]
    b2 = row["B2"]
    b3 = row["B3"]
    # Metadata
    TBAMatchJson["alliances"]["blue"]["team_keys"][0] = b1
    TBAMatchJson["alliances"]["red"]["team_keys"][0] = r1
    TBAMatchJson["alliances"]["blue"]["team_keys"][1] = b2
    TBAMatchJson["alliances"]["red"]["team_keys"][1] = r2
    TBAMatchJson["alliances"]["blue"]["team_keys"][2] = b3
    TBAMatchJson["alliances"]["red"]["team_keys"][2] = r3
    matchNumber = row["Match Number"]
    TBAMatchJson["key"] = "2023fake_qm"+matchNumber
    TBAMatchJson["match_number"] = matchNumber
    scoreBreakdown = TBAMatchJson["score_breakdown"]
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
                if (dock != 0):
                    scoreBreakdown["red"]["autoChargeStationRobot1"] = "Docked"
                    scoreBreakdown["red"]["autoDocked"] = True
                if (dock  == 8):
                    scoreBreakdown["red"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["red"]["autoChargeStationPoints"] = dock
            elif string == "r2":
                dock = matchRobots[1].getAutoDock()
                if (dock != 0):
                    scoreBreakdown["red"]["autoChargeStationRobot2"] = "Docked"
                    scoreBreakdown["red"]["autoDocked"] = True
                if (dock  == 8):
                    scoreBreakdown["red"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["red"]["autoChargeStationPoints"] = dock
            elif string == "r3":
                dock = matchRobots[2].getAutoDock()
                if (dock != 0):
                    scoreBreakdown["red"]["autoChargeStationRobot3"] = "Docked"
                    scoreBreakdown["red"]["autoDocked"] = True
                if (dock  == 8):
                    scoreBreakdown["red"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["red"]["autoChargeStationPoints"] = dock
        else:
            if string == "b1":
                dock = matchRobots[3].getAutoDock()
                if (dock != 0):
                    scoreBreakdown["blue"]["autoChargeStationRobot1"] = "Docked"
                    scoreBreakdown["blue"]["autoDocked"] = True
                if (dock  == 8):
                    scoreBreakdown["blue"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["blue"]["autoChargeStationPoints"] = dock
            elif string == "b2":
                dock = matchRobots[4].getAutoDock()
                if (dock != 0):
                    scoreBreakdown["blue"]["autoChargeStationRobot2"] = "Docked"
                    scoreBreakdown["blue"]["autoDocked"] = True
                if (dock  == 8):
                    scoreBreakdown["blue"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["blue"]["autoChargeStationPoints"] = dock
            elif string == "b3":
                dock = matchRobots[5].getAutoDock()
                if (dock != 0):
                    scoreBreakdown["blue"]["autoChargeStationRobot3"] = "Docked"
                    scoreBreakdown["blue"]["autoDocked"] = True
                if (dock  == 8):
                    scoreBreakdown["blue"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["blue"]["autoChargeStationPoints"] = dock
        allianceIdx += 1
    # Auto Scoring
    if autoDockRobots[1][-1] == '1':
        blueAutoDockIdx = 0
    elif autoDockRobots[1][-1] == '2':
        blueAutoDockIdx = 2
    else:
        blueAutoDockIdx = 3
    blueScoring = getAutoPlacements(blueBots, blueAutoDockIdx)
    if autoDockRobots[0][-1] == '1':
        redAutoDockIdx = 0
    elif autoDockRobots[0][-1] == '2':
        redAutoDockIdx = 2
    else:
        redAutoDockIdx = 3
    redScoring = getAutoPlacements(redBots, redAutoDockIdx)
    