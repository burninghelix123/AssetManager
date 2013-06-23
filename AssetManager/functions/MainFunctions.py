'''Main functions for Asset Manager'''
from PyQt4 import QtCore, QtGui
import MySQLdb as mysql
import base64
import os
from ..ui import PropertiesWindow
from ..ui import CustomUi
from ..ui import MessageDialog
from ..functions import ItemDisplay
import ConfigParser
from ..functions import DatabaseConnect
import tempfile
import warnings

class MainFunctions():
    
    def __init__(self, window, mainWindow, currentMode, database,
                 copiedItems, propertiesWindow):
        MainFunctions.database = database
        MainFunctions.currentMode = currentMode
        MainFunctions.mainWindow = mainWindow
        MainFunctions.window = window
        MainFunctions.copiedItems = copiedItems
        MainFunctions.propertiesWindow = propertiesWindow
        MainFunctions.tabs = ['projects_listView', 'models_listView',
                              'shaders_listView', 'images_listView',
                              'videos_listView', 'audio_listView',
                              'scripts_listView', 'simulations_listView']
   
    def addFile(self):
        '''Add asset file to saved list'''
        url = QtGui.QFileDialog.getOpenFileName(MainFunctions.window, 'Select asset file to add',
                                                '', ("Select Asset: (*.Asset)"))
        fileEntry = QtGui.QListWidgetItem(url, MainFunctions.window.listWidget_2)
        url = os.path.abspath(url)
        itemNameExt = os.path.split(url)
        itemNameExt = itemNameExt[1]
        itemName = (itemNameExt.split('.', 1)[0])
        fileEntry.setText(str(itemName))
        fileEntry.setStatusTip(str(url))
        
    def addItemToList(self, url, listVar):
        '''Add asset manager file to saved list'''
        url = os.path.abspath(url)
        if MainFunctions.currentMode == 0: #If run locally
            if os.path.exists(url):
                tempDir = tempfile.gettempdir()
                tempLocation = os.path.join(tempDir,'AssetManagerTemp')
                itemNameExt = os.path.split(url)
                itemNameExt = itemNameExt[1]
                itemName = (itemNameExt.split('.', 1)[0])
                tempPath= tempLocation + itemName + '.png'
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
                if os.path.exists(tempLocation + itemName + '.properties'):
                    config = ConfigParser.ConfigParser()
                    wholeFile = str(tempLocation + itemName + '.properties')
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
                    text = ItemDisplay.itemDisplay(fileField, locationField, nameField,
                                       categoryField, tagsField, statusField,
                                       dateField, authorField, versionField,
                                       commentsField)
                    item.setText(text)
                else:
                    item.setText(url)
                item.setStatusTip(url)
                
        if MainFunctions.currentMode == 1: #If run dynamically
            if os.path.exists(url):
                itemNameExt = os.path.split(url)
                itemNameExt = itemNameExt[1]
                itemName = (itemNameExt.split('.', 1)[0])
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
                    text = ItemDisplay.itemDisplay(fileField, locationField, nameField,
                                       categoryField, tagsField, statusField,
                                       dateField, authorField, versionField,
                                       commentsField)
                    item.setText(text)
                else:
                    item.setText(url)
                item.setStatusTip(url)
                            
    def checkDatabase(self):
        if MainFunctions.currentMode == 1:
            warnings.filterwarnings('ignore')
            tempDir = tempfile.gettempdir()
            tempLocation = os.path.join(tempDir,'AssetManagerTemp')
            tempLocation = os.path.join(tempLocation,'LoginInfo.txt')
            if os.path.exists(tempLocation):
                input = MessageDialog.Dialog('Use Stored Login Info?', 'Would you like to use the login info stored previously?', 'Yes', 'No')
                MessageDialog.Dialog.msgBox.connect(MessageDialog.Dialog.btnYes, QtCore.SIGNAL('clicked()'), lambda : self.useStored(tempLocation))
                MessageDialog.Dialog.msgBox.connect(MessageDialog.Dialog.btnNo, QtCore.SIGNAL('clicked()'), lambda : self.dontUseStored())                
                input.exec_()        
            else:
                connect = DatabaseConnect.Connect()
                MainFunctions.username, MainFunctions.address, MainFunctions.password, MainFunctions.databasename = connect.connect()
            try:
                MainFunctions.database = mysql.connect(user=str(MainFunctions.username),
                                                       host=str(MainFunctions.address),
                                                       passwd=str(MainFunctions.password),
                                                       db=str(MainFunctions.databasename))
            except:
                QtGui.QMessageBox.critical(MainFunctions.window,
                            'Error','Could not connect to database!\nPlease check '
                                           'login info on left and retry!')
                MainFunctions.currentMode = 0
            try:
                global cur
                cur = MainFunctions.database.cursor()
                global ex
                ex = cur.execute
            except:
                pass
            try:
                ex('CREATE TABLE IF NOT EXISTS AssetManager (P_Id int NOT NULL AUTO_INCREMENT, '
                   'Settings text, Bookmarks text, Shots text, Projects text, Models text, '
                   'Shaders text, Images text, Videos text, Audio text, Scripts text, '
                   'Simulations text, PRIMARY KEY(P_Id))')
            except:
                pass
            try:
                ex('CREATE TABLE IF NOT EXISTS Properties (File VARCHAR(100), Location text, '
                   'Name text, Category text, Tags text, Status text, Date text, Author text, '
                   'Version text, Comments text, PRIMARY KEY(File))')
            except:
                pass
            try:
                ex('CREATE TABLE IF NOT EXISTS Icons (Name VARCHAR(100), Location text, '
                   'Data LONGBLOB, PRIMARY KEY(Name))')
            except:
                pass
            
    def useStored(self, tempLocation):
        config = ConfigParser.ConfigParser()
        config.read(tempLocation)
        MainFunctions.address = config.get('Address', 'Address')
        MainFunctions.username = config.get('Username', 'Username')
        encpassword = config.get('Password', 'Password')
        MainFunctions.password = base64.b64decode(encpassword)
        MainFunctions.databasename = config.get('DatabaseName', 'DatabaseName') 
        
    def dontUseStored(self):
        connect = DatabaseConnect.Connect()
        MainFunctions.username, MainFunctions.address, MainFunctions.password, MainFunctions.databasename = connect.connect()            
    
    def closeEvent(self, event):
        reply2 = QtGui.QMessageBox.question(MainFunctions.window, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
        if reply2 == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()          

    def connectToDB(self):
        '''Toggle between locally and dynamically using the program'''
        if MainFunctions.currentMode == 0: #If run locally
            warnings.filterwarnings('ignore')
            username = MainFunctions.window.username_lineEdit.text()
            password = MainFunctions.window.password_lineEdit.text()
            address = MainFunctions.window.address_lineEdit.text()
            databaseName = MainFunctions.window.database_lineEdit.text()
            if not (username == '' or username == ' ' or password == '' or password == ' '
                    or address == '' or address == ' ' or databaseName == '' or databaseName == ' '):    
                try:
                    MainFunctions.database = mysql.connect(user=str(username),
                                                           host=str(address),
                                                           passwd=str(password),
                                                           db=str(databaseName))
                except:
                    QtGui.QMessageBox.critical(MainFunctions.window,
                                'Error',
                                'Could not connect to database!\nPlease check login info!')
                try:
                    global cur
                    cur = MainFunctions.database.cursor()
                    global ex
                    ex = cur.execute
                except:
                    pass
                try:
                    ex('CREATE TABLE IF NOT EXISTS AssetManager (P_Id int NOT NULL AUTO_INCREMENT, '
                       'Settings text, Bookmarks text, Shots text, Projects text, Models text, Shaders text, '
                       'Images text, Videos text, Audio text, Scripts text, Simulations text, PRIMARY KEY(P_Id))')
                except:
                    pass
                try:
                    ex('CREATE TABLE IF NOT EXISTS Properties (File VARCHAR(100), Location text, Name text, '
                       'Category text, Tags text, Status text, Date text, Author text, Version text, '
                       'Comments text, PRIMARY KEY(File))')
                except:
                    pass
                try:
                    ex('CREATE TABLE IF NOT EXISTS Icons (Name VARCHAR(100), Location text, Data LONGBLOB, '
                       'PRIMARY KEY(Name))')
                except:
                    pass
                MainFunctions.currentMode = 1
                QtGui.QMessageBox.information(MainFunctions.window,'Connected','You have connected to the server!')
            else:
                QtGui.QMessageBox.critical(MainFunctions.window, 'Error', 'All fields are required to login!')
        elif MainFunctions.currentMode == 1: #If run dynamically
            MainFunctions.currentMode = 0
            QtGui.QMessageBox.information(MainFunctions.window,'Disconnected','You have disconnected from the server!')

    def copyItem(self):
        '''Copy selected item'''
        currentTab = MainFunctions.window.main_tabWidget.currentIndex()
        currentTab = str(MainFunctions.window.main_tabWidget.tabText(currentTab).toLower())
        currentTab = 'MainFunctions.window.' + currentTab + '_listView'
        currentTab = eval(currentTab)
        items = currentTab.count()
        selectedItems=[]
        rangedList =range(items)
        rangedList.reverse()
        MainFunctions.copiedItems = []
        for i in rangedList:
            if currentTab.isItemSelected(currentTab.item(i))==True:
                MainFunctions.copiedItems.append(str(currentTab.item(i).statusTip()))
                    
    def deleteEntry(self, listVar):
        '''Delete selected item'''
        items = listVar.count()
        selectedItems=[]
        rangedList =range(items)
        rangedList.reverse()
        for i in rangedList:
            if listVar.isItemSelected(listVar.item(i))==True:
                listVar.takeItem(i)

    def deleteItem(self, listVar):
        '''Delete selected item'''
        currentTab = MainFunctions.window.main_tabWidget.currentIndex()
        currentTab = str(MainFunctions.window.main_tabWidget.tabText(currentTab).toLower())
        currentTab = 'MainFunctions.window.' + currentTab + '_listView'
        currentTab = eval(currentTab)
        item = currentTab.takeItem(currentTab.currentRow())
        item = None
            
    def fileProperties(self, listVar):
        '''Open file properties'''
        MainFunctions.propertiesWindow = QtGui.QDialog()
        uiColors = CustomUi.UiColors()
        self.ui = PropertiesWindow.PropertiesPopUp(MainFunctions.propertiesWindow, listVar,
                                                   uiColors.interfaceColor,
                                                   MainFunctions.currentMode,
                                                   MainFunctions.database)
        self.var = MainFunctions.propertiesWindow.exec_()
        
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
    
    def importAssetFile(self, var):
        '''Import Asset manager file into project'''
        if var == 0:
            fileToOpen = QtGui.QFileDialog.getOpenFileName(MainFunctions.window, 'Open file',
                                                           '', ("(*.asset)"))
            fileToOpen = str(fileToOpen)
        if var == 1:
            fileToOpen = self.findSelection(MainFunctions.window.listWidget_2)
            fileToOpen = str(fileToOpen)
        if not fileToOpen == '':
            self.readAssets(fileToOpen)
                                
    def importEntry(self, listName, listVar):
        '''Handling import via right click'''

        files = QtGui.QFileDialog.getOpenFileNames(None, 'Open file',
                                                   '', (""+listName+" (*.*)"))
        for url in files:
            self.addItemToList(url, listVar)

    def itemDropped(self, l, listVar):
        '''Import item when drag and dropped'''
        selectedItem = self.findSelection(listVar)
        for url in l:
            self.addItemToList(url, listVar)

    def openAssetFile(self, var):
        '''Open Asset Manager File'''

        exists = 0
        if var == 0:
            fileToOpen = QtGui.QFileDialog.getOpenFileName(MainFunctions.window, 'Open file',
                                                           '', ("(*.asset)"))
        if var == 1:
            fileToOpen = self.findSelection(MainFunctions.window.listWidget_2)
            fileToOpen = str(fileToOpen)
        if not fileToOpen == '':
            for item in MainFunctions.tabs:
                listVar = getattr(MainFunctions.window, item)
                items = listVar.count()
                if items > 0:
                    exists = 1
            if exists == 1:
                reply = QtGui.QMessageBox.question(MainFunctions.window, 'Message',
                                                   "Are you sure you want to open?\nDoing "
                                                   "so will clear current workspace!",
                                                   QtGui.QMessageBox.Yes | 
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    for item in MainFunctions.tabs:
                        listVar = getattr(MainFunctions.window, item)
                        items = listVar.count()
                        selectedItems=[]
                        rangedList =range(items)
                        rangedList.reverse()
                        for i in rangedList:
                            listVar.takeItem(i)
                    self.readAssets(fileToOpen)
            if exists == 0:
                self.readAssets(fileToOpen)

    def pasteItem(self):
        '''Paste selected item'''
        currentTab = MainFunctions.window.main_tabWidget.currentIndex()
        currentTab = str(MainFunctions.window.main_tabWidget.tabText(currentTab).toLower())
        currentTab = 'MainFunctions.window.' + currentTab + '_listView'
        currentTab = eval(currentTab)
        MainFunctions.copiedItems.reverse()
        for item in MainFunctions.copiedItems:
            self.addItemToList(item, currentTab)
            
    def previewFile(self, listVar):
        '''Future implementation to preview file without opening'''
        pass

    def readAssets(self, fileToOpen):
        fileToOpen = str(fileToOpen)
        config = ConfigParser.ConfigParser()
        config.read(fileToOpen)
        newdict = {'projectsItems':'Projects','modelsItems':'Models',
                   'shadersItems':'Shaders','imagesItems':'Images',
                   'videosItems':'Videos','audioItems':'Audio',
                   'scriptsItems':'Scripts','simulationsItems':'Simulations'}
        for key, value in newdict.iteritems() :
            key = config.get(value, 'Items')
            listName = value.lower() + '_listView'
            if not key == '':
                key = key.split('\n')
                for item in key:
                    if not item == '':
                        self.addItemToList(str(item), getattr(MainFunctions.window, str(listName)))

    def refreshItems(self):
        '''Refresh items properties'''
        for item in MainFunctions.tabs:
            listVar = getattr(MainFunctions.window, item)
            items = listVar.count()
            selectedItems = []
            rangedList = range(items)
            #rangedList.reverse()
            for i in rangedList:
                url = listVar.item(i).statusTip()
                listVar.takeItem(i)
                self.addItemToList(url, listVar)

    def removeFile(self):
        '''Remove file from list'''
        item = MainFunctions.window.listWidget_2.takeItem(MainFunctions.window.listWidget_2.currentRow())
        item = None
        
    def saveAssetFile(self):
        '''Save asset manager file to disc'''
        fileToSave = QtGui.QFileDialog.getSaveFileName(MainFunctions.window, 'Save file',
                                                       '', ("(*.asset)"))
        file = open(fileToSave, 'w+')
        file.write('[Project]\n')
        file.write('Name = ' + 'MyProject' + '\n\n')
        for category in ['Projects', 'Models', 'Shaders', 'Images', 
                         'Videos', 'Audio', 'Scripts', 'Simulations']:
            file.write('[%s]\n' % category)
            file.write('Items = \n')
            view = getattr(MainFunctions.window, category.lower() + '_listView')
            for i in range(view.count()):
                    file.write('\t')
                    file.write(view.item(i).statusTip())
                    file.write('\n')
            file.write('\n\n')
        file.close()          
  
    def setFolder(self):
        '''Add a folder of asset manager files to list'''
        url = QtGui.QFileDialog.getExistingDirectory(MainFunctions.window, 'Select Folder containing asset files','')
        onlyfiles = [ f for f in os.listdir(str(url)) if os.path.isfile(os.path.join(str(url),f)) ]
        files=[]
        for item in onlyfiles:
            if item.endswith(".asset"):
                file = str(url) + str(item)
                fileEntry = QtGui.QListWidgetItem(file, MainFunctions.window.listWidget_2)
                fileEntry.setText(str(item))
                fileEntry.setStatusTip(str(file))

    def sortAscending(self):
        for item in MainFunctions.tabs:
            listVar = getattr(MainFunctions.window, item)
            listVar.sortItems(0)
            
    def sortDescending(self):
        for item in MainFunctions.tabs:
            listVar = getattr(MainFunctions.window, item)
            listVar.sortItems(1)
                    