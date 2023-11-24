import copy
import json
import random
import pandas as pd
from Performance import NpEncoder, getAutoPlacements, getLinks, getTeleopPlacements

from Robot import dockingAutoRobots, randomRobot
from Scout import getRandomScout


def simulateData(teamsCSV, matchCSV):
    numTeams = 0
    robots = []
    ActualMatchesJson = []
    TBAMatchesJson = []
    for team in teamsCSV["Team"]:
        robots.append(randomRobot(team))
        numTeams += 1
    numMatches = 0
    for matchNumber in matchCSV["Match Number"]:
        numMatches += 1
    for matchNumber in matchCSV["Match Number"]:
        matchJSONFile = open("Match.json")
        ActualMatchJson = json.load(matchJSONFile)
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
        ActualMatchJson["alliances"]["blue"]["team_keys"][0] = "frc" + str(b1)
        ActualMatchJson["alliances"]["red"]["team_keys"][0] = "frc" + str(r1)
        ActualMatchJson["alliances"]["blue"]["team_keys"][1] = "frc" + str(b2)
        ActualMatchJson["alliances"]["red"]["team_keys"][1] = "frc" + str(r2)
        ActualMatchJson["alliances"]["blue"]["team_keys"][2] = "frc" + str(b3)
        ActualMatchJson["alliances"]["red"]["team_keys"][2] = "frc" + str(r3)
        ActualMatchJson["key"] = "2023fake_qm" + str(matchNumber)
        ActualMatchJson["match_number"] = matchNumber
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
        redAutoDockPoints = 0
        blueAutoDockPoints = 0
        allianceIdx = 0
        for string in autoDockRobots:
            if allianceIdx == 0:
                if string == "r1":
                    dock = matchRobots[0].getAutoDock()
                    if dock != 0:
                        ActualMatchJson["score_breakdown"]["red"][
                            "autoChargeStationRobot1"
                        ] = "Docked"
                        ActualMatchJson["score_breakdown"]["red"]["autoDocked"] = True
                    if dock == 8:
                        ActualMatchJson["score_breakdown"]["red"][
                            "autoBridgeState"
                        ] = "NotLevel"
                    ActualMatchJson["score_breakdown"]["red"][
                        "autoChargeStationPoints"
                    ] = dock
                    redAutoDockPoints = dock
                elif string == "r2":
                    dock = matchRobots[1].getAutoDock()
                    if dock != 0:
                        ActualMatchJson["score_breakdown"]["red"][
                            "autoChargeStationRobot2"
                        ] = "Docked"
                        ActualMatchJson["score_breakdown"]["red"]["autoDocked"] = True
                    if dock == 8:
                        ActualMatchJson["score_breakdown"]["red"][
                            "autoBridgeState"
                        ] = "NotLevel"
                    ActualMatchJson["score_breakdown"]["red"][
                        "autoChargeStationPoints"
                    ] = dock
                    redAutoDockPoints = dock
                elif string == "r3":
                    dock = matchRobots[2].getAutoDock()
                    if dock != 0:
                        ActualMatchJson["score_breakdown"]["red"][
                            "autoChargeStationRobot3"
                        ] = "Docked"
                        ActualMatchJson["score_breakdown"]["red"]["autoDocked"] = True
                    if dock == 8:
                        ActualMatchJson["score_breakdown"]["red"][
                            "autoBridgeState"
                        ] = "NotLevel"
                    ActualMatchJson["score_breakdown"]["red"][
                        "autoChargeStationPoints"
                    ] = dock
                    redAutoDockPoints = dock
            else:
                if string == "b1":
                    dock = matchRobots[3].getAutoDock()
                    if dock != 0:
                        ActualMatchJson["score_breakdown"]["blue"][
                            "autoChargeStationRobot1"
                        ] = "Docked"
                        ActualMatchJson["score_breakdown"]["blue"]["autoDocked"] = True
                    if dock == 8:
                        ActualMatchJson["score_breakdown"]["blue"][
                            "autoBridgeState"
                        ] = "NotLevel"
                    ActualMatchJson["score_breakdown"]["blue"][
                        "autoChargeStationPoints"
                    ] = dock
                    blueAutoDockPoints = dock
                elif string == "b2":
                    dock = matchRobots[4].getAutoDock()
                    if dock != 0:
                        ActualMatchJson["score_breakdown"]["blue"][
                            "autoChargeStationRobot2"
                        ] = "Docked"
                        ActualMatchJson["score_breakdown"]["blue"]["autoDocked"] = True
                    if dock == 8:
                        ActualMatchJson["score_breakdown"]["blue"][
                            "autoBridgeState"
                        ] = "NotLevel"
                    ActualMatchJson["score_breakdown"]["blue"][
                        "autoChargeStationPoints"
                    ] = dock
                    blueAutoDockPoints = dock
                elif string == "b3":
                    dock = matchRobots[5].getAutoDock()
                    if dock != 0:
                        ActualMatchJson["score_breakdown"]["blue"][
                            "autoChargeStationRobot3"
                        ] = "Docked"
                        ActualMatchJson["score_breakdown"]["blue"]["autoDocked"] = True
                    if dock == 8:
                        ActualMatchJson["score_breakdown"]["blue"][
                            "autoBridgeState"
                        ] = "NotLevel"
                    ActualMatchJson["score_breakdown"]["blue"][
                        "autoChargeStationPoints"
                    ] = dock
                    blueAutoDockPoints = dock
            allianceIdx += 1

        # Teleop Docking
        redTeleDockingAttempts = []
        redTeleDocking = []
        redEndgameLevel = "Level"
        redTeleDockPoints = 0
        redParkingPoints = 0
        blueTeleDockingAttempts = []
        blueTeleDocking = []
        blueEndgameLevel = "Level"
        blueTeleDockPoints = 0
        blueParkingPoints = 0
        for i in range(3):
            redTeleDocking.append(redBots[i].engaged())
            blueTeleDocking.append(blueBots[i].engaged())
            redTeleDockingAttempts.append(redBots[i].attemptedDock())
            blueTeleDockingAttempts.append(blueBots[i].attemptedDock())
            if redTeleDockingAttempts[i]:
                ActualMatchJson["score_breakdown"]["red"][
                    "endGameChargeStationRobot" + str(i + 1)
                ] = "Docked"
                if not redTeleDocking[i]:
                    redEndgameLevel = "NotLevel"
            else:
                rand = random.random()
                if rand < 0.5:
                    ActualMatchJson["score_breakdown"]["red"][
                        "endGameChargeStationRobot" + str(i + 1)
                    ] = "Park"
                    redParkingPoints += 2
            if blueTeleDockingAttempts[i]:
                ActualMatchJson["score_breakdown"]["blue"][
                    "endGameChargeStationRobot" + str(i + 1)
                ] = "Docked"
                if not blueTeleDocking[i]:
                    blueEndgameLevel = "NotLevel"
            else:
                rand = random.random()
                if rand < 0.5:
                    ActualMatchJson["score_breakdown"]["blue"][
                        "endGameChargeStationRobot" + str(i + 1)
                    ] = "Park"
                    blueParkingPoints += 2
        for i in range(3):
            if redTeleDockingAttempts[i]:
                if redEndgameLevel == "NotLevel":
                    redTeleDockPoints += 6
                else:
                    redTeleDockPoints += 10
            if blueTeleDockingAttempts[i]:
                if blueEndgameLevel == "NotLevel":
                    blueTeleDockPoints += 6
                else:
                    blueTeleDockPoints += 10
        ActualMatchJson["score_breakdown"]["red"][
            "endGameChargeStationPoints"
        ] = redTeleDockPoints
        ActualMatchJson["score_breakdown"]["red"][
            "endGameBridgeState"
        ] = redEndgameLevel
        ActualMatchJson["score_breakdown"]["red"][
            "endGameParkPoints"
        ] = redParkingPoints
        ActualMatchJson["score_breakdown"]["blue"][
            "endGameChargeStationPoints"
        ] = blueTeleDockPoints
        ActualMatchJson["score_breakdown"]["blue"][
            "endGameBridgeState"
        ] = blueEndgameLevel
        ActualMatchJson["score_breakdown"]["blue"][
            "endGameParkPoints"
        ] = blueParkingPoints
        blueEndgamePoints = blueTeleDockPoints + blueParkingPoints
        redEndgamePoints = redTeleDockPoints + redParkingPoints

        # Auto Scoring
        if autoDockRobots[1][-1] == "1":
            blueAutoDockIdx = 0
        elif autoDockRobots[1][-1] == "2":
            blueAutoDockIdx = 2
        else:
            blueAutoDockIdx = 3
        blueAutoScoring = getAutoPlacements(blueBots, blueAutoDockIdx, "blue")
        blueAutoPlacements = blueAutoScoring["Placements"]
        blueAutoMobility = blueAutoScoring["Mobility"]
        if autoDockRobots[0][-1] == "1":
            redAutoDockIdx = 0
        elif autoDockRobots[0][-1] == "2":
            redAutoDockIdx = 2
        else:
            redAutoDockIdx = 3
        redAutoScoring = getAutoPlacements(redBots, redAutoDockIdx, "red")
        redAutoPlacements = redAutoScoring["Placements"]
        redAutoMobility = redAutoScoring["Mobility"]
        ActualMatchJson["score_breakdown"]["blue"]["autoCommunity"][
            "B"
        ] = blueAutoPlacements[0]
        ActualMatchJson["score_breakdown"]["blue"]["autoCommunity"][
            "M"
        ] = blueAutoPlacements[1]
        ActualMatchJson["score_breakdown"]["blue"]["autoCommunity"][
            "T"
        ] = blueAutoPlacements[2]
        ActualMatchJson["score_breakdown"]["red"]["autoCommunity"][
            "B"
        ] = redAutoPlacements[0]
        ActualMatchJson["score_breakdown"]["red"]["autoCommunity"][
            "M"
        ] = redAutoPlacements[1]
        ActualMatchJson["score_breakdown"]["red"]["autoCommunity"][
            "T"
        ] = redAutoPlacements[2]
        redAutoGamePieceCount = 0
        redAutoGamePiecePoints = 0
        blueAutoGamePieceCount = 0
        blueAutoGamePiecePoints = 0
        for row in range(len(redAutoPlacements)):
            for spot in range(len(redAutoPlacements[row])):
                if not (redAutoPlacements[row][spot][:4] == "None"):
                    redAutoGamePieceCount += 1
                    match row:
                        case 0:
                            redAutoGamePiecePoints += 3
                        case 1:
                            redAutoGamePiecePoints += 4
                        case 2:
                            redAutoGamePiecePoints += 6
                if not (blueAutoPlacements[row][spot][:4] == "None"):
                    blueAutoGamePieceCount += 1
                    match row:
                        case 0:
                            blueAutoGamePiecePoints += 3
                        case 1:
                            blueAutoGamePiecePoints += 4
                        case 2:
                            blueAutoGamePiecePoints += 6
        ActualMatchJson["score_breakdown"]["blue"][
            "autoGamePieceCount"
        ] = blueAutoGamePieceCount
        ActualMatchJson["score_breakdown"]["blue"][
            "autoGamePiecePoints"
        ] = blueAutoGamePiecePoints
        ActualMatchJson["score_breakdown"]["red"][
            "autoGamePieceCount"
        ] = redAutoGamePieceCount
        ActualMatchJson["score_breakdown"]["red"][
            "autoGamePiecePoints"
        ] = redAutoGamePiecePoints

        # Mobility
        redMobilityPoints = 0
        blueMobilityPoints = 0
        for i in range(len(redAutoMobility)):
            redMobilityPoints += redAutoMobility[i]
            if redAutoMobility[i] == 3:
                ActualMatchJson["score_breakdown"]["red"][
                    "mobilityRobot" + str(i + 1)
                ] = "Yes"
            else:
                ActualMatchJson["score_breakdown"]["red"][
                    "mobilityRobot" + str(i + 1)
                ] = "No"
            blueMobilityPoints += blueAutoMobility[i]
            if blueAutoMobility[i] == 3:
                ActualMatchJson["score_breakdown"]["blue"][
                    "mobilityRobot" + str(i + 1)
                ] = "Yes"
            else:
                ActualMatchJson["score_breakdown"]["blue"][
                    "mobilityRobot" + str(i + 1)
                ] = "No"
        ActualMatchJson["score_breakdown"]["blue"][
            "autoMobilityPoints"
        ] = blueMobilityPoints
        ActualMatchJson["score_breakdown"]["red"][
            "autoMobilityPoints"
        ] = redMobilityPoints

        # Teleop Scoring
        blueTeleopScoring = getTeleopPlacements(blueBots, blueAutoPlacements, "blue")
        redTeleopScoring = getTeleopPlacements(redBots, redAutoPlacements, "red")
        ActualMatchJson["score_breakdown"]["blue"]["teleopCommunity"][
            "B"
        ] = blueTeleopScoring[0]
        ActualMatchJson["score_breakdown"]["blue"]["teleopCommunity"][
            "M"
        ] = blueTeleopScoring[1]
        ActualMatchJson["score_breakdown"]["blue"]["teleopCommunity"][
            "T"
        ] = blueTeleopScoring[2]
        ActualMatchJson["score_breakdown"]["red"]["teleopCommunity"][
            "B"
        ] = redTeleopScoring[0]
        ActualMatchJson["score_breakdown"]["red"]["teleopCommunity"][
            "M"
        ] = redTeleopScoring[1]
        ActualMatchJson["score_breakdown"]["red"]["teleopCommunity"][
            "T"
        ] = redTeleopScoring[2]
        redGamePieceCount = 0
        redGamePiecePoints = 0
        blueGamePieceCount = 0
        blueGamePiecePoints = 0
        for row in range(len(redTeleopScoring)):
            for spot in range(len(redTeleopScoring[row])):
                if not (redTeleopScoring[row][spot][:4] == "None"):
                    redGamePieceCount += 1
                    match row:
                        case 0:
                            redGamePiecePoints += 3
                        case 1:
                            redGamePiecePoints += 4
                        case 2:
                            redGamePiecePoints += 6
                if not (blueTeleopScoring[row][spot][:4] == "None"):
                    blueGamePieceCount += 1
                    match row:
                        case 0:
                            blueGamePiecePoints += 3
                        case 1:
                            blueGamePiecePoints += 4
                        case 2:
                            blueGamePiecePoints += 6
        redGamePiecePoints -= redAutoGamePiecePoints
        redAutoGamePiecePoints += redAutoGamePieceCount
        blueGamePiecePoints -= blueAutoGamePiecePoints
        blueAutoGamePiecePoints += blueAutoGamePieceCount
        ActualMatchJson["score_breakdown"]["blue"][
            "teleopGamePieceCount"
        ] = blueGamePieceCount
        ActualMatchJson["score_breakdown"]["blue"][
            "teleopGamePiecePoints"
        ] = blueGamePiecePoints
        ActualMatchJson["score_breakdown"]["red"][
            "teleopGamePieceCount"
        ] = redGamePieceCount
        ActualMatchJson["score_breakdown"]["red"][
            "teleopGamePiecePoints"
        ] = redGamePiecePoints

        # Cooperatition Bonus
        redCooperatitionPieceCount = 0
        for row in redTeleopScoring:
            for i in range(3):
                if not (row[i + 3][:4] == "None"):
                    redCooperatitionPieceCount += 1
        blueCooperatitionPieceCount = 0
        for row in blueTeleopScoring:
            for i in range(3):
                if not (row[i + 3][:4] == "None"):
                    blueCooperatitionPieceCount += 1
        redCooperatitionMet = False
        if redCooperatitionPieceCount >= 3:
            redCooperatitionMet = True
        blueCooperatitionMet = False
        if blueCooperatitionPieceCount >= 3:
            blueCooperatitionMet = True
        cooperatitionBonus = redCooperatitionMet & blueCooperatitionMet
        ActualMatchJson["score_breakdown"]["red"][
            "coopGamePieceCount"
        ] = redCooperatitionPieceCount
        ActualMatchJson["score_breakdown"]["red"][
            "coopertitionCriteriaMet"
        ] = redCooperatitionMet
        ActualMatchJson["score_breakdown"]["blue"][
            "coopGamePieceCount"
        ] = blueCooperatitionPieceCount
        ActualMatchJson["score_breakdown"]["blue"][
            "coopertitionCriteriaMet"
        ] = blueCooperatitionMet

        # Links
        redLinks = getLinks(redTeleopScoring)
        ActualMatchJson["score_breakdown"]["red"]["links"] = redLinks
        redLinkPoints = 0
        for link in redLinks:
            redLinkPoints += 5
        ActualMatchJson["score_breakdown"]["red"]["linkPoints"] = redLinkPoints
        blueLinks = getLinks(blueTeleopScoring)
        ActualMatchJson["score_breakdown"]["blue"]["links"] = blueLinks
        blueLinkPoints = 0
        for link in blueLinks:
            blueLinkPoints += 5
        ActualMatchJson["score_breakdown"]["blue"]["linkPoints"] = blueLinkPoints

        # Points
        redAutoPoints = redAutoGamePiecePoints + redAutoDockPoints + redMobilityPoints
        blueAutoPoints = (
            blueAutoGamePiecePoints + blueAutoDockPoints + blueMobilityPoints
        )
        redTeleopPoints = redGamePiecePoints + redLinkPoints + redEndgamePoints
        blueTeleopPoints = blueGamePiecePoints + blueLinkPoints + blueEndgamePoints
        redChargeStationPoints = redAutoDockPoints + redTeleDockPoints
        blueChargeStationPoints = blueAutoDockPoints + blueTeleDockPoints
        blueTotalPoints = blueAutoPoints + blueTeleopPoints
        redTotalPoints = redAutoPoints + redTeleopPoints
        blueRPs = 0
        redRPs = 0
        winningAlliance = "None"
        if blueTotalPoints > redTotalPoints:
            blueRPs += 2
            winningAlliance = "blue"
        elif blueTotalPoints < redTotalPoints:
            redRPs += 2
            winningAlliance = "red"
        else:
            redRPs += 1
            blueRPs += 1
        redActivationBonus = False
        if redChargeStationPoints > 26:
            redActivationBonus = True
            redRPs += 1
        blueActivationBonus = False
        if blueChargeStationPoints > 26:
            blueActivationBonus = True
            blueRPs += 1
        redSustainablilityBonus = False
        if len(redLinks) == 5:
            if cooperatitionBonus:
                redSustainablilityBonus = True
        elif len(redLinks) > 5:
            redSustainablilityBonus = True
        blueSustainablilityBonus = False
        if len(blueLinks) == 5:
            if cooperatitionBonus:
                blueSustainablilityBonus = True
        elif len(blueLinks) > 5:
            blueSustainablilityBonus = True
        if redSustainablilityBonus:
            redRPs += 1
        if blueSustainablilityBonus:
            blueRPs += 1
        ActualMatchJson["alliances"]["blue"]["score"] = blueTotalPoints
        ActualMatchJson["score_breakdown"]["blue"]["autoPoints"] = blueAutoPoints
        ActualMatchJson["score_breakdown"]["blue"]["teleopPoints"] = blueTeleopPoints
        ActualMatchJson["score_breakdown"]["blue"][
            "totalChargeStationPoints"
        ] = blueChargeStationPoints
        ActualMatchJson["score_breakdown"]["blue"]["totalPoints"] = blueTotalPoints
        ActualMatchJson["score_breakdown"]["blue"][
            "sustainabilityBonusAchieved"
        ] = blueSustainablilityBonus
        ActualMatchJson["score_breakdown"]["blue"][
            "activationBonusAchieved"
        ] = blueActivationBonus
        ActualMatchJson["score_breakdown"]["blue"]["rp"] = blueRPs
        ActualMatchJson["alliances"]["red"]["score"] = redTotalPoints
        ActualMatchJson["score_breakdown"]["red"]["autoPoints"] = redAutoPoints
        ActualMatchJson["score_breakdown"]["red"]["teleopPoints"] = redTeleopPoints
        ActualMatchJson["score_breakdown"]["red"][
            "totalChargeStationPoints"
        ] = redChargeStationPoints
        ActualMatchJson["score_breakdown"]["red"]["totalPoints"] = redTotalPoints
        ActualMatchJson["score_breakdown"]["red"][
            "sustainabilityBonusAchieved"
        ] = redSustainablilityBonus
        ActualMatchJson["score_breakdown"]["red"][
            "activationBonusAchieved"
        ] = redActivationBonus
        ActualMatchJson["score_breakdown"]["red"]["rp"] = redRPs
        ActualMatchJson["winning_alliance"] = winningAlliance

        # Make Blue Alliance Data
        TBAMatchJson = copy.deepcopy(ActualMatchJson)

        # Scoring Without Team who scored each piece for TBA
        TBAMatchJson["score_breakdown"]["blue"]["autoCommunity"]["B"] = [
            i[:4] for i in blueAutoPlacements[0]
        ]
        TBAMatchJson["score_breakdown"]["blue"]["autoCommunity"]["M"] = [
            i[:4] for i in blueAutoPlacements[1]
        ]
        TBAMatchJson["score_breakdown"]["blue"]["autoCommunity"]["T"] = [
            i[:4] for i in blueAutoPlacements[2]
        ]
        TBAMatchJson["score_breakdown"]["red"]["autoCommunity"]["B"] = [
            i[:4] for i in redAutoPlacements[0]
        ]
        TBAMatchJson["score_breakdown"]["red"]["autoCommunity"]["M"] = [
            i[:4] for i in redAutoPlacements[1]
        ]
        TBAMatchJson["score_breakdown"]["red"]["autoCommunity"]["T"] = [
            i[:4] for i in redAutoPlacements[2]
        ]
        TBAMatchJson["score_breakdown"]["blue"]["teleopCommunity"]["B"] = [
            i[:4] for i in blueTeleopScoring[0]
        ]
        TBAMatchJson["score_breakdown"]["blue"]["teleopCommunity"]["M"] = [
            i[:4] for i in blueTeleopScoring[1]
        ]
        TBAMatchJson["score_breakdown"]["blue"]["teleopCommunity"]["T"] = [
            i[:4] for i in blueTeleopScoring[2]
        ]
        TBAMatchJson["score_breakdown"]["red"]["teleopCommunity"]["B"] = [
            i[:4] for i in redTeleopScoring[0]
        ]
        TBAMatchJson["score_breakdown"]["red"]["teleopCommunity"]["M"] = [
            i[:4] for i in redTeleopScoring[1]
        ]
        TBAMatchJson["score_breakdown"]["red"]["teleopCommunity"]["T"] = [
            i[:4] for i in redTeleopScoring[2]
        ]

        # Append Match Data
        ActualMatchesJson.append(ActualMatchJson)
        TBAMatchesJson.append(TBAMatchJson)

    # Dump Data to Files
    # output = open("Output.json", "w")
    # TBAOutput = open("TBAOutput.json", "w")

    # Now Do Scouting Data
    scouts = []
    scoutIdx = 0
    foundTeams = 0
    scoutingTeams = []
    while foundTeams < 4:
        team = random.choice(teamsCSV["Team"])
        if not scoutingTeams.__contains__(team):
            foundTeams += 1
            scoutingTeams.append(team)
    for team in scoutingTeams:
        for i in range(6):
            scouts.append(
                getRandomScout(
                    scoutIdx, team, str(scoutIdx) + "@" + str(team) + ".com", numMatches
                )
            )
            scoutIdx += 1
    driverStations = ["r1", "r2", "r3", "b1", "b2", "b3"]
    scoutingData = []
    for game in ActualMatchesJson:
        for i in range(len(scouts)):
            driverStation = random.choice(driverStations)
            scout = scouts[i]
            data = scout.scoutMatch(game, driverStation)
            if data is not None:
                scoutingData.append(data)
    # scoutingOutput = open("ScoutingOutput.json", "w")
    return [ActualMatchesJson, TBAMatchesJson, scoutingData]

