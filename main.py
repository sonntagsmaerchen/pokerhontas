#!/usr/bin/env python3

import sys
import os
import re

import helper
from classes import *

if __name__ == '__main__':
    path = sys.argv[1]

    if path[-1:] != "/":
        path += "/"

    print("Specify a file? ", end="")
    answered = False
    while not answered:
        userIn = input()
        if re.match("[yY](es)?", userIn):
            files = os.listdir(path)
            n = 0

            form = "{0:>3}: {1}"
            for f in files:
                print(form.format(str(n + 1), f))
                n += 1

            correctNumber = False
            print("Please enter a number between 1 and " + str(n)\
                  + " to select a file: ", end="")
            fileNumber = int(input()) - 1

            while not correctNumber:
                if fileNumber >= 0 and fileNumber < n:
                    fileName = files[fileNumber]
                    correctNumber = True

            print("Tracking " + fileName + "...")
            fileInput = open(path + fileName, "r", 1)
            answered = True

        elif re.match("[nN]o?", userIn):
            print("Watching " + path + " for new files...")
            fileName = helper.followDir(path)
            print("Found " + fileName + ". Tracking...")
            fileInput = open(path + fileName, "r", 1)
            answered = True

        else:
            print("Please enter yes or no: ", end="")

    header = fileInput.readline()
    # Matches $0.44+$0.06 for example
    stake = re.search("[$€£][0-9]*\.[0-9]*\+[$€£][0-9]*\.[0-9]*", header)\
              .group(0)
    # Matches (10/20) for example
    bigBlind = int(re.search("\([0-9]*\/[0-9]*\)", header).group(0)[1:-1]\
                                                          .split("/")[1])
    game = Game(stake, bigBlind)

    for line in fileInput:
        words = line.split(" ")

        if words[0] == "Seat":
            inSeat = True
            player = Player(words[1][:-1], words[2], words[3][1:])
            game.addPlayer(player)

        elif words[1] == "posts":
            if words[2] == "big":
                break

    state = "GAMEDATA"

    data = helper.followFile(fileInput)
    for line in data:
        words = line.split(" ")

        #state changing
        if words[0] == "***":

            #change from HOLECARDS to next state (either FLOP or SUMMARY)
            if state == "HOLECARDS":
                for player in game.players:
                    player.hasBet = False
                    player.hasRaised = False
                    if player.name == game.lastPlayertoRaise:
                        player.preFlopAggresor += 1

            #get new state
            state = ""
            for word in words[1:]:
                if word == "***" or word == "***\n": break
                state += word

        #change from SUMMARY to GAMEDATA (preflop) at start of new hand
        elif line == "\n" and state != "GAMEDATA":
            state = "GAMEDATA"
            game.lastPlayertoRaise = ""

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
