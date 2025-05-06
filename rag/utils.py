def getMoonPeek():
    with open("test_data/moonpeek.txt") as fp:
        return fp.read()

def getCode():
    with open("utils.py") as fp:
        return fp.read()