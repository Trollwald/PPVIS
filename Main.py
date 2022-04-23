import os
import json
import random

from Ocean import Ocean
import Inhabitants

clear = lambda: os.system("clear")


class Interface:
    def __init__(self):
        self.ocean: Ocean

    def start(self):
        print("0. create new ocean\n1. load saved \n2. randomise")
        match self.input(0, 2):
            case 0:
                self.__newOcean()
            case 1:
                self.__download()
            case 2:
                self.__random()
            case _:
                print("Error")
                return
        self.__printOcean()

    @staticmethod
    def input(begin, end):
        while True:
            key = input()
            if key.isdigit():
                if end >= int(key) >= begin:
                    return int(key)
            elif key == '':
                return begin
            print("invalid input, please try again")

    def __makeInhabitant (self, image):
        inhabitantsType = {'::': Inhabitants.Plankton(self.ocean),
                        'oO': Inhabitants.Goldfish(self.ocean),
                        'oЖ': Inhabitants.Octopus(self.ocean),
                        '<A': Inhabitants.Shark(self.ocean),
                        'Wh': Inhabitants.Whale(self.ocean)}
        return inhabitantsType[image]

    def __printMenu(self):
        clear()
        print("0. back to ocean\n1. create new\n2. load saved\n3. save\n4. exit")
        match self.input(0, 4):
            case 0:
                self.__printOcean()
            case 1:
                self.__newOcean()
                self.__printOcean()
            case 2:
                self.__download()
                self.__printOcean()
            case 3:
                self.__save()
                self.__printOcean()
            case 4:
                self.__exit()

    def __printOcean(self):
        clear()
        self.ocean.print()
        print("0. next step\n1. menu\n2. add creature\n3. kill someone")
        match self.input(0, 3):
            case 0:
                self.ocean.makeMove()
                self.__printOcean()
            case 1:
                self.__printMenu()
            case 2:
                self.__addInhabitant()
                self.__printOcean()
            case 3:
                self.__removeInhabitant()
                self.__printOcean()

    def __newOcean(self):
        print("enter ocean size: ")
        self.ocean = Ocean(self.input(2, 64))

    def __random(self):
        self.ocean = Ocean(random.randrange(8, 12))
        inhabitantType = ['::', '::', '::','::','::', 'oO', 'oO', 'oO', 'oЖ','<A', 'Wh']
        for xCoordinate in range(self.ocean.getSize()):
            for yCoordinate in range(self.ocean.getSize()):
                if random.randrange(4) != 0:
                    dweller = self.__makeInhabitant(random.choice(inhabitantType))
                    self.ocean.addInhabitant(dweller, [xCoordinate, yCoordinate])

    def __download(self):
        with open('Save.json') as file:
            data = json.load(file)
        self.ocean = Ocean(data['field size'])
        for characteristic in data['queue']:
            inhabitant = self.__makeInhabitant(characteristic['type'])
            inhabitant.setSex(characteristic['sex'])
            inhabitant.setHp(characteristic['hp'])
            inhabitant.setWeight(characteristic['weight'])
            inhabitant.setSatiety(characteristic['satiety'])
            inhabitant.setSpeed(characteristic['speed'])
            inhabitant.setCooldown(characteristic['cooldown'])
            self.ocean.addInhabitant(inhabitant, characteristic['location'])
        self.ocean.makeMove()
        for characteristic in data['newborn']:
            newborn = self.__makeInhabitant(characteristic['type'])
            newborn.setSex(characteristic['sex'])
            self.ocean.addInhabitant(newborn, characteristic['location'])

    def __save(self):
        data = {'field size': self.ocean.getSize(), 'queue': [], 'newborn': []}
        for inhabitant in self.ocean.getQueue():
            if isinstance(inhabitant, Inhabitants.Inhabitant):
                data['queue'].append({
                    'type': str(inhabitant),
                    'location': inhabitant.getLocation(),
                    'sex': inhabitant.getSex(),
                    'hp': inhabitant.getHp(),
                    'weight': inhabitant.getWeight(),
                    'satiety': inhabitant.getSatiety(),
                    'speed': inhabitant.getSpeed(),
                    'cooldown': inhabitant.getCooldown()
                })
        for newborn in self.ocean.getNewborn():
            if isinstance(newborn, Inhabitants.Inhabitant):
                data['newborn'].append({
                    'type': str(newborn),
                    'sex': newborn.getSex(),
                })
        with open('Save.json', 'w') as file:
            json.dump(data, file, indent=4)

    def __addInhabitant(self):
        print("choose location:\nline - ", end='')
        xСoordinate = self.input(0, self.ocean.getSize()-1)
        print("column - ", end='')
        yСoordinate = self.input(0, self.ocean.getSize() - 1)
        if str(self.ocean.getCell([xСoordinate, yСoordinate])) != '~~':
            print("attention! this cell is occupied")
        print("choose creature:\n0. CANCEL\n1. plankton : '::'\n2. goldfish : 'oO'\n3. octopus : 'oЖ'\n4. shark : '<A'\n5. whale : 'Wh'")
        match self.input(0, 7):
            case 0:
                pass
            case 1:
                self.ocean.addInhabitant(Inhabitants.Plankton(self.ocean), (xСoordinate, yСoordinate))
            case 2:
                self.ocean.addInhabitant(Inhabitants.Goldfish(self.ocean), (xСoordinate, yСoordinate))
            case 3:
                self.ocean.addInhabitant(Inhabitants.Octopus(self.ocean), (xСoordinate, yСoordinate))
            case 4:
                self.ocean.addInhabitant(Inhabitants.Shark(self.ocean), (xСoordinate, yСoordinate))
            case 5:
                self.ocean.addInhabitant(Inhabitants.Whale(self.ocean), (xСoordinate, yСoordinate))

    def __removeInhabitant(self):
        print("choose location:\nline - ", end='')
        xСoordinate = self.input(0, self.ocean.getSize() - 1)
        print("column - ", end='')
        yСoordinate = self.input(0, self.ocean.getSize() - 1)
        dweller = self.ocean.getCell((xСoordinate, yСoordinate))
        if isinstance(dweller, Inhabitants.Inhabitant):
            self.ocean.removeInhabitant(dweller)

    @staticmethod
    def __exit():
        clear()
        print("program has ended")
        return


interface = Interface()
interface.start()
