"""
Helper functions for tracking files and directories for changes.
"""

import os
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

def followFile(fileIn, USES_CLI):
    """Tracks and returns changes in a file"""

    while True:
        if not USES_CLI: QApplication.instance().processEvents()
        line = fileIn.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def followDir(path, USES_CLI):
    """Tracks and returns changes in a directory"""

    fileNames = os.listdir(path)
    while True:
        if not USES_CLI: QApplication.instance().processEvents()
        newFileNames = os.listdir(path)
        if fileNames == newFileNames:
            time.sleep(0.5)
            continue
        if len(newFileNames) > len(fileNames):
            files = list(set(newFileNames) - set(fileNames))
            return files[0]
