#!/usr/bin/env python2.7

import sys
import os

from helper import *

if __name__ == '__main__':
    path = sys.argv[1]

    trackedFiles = followDir(path)

    fileInput = open(filePath, "r", 1)

    data = followFile(fileInput)
    for line in data:
        print(line)
