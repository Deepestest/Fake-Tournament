import random
from typing import Any
import csv
import json
class Robot:
    def __init__(self, team, HCO, HCOV, HCU, HCUV, MCO, MCOV, MCU, MCUV, LP, LPV):
        self.HCO = HCO
        self.HCOV = HCOV
        self.HCU = HCU
        self.HCUV = HCUV
        self.MCO = MCO
        self.MCOV = MCOV
        self.MCU = MCU
        self.MCUV = MCUV
        self.LP = LP
        self.LPV = LPV
        self.team = team
    def getTeam(self) -> int:
        return self.team
    def getHCO(self) -> int:
        return self.HCO
    def getHCOV(self) -> int:
        return self.HCOV
    def getHCU(self) -> int:
        return self.HCU
    def getHCUV(self) -> int:
        return self.HCUV
    def getMCO(self) -> int:
        return self.MCO
    def getMCOV(self) -> int:
        return self.MCOV
    def getMCU(self) -> int:
        return self.MCU
    def getMCUV(self) -> int:
        return self.MCUV
    def getLP(self) -> int:
        return self.LP
    def getLPV(self) -> int:
        return self.LPV

class LowCube(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 0, 0, 0, 0, 0, 0, 0, 0, 5, 2)

class Cube(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 0, 0, 1, 1, 0, 0, 1, 1, 5, 2)

class BadCone(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 2, 2, 0, 0, 3, 1, 0, 0, 0, 2)

class GoodCone(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 5, 1, 0, 0, 4, 1, 0, 0, 0, 2)

class GodBot(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 4, 1, 2, 1, 2, 1, 1, 1, 2, 2)

class NoHigh(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 0, 0, 0, 0, 4, 1, 2, 1, 2, 2)

class NoHighCones(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 0, 0, 2, 1, 3, 1, 1, 1, 2, 2)

class DefenseBot(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2)

class Okay(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2)

class Bad(Robot):
    def __init__(self, team:int):
        Robot.__init__(self, team, 0, 1, 0, 1, 0, 1, 0, 1, 3, 2)

def randomRobot(team:int) -> Robot:
    num = random.randint(1, 10)
    match num:
        case 1:
            return LowCube(team)
        case 2:
            return Cube(team)
        case 3:
            return BadCone(team)
        case 4:
            return GoodCone(team)
        case 5:
            return GodBot(team)
        case 6:
            return NoHigh(team)
        case 7:
            return NoHighCones(team)
        case 8:
            return DefenseBot(team)
        case 9:
            return Okay(team)
        case 10:
            return Bad(team)

with open("Teams.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    numTeams = 0
    for row in reader:
        numTeams+=1
    robots = Robot[numTeams]
    teamNumber = 0
    for row in reader:
        team = row['Team']
        robots[teamNumber] = randomRobot(team)
        teamNumber +=1
matchesJson = []
with open("Matches.csv", newline='') as csvfile:
    matchReader = csv.DictReader(csvfile)
numMatches = 0
for row in matchReader:
    numMatches+=1
for row in matchReader:
    matchRobots = Robot[6]
    r1 = row["R1"]
    r2 = row["R2"]
    r3 = row["R3"]
    b1 = row["B1"]
    b2 = row["B2"]
    b3 = row["B3"]
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
    matchNumber = row["Match Number"]
    matchJson = {
        "actual_time": 0,
        "alliances": {
            "blue": {
                "dq_team_keys": [],
                "score": 153,
                "surrogate_team_keys": [],
                "team_keys": [
                    "frc"+b1,
                    "frc"+b2,
                    "frc"+b3
                ]
            },
            "red": {
                "dq_team_keys": [],
                "score": 181,
                "surrogate_team_keys": [],
                "team_keys": [
                    "frc"+r1,
                    "frc"+r2,    
                    "frc"+r3
                ]
            }
        },
        "comp_level": "f",
        "event_key": "2023fake",
        "key": "2023fake_f1m"+matchNumber,
        "match_number": matchNumber,
        "post_result_time": 0,
        "predicted_time": 0,
        "score_breakdown": {
            "blue": {
                "activationBonusAchieved": False,
                "adjustPoints": 0,
                "autoBridgeState": "Level",
                "autoChargeStationPoints": 12,
                "autoChargeStationRobot1": "None",
                "autoChargeStationRobot2": "Docked",
                "autoChargeStationRobot3": "None",
                "autoCommunity": {
                    "B": [
                        "Cube",
                        "None",
                        "None",
                        "None",
                        "None",
                        "None",
                        "None",
                        "None",
                        "None"
                    ],
                    "M": [
                        "None",
                        "None",
                        "None",
                        "None",         
                        "None",
                        "None",
                        "None",         
                        "None",
                        "None"
                    ],
                    "T": [
                        "None",
                        "None",
                        "None",
                        "None",
                        "None",
                        "None",
                        "None",
                        "None",
                        "Cone"
                    ]
                },
                "autoDocked": true,
                "autoGamePieceCount": 2,
                "autoGamePiecePoints": 9,
                "autoMobilityPoints": 6,
                "autoPoints": 27,
                "coopGamePieceCount": 7,
                "coopertitionCriteriaMet": false,
                "endGameBridgeState": "Level",
                "endGameChargeStationPoints": 30,
                "endGameChargeStationRobot1": "Docked",
                "endGameChargeStationRobot2": "Docked",
                "endGameChargeStationRobot3": "Docked",
                "endGameParkPoints": 0,
                "extraGamePieceCount": 0,
                "foulCount": 2,
                "foulPoints": 5,
                "g405Penalty": false,
                "h111Penalty": false,
                "linkPoints": 30,
                "links": [
                    {
                        "nodes": [
                            0,
                            1,
                            2
                        ],
                        "row": "Bottom"
                    },
                    {
                        "nodes": [
                            3,
                            4,
                            5
                        ],
            "row": "Bottom"
          },
          {
            "nodes": [
              6,
              7,
              8
            ],
            "row": "Bottom"
          },
          {
            "nodes": [
              6,
              7,
              8
            ],
            "row": "Mid"
          },
          {
            "nodes": [
              2,
              3,
              4
            ],
            "row": "Top"
          },
          {
            "nodes": [
              5,
              6,
              7
            ],
            "row": "Top"
          }
        ],
        "mobilityRobot1": "Yes",
        "mobilityRobot2": "No",
        "mobilityRobot3": "Yes",
        "rp": 0,
        "sustainabilityBonusAchieved": false,
        "techFoulCount": 0,
        "teleopCommunity": {
          "B": [
            "Cube",
            "Cube",
            "Cube",
            "Cube",
            "Cube",
            "Cube",
            "Cube",
            "Cube",
            "Cube"
          ],
          "M": [
            "None",
            "Cube",
            "None",
            "None",
            "Cube",
            "None",
            "Cone",
            "Cube",
            "Cone"
          ],
          "T": [
            "None",
            "None",
            "Cone",
            "Cone",
            "Cube",
            "Cone",
            "Cone",
            "Cube",
            "Cone"
          ]
        },
        "teleopGamePieceCount": 21,
        "teleopGamePiecePoints": 61,
        "teleopPoints": 91,
        "totalChargeStationPoints": 42,
        "totalPoints": 153
      },
      "red": {
        "activationBonusAchieved": false,
        "adjustPoints": 0,
        "autoBridgeState": "Level",
        "autoChargeStationPoints": 12,
        "autoChargeStationRobot1": "None",
        "autoChargeStationRobot2": "Docked",
        "autoChargeStationRobot3": "None",
        "autoCommunity": {
          "B": [
            "None",
            "None",
            "None",
            "None",
            "Cube",
            "None",
            "None",
            "None",
            "None"
          ],
          "M": [
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None"
          ],
          "T": [
            "Cone",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "Cone"
          ]
        },
        "autoDocked": true,
        "autoGamePieceCount": 3,
        "autoGamePiecePoints": 15,
        "autoMobilityPoints": 6,
        "autoPoints": 33,
        "coopGamePieceCount": 8,
        "coopertitionCriteriaMet": false,
        "endGameBridgeState": "Level",
        "endGameChargeStationPoints": 30,
        "endGameChargeStationRobot1": "Docked",
        "endGameChargeStationRobot2": "Docked",
        "endGameChargeStationRobot3": "Docked",
        "endGameParkPoints": 0,
        "extraGamePieceCount": 0,
        "foulCount": 1,
        "foulPoints": 10,
        "g405Penalty": false,
        "h111Penalty": false,
        "linkPoints": 35,
        "links": [
          {
            "nodes": [
              0,
              1,
              2
            ],
            "row": "Bottom"
          },
          {
            "nodes": [
              3,
              4,
              5
            ],
            "row": "Bottom"
          },
          {
            "nodes": [
              0,
              1,
              2
            ],
            "row": "Mid"
          },
          {
            "nodes": [
              4,
              5,
              6
            ],
            "row": "Mid"
          },
          {
            "nodes": [
              0,
              1,
              2
            ],
            "row": "Top"
          },
          {
            "nodes": [
              3,
              4,
              5
            ],
            "row": "Top"
          },
          {
            "nodes": [
              6,
              7,
              8
            ],
            "row": "Top"
          }
        ],
        "mobilityRobot1": "Yes",
        "mobilityRobot2": "No",
        "mobilityRobot3": "Yes",
        "rp": 0,
        "sustainabilityBonusAchieved": false,
        "techFoulCount": 0,
        "teleopCommunity": {
          "B": [
            "Cube",
            "Cube",
            "Cube",
            "Cube",
            "Cube",
            "Cube",
            "Cone",
            "None",
            "Cube"
          ],
          "M": [
            "Cone",
            "Cube",
            "Cone",
            "None",
            "Cube",
            "Cone",
            "Cone",
            "Cube",
            "Cone"
          ],
          "T": [
            "Cone",
            "Cube",
            "Cone",
            "Cone",
            "Cube",
            "Cone",
            "Cone",
            "Cube",
            "Cone"
          ]
        },
        "teleopGamePieceCount": 25,
        "teleopGamePiecePoints": 73,
        "teleopPoints": 103,
        "totalChargeStationPoints": 42,
        "totalPoints": 181
      }
    },
    "set_number": 1,
    "time": 1697408580,
    "videos": [],
        "winning_alliance": "red"
    }