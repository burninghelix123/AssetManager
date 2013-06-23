'''Module that adds logging to AssetManager'''

import sys
import os
import tempfile

def logSetup(appName):
    '''Create folder for logs'''
    tempDir = tempfile.gettempdir()
    tempLocation = os.path.join(tempDir,'AssetManagerTemp')
    tempError = os.path.join(tempLocation,'error.log')
    tempOutput = os.path.join(tempLocation,'output.log')
    if not os.path.exists(tempLocation):
        os.makedirs(tempLocation)
    sys.stderr = open(tempError, 'w')
    sys.stdout = open(tempOutput, 'w')
