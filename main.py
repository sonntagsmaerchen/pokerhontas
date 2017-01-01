#!/usr/bin/env python3

import sys
import os
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui
import helper
from classes import *

def main(fileInput, USES_CLI):

    window = 0
    if not USES_CLI:
        height = QApplication.instance().desktop().availableGeometry().height()
        window = ui.Window("Pokerhontas", [0, 0, 300, height])
        if os.name == "posix":
            window.setFixedSize(500, 1080)

        layout = QVBoxLayout(window)

        window.setLayout(layout)

        def exitHandler(self):
            sys.exit()

        window.closeEvent = exitHandler


    header = fileInput.readline()
    # Matches $0.44+$0.06 for example
    stake = re.search("[$€£][0-9]*\.[0-9]*\+[$€£][0-9]*\.[0-9]*", header)\
              .group(0)
    # Matches (10/20) for example
    bigBlind = int(re.search("\([0-9]*\/[0-9]*\)", header).group(0)[1:-1]\
                                                          .split("/")[1])
    game = Game(stake, bigBlind, window)

    for line in fileInput:
        words = line.split(" ")

        if words[0] == "Seat":
            inSeat = True
            player = Player(words[1][:-1], words[2], words[3][1:])
            game.addPlayer(player)

            # init for GUI
            if not USES_CLI:
                playerBox = ui.playerBox(player, game.handCount, game.bigBlind)
                game.GUIPlayerBoxes.append(playerBox)

                layout.addWidget(playerBox)


        elif words[1] == "posts":
            if words[2] == "big":
                break

    state = "GAMEDATA"

    data = helper.followFile(fileInput, USES_CLI)
    for line in data:
        words = line.split(" ")

        #state changing
        if words[0] == "***":

            prevState = state

            #get new state
            state = ""
            for word in words[1:]:
                if word == "***" or word == "***\n": break
                state += word

            #change from HOLECARDS to next state (either FLOP or SUMMARY)
            if prevState == "HOLECARDS":
                for player in game.players:
                    player.hasBet = False
                    player.hasRaised = False
                    if player.name == game.lastPlayertoRaise\
                       and state == "FLOP" and not player.allIn :
                       player.preFlopAggresor += 1

        #change from SUMMARY to GAMEDATA (preflop) at start of new hand
        elif line == "\n" and state != "GAMEDATA":
            state = "GAMEDATA"
            game.lastPlayertoRaise = ""
            for player in game.players: player.allIn = False

        #state handling
        if state == "GAMEDATA": game.gamedata(words)
        elif state == "HOLECARDS": game.holeCards(words)
        elif state == "FLOP": game.flop(words)
        elif state == "TURN":
            a=1
        elif state == "RIVER":
            a=1
        elif state == "SUMMARY":
            a=1
        elif state == "SHOWDOWN":
            a=1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
        ui.cli(path)
    else:
        app = QApplication(sys.argv)
        app.setStyle("cleanlooks")
        window = ui.gui()
        sys.exit(app.exec_())
