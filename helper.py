import time

def followFile(fileIn):
    while True:
        line = fileIn.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def followDir(path):
    fileNames = os.listdir(path)
    while True:
        newFileNames = os.listdir(path)
        if fileNames == newFileNames:
            time.sleep(0.5)
            continue
        yield list(set(newFileNames) - set(fileNames))
        fileNames = newFileNames
