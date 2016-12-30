#!/usr/bin/env python2.7

import sys
import os
from itertools import chain

from helper import *

if __name__ == '__main__':
    path = sys.argv[1]

    trackedFiles = followDir(path)

    data = []
    for files in trackedFiles:
        for filePath in files:
            fileInput = open(path + filePath, "r", 1)
            data = chain(data, followFile(fileInput))


            end = []
            for gen in data:
                end = zip(end, gen)
                print(end)

            for line in end:
                print(line)

