import csv
import json
from numpy import *
from Robot import *

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
    matchJson = json.load(matchJSONFile)
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
    matchJson["alliances"]["blue"]["team_keys"][0] = b1
    matchJson["alliances"]["red"]["team_keys"][0] = r1
    matchJson["alliances"]["blue"]["team_keys"][1] = b2
    matchJson["alliances"]["red"]["team_keys"][1] = r2
    matchJson["alliances"]["blue"]["team_keys"][2] = b3
    matchJson["alliances"]["red"]["team_keys"][2] = r3
    matchNumber = row["Match Number"]
    matchJson["key"] = "2023fake_qm"+matchNumber
    matchJson["match_number"] = matchNumber
    scoreBreakdown = matchJson["score_breakdown"]
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
    # Autonomous Docking
    autoDockRobots = dockingAutoRobots(matchRobots)
    allianceIdx = 0
    for string in autoDockRobots:
        if allianceIdx == 0:
            if string == "r1":
                if (matchRobots[0].getAutoDock() != 0):
                    scoreBreakdown["red"]["autoChargeStationRobot1"] = "Docked"
                    scoreBreakdown["red"]["autoDocked"] = False
                if (matchRobots[0].getAutoDock()  == 8):
                    scoreBreakdown["red"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["red"]["autoChargeStationPoints"] = matchRobots[0].getAutoDock()
            elif string == "r2":
                if (matchRobots[1].getAutoDock() != 0):
                    scoreBreakdown["red"]["autoChargeStationRobot2"] = "Docked"
                    scoreBreakdown["red"]["autoDocked"] = False
                if (matchRobots[1].getAutoDock()  == 8):
                    scoreBreakdown["red"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["red"]["autoChargeStationPoints"] = matchRobots[1].getAutoDock()
            elif string == "r3":
                if (matchRobots[2].getAutoDock() != 0):
                    scoreBreakdown["red"]["autoChargeStationRobot3"] = "Docked"
                    scoreBreakdown["red"]["autoDocked"] = False
                if (matchRobots[2].getAutoDock()  == 8):
                    scoreBreakdown["red"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["red"]["autoChargeStationPoints"] = matchRobots[2].getAutoDock()
        else:
            if string == "b1":
                if (matchRobots[3].getAutoDock() != 0):
                    scoreBreakdown["blue"]["autoChargeStationRobot1"] = "Docked"
                    scoreBreakdown["blue"]["autoDocked"] = False
                if (matchRobots[3].getAutoDock()  == 8):
                    scoreBreakdown["blue"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["blue"]["autoChargeStationPoints"] = matchRobots[3].getAutoDock()
            elif string == "b2":
                if (matchRobots[4].getAutoDock() != 0):
                    scoreBreakdown["blue"]["autoChargeStationRobot2"] = "Docked"
                    scoreBreakdown["blue"]["autoDocked"] = False
                if (matchRobots[4].getAutoDock()  == 8):
                    scoreBreakdown["blue"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["blue"]["autoChargeStationPoints"] = matchRobots[4].getAutoDock()
            elif string == "b3":
                if (matchRobots[5].getAutoDock() != 0):
                    scoreBreakdown["blue"]["autoChargeStationRobot3"] = "Docked"
                    scoreBreakdown["blue"]["autoDocked"] = False
                if (matchRobots[5].getAutoDock()  == 8):
                    scoreBreakdown["blue"]["autoBridgeState"] = "NotLevel"
                scoreBreakdown["blue"]["autoChargeStationPoints"] = matchRobots[5].getAutoDock()
    