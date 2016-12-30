"""
Collection of classes for a poker game's data.
"""

class Game:
    """A class for a poker game"""

    def __init__(self, newStake, newBigBlind):
        self.stake = newStake
        self.handCount = 0
        self.update(newBigBlind)
        self.players = []

    def update(self, newBigBlind):
        self.handCount += 1
        self.bigBlind = newBigBlind

    def addPlayer(self, newPlayer):
        self.players.append(newPlayer)

    def removePlayer(self, newPlayer):
        self.players.remove(newPlayer)


class Player:
    """A player in a poker game"""

    def __init__(self, newSeat, newName, newChipCount):
        self.seat = newSeat
        self.name = newName
        self.chipCount = newChipCount

        self.vpip = 0
        self.pfr = 0

    def setChipCount(self, newChipCount):
        self.chipCount = newChipCount
