import random

from Autos import Autos, NoAuto, OnePiece, ThreePiece, TwoPiece, getRandomAuto


class Robot:
    def __init__(
        self,
        team: int,
        HCO: int,
        HCOV: int,
        HCU: int,
        HCUV: int,
        MCO: int,
        MCOV: int,
        MCU: int,
        MCUV: int,
        LCO: int,
        LCOV: int,
        LCU: int,
        LCUV: int,
        deathRate: float,
        autos: Autos,
    ):
        self.HCO = HCO
        self.HCOV = HCOV
        self.HCU = HCU
        self.HCUV = HCUV
        self.MCO = MCO
        self.MCOV = MCOV
        self.MCU = MCU
        self.MCUV = MCUV
        self.LCO = LCO
        self.LCOV = LCOV
        self.LCU = LCU
        self.LCUV = LCUV
        self.deathRate = 0
        self.team = team
        self.autos = autos
        rand = random.randint(0, 19)
        if rand == 0:
            self.driveTrain = "Mecanum"
            autos.getBump().setDockPercent(0)
            autos.getBump().setEngagePercent(0)
            autos.getMiddle().setDockPercent(0)
            autos.getMiddle().setEngagePercent(0)
            autos.getFeeder().setDockPercent(0)
            autos.getFeeder().setEngagePercent(0)
            self.teleEng = 0.01
            self.teleDockAttempt = 0.05
        elif rand > 12:
            self.driveTrain = "Swerve"
            randFloat = random.random()
            if randFloat < 0.6:
                randFloat = 0.6
            self.teleEng = randFloat
            self.teleDockAttempt = 0.8
        else:
            self.driveTrain = "Tank"
            randFloat = random.random()
            if randFloat < 0.6:
                randFloat = 0.6
            self.teleEng = randFloat
            self.teleDockAttempt = 0.8

    def getTeam(self) -> int:
        return self.team

    def getHCO(self) -> int:
        rand = random.randint(-self.HCOV, self.HCOV)
        if rand + self.HCO < 0:
            return 0
        else:
            return rand + self.HCO

    def getHCOV(self) -> int:
        return self.HCOV

    def getHCU(self) -> int:
        rand = random.randint(-self.HCUV, self.HCUV)
        if rand + self.HCU < 0:
            return 0
        else:
            return rand + self.HCU

    def getHCUV(self) -> int:
        return self.HCUV

    def getMCO(self) -> int:
        rand = random.randint(-self.MCOV, self.MCOV)
        if rand + self.MCO < 0:
            return 0
        else:
            return rand + self.MCO

    def getMCOV(self) -> int:
        return self.MCOV

    def getMCU(self) -> int:
        rand = random.randint(-self.MCUV, self.MCUV)
        if rand + self.MCU < 0:
            return 0
        else:
            return rand + self.MCU

    def getMCUV(self) -> int:
        return self.MCUV

    def getLCO(self) -> int:
        rand = random.randint(-self.LCOV, self.LCOV)
        if rand + self.LCO < 0:
            return 0
        else:
            return rand + self.LCO

    def getLCOV(self) -> int:
        return self.LCOV

    def getLCU(self) -> int:
        rand = random.randint(-self.LCUV, self.LCUV)
        if rand + self.LCU < 0:
            return 0
        else:
            return rand + self.LCU

    def getLCUV(self) -> int:
        return self.LCUV

    def getAutos(self) -> Autos:
        return self.autos

    def getAutoEngagePercent(self) -> float:
        return self.autos.getMiddle().engagePercent

    def getAutoDockPercent(self) -> float:
        return self.autos.getMiddle().dockPercent

    def getAutoDock(self) -> int:
        rand = random.random()
        retval = 0
        if rand < self.getAutoEngagePercent():
            retval = 12
        elif rand < (self.getAutoDockPercent() + self.getAutoEngagePercent()):
            retval = 8
        return retval

    def attemptedDock(self) -> bool:
        rand = random.random()
        if rand < self.teleDockAttempt:
            return True
        else:
            return False

    def engaged(self) -> bool:
        rand = random.random()
        if rand < self.teleEng:
            return True
        else:
            return False

    def isDead(self) -> bool:
        rand = random.random()
        return False
        if rand < self.deathRate:
            return True
        else:
            return False


class LowCube(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cube", 0, 4, 0.2, 0.7, 3),
                OnePiece("Cube", 0, 4, 0.2, 0.7, 0),
                OnePiece("Cube", 0, 4, 0, 0, 0),
            ]
        )
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cube", 0, 0, 0, 0, 0),
                OnePiece("Cube", 0, 0, 0, 0, 3),
                TwoPiece(["Cube", "Cube"], [0, 0], [0, 1], 0, 0),
                ThreePiece(["Cube", "Cube", "Cube"], [0, 0, 0], [0, 1, 2], 0, 0),
            ]
        )
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cube", 0, 8, 0, 0, 0),
                OnePiece("Cube", 0, 8, 0, 0, 3),
                TwoPiece(["Cube", "Cube"], [0, 0], [7, 8], 0, 0),
                ThreePiece(["Cube", "Cube", "Cube"], [0, 0, 0], [6, 7, 8], 0, 0),
            ]
        )
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2, 0.1, autos)


class Cube(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cube", 0, 4, 0.2, 0.7, 3),
                OnePiece("Cube", 0, 4, 0.2, 0.7, 0),
                OnePiece("Cube", 0, 4, 0, 0, 0),
                OnePiece("Cube", 1, 4, 0.2, 0.7, 3),
                OnePiece("Cube", 1, 4, 0.2, 0.7, 0),
                OnePiece("Cube", 1, 4, 0, 0, 0),
                OnePiece("Cube", 2, 4, 0.2, 0.7, 3),
                OnePiece("Cube", 2, 4, 0.2, 0.7, 0),
                OnePiece("Cube", 2, 4, 0, 0, 0),
            ]
        )
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cube", 2, 1, 0, 0, 0),
                OnePiece("Cube", 2, 1, 0, 0, 3),
                TwoPiece(["Cube", "Cube"], [0, 2], [0, 1], 0, 0),
                ThreePiece(["Cube", "Cube", "Cube"], [0, 2, 0], [0, 1, 2], 0, 0),
            ]
        )
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cube", 2, 7, 0, 0, 0),
                OnePiece("Cube", 2, 7, 0, 0, 3),
                TwoPiece(["Cube", "Cube"], [2, 0], [7, 8], 0, 0),
                ThreePiece(["Cube", "Cube", "Cube"], [0, 2, 0], [6, 7, 8], 0, 0),
            ]
        )
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 0, 0, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, autos)


class BadCone(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cone", 1, 3, 0.2, 0.7, 3),
                OnePiece("Cone", 1, 3, 0.2, 0.7, 0),
                OnePiece("Cone", 1, 3, 0, 0, 0),
            ]
        )
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cone", 0, 0, 0, 0, 0),
                OnePiece("Cone", 0, 0, 0, 0, 3),
                TwoPiece(["Cone", "Cone"], [0, 1], [0, 0], 0, 0),
                ThreePiece(["Cone", "Cone", "Cone"], [0, 1, 2], [0, 0, 0], 0, 0),
            ]
        )
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cone", 0, 8, 0, 0, 0),
                OnePiece("Cone", 0, 8, 0, 0, 3),
                TwoPiece(["Cone", "Cone"], [0, 1], [8, 8], 0, 0),
                ThreePiece(["Cone", "Cone", "Cone"], [0, 1, 2], [8, 8, 8], 0, 0),
            ]
        )
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, autos)


class GoodCone(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto(
            [
                OnePiece("Cone", 2, 3, 0.1, 0.8, 3),
                OnePiece("Cone", 2, 3, 0.1, 0.8, 0),
                OnePiece("Cone", 2, 3, 0, 0, 0),
            ]
        )
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto(
            [
                TwoPiece(["Cone", "Cone"], [2, 1], [0, 0], 0, 0),
                ThreePiece(["Cone", "Cone", "Cone"], [2, 1, 2], [2, 0, 0], 0, 0),
            ]
        )
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto(
            [
                TwoPiece(["Cone", "Cone"], [2, 1], [8, 8], 0, 0),
                ThreePiece(["Cone", "Cone", "Cone"], [2, 1, 2], [6, 8, 8], 0, 0),
            ]
        )
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, autos)


class GodBot(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto([OnePiece("Cube", 2, 4, 0.1, 0.9, 3)])
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto(
            [ThreePiece(["Cone", "Cube", "Cone"], [2, 2, 2], [2, 1, 0], 0, 0)]
        )
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto(
            [ThreePiece(["Cone", "Cube", "Cone"], [2, 2, 2], [6, 7, 8], 0, 0)]
        )
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 4, 1, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, autos)


class NoHigh(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cone", 1, 3, 0.1, 0.8, 3),
                OnePiece("Cone", 1, 3, 0.1, 0.8, 0),
                OnePiece("Cone", 1, 3, 0, 0, 0),
            ]
        )
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto(
            [NoAuto(), TwoPiece(["Cone", "Cube"], [1, 1], [0, 1], 0, 0)]
        )
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto(
            [NoAuto(), TwoPiece(["Cone", "Cube"], [1, 1], [8, 7], 0, 0)]
        )
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 0, 0, 0, 0, 4, 1, 3, 1, 0, 0, 0, 0, 0.1, autos)


class NoHighCones(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cone", 1, 3, 0.1, 0.8, 3),
                OnePiece("Cone", 1, 3, 0.1, 0.8, 0),
                OnePiece("Cone", 1, 3, 0, 0, 0),
            ]
        )
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto(
            [NoAuto(), TwoPiece(["Cone", "Cube"], [1, 2], [0, 1], 0, 0)]
        )
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto(
            [NoAuto(), TwoPiece(["Cone", "Cube"], [1, 2], [8, 7], 0, 0)]
        )
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 0, 0, 2, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0.1, autos)


class DefenseBot(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto(
            [
                NoAuto(),
                OnePiece("Cube", 0, 4, 0.1, 0.8, 3),
                OnePiece("Cube", 0, 4, 0.1, 0.8, 0),
                OnePiece("Cube", 0, 4, 0, 0, 0),
            ]
        )
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto(
            [NoAuto(), OnePiece("Cube", 0, 0, 0, 0, 0), OnePiece("Cube", 0, 0, 0, 0, 3)]
        )
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto(
            [NoAuto(), OnePiece("Cube", 0, 8, 0, 0, 0), OnePiece("Cube", 0, 8, 0, 0, 3)]
        )
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0.0, autos)


class Okay(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto([OnePiece("Cube", 1, 4, 0.2, 0.7, 3)])
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto(
            [
                TwoPiece(["Cone", "Cube"], [1, 1], [0, 1], 0, 0),
                ThreePiece(["Cone", "Cube", "Cone"], [1, 1, 1], [2, 1, 0], 0, 0),
            ]
        )
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto(
            [
                TwoPiece(["Cone", "Cube"], [1, 1], [8, 7], 0, 0),
                ThreePiece(["Cone", "Cube", "Cone"], [1, 1, 1], [6, 7, 8], 0, 0),
            ]
        )
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 3, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.3, autos)


class Bad(Robot):
    def __init__(self, team: int):
        # Randomizing Middle Auto
        middleAuto = getRandomAuto([NoAuto()])
        # Randomizing Feeder Auto
        feederAuto = getRandomAuto([NoAuto()])
        # Randomizing Bump Auto
        bumpAuto = getRandomAuto([NoAuto()])
        autos = Autos(feederAuto, middleAuto, bumpAuto)
        Robot.__init__(self, team, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, autos)


def randomRobot(team: int) -> Robot:
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


def dockingAutoRobots(bots: list) -> list:
    retval = ["", ""]
    if (bots[0].getAutoEngagePercent() >= bots[1].getAutoEngagePercent()) & (
        bots[0].getAutoEngagePercent() >= bots[2].getAutoEngagePercent()
    ):
        retval[0] = "r1"
    elif bots[1].getAutoEngagePercent() >= bots[2].getAutoEngagePercent():
        retval[0] = "r2"
    else:
        retval[0] = "r3"
    if (bots[3].getAutoEngagePercent() >= bots[4].getAutoEngagePercent()) & (
        bots[3].getAutoEngagePercent() >= bots[5].getAutoEngagePercent()
    ):
        retval[1] = "b1"
    elif bots[4].getAutoEngagePercent() >= bots[5].getAutoEngagePercent():
        retval[1] = "b2"
    else:
        retval[1] = "b3"
    return retval
