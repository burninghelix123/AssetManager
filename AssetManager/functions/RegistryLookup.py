'''Lookup paths for programs for Asset Manager'''

from PyQt4 import QtCore, QtGui
from _winreg import *
import unicodedata
import re
lookupFailed = False

def findPaths(keyNumber, program, program2, program3, program4):
    '''Find paths to programs'''
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
        allKey += [oneKey]
    for key in range(0,len(allKey),1):
        newMasterKey = OpenKey(HKEY_LOCAL_MACHINE,
                               r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\'+(allKey[key]),
                               0, KEY_READ)
        try:
            value = QueryValueEx(newMasterKey, 'DisplayName')
        except:
            value = None
        try:
            value2 = QueryValueEx(newMasterKey, 'InstallLocation')
        except:
            value2 = None
        try:
            value3 = QueryValueEx(newMasterKey, 'UninstallString')
        except:
            value3 = None
        entry = () 
        if not value == None:
            entry += value,
        if not value2 == None:
            entry += value2,
        if not value3 == None:
            entry += value3,
        if not (value == None and value2 == None and value3 == None):
            try:
                keyList += (entry),
            except:
                pass                   
    return keyList
try:
    keyList = lookupKeys()
except:
    lookupFailed = True
    
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
        allKey += [oneKey]
    for key in range(0,len(allKey),1):
        newMasterKey = OpenKey(HKEY_LOCAL_MACHINE,
                               r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\'+(allKey[key]),
                               0, KEY_READ)
        try:
            value = QueryValueEx(newMasterKey, 'Path')
        except:
            value = None
        entry = ()
        if not value == None:
            entry += ((allKey[key]),),
            entry += (value),
            try:
                keyList2 += (entry),
            except:
                pass        
    return keyList2

def lookupGenericPath(keyList, keyNumber, program, program2, program3, program4):
    '''Template to lookup program's path'''
    genericPath = []
    for number, name in enumerate(program):
        matches = []
        matchFound = False
        for item in keyList:
            searchItem = item[0][0]
            if re.search(program[number], searchItem):
                matches += [item]
        for count, list in enumerate(matches):
            match = list[0][0]
            if re.search(program2[number], match):
                if keyNumber == 1:
                    genericPath += [list[1]]                        
                if keyNumber == 2:
                    genericPath += [list[1]]
                matchFound = True
        if matchFound == False:
            for count, list in enumerate(matches):
                match = list[0][0]
                if re.search(program3[number], match):
                    if keyNumber == 1:
                        genericPath += [list[1]]                        
                    if keyNumber == 2:
                        genericPath += [list[1]]
                    matchFound = True
        if matchFound == False:
            for count, list in enumerate(matches):
                match = list[0][0]
                if re.search(program4[number], match):
                    if keyNumber == 1:
                        genericPath += [list[1]]                        
                    if keyNumber == 2:
                        genericPath += [list[1]]
                    matchFound = True
        if matchFound == False:
            for count, list in enumerate(matches):
                if keyNumber == 1:
                    genericPath += [list[1]]
                if keyNumber == 2:
                    genericPath += [list[1]]
    programPaths = []
    for path in genericPath:
        path = unicodedata.normalize('NFKD', path[0]).encode('ascii','ignore')
        programPaths += [path]
    programs = []
    for i in programPaths:
        if i not in programs:
            programs.append(i)
    return programs