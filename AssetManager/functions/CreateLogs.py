'''Adds Logging'''

import sys
import os
import tempfile

def logSetup(appName, location):
    '''Create folder for logs'''
    tempError = os.path.join(location,'error.log')
    tempOutput = os.path.join(location,'output.log')
    sys.stderr = open(tempError, 'w')
    sys.stdout = open(tempOutput, 'w')
