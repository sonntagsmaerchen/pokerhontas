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
        self.lastPlayertoRaise = ""
        self.inSeat = False

    def update(self, newBigBlind):
        self.bigBlind = newBigBlind
        if self.handCount >= 1:
            for player in self.players:
                player.printStats(self.handCount)
        print("\n\n\n")
        self.handCount += 1

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

            self.currentPlayers = []
            self.inSeat = False

    # do stuff with blinds here

    def holeCards(self, words):
        if words[1] == "calls" or words[1] == "raises":
            for player in self.players:
                if player.name == words[0][:-1]:
                    if not player.hasBet:
                        player.vpip += 1
                        player.hasBet = True
                    if not player.hasRaised and words[1] == "raises":
                        player.pfr += 1
                        player.hasRaised = True
                        self.lastPlayertoRaise = player.name

    def flop(self, words):
        if words[1] == "bets":
            for player in self.players:
                if player.name == words[0][:-1]:
                    if self.lastPlayertoRaise == player.name:
                        player.flopCbet +=1
                    self.lastPlayertoRaise = player.name

        elif words[1] == "raises":
            for player in self.players:
                if player.name == words[0][:-1]:
                    self.lastPlayertoRaise = player.name

class Player:
    """A player in a poker game"""

    def __init__(self, newSeat, newName, newChipCount):
        self.seat = newSeat
        self.name = newName
        self.chipCount = newChipCount
        self.hasBet = False
        self.hasRaised = False
        self.preFlopAggresor = 0

        self.vpip = 0
        self.pfr = 0
        self.flopCbet = 0

    def setChipCount(self, newChipCount):
        self.chipCount = newChipCount

    def printStats(self, handCount):
        if self.preFlopAggresor > 0:
            output = self.name + " VPIP: " + ("{0:.2f}".format((self.vpip/handCount)*100)) + "%"\
                               + " PFR: " + ("{0:.2f}".format((self.pfr/handCount)*100)) + "%"\
                               + " FlopCBet: " + ("{0:.2f}".format((self.flopCbet/self.preFlopAggresor)*100)) + "%"
        else:
            output = self.name + " VPIP: " + ("{0:.2f}".format((self.vpip/handCount)*100)) + "%"\
                               + " PFR: " + ("{0:.2f}".format((self.pfr/handCount)*100)) + "%"\
                               + " FlopCBet: / "
        print(output)
