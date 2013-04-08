#!/usr/bin/python
# -*- coding: utf-8 -*-

# AssetManager.py
# 2013 April 8

'''AssetManager.py is a program I created to manage and organize
assets and files either locally on a computer or dynamically on
an SQL server.

===========================================
Copyright © 2013 Craig Barnett
===========================================

This program is to be distributed only by the owner, it was created
in the hope that it will be useful to artists, but WITHOUT ANY WARRANTY.

===========================================
Craig Barnett,
302 W 40th St Apt A, Savannah, Ga 31401
mailto: craigbme@hotmail.com
http://www.bhvfx.com
===========================================

This script allows the user to import files and add a variety of properties
and information to them along with custom icons. The asset manager can
either run locally, storing all of the information on your computer,
or dynamically through a SQL database. It has options for opening files
with Maya, Houdini, Nuke, Photoshop, Text Editor, Photo Viewer, and
the default application. It has 8 categories to organize files by and
some basic custom ui options. (Python, PyQt, MySQLdb)

The program can be used in two different ways. The first, locally where
all of the information is stored on the harddisk in either the
installation folder or the current working folder. The second, dynamically
where all of the information is stored on a SQL server and can be shared
and modified by other users.

To connect to a server the user will need to enter a server address, a
database name, a username, and a password.

The following server information is my own personal server provided for
testing purposes. In no way will this server be guarenteed to always be
online or available:
Address:         mysql.bhvfx.com
Database Name:   burninghelix123
Username:        exampleuser123
Password:        password

For any additional information, problems, or advice feel free to contact
me using the information that was above.

'''


from PyQt4 import QtCore, QtGui
import sys
import os
import subprocess
from _winreg import *
import re
import unicodedata
import ConfigParser
import MySQLdb as mysql
import base64

def logSetup():
    '''Create folder for logs'''
    fileLocation = os.getcwd()
    fileLocation = fileLocation + '\\AssetManagerFiles\\'
    if not os.path.exists(fileLocation):
        os.makedirs(fileLocation)
    sys.stderr = open(fileLocation + 'error.log', 'w')
    sys.stdout = open(fileLocation + 'output.log', 'w')
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
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

class PropertiesPopUp(QtGui.QDialog):
    '''
    Pop-up window for file/asset properties
    '''
    window = ''

    def __init__(self, propertiesWindow, listVar):
        QtGui.QWidget.__init__(self)
        self.setupUi(propertiesWindow, listVar)

    def findSelection(self, listVar):
        '''Retrieve selected item'''
        items = listVar.count()
        fileToOpen = ''
        selectedItems=[]
        rangedList =range(items)
        for i in rangedList:
            if listVar.isItemSelected(listVar.item(i))==True:
                fileToOpen = listVar.item(i).statusTip()
        return(fileToOpen)
    
    def saveProperties(self, propertiesWindow, listVar):
        '''Save properties information'''
        if changeMode.currentMode == 0: #If ran locally
            fileLocation = os.getcwd()
            fileLocation = fileLocation + '\\AssetManagerFiles\\'
            item = self.findSelection(listVar)
            itemSplit = []
            itemPath = item.split('\\')
            itemPath = filter(None, itemPath)
            itemName = itemPath[len(itemPath)-1]
            itemName = (itemName.split('.', 1)[0])
            file = open(fileLocation + itemName + '.properties', 'w+')
            nameField = PropertiesPopUp.window.nameField.text()
            categoryField = PropertiesPopUp.window.categoryField.text()
            tagsField = PropertiesPopUp.window.tagsField.text()
            statusField = PropertiesPopUp.window.statusField.text()
            dateField = PropertiesPopUp.window.dateField.text()
            authorField = PropertiesPopUp.window.authorField.text()
            versionField = PropertiesPopUp.window.versionField.text()
            commentsField = PropertiesPopUp.window.commentsField.toPlainText()
            file.write('[File]\n')
            file.write('File = ' + itemName + '\n\n')
            file.write('[Location]\n')
            file.write('Location = ' + fileLocation + '\n\n')       
            file.write('[Name]\n')
            file.write('Name = ' + nameField + '\n\n')
            file.write('[Category]\n')
            file.write('Category = ' + categoryField + '\n\n')
            file.write('[Tags]\n')
            file.write('Tags = ' + tagsField + '\n\n')
            file.write('[Status]\n')
            file.write('Status = ' + statusField + '\n\n')
            file.write('[Date Updated]\n')
            file.write('Date = ' + dateField + '\n\n')
            file.write('[Author]\n')
            file.write('Author = ' + authorField + '\n\n')
            file.write('[Version]\n')
            file.write('Version = ' + versionField + '\n\n')
            file.write('[Comments]\n')
            file.write('Comments = ' + commentsField + '\n\n')
            file.close
            file = open(fileLocation + itemName + '.properties', 'w+')
            items = listVar.count()
            selectedItems=[]
            rangedList =range(items)
            rangedList.reverse()
            for i in rangedList:
                if listVar.isItemSelected(listVar.item(i))==True:
                    url = listVar.item(i).statusTip()
                    listVar.takeItem(i)
                    if os.path.exists(url):
                        fileLocation = os.getcwd()
                        fileLocation = fileLocation + '\\AssetManagerFiles\\'
                        itemSplit = []
                        itemPath = url.split('\\')
                        itemPath = filter(None, itemPath)
                        itemName = itemPath[len(itemPath)-1]
                        itemNameExt = itemName
                        itemName = (itemName.split('.', 1)[0])
                        tempPath= fileLocation + itemName + '.png'
                        if os.path.exists(tempPath):
                            item = QtGui.QListWidgetItem(url)
                            QtGui.QListWidget.insertItem(listVar, i, item)
                            icon = QtGui.QIcon()
                            icon.addFile(tempPath,QtCore.QSize(72,72))
                            pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                 QtGui.QIcon.Normal, QtGui.QIcon.Off)
                            item.setIcon(icon)
                            pixmap.save((tempPath), 'PNG', 1)
                        else:
                            if str(url).endswith(('.gif', '.jpg', '.tif', '.png',
                                                  '.tiff', '.bmp', '.ico')) == True:
                                item = QtGui.QListWidgetItem(url)
                                QtGui.QListWidget.insertItem(listVar, i, item)
                                icon = QtGui.QIcon()
                                icon.addFile(url,QtCore.QSize(72,72))
                                pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                     QtGui.QIcon.Normal, QtGui.QIcon.Off)
                                item.setIcon(icon)
                                pixmap.save((tempPath), 'PNG', 1)
                            else:                    
                                item = QtGui.QListWidgetItem(url)
                                QtGui.QListWidget.insertItem(listVar, i, item)
                        item.setStatusTip(url)
                        if os.path.exists(fileLocation + itemName + '.properties'):
                            config = ConfigParser.ConfigParser()
                            wholeFile = str(fileLocation + itemName + '.properties')
                            config.read(wholeFile)
                            fileField = itemNameExt
                            locationField = fileLocation
                            nameField = config.get('Name', 'Name')
                            categoryField = config.get('Category', 'Category')
                            tagsField = config.get('Tags', 'Tags')
                            statusField = config.get('Status', 'Status')
                            dateField = config.get('Date Updated', 'Date')
                            authorField = config.get('Author', 'Author')
                            versionField = config.get('Version', 'Version')
                            commentsField = config.get('Comments', 'Comments')
                            text = 'File:   '
                            text += fileField
                            text += '\nLocation:   '
                            text += locationField
                            text += '\n'
                            if not (nameField == '' or nameField == ' '):
                                text += 'Name:   '
                                text += nameField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (categoryField == '' or categoryField == ' '):
                                text += 'Category:   '
                                text += categoryField
                                exists2 = 1
                            else:
                                exists2 = 0
                            if exists == 1 or exists2 == 1:
                                text += '\n'
                            if not (tagsField == '' or tagsField == ' '):
                                text += 'Tags:   '
                                text += tagsField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (statusField == '' or statusField == ' '):
                                text += 'Status:   '
                                text += statusField
                                exists2 = 1
                            else:                        
                                exists2 = 0
                            if exists == 1 or exists2 == 1:
                                text += '\n'
                            if not (dateField == '' or dateField == ' '):
                                text += 'Date:   '
                                text += dateField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (authorField == '' or authorField == ' '):
                                text += 'Author:   '
                                text += authorField
                                exists2 = 1
                            else:
                                exists2 = 0
                            if exists2 == 1:
                                text += '        '
                            if not (versionField == '' or versionField == ' '):
                                text += 'Version:   '
                                text += versionField
                                exists3 = 1
                            else:
                                exists3 = 0
                            if exists == 1 or exists2 == 1 or exists3 == 1:
                                text += '\n'
                            if not (commentsField == '' or commentsField == ' '):
                                text += 'Comments:   '
                                text += commentsField
                                exists = 1
                            item.setText(text)
                        else:
                            item.setText(url)
                        item.setStatusTip(url)
            self.close()
            
        if changeMode.currentMode == 1: #If ran dynamically
            fileLocation = os.getcwd()
            fileLocation = fileLocation + '\\AssetManagerFiles\\'
            if not os.path.exists(fileLocation):
                os.makedirs(fileLocation)
            item = self.findSelection(listVar)
            itemSplit = []
            itemPath = item.split('\\')
            itemPath = filter(None, itemPath)
            itemName = itemPath[len(itemPath)-1]
            itemNameExt = str(itemName)
            itemName = (itemName.split('.', 1)[0])
            itemName = str(itemName)
            nameField = str(PropertiesPopUp.window.nameField.text())
            categoryField = str(PropertiesPopUp.window.categoryField.text())
            tagsField = str(PropertiesPopUp.window.tagsField.text())
            statusField = str(PropertiesPopUp.window.statusField.text())
            dateField = str(PropertiesPopUp.window.dateField.text())
            authorField = str(PropertiesPopUp.window.authorField.text())
            versionField = str(PropertiesPopUp.window.versionField.text())
            commentsField = str(PropertiesPopUp.window.commentsField.toPlainText())
            propertiesData = (itemNameExt, item, nameField, categoryField,
                              tagsField, statusField, dateField, authorField,
                              versionField, commentsField)
            ex('REPLACE INTO Properties (File, Location, Name, Category, Tags, Status, Date, Author, Version, Comments) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', propertiesData)
            items = listVar.count()
            selectedItems=[]
            rangedList =range(items)
            rangedList.reverse()
            for i in rangedList:
                if listVar.isItemSelected(listVar.item(i))==True:
                    url = listVar.item(i).statusTip()
                    listVar.takeItem(i)
                    if os.path.exists(url):
                        fileLocation = os.getcwd()
                        fileLocation = fileLocation + '\\AssetManagerFiles\\'
                        itemSplit = []
                        itemPath = url.split('\\')
                        itemPath = filter(None, itemPath)
                        itemName = itemPath[len(itemPath)-1]
                        itemNameExt = itemName
                        itemName = (itemName.split('.', 1)[0])
                        tempPath= fileLocation + itemName + 'temp.png'
                        tempPath2= fileLocation + itemName + '.png'
                        data = 0
                        try:
                            data = ex("SELECT Data FROM Icons WHERE Name=%s",
                                      itemNameExt)
                        except:
                            pass
                        if data >= 1:
                            imgFile = open(tempPath2, 'wb')
                            imgFile.write(cur.fetchone()[0])
                            imgFile.close
                            item = QtGui.QListWidgetItem(url)
                            QtGui.QListWidget.insertItem(listVar, i, item)
                            icon = QtGui.QIcon()
                            icon.addFile(tempPath2,QtCore.QSize(72,72))
                            pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                 QtGui.QIcon.Normal, QtGui.QIcon.Off)
                            item.setIcon(icon)
                        else:
                            if str(url).endswith(('.gif', '.jpg', '.tif',
                                                  '.png', '.tiff', '.bmp', '.ico')) == True:
                                item = QtGui.QListWidgetItem(url)
                                QtGui.QListWidget.insertItem(listVar, i, item)
                                icon = QtGui.QIcon()
                                icon.addFile(url,QtCore.QSize(72,72))
                                pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                     QtGui.QIcon.Normal, QtGui.QIcon.Off)
                                item.setIcon(icon)
                                blobValue = open(tempPath, 'rb').read()
                                data = (itemNameExt, url, blobValue)
                                ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                                os.remove(str(tempPath))
                            else:                    
                                item = QtGui.QListWidgetItem(url)
                                QtGui.QListWidget.insertItem(listVar, i, item)
                        item.setStatusTip(url)
                        data = 0
                        try:
                            data = ex("SELECT * FROM Properties WHERE File=%s",itemNameExt)
                        except:
                            pass
                        if data >= 1:
                            data = cur.fetchone()
                            fileField = data[0]
                            locationField = data[1]
                            nameField = data[2]
                            categoryField = data[3]
                            tagsField = data[4]
                            statusField = data[5]
                            dateField = data[6]
                            authorField = data[7]
                            versionField = data[8]
                            commentsField = data[9]
                            text = 'File:   '
                            text += fileField
                            text += '\nLocation:   '
                            text += locationField
                            text += '\n'
                            if not (nameField == '' or nameField == ' '):
                                text += 'Name:   '
                                text += nameField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (categoryField == '' or categoryField == ' '):
                                text += 'Category:   '
                                text += categoryField
                                exists2 = 1
                            else:
                                exists2 = 0
                            if exists == 1 or exists2 == 1:
                                text += '\n'
                            if not (tagsField == '' or tagsField == ' '):
                                text += 'Tags:   '
                                text += tagsField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (statusField == '' or statusField == ' '):
                                text += 'Status:   '
                                text += statusField
                                exists2 = 1
                            else:                        
                                exists2 = 0
                            if exists == 1 or exists2 == 1:
                                text += '\n'
                            if not (dateField == '' or dateField == ' '):
                                text += 'Date:   '
                                text += dateField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (authorField == '' or authorField == ' '):
                                text += 'Author:   '
                                text += authorField
                                exists2 = 1
                            else:
                                exists2 = 0
                            if exists2 == 1:
                                text += '        '
                            if not (versionField == '' or versionField == ' '):
                                text += 'Version:   '
                                text += versionField
                                exists3 = 1
                            else:
                                exists3 = 0
                            if exists == 1 or exists2 == 1 or exists3 == 1:
                                text += '\n'
                            if not (commentsField == '' or commentsField == ' '):
                                text += 'Comments:   '
                                text += commentsField
                                exists = 1
                            item.setText(text)
                        else:
                            item.setText(url)
                        item.setStatusTip(url)
        propertiesWindow.close()
        
    def customIcon(self, listVar):
        '''Add custom icon to file/asset'''
        if changeMode.currentMode == 0: #If ran locally
            url = QtGui.QFileDialog.getOpenFileName(self,
                                                    'Open file','', ("Select Image: (*.*)"))
            url = os.path.abspath(url)
            items = listVar.count()
            rangedList =range(items)
            rangedList.reverse()
            for i in rangedList:
                if listVar.isItemSelected(listVar.item(i))==True:
                    item = listVar.item(i)
                    itemtext= str(item.statusTip())
                    fileLocation = os.getcwd()
                    fileLocation = fileLocation + '\\AssetManagerFiles\\'
                    itemSplit = []
                    itemPath = itemtext.split('\\')
                    itemPath = filter(None, itemPath)
                    itemName = itemPath[len(itemPath)-1]
                    itemName = (itemName.split('.', 1)[0])
                    tempName = str(itemName)
                    tempPath= fileLocation + itemName + '.png'
                    icon = QtGui.QIcon(url)
                    icon = QtGui.QIcon()
                    icon.addFile(url,QtCore.QSize(72,72))
                    pixmap = icon.pixmap(QtCore.QSize(72,72),
                                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    item.setIcon(icon)
                    pixmap.save((tempPath), 'PNG', 1)
                    
        if changeMode.currentMode == 1: #If ran dynamically
            url = QtGui.QFileDialog.getOpenFileName(self, 'Open file','',
                                                    ("Select Image: (*.*)"))
            url = os.path.abspath(url)
            items = listVar.count()
            rangedList =range(items)
            rangedList.reverse()
            for i in rangedList:
                if listVar.isItemSelected(listVar.item(i))==True:
                    item = listVar.item(i)
                    itemtext = str(item.statusTip())
                    fileLocation = os.getcwd()
                    fileLocation = fileLocation + '\\AssetManagerFiles\\'
                    itemSplit = []
                    itemPath = itemtext.split('\\')
                    itemPath = filter(None, itemPath)
                    itemName = itemPath[len(itemPath)-1]
                    itemNameExt = itemName
                    itemName = (itemName.split('.', 1)[0])
                    tempPath= fileLocation + itemName + 'temp.png'
                    icon = QtGui.QIcon(url)
                    icon = QtGui.QIcon()
                    icon.addFile(url,QtCore.QSize(72,72))
                    pixmap = icon.pixmap(QtCore.QSize(72,72),
                                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    item.setIcon(icon)
                    pixmap.save((tempPath), 'PNG', 1)
                    with open(tempPath, "rb") as input_file:
                            blobValue = input_file.read()
                            data = (itemNameExt, url, blobValue)
                            ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                    os.remove(str(tempPath))
        
    def setupUi(self, propertiesWindow, listVar):
        '''Create properties window UI'''
        propertiesWindow.setObjectName(_fromUtf8("dialog"))
        propertiesWindow.resize(235, 377)
        PropertiesPopUp.window = self
        self.save = QtGui.QPushButton(propertiesWindow)
        self.save.setGeometry(QtCore.QRect(5, 350, 75, 23))
        self.save.setObjectName(_fromUtf8("save"))
        self.save.clicked.connect(lambda : self.saveProperties(propertiesWindow, listVar)) 
        self.closebtn = QtGui.QPushButton(propertiesWindow)
        self.closebtn.setGeometry(QtCore.QRect(155, 350, 75, 23))
        self.closebtn.setObjectName(_fromUtf8("close"))
        self.closebtn.clicked.connect(propertiesWindow.close)
        self.icon = QtGui.QPushButton(propertiesWindow)
        self.icon.setGeometry(QtCore.QRect(80, 350, 75, 23))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.icon.clicked.connect(lambda : self.customIcon(listVar)) 
        self.name = QtGui.QLabel(propertiesWindow)
        self.name.setGeometry(QtCore.QRect(10, 10, 46, 13))
        self.name.setObjectName(_fromUtf8("name"))
        self.date = QtGui.QLabel(propertiesWindow)
        self.date.setGeometry(QtCore.QRect(10, 130, 71, 16))
        self.date.setObjectName(_fromUtf8("date"))
        self.author = QtGui.QLabel(propertiesWindow)
        self.author.setGeometry(QtCore.QRect(10, 160, 46, 13))
        self.author.setObjectName(_fromUtf8("author"))
        self.version = QtGui.QLabel(propertiesWindow)
        self.version.setGeometry(QtCore.QRect(10, 190, 46, 13))
        self.version.setObjectName(_fromUtf8("version"))
        self.category = QtGui.QLabel(propertiesWindow)
        self.category.setGeometry(QtCore.QRect(10, 40, 51, 16))
        self.category.setObjectName(_fromUtf8("category"))
        self.tags = QtGui.QLabel(propertiesWindow)
        self.tags.setGeometry(QtCore.QRect(10, 70, 46, 13))
        self.tags.setObjectName(_fromUtf8("tags"))
        self.status = QtGui.QLabel(propertiesWindow)
        self.status.setGeometry(QtCore.QRect(10, 100, 46, 13))
        self.status.setObjectName(_fromUtf8("status"))
        self.comments = QtGui.QLabel(propertiesWindow)
        self.comments.setGeometry(QtCore.QRect(10, 230, 61, 16))
        self.comments.setObjectName(_fromUtf8("comments"))
        self.nameField = QtGui.QLineEdit(propertiesWindow)
        self.nameField.setGeometry(QtCore.QRect(102, 10, 121, 20))
        self.nameField.setObjectName(_fromUtf8("nameField"))
        self.categoryField = QtGui.QLineEdit(propertiesWindow)
        self.categoryField.setGeometry(QtCore.QRect(102, 40, 121, 20))
        self.categoryField.setObjectName(_fromUtf8("categoryField"))
        self.tagsField = QtGui.QLineEdit(propertiesWindow)
        self.tagsField.setGeometry(QtCore.QRect(102, 70, 121, 20))
        self.tagsField.setObjectName(_fromUtf8("tagsField"))
        self.statusField = QtGui.QLineEdit(propertiesWindow)
        self.statusField.setGeometry(QtCore.QRect(102, 100, 121, 20))
        self.statusField.setObjectName(_fromUtf8("statusField"))
        self.dateField = QtGui.QLineEdit(propertiesWindow)
        self.dateField.setGeometry(QtCore.QRect(102, 130, 121, 20))
        self.dateField.setObjectName(_fromUtf8("dateField"))
        self.authorField = QtGui.QLineEdit(propertiesWindow)
        self.authorField.setGeometry(QtCore.QRect(102, 160, 121, 20))
        self.authorField.setObjectName(_fromUtf8("authorField"))
        self.versionField = QtGui.QLineEdit(propertiesWindow)
        self.versionField.setGeometry(QtCore.QRect(102, 190, 121, 20))
        self.versionField.setObjectName(_fromUtf8("versionField"))
        self.commentsField = QtGui.QTextEdit(propertiesWindow)
        self.commentsField.setGeometry(QtCore.QRect(10, 250, 211, 81))
        self.commentsField.setObjectName(_fromUtf8("commentsField"))
        self.retranslateUi(propertiesWindow, listVar)
        QtCore.QMetaObject.connectSlotsByName(propertiesWindow)
        if Ui_MainWindow.interfaceColor == 1: #UI Dark Layout
            propertiesWindow.setStyleSheet('background-color:darkgrey;')
            self.nameField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
            self.categoryField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
            self.tagsField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
            self.statusField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
            self.dateField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
            self.authorField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
            self.versionField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
            self.commentsField.setStyleSheet('QTextEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
            self.save.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
            self.icon.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
            self.closebtn.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        if Ui_MainWindow.interfaceColor == 2: #UI Light Layout
            propertiesWindow.setStyleSheet('')
            self.nameField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; color:black}')
            self.categoryField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; color:black}')
            self.tagsField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; color:black}')
            self.statusField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; color:black}')
            self.dateField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; color:black}')
            self.authorField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; color:black}')
            self.versionField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; color:black}')
            self.commentsField.setStyleSheet('QTextEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; color:black}')
            self.save.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
            self.icon.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
            self.closebtn.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        if Ui_MainWindow.interfaceColor == 3: #UI Custom Layout
            propertiesWindow.setStyleSheet('background-color: %(color)s;' % {'color':ColorPicker.col.name()})
            self.nameField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':ColorPicker.col1.name(),'color4':ColorPicker.col4.name()})
            self.categoryField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':ColorPicker.col1.name(),'color4':ColorPicker.col4.name()})
            self.tagsField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':ColorPicker.col1.name(),'color4':ColorPicker.col4.name()})
            self.statusField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':ColorPicker.col1.name(),'color4':ColorPicker.col4.name()})
            self.dateField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':ColorPicker.col1.name(),'color4':ColorPicker.col4.name()})
            self.authorField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':ColorPicker.col1.name(),'color4':ColorPicker.col4.name()})
            self.versionField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color: %(color4)s}' % {'color1':ColorPicker.col1.name(),'color4':ColorPicker.col4.name()})
            self.commentsField.setStyleSheet('QTextEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color: %(color4)s}' % {'color1':ColorPicker.col1.name(),'color4':ColorPicker.col4.name()})
            self.save.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);color: %(color4)s}' % {'color4':ColorPicker.col4.name()})
            self.icon.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);color: %(color4)s}' % {'color4':ColorPicker.col4.name()})
            self.closebtn.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s}' % {'color4':ColorPicker.col4.name()})

    def retranslateUi(self, propertiesWindow, listVar):
        '''UI Renaming'''
        propertiesWindow.setWindowTitle(QtGui.QApplication.translate("dialog", "File Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.save.setText(QtGui.QApplication.translate("dialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.closebtn.setText(QtGui.QApplication.translate("dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.icon.setText(QtGui.QApplication.translate("dialog", "Select Icon", None, QtGui.QApplication.UnicodeUTF8))
        self.name.setText(QtGui.QApplication.translate("dialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.date.setText(QtGui.QApplication.translate("dialog", "Date Updated:", None, QtGui.QApplication.UnicodeUTF8))
        self.author.setText(QtGui.QApplication.translate("dialog", "Author:", None, QtGui.QApplication.UnicodeUTF8))
        self.version.setText(QtGui.QApplication.translate("dialog", "Version:", None, QtGui.QApplication.UnicodeUTF8))
        self.category.setText(QtGui.QApplication.translate("dialog", "Category:", None, QtGui.QApplication.UnicodeUTF8))
        self.tags.setText(QtGui.QApplication.translate("dialog", "Tags:", None, QtGui.QApplication.UnicodeUTF8))
        self.status.setText(QtGui.QApplication.translate("dialog", "Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.comments.setText(QtGui.QApplication.translate("dialog", "Comments:", None, QtGui.QApplication.UnicodeUTF8))
        fileLocation = os.getcwd()
        fileLocation = fileLocation + '\\AssetManagerFiles\\'
        item = self.findSelection(listVar)
        itemSplit = []
        itemPath = item.split('\\')
        itemPath = filter(None, itemPath)
        try:
            itemName = itemPath[len(itemPath)-1]
            itemNameExt = str(itemName)
            itemName = (itemName.split('.', 1)[0])
            
            if changeMode.currentMode == 0: #If ran locally
                if os.path.exists(fileLocation + itemName + '.properties'):
                    config = ConfigParser.ConfigParser()
                    wholeFile = str(fileLocation + itemName + '.properties')
                    config.read(wholeFile)
                    nameField = config.get('Name', 'Name')
                    categoryField = config.get('Category', 'Category')
                    tagsField = config.get('Tags', 'Tags')
                    statusField = config.get('Status', 'Status')
                    dateField = config.get('Date Updated', 'Date')
                    authorField = config.get('Author', 'Author')
                    versionField = config.get('Version', 'Version')
                    commentsField = config.get('Comments', 'Comments')
                    PropertiesPopUp.window.nameField.setText(nameField)
                    PropertiesPopUp.window.categoryField.setText(categoryField)
                    PropertiesPopUp.window.tagsField.setText(tagsField)
                    PropertiesPopUp.window.statusField.setText(statusField)
                    PropertiesPopUp.window.dateField.setText(dateField)
                    PropertiesPopUp.window.authorField.setText(authorField)
                    PropertiesPopUp.window.versionField.setText(versionField)
                    PropertiesPopUp.window.commentsField.setText(commentsField)
                    
            if changeMode.currentMode == 1: #If ran dynamically
                try:
                    ex("SELECT * FROM Properties WHERE File=%s",itemNameExt)
                    data = cur.fetchone()
                    fileField = data[0]
                    locationField = data[1]
                    nameField = data[2]
                    categoryField = data[3]
                    tagsField = data[4]
                    statusField = data[5]
                    dateField = data[6]
                    authorField = data[7]
                    versionField = data[8]
                    commentsField = data[9]
                    PropertiesPopUp.window.nameField.setText(nameField)
                    PropertiesPopUp.window.categoryField.setText(categoryField)
                    PropertiesPopUp.window.tagsField.setText(tagsField)
                    PropertiesPopUp.window.statusField.setText(statusField)
                    PropertiesPopUp.window.dateField.setText(dateField)
                    PropertiesPopUp.window.authorField.setText(authorField)
                    PropertiesPopUp.window.versionField.setText(versionField)
                    PropertiesPopUp.window.commentsField.setText(commentsField)
                except:
                    pass
        except:
            pass


class changeMode(QtGui.QMessageBox):
    '''Switch between running locally and dynamically'''
    currentMode = 0
    MainWindow = ''
    
    def __init__(self):
        super(changeMode, self).__init__()
        self.initUI()
        
    def initUI(self):
        '''Setup UI'''
        msgBox = self
        msgBox.setWindowTitle('Manager Mode:')
        msgBox.setText('Would you like to run this locally or dynamically through a datbase?')
        btnYes = QtGui.QPushButton('Locally')
        msgBox.addButton(btnYes, QtGui.QMessageBox.YesRole)
        btnNo = QtGui.QPushButton('Dynamically')
        msgBox.addButton(btnNo, QtGui.QMessageBox.NoRole)
        msgBox.show()
        self.connect(btnYes, QtCore.SIGNAL('clicked()'), self.runLocally)
        self.connect(btnNo, QtCore.SIGNAL('clicked()'), self.runDynamically)
 
    def runLocally(self):
        '''Run locally on computer'''
        changeMode.currentMode = 0
        changeMode.MainWindow = QtGui.QMainWindow()
        self.ui = Ui_MainWindow(changeMode.MainWindow)
        self.var = changeMode.MainWindow.show()
            
    def runDynamically(self):
        '''Run dynamically through SQL server'''
        changeMode.currentMode = 1
        fileLocation = os.getcwd()
        fileLocation = fileLocation + '\\AssetManagerFiles\\'
        if not os.path.exists(fileLocation):
            os.makedirs(fileLocation)
        fileLocation = fileLocation + "LoginInfo.txt"
        if os.path.exists(fileLocation):
            usestoredloginui=UseStoredLoginUi()
            ok = usestoredloginui.showDialog()
            if ok == QtGui.QMessageBox.Yes:
                config = ConfigParser.ConfigParser()
                config.read(fileLocation)
                address = config.get('Address', 'Address')
                username = config.get('Username', 'Username')
                encpassword = config.get('Password', 'Password')
                password = base64.b64decode(encpassword)
                databasename = config.get('DatabaseName', 'DatabaseName')
            else:
                connect=Connect()
                username, address, password, databasename = connect.connect()
        else:
            connect=Connect()
            username, address, password, databasename = connect.connect()
        try:
            database = mysql.connect(user=str(username), host=str(address), passwd=str(password), db=str(databasename))
        except:
            QtGui.QMessageBox.critical(self,
                        "Error",
                        "Could not connect to database!\nPlease check login info on left and retry!")
            changeMode.currentMode = 0
        global cur
        cur = database.cursor()
        global ex
        ex = cur.execute
        try:
            ex('CREATE TABLE IF NOT EXISTS AssetManager (P_Id int NOT NULL AUTO_INCREMENT, Settings text, Bookmarks text, Shots text, Projects text, Models text, Shaders text, Images text, Videos text, Audio text, Scripts text, Simulations text, PRIMARY KEY(P_Id))')
        except:
            pass
        try:
            ex('CREATE TABLE IF NOT EXISTS Properties (File VARCHAR(100), Location text, Name text, Category text, Tags text, Status text, Date text, Author text, Version text, Comments text, PRIMARY KEY(File))')
        except:
            pass
        try:
            ex('CREATE TABLE IF NOT EXISTS Icons (Name VARCHAR(100), Location text, Data LONGBLOB, PRIMARY KEY(Name))')
        except:
            pass
        changeMode.MainWindow = QtGui.QMainWindow()
        self.ui = Ui_MainWindow(changeMode.MainWindow)
        self.var = changeMode.MainWindow.show()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class Connect(QtGui.QWidget):
    '''Connect to SQL server'''
    def __init__(self):
        super(Connect, self).__init__()

    def connect(self):
        fileLocation = os.getcwd()
        fileLocation = fileLocation + '\\AssetManagerFiles\\LoginInfo.txt'
        addressui=AddressUi()
        address, ok = addressui.showDialog()
        if ok == False:
            sys.exit()
        usernameui = UsernameUi()
        username, ok = usernameui.showDialog()
        if ok == False:
            sys.exit()
        passwordui=PasswordUi()
        password, ok = passwordui.showDialog()
        if ok == False:
            sys.exit()
        databaseui=DatabaseUi()
        databasename, ok = databaseui.showDialog()
        if ok == False:
            sys.exit()
        storeloginui=StoreLoginUi()
        ok = storeloginui.showDialog()
        if ok == QtGui.QMessageBox.Yes:
            file = open(fileLocation, 'w+')
            file.write('[Address]\n')
            file.write('Address = ' + address + '\n\n')
            file.write('[Username]\n')
            file.write('Username = ' + username + '\n\n')       
            file.write('[Password]\n')
            encPassword = base64.b64encode(str(password))
            file.write('Password = ' + encPassword + '\n\n')
            file.write('[DatabaseName]\n')
            file.write('DatabaseName = ' + databasename + '\n\n')
            file.close
        else:
            pass
        return (username, address, password, databasename) 


class StoreLoginUi(QtGui.QWidget):
    '''Prompt to store login info'''
    def __init__(self):
        super(StoreLoginUi, self).__init__()

    def showDialog(self):
        msg = "Remember login info for next time?"
        ok = QtGui.QMessageBox.question(self, 'Login Info', 
                     msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        return (ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class UseStoredLoginUi(QtGui.QWidget):
    '''Prompt to use stored login info'''
    def __init__(self):
        super(UseStoredLoginUi, self).__init__()

    def showDialog(self):
        msg = "Login using stored information?"
        ok = QtGui.QMessageBox.question(self, 'Login Info', 
                     msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        return (ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class AddressUi(QtGui.QWidget):
    '''Prompt for server address'''
    def __init__(self):
        super(AddressUi, self).__init__()

    def showDialog(self):
        address = ''
        address, ok = QtGui.QInputDialog.getText(self, 'Server Address', 
            'Enter your server address:')
        return (address, ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class DatabaseUi(QtGui.QWidget):
    '''Prompt for database name'''
    def __init__(self):
        super(DatabaseUi, self).__init__()

    def showDialog(self):
        database = ''
        database, ok = QtGui.QInputDialog.getText(self, 'Database Name', 
            'Enter name of database to create table:')
        return (database, ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class PasswordUi(QtGui.QWidget):
    '''Prompt for server password'''
    def __init__(self):
        super(PasswordUi, self).__init__()

    def showDialog(self):
        password = ''
        password, ok = QtGui.QInputDialog.getText(self, 'Server Password', 
            'Enter your server password:', QtGui.QLineEdit.Password)
        return (password, ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class UsernameUi(QtGui.QWidget):
    '''Prompt for server username'''
    def __init__(self):
        super(UsernameUi, self).__init__()
        
    def showDialog(self):
        username = ''
        username, ok = QtGui.QInputDialog.getText(self, 'Server Username', 
            'Enter your server username:')
        return (username, ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class Ui_MainWindow(QtGui.QMainWindow):
    '''Main application UI'''
    interfaceColor = 0
    copiedItems = []
    propertiesWindow = ''
    window = ''
    
    def __init__(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(MainWindow)

    def closeEvent(self, event):
        reply2 = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
        if reply2 == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()          
    
    def importEntry(self, listName, listVar):
        '''Handling import via right click'''
        if changeMode.currentMode == 0: #If run locally
            files = QtGui.QFileDialog.getOpenFileNames(self, 'Open file',
                                                       '', (""+listName+" (*.*)"))
            for url in files:
                if os.path.exists(url):
                    fileLocation = os.getcwd()
                    fileLocation = fileLocation + '\\AssetManagerFiles\\'
                    itemSplit = []
                    itemPath = url.split('\\')
                    itemPath = filter(None, itemPath)
                    itemName = itemPath[len(itemPath)-1]
                    itemNameExt = itemName
                    itemName = (itemName.split('.', 1)[0])
                    tempPath= fileLocation + itemName + '.png'
                    if os.path.exists(tempPath):                     
                        item = QtGui.QListWidgetItem(url, listVar)
                        icon = QtGui.QIcon()
                        icon.addFile(tempPath,QtCore.QSize(72,72))
                        pixmap = icon.pixmap(QtCore.QSize(72,72),QtGui.QIcon.Normal,
                                             QtGui.QIcon.Off)
                        item.setIcon(icon)
                    else:
                        if str(url).endswith(('.gif', '.jpg', '.tif', '.png',
                                              '.tiff', '.bmp', '.ico')) == True:
                            item = QtGui.QListWidgetItem(url, listVar)
                            icon = QtGui.QIcon()
                            icon.addFile(url,QtCore.QSize(72,72))
                            pixmap = icon.pixmap(QtCore.QSize(72,72),QtGui.QIcon.Normal,
                                                 QtGui.QIcon.Off)
                            item.setIcon(icon)
                            pixmap.save((tempPath), 'PNG', 1)
                        else:                    
                            item = QtGui.QListWidgetItem(url)
                            QtGui.QListWidget.addItem(listVar, item)
                    item.setStatusTip(url)
                    if os.path.exists(fileLocation + itemName + '.properties'):
                        config = ConfigParser.ConfigParser()
                        wholeFile = str(fileLocation + itemName + '.properties')
                        config.read(wholeFile)
                        fileField = itemNameExt
                        locationField = url
                        nameField = config.get('Name', 'Name')
                        categoryField = config.get('Category', 'Category')
                        tagsField = config.get('Tags', 'Tags')
                        statusField = config.get('Status', 'Status')
                        dateField = config.get('Date Updated', 'Date')
                        authorField = config.get('Author', 'Author')
                        versionField = config.get('Version', 'Version')
                        commentsField = config.get('Comments', 'Comments')
                        text = 'File:   '
                        text += fileField
                        text += '\nLocation:   '
                        text += locationField
                        text += '\n'        
                        if not (nameField == '' or nameField == ' '):
                            text += 'Name:   '
                            text += nameField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (categoryField == '' or categoryField == ' '):
                            text += 'Category:   '
                            text += categoryField
                            exists2 = 1
                        else:
                            exists2 = 0
                        if exists == 1 or exists2 == 1:
                            text += '\n'
                        if not (tagsField == '' or tagsField == ' '):
                            text += 'Tags:   '
                            text += tagsField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (statusField == '' or statusField == ' '):
                            text += 'Status:   '
                            text += statusField
                            exists2 = 1
                        else:                        
                            exists2 = 0
                        if exists == 1 or exists2 == 1:
                            text += '\n'
                        if not (dateField == '' or dateField == ' '):
                            text += 'Date:   '
                            text += dateField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (authorField == '' or authorField == ' '):
                            text += 'Author:   '
                            text += authorField
                            exists2 = 1
                        else:
                            exists2 = 0
                        if exists2 == 1:
                            text += '        '
                        if not (versionField == '' or versionField == ' '):
                            text += 'Version:   '
                            text += versionField
                            exists3 = 1
                        else:
                            exists3 = 0
                        if exists == 1 or exists2 == 1 or exists3 == 1:
                            text += '\n'
                        if not (commentsField == '' or commentsField == ' '):
                            text += 'Comments:   '
                            text += commentsField
                            exists = 1
                        item.setText(text)
                    else:
                        item.setText(url)
                    item.setStatusTip(url)
                    
        if changeMode.currentMode == 1: #If run dynamically
            files = QtGui.QFileDialog.getOpenFileNames(self, 'Open file','', (""+listName+" (*.*)"))
            for url in files:
                if os.path.exists(url):
                    fileLocation = os.getcwd()
                    fileLocation = fileLocation + '\\AssetManagerFiles\\'
                    itemSplit = []
                    itemPath = url.split('\\')
                    itemPath = filter(None, itemPath)
                    itemName = itemPath[len(itemPath)-1]
                    itemNameExt = itemName
                    itemName = (itemName.split('.', 1)[0])
                    tempPath= fileLocation + itemName + 'temp.png'
                    tempPath2= fileLocation + itemName + '.png'
                    data = 0
                    try:
                        data = ex("SELECT Data FROM Icons WHERE Name=%s",
                                  itemNameExt)
                    except:
                        pass
                    if data >= 1:
                        imgFile = open(tempPath2, 'wb')
                        imgFile.write(cur.fetchone()[0])
                        imgFile.close
                        item = QtGui.QListWidgetItem(url, listVar)
                        icon = QtGui.QIcon()
                        icon.addFile(tempPath2,QtCore.QSize(72,72))
                        pixmap = icon.pixmap(QtCore.QSize(72,72),
                                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        item.setIcon(icon)
                    else:
                        if str(url).endswith(('.gif', '.jpg', '.tif',
                                              '.png', '.tiff', '.bmp',
                                              '.ico')) == True:
                         
                            item = QtGui.QListWidgetItem(url, listVar)
                            icon = QtGui.QIcon()
                            icon.addFile(url,QtCore.QSize(72,72))
                            pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                 QtGui.QIcon.Normal,
                                                 QtGui.QIcon.Off)
                            item.setIcon(icon)
                            pixmap.save((tempPath), 'PNG', 1)
                            blobValue = open(tempPath, 'rb').read()
                            data = (itemNameExt, url, blobValue)
                            ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                            os.remove(str(tempPath))
                        else:                    
                            item = QtGui.QListWidgetItem(url)
                            QtGui.QListWidget.addItem(listVar, item)
                    item.setStatusTip(url)
                    data = 0
                    try:
                        data = ex("SELECT * FROM Properties WHERE File=%s",itemNameExt)
                    except:
                        pass
                    if data >= 1:
                        data = cur.fetchone()
                        fileField = data[0]
                        locationField = data[1]
                        nameField = data[2]
                        categoryField = data[3]
                        tagsField = data[4]
                        statusField = data[5]
                        dateField = data[6]
                        authorField = data[7]
                        versionField = data[8]
                        commentsField = data[9]
                        text = 'File:   '
                        text += fileField
                        text += '\nLocation:   '
                        text += locationField
                        text += '\n'
                        if not (nameField == '' or nameField == ' '):
                            text += 'Name:   '
                            text += nameField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (categoryField == '' or categoryField == ' '):
                            text += 'Category:   '
                            text += categoryField
                            exists2 = 1
                        else:
                            exists2 = 0
                        if exists == 1 or exists2 == 1:
                            text += '\n'
                        if not (tagsField == '' or tagsField == ' '):
                            text += 'Tags:   '
                            text += tagsField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (statusField == '' or statusField == ' '):
                            text += 'Status:   '
                            text += statusField
                            exists2 = 1
                        else:                        
                            exists2 = 0
                        if exists == 1 or exists2 == 1:
                            text += '\n'
                        if not (dateField == '' or dateField == ' '):
                            text += 'Date:   '
                            text += dateField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (authorField == '' or authorField == ' '):
                            text += 'Author:   '
                            text += authorField
                            exists2 = 1
                        else:
                            exists2 = 0
                        if exists2 == 1:
                            text += '        '
                        if not (versionField == '' or versionField == ' '):
                            text += 'Version:   '
                            text += versionField
                            exists3 = 1
                        else:
                            exists3 = 0
                        if exists == 1 or exists2 == 1 or exists3 == 1:
                            text += '\n'
                        if not (commentsField == '' or commentsField == ' '):
                            text += 'Comments:   '
                            text += commentsField
                            exists = 1
                        item.setText(text)
                    else:
                        item.setText(url)
                    item.setStatusTip(url)
                    
    def deleteEntry(self, listVar):
        '''Delete selected item'''
        items = listVar.count()
        selectedItems=[]
        rangedList =range(items)
        rangedList.reverse()
        for i in rangedList:
            if listVar.isItemSelected(listVar.item(i))==True:
                listVar.takeItem(i)

    def openFile(self, listVar):
        '''Open selected file with default application'''
        fileToOpen = self.findSelection(listVar)
        os.startfile(str(fileToOpen))
        
    def openFileWith(self, listVar):
        '''Future implementation for custom applications'''
        pass
    
    def findSelection(self, listVar):
        '''Find selected item/asset'''
        items = listVar.count()
        fileToOpen = ''
        selectedItems=[]
        rangedList =range(items)
        for i in rangedList:
            if listVar.isItemSelected(listVar.item(i))==True:
                fileToOpen = listVar.item(i).statusTip()
        return(fileToOpen)
    
    def openFileWithMaya(self, listVar):
        '''Open file with Maya'''
        fileToOpen = self.findSelection(listVar)
        fileToOpen = str(fileToOpen)
        mayaPath = RegistryLookup.mayaPath + 'bin\maya.exe'
        subprocess.Popen("%s %s" % (mayaPath, fileToOpen))
        
    def openFileWithHoudini(self, listVar):
        '''Open file with Houdini'''
        fileToOpen = self.findSelection(listVar)
        fileToOpen = str(fileToOpen)
        houdiniPath = RegistryLookup.houdiniPath + 'bin\houdini.exe'
        subprocess.Popen("%s %s" % (houdiniPath, fileToOpen))
        
    def openFileWithNuke(self, listVar):
        '''Open file with Nuke'''
        fileToOpen = self.findSelection(listVar)
        fileToOpen = str(fileToOpen)
        nukePath = RegistryLookup.nukePath
        subprocess.Popen("%s %s" % (nukePath, fileToOpen))
        
    def openFileWithPhotoshop(self, listVar):
        '''Open file with Photoshop'''
        fileToOpen = self.findSelection(listVar)
        fileToOpen = str(fileToOpen)
        photoshopPath = RegistryLookup.photoshopPath + 'Photoshop.exe'
        subprocess.Popen("%s %s" % (photoshopPath, fileToOpen))
        
    def openFileWithTextEditor(self, listVar):
        '''Open file with text editor'''
        fileToOpen = self.findSelection(listVar)
        fileToOpen = str(fileToOpen)
        subprocess.Popen("%s %s" % ('notepad', fileToOpen))
        
    def openFileWithImageViewer(self, listVar):
        '''Open file with Image Viewer'''
        fileToOpen = self.findSelection(listVar)
        fileToOpen = str(fileToOpen)
        imageViewerPath = 'C:\\Windows\\System32\\rundll32.exe \"C:\\Program Files\\Windows Photo Viewer\\PhotoViewer.dll\", ImageView_Fullscreen ' + fileToOpen
        subprocess.Popen(imageViewerPath)
        
    def fileProperties(self, listVar):
        '''Open file properties'''
        Ui_MainWindow.propertiesWindow = QtGui.QDialog()
        self.ui = PropertiesPopUp(Ui_MainWindow.propertiesWindow, listVar)
        self.var = Ui_MainWindow.propertiesWindow.exec_()
        
    def previewFile(self, listVar):
        '''Future implementation to preview file without opening'''
        pass

    def openAssetFile(self, var):
        '''Open Asset Manager File'''
        if changeMode.currentMode == 0: #If run locally
            exists = 0
            tabs = [self.projects_listView, self.models_listView, self.shaders_listView,
                    self.images_listView, self.videos_listView, self.audio_listView,
                    self.scripts_listView, self.simulations_listView]
            if var == 0:
                fileToOpen = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                               '', ("(*.asset)"))
            if var == 1:
                fileToOpen = self.findSelection(self.listWidget_2)
                fileToOpen = str(fileToOpen)
            if not fileToOpen == '':
                for listVar in tabs:
                    items = listVar.count()
                    if items > 0:
                        exists = 1
                if exists == 1:
                    reply = QtGui.QMessageBox.question(self, 'Message',
                                                       "Are you sure you want to open?\nDoing so will clear current workspace!",
                                                       QtGui.QMessageBox.Yes | 
                    QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        for listVar in tabs:
                            items = listVar.count()
                            selectedItems=[]
                            rangedList =range(items)
                            rangedList.reverse()
                            for i in rangedList:
                                listVar.takeItem(i)
                        fileToOpen = str(fileToOpen)
                        config = ConfigParser.ConfigParser()
                        config.read(fileToOpen)
                        nameField = config.get('Project', 'Name')
                        projectsItems = config.get('Projects', 'Items')
                        modelsItems = config.get('Models', 'Items')
                        shadersItems = config.get('Shaders', 'Items')
                        imagesItems = config.get('Images', 'Items')
                        videosItems = config.get('Videos', 'Items')
                        audioItems = config.get('Audio', 'Items')
                        scriptsItems = config.get('Scripts', 'Items')
                        simulationsItems = config.get('Simulations', 'Items')
                        projectsItems = projectsItems.split('\n')
                        modelsItems = modelsItems.split('\n')
                        shadersItems = shadersItems.split('\n')
                        imagesItems = imagesItems.split('\n')
                        videosItems = videosItems.split('\n')
                        audioItems = audioItems.split('\n')
                        scriptsItems = scriptsItems.split('\n')
                        simulationsItems = simulationsItems.split('\n')
                        for item in projectsItems:
                            self.addItemToList(item, self.projects_listView)
                        for item in modelsItems:
                            self.addItemToList(item, self.models_listView)
                        for item in shadersItems:
                            self.addItemToList(item, self.shaders_listView)
                        for item in imagesItems:
                            self.addItemToList(item, self.images_listView)
                        for item in videosItems:
                            self.addItemToList(item, self.videos_listView)
                        for item in audioItems:
                            self.addItemToList(item, self.audio_listView)
                        for item in scriptsItems:
                            self.addItemToList(item, self.scripts_listView)
                        for item in simulationsItems:
                            self.addItemToList(item, self.simulations_listView)
                if exists == 0:
                    for listVar in tabs:
                        items = listVar.count()
                        selectedItems=[]
                        rangedList =range(items)
                        rangedList.reverse()
                        for i in rangedList:
                            listVar.takeItem(i)
                    fileToOpen = str(fileToOpen)
                    config = ConfigParser.ConfigParser()
                    config.read(fileToOpen)
                    nameField = config.get('Project', 'Name')
                    projectsItems = config.get('Projects', 'Items')
                    modelsItems = config.get('Models', 'Items')
                    shadersItems = config.get('Shaders', 'Items')
                    imagesItems = config.get('Images', 'Items')
                    videosItems = config.get('Videos', 'Items')
                    audioItems = config.get('Audio', 'Items')
                    scriptsItems = config.get('Scripts', 'Items')
                    simulationsItems = config.get('Simulations', 'Items')
                    projectsItems = projectsItems.split('\n')
                    modelsItems = modelsItems.split('\n')
                    shadersItems = shadersItems.split('\n')
                    imagesItems = imagesItems.split('\n')
                    videosItems = videosItems.split('\n')
                    audioItems = audioItems.split('\n')
                    scriptsItems = scriptsItems.split('\n')
                    simulationsItems = simulationsItems.split('\n')
                    for item in projectsItems:
                        self.addItemToList(item, self.projects_listView)
                    for item in modelsItems:
                        self.addItemToList(item, self.models_listView)
                    for item in shadersItems:
                        self.addItemToList(item, self.shaders_listView)
                    for item in imagesItems:
                        self.addItemToList(item, self.images_listView)
                    for item in videosItems:
                        self.addItemToList(item, self.videos_listView)
                    for item in audioItems:
                        self.addItemToList(item, self.audio_listView)
                    for item in scriptsItems:
                        self.addItemToList(item, self.scripts_listView)
                    for item in simulationsItems:
                        self.addItemToList(item, self.simulations_listView)

        if changeMode.currentMode == 1: #If run dynamically
            exists = 0
            tabs = [self.projects_listView, self.models_listView,
                    self.shaders_listView, self.images_listView,
                    self.videos_listView, self.audio_listView,
                    self.scripts_listView, self.simulations_listView]
            if var == 0:
                fileToOpen = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                               '', ("(*.asset)"))
            if var == 1:
                fileToOpen = self.findSelection(self.listWidget_2)
                fileToOpen = str(fileToOpen)
            if not fileToOpen == '':
                for listVar in tabs:
                    items = listVar.count()
                    if items > 0:
                        exists = 1
                if exists == 1:
                    reply = QtGui.QMessageBox.question(self, 'Message',
                                                       "Are you sure you want to open?\nDoing so will clear current workspace!",
                                                       QtGui.QMessageBox.Yes | 
                    QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        for listVar in tabs:
                            items = listVar.count()
                            selectedItems=[]
                            rangedList =range(items)
                            rangedList.reverse()
                            for i in rangedList:
                                listVar.takeItem(i)
                        fileToOpen = str(fileToOpen)
                        config = ConfigParser.ConfigParser()
                        config.read(fileToOpen)
                        nameField = config.get('Project', 'Name')
                        projectsItems = config.get('Projects', 'Items')
                        modelsItems = config.get('Models', 'Items')
                        shadersItems = config.get('Shaders', 'Items')
                        imagesItems = config.get('Images', 'Items')
                        videosItems = config.get('Videos', 'Items')
                        audioItems = config.get('Audio', 'Items')
                        scriptsItems = config.get('Scripts', 'Items')
                        simulationsItems = config.get('Simulations', 'Items')
                        projectsItems = projectsItems.split('\n')
                        modelsItems = modelsItems.split('\n')
                        shadersItems = shadersItems.split('\n')
                        imagesItems = imagesItems.split('\n')
                        videosItems = videosItems.split('\n')
                        audioItems = audioItems.split('\n')
                        scriptsItems = scriptsItems.split('\n')
                        simulationsItems = simulationsItems.split('\n')
                        for item in projectsItems:
                            self.addItemToList(item, self.projects_listView)
                        for item in modelsItems:
                            self.addItemToList(item, self.models_listView)
                        for item in shadersItems:
                            self.addItemToList(item, self.shaders_listView)
                        for item in imagesItems:
                            self.addItemToList(item, self.images_listView)
                        for item in videosItems:
                            self.addItemToList(item, self.videos_listView)
                        for item in audioItems:
                            self.addItemToList(item, self.audio_listView)
                        for item in scriptsItems:
                            self.addItemToList(item, self.scripts_listView)
                        for item in simulationsItems:
                            self.addItemToList(item, self.simulations_listView)
                if exists == 0:
                    for listVar in tabs:
                        items = listVar.count()
                        selectedItems=[]
                        rangedList =range(items)
                        rangedList.reverse()
                        for i in rangedList:
                            listVar.takeItem(i)
                    fileToOpen = str(fileToOpen)
                    config = ConfigParser.ConfigParser()
                    config.read(fileToOpen)
                    nameField = config.get('Project', 'Name')
                    projectsItems = config.get('Projects', 'Items')
                    modelsItems = config.get('Models', 'Items')
                    shadersItems = config.get('Shaders', 'Items')
                    imagesItems = config.get('Images', 'Items')
                    videosItems = config.get('Videos', 'Items')
                    audioItems = config.get('Audio', 'Items')
                    scriptsItems = config.get('Scripts', 'Items')
                    simulationsItems = config.get('Simulations', 'Items')
                    projectsItems = projectsItems.split('\n')
                    modelsItems = modelsItems.split('\n')
                    shadersItems = shadersItems.split('\n')
                    imagesItems = imagesItems.split('\n')
                    videosItems = videosItems.split('\n')
                    audioItems = audioItems.split('\n')
                    scriptsItems = scriptsItems.split('\n')
                    simulationsItems = simulationsItems.split('\n')
                    for item in projectsItems:
                        self.addItemToList(item, self.projects_listView)
                    for item in modelsItems:
                        self.addItemToList(item, self.models_listView)
                    for item in shadersItems:
                        self.addItemToList(item, self.shaders_listView)
                    for item in imagesItems:
                        self.addItemToList(item, self.images_listView)
                    for item in videosItems:
                        self.addItemToList(item, self.videos_listView)
                    for item in audioItems:
                        self.addItemToList(item, self.audio_listView)
                    for item in scriptsItems:
                        self.addItemToList(item, self.scripts_listView)
                    for item in simulationsItems:
                        self.addItemToList(item, self.simulations_listView)

    def importAssetFile(self, var):
        '''Import Asset manager file into project'''
        if changeMode.currentMode == 0: #If run locally
            if var == 0:
                fileToOpen = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                               '', ("(*.asset)"))
                fileToOpen = str(fileToOpen)
            if var == 1:
                fileToOpen = self.findSelection(self.listWidget_2)
                fileToOpen = str(fileToOpen)
            if not fileToOpen == '':
                config = ConfigParser.ConfigParser()
                config.read(fileToOpen)
                nameField = config.get('Project', 'Name')
                projectsItems = config.get('Projects', 'Items')
                modelsItems = config.get('Models', 'Items')
                shadersItems = config.get('Shaders', 'Items')
                imagesItems = config.get('Images', 'Items')
                videosItems = config.get('Videos', 'Items')
                audioItems = config.get('Audio', 'Items')
                scriptsItems = config.get('Scripts', 'Items')
                simulationsItems = config.get('Simulations', 'Items')
                projectsItems = projectsItems.split('\n')
                modelsItems = modelsItems.split('\n')
                shadersItems = shadersItems.split('\n')
                imagesItems = imagesItems.split('\n')
                videosItems = videosItems.split('\n')
                audioItems = audioItems.split('\n')
                scriptsItems = scriptsItems.split('\n')
                simulationsItems = simulationsItems.split('\n')
                for item in projectsItems:
                    self.addItemToList(item, self.projects_listView)
                for item in modelsItems:
                    self.addItemToList(item, self.models_listView)
                for item in shadersItems:
                    self.addItemToList(item, self.shaders_listView)
                for item in imagesItems:
                    self.addItemToList(item, self.images_listView)
                for item in videosItems:
                    self.addItemToList(item, self.videos_listView)
                for item in audioItems:
                    self.addItemToList(item, self.audio_listView)
                for item in scriptsItems:
                    self.addItemToList(item, self.scripts_listView)
                for item in simulationsItems:
                    self.addItemToList(item, self.simulations_listView)
                    
        if changeMode.currentMode == 1: #If run dynamically
            if var == 0:
                fileToOpen = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                               '', ("(*.asset)"))
                fileToOpen = str(fileToOpen)
            if var == 1:
                fileToOpen = self.findSelection(self.listWidget_2)
                fileToOpen = str(fileToOpen)
            if not fileToOpen == '':
                config = ConfigParser.ConfigParser()
                config.read(fileToOpen)
                nameField = config.get('Project', 'Name')
                projectsItems = config.get('Projects', 'Items')
                modelsItems = config.get('Models', 'Items')
                shadersItems = config.get('Shaders', 'Items')
                imagesItems = config.get('Images', 'Items')
                videosItems = config.get('Videos', 'Items')
                audioItems = config.get('Audio', 'Items')
                scriptsItems = config.get('Scripts', 'Items')
                simulationsItems = config.get('Simulations', 'Items')
                projectsItems = projectsItems.split('\n')
                modelsItems = modelsItems.split('\n')
                shadersItems = shadersItems.split('\n')
                imagesItems = imagesItems.split('\n')
                videosItems = videosItems.split('\n')
                audioItems = audioItems.split('\n')
                scriptsItems = scriptsItems.split('\n')
                simulationsItems = simulationsItems.split('\n')
                for item in projectsItems:
                    self.addItemToList(item, self.projects_listView)
                for item in modelsItems:
                    self.addItemToList(item, self.models_listView)
                for item in shadersItems:
                    self.addItemToList(item, self.shaders_listView)
                for item in imagesItems:
                    self.addItemToList(item, self.images_listView)
                for item in videosItems:
                    self.addItemToList(item, self.videos_listView)
                for item in audioItems:
                    self.addItemToList(item, self.audio_listView)
                for item in scriptsItems:
                    self.addItemToList(item, self.scripts_listView)
                for item in simulationsItems:
                    self.addItemToList(item, self.simulations_listView)
                      
    def addItemToList(self, url, listVar):
        '''Add asset manager file to saved list'''
        if changeMode.currentMode == 0: #If run locally
            if os.path.exists(url):
                fileLocation = os.getcwd()
                fileLocation = fileLocation + '\\AssetManagerFiles\\'
                itemSplit = []
                itemPath = url.split('\\')
                itemPath = filter(None, itemPath)
                itemName = itemPath[len(itemPath)-1]
                itemNameExt = itemName
                itemName = (itemName.split('.', 1)[0])
                tempPath= fileLocation + itemName + '.png'
                if os.path.exists(tempPath):
                    item = QtGui.QListWidgetItem(url, listVar)
                    icon = QtGui.QIcon()
                    icon.addFile(tempPath,QtCore.QSize(72,72))
                    pixmap = icon.pixmap(QtCore.QSize(72,72),
                                         QtGui.QIcon.Normal,
                                         QtGui.QIcon.Off)
                    item.setIcon(icon)
                else:
                    if str(url).endswith(('.gif', '.jpg', '.tif',
                                          '.png', '.tiff', '.bmp', '.ico')) == True:
                        item = QtGui.QListWidgetItem(url, listVar)
                        icon = QtGui.QIcon()
                        icon.addFile(url,QtCore.QSize(72,72))
                        pixmap = icon.pixmap(QtCore.QSize(72,72),
                                             QtGui.QIcon.Normal,
                                             QtGui.QIcon.Off)
                        item.setIcon(icon)
                    else:                    
                        item = QtGui.QListWidgetItem(url)
                        QtGui.QListWidget.addItem(listVar, item)
                if os.path.exists(fileLocation + itemName + '.properties'):
                    config = ConfigParser.ConfigParser()
                    wholeFile = str(fileLocation + itemName + '.properties')
                    config.read(wholeFile)
                    fileField = itemNameExt
                    locationField = url
                    nameField = config.get('Name', 'Name')
                    categoryField = config.get('Category', 'Category')
                    tagsField = config.get('Tags', 'Tags')
                    statusField = config.get('Status', 'Status')
                    dateField = config.get('Date Updated', 'Date')
                    authorField = config.get('Author', 'Author')
                    versionField = config.get('Version', 'Version')
                    commentsField = config.get('Comments', 'Comments')
                    text = 'File:   '
                    text += fileField
                    text += '\nLocation:   '
                    text += locationField
                    text += '\n'
                    if not (nameField == '' or nameField == ' '):
                        text += 'Name:   '
                        text += nameField
                        exists = 1
                    else:
                        exists = 0
                    if exists == 1:
                        text += '        '
                    if not (categoryField == '' or categoryField == ' '):
                        text += 'Category:   '
                        text += categoryField
                        exists2 = 1
                    else:
                        exists2 = 0
                    if exists == 1 or exists2 == 1:
                        text += '\n'
                    if not (tagsField == '' or tagsField == ' '):
                        text += 'Tags:   '
                        text += tagsField
                        exists = 1
                    else:
                        exists = 0
                    if exists == 1:
                        text += '        '
                    if not (statusField == '' or statusField == ' '):
                        text += 'Status:   '
                        text += statusField
                        exists2 = 1
                    else:                        
                        exists2 = 0
                    if exists == 1 or exists2 == 1:
                        text += '\n'
                    if not (dateField == '' or dateField == ' '):
                        text += 'Date:   '
                        text += dateField
                        exists = 1
                    else:
                        exists = 0
                    if exists == 1:
                        text += '        '
                    if not (authorField == '' or authorField == ' '):
                        text += 'Author:   '
                        text += authorField
                        exists2 = 1
                    else:
                        exists2 = 0
                    if exists2 == 1:
                        text += '        '
                    if not (versionField == '' or versionField == ' '):
                        text += 'Version:   '
                        text += versionField
                        exists3 = 1
                    else:
                        exists3 = 0
                    if exists == 1 or exists2 == 1 or exists3 == 1:
                        text += '\n'
                    if not (commentsField == '' or commentsField == ' '):
                        text += 'Comments:   '
                        text += commentsField
                        exists = 1
                    
                    item.setText(text)
                else:
                    item.setText(url)
                item.setStatusTip(url)
                
        if changeMode.currentMode == 1: #If run dynamically
            if os.path.exists(url):
                fileLocation = os.getcwd()
                fileLocation = fileLocation + '\\AssetManagerFiles\\'
                itemSplit = []
                itemPath = url.split('\\')
                itemPath = filter(None, itemPath)
                itemName = itemPath[len(itemPath)-1]
                itemNameExt = itemName
                itemName = (itemName.split('.', 1)[0])
                tempPath = itemName + 'temp.png'
                tempPath2 = itemName + '.png'
                if str(url).endswith(('.gif', '.jpg', '.tif',
                                      '.png', '.tiff', '.bmp', '.ico')) == True:
                    item = QtGui.QListWidgetItem(url, listVar)
                    icon = QtGui.QIcon()
                    icon.addFile(tempPath2,QtCore.QSize(72,72))
                    pixmap = icon.pixmap(QtCore.QSize(72,72),
                                         QtGui.QIcon.Normal,
                                         QtGui.QIcon.Off)
                    item.setIcon(icon)
                    pixmap.save((tempPath), 'PNG', 1)
                    blobValue = open(tempPath, 'rb').read()
                    data = (itemNameExt, url, blobValue)
                    ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                    os.remove(str(tempPath))
                else:                    
                    item = QtGui.QListWidgetItem(url)
                    QtGui.QListWidget.addItem(listVar, item)
                data = 0
                try:
                    data = ex("SELECT Data FROM Icons WHERE Name=%s",itemNameExt)
                except:
                    pass
                if data >= 1:
                    imgFile = open(tempPath2, 'wb')
                    imgFile.write(cur.fetchone()[0])
                    imgFile.close
                    item = QtGui.QListWidgetItem(url, listVar)
                    icon = QtGui.QIcon()
                    icon.addFile(tempPath2,QtCore.QSize(72,72))
                    pixmap = icon.pixmap(QtCore.QSize(72,72),
                                         QtGui.QIcon.Normal,
                                         QtGui.QIcon.Off)
                    item.setIcon(icon)
                else:
                    if str(url).endswith(('.gif', '.jpg', '.tif',
                                          '.png', '.tiff', '.bmp', '.ico')) == True:
                        item = QtGui.QListWidgetItem(url, listVar)
                        icon = QtGui.QIcon()
                        icon.addFile(url,QtCore.QSize(72,72))
                        pixmap = icon.pixmap(QtCore.QSize(72,72),
                                             QtGui.QIcon.Normal,
                                             QtGui.QIcon.Off)
                        item.setIcon(icon)
                        pixmap.save((tempPath), 'PNG', 1)
                        blobValue = open(tempPath, 'rb').read()
                        data = (itemNameExt, url, blobValue)
                        ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                        os.remove(str(tempPath))
                    else:                    
                        item = QtGui.QListWidgetItem(url)
                        QtGui.QListWidget.addItem(listVar, item)
                item.setStatusTip(url)
                data = 0
                try:
                    data = ex("SELECT * FROM Properties WHERE File=%s",itemNameExt)
                except:
                    pass
                if data >= 1:
                    data = cur.fetchone()
                    fileField = data[0]
                    locationField = data[1]
                    nameField = data[2]
                    categoryField = data[3]
                    tagsField = data[4]
                    statusField = data[5]
                    dateField = data[6]
                    authorField = data[7]
                    versionField = data[8]
                    commentsField = data[9]
                    text = 'File:   '
                    text += fileField
                    text += '\nLocation:   '
                    text += locationField
                    text += '\n'                  
                    if not (nameField == '' or nameField == ' '):
                        text += 'Name:   '
                        text += nameField
                        exists = 1
                    else:
                        exists = 0
                    if exists == 1:
                        text += '        '
                    if not (categoryField == '' or categoryField == ' '):
                        text += 'Category:   '
                        text += categoryField
                        exists2 = 1
                    else:
                        exists2 = 0
                    if exists == 1 or exists2 == 1:
                        text += '\n'
                    if not (tagsField == '' or tagsField == ' '):
                        text += 'Tags:   '
                        text += tagsField
                        exists = 1
                    else:
                        exists = 0
                    if exists == 1:
                        text += '        '
                    if not (statusField == '' or statusField == ' '):
                        text += 'Status:   '
                        text += statusField
                        exists2 = 1
                    else:                        
                        exists2 = 0
                    if exists == 1 or exists2 == 1:
                        text += '\n'
                    if not (dateField == '' or dateField == ' '):
                        text += 'Date:   '
                        text += dateField
                        exists = 1
                    else:
                        exists = 0
                    if exists == 1:
                        text += '        '
                    if not (authorField == '' or authorField == ' '):
                        text += 'Author:   '
                        text += authorField
                        exists2 = 1
                    else:
                        exists2 = 0
                    if exists2 == 1:
                        text += '        '
                    if not (versionField == '' or versionField == ' '):
                        text += 'Version:   '
                        text += versionField
                        exists3 = 1
                    else:
                        exists3 = 0
                    if exists == 1 or exists2 == 1 or exists3 == 1:
                        text += '\n'
                    if not (commentsField == '' or commentsField == ' '):
                        text += 'Comments:   '
                        text += commentsField
                        exists = 1
                    item.setText(text)
                else:
                    item.setText(url)

                item.setStatusTip(url)

    def saveAssetFile(self):
        '''Sava asset manager file to disc'''
        if changeMode.currentMode == 0: #If run locally
            fileToSave = QtGui.QFileDialog.getSaveFileName(self, 'Save file',
                                                           '', ("(*.asset)"))
            file = open(fileToSave, 'w+')
            file.write('[Project]\n')
            file.write('Name = ' + 'MyProject' + '\n\n')
            file.write('[Projects]\n')
            file.write('Items = \n')
            items = self.projects_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.projects_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Models]\n')
            file.write('Items = \n')
            items = self.models_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.models_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Shaders]\n')
            file.write('Items = \n')
            items = self.shaders_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.shaders_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Images]\n')
            file.write('Items = \n')
            items = self.images_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.images_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Videos]\n')
            file.write('Items = \n')
            items = self.videos_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.videos_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Audio]\n')
            file.write('Items = \n')
            items = self.audio_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.audio_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Scripts]\n')
            file.write('Items = \n')
            items = self.scripts_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.scripts_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Simulations]\n')
            file.write('Items = \n')
            items = self.simulations_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.simulations_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.close
            
        if changeMode.currentMode == 1: #If run dynamically
            fileToSave = QtGui.QFileDialog.getSaveFileName(self, 'Save file',
                                                           '', ("(*.asset)"))
            file = open(fileToSave, 'w+')
            file.write('[Project]\n')
            file.write('Name = ' + 'MyProject' + '\n\n')
            file.write('[Projects]\n')
            file.write('Items = \n')
            items = self.projects_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.projects_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Models]\n')
            file.write('Items = \n')
            items = self.models_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.models_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Shaders]\n')
            file.write('Items = \n')
            items = self.shaders_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.shaders_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Images]\n')
            file.write('Items = \n')
            items = self.images_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.images_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Videos]\n')
            file.write('Items = \n')
            items = self.videos_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.videos_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Audio]\n')
            file.write('Items = \n')
            items = self.audio_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.audio_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Scripts]\n')
            file.write('Items = \n')
            items = self.scripts_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.scripts_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.write('[Simulations]\n')
            file.write('Items = \n')
            items = self.simulations_listView.count()
            selectedItems=[]
            rangedList =range(items)
            for i in rangedList:
                    file.write('\t')
                    file.write(self.simulations_listView.item(i).text())
                    file.write('\n')
            file.write('\n\n')
            file.close
                      
    def itemDropped(self, l, listVar):
        '''Import item when drag and dropped'''
        selectedItem = self.findSelection(listVar)
        if not selectedItem == '':
            pass
        if changeMode.currentMode == 0:
            for url in l:
                if os.path.exists(url):
                    fileLocation = os.getcwd()
                    fileLocation = fileLocation + '\\AssetManagerFiles\\'
                    itemSplit = []
                    url = os.path.abspath(url)
                    itemPath = url.split('\\')
                    itemPath = filter(None, itemPath)
                    itemName = itemPath[len(itemPath)-1]
                    itemNameExt = itemName
                    itemName = (itemName.split('.', 1)[0])
                    tempPath= fileLocation + itemName + '.png'
                    if os.path.exists(fileLocation + itemName + '.png'):
                        item = QtGui.QListWidgetItem(url, listVar)
                        icon = QtGui.QIcon()
                        icon.addFile(tempPath,QtCore.QSize(72,72))
                        pixmap = icon.pixmap(QtCore.QSize(72,72),
                                             QtGui.QIcon.Normal,
                                             QtGui.QIcon.Off)
                        item.setIcon(icon)
                    else:
                        if str(url).endswith(('.gif', '.jpg', '.tif',
                                              '.png', '.tiff', '.bmp', '.ico')) == True:
                            item = QtGui.QListWidgetItem(url, listVar)
                            icon = QtGui.QIcon()
                            icon.addFile(url,QtCore.QSize(72,72))
                            pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                 QtGui.QIcon.Normal,
                                                 QtGui.QIcon.Off)
                            item.setIcon(icon)
                        else:                    
                            item = QtGui.QListWidgetItem(url)
                            QtGui.QListWidget.addItem(listVar, item)
                    if os.path.exists(fileLocation + itemName + '.properties'):
                        config = ConfigParser.ConfigParser()
                        wholeFile = str(fileLocation + itemName + '.properties')
                        config.read(wholeFile)
                        fileField = itemNameExt
                        locationField = url
                        nameField = config.get('Name', 'Name')
                        categoryField = config.get('Category', 'Category')
                        tagsField = config.get('Tags', 'Tags')
                        statusField = config.get('Status', 'Status')
                        dateField = config.get('Date Updated', 'Date')
                        authorField = config.get('Author', 'Author')
                        versionField = config.get('Version', 'Version')
                        commentsField = config.get('Comments', 'Comments')
                        text = 'File:   '
                        text += fileField
                        text += '\nLocation:   '
                        text += locationField
                        text += '\n'
                        if not (nameField == '' or nameField == ' '):
                            text += 'Name:   '
                            text += nameField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (categoryField == '' or categoryField == ' '):
                            text += 'Category:   '
                            text += categoryField
                            exists2 = 1
                        else:
                            exists2 = 0
                        if exists == 1 or exists2 == 1:
                            text += '\n'
                        if not (tagsField == '' or tagsField == ' '):
                            text += 'Tags:   '
                            text += tagsField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (statusField == '' or statusField == ' '):
                            text += 'Status:   '
                            text += statusField
                            exists2 = 1
                        else:                        
                            exists2 = 0
                        if exists == 1 or exists2 == 1:
                            text += '\n'
                        if not (dateField == '' or dateField == ' '):
                            text += 'Date:   '
                            text += dateField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (authorField == '' or authorField == ' '):
                            text += 'Author:   '
                            text += authorField
                            exists2 = 1
                        else:
                            exists2 = 0
                        if exists2 == 1:
                            text += '        '
                        if not (versionField == '' or versionField == ' '):
                            text += 'Version:   '
                            text += versionField
                            exists3 = 1
                        else:
                            exists3 = 0
                        if exists == 1 or exists2 == 1 or exists3 == 1:
                            text += '\n'
                        if not (commentsField == '' or commentsField == ' '):
                            text += 'Comments:   '
                            text += commentsField
                            exists = 1
                        item.setText(text)
                    else:
                        item.setText(url)
                    item.setStatusTip(url)
                    
        if changeMode.currentMode == 1: #If run dynamically
            for url in l:
                if os.path.exists(url):
                    fileLocation = os.getcwd()
                    fileLocation = fileLocation + '\\AssetManagerFiles\\'
                    itemSplit = []
                    url = os.path.abspath(url)
                    itemPath = url.split('\\')
                    itemPath = filter(None, itemPath)
                    itemName = itemPath[len(itemPath)-1]
                    itemNameExt = itemName
                    itemName = (itemName.split('.', 1)[0])
                    tempPath= fileLocation + itemName + 'temp.png'
                    tempPath2= fileLocation + itemName + '.png'
                    data = 0
                    try:
                        data = ex("SELECT Data FROM Icons WHERE Name=%s",itemNameExt)
                    except:
                        pass
                    if data >= 1:
                        imgFile = open(tempPath2, 'wb')
                        imgFile.write(cur.fetchone()[0])
                        imgFile.close
                        item = QtGui.QListWidgetItem(url, listVar)
                        icon = QtGui.QIcon()
                        icon.addFile(tempPath2,QtCore.QSize(72,72))
                        pixmap = icon.pixmap(QtCore.QSize(72,72),
                                             QtGui.QIcon.Normal,
                                             QtGui.QIcon.Off)
                        item.setIcon(icon)
                    else:
                        if str(url).endswith(('.gif', '.jpg', '.tif',
                                              '.png', '.tiff', '.bmp', '.ico')) == True:
                            item = QtGui.QListWidgetItem(url, listVar)
                            icon = QtGui.QIcon()
                            icon.addFile(url,QtCore.QSize(72,72))
                            pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                 QtGui.QIcon.Normal,
                                                 QtGui.QIcon.Off)
                            item.setIcon(icon)
                            pixmap.save((tempPath), 'PNG', 1)
                            blobValue = open(tempPath, 'rb').read()
                            data = (itemNameExt, url, blobValue)
                            ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                            os.remove(str(tempPath))
                        else:                    
                            item = QtGui.QListWidgetItem(url)
                            QtGui.QListWidget.addItem(listVar, item)
                    item.setStatusTip(url)
                    data = 0
                    try:
                        data = ex("SELECT * FROM Properties WHERE File=%s",itemNameExt)
                    except:
                        pass
                    if data >= 1:
                        data = cur.fetchone()
                        fileField = data[0]
                        locationField = data[1]
                        nameField = data[2]
                        categoryField = data[3]
                        tagsField = data[4]
                        statusField = data[5]
                        dateField = data[6]
                        authorField = data[7]
                        versionField = data[8]
                        commentsField = data[9]
                        text = 'File:   '
                        text += fileField
                        text += '\nLocation:   '
                        text += locationField
                        text += '\n'
                        if not (nameField == '' or nameField == ' '):
                            text += 'Name:   '
                            text += nameField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (categoryField == '' or categoryField == ' '):
                            text += 'Category:   '
                            text += categoryField
                            exists2 = 1
                        else:
                            exists2 = 0
                        if exists == 1 or exists2 == 1:
                            text += '\n'
                        if not (tagsField == '' or tagsField == ' '):
                            text += 'Tags:   '
                            text += tagsField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (statusField == '' or statusField == ' '):
                            text += 'Status:   '
                            text += statusField
                            exists2 = 1
                        else:                        
                            exists2 = 0
                        if exists == 1 or exists2 == 1:
                            text += '\n'
                        if not (dateField == '' or dateField == ' '):
                            text += 'Date:   '
                            text += dateField
                            exists = 1
                        else:
                            exists = 0
                        if exists == 1:
                            text += '        '
                        if not (authorField == '' or authorField == ' '):
                            text += 'Author:   '
                            text += authorField
                            exists2 = 1
                        else:
                            exists2 = 0
                        if exists2 == 1:
                            text += '        '
                        if not (versionField == '' or versionField == ' '):
                            text += 'Version:   '
                            text += versionField
                            exists3 = 1
                        else:
                            exists3 = 0
                        if exists == 1 or exists2 == 1 or exists3 == 1:
                            text += '\n'
                        if not (commentsField == '' or commentsField == ' '):
                            text += 'Comments:   '
                            text += commentsField
                            exists = 1
                        item.setText(text)
                    else:
                        item.setText(url)
                    item.setStatusTip(url)
                    
    def contextActions(self, actions, listVar):
        '''Setup actions for menus'''
        listVar.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        listVar.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        listVar.doubleClicked.connect(lambda : self.openFile(listVar))
        actions[6].addAction(actions[7])
        actions[6].addAction(actions[8])
        actions[6].addAction(actions[9])
        actions[6].addAction(actions[10])
        actions[6].addAction(actions[11])
        actions[6].addAction(actions[12])
        actions[1].setMenu(actions[6])
        actions[7].setStatusTip('Open file with Maya')
        actions[8].setStatusTip('Open file with Houdini')
        actions[9].setStatusTip('Open file with Nuke')
        actions[10].setStatusTip('Open file with Photoshop')
        actions[11].setStatusTip('Open file with Text Editor')
        actions[12].setStatusTip('Open file with Image Viewer')
        actions[7].triggered.connect(lambda : self.openFileWithMaya(listVar))
        actions[8].triggered.connect(lambda : self.openFileWithHoudini(listVar))
        actions[9].triggered.connect(lambda : self.openFileWithNuke(listVar))
        actions[10].triggered.connect(lambda : self.openFileWithPhotoshop(listVar))
        actions[11].triggered.connect(lambda : self.openFileWithTextEditor(listVar))
        actions[12].triggered.connect(lambda : self.openFileWithImageViewer(listVar))
        listVar.addAction(actions[0])
        listVar.addAction(actions[1])
        #listVar.addAction(actions[2]) //preview //Future Implementation
        listVar.addAction(actions[3])
        listVar.addAction(actions[4])
        listVar.addAction(actions[5])
        actions[0].setStatusTip('Open selected file with default program')
        actions[1].setStatusTip('Open selected file with chosen program')
        #actions[2].setStatusTip('Preview file if possible') //preview //Future Implementation
        actions[3].setStatusTip('View and edit properties of file')
        actions[4].setStatusTip('Import file into asset manager')
        actions[5].setStatusTip('Remove selected file/s from asset manager')
        actions[5].setShortcut('Delete')
        actions[0].triggered.connect(lambda : self.openFile(listVar))
        actions[2].triggered.connect(lambda : self.previewFile(listVar))
        actions[3].triggered.connect(lambda : self.fileProperties(listVar))
        actions[5].triggered.connect(lambda : self.deleteEntry(listVar))
        actions[4].triggered.connect(lambda : self.importEntry("Projects", listVar))
        actions[0].setEnabled(False)
        actions[1].setEnabled(False)
        #actions[2].setEnabled(False) //preview //Future Implementation
        actions[3].setEnabled(False)
        actions[5].setEnabled(False)
        
    def connectToDB(self):
        '''Toggle between locally and dynamically using the program'''
        if changeMode.currentMode == 0: #If run locally
            username = Ui_MainWindow.window.username_lineEdit.text()
            password = Ui_MainWindow.window.password_lineEdit.text()
            address = Ui_MainWindow.window.address_lineEdit.text()
            databaseName = Ui_MainWindow.window.database_lineEdit.text()
            if not (username == '' or username == ' ' or password == '' or password == ' ' or address == '' or address == ' ' or databaseName == '' or databaseName == ' '):    
                try:
                    database = mysql.connect(user=str(username), host=str(address), passwd=str(password), db=str(databaseName))
                except:
                    QtGui.QMessageBox.critical(self,
                                "Error",
                                "Could not connect to database!\nPlease check login info!")
                global cur
                cur = database.cursor()
                global ex
                ex = cur.execute
                try:
                    ex('CREATE TABLE IF NOT EXISTS AssetManager (P_Id int NOT NULL AUTO_INCREMENT, Settings text, Bookmarks text, Shots text, Projects text, Models text, Shaders text, Images text, Videos text, Audio text, Scripts text, Simulations text, PRIMARY KEY(P_Id))')
                except:
                    pass
                try:
                    ex('CREATE TABLE IF NOT EXISTS Properties (File VARCHAR(100), Location text, Name text, Category text, Tags text, Status text, Date text, Author text, Version text, Comments text, PRIMARY KEY(File))')
                except:
                    pass
                try:
                    ex('CREATE TABLE IF NOT EXISTS Icons (Name VARCHAR(100), Location text, Data LONGBLOB, PRIMARY KEY(Name))')
                except:
                    pass
                changeMode.currentMode = 1
                QtGui.QMessageBox.information(self,
                    "Connected",
                    "You have connected to the server!")
            else:
                QtGui.QMessageBox.critical(self,
                                "Error",
                                "All fields are required to login!")
                
        elif changeMode.currentMode == 1: #If run dynamically
            changeMode.currentMode = 0
            QtGui.QMessageBox.information(self,
                "Disconnected",
                "You have disconnected from the server!")
            
    def setFolder(self):
        '''Add a folder of asset manager files to list'''
        url = QtGui.QFileDialog.getExistingDirectory(self, 'Select Folder containing asset files','')
        onlyfiles = [ f for f in os.listdir(str(url)) if os.path.isfile(os.path.join(str(url),f)) ]
        files=[]
        for item in onlyfiles:
            if item.endswith(".asset"):
                file = str(url) + str(item)
                fileEntry = QtGui.QListWidgetItem(file, self.listWidget_2)
                fileEntry.setText(str(item))
                fileEntry.setStatusTip(str(file))

    def addFile(self):
        '''Add asset file to saved list'''
        url = QtGui.QFileDialog.getOpenFileName(self, 'Select asset file to add',
                                                '', ("Select Asset: (*.Asset)"))
        fileEntry = QtGui.QListWidgetItem(url, self.listWidget_2)
        itemSplit = []
        url = os.path.abspath(url)
        itemPath = url.split('\\')
        itemPath = filter(None, itemPath)
        itemName = itemPath[len(itemPath)-1]
        fileEntry.setText(str(itemName))
        fileEntry.setStatusTip(str(url))
        
    def removeFile(self):
        '''Remove file from list'''
        item = self.listWidget_2.takeItem(self.listWidget_2.currentRow())
        item = None
        
    def refreshItems(self):
        '''Refresh items properties'''
        tabs = [self.projects_listView, self.models_listView, self.shaders_listView, self.images_listView, self.videos_listView, self.audio_listView, self.scripts_listView, self.simulations_listView]
        for listVar in tabs:
            items = listVar.count()
            selectedItems=[]
            rangedList =range(items)
            rangedList.reverse()
            if changeMode.currentMode == 0: #If run locally
                for i in rangedList:
                    url = listVar.item(i).statusTip()
                    listVar.takeItem(i)
                    if os.path.exists(url):
                        fileLocation = os.getcwd()
                        fileLocation = fileLocation + '\\AssetManagerFiles\\'
                        itemSplit = []
                        itemPath = url.split('\\')
                        itemPath = filter(None, itemPath)
                        itemName = itemPath[len(itemPath)-1]
                        itemNameExt = itemName
                        itemName = (itemName.split('.', 1)[0])
                        tempPath= fileLocation + itemName + '.png'
                        if os.path.exists(tempPath):
                            item = QtGui.QListWidgetItem(url)
                            QtGui.QListWidget.insertItem(listVar, i, item)
                            icon = QtGui.QIcon()
                            icon.addFile(tempPath,QtCore.QSize(72,72))
                            pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                 QtGui.QIcon.Normal,
                                                 QtGui.QIcon.Off)
                            item.setIcon(icon)
                        else:
                            if str(url).endswith(('.gif', '.jpg', '.tif',
                                                  '.png', '.tiff', '.bmp', '.ico')) == True:
                                item = QtGui.QListWidgetItem(url)
                                QtGui.QListWidget.insertItem(listVar, i, item)
                                icon = QtGui.QIcon()
                                icon.addFile(url,QtCore.QSize(72,72))
                                pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                     QtGui.QIcon.Normal,
                                                     QtGui.QIcon.Off)
                                item.setIcon(icon)
                            else:                    
                                item = QtGui.QListWidgetItem(url)
                                QtGui.QListWidget.insertItem(listVar, i, item)
                        item.setStatusTip(url)
                        if os.path.exists(fileLocation + itemName + '.properties'):
                            config = ConfigParser.ConfigParser()
                            wholeFile = str(fileLocation + itemName + '.properties')
                            config.read(wholeFile)
                            fileField = itemNameExt
                            locationField = url
                            nameField = config.get('Name', 'Name')
                            categoryField = config.get('Category', 'Category')
                            tagsField = config.get('Tags', 'Tags')
                            statusField = config.get('Status', 'Status')
                            dateField = config.get('Date Updated', 'Date')
                            authorField = config.get('Author', 'Author')
                            versionField = config.get('Version', 'Version')
                            commentsField = config.get('Comments', 'Comments')
                            text = 'File:   '
                            text += fileField
                            text += '\nLocation:   '
                            text += locationField
                            text += '\n'
                            if not (nameField == '' or nameField == ' '):
                                text += 'Name:   '
                                text += nameField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (categoryField == '' or categoryField == ' '):
                                text += 'Category:   '
                                text += categoryField
                                exists2 = 1
                            else:
                                exists2 = 0
                            if exists == 1 or exists2 == 1:
                                text += '\n'
                            if not (tagsField == '' or tagsField == ' '):
                                text += 'Tags:   '
                                text += tagsField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (statusField == '' or statusField == ' '):
                                text += 'Status:   '
                                text += statusField
                                exists2 = 1
                            else:                        
                                exists2 = 0
                            if exists == 1 or exists2 == 1:
                                text += '\n'
                            if not (dateField == '' or dateField == ' '):
                                text += 'Date:   '
                                text += dateField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (authorField == '' or authorField == ' '):
                                text += 'Author:   '
                                text += authorField
                                exists2 = 1
                            else:
                                exists2 = 0
                            if exists2 == 1:
                                text += '        '
                            if not (versionField == '' or versionField == ' '):
                                text += 'Version:   '
                                text += versionField
                                exists3 = 1
                            else:
                                exists3 = 0
                            if exists == 1 or exists2 == 1 or exists3 == 1:
                                text += '\n'
                            if not (commentsField == '' or commentsField == ' '):
                                text += 'Comments:   '
                                text += commentsField
                                exists = 1
                            item.setText(text)
                        else:
                            item.setText(url)
                        item.setStatusTip(url)

            if changeMode.currentMode == 1: #If run dynamically
                for i in rangedList:
                    url = listVar.item(i).statusTip()
                    listVar.takeItem(i)
                    if os.path.exists(url):
                        fileLocation = os.getcwd()
                        fileLocation = fileLocation + '\\AssetManagerFiles\\'
                        itemSplit = []
                        itemPath = url.split('\\')
                        itemPath = filter(None, itemPath)
                        itemName = itemPath[len(itemPath)-1]
                        itemNameExt = itemName
                        itemName = (itemName.split('.', 1)[0])
                        tempPath= fileLocation + itemName + 'temp.png'
                        tempPath2= fileLocation + itemName + '.png'
                        data = 0
                        try:
                            data = ex("SELECT Data FROM Icons WHERE Name=%s",itemNameExt)
                        except:
                            pass
                        if data >= 1:
                            imgFile = open(tempPath2, 'wb')
                            imgFile.write(cur.fetchone()[0])
                            imgFile.close
                            item = QtGui.QListWidgetItem(url)
                            QtGui.QListWidget.insertItem(listVar, i, item)
                            icon = QtGui.QIcon()
                            icon.addFile(tempPath2,QtCore.QSize(72,72))
                            pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                 QtGui.QIcon.Normal,
                                                 QtGui.QIcon.Off)
                            item.setIcon(icon)
                        else:
                            if str(url).endswith(('.gif', '.jpg', '.tif',
                                                  '.png', '.tiff', '.bmp', '.ico')) == True:
                                item = QtGui.QListWidgetItem(url)
                                QtGui.QListWidget.insertItem(listVar, i, item)
                                icon = QtGui.QIcon()
                                icon.addFile(url,QtCore.QSize(72,72))
                                pixmap = icon.pixmap(QtCore.QSize(72,72),
                                                     QtGui.QIcon.Normal,
                                                     QtGui.QIcon.Off)
                                item.setIcon(icon)
                                pixmap.save((tempPath), 'PNG', 1)
                                blobValue = open(tempPath, 'rb').read()
                                data = (itemNameExt, url, blobValue)
                                ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                                os.remove(str(tempPath))                                          
                            else:
                                item = QtGui.QListWidgetItem(url)
                                QtGui.QListWidget.insertItem(listVar, i, item)
                        item.setStatusTip(url)
                        data = 0
                        try:
                            data = ex("SELECT * FROM Properties WHERE File=%s",itemNameExt)
                        except:
                            pass
                        if data >= 1:
                            data = cur.fetchone()
                            fileField = data[0]
                            locationField = data[1]
                            nameField = data[2]
                            categoryField = data[3]
                            tagsField = data[4]
                            statusField = data[5]
                            dateField = data[6]
                            authorField = data[7]
                            versionField = data[8]
                            commentsField = data[9]
                            text = 'File:   '
                            text += fileField
                            text += '\nLocation:   '
                            text += locationField
                            text += '\n'
                            if not (nameField == '' or nameField == ' '):
                                text += 'Name:   '
                                text += nameField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (categoryField == '' or categoryField == ' '):
                                text += 'Category:   '
                                text += categoryField
                                exists2 = 1
                            else:
                                exists2 = 0
                            if exists == 1 or exists2 == 1:
                                text += '\n'
                            if not (tagsField == '' or tagsField == ' '):
                                text += 'Tags:   '
                                text += tagsField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (statusField == '' or statusField == ' '):
                                text += 'Status:   '
                                text += statusField
                                exists2 = 1
                            else:                        
                                exists2 = 0
                            if exists == 1 or exists2 == 1:
                                text += '\n'
                            if not (dateField == '' or dateField == ' '):
                                text += 'Date:   '
                                text += dateField
                                exists = 1
                            else:
                                exists = 0
                            if exists == 1:
                                text += '        '
                            if not (authorField == '' or authorField == ' '):
                                text += 'Author: -=  '
                                text += authorField
                                exists2 = 1
                            else:
                                exists2 = 0
                            if exists2 == 1:
                                text += '        '
                            if not (versionField == '' or versionField == ' '):
                                text += 'Version:   '
                                text += versionField
                                exists3 = 1
                            else:
                                exists3 = 0
                            if exists == 1 or exists2 == 1 or exists3 == 1:
                                text += '\n'
                            if not (commentsField == '' or commentsField == ' '):
                                text += 'Comments:   '
                                text += commentsField
                                exists = 1
                            item.setText(text)
                        else:
                            item.setText(url)
                        item.setStatusTip(url)

    def interfaceColor1(self):
        '''Set interface color to dark'''
        Ui_MainWindow.window.projects_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.models_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.shaders_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.images_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.videos_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.audio_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.scripts_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.simulations_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        changeMode.MainWindow.setStyleSheet('background-color: darkgrey')
        Ui_MainWindow.window.address_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        Ui_MainWindow.window.username_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        Ui_MainWindow.window.password_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        Ui_MainWindow.window.database_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        Ui_MainWindow.window.connect_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.setFolder_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.addFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.removeFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.listWidget_2.setStyleSheet('background-color: rgb(200,200,200)')
        Ui_MainWindow.window.statusbar.setStyleSheet('background-color: rgb(200,200,200)')
        Ui_MainWindow.window.menubar.setStyleSheet('QMenuBar {background-color: rgb(200,200,200)} QMenuBar::item {background-color: transparent;} QMenuBar::item:selected {background-color: rgb(240,240,240);}  QMenuBar::item:inactive{color: black}')
        Ui_MainWindow.window.menuFile.setStyleSheet('QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;}')
        Ui_MainWindow.window.menuEdit.setStyleSheet('QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;}')
        Ui_MainWindow.window.menuDisplay.setStyleSheet('QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;}')
        Ui_MainWindow.window.listWidget_2.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.main_tabWidget.setStyleSheet('QTabWidget::pane {border: 1px solid grey;} QTabWidget {border: 1px solid grey; padding: 0px;} QTabBar::tab {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D8D8D8, stop: 0.4 #C5C5C5, stop: 0.5 #B6B6B6, stop: 1.0 #A2A2A2); border: 2px solid #C4C4C3; border-bottom-color: #C2C7CB;  border-top-left-radius: 4px; border-top-right-radius: 4px; min-width: 21ex; padding: 2px;} QTabBar::tab:selected, QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}')
        Ui_MainWindow.window.simulations_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.scripts_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.audio_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.videos_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.images_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.shaders_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.Models_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.projects_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.interfaceColor = 1

    def interfaceColor2(self):
        '''Set interface color to light'''
        Ui_MainWindow.window.projects_listView.setStyleSheet('QListView { border: 0px} QMenu {border: 2px solid darkgrey; ; color: black} QMenu::item:selected { color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {  color:black} QListWidget:item:hover {  color:black}')
        Ui_MainWindow.window.models_listView.setStyleSheet('QListView { border: 0px} QMenu {border: 2px solid darkgrey; ; color: black} QMenu::item:selected { color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {  color:black} QListWidget:item:hover {  color:black}')
        Ui_MainWindow.window.shaders_listView.setStyleSheet('QListView { border: 0px} QMenu {border: 2px solid darkgrey; ; color: black} QMenu::item:selected { color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {  color:black} QListWidget:item:hover {  color:black}')
        Ui_MainWindow.window.images_listView.setStyleSheet('QListView { border: 0px} QMenu {border: 2px solid darkgrey; ; color: black} QMenu::item:selected { color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {  color:black} QListWidget:item:hover {  color:black}')
        Ui_MainWindow.window.videos_listView.setStyleSheet('QListView { border: 0px} QMenu {border: 2px solid darkgrey; ; color: black} QMenu::item:selected { color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {  color:black} QListWidget:item:hover {  color:black}')
        Ui_MainWindow.window.audio_listView.setStyleSheet('QListView { border: 0px} QMenu {border: 2px solid darkgrey; ; color: black} QMenu::item:selected { color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {  color:black} QListWidget:item:hover {  color:black}')
        Ui_MainWindow.window.scripts_listView.setStyleSheet('QListView { border: 0px} QMenu {border: 2px solid darkgrey; ; color: black} QMenu::item:selected { color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {  color:black} QListWidget:item:hover {  color:black}')
        Ui_MainWindow.window.simulations_listView.setStyleSheet('QListView { border: 0px} QMenu {border: 2px solid darkgrey; ; color: black} QMenu::item:selected { color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {  color:black} QListWidget:item:hover {  color:black}')
        changeMode.MainWindow.setStyleSheet('')
        Ui_MainWindow.window.address_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; ; color:black}')
        Ui_MainWindow.window.username_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; ; color:black}')
        Ui_MainWindow.window.password_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; ; color:black}')
        Ui_MainWindow.window.database_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; ; color:black}')
        Ui_MainWindow.window.connect_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.setFolder_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.addFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.removeFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.listWidget_2.setStyleSheet('')
        Ui_MainWindow.window.statusbar.setStyleSheet('')
        Ui_MainWindow.window.menubar.setStyleSheet('QMenuBar {background-color: rgb(240,240,240)} QMenuBar::item {background-color: transparent;} QMenuBar::item:selected QMenuBar::item:inactive{color: black}')
        Ui_MainWindow.window.menuFile.setStyleSheet('QMenu { border: 2px solid darkgrey; color: black} QMenu::item:selected { color: black;}')
        Ui_MainWindow.window.menuEdit.setStyleSheet('QMenu { border: 2px solid darkgrey; color: black} QMenu::item:selected { color: black;}')
        Ui_MainWindow.window.menuDisplay.setStyleSheet('QMenu { border: 2px solid darkgrey; color: black} QMenu::item:selected { color: black;}')
        Ui_MainWindow.window.listWidget_2.setStyleSheet('QListView {; border: 0px} QMenu {; border: 2px solid darkgrey; color: black} QMenu::item:selected { color: black;} QListWidget:item:selected:active {  color:black} QListWidget:item:hover {  color:black}')
        Ui_MainWindow.window.main_tabWidget.setStyleSheet('QTabWidget::pane {border: 1px solid grey;} QTabWidget {border: 1px solid grey; padding: 0px;} QTabBar::tab {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FFFFFF, stop: 0.4 #EEEEEE, stop: 0.5 #DDDDDD, stop: 1.0 #CCCCCC); border: 2px solid #C4C4C3; border-bottom-color: #C2C7CB;  border-top-left-radius: 4px; border-top-right-radius: 4px; min-width: 21ex; padding: 2px;} QTabBar::tab:selected, QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}')
        Ui_MainWindow.window.simulations_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.scripts_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.audio_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.videos_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.images_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.shaders_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.Models_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.projects_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.interfaceColor = 2
        
    def interfaceColorCustom(self):
        '''Set custom interface color'''
        ui = ColorPicker()
        ui.exec_()

    def copyItem(self):
        '''Copy selected item'''
        currentTab = self.main_tabWidget.currentIndex()
        currentTab = str(self.main_tabWidget.tabText(currentTab).toLower())
        currentTab = 'self.' + currentTab + '_listView'
        currentTab = eval(currentTab)
        items = currentTab.count()
        selectedItems=[]
        rangedList =range(items)
        rangedList.reverse()
        Ui_MainWindow.copiedItems = []
        for i in rangedList:
            if currentTab.isItemSelected(currentTab.item(i))==True:
                Ui_MainWindow.copiedItems.append(str(currentTab.item(i).statusTip()))        

    def pasteItem(self):
        '''Paste selected item'''
        currentTab = self.main_tabWidget.currentIndex()
        currentTab = str(self.main_tabWidget.tabText(currentTab).toLower())
        currentTab = 'self.' + currentTab + '_listView'
        currentTab = eval(currentTab)
        Ui_MainWindow.copiedItems.reverse()
        for item in Ui_MainWindow.copiedItems:
            self.addItemToList(item, currentTab)

    def deleteItem(self, listVar):
        '''Delete selected item'''
        currentTab = self.main_tabWidget.currentIndex()
        currentTab = str(self.main_tabWidget.tabText(currentTab).toLower())
        currentTab = 'self.' + currentTab + '_listView'
        currentTab = eval(currentTab)
        item = currentTab.takeItem(currentTab.currentRow())
        item = None
        
    def setupUi(self, MainWindow):
        '''Setup UI for main window'''
        changeMode()
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(783, 613)
        self.centralwidget = QtGui.QWidget(MainWindow)
        Ui_MainWindow.window = self
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.main_tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.main_tabWidget.setGeometry(QtCore.QRect(210, 5, 570, 565))
        self.main_tabWidget.setObjectName(_fromUtf8("main_tabWidget"))
        self.projects_tab = QtGui.QWidget()
        self.projects_tab.setObjectName(_fromUtf8("projects_tab"))
        self.projects_scrollArea = QtGui.QScrollArea(self.projects_tab)
        self.projects_scrollArea.setGeometry(QtCore.QRect(0, 0, 570, 545))
        self.projects_scrollArea.setMinimumSize(QtCore.QSize(550, 520))
        self.projects_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.projects_scrollArea.setWidgetResizable(True)
        self.projects_scrollArea.setObjectName(_fromUtf8("projects_scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 529, 516))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.projects_listView = DragAndDrop(self)
        self.projects_listView.setObjectName(_fromUtf8("projects_listView"))
        self.connect(self.projects_listView, QtCore.SIGNAL("dropped"), (lambda links: self.itemDropped(links, self.projects_listView)))  
        self.actionOpenProjects = QtGui.QAction("Open", self.projects_listView)        
        self.actionOpenWithProjects = QtGui.QAction("Open With", self.projects_listView)
        self.actionPreviewProjects = QtGui.QAction("Preview", self.projects_listView)
        self.actionPropertiesProjects = QtGui.QAction("Properties", self.projects_listView)
        self.actionImportProjects = QtGui.QAction("Import", self.projects_listView)
        self.actionDeleteProjects = QtGui.QAction("Delete", self.projects_listView)
        self.openWithProjects = QtGui.QMenu(self.projects_listView)
        self.actionOpenWithMayaProjects = QtGui.QAction("Maya", self.openWithProjects)
        self.actionOpenWithHoudiniProjects = QtGui.QAction("Houdini", self.openWithProjects)
        self.actionOpenWithNukeProjects = QtGui.QAction("Nuke", self.openWithProjects)
        self.actionOpenWithPhotoshopProjects = QtGui.QAction("Photoshop", self.openWithProjects)
        self.actionOpenWithTextEditorProjects = QtGui.QAction("Text Editor", self.openWithProjects)
        self.actionOpenWithImageViewerProjects = QtGui.QAction("Image Viewer", self.openWithProjects)
        actions = [Ui_MainWindow.window.actionOpenProjects, Ui_MainWindow.window.actionOpenWithProjects,
                   Ui_MainWindow.window.actionPreviewProjects, Ui_MainWindow.window.actionPropertiesProjects,
                   Ui_MainWindow.window.actionImportProjects, Ui_MainWindow.window.actionDeleteProjects,
                   Ui_MainWindow.window.openWithProjects, Ui_MainWindow.window.actionOpenWithMayaProjects,
                   Ui_MainWindow.window.actionOpenWithHoudiniProjects, Ui_MainWindow.window.actionOpenWithNukeProjects,
                   Ui_MainWindow.window.actionOpenWithPhotoshopProjects, Ui_MainWindow.window.actionOpenWithTextEditorProjects,
                   Ui_MainWindow.window.actionOpenWithImageViewerProjects]
        self.contextActions(actions, self.projects_listView)
        self.gridLayout.addWidget(self.projects_listView, 2, 2, 1, 1)
        self.projects_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.main_tabWidget.addTab(self.projects_tab, _fromUtf8(""))
        self.models_tab = QtGui.QWidget()
        self.models_tab.setObjectName(_fromUtf8("models_tab"))
        self.Models_scrollArea = QtGui.QScrollArea(self.models_tab)
        self.Models_scrollArea.setGeometry(QtCore.QRect(0, 0, 570, 545))
        self.Models_scrollArea.setMinimumSize(QtCore.QSize(550, 520))
        self.Models_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Models_scrollArea.setWidgetResizable(True)
        self.Models_scrollArea.setObjectName(_fromUtf8("Models_scrollArea"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 529, 516))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.models_listView = DragAndDrop(self)
        self.models_listView.setObjectName(_fromUtf8("models_listView"))
        self.connect(self.models_listView, QtCore.SIGNAL("dropped"), (lambda links: self.itemDropped(links, self.models_listView)))  
        self.actionOpenModels = QtGui.QAction("Open", self.models_listView)        
        self.actionOpenWithModels = QtGui.QAction("Open With", self.models_listView)
        self.actionPreviewModels = QtGui.QAction("Preview", self.models_listView)
        self.actionPropertiesModels = QtGui.QAction("Properties", self.models_listView)
        self.actionImportModels = QtGui.QAction("Import", self.models_listView)
        self.actionDeleteModels = QtGui.QAction("Delete", self.models_listView)
        self.openWithModels = QtGui.QMenu(self.models_listView)
        self.actionOpenWithMayaModels = QtGui.QAction("Maya", self.openWithModels)
        self.actionOpenWithHoudiniModels = QtGui.QAction("Houdini", self.openWithModels)
        self.actionOpenWithNukeModels = QtGui.QAction("Nuke", self.openWithModels)
        self.actionOpenWithPhotoshopModels = QtGui.QAction("Photoshop", self.openWithModels)
        self.actionOpenWithTextEditorModels = QtGui.QAction("Text Editor", self.openWithModels)
        self.actionOpenWithImageViewerModels = QtGui.QAction("Image Viewer", self.openWithModels)
        actions = [Ui_MainWindow.window.actionOpenModels, Ui_MainWindow.window.actionOpenWithModels,
                   Ui_MainWindow.window.actionPreviewModels, Ui_MainWindow.window.actionPropertiesModels,
                   Ui_MainWindow.window.actionImportModels, Ui_MainWindow.window.actionDeleteModels,
                   Ui_MainWindow.window.openWithModels, Ui_MainWindow.window.actionOpenWithMayaModels,
                   Ui_MainWindow.window.actionOpenWithHoudiniModels, Ui_MainWindow.window.actionOpenWithNukeModels,
                   Ui_MainWindow.window.actionOpenWithPhotoshopModels, Ui_MainWindow.window.actionOpenWithTextEditorModels,
                   Ui_MainWindow.window.actionOpenWithImageViewerModels]
        self.contextActions(actions, self.models_listView)
        self.gridLayout_2.addWidget(self.models_listView, 0, 0, 1, 1)
        self.Models_scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.main_tabWidget.addTab(self.models_tab, _fromUtf8(""))
        self.shaders_tab = QtGui.QWidget()
        self.shaders_tab.setObjectName(_fromUtf8("shaders_tab"))
        self.shaders_scrollArea = QtGui.QScrollArea(self.shaders_tab)
        self.shaders_scrollArea.setGeometry(QtCore.QRect(0, 0, 570, 545))
        self.shaders_scrollArea.setMinimumSize(QtCore.QSize(550, 520))
        self.shaders_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.shaders_scrollArea.setWidgetResizable(True)
        self.shaders_scrollArea.setObjectName(_fromUtf8("shaders_scrollArea"))
        self.scrollAreaWidgetContents_3 = QtGui.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 529, 516))
        self.scrollAreaWidgetContents_3.setObjectName(_fromUtf8("scrollAreaWidgetContents_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.shaders_listView = DragAndDrop(self)
        self.shaders_listView.setObjectName(_fromUtf8("shaders_listView"))
        self.connect(self.shaders_listView, QtCore.SIGNAL("dropped"), (lambda links: self.itemDropped(links, self.shaders_listView)))  
        self.actionOpenShaders = QtGui.QAction("Open", self.shaders_listView)        
        self.actionOpenWithShaders = QtGui.QAction("Open With", self.shaders_listView)
        self.actionPreviewShaders = QtGui.QAction("Preview", self.shaders_listView)
        self.actionPropertiesShaders = QtGui.QAction("Properties", self.shaders_listView)
        self.actionImportShaders = QtGui.QAction("Import", self.shaders_listView)
        self.actionDeleteShaders = QtGui.QAction("Delete", self.shaders_listView)
        self.openWithShaders = QtGui.QMenu(self.shaders_listView)
        self.actionOpenWithMayaShaders = QtGui.QAction("Maya", self.openWithShaders)
        self.actionOpenWithHoudiniShaders = QtGui.QAction("Houdini", self.openWithShaders)
        self.actionOpenWithNukeShaders = QtGui.QAction("Nuke", self.openWithShaders)
        self.actionOpenWithPhotoshopShaders = QtGui.QAction("Photoshop", self.openWithShaders)
        self.actionOpenWithTextEditorShaders = QtGui.QAction("Text Editor", self.openWithShaders)
        self.actionOpenWithImageViewerShaders = QtGui.QAction("Image Viewer", self.openWithShaders)
        actions = [Ui_MainWindow.window.actionOpenShaders, Ui_MainWindow.window.actionOpenWithShaders,
                   Ui_MainWindow.window.actionPreviewShaders, Ui_MainWindow.window.actionPropertiesShaders,
                   Ui_MainWindow.window.actionImportShaders, Ui_MainWindow.window.actionDeleteShaders,
                   Ui_MainWindow.window.openWithShaders, Ui_MainWindow.window.actionOpenWithMayaShaders,
                   Ui_MainWindow.window.actionOpenWithHoudiniShaders, Ui_MainWindow.window.actionOpenWithNukeShaders,
                   Ui_MainWindow.window.actionOpenWithPhotoshopShaders, Ui_MainWindow.window.actionOpenWithTextEditorShaders,
                   Ui_MainWindow.window.actionOpenWithImageViewerShaders]
        self.contextActions(actions, self.shaders_listView)
        self.gridLayout_3.addWidget(self.shaders_listView, 0, 0, 1, 1)
        self.shaders_scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.main_tabWidget.addTab(self.shaders_tab, _fromUtf8(""))
        self.images_tab = QtGui.QWidget()
        self.images_tab.setObjectName(_fromUtf8("images_tab"))
        self.images_scrollArea = QtGui.QScrollArea(self.images_tab)
        self.images_scrollArea.setGeometry(QtCore.QRect(0, 0, 570, 545))
        self.images_scrollArea.setMinimumSize(QtCore.QSize(550, 520))
        self.images_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.images_scrollArea.setWidgetResizable(True)
        self.images_scrollArea.setObjectName(_fromUtf8("images_scrollArea"))
        self.scrollAreaWidgetContents_4 = QtGui.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 529, 516))
        self.scrollAreaWidgetContents_4.setObjectName(_fromUtf8("scrollAreaWidgetContents_4"))
        self.gridLayout_4 = QtGui.QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.images_listView = DragAndDrop(self)
        self.images_listView.setObjectName(_fromUtf8("images_listView"))
        self.connect(self.images_listView, QtCore.SIGNAL("dropped"), (lambda links: self.itemDropped(links, self.images_listView)))  
        self.actionOpenImages = QtGui.QAction("Open", self.images_listView)        
        self.actionOpenWithImages = QtGui.QAction("Open With", self.images_listView)
        self.actionPreviewImages = QtGui.QAction("Preview", self.images_listView)
        self.actionPropertiesImages = QtGui.QAction("Properties", self.images_listView)
        self.actionImportImages = QtGui.QAction("Import", self.images_listView)
        self.actionDeleteImages = QtGui.QAction("Delete", self.images_listView)
        self.openWithImages = QtGui.QMenu(self.images_listView)
        self.actionOpenWithMayaImages = QtGui.QAction("Maya", self.openWithImages)
        self.actionOpenWithHoudiniImages = QtGui.QAction("Houdini", self.openWithImages)
        self.actionOpenWithNukeImages = QtGui.QAction("Nuke", self.openWithImages)
        self.actionOpenWithPhotoshopImages = QtGui.QAction("Photoshop", self.openWithImages)
        self.actionOpenWithTextEditorImages = QtGui.QAction("Text Editor", self.openWithImages)
        self.actionOpenWithImageViewerImages = QtGui.QAction("Image Viewer", self.openWithImages)
        actions = [Ui_MainWindow.window.actionOpenImages, Ui_MainWindow.window.actionOpenWithImages,
                   Ui_MainWindow.window.actionPreviewImages, Ui_MainWindow.window.actionPropertiesImages,
                   Ui_MainWindow.window.actionImportImages, Ui_MainWindow.window.actionDeleteImages,
                   Ui_MainWindow.window.openWithImages, Ui_MainWindow.window.actionOpenWithMayaImages,
                   Ui_MainWindow.window.actionOpenWithHoudiniImages, Ui_MainWindow.window.actionOpenWithNukeImages,
                   Ui_MainWindow.window.actionOpenWithPhotoshopImages, Ui_MainWindow.window.actionOpenWithTextEditorImages,
                   Ui_MainWindow.window.actionOpenWithImageViewerImages]
        self.contextActions(actions, self.images_listView)
        self.gridLayout_4.addWidget(self.images_listView, 0, 0, 1, 1)
        self.images_scrollArea.setWidget(self.scrollAreaWidgetContents_4)
        self.main_tabWidget.addTab(self.images_tab, _fromUtf8(""))
        self.videos_tab = QtGui.QWidget()
        self.videos_tab.setObjectName(_fromUtf8("videos_tab"))
        self.videos_scrollArea = QtGui.QScrollArea(self.videos_tab)
        self.videos_scrollArea.setGeometry(QtCore.QRect(0, 0, 570, 545))
        self.videos_scrollArea.setMinimumSize(QtCore.QSize(550, 520))
        self.videos_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videos_scrollArea.setWidgetResizable(True)
        self.videos_scrollArea.setObjectName(_fromUtf8("videos_scrollArea"))
        self.scrollAreaWidgetContents_5 = QtGui.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 529, 516))
        self.scrollAreaWidgetContents_5.setObjectName(_fromUtf8("scrollAreaWidgetContents_5"))
        self.gridLayout_5 = QtGui.QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.videos_listView = DragAndDrop(self)
        self.videos_listView.setObjectName(_fromUtf8("videos_listView"))
        self.connect(self.videos_listView, QtCore.SIGNAL("dropped"), (lambda links: self.itemDropped(links, self.videos_listView)))          
        self.actionOpenVideos = QtGui.QAction("Open", self.videos_listView)        
        self.actionOpenWithVideos = QtGui.QAction("Open With", self.videos_listView)
        self.actionPreviewVideos = QtGui.QAction("Preview", self.videos_listView)
        self.actionPropertiesVideos = QtGui.QAction("Properties", self.videos_listView)
        self.actionImportVideos = QtGui.QAction("Import", self.videos_listView)
        self.actionDeleteVideos = QtGui.QAction("Delete", self.videos_listView)
        self.openWithVideos = QtGui.QMenu(self.videos_listView)
        self.actionOpenWithMayaVideos = QtGui.QAction("Maya", self.openWithVideos)
        self.actionOpenWithHoudiniVideos = QtGui.QAction("Houdini", self.openWithVideos)
        self.actionOpenWithNukeVideos = QtGui.QAction("Nuke", self.openWithVideos)
        self.actionOpenWithPhotoshopVideos = QtGui.QAction("Photoshop", self.openWithVideos)
        self.actionOpenWithTextEditorVideos = QtGui.QAction("Text Editor", self.openWithVideos)
        self.actionOpenWithImageViewerVideos = QtGui.QAction("Image Viewer", self.openWithVideos)
        actions = [Ui_MainWindow.window.actionOpenVideos, Ui_MainWindow.window.actionOpenWithVideos,
                   Ui_MainWindow.window.actionPreviewVideos, Ui_MainWindow.window.actionPropertiesVideos,
                   Ui_MainWindow.window.actionImportVideos, Ui_MainWindow.window.actionDeleteVideos,
                   Ui_MainWindow.window.openWithVideos, Ui_MainWindow.window.actionOpenWithMayaVideos,
                   Ui_MainWindow.window.actionOpenWithHoudiniVideos, Ui_MainWindow.window.actionOpenWithNukeVideos,
                   Ui_MainWindow.window.actionOpenWithPhotoshopVideos, Ui_MainWindow.window.actionOpenWithTextEditorVideos,
                   Ui_MainWindow.window.actionOpenWithImageViewerVideos]
        self.contextActions(actions, self.videos_listView)
        self.gridLayout_5.addWidget(self.videos_listView, 0, 0, 1, 1)
        self.videos_scrollArea.setWidget(self.scrollAreaWidgetContents_5)
        self.main_tabWidget.addTab(self.videos_tab, _fromUtf8(""))
        self.audio_tab = QtGui.QWidget()
        self.audio_tab.setObjectName(_fromUtf8("audio_tab"))
        self.audio_scrollArea = QtGui.QScrollArea(self.audio_tab)
        self.audio_scrollArea.setGeometry(QtCore.QRect(0, 0, 570, 545))
        self.audio_scrollArea.setMinimumSize(QtCore.QSize(550, 520))
        self.audio_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.audio_scrollArea.setWidgetResizable(True)
        self.audio_scrollArea.setObjectName(_fromUtf8("audio_scrollArea"))
        self.scrollAreaWidgetContents_6 = QtGui.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 529, 516))
        self.scrollAreaWidgetContents_6.setObjectName(_fromUtf8("scrollAreaWidgetContents_6"))
        self.gridLayout_6 = QtGui.QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.audio_listView = DragAndDrop(self)
        self.audio_listView.setObjectName(_fromUtf8("audio_listView"))
        self.connect(self.audio_listView, QtCore.SIGNAL("dropped"), (lambda links: self.itemDropped(links, self.audio_listView)))          
        self.actionOpenAudio = QtGui.QAction("Open", self.audio_listView)        
        self.actionOpenWithAudio = QtGui.QAction("Open With", self.audio_listView)
        self.actionPreviewAudio = QtGui.QAction("Preview", self.audio_listView)
        self.actionPropertiesAudio = QtGui.QAction("Properties", self.audio_listView)
        self.actionImportAudio = QtGui.QAction("Import", self.audio_listView)
        self.actionDeleteAudio = QtGui.QAction("Delete", self.audio_listView)
        self.openWithAudio = QtGui.QMenu(self.audio_listView)
        self.actionOpenWithMayaAudio = QtGui.QAction("Maya", self.openWithAudio)
        self.actionOpenWithHoudiniAudio = QtGui.QAction("Houdini", self.openWithAudio)
        self.actionOpenWithNukeAudio = QtGui.QAction("Nuke", self.openWithAudio)
        self.actionOpenWithPhotoshopAudio = QtGui.QAction("Photoshop", self.openWithAudio)
        self.actionOpenWithTextEditorAudio = QtGui.QAction("Text Editor", self.openWithAudio)
        self.actionOpenWithImageViewerAudio = QtGui.QAction("Image Viewer", self.openWithAudio)
        actions = [Ui_MainWindow.window.actionOpenAudio, Ui_MainWindow.window.actionOpenWithAudio,
                   Ui_MainWindow.window.actionPreviewAudio, Ui_MainWindow.window.actionPropertiesAudio,
                   Ui_MainWindow.window.actionImportAudio, Ui_MainWindow.window.actionDeleteAudio,
                   Ui_MainWindow.window.openWithAudio, Ui_MainWindow.window.actionOpenWithMayaAudio,
                   Ui_MainWindow.window.actionOpenWithHoudiniAudio, Ui_MainWindow.window.actionOpenWithNukeAudio,
                   Ui_MainWindow.window.actionOpenWithPhotoshopAudio, Ui_MainWindow.window.actionOpenWithTextEditorAudio,
                   Ui_MainWindow.window.actionOpenWithImageViewerAudio]
        self.contextActions(actions, self.audio_listView)
        self.gridLayout_6.addWidget(self.audio_listView, 0, 0, 1, 1)
        self.audio_scrollArea.setWidget(self.scrollAreaWidgetContents_6)
        self.main_tabWidget.addTab(self.audio_tab, _fromUtf8(""))
        self.scripts_tab = QtGui.QWidget()
        self.scripts_tab.setObjectName(_fromUtf8("scripts_tab"))
        self.scripts_scrollArea = QtGui.QScrollArea(self.scripts_tab)
        self.scripts_scrollArea.setGeometry(QtCore.QRect(0, 0, 570, 545))
        self.scripts_scrollArea.setMinimumSize(QtCore.QSize(550, 520))
        self.scripts_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scripts_scrollArea.setWidgetResizable(True)
        self.scripts_scrollArea.setObjectName(_fromUtf8("scripts_scrollArea"))
        self.scrollAreaWidgetContents_7 = QtGui.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 529, 516))
        self.scrollAreaWidgetContents_7.setObjectName(_fromUtf8("scrollAreaWidgetContents_7"))
        self.gridLayout_7 = QtGui.QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.scripts_listView = DragAndDrop(self)
        self.scripts_listView.setObjectName(_fromUtf8("scripts_listView"))
        self.connect(self.scripts_listView, QtCore.SIGNAL("dropped"), (lambda links: self.itemDropped(links, self.scripts_listView)))          
        self.actionOpenScripts = QtGui.QAction("Open", self.scripts_listView)        
        self.actionOpenWithScripts = QtGui.QAction("Open With", self.scripts_listView)
        self.actionPreviewScripts = QtGui.QAction("Preview", self.scripts_listView)
        self.actionPropertiesScripts = QtGui.QAction("Properties", self.scripts_listView)
        self.actionImportScripts = QtGui.QAction("Import", self.scripts_listView)
        self.actionDeleteScripts = QtGui.QAction("Delete", self.scripts_listView)
        self.openWithScripts = QtGui.QMenu(self.scripts_listView)
        self.actionOpenWithMayaScripts = QtGui.QAction("Maya", self.openWithScripts)
        self.actionOpenWithHoudiniScripts = QtGui.QAction("Houdini", self.openWithScripts)
        self.actionOpenWithNukeScripts = QtGui.QAction("Nuke", self.openWithScripts)
        self.actionOpenWithPhotoshopScripts = QtGui.QAction("Photoshop", self.openWithScripts)
        self.actionOpenWithTextEditorScripts = QtGui.QAction("Text Editor", self.openWithScripts)
        self.actionOpenWithImageViewerScripts = QtGui.QAction("Image Viewer", self.openWithScripts)
        actions = [Ui_MainWindow.window.actionOpenScripts, Ui_MainWindow.window.actionOpenWithScripts,
                   Ui_MainWindow.window.actionPreviewScripts, Ui_MainWindow.window.actionPropertiesScripts,
                   Ui_MainWindow.window.actionImportScripts, Ui_MainWindow.window.actionDeleteScripts,
                   Ui_MainWindow.window.openWithScripts, Ui_MainWindow.window.actionOpenWithMayaScripts,
                   Ui_MainWindow.window.actionOpenWithHoudiniScripts, Ui_MainWindow.window.actionOpenWithNukeScripts,
                   Ui_MainWindow.window.actionOpenWithPhotoshopScripts, Ui_MainWindow.window.actionOpenWithTextEditorScripts,
                   Ui_MainWindow.window.actionOpenWithImageViewerScripts]
        self.contextActions(actions, self.scripts_listView)
        self.gridLayout_7.addWidget(self.scripts_listView, 1, 2, 1, 1)
        self.scripts_scrollArea.setWidget(self.scrollAreaWidgetContents_7)
        self.main_tabWidget.addTab(self.scripts_tab, _fromUtf8(""))
        self.simulations_tab = QtGui.QWidget()
        self.simulations_tab.setObjectName(_fromUtf8("simulations_tab"))
        self.simulations_scrollArea = QtGui.QScrollArea(self.simulations_tab)
        self.simulations_scrollArea.setGeometry(QtCore.QRect(0, 0, 570, 545))
        self.simulations_scrollArea.setMinimumSize(QtCore.QSize(550, 520))
        self.simulations_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.simulations_scrollArea.setWidgetResizable(True)
        self.simulations_scrollArea.setObjectName(_fromUtf8("simulations_scrollArea"))
        self.scrollAreaWidgetContents_8 = QtGui.QWidget()
        self.scrollAreaWidgetContents_8.setGeometry(QtCore.QRect(0, 0, 529, 516))
        self.scrollAreaWidgetContents_8.setObjectName(_fromUtf8("scrollAreaWidgetContents_8"))
        self.gridLayout_8 = QtGui.QGridLayout(self.scrollAreaWidgetContents_8)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.simulations_listView = DragAndDrop(self)
        self.simulations_listView.setObjectName(_fromUtf8("simulations_listView"))
        self.connect(self.simulations_listView, QtCore.SIGNAL("dropped"), (lambda links: self.itemDropped(links, self.simulations_listView)))
        self.actionOpenSimulations = QtGui.QAction("Open", self.simulations_listView)        
        self.actionOpenWithSimulations = QtGui.QAction("Open With", self.simulations_listView)
        self.actionPreviewSimulations = QtGui.QAction("Preview", self.simulations_listView)
        self.actionPropertiesSimulations = QtGui.QAction("Properties", self.simulations_listView)
        self.actionImportSimulations = QtGui.QAction("Import", self.simulations_listView)
        self.actionDeleteSimulations = QtGui.QAction("Delete", self.simulations_listView)
        self.openWithSimulations = QtGui.QMenu(self.simulations_listView)
        self.actionOpenWithMayaSimulations = QtGui.QAction("Maya", self.openWithSimulations)
        self.actionOpenWithHoudiniSimulations = QtGui.QAction("Houdini", self.openWithSimulations)
        self.actionOpenWithNukeSimulations = QtGui.QAction("Nuke", self.openWithSimulations)
        self.actionOpenWithPhotoshopSimulations = QtGui.QAction("Photoshop", self.openWithSimulations)
        self.actionOpenWithTextEditorSimulations = QtGui.QAction("Text Editor", self.openWithSimulations)
        self.actionOpenWithImageViewerSimulations = QtGui.QAction("Image Viewer", self.openWithSimulations)
        actions = [Ui_MainWindow.window.actionOpenSimulations, Ui_MainWindow.window.actionOpenWithSimulations,
                   Ui_MainWindow.window.actionPreviewSimulations, Ui_MainWindow.window.actionPropertiesSimulations,
                   Ui_MainWindow.window.actionImportSimulations, Ui_MainWindow.window.actionDeleteSimulations,
                   Ui_MainWindow.window.openWithSimulations, Ui_MainWindow.window.actionOpenWithMayaSimulations,
                   Ui_MainWindow.window.actionOpenWithHoudiniSimulations, Ui_MainWindow.window.actionOpenWithNukeSimulations,
                   Ui_MainWindow.window.actionOpenWithPhotoshopSimulations, Ui_MainWindow.window.actionOpenWithTextEditorSimulations,
                   Ui_MainWindow.window.actionOpenWithImageViewerSimulations]
        self.contextActions(actions, self.simulations_listView)
        self.gridLayout_8.addWidget(self.simulations_listView, 0, 1, 1, 1)
        self.simulations_scrollArea.setWidget(self.scrollAreaWidgetContents_8)
        self.main_tabWidget.addTab(self.simulations_tab, _fromUtf8(""))
        self.settings_frame = QtGui.QFrame(self.centralwidget)
        self.settings_frame.setGeometry(QtCore.QRect(0, 0, 201, 200))
        self.settings_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.settings_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.settings_frame.setObjectName(_fromUtf8("settings_frame"))
        self.settings_label = QtGui.QLabel(self.settings_frame)
        self.settings_label.setGeometry(QtCore.QRect(65, 5, 145, 13))
        self.settings_label.setObjectName(_fromUtf8("settings_label"))
        self.address_label = QtGui.QLabel(self.settings_frame)
        self.address_label.setGeometry(QtCore.QRect(10, 20, 46, 13))
        self.address_label.setObjectName(_fromUtf8("address_label"))
        self.username_label = QtGui.QLabel(self.settings_frame)
        self.username_label.setGeometry(QtCore.QRect(10, 45, 60, 13))
        self.username_label.setObjectName(_fromUtf8("username_label"))
        self.password_label = QtGui.QLabel(self.settings_frame)
        self.password_label.setGeometry(QtCore.QRect(10, 70, 60, 13))
        self.password_label.setObjectName(_fromUtf8("password_label"))
        self.database_label = QtGui.QLabel(self.settings_frame)
        self.database_label.setGeometry(QtCore.QRect(10, 95, 60, 13))
        self.database_label.setObjectName(_fromUtf8("database_label"))        
        self.address_lineEdit = QtGui.QLineEdit(self.settings_frame)
        self.address_lineEdit.setGeometry(QtCore.QRect(80, 20, 113, 20))
        self.address_lineEdit.setObjectName(_fromUtf8("address_lineEdit"))
        self.username_lineEdit = QtGui.QLineEdit(self.settings_frame)
        self.username_lineEdit.setGeometry(QtCore.QRect(80, 45, 113, 20))
        self.username_lineEdit.setObjectName(_fromUtf8("username_lineEdit"))
        self.password_lineEdit = QtGui.QLineEdit(self.settings_frame)
        self.password_lineEdit.setGeometry(QtCore.QRect(80, 70, 113, 20))
        self.password_lineEdit.setObjectName(_fromUtf8("password_lineEdit"))
        self.password_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.database_lineEdit = QtGui.QLineEdit(self.settings_frame)
        self.database_lineEdit.setGeometry(QtCore.QRect(80, 95, 113, 20))
        self.database_lineEdit.setObjectName(_fromUtf8("database_lineEdit"))
        self.connect_pushButton = QtGui.QPushButton(self.settings_frame)
        self.connect_pushButton.setGeometry(QtCore.QRect(10, 120, 180, 23))
        self.connect_pushButton.setObjectName(_fromUtf8("connect_pushButton"))
        self.connect(self.connect_pushButton, QtCore.SIGNAL("clicked()"), self.connectToDB)  
        self.refresh_pushButton = QtGui.QPushButton(self.settings_frame)
        self.refresh_pushButton.setGeometry(QtCore.QRect(10, 147, 180, 23))
        self.refresh_pushButton.setObjectName(_fromUtf8("refresh_pushButton"))
        self.connect(self.refresh_pushButton, QtCore.SIGNAL("clicked()"), self.refreshItems)
        self.projects_frame = QtGui.QFrame(self.centralwidget)
        self.projects_frame.setGeometry(QtCore.QRect(0, 170, 201, 420))
        self.projects_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.projects_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.projects_frame.setObjectName(_fromUtf8("projects_frame"))
        self.projectloc_label = QtGui.QLabel(self.projects_frame)
        self.projectloc_label.setGeometry(QtCore.QRect(65, 30, 91, 20))
        self.projectloc_label.setObjectName(_fromUtf8("projectloc_label"))
        self.projectloc_scrollArea = QtGui.QScrollArea(self.projects_frame)
        self.projectloc_scrollArea.setGeometry(QtCore.QRect(10, 50, 150, 170))
        self.projectloc_scrollArea.setMinimumSize(QtCore.QSize(180, 290))
        self.projectloc_scrollArea.setMaximumSize(QtCore.QSize(180, 290))
        self.projectloc_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.projectloc_scrollArea.setWidgetResizable(True)
        self.projectloc_scrollArea.setObjectName(_fromUtf8("projectloc_scrollArea"))
        self.setFolder_pushButton = QtGui.QPushButton(self.projects_frame)
        self.setFolder_pushButton.setGeometry(QtCore.QRect(10, 345, 180, 23))
        self.setFolder_pushButton.setObjectName(_fromUtf8("setFolder_pushButton"))
        self.addFile_pushButton = QtGui.QPushButton(self.projects_frame)
        self.addFile_pushButton.setGeometry(QtCore.QRect(10, 370, 90, 23))
        self.addFile_pushButton.setObjectName(_fromUtf8("addFile_pushButton"))
        self.removeFile_pushButton = QtGui.QPushButton(self.projects_frame)
        self.removeFile_pushButton.setGeometry(QtCore.QRect(100, 370, 90, 23))
        self.removeFile_pushButton.setObjectName(_fromUtf8("removeFile_pushButton"))
        self.connect(self.setFolder_pushButton, QtCore.SIGNAL("clicked()"), self.setFolder)  
        self.connect(self.addFile_pushButton, QtCore.SIGNAL("clicked()"), self.addFile)  
        self.connect(self.removeFile_pushButton, QtCore.SIGNAL("clicked()"), self.removeFile)
        self.scrollAreaWidgetContents_10 = QtGui.QWidget()
        self.scrollAreaWidgetContents_10.setGeometry(QtCore.QRect(0, 0, 159, 218))
        self.scrollAreaWidgetContents_10.setObjectName(_fromUtf8("scrollAreaWidgetContents_10"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_10)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.listWidget_2 = QtGui.QListWidget(self.scrollAreaWidgetContents_10)
        self.listWidget_2.setMinimumSize(QtCore.QSize(140, 200))
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.projectloc_scrollArea.setWidget(self.scrollAreaWidgetContents_10)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 778, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuDisplay = QtGui.QMenu(self.menubar)
        self.menuDisplay.setObjectName(_fromUtf8("menuDisplay"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.openAssetFileAction = QtGui.QAction(MainWindow)
        self.openAssetFileAction.setObjectName(_fromUtf8("actionBlah"))
        self.saveAssetFileAction = QtGui.QAction(MainWindow)
        self.saveAssetFileAction.setObjectName(_fromUtf8("actionBlah_2"))
        self.importAssetFileAction = QtGui.QAction(MainWindow)
        self.importAssetFileAction.setObjectName(_fromUtf8("actionBlah_3"))
        self.copyAction = QtGui.QAction(MainWindow)
        self.copyAction.setObjectName(_fromUtf8("actionBlah"))
        self.pasteAction = QtGui.QAction(MainWindow)
        self.pasteAction.setObjectName(_fromUtf8("actionBlah_2"))
        self.deleteAction = QtGui.QAction(MainWindow)
        self.deleteAction.setObjectName(_fromUtf8("actionBlah_3"))        
        self.interfaceColor1Action = QtGui.QAction(MainWindow)
        self.interfaceColor1Action.setObjectName(_fromUtf8("actionBlah"))
        self.interfaceColor2Action = QtGui.QAction(MainWindow)
        self.interfaceColor2Action.setObjectName(_fromUtf8("actionBlah_2"))
        self.interfaceColorCustomAction = QtGui.QAction(MainWindow)
        self.interfaceColorCustomAction.setObjectName(_fromUtf8("actionBlah_3"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.openAssetFileAction)
        self.menuFile.addAction(self.saveAssetFileAction)
        self.menuFile.addAction(self.importAssetFileAction)
        self.menuEdit.addAction(self.copyAction)
        self.menuEdit.addAction(self.pasteAction)
        self.menuEdit.addAction(self.deleteAction)
        self.menuDisplay.addAction(self.interfaceColor1Action)
        self.menuDisplay.addAction(self.interfaceColor2Action)
        self.menuDisplay.addAction(self.interfaceColorCustomAction)
        self.interfaceColor1Action.triggered.connect(self.interfaceColor1)
        self.interfaceColor2Action.triggered.connect(self.interfaceColor2)
        self.interfaceColorCustomAction.triggered.connect(self.interfaceColorCustom)
        self.openAssetFileAction.triggered.connect(lambda : self.openAssetFile(0))
        self.saveAssetFileAction.triggered.connect(self.saveAssetFile)
        self.importAssetFileAction.triggered.connect(lambda : self.importAssetFile(0))
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuDisplay.menuAction())
        self.retranslateUi(MainWindow)
        self.main_tabWidget.setCurrentIndex(7)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.listWidget_2.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.actionOpenAssetFile = QtGui.QAction("Open", self.listWidget_2)        
        self.listWidget_2.addAction(self.actionOpenAssetFile)
        self.actionOpenAssetFile.setStatusTip('Open asset file')
        self.actionOpenAssetFile.triggered.connect(lambda : self.openAssetFile(1))
        self.actionImportAssetFile = QtGui.QAction("Import", self.listWidget_2)        
        self.listWidget_2.addAction(self.actionImportAssetFile)
        self.actionImportAssetFile.setStatusTip('Import asset file')
        self.actionImportAssetFile.triggered.connect(lambda : self.importAssetFile(1))
        self.actionRemoveAssetFile = QtGui.QAction("Remove", self.listWidget_2)        
        self.listWidget_2.addAction(self.actionRemoveAssetFile)
        self.actionRemoveAssetFile.setStatusTip('Remove asset file')
        self.actionRemoveAssetFile.triggered.connect(self.removeFile)
        self.copyAction.triggered.connect(self.copyItem)
        self.pasteAction.triggered.connect(self.pasteItem)
        self.deleteAction.triggered.connect(self.deleteItem)
        Ui_MainWindow.window.projects_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.models_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.shaders_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.images_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.videos_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.audio_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.scripts_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.simulations_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        MainWindow.setStyleSheet('background-color: darkgrey')
        Ui_MainWindow.window.address_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        Ui_MainWindow.window.username_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        Ui_MainWindow.window.password_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        Ui_MainWindow.window.database_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        Ui_MainWindow.window.connect_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.setFolder_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.addFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.removeFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        Ui_MainWindow.window.listWidget_2.setStyleSheet('background-color: rgb(200,200,200)')
        Ui_MainWindow.window.statusbar.setStyleSheet('background-color: rgb(200,200,200)')
        Ui_MainWindow.window.menubar.setStyleSheet('QMenuBar {background-color: rgb(200,200,200)} QMenuBar::item {background-color: transparent;} QMenuBar::item:selected {background-color: rgb(240,240,240);} QMenuBar::item:inactive{color: black}')
        Ui_MainWindow.window.menuFile.setStyleSheet('QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;}')
        Ui_MainWindow.window.menuDisplay.setStyleSheet('QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;}')
        Ui_MainWindow.window.listWidget_2.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        Ui_MainWindow.window.main_tabWidget.setStyleSheet('QTabWidget::pane {border: 1px solid grey;} QTabWidget {border: 1px solid grey; padding: 0px;} QTabBar::tab {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D8D8D8, stop: 0.4 #C5C5C5, stop: 0.5 #B6B6B6, stop: 1.0 #A2A2A2); border: 2px solid #C4C4C3; border-bottom-color: #C2C7CB;  border-top-left-radius: 4px; border-top-right-radius: 4px; min-width: 21ex; padding: 2px;} QTabBar::tab:selected, QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}')
        Ui_MainWindow.window.simulations_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.scripts_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.audio_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.videos_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.images_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.shaders_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.Models_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.projects_scrollArea.setStyleSheet('border: 0px;')
        self.listWidget_2.setDragDropMode(QtGui.QAbstractItemView.InternalMove);
        fileLocation = os.getcwd()
        fileLocation = fileLocation + '\\AssetManagerFiles\\LoginInfo.txt'
        self.interfaceColor1()        
        if os.path.exists(fileLocation):
            config = ConfigParser.ConfigParser()
            config.read(fileLocation)
            address = config.get('Address', 'Address')
            username = config.get('Username', 'Username')
            encpassword = config.get('Password', 'Password')
            password = base64.b64decode(encpassword)
            databasename = config.get('DatabaseName', 'DatabaseName')
            self.address_lineEdit.setText(address)
            self.username_lineEdit.setText(username)
            self.password_lineEdit.setText(password)
            self.database_lineEdit.setText(databasename)

    def retranslateUi(self, MainWindow):
        '''Rename UI items'''
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Asset Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.projects_tab), QtGui.QApplication.translate("MainWindow", "Projects", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.models_tab), QtGui.QApplication.translate("MainWindow", "Models", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.shaders_tab), QtGui.QApplication.translate("MainWindow", "Shaders", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.images_tab), QtGui.QApplication.translate("MainWindow", "Images", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.videos_tab), QtGui.QApplication.translate("MainWindow", "Videos", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.audio_tab), QtGui.QApplication.translate("MainWindow", "Audio", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.scripts_tab), QtGui.QApplication.translate("MainWindow", "Scripts", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.simulations_tab), QtGui.QApplication.translate("MainWindow", "Simulations", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_label.setText(QtGui.QApplication.translate("MainWindow", "Server Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.address_label.setText(QtGui.QApplication.translate("MainWindow", "Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.username_label.setText(QtGui.QApplication.translate("MainWindow", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.password_label.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.database_label.setText(QtGui.QApplication.translate("MainWindow", "Database:", None, QtGui.QApplication.UnicodeUTF8))
        self.connect_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Connect/Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Refresh Items", None, QtGui.QApplication.UnicodeUTF8))
        self.setFolder_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Add Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.addFile_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Add File", None, QtGui.QApplication.UnicodeUTF8))
        self.removeFile_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Remove File", None, QtGui.QApplication.UnicodeUTF8))
        self.projectloc_label.setText(QtGui.QApplication.translate("MainWindow", "Project Files", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDisplay.setTitle(QtGui.QApplication.translate("MainWindow", "Display", None, QtGui.QApplication.UnicodeUTF8))
        self.copyAction.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.pasteAction.setText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteAction.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.openAssetFileAction.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.saveAssetFileAction.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.importAssetFileAction.setText(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.interfaceColor1Action.setText(QtGui.QApplication.translate("MainWindow", "Interface Color Dark", None, QtGui.QApplication.UnicodeUTF8))
        self.interfaceColor2Action.setText(QtGui.QApplication.translate("MainWindow", "Interface Color Light", None, QtGui.QApplication.UnicodeUTF8))
        self.interfaceColorCustomAction.setText(QtGui.QApplication.translate("MainWindow", "Custom Interface Color", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

class ColorPicker(QtGui.QDialog):
    '''Color picker for custom UI'''
    col = QtGui.QColor(0, 0, 0)
    col1 = QtGui.QColor(0, 0, 0) 
    col2 = QtGui.QColor(0, 0, 0) 
    col3 = QtGui.QColor(0, 0, 0)
    col4 = QtGui.QColor(0, 0, 0)     
    def __init__(self):
        super(ColorPicker, self).__init__()        
        self.initUI()
        
    def initUI(self):
        '''Setup UI'''
        self.bgbtn = QtGui.QPushButton('Background Color', self)
        self.bgbtn.setGeometry(QtCore.QRect(20, 20, 100, 23))
        self.fgbtn = QtGui.QPushButton('Foreground Color', self)
        self.fgbtn.setGeometry(QtCore.QRect(20, 44, 100, 23))
        self.d1btn = QtGui.QPushButton('Detail Color 1', self)
        self.d1btn.setGeometry(QtCore.QRect(20, 68, 100, 23))
        self.d2btn = QtGui.QPushButton('Detail Color 2', self)
        self.d2btn.setGeometry(QtCore.QRect(20, 92, 100, 23))
        self.tbtn = QtGui.QPushButton('Text Color', self)
        self.tbtn.setGeometry(QtCore.QRect(20, 116, 100, 23))
        self.bgbtn.clicked.connect(self.showDialog)
        self.fgbtn.clicked.connect(self.showDialog1)
        self.d1btn.clicked.connect(self.showDialog2)
        self.d2btn.clicked.connect(self.showDialog3)
        self.tbtn.clicked.connect(self.showDialog4)
        self.okbtn = QtGui.QPushButton('Apply', self)
        self.okbtn.setGeometry(QtCore.QRect(20, 150, 100, 23))
        self.cancelbtn = QtGui.QPushButton('Close', self)
        self.cancelbtn.setGeometry(QtCore.QRect(130, 150, 100, 23))
        self.okbtn.clicked.connect(lambda : self.ok(ColorPicker.col,
                                                    ColorPicker.col1,
                                                    ColorPicker.col2))
        self.cancelbtn.clicked.connect(self.cancel)
        self.frm = QtGui.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col.name())
        self.frm.setGeometry(130, 22, 100, 20)            
        self.frm1 = QtGui.QFrame(self)
        self.frm1.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col1.name())
        self.frm1.setGeometry(130, 44, 100, 20)
        self.frm2 = QtGui.QFrame(self)
        self.frm2.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col2.name())
        self.frm2.setGeometry(130, 66, 100, 20)
        self.frm3 = QtGui.QFrame(self)
        self.frm3.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col3.name())
        self.frm3.setGeometry(130, 88, 100, 20)
        self.frm4 = QtGui.QFrame(self)
        self.frm4.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col4.name())
        self.frm4.setGeometry(130, 110, 100, 20) 
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')
        
    def ok(self, col, col1, col2):
        '''Sets colors'''
        Ui_MainWindow.window.projects_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.models_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col.name(),'color2': ColorPicker.col.name(),'color3': ColorPicker.col.name(),'color4': ColorPicker.col.name()})
        Ui_MainWindow.window.shaders_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col.name(),'color2': ColorPicker.col.name(),'color3': ColorPicker.col.name(),'color4': ColorPicker.col.name()})
        Ui_MainWindow.window.images_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col.name(),'color2': ColorPicker.col.name(),'color3': ColorPicker.col.name(),'color4': ColorPicker.col.name()})
        Ui_MainWindow.window.videos_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.audio_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.scripts_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.simulations_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        changeMode.MainWindow.setStyleSheet('background-color: %(color)s;  color: %(color4)s' % {'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.address_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.username_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.password_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.database_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.connect_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}'  % {'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.setFolder_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}'  % {'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.addFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}'  % {'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.removeFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}'  % {'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.listWidget_2.setStyleSheet('background-color: %(color1)s; color: %(color4)s' % {'color1': ColorPicker.col.name(),'color4': ColorPicker.col.name()})
        Ui_MainWindow.window.statusbar.setStyleSheet('background-color: %(color1)s; color: %(color4)s' % {'color1': ColorPicker.col.name(),'color4': ColorPicker.col.name()})
        Ui_MainWindow.window.menubar.setStyleSheet('QMenuBar {background-color: %(color1)s} QMenuBar::item {background-color: transparent;} QMenuBar::item:selected {background-color: %(color3)s;} QMenuBar::item:inactive{color: %(color4)s}' % {'color1': ColorPicker.col1.name(),'color3': ColorPicker.col3.name(), 'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.menuFile.setStyleSheet('QMenu {background-color: %(color1)s; border: 2px solid %(color)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.menuEdit.setStyleSheet('QMenu {background-color: %(color1)s; border: 2px solid %(color)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.menuDisplay.setStyleSheet('QMenu {background-color: %(color1)s; border: 2px solid %(color)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.listWidget_2.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {background-color: %(color1)s; border: 2px solid darkgrey; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.main_tabWidget.setStyleSheet('QTabWidget::pane {border: 1px solid grey;} QTabWidget {border: 1px solid grey; padding: 0px;} QTabBar::tab {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D8D8D8, stop: 0.4 #C5C5C5, stop: 0.5 #B6B6B6, stop: 1.0 %(color)s); border: 2px solid #C4C4C3; border-bottom-color: #C2C7CB;  border-top-left-radius: 4px; border-top-right-radius: 4px; min-width: 21ex; padding: 2px;} QTabBar::tab:selected, QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa); color: %(color4)s;}' % {'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        Ui_MainWindow.window.simulations_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.scripts_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.audio_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.videos_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.images_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.shaders_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.Models_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.window.projects_scrollArea.setStyleSheet('border: 0px;')
        Ui_MainWindow.interfaceColor = 3
        
    def cancel(self):
        self.close()
        
    def showDialog(self):
        '''Dialog for first color'''
        ColorPicker.col = QtGui.QColorDialog.getColor()
        if ColorPicker.col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col.name())
        
    def showDialog1(self):
        '''Dialog for second color'''
        ColorPicker.col1 = QtGui.QColorDialog.getColor()
        if ColorPicker.col1.isValid():
            self.frm1.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col1.name())
        
    def showDialog2(self):
        '''Dialog for third color'''
        ColorPicker.col2 = QtGui.QColorDialog.getColor()
        if ColorPicker.col2.isValid():
            self.frm2.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col2.name())
            
    def showDialog3(self):
        '''Dialog for fourth color'''
        ColorPicker.col3 = QtGui.QColorDialog.getColor()
        if ColorPicker.col3.isValid():
            self.frm3.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col3.name())
            
    def showDialog4(self):
        '''Dialog for fith color'''
        ColorPicker.col4 = QtGui.QColorDialog.getColor()
        if ColorPicker.col4.isValid():
            self.frm4.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col4.name())

            
class DragAndDrop(QtGui.QListWidget):
    '''Setup Drag and drop events'''
    def __init__(self, parent):
        super(DragAndDrop, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(100, 100))
        self.itemClicked.connect(self.on_item_clicked)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
      
    def dragEnterEvent(self, event):
        '''Drag event when entering window'''
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            super(DragAndDrop, self).dragEnterEvent(event)
            
    def dragMoveEvent(self, event):
        '''Drag event when moving in window'''
        super(DragAndDrop, self).dragMoveEvent(event)
            
    def dropEvent(self, event):
        '''Drop event in window'''
        if event.mimeData().hasUrls():
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
            event.acceptProposedAction()
        else:
            super(DragAndDrop,self).dropEvent(event)

    def mousePressEvent(self, event):
        '''
        Mouse press event in window
        Enables/Disables menu actions
        '''
        self._mouse_button = event.button()
        super(DragAndDrop, self).mousePressEvent(event)
        propertiesActions = [Ui_MainWindow.window.actionOpenProjects,
                             Ui_MainWindow.window.actionOpenWithProjects,
                             Ui_MainWindow.window.actionPropertiesProjects,
                             Ui_MainWindow.window.actionPreviewProjects,
                             Ui_MainWindow.window.actionDeleteProjects,
                             Ui_MainWindow.window.actionOpenModels,
                             Ui_MainWindow.window.actionOpenWithModels,
                             Ui_MainWindow.window.actionPropertiesModels,
                             Ui_MainWindow.window.actionPreviewModels,
                             Ui_MainWindow.window.actionDeleteModels,
                             Ui_MainWindow.window.actionOpenAudio,
                             Ui_MainWindow.window.actionOpenWithAudio,
                             Ui_MainWindow.window.actionPropertiesAudio,
                             Ui_MainWindow.window.actionPreviewAudio,
                             Ui_MainWindow.window.actionDeleteAudio,
                             Ui_MainWindow.window.actionOpenVideos,
                             Ui_MainWindow.window.actionOpenWithVideos,
                             Ui_MainWindow.window.actionPropertiesVideos,
                             Ui_MainWindow.window.actionPreviewVideos,
                             Ui_MainWindow.window.actionDeleteVideos,
                             Ui_MainWindow.window.actionOpenImages,
                             Ui_MainWindow.window.actionOpenWithImages,
                             Ui_MainWindow.window.actionPropertiesImages,
                             Ui_MainWindow.window.actionPreviewImages,
                             Ui_MainWindow.window.actionDeleteImages,
                             Ui_MainWindow.window.actionOpenShaders,
                             Ui_MainWindow.window.actionOpenWithShaders,
                             Ui_MainWindow.window.actionPropertiesShaders,
                             Ui_MainWindow.window.actionPreviewShaders,
                             Ui_MainWindow.window.actionDeleteShaders,
                             Ui_MainWindow.window.actionOpenScripts,
                             Ui_MainWindow.window.actionOpenWithScripts,
                             Ui_MainWindow.window.actionPropertiesScripts,
                             Ui_MainWindow.window.actionPreviewScripts,
                             Ui_MainWindow.window.actionDeleteScripts,
                             Ui_MainWindow.window.actionOpenSimulations,
                             Ui_MainWindow.window.actionOpenWithSimulations,
                             Ui_MainWindow.window.actionPropertiesSimulations,
                             Ui_MainWindow.window.actionPreviewSimulations,
                             Ui_MainWindow.window.actionDeleteSimulations]
        items = self.count()
        rangedList =range(items)
        rangedList.reverse()
        numberSelected = 0
        for i in rangedList:
            if self.isItemSelected(self.item(i))==True:
                numberSelected += 1
        for action in propertiesActions:
            if numberSelected == 0:
                action.setEnabled(False)
            if numberSelected == 1:
                action.setEnabled(True)
            if numberSelected > 1:
                action.setEnabled(False)
        for action in range(4, len(propertiesActions), 5):
            if numberSelected > 1:
                propertiesActions[action].setEnabled(True)
        if self._mouse_button == 2:
            for action in propertiesActions:
                if numberSelected == 0:
                    action.setEnabled(False)
            
    def on_item_clicked(self, item):
        '''Future implementation'''
        pass


def main():
    logSetup()
    app = QtGui.QApplication(sys.argv)
    cm = changeMode()
    app.exec_()
    
if __name__ == "__main__":
    main()
