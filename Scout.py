import json
import random


dataOutlineFile = open("ScoutingDataOutline.json", "r")


class Scout:
    def __init__(
        self,
        maxMatches: int,
        errorPercent: float,
        name: str,
        team_number: int,
        email: str,
    ):
        self.errorPercent = errorPercent
        self.name = name
        self.team_number = team_number
        self.email = email
        self.maxMatches = maxMatches
        self.canScout = True

    def scoutMatch(self, match: dict, driverStation: str) -> dict:
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
    for piece in match["score_breakdown"][allianceStr][communityStr][row]:
        if piece[4:] == driverStation:
            if piece[:4] == piece:
                retval += 1
    return retval


def getErrorAdjustedPieces(numPieces: int, errorPercent: float, max: int) -> int:
    retval = numPieces
    errorVal = 0
    for i in range(numPieces):
        rand = random.random()
        if rand < errorPercent:
            errorVal += 1
    rand = random.random()
    if rand < 0.5:
        errorVal *= -1
    retval += errorVal
    if retval > max:
        retval = max
    elif retval < 0:
        retval = 0
    return retval


class Vaclav(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 30, 0.3, "Vaclav" + str(name), team_number, email)


class Vishnu(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 10, 0.25, "Vishnu" + str(name), team_number, email)


class Dmitri(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 100, 0.05, "Dmitri" + str(name), team_number, email)


class Ivan(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 100, 0.1, "Ivan" + str(name), team_number, email)


class Adarsh(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 1, 0.1, "Adarsh" + str(name), team_number, email)


class Rishabh(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 80, 0.15, "Rishabh" + str(name), team_number, email)


class Ben(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 80, 0.2, "Ben" + str(name), team_number, email)


class Roarke(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 80, 0.08, "Roarke" + str(name), team_number, email)


class Deepesh(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 80, 0.18, "Deepesh" + str(name), team_number, email)


class Rwad(Scout):
    def __init__(self, name: str, team_number: int, email: str):
        Scout.__init__(self, 40, 0.23, "Rwad" + str(name), team_number, email)


def getRandomScout(name: str, team_number: int, email: str) -> Scout:
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
            return Vaclav(name, team_number, email)
        case "Vishnu":
            return Vishnu(name, team_number, email)
        case "Dmitri":
            return Dmitri(name, team_number, email)
        case "Ivan":
            return Ivan(name, team_number, email)
        case "Adarsh":
            return Adarsh(name, team_number, email)
        case "Rishabh":
            return Rishabh(name, team_number, email)
        case "Ben":
            return Ben(name, team_number, email)
        case "Roarke":
            return Roarke(name, team_number, email)
        case "Deepesh":
            return Deepesh(name, team_number, email)
        case "Rwad":
            return Rwad(name, team_number, email)
        case _:
            raise ValueError("Invalid subclass name")
