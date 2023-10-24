import random


class Auto:
    def __init__(self, placements : list, dockPercent : float, engagePercent : float, mobility : int):
        self.placements = placements
        self.dockPercent = dockPercent
        self.engagePercent = engagePercent
        self.mobility = mobility
    def getPlacements(self) -> list:
        return self.placements
    def getDockPercent(self) -> float:
        return self.dockPercent
    def getEngagePercent(self) -> float:
        return self.engagePercent
    def setDockPercent(self, percent:float):
        self.dockPercent = percent
    def setEngagePercent(self, percent:float):
        self.engagePercent = percent
class Autos:
    def __init__(self, feederAuto:Auto, middleAuto:Auto, bumpAuto:Auto):
        self.feederAuto = feederAuto
        self.middleAuto = middleAuto
        self.bumpAuto = bumpAuto
    def getFeeder(self) -> Auto:
        return self.feederAuto
    def getMiddle(self) -> Auto:
        return self.middleAuto
    def getBump(self) -> Auto:
        return self.bumpAuto
    
class NoAuto(Auto):
    def __init__(self):
        placements = []
        for rowIdx in range(3):
            placements.append([])
            for spotIdx in range(9):
                placements[rowIdx].append("None")
                spotIdx += 1
            rowIdx += 1
        Auto.__init__(self, placements, 0, 0, 0)

class OnePiece(Auto):
    def __init__(self, piece:list, rIdx:list, cIdx:list, dockPercent:list, engagePercent:list, mobility:list):
        placements = []
        for rowIdx in range(3):
            placements.append([])
            for spotIdx in range(9):
                placements[rowIdx].append("None")
                spotIdx += 1
            rowIdx += 1
        placements[rIdx][cIdx] = piece
        Auto.__init__(self, placements, dockPercent, engagePercent, mobility)

class TwoPiece(Auto):
    def __init__(self, piece:list, rIdx:list, cIdx:list, dockPercent:list, engagePercent:list):
        placements = []
        for rowIdx in range(3):
            placements.append([])
            for spotIdx in range(9):
                placements[rowIdx].append("None")
                spotIdx += 1
            rowIdx += 1
        for i in range(2):
            placements[rIdx[i]][cIdx[i]] = piece[i]
        Auto.__init__(self, placements, dockPercent, engagePercent, 3)

class ThreePiece(Auto):
    def __init__(self, piece:list, rIdx:list, cIdx:list, dockPercent:list, engagePercent:list):
        placements = []
        for rowIdx in range(3):
            placements.append([])
            for spotIdx in range(9):
                placements[rowIdx].append("None")
                spotIdx += 1
            rowIdx += 1
        for i in range(3):
            placements[rIdx[i]][cIdx[i]] = piece[i]
        Auto.__init__(self, placements, dockPercent, engagePercent, 3)

def getRandomAuto(autoList:list) -> Auto:
    rand = random.randint(0, len(autoList)-1)
    return autoList(rand)