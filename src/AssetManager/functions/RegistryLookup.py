'''Lookup paths for programs for Asset Manager'''

from PyQt4 import QtCore, QtGui
from _winreg import *
import unicodedata
import re


class RegistryLookup():
    '''Use registry to find application paths'''
    lookupFailed = False
    
    def lookupKeys():
        '''Read in registry information'''
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
                value = QueryValueEx(newMasterKey, "DisplayName")
            except:
                pass
            try:
                value2 = QueryValueEx(newMasterKey, "InstallLocation")
            except:
                pass
            try:
                value3 = QueryValueEx(newMasterKey, "UninstallString")
            except:
                pass
            try:
                keyList += (allKey[key], value, value2, value3),
            except:
                pass
        return keyList
    try:
        keyList = lookupKeys()
    except:
        lookupFailed = True
        
    def lookupKeys2():
        '''Read in remaining registry information'''
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
                value = QueryValueEx(newMasterKey, "Path")
            except:
                pass
            try:
                keyList2 += (allKey[key], value),
            except:
                pass
        return keyList2
    try:
        keyList2 = lookupKeys2()
    except:
        lookupFailed = True
        
    def lookupMayaPath(keyList):
        '''Find path for Maya'''
        mayaPath = ''
        for item in keyList:
            searchItem = item[1][0]
            searchItem = unicodedata.normalize('NFKD', searchItem).encode('ascii','ignore')
            if re.search(r'(.*)Autodesk Maya(.*)', searchItem):
                if re.search(r'(.*)Autodesk Maya 2013(.*)', searchItem):
                    mayaPath = item[2][0]
                elif re.search(r'(.*)Autodesk Maya 2012(.*)', searchItem):
                    mayaPath = item[2][0]
                else:
                    mayaPath = item[2][0]
        return mayaPath
    try:
        mayaPath = lookupMayaPath(keyList)
    except:
        lookupFailed = True
        
    def lookupNukePath(keyList):
        '''Find path for Nuke'''
        nukePath = ''
        for item in keyList:
            searchItem = item[1][0]
            searchItem = unicodedata.normalize('NFKD', searchItem).encode('ascii','ignore')
            if re.search(r'(.*)Nuke(.*)', searchItem):
                if re.search(r'(.*)Nuke 6(.*)', searchItem):
                    nukePath = item[2][0]
                elif re.search(r'(.*)Nuke 5(.*)', searchItem):
                    nukePath = item[2][0]
                else:
                    nukePath = item[2][0]
        nukePath = re.sub(r'Uninstall Houdini.exe','',nukePath)
        nukeExe = []
        nukePath2 = nukePath.split('\\')
        nukePath2 = filter(None, nukePath2)
        nukeExe = nukePath2[len(nukePath2)-1]
        nukeExe = (nukeExe.split('v', 1)[0]) + '.exe'
        nukePath = nukePath + str(nukeExe)
        return nukePath
    try:
        nukePath = lookupNukePath(keyList)
    except:
        lookupFailed = True
        
    def lookupHoudiniPath(keyList):
        '''Find path for Houdini'''
        houdiniPath = ''
        for item in keyList:
            searchItem = item[1][0]
            searchItem = unicodedata.normalize('NFKD', searchItem).encode('ascii','ignore')
            if re.search(r'(.*)Houdini(.*)', searchItem):
                if re.search(r'(.*)Houdini 12(.*)', searchItem):
                    houdiniPath = item[3][0]
                elif re.search(r'(.*)Houdini 11(.*)', searchItem):
                    houdiniPath = item[3][0]
                else:
                    houdiniPath = item[3][0]
        return houdiniPath
    try:
        houdiniPath = lookupHoudiniPath(keyList)
    except:
        lookupFailed = True
        
    def lookupPhotoshopPath(keyList2):
        '''Find path for Photoshop'''
        photoshopPath = ''
        for item in keyList2:
            searchItem = item[0]
            if re.search(r'(.*)Photoshop(.*)', searchItem):
                photoshopPath = item[1][0]
        return photoshopPath
    try:
        photoshopPath = lookupPhotoshopPath(keyList2) 
    except:
        lookupFailed = True
    if lookupFailed == True:
        QtGui.QMessageBox.critical(self,
            "Warning",
            "Not all programs could be found installed on your computer.\nSome features may not function as intended.")
