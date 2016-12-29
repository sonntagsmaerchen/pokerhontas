#!/usr/bin/env python3

import sys
import os

from helper import *

filePath = sys.argv[1]

fileTime = os.path.getmtime(filePath)

fileInput = open(filePath, "r", 1)

data = follow(fileInput)
for line in data:
    print(line)
