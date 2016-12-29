#!/usr/bin/env python3

import sys
import os

from helper import *

filePath = sys.argv[1]

fileTime = os.path.getmtime(filePath)

fileInput = open(filePath, "r", 1)

done = False
while not done:
    data = follow(fileInput)
    for line in data:
        print(line)

    break
