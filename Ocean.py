from typing import List
from Dwellers import Dweller


class Ocean:
    def __init__(self, field_size):
        self.__field = [['~~'] * field_size for i in range(field_size)]
        self.__queue = []
        self.__newborn: List[Dweller] = []

    def getSize(self):
        return len(self.__field)

    def getQueue(self):
        return self.__queue

    def getNewborn(self):
        return self.__newborn

    def addDweller(self, dweller, location):
        self.__field[location[0]][location[1]] = dweller
        dweller.setLocation(location)
        self.__newborn.append(dweller)

    def removeDweller(self, dweller):
        self.setCell('~~', dweller.getLocation())
        if self.__queue.count(dweller):
            self.__queue.insert(self.__queue.index(dweller), None)
            self.__queue.remove(dweller)
        elif self.__newborn.count(dweller):
            self.__newborn.remove(dweller)

    def getCell(self, location):
        return self.__field[location[0]][location[1]]

    def setCell(self, obj, location):
        self.__field[location[0]][location[1]] = obj

    def makeMove(self):
        for dweller in self.__queue:
            if dweller is not None:
                dweller.makeMove()
        self.__newborn.extend(self.__queue)
        self.__queue = sorted(list(filter(None, self.__newborn)), key=lambda iDweller: iDweller.getWeight())
        self.__newborn.clear()

    def print(self):
        for row in self.__field:
            for element in row:
                print(str(element), end=' ')
            print()