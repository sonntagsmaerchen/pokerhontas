"""
Helper functions for tracking files and directories for changes.
"""

import os
import time

def followFile(fileIn):
    """Tracks and returns changes in a file"""

    while True:
        line = fileIn.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def followDir(path):
    """Tracks and returns changes in a directory"""

    fileNames = os.listdir(path)
    while True:
        newFileNames = os.listdir(path)
        if fileNames == newFileNames:
            time.sleep(0.5)
            continue
        files = list(set(newFileNames) - set(fileNames))
        return files[0]
