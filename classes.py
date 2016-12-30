"""
Collection of classes for a poker game's data.
"""

class Game:
    """A class for a poker game"""

    def __init__(self, newStake, newBlindLevel):
        self.stake = newStake
        self.handCount = 0
        self.update(newHandCount, newBlindLevel)

    def update(self, newHandCount, newBlindLevel):
        self.handCount += 1
        self.handCount = newHandCount
        self.blindLevel = newBlindLevel

    def addPlayer(self, newPlayer):
        self.players.append(newPlayer)

    def removePlayer(self, newPlayer):
        self.players.remove(newPlayer)


class Player:
    """A player in a poker game"""

    def __init__(self, newName, newChipCount):
        self.name = newName
        self.chipCount = newChipCount

    def setChipCount(self, newChipCount):
        self.chipCount = newChipCount
