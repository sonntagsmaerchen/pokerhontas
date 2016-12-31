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

    filePath = helper.followDir(path)

    fileInput = open(path + filePath, "r", 1)

    header = fileInput.readline()
    # Matches $0.44+$0.06 for example
    stake = re.search("[$€£][0-9]*\.[0-9]*\+[$€£][0-9]*\.[0-9]*", header)\
              .group(0)
    # Matches (10/20) for example
    bigBlind = int(re.search("\([0-9]*\/[0-9]*\)", header).group(0)[1:-1]\
                                                          .split("/")[1])
    game = Game(stake, bigBlind)

    inSeat = False
    for line in fileInput:
        words = line.split(" ")

        if words[0] == "Seat":
            inSeat = True
            player = Player(words[1][:-1], words[2], words[4][1:])
            game.addPlayer(player)

        elif inSeat:
            break

    data = helper.followFile(fileInput)
    for line in data:
        print(line)
