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
        self.currentPlayers = []
        self.inSeat = False

    def update(self, newBigBlind):
        self.handCount += 1
        self.bigBlind = newBigBlind

    def addPlayer(self, newPlayer):
        self.players.append(newPlayer)

    def removePlayer(self, newPlayer):
        self.players.remove(newPlayer)

    def gamedata(self, words):
        if words[0] == "PokerStars":
            bigBlind = int(words[13][1:-1].split("/")[1])
            self.update(bigBlind)

        elif words[0] == "Seat":
            self.inSeat = True
            self.currentPlayers.append(words[2])

        elif self.inSeat:
            playerNames = (player.name for player in self.players)
            diffplayers = list(set(playerNames)-set(self.currentPlayers))

            for name in diffplayers:
                for player in self.players:
                    if player.name == name: self.removePlayer(player)
                    break

            self.currentPlayers = []
            self.inSeat = False

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
