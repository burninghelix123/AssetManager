'''Lookup paths for programs by searching for it in the Registry'''
'''
RegistryLookup.findPaths(0 = Lookup by Uninstall or 1 = Lookup by AppPath Registry,
                        ['Program Name'] = ['Maya'], ['Program Version 1'], 
                        ['Program Version 2'], ['Program Version 3'])
RegistryLookup.findPaths(0, ['AVG'], ['Maya2012'], ['Maya2013'], ['Maya2014'])                        
'''

from PyQt4 import QtCore, QtGui
from sys import platform as _platform
import os
import unicodedata
import re
if _platform == "win32":
    from _winreg import * 
lookupFailed = False

def findPaths(keyNumber, program, program2, program3, program4):
    '''Find paths to programs'''
    if _platform == "linux" or _platform == "linux2":
        # Future Linux Program Lookup
        pass
    elif _platform == "darwin":
        # Future OS X Program Lookup
        pass
    elif _platform == "win32":
        keyList1 = lookupKeys()
        keyList2 = lookupKeys2()
        if keyNumber == 1:
            keyList = keyList1
        if keyNumber == 2:
            keyList = keyList2
        path = lookupGenericPath(keyList, keyNumber, program, program2, program3, program4)    
        return path

def lookupKeys():
    '''Read in registry information from Uninstall Registry'''
    oneKey = ''
    allKey = []
    keyList = []
    masterKey = OpenKey(HKEY_LOCAL_MACHINE,
                        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                        0, KEY_READ)
    keys = QueryInfoKey(masterKey)
    for key in range(keys[0]):
        oneKey = str(EnumKey(masterKey, key))
        newMasterKey = OpenKey(HKEY_LOCAL_MACHINE,
                               r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\'+oneKey,
                               0, KEY_READ)
        for location in ['DisplayName','InstallLocation','UninstallString']:
            try:
                keyList.append(QueryValueEx(newMasterKey, location))
            except:
                pass    
    return keyList
    
def lookupKeys2():
    '''Read in remaining registry information from App Paths Registry'''
    oneKey = ''
    allKey = []
    keyList2 = []
    masterKey = OpenKey(HKEY_LOCAL_MACHINE,
                        r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths',
                        0, KEY_READ)
    keys = QueryInfoKey(masterKey)
    for key in range(keys[0]):
        oneKey = str(EnumKey(masterKey, key))
        newMasterKey = OpenKey(HKEY_LOCAL_MACHINE,
                               r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\'+oneKey,
                               0, KEY_READ)
        try:
            keyList2.append(QueryValueEx(newMasterKey, 'Path'))
        except:
            pass
    return keyList2

def lookupGenericPath(keyList, keyNumber, program, program2, program3, program4):
    '''Template to lookup program's path'''
    programPaths = []
    for item in keyList:
        searchItem = item[0]
        matchFound = False
        if re.search(program[0], searchItem):
            '''Program Name Match'''
            if re.search(program2[0], searchItem):
                '''Program Version 1 Match'''
                genericPath = searchItem
                matchFound = True
            if matchFound == False:
                if re.search(program3[0], searchItem):
                    '''Program Version 2 Match'''
                    genericPath = searchItem
                    matchFound = True
            if matchFound == False:
                if re.search(program4[0], searchItem):
                    '''Program Version 3 Match'''
                    genericPath = searchItem
                    matchFound = True
            if matchFound == False:
                '''Program Any Version Match'''
                genericPath = searchItem
            path = unicodedata.normalize('NFKD', genericPath).encode('ascii','ignore')
            if path not in programPaths:
                programPaths.append(path)
    return programPaths
