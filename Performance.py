import copy
import random
import numpy as np
import json


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def getBlankPlacements() -> list:
    retval = []
    for i in range(3):
        retval.append([])
        for j in range(9):
            retval[i].append("None")
    return retval


def combinePlacements(placementList: list) -> list:
    retval = getBlankPlacements()
    for placements in placementList:
        for i in range(len(placements)):
            for j in range(len(placements[i])):
                if retval[i][j] == "None":
                    retval[i][j] = placements[i][j]
                else:
                    rand = random.random()
                    if rand < 0.5:
                        retval[i][j] = placements[i][j]
    return retval


def getAutoPlacements(bots: list, middleBot: int, alliance: str) -> dict:
    retval = {"Placements": [], "Mobility": []}
    retPlacements = (
        bots[0].getAutos().getMiddle().getPlacements(alliance, middleBot + 1)
    )
    rand = random.random()
    feederBot = (middleBot + 1) % 3
    if rand < 0.5:
        bumpBot = feederBot
        feederBot += 1
        feederBot %= 3
    else:
        bumpBot = feederBot + 1
        bumpBot %= 3
    retPlacements = combinePlacements(
        [
            retPlacements,
            bots[bumpBot].getAutos().getBump().getPlacements(alliance, bumpBot + 1),
            bots[feederBot]
            .getAutos()
            .getFeeder()
            .getPlacements(alliance, feederBot + 1),
        ]
    )
    for i in range(len(bots)):
        if i == bumpBot:
            retval["Mobility"].append(bots[i].getAutos().getBump().getMobilityPercent())
        elif i == middleBot:
            retval["Mobility"].append(
                bots[i].getAutos().getMiddle().getMobilityPercent()
            )
        else:
            retval["Mobility"].append(
                bots[i].getAutos().getFeeder().getMobilityPercent()
            )
    retval["Placements"] = retPlacements
    return retval


def getBlankNode(row: int, checkSpots: list, placements: list) -> list:
    retval = []
    exists = False
    found = False
    for spot in checkSpots:
        if placements[row][spot][:4] == "None":
            exists = True
            retval.append(row)
            break
    if not exists:
        retval.append(-1)
        retval.append(-1)
    if exists:
        while not found:
            rand = random.randint(0, (len(checkSpots) - 1))
            if placements[row][checkSpots[rand]][:4] == "None":
                found = True
                retval.append(checkSpots[rand])
                break
    return retval


def getBlankSpot(spotType: str, placements: list) -> list:
    retval = []
    match spotType:
        case "hco":
            retval = getBlankNode(2, [0, 2, 3, 5, 6, 8], placements)
        case "hcu":
            retval = getBlankNode(2, [1, 4, 7], placements)
        case "mco":
            retval = getBlankNode(1, [0, 2, 3, 5, 6, 8], placements)
        case "mcu":
            retval = getBlankNode(1, [1, 4, 7], placements)
        case "lco" | "lcu":
            retval = getBlankNode(0, [1, 2, 3, 4, 5, 6, 7, 8], placements)
    return retval


def getTeleopPlacements(bots: list, autoScoring: list, alliance: str) -> list:
    retval = copy.deepcopy(autoScoring)
    for botIdx in range(len(bots)):
        botPlacements = copy.deepcopy(retval)
        hco = bots[botIdx].getHCO()
        for i in range(hco):
            randSpot = getBlankSpot("hco", botPlacements)
            if randSpot is not None:
                botPlacements[randSpot[0]][randSpot[1]] = (
                    "Cone" + alliance[0] + str(botIdx + 1)
                )
        hcu = bots[botIdx].getHCU()
        for i in range(hcu):
            randSpot = getBlankSpot("hcu", botPlacements)
            if randSpot is not None:
                botPlacements[randSpot[0]][randSpot[1]] = (
                    "Cube" + alliance[0] + str(botIdx + 1)
                )
        mco = bots[botIdx].getMCO()
        for i in range(mco):
            randSpot = getBlankSpot("mco", botPlacements)
            if randSpot is not None:
                botPlacements[randSpot[0]][randSpot[1]] = (
                    "Cone" + alliance[0] + str(botIdx + 1)
                )
        mcu = bots[botIdx].getMCU()
        for i in range(mcu):
            randSpot = getBlankSpot("mcu", botPlacements)
            if randSpot is not None:
                botPlacements[randSpot[0]][randSpot[1]] = (
                    "Cube" + alliance[0] + str(botIdx + 1)
                )
        lco = bots[botIdx].getLCO()
        for i in range(lco):
            randSpot = getBlankSpot("lco", botPlacements)
            if randSpot is not None:
                botPlacements[randSpot[0]][randSpot[1]] = (
                    "Cone" + alliance[0] + str(botIdx + 1)
                )
        lcu = bots[botIdx].getLCU()
        for i in range(lcu):
            randSpot = getBlankSpot("lcu", botPlacements)
            if randSpot is not None:
                botPlacements[randSpot[0]][randSpot[1]] = (
                    "Cube" + alliance[0] + str(botIdx + 1)
                )
        retval = combinePlacements([retval, botPlacements])
    return retval


def getLinks(placements: list) -> list:
    retval = []
    linkList = []
    rowStr = ""
    linksBlankDict = {"nodes": [], "row": ""}
    piecesTogether = 0
    for row in range(len(placements)):
        piecesTogether = 0
        for spot in range(len(placements[row])):
            if placements[row][spot][:4] == "None":
                piecesTogether = 0
            else:
                piecesTogether += 1
                if piecesTogether == 1:
                    linkList = list()
                linkList.append(spot + 1)
                if piecesTogether == 3:
                    newDict = copy.deepcopy(linksBlankDict)
                    newDict["nodes"] = linkList
                    match row:
                        case 0:
                            rowStr = "Bottom"
                        case 1:
                            rowStr = "Mid"
                        case 2:
                            rowStr = "Top"
                    newDict["row"] = rowStr
                    piecesTogether = 0
                    retval.append(newDict)
    return retval
