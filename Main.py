import os
import json
import random

from Ocean import Ocean
import Dwellers

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

    def __makeDweller (self, image):
        dwellersType = {'::': Dwellers.Plankton(self.ocean),
                        'oO': Dwellers.Goldfish(self.ocean),
                        'oЖ': Dwellers.Octopus(self.ocean),
                        '<A': Dwellers.Shark(self.ocean),
                        'Wh': Dwellers.Whale(self.ocean)}
        return dwellersType[image]

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
                self.__addDweller()
                self.__printOcean()
            case 3:
                self.__removeDweller()
                self.__printOcean()

    def __newOcean(self):
        print("enter ocean size: ")
        self.ocean = Ocean(self.input(2, 64))

    def __random(self):
        self.ocean = Ocean(random.randrange(8, 12))
        dwellerType = ['::', '::', '::','::','::', 'oO', 'oO', 'oO', 'oЖ','<A', 'Wh']
        for xCoordinate in range(self.ocean.getSize()):
            for yCoordinate in range(self.ocean.getSize()):
                if random.randrange(4) != 0:
                    dweller = self.__makeDweller(random.choice(dwellerType))
                    self.ocean.addDweller(dweller, [xCoordinate, yCoordinate])

    def __download(self):
        with open('Preservation.json') as file:
            data = json.load(file)
        self.ocean = Ocean(data['field size'])
        for characteristic in data['queue']:
            dweller = self.__makeDweller(characteristic['type'])
            dweller.setSex(characteristic['sex'])
            dweller.setHp(characteristic['hp'])
            dweller.setWeight(characteristic['weight'])
            dweller.setSatiety(characteristic['satiety'])
            dweller.setSpeed(characteristic['speed'])
            dweller.setCooldown(characteristic['cooldown'])
            self.ocean.addDweller(dweller, characteristic['location'])
        self.ocean.makeMove()
        for characteristic in data['newborn']:
            newborn = self.__makeDweller(characteristic['type'])
            newborn.setSex(characteristic['sex'])
            self.ocean.addDweller(newborn, characteristic['location'])

    def __save(self):
        data = {'field size': self.ocean.getSize(), 'queue': [], 'newborn': []}
        for dweller in self.ocean.getQueue():
            if isinstance(dweller, Dwellers.Dweller):
                data['queue'].append({
                    'type': str(dweller),
                    'location': dweller.getLocation(),
                    'sex': dweller.getSex(),
                    'hp': dweller.getHp(),
                    'weight': dweller.getWeight(),
                    'satiety': dweller.getSatiety(),
                    'speed': dweller.getSpeed(),
                    'cooldown': dweller.getCooldown()
                })
        for newborn in self.ocean.getNewborn():
            if isinstance(newborn, Dwellers.Dweller):
                data['newborn'].append({
                    'type': str(newborn),
                    'sex': newborn.getSex(),
                })
        with open('Preservation.json', 'w') as file:
            json.dump(data, file, indent=4)

    def __addDweller(self):
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
                self.ocean.addDweller(Dwellers.Plankton(self.ocean), (xСoordinate, yСoordinate))
            case 2:
                self.ocean.addDweller(Dwellers.Goldfish(self.ocean), (xСoordinate, yСoordinate))
            case 3:
                self.ocean.addDweller(Dwellers.Octopus(self.ocean), (xСoordinate, yСoordinate))
            case 4:
                self.ocean.addDweller(Dwellers.Shark(self.ocean), (xСoordinate, yСoordinate))
            case 5:
                self.ocean.addDweller(Dwellers.Whale(self.ocean), (xСoordinate, yСoordinate))

    def __removeDweller(self):
        print("choose location:\nline - ", end='')
        xСoordinate = self.input(0, self.ocean.getSize() - 1)
        print("column - ", end='')
        yСoordinate = self.input(0, self.ocean.getSize() - 1)
        dweller = self.ocean.getCell((xСoordinate, yСoordinate))
        if isinstance(dweller, Dwellers.Dweller):
            self.ocean.removeDweller(dweller)

    @staticmethod
    def __exit():
        clear()
        print("program has ended")
        return


interface = Interface()
interface.start()
