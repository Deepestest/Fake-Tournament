import random
from typing import Any
import csv
import json
class Robot:
    def __init__(self, HCO, HCOV, HCU, HCUV, MCO, MCOV, MCU, MCUV, LP, LPV):
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

class LowCube(Robot):
    def __init__(self):
        Robot.__init__(self, 0, 0, 0, 0, 0, 0, 0, 0, 5, 2)

class Cube(Robot):
    def __init__(self):
        Robot.__init__(self, 0, 0, 1, 1, 0, 0, 1, 1, 5, 2)

class BadCone(Robot):
    def __init__(self):
        Robot.__init__(self, 2, 2, 0, 0, 3, 1, 0, 0, 0, 2)

class GoodCone(Robot):
    def __init__(self):
        Robot.__init__(self, 5, 1, 0, 0, 4, 1, 0, 0, 0, 2)

class GodBot(Robot):
    def __init__(self):
        Robot.__init__(self, 4, 1, 2, 1, 2, 1, 1, 1, 2, 2)

class NoHigh(Robot):
    def __init__(self):
        Robot.__init__(self, 0, 0, 0, 0, 4, 1, 2, 1, 2, 2)

class NoHighCones(Robot):
    def __init__(self):
        Robot.__init__(self, 0, 0, 2, 1, 3, 1, 1, 1, 2, 2)

class DefenseBot(Robot):
    def __init__(self):
        Robot.__init__(self, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2)

class Okay(Robot):
    def __init__(self):
        Robot.__init__(self, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2)

class Bad(Robot):
    def __init__(self):
        Robot.__init__(self, 0, 1, 0, 1, 0, 1, 0, 1, 3, 2)
def randomRobot() -> Robot:
    num = random.randint(1, 10)
    match num:
        case 1:
            return LowCube
        case 2:
            return Cube
        case 3:
            return BadCone
        case 4:
            return GoodCone
        case 5:
            return GodBot
        case 6:
            return NoHigh
        case 7:
            return NoHighCones
        case 8:
            return DefenseBot
        case 9:
            return Okay
        case 10:
            return Bad

with open("Teams.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    numTeams = 0
    for row in reader:
        numTeams+=1
    robots = Robot[numTeams]
    for row in reader:
        team = row['Team']
        robots[team] = randomRobot()
matchesJson = []
with open("Matches.csv", newline='') as csvfile:
    matchReader = csv.DictReader(csvfile)
numMatches = 0
for row in matchReader:
    numMatches+=1
for row in matchReader:
    matchJson = {
        "actual_time": 1697410390,
        "alliances": {
            "blue": {
                "dq_team_keys": [],
                "score": 153,
                "surrogate_team_keys": [],
                "team_keys": [
                    "frc1410",
                    "frc4944",
                    "frc9992"
                ]
            },
            "red": {
                "dq_team_keys": [],
                "score": 181,
                "surrogate_team_keys": [],
                "team_keys": [
                    "frc1619",
                    "frc3374",    
                    "frc4499"
                ]
            }
        },
        "comp_level": "f",
        "event_key": "2023cokc",
        "key": "2023cokc_f1m1",
        "match_number": 1,
        "post_result_time": 1697410681,
        "predicted_time": 1697410635,
        "score_breakdown": {
            "blue": {
                "activationBonusAchieved": false,
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