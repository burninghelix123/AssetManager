'''Module that adds logging to AssetManager'''

import sys
import os

def logSetup(appName):
    '''Create folder for logs'''
    fileLocation = os.getcwd()
    fileLocation = fileLocation + '\\'+appName+'\\'
    if not os.path.exists(fileLocation):
        os.makedirs(fileLocation)
    sys.stderr = open(fileLocation + 'error.log', 'w')
    sys.stdout = open(fileLocation + 'output.log', 'w')

