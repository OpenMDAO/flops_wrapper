import numpy as np




def loadFile(fileName):
    fileIn = open(fileName,'r')
    dictionaries = {}
    for line in fileIn:
        line = line.rstrip()
        keys = line.split(':')
        if len(keys)>1:
            curVariable = keys[0]
            curVal = 
