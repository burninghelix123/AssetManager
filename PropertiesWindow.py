'''Ui for properties window for Asset Manager'''
from PyQt4 import QtCore, QtGui
import os
import ConfigParser
import MySQLdb as mysql
import ItemDisplay

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class PropertiesPopUp(QtGui.QDialog):
    '''Pop-up window for asset properties'''
    window = ''
    col = QtGui.QColor(0, 0, 0)
    col1 = QtGui.QColor(0, 0, 0) 
    col2 = QtGui.QColor(0, 0, 0) 
    col3 = QtGui.QColor(0, 0, 0)
    col4 = QtGui.QColor(0, 0, 0)
    
    def __init__(self, propertiesWindow, listVar, interfaceColor,
                 currentMode, database, col, col1, col2, col3, col4):
        QtGui.QWidget.__init__(self)
        PropertiesPopUp.col = col
        PropertiesPopUp.col1 = col1
        PropertiesPopUp.col2 = col2
        PropertiesPopUp.col3 = col3
        PropertiesPopUp.col4 = col4
        self.setupUi(propertiesWindow, listVar, interfaceColor,
                     currentMode, database)

    def findSelection(self, listVar):
        '''Retrieve selected item'''
        items = listVar.count()
        fileToOpen = ''
        selectedItems = []
        rangedList = range(items)
        for i in rangedList:
            if listVar.isItemSelected(listVar.item(i)) == True:
                fileToOpen = listVar.item(i).statusTip()
        return(fileToOpen)

    def writeProperties(self, listVar, itemName, fileLocation, nameField,
                        categoryField, tagsField, statusField,
                        dateField, authorField, versionField,
                        commentsField):
        '''Writes information to file'''        
        item = self.findSelection(listVar)
        itemSplit = []
        itemPath = item.split('\\')
        itemPath = filter(None, itemPath)
        itemName = itemPath[len(itemPath)-1]
        itemName = (itemName.split('.', 1)[0])
        file = open(fileLocation + itemName + '.properties', 'w+')
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
    
    def saveProperties(self, propertiesWindow, listVar, currentMode, database):
        '''Save properties information'''
        if currentMode == 0: #If ran locally
            fileLocation = os.getcwd()
            fileLocation = fileLocation + '\\AssetManagerFiles\\'
            item = self.findSelection(listVar)
            itemSplit = []
            itemPath = item.split('\\')
            itemPath = filter(None, itemPath)
            itemName = itemPath[len(itemPath)-1]
            itemName = (itemName.split('.', 1)[0])
            nameField = PropertiesPopUp.window.nameField.text()
            categoryField = PropertiesPopUp.window.categoryField.text()
            tagsField = PropertiesPopUp.window.tagsField.text()
            statusField = PropertiesPopUp.window.statusField.text()
            dateField = PropertiesPopUp.window.dateField.text()
            authorField = PropertiesPopUp.window.authorField.text()
            versionField = PropertiesPopUp.window.versionField.text()
            commentsField = PropertiesPopUp.window.commentsField.toPlainText()

            self.writeProperties(listVar, itemName, fileLocation, nameField,
                            categoryField, tagsField, statusField,
                            dateField, authorField, versionField,
                            commentsField)
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
                            text = ItemDisplay.itemDisplay(fileField, locationField, nameField,
                                                           categoryField, tagsField, statusField,
                                                           dateField, authorField, versionField,
                                                           commentsField)
                            item.setText(text)
                        else:
                            item.setText(url)
                        item.setStatusTip(url)
            self.close()
            
        if currentMode == 1: #If ran dynamically
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
            cur = database.cursor()
            ex = cur.execute
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
                            cur = database.cursor()
                            ex = cur.execute
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
                                cur = database.cursor()
                                ex = cur.execute
                                ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                                os.remove(str(tempPath))
                            else:                    
                                item = QtGui.QListWidgetItem(url)
                                QtGui.QListWidget.insertItem(listVar, i, item)
                        item.setStatusTip(url)
                        data = 0
                        try:
                            cur = database.cursor()
                            ex = cur.execute
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
        propertiesWindow.close()
        
    def customIcon(self, listVar, currentMode, database):
        '''Add custom icon to file/asset'''
        if currentMode == 0: #If ran locally
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
                    
        if currentMode == 1: #If ran dynamically
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
                            cur = database.cursor()
                            ex = cur.execute
                            ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                    os.remove(str(tempPath))
        
    def setupUi(self, propertiesWindow, listVar, interfaceColor,
                currentMode, database):
        '''Create properties window UI'''
        propertiesWindow.setObjectName(_fromUtf8("dialog"))
        propertiesWindow.resize(235, 377)
        PropertiesPopUp.window = self
        self.save = QtGui.QPushButton(propertiesWindow)
        self.save.setGeometry(QtCore.QRect(5, 350, 75, 23))
        self.save.setObjectName(_fromUtf8("save"))
        self.save.clicked.connect(lambda : self.saveProperties(propertiesWindow, listVar, currentMode, database)) 
        self.closebtn = QtGui.QPushButton(propertiesWindow)
        self.closebtn.setGeometry(QtCore.QRect(155, 350, 75, 23))
        self.closebtn.setObjectName(_fromUtf8("close"))
        self.closebtn.clicked.connect(propertiesWindow.close)
        self.icon = QtGui.QPushButton(propertiesWindow)
        self.icon.setGeometry(QtCore.QRect(80, 350, 75, 23))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.icon.clicked.connect(lambda : self.customIcon(listVar, currentMode, database)) 
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
        QtCore.QMetaObject.connectSlotsByName(propertiesWindow)
        self.setupUiColor(propertiesWindow, listVar, interfaceColor, currentMode, database)
        self.retranslateUi(propertiesWindow, listVar, currentMode, database)

    def setupUiColor(self, propertiesWindow, listVar, interfaceColor,
                     currentMode, database):
        '''Color interface based on main application window'''
        if interfaceColor == 1: #UI Dark Layout
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
        if interfaceColor == 2: #UI Light Layout
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
        if interfaceColor == 3: #UI Custom Layout
            propertiesWindow.setStyleSheet('background-color: %(color)s;' % {'color':PropertiesPopUp.col.name()})
            self.name.setStyleSheet('QLabel {color: %(color4)s}' % {'color4':PropertiesPopUp.col4.name()})
            self.category.setStyleSheet('QLabel {color: %(color4)s}' % {'color4':PropertiesPopUp.col4.name()})
            self.tags.setStyleSheet('QLabel {color: %(color4)s}' % {'color4':PropertiesPopUp.col4.name()})
            self.status.setStyleSheet('QLabel {color: %(color4)s}' % {'color4':PropertiesPopUp.col4.name()})
            self.date.setStyleSheet('QLabel {color: %(color4)s}' % {'color4':PropertiesPopUp.col4.name()})
            self.author.setStyleSheet('QLabel {color: %(color4)s}' % {'color4':PropertiesPopUp.col4.name()})
            self.version.setStyleSheet('QLabel {color: %(color4)s}' % {'color4':PropertiesPopUp.col4.name()})
            self.comments.setStyleSheet('QLabel {color: %(color4)s}' % {'color4':PropertiesPopUp.col4.name()})           
            self.nameField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':PropertiesPopUp.col1.name(),'color4':PropertiesPopUp.col4.name()})
            self.categoryField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':PropertiesPopUp.col1.name(),'color4':PropertiesPopUp.col4.name()})
            self.tagsField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':PropertiesPopUp.col1.name(),'color4':PropertiesPopUp.col4.name()})
            self.statusField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':PropertiesPopUp.col1.name(),'color4':PropertiesPopUp.col4.name()})
            self.dateField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':PropertiesPopUp.col1.name(),'color4':PropertiesPopUp.col4.name()})
            self.authorField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1':PropertiesPopUp.col1.name(),'color4':PropertiesPopUp.col4.name()})
            self.versionField.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color: %(color4)s}' % {'color1':PropertiesPopUp.col1.name(),'color4':PropertiesPopUp.col4.name()})
            self.commentsField.setStyleSheet('QTextEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color: %(color4)s}' % {'color1':PropertiesPopUp.col1.name(),'color4':PropertiesPopUp.col4.name()})
            self.save.setStyleSheet(' color: %(color4)s; QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}' % {'color4':PropertiesPopUp.col4.name()})
            self.icon.setStyleSheet(' color: %(color4)s; QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}' % {'color4':PropertiesPopUp.col4.name()})
            self.closebtn.setStyleSheet(' color: %(color4)s; QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}' % {'color4':PropertiesPopUp.col4.name()})

    def retranslateUi(self, propertiesWindow, listVar, currentMode, database):
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
        self.populatePropertiesWindow(propertiesWindow, listVar, currentMode, database)

    def populatePropertiesWindow(self, propertiesWindow, listVar,
                                 currentMode, database):
        '''Populates stored information into fields'''
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
            
            if currentMode == 0: #If ran locally
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
                    
            if currentMode == 1: #If ran dynamically
                try:
                    cur = database.cursor()
                    ex = cur.execute
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
