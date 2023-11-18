import json
import random

class Scout:
    def __init__(
        self,
        maxMatches: int,
        errorPercent: float,
        name: str,
        team_number: int,
        email: str,
        numMatches: int,
    ):
        self.errorPercent = errorPercent
        self.name = name
        self.team_number = team_number
        self.email = email
        self.maxMatches = maxMatches
        self.scoutChance = maxMatches/numMatches
        self.scoutedMatches = 0
        self.canScout = True

    def scoutMatch(self, match: dict, driverStation: str) -> dict:
        if self.canScout:
            rand = random.random()
            if rand < self.scoutChance:
                dataOutlineFile = open("ScoutingDataOutline.json")
                retval = json.load(dataOutlineFile)
                teleopPieces = getPiecesScored(match, "teleopCommunity", driverStation)
                autoPieces = getPiecesScored(match, "autoCommunity", driverStation)
                retval["data"]["auto"]["hco"] = getErrorAdjustedPieces(
                    autoPieces[0], self.errorPercent, 6
                )
                retval["data"]["auto"]["hcu"] = getErrorAdjustedPieces(
                    autoPieces[1], self.errorPercent, 3
                )
                retval["data"]["auto"]["mco"] = getErrorAdjustedPieces(
                    autoPieces[2], self.errorPercent, 6
                )
                retval["data"]["auto"]["mcu"] = getErrorAdjustedPieces(
                    autoPieces[3], self.errorPercent, 3
                )
                retval["data"]["auto"]["lp"] = getErrorAdjustedPieces(
                    autoPieces[4], self.errorPercent, 9
                )
                retval["data"]["teleop"]["hco"] = getErrorAdjustedPieces(
                    teleopPieces[0], self.errorPercent, 6
                )
                retval["data"]["teleop"]["hcu"] = getErrorAdjustedPieces(
                    teleopPieces[1], self.errorPercent, 3
                )
                retval["data"]["teleop"]["mco"] = getErrorAdjustedPieces(
                    teleopPieces[2], self.errorPercent, 6
                )
                retval["data"]["teleop"]["mcu"] = getErrorAdjustedPieces(
                    teleopPieces[3], self.errorPercent, 3
                )
                retval["data"]["teleop"]["lp"] = getErrorAdjustedPieces(
                    teleopPieces[4], self.errorPercent, 9
                )
                if driverStation[0] == "r":
                    allianceStr = "red"
                else:
                    allianceStr = "blue"
                teamIdx = int(driverStation[1]) - 1
                retval["metadata"]["team_number"] = match["alliances"][allianceStr][
                    "team_keys"
                ][teamIdx][3:]
                retval["metadata"]["match_number"] = match["match_number"]
                retval["metadata"]["scout_info"]["email"] = self.email
                retval["metadata"]["scout_info"]["name"] = self.name
                retval["metadata"]["scout_info"]["team_number"] = self.team_number
                self.scoutedMatches += 1
                if self.scoutedMatches == self.maxMatches:
                    self.canScout = False
                return retval


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


def getErrorAdjustedPieces(numPieces: int, errorPercent: float, max: int) -> int:
    retval = numPieces
    # for i in range(numPieces):
    #     rand = random.random()
    #     if rand < errorPercent:
    #         rand = random.random()
    #         if rand < 0.5:
    #             retval += 1
    #         else:
    #             retval -= 1
    # rand = random.random()
    # if rand < 0.5:
    #     retval *= -1
    # if retval > max:
    #     retval = max
    # elif retval < 0:
    #     retval = 0
    return retval


class Vaclav(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(self, 30, 0.3, "Vaclav" + str(name), team_number, email, numMatches)


class Vishnu(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(self, 10, 0.25, "Vishnu" + str(name), team_number, email, numMatches)


class Dmitri(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(self, 100, 0.05, "Dmitri" + str(name), team_number, email, numMatches)


class Ivan(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(self, 100, 0.1, "Ivan" + str(name), team_number, email, numMatches)


class Adarsh(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(self, 1, 0.1, "Adarsh" + str(name), team_number, email, numMatches)


class Rishabh(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(
            self, 80, 0.15, ("Rishabh" + str(name)), team_number, email, numMatches
        )


class Ben(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(self, 80, 0.2, "Ben" + str(name), team_number, email, numMatches)


class Roarke(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(self, 80, 0.08, "Roarke" + str(name), team_number, email, numMatches)


class Deepesh(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(self, 80, 0.18, "Deepesh" + str(name), team_number, email, numMatches)


class Rwad(Scout):
    def __init__(self, name: str, team_number: int, email: str, numMatches: int):
        Scout.__init__(self, 40, 0.23, "Rwad" + str(name), team_number, email, numMatches)


def getRandomScout(name: str, team_number: int, email: str, matchCount: int) -> Scout:
    subclass_names = [
        "Vaclav",
        "Vishnu",
        "Dmitri",
        "Ivan",
        "Adarsh",
        "Rishabh",
        "Ben",
        "Roarke",
        "Deepesh",
        "Rwad",
    ]
    random_subclass_name = random.choice(subclass_names)
    match random_subclass_name:
        case "Vaclav":
            return Vaclav(name, team_number, email, matchCount)
        case "Vishnu":
            return Vishnu(name, team_number, email, matchCount)
        case "Dmitri":
            return Dmitri(name, team_number, email, matchCount)
        case "Ivan":
            return Ivan(name, team_number, email, matchCount)
        case "Adarsh":
            return Adarsh(name, team_number, email, matchCount)
        case "Rishabh":
            return Rishabh(name, team_number, email, matchCount)
        case "Ben":
            return Ben(name, team_number, email, matchCount)
        case "Roarke":
            return Roarke(name, team_number, email, matchCount)
        case "Deepesh":
            return Deepesh(name, team_number, email, matchCount)
        case "Rwad":
            return Rwad(name, team_number, email, matchCount)
        case _:
            raise ValueError("Invalid subclass name")
