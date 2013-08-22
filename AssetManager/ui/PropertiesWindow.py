'''Ui for properties window for Asset Manager'''
from PyQt4 import QtCore, QtGui
import os
import ConfigParser
import string
import MySQLdb as mysql
from ..functions import ItemDisplay
from ..functions import FileIO
import tempfile
from ..ui import CustomUi

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class PropertiesPopUp(QtGui.QDialog):
    '''Pop-up window for asset properties'''
    window = ''
    
    def __init__(self, propertiesWindow, listVar, interfaceColor,
                 currentMode, database, cur, ex):
        QtGui.QWidget.__init__(self)
        PropertiesPopUp.col = CustomUi.ColorPicker.col
        PropertiesPopUp.col1 = CustomUi.ColorPicker.col1
        PropertiesPopUp.col2 = CustomUi.ColorPicker.col2
        PropertiesPopUp.col3 = CustomUi.ColorPicker.col3
        PropertiesPopUp.col4 = CustomUi.ColorPicker.col4
        PropertiesPopUp.cur = cur
        PropertiesPopUp.ex = ex
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
    
    def AddIcon(self):
                                                                
        pass
    
    def saveProperties(self, propertiesWindow, listVar, currentMode, database):
        '''Save properties information'''
        tempDir = tempfile.gettempdir()
        tempLocation = os.path.join(tempDir,'AssetManagerTemp')

        url = self.findSelection(listVar)
        valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
        fileName = ''.join(c for c in str(url) if c in valid_chars)
        items = listVar.count()
        listItem = ''
        selectedItems=[]
        rangedList = range(items)
        itemNumber = ''
        for i in rangedList:
            if listVar.isItemSelected(listVar.item(i))==True:
                itemNumber = i
        listVar.takeItem(itemNumber)
        listItem = QtGui.QListWidgetItem(url)
        itemNameExt = os.path.split(str(url))
        itemNameExt = itemNameExt[1]
        itemName = (itemNameExt.split('.', 1)[0])
        nameField = PropertiesPopUp.window.nameField.text()
        categoryField = PropertiesPopUp.window.categoryField.text()
        tagsField = PropertiesPopUp.window.tagsField.text()
        statusField = PropertiesPopUp.window.statusField.text()
        dateField = PropertiesPopUp.window.dateField.text()
        authorField = PropertiesPopUp.window.authorField.text()
        versionField = PropertiesPopUp.window.versionField.text()
        commentsField = PropertiesPopUp.window.commentsField.toPlainText()
        tempFile = os.path.join(tempLocation, 'Properties')
        tempFile = os.path.join(tempFile,(str(fileName) +'.properties'))
        if currentMode == 0: #If ran locally
            data = '#Properties File for: ' + str(itemName)
            section = ['File', 'Location', 'Name', 'Category', 'Tags', 'Status', 'Date', 'Author', 'Version', 'Comments']
            key = ['File', '\n', 'Location', '\n', 'Name', '\n', 'Category', '\n', 'Tags', '\n', 'Status', '\n', 'Date', '\n', 'Author', '\n', 'Version', '\n', 'Comments']
            value = [str(itemNameExt), '\n', str(url), '\n', str(nameField), '\n', str(categoryField), '\n', str(tagsField), '\n', str(statusField), '\n', str(dateField), '\n', str(authorField), '\n', str(versionField), '\n', str(commentsField)]
            data = FileIO.build(data, section, key, value)
            FileIO.write(data, tempFile)
            if os.path.exists(url):
                itemNameExt = os.path.split(str(url))
                itemNameExt = itemNameExt[1]
                itemName = (itemNameExt.split('.', 1)[0])
                tempPath = os.path.join(tempLocation, 'Images')
                tempPath = os.path.join(tempPath,(str(fileName) + '.png'))
                if os.path.exists(tempPath):
                    pixmap = QtGui.QPixmap()
                    pixmap.load(tempPath)
                    pixmap.scaled(72, 72, QtCore.Qt.IgnoreAspectRatio)
                    icon = QtGui.QIcon()
                    icon.addPixmap(pixmap)
                    listItem.setIcon(icon)                 
                else:
                    if str(url).endswith(('.gif', '.jpg', '.tif', '.png',
                                          '.tiff', '.bmp', '.ico')) == True:
                        icon = QtGui.QIcon()
                        icon.addFile(url,QtCore.QSize(72,72))
                        pixmap = icon.pixmap(QtCore.QSize(72,72),
                                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        listItem.setIcon(icon)
                        pixmap.save((tempPath), 'PNG', 1)
                if os.path.exists(tempFile):
                    data = FileIO.read(tempFile)
                    nameField = data['name']
                    categoryField = data['category']
                    tagsField = data['tags']
                    statusField = data['status']
                    dateField = data['date']
                    authorField = data['author']
                    versionField = data['version']
                    commentsField = data['comments']
                    fileField = itemNameExt
                    locationField = tempLocation
                    info = [('Name:  ', nameField ), ('File:  ', fileField), ('Location:  ',locationField), 
                            ('Category:  ', categoryField), ('Tags:  ',tagsField), ('Status:  ',statusField), 
                            ('Date:  ',dateField), ('Author:  ',authorField), ('Version:  ',versionField), 
                            ('Comments:  ',commentsField)]
                    text = ItemDisplay.itemDisplay(info)
                    listItem.setText(text)
                else:
                    listItem.setText(url)
                listItem.setStatusTip(url)
                QtGui.QListWidget.insertItem(listVar, itemNumber, listItem)
            
        if currentMode == 1:
            propertiesData = (itemNameExt, url, nameField, categoryField,
                              tagsField, statusField, dateField, authorField,
                              versionField, commentsField)
            PropertiesPopUp.ex('REPLACE INTO Properties (File, Location, Name, Category, Tags, Status, Date, Author, Version, Comments) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', propertiesData)            

            if os.path.exists(url):
                tempPath = os.path.join(tempLocation, 'Images')
                tempPath = os.path.join(tempPath, (str(fileName) + 'temp.png'))
                tempPath2 = os.path.join(tempPath,(str(fileName) + '.png'))
                info = [('Name:  ', str(itemNameExt)), ('File:  ', str(url)), ('Location:  ',str(nameField)), 
                        ('Category:  ', str(categoryField)), ('Tags:  ',str(tagsField)), ('Status:  ',str(statusField)), 
                        ('Date:  ',str(dateField)), ('Author:  ',str(authorField)), ('Version:  ',str(versionField)), 
                        ('Comments:  ',str(commentsField))]
                text = ItemDisplay.itemDisplay(info)
                listItem.setText(text)

                if str(url).endswith(('.gif', '.jpg', '.tif',
                                      '.png', '.tiff', '.bmp', '.ico')) == True:
                    icon = QtGui.QIcon()
                    icon.addFile(tempPath2,QtCore.QSize(72,72))
                    pixmap = icon.pixmap(QtCore.QSize(72,72),
                                         QtGui.QIcon.Normal,
                                         QtGui.QIcon.Off)
                    listItem.setIcon(icon)
                    pixmap.save((tempPath), 'PNG', 1)
                    blobValue = open(tempPath, 'rb').read()
                    data = (itemNameExt, url, blobValue)
                    PropertiesPopUp.ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)
                    os.remove(str(tempPath))
                data = 0
                try:
                    data = PropertiesPopUp.ex('SELECT Data FROM Icons WHERE Location=%s',url)
                except:
                    pass
                if data >= 1:
                    ablob = PropertiesPopUp.cur.fetchone()[0]
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(ablob)
                    pixmap.scaled(72, 72, QtCore.Qt.IgnoreAspectRatio)
                    icon = QtGui.QIcon()
                    icon.addPixmap(pixmap)
                    listItem.setIcon(icon)
                listItem.setStatusTip(url)
                QtGui.QListWidget.insertItem(listVar, itemNumber, listItem)
        propertiesWindow.close()

    def customIcon(self, listVar, currentMode, database):
        '''Add custom icon to file/asset'''
        items = listVar.count()
        listItem = ''
        selectedItems=[]
        rangedList =range(items)
        itemNumber = ''
        for i in rangedList:
            if listVar.isItemSelected(listVar.item(i))==True:
                item = listVar.item(i)
        if currentMode == 0: #If ran locally
            url = QtGui.QFileDialog.getOpenFileName(self,
                                                    'Open file','', ("Select Image: (*.*)"))
            url = os.path.abspath(url)
            itemtext= str(item.statusTip())
            valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
            fileName = ''.join(c for c in str(itemtext) if c in valid_chars)
            tempDir = tempfile.gettempdir()
            tempLocation = os.path.join(tempDir,'AssetManagerTemp')
            itemNameExt = os.path.split(str(itemtext))
            itemNameExt = itemNameExt[1]
            itemName = (itemNameExt.split('.', 1)[0])
            tempPath = os.path.join(tempLocation, 'Images')
            tempPath = os.path.join(tempPath,(str(fileName) + '.png'))
            tempName = str(itemName)            
            pixmap = QtGui.QPixmap()
            pixmap.load(url)
            pixmap.scaled(72, 72, QtCore.Qt.IgnoreAspectRatio)
            icon = QtGui.QIcon()
            icon.addPixmap(pixmap)
            item.setIcon(icon) 
            pixmap.save((tempPath), 'PNG', 1)
                    
        if currentMode == 1: #If ran dynamically
            url = QtGui.QFileDialog.getOpenFileName(self, 'Open file','',
                                                    ("Select Image: (*.*)"))
            url = os.path.abspath(url)
            itemtext = str(item.statusTip())
            valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
            fileName = ''.join(c for c in str(itemtext) if c in valid_chars)
            tempDir = tempfile.gettempdir()
            tempLocation = os.path.join(tempDir,'AssetManagerTemp')
            itemNameExt = os.path.split(str(itemtext))
            itemNameExt = itemNameExt[1]
            itemName = (itemNameExt.split('.', 1)[0])
            tempPath = os.path.join(tempLocation, 'Images')
            tempPath = os.path.join(tempPath, (str(fileName) + 'temp.png'))

            pixmap = QtGui.QPixmap()
            pixmap.load(url)
            pixmap.scaled(72, 72, QtCore.Qt.IgnoreAspectRatio)
            icon = QtGui.QIcon()
            icon.addPixmap(pixmap)
            item.setIcon(icon) 
            pixmap.save((tempPath), 'PNG', 1)

            blobValue = open(tempPath, 'rb').read()
            data = (itemNameExt, itemtext, blobValue)
            PropertiesPopUp.ex('REPLACE INTO Icons(Name, Location, Data) VALUES(%s, %s, %s)', data)                
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
        tempDir = tempfile.gettempdir()
        tempLocation = os.path.join(tempDir,'AssetManagerTemp')
        item = self.findSelection(listVar)
        valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
        fileName = ''.join(c for c in str(item) if c in valid_chars)
        itemNameExt = os.path.split(str(item))
        itemNameExt = itemNameExt[1]
        itemName = (itemNameExt.split('.', 1)[0])
        tempFile = os.path.join(tempLocation, 'Properties')
        tempFile = os.path.join(tempFile,(str(fileName) +'.properties'))
        if currentMode == 0: #If ran locally
            if os.path.exists(tempFile):
                data = FileIO.read(tempFile)
                nameField = data['name']
                categoryField = data['category']
                tagsField = data['tags']
                statusField = data['status']
                dateField = data['date']
                authorField = data['author']
                versionField = data['version']
                commentsField = data['comments']
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
                PropertiesPopUp.ex("SELECT * FROM Properties WHERE File=%s",itemNameExt)
                data = PropertiesPopUp.cur.fetchone()
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
