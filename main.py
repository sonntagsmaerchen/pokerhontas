#!/usr/bin/env python3

import sys
import os

import helper
from classes import *

if __name__ == '__main__':
    path = sys.argv[1]

    filePath = helper.followDir(path)

    fileInput = open(path + filePath, "r", 1)

    data = helper.followFile(fileInput)
    for line in data:
        print(line)
