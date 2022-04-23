import random
import Ocean


class Inhabitant:
    def __init__(self, ocean, hp, weight, satiety, speed, cooldown):
        self.__ocean: Ocean.Ocean = ocean
        self.__location = [0, 0]
        self.__sex = random.randrange(2)
        self.__hp = hp
        self.__weight = weight
        self.__satiety = satiety
        self.__maxSatiety = satiety
        self.__speed = speed
        self.__cooldown = int(cooldown / 3)
        self.__maxCooldown = cooldown

    def __str__(self):
        return 'XX'

    def getOcean(self):
        return self.__ocean

    def getHeir(self):
        pass

    def getLocation(self):
        return self.__location

    def getSex(self):
        return self.__sex

    def getHp(self):
        return self.__hp

    def getWeight(self):
        return self.__weight

    def getSatiety(self):
        return self.__satiety

    def getSpeed(self):
        return self.__speed

    def getCooldown(self):
        return self.__cooldown

    def isHungry(self):
        if self.__satiety <= self.__maxSatiety / 2:
            return True
        else:
            return False

    def setLocation(self, location):
        self.__location[0] = location[0]
        self.__location[1] = location[1]

    def setSex(self, sex):
        self.__sex = sex

    def setHp(self, hp):
        self.__hp = hp

    def setWeight(self, weight):
        self.__weight = weight

    def setSatiety(self, satiety):
        self.__satiety = satiety

    def setSpeed(self, speed):
        self.__speed = speed

    def setCooldown(self, cooldown):
        self.__cooldown = cooldown

    def increaseSatiety(self, foodWeight):
        self.__satiety = self.__satiety + foodWeight
        if self.__satiety > self.__maxSatiety:
            self.__satiety = self.__maxSatiety

    def restartCooldown(self):
        self.__cooldown = self.__maxCooldown if self.getSex() else 0

    @staticmethod
    def getRoute():
        route = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]
        random.shuffle(route)
        return route

    def checkLocation(self):
        if self.__location[0] == self.__ocean.getSize() - 1:
            self.__location[0] = -1
        if self.__location[0] == - self.__ocean.getSize():
            self.__location[0] = 0
        if self.__location[1] == self.__ocean.getSize() - 1:
            self.__location[1] = -1
        if self.__location[1] == - self.__ocean.getSize():
            self.__location[1] = 0

    def makeMove(self):
        self.__hp = self.__hp - 1
        self.__satiety = self.__satiety - 1
        self.__cooldown = self.__cooldown - 1
        if self.__hp > 0 and self.__satiety > 0:
            return True
        self.die()

    def moveTo(self, location):
        if isinstance(self.__ocean.getCell([self.__location[0] + location[0], self.__location[1] + location[1]]),
                      Inhabitant):
            self.__ocean.getCell([self.__location[0] + location[0], self.__location[1] + location[1]]).die()
        self.__ocean.setCell('~~', self.__location)
        self.__location[0] = self.__location[0] + location[0]
        self.__location[1] = self.__location[1] + location[1]
        self.__ocean.setCell(self, self.__location)

    def move(self):
        for idx in self.getRoute():
            if str(self.__ocean.getCell([self.__location[0] + idx[0], self.__location[1] + idx[1]])) == '~~':
                self.moveTo(idx)
                return

    def eat(self):
        pass

    def multiply(self):
        pass

    def die(self):
        self.__ocean.removeInhabitant(self)


class Plant(Inhabitant):
    def __init__(self, ocean, hp, weight):
        super().__init__(ocean, hp, weight, hp, 0, 0)

    def __str__(self):
        return 'XP'

    def makeMove(self):
        if super().makeMove():
            self.checkLocation()
            self.multiply()

    def multiply(self):
        for idx in self.getRoute():
            if str(self.getOcean().getCell([self.getLocation()[0] + idx[0], self.getLocation()[1] + idx[1]])) == '~~':
                newborn = self.getHeir()
                self.getOcean().addInhabitant(newborn, [self.getLocation()[0] + idx[0], self.getLocation()[1] + idx[1]])
                break


class Animal(Inhabitant):
    def __init__(self, ocean, hp, weight, satiety, speed, cooldown):
        super().__init__(ocean, hp, weight, satiety, speed, cooldown)

    def __str__(self):
        return 'XA'

    def multiply(self):
        for idxPartner in self.getRoute():
            partner = self.getOcean().getCell(
                [self.getLocation()[0] + idxPartner[0], self.getLocation()[1] + idxPartner[1]])
            if type(partner) == type(self) and partner.getSex() != self.getSex():
                typeFlag = True
                if self.getCooldown() <= 0 and partner.getCooldown() <= 0:
                    cooldownFlag = True
                    if typeFlag == True and cooldownFlag == True:
                        for idx in self.getRoute():
                            if str(self.getOcean().getCell(
                                    [self.getLocation()[0] + idx[0], self.getLocation()[1] + idx[1]])) == '~~':
                                newborn = self.getHeir()
                                self.getOcean().addInhabitant(newborn,
                                                              [self.getLocation()[0] + idx[0],
                                                            self.getLocation()[1] + idx[1]])
                                self.restartCooldown()
                                partner.restartCooldown()
                                return True


class Herbivorous(Animal):
    def __init__(self, ocean, hp, weight, satiety, speed, cooldown):
        super().__init__(ocean, hp, weight, satiety, speed, cooldown)

    def __str__(self):
        return 'XH'

    def makeMove(self):
        if super().makeMove():
            for idx in range(self.getSpeed()):
                self.checkLocation()
                if self.getCooldown() <= 0:
                    if self.multiply():
                        return
                if self.eat():
                    return
                self.move()

    def eat(self):
        for idx in self.getRoute():
            victim = self.getOcean().getCell([self.getLocation()[0] + idx[0], self.getLocation()[1] + idx[1]])
            if isinstance(victim, Plant):
                self.increaseSatiety(victim.getWeight())
                self.moveTo(idx)
                return True


class Predator(Animal):
    def __init__(self, ocean, hp, weight, satiety, speed, cooldown):
        super().__init__(ocean, hp, weight, satiety, speed, cooldown)

    def makeMove(self):
        if super().makeMove():
            for idx in range(self.getSpeed()):
                self.checkLocation()
                if self.getCooldown() <= 0 and not self.isHungry():
                    if self.multiply():
                        return
                if self.eat():
                    return
                self.move()

    def __str__(self):
        return 'XR'

    def eat(self):
        for idx in self.getRoute():
            victim = self.getOcean().getCell([self.getLocation()[0] + idx[0], self.getLocation()[1] + idx[1]])
            if isinstance(victim, Animal) and self.getWeight() > victim.getWeight() > self.getWeight() / 5:
                self.increaseSatiety(victim.getWeight())
                self.moveTo(idx)
                return True


class Plankton(Plant):
    def __init__(self, ocean):
        super().__init__(ocean, 3, 1)

    def __str__(self):
        return '::'

    def getHeir(self):
        return Plankton(self.getOcean())


class Goldfish(Herbivorous):
    def __init__(self, ocean):
        super().__init__(ocean, 10, 2, 5, 1, 2)

    def __str__(self):
        return 'oO'

    def getHeir(self):
        return Goldfish(self.getOcean())


class Octopus(Predator):
    def __init__(self, ocean):
        super().__init__(ocean, 30, 7, 10, 3, 6)

    def __str__(self):
        return 'oЖ'

    def getHeir(self):
        return Octopus(self.getOcean())


class Shark(Predator):
    def __init__(self, ocean):
        super().__init__(ocean, 60, 30, 20, 3, 10)

    def __str__(self):
        return '<A'

    def getHeir(self):
        return Shark(self.getOcean())


class Whale(Herbivorous):
    def __init__(self, ocean):
        super().__init__(ocean, 100, 50, 30, 2, 15)

    def __str__(self):
        return 'Wh'

    def getHeir(self):
        return Whale(self.getOcean())
