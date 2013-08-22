'''Main functions for Asset Manager'''
from PyQt4 import QtCore, QtGui
import MySQLdb as mysql
import os
import ConfigParser
from ..ui import PropertiesWindow
from ..ui import CustomUi
from ..ui import MessageDialog
from ..ui import InputDialog
from ..functions import AddItem
from ..functions import DatabaseConnect


class MainFunctions():
    
    def __init__(self, window, mainWindow, currentMode, database,
                 copiedItems, propertiesWindow, cur, ex):
        MainFunctions.database = database
        MainFunctions.currentMode = currentMode
        MainFunctions.mainWindow = mainWindow
        MainFunctions.window = window
        MainFunctions.copiedItems = copiedItems
        MainFunctions.propertiesWindow = propertiesWindow
        MainFunctions.cur = cur
        MainFunctions.ex = ex
        MainFunctions.tabs = ['projects_listView', 'models_listView',
                              'shaders_listView', 'images_listView',
                              'videos_listView', 'audio_listView',
                              'scripts_listView', 'simulations_listView']
   
    def addFile(self):
        '''Add asset file to saved list'''
        url = QtGui.QFileDialog.getOpenFileName(MainFunctions.window, 'Select asset file to add',
                                                '', ('Select Asset: (*.Asset)'))
        fileEntry = QtGui.QListWidgetItem(url, MainFunctions.window.listWidget_2)
        url = os.path.abspath(url)
        itemNameExt = os.path.split(url)
        itemNameExt = itemNameExt[1]
        itemName = (itemNameExt.split('.', 1)[0])
        fileEntry.setText(str(itemName))
        fileEntry.setStatusTip(str(url))
        
    def closeEvent(self, event):
        reply2 = QtGui.QMessageBox.question(MainFunctions.window, 'Message',
            'Are you sure you want to quit?', QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
        if reply2 == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()          

    def connectToDB(self):
        '''Toggle between locally and dynamically using the program'''
        if MainFunctions.currentMode == 0: #If run locally
            validLogin = False
            username = MainFunctions.window.username_lineEdit.text()
            password = MainFunctions.window.password_lineEdit.text()
            address = MainFunctions.window.address_lineEdit.text()
            databaseName = MainFunctions.window.database_lineEdit.text()
            for item in (username, password, address, databaseName):
                if str(item).strip():
                    validLogin = True
                else: 
                    QtGui.QMessageBox.information(None,'Error','All fields are required!')
                    validLogin = False
                    break
            if validLogin == True:
                MainFunctions.currentMode, MainFunctions.cur, MainFunctions.ex = DatabaseConnect.connect(username, address, password, databaseName)
                QtGui.QMessageBox.information(MainFunctions.window,'Connected','You have connected to the server!')
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
                                                   MainFunctions.database,
                                                   MainFunctions.cur,
                                                   MainFunctions.ex)
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
                                                           '', ('(*.asset)'))
            fileToOpen = str(fileToOpen)
        if var == 1:
            fileToOpen = self.findSelection(MainFunctions.window.listWidget_2)
            fileToOpen = str(fileToOpen)
        if fileToOpen.strip():
            self.readAssets(fileToOpen)
                                
    def importEntry(self, listName, listVar):
        '''Handling import via right click'''
        files = QtGui.QFileDialog.getOpenFileNames(None, 'Open file',
                                                   '', (''+listName+' (*.*)'))
        for url in files:
            AddItem.addItemToList(url, listVar, MainFunctions.currentMode, MainFunctions.cur, MainFunctions.ex)

    def itemDropped(self, l, listVar):
        '''Import item when drag and dropped'''
        selectedItem = self.findSelection(listVar)
        for url in l:
            AddItem.addItemToList(url, listVar, MainFunctions.currentMode, MainFunctions.cur, MainFunctions.ex)

    def openAssetFile(self, var):
        '''Open Asset Manager File'''

        exists = 0
        if var == 0:
            fileToOpen = QtGui.QFileDialog.getOpenFileName(MainFunctions.window, 'Open file',
                                                           '', ('(*.asset)'))
        if var == 1:
            fileToOpen = self.findSelection(MainFunctions.window.listWidget_2)
            fileToOpen = str(fileToOpen)
        if fileToOpen.strip():
            for item in MainFunctions.tabs:
                listVar = getattr(MainFunctions.window, item)
                items = listVar.count()
                if items > 0:
                    exists = 1
            if exists == 1:
                reply = QtGui.QMessageBox.question(MainFunctions.window, 'Message',
                                                   'Are you sure you want to open?\nDoing '
                                                   'so will clear current workspace!',
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
            AddItem.addItemToList(item, currentTab, MainFunctions.currentMode, MainFunctions.cur, MainFunctions.ex)
            
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
            if key.strip():
                key = key.split('\n')
                for item in key:
                    if item.strip():
                        AddItem.addItemToList(str(item), getattr(MainFunctions.window, str(listName)), MainFunctions.currentMode, MainFunctions.cur, MainFunctions.ex)

    def refreshItems(self):
        '''Refresh items properties'''
        for item in MainFunctions.tabs:
            listVar = getattr(MainFunctions.window, item)
            items = listVar.count()
            urls = []
            if item > 0:
                rangedList = range(items)
                rangedList.reverse()
                for i in rangedList:
                    url = listVar.item(i).statusTip()
                    urls += url,
                    listVar.takeItem(i)
                for url in urls:    
                    AddItem.addItemToList(url, listVar, MainFunctions.currentMode, MainFunctions.cur, MainFunctions.ex)

    def removeFile(self):
        '''Remove file from list'''
        item = MainFunctions.window.listWidget_2.takeItem(MainFunctions.window.listWidget_2.currentRow())
        item = None
        
    def saveAssetFile(self):
        '''Save asset manager file to disc'''
        fileToSave = QtGui.QFileDialog.getSaveFileName(MainFunctions.window, 'Save file',
                                                       '', ('(*.asset)'))
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
                    