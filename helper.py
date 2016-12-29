import time

def follow(fileIn):
    while True:
        line = fileIn.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

