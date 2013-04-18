'''Modual that adds logging to AssetManager'''

import sys
import os
class Logging():
    def logSetup(self):
        '''Create folder for logs'''
        fileLocation = os.getcwd()
        fileLocation = fileLocation + '\\AssetManagerFiles\\'
        if not os.path.exists(fileLocation):
            os.makedirs(fileLocation)
        sys.stderr = open(fileLocation + 'error.log', 'w')
        sys.stdout = open(fileLocation + 'output.log', 'w')

