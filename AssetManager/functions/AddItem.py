''' Adds a file to a list while loading any icons or properties.''' 
import os
import string
import tempfile
from PyQt4 import QtCore, QtGui
from ..functions import FileIO
from ..functions import ItemDisplay


def addItemToList(url, listVar, currentMode, cur, ex):
    '''Add asset manager file to list'''
    url = os.path.abspath(str(url))
    valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
    fileName = ''.join(c for c in str(url) if c in valid_chars)
    if currentMode == 0: #If run locally
        if os.path.exists(url):
            tempDir = tempfile.gettempdir()
            tempLocation = os.path.join(tempDir,'AssetManagerTemp')
            itemNameExt = os.path.split(str(url))
            itemNameExt = itemNameExt[1]
            itemName = (itemNameExt.split('.', 1)[0])
            tempFile = os.path.join(tempLocation, 'Properties')
            tempFile = os.path.join(tempFile,(str(fileName) +'.properties'))
            tempPath = os.path.join(tempLocation, 'Images')
            tempPath = os.path.join(tempPath,(str(fileName) + '.png'))
            item = QtGui.QListWidgetItem(url, listVar)
            if os.path.exists(tempPath): #If saved image exists load
                pixmap = QtGui.QPixmap()
                pixmap.load(tempPath)
                pixmap.scaled(72, 72, QtCore.Qt.IgnoreAspectRatio)
                icon = QtGui.QIcon()
                icon.addPixmap(pixmap)
                item.setIcon(icon) 
            else: # If no saved image and file is an image load 
                if str(url).endswith(('.gif', '.jpg', '.tif',
                                      '.png', '.tiff', '.bmp', '.ico')) == True:
                    icon = QtGui.QIcon()
                    icon.addFile(url,QtCore.QSize(72,72))
                    pixmap = icon.pixmap(QtCore.QSize(72,72),
                                         QtGui.QIcon.Normal,
                                         QtGui.QIcon.Off)
                    item.setIcon(icon)
            if os.path.exists(tempFile): #If properties file exists
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
                locationField = url
                info = [('Name:  ', nameField ), ('File:  ', fileField),
                        ('Location:  ',locationField), ('Category:  ', categoryField),
                        ('Tags:  ',tagsField), ('Status:  ',statusField), 
                        ('Date:  ',dateField), ('Author:  ',authorField),
                        ('Version:  ',versionField), ('Comments:  ',commentsField)]
                text = ItemDisplay.itemDisplay(info)
                item.setText(text)
            else: #Else no info to load
                item.setText(url)
            item.setStatusTip(url)
            
    if currentMode == 1: #If run dynamically
        if os.path.exists(url):
            tempDir = tempfile.gettempdir()
            tempLocation = os.path.join(tempDir,'AssetManagerTemp')
            itemNameExt = os.path.split(url)
            itemNameExt = itemNameExt[1]
            itemName = (itemNameExt.split('.', 1)[0])
            tempPath = os.path.join(tempLocation, 'Images')
            tempPath = os.path.join(tempPath, (str(fileName) + 'temp.png'))
            tempPath2 = os.path.join(tempPath,(str(fileName) + '.png'))
            item = QtGui.QListWidgetItem(url, listVar)
            data = 0
            try:
                data = ex('SELECT Data FROM Icons WHERE Location=%s',url)
            except:
                pass
            if data >= 1: #If icon found on server
                ablob = cur.fetchone()[0]
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(ablob)
                pixmap.scaled(72, 72, QtCore.Qt.IgnoreAspectRatio)
                icon = QtGui.QIcon()
                icon.addPixmap(pixmap)
                item.setIcon(icon)
            else: 
                if str(url).endswith(('.gif', '.jpg', '.tif',
                                      '.png', '.tiff', '.bmp', '.ico')) == True: 
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
            item.setStatusTip(url)
            data = 0
            try:
                data = ex('SELECT * FROM Properties WHERE Location=%s',url)
            except:
                pass
            if data >= 1: #If properties info found on server
                ablob = cur.fetchall()[0]
                info = [('Name:  ', ablob[0] ), ('File:  ', ablob[1]),
                        ('Location:  ',ablob[2]), ('Category:  ', ablob[3]),
                        ('Tags:  ',ablob[4]), ('Status:  ',ablob[5]), 
                        ('Date:  ',ablob[6]), ('Author:  ',ablob[7]),
                        ('Version:  ',ablob[8]), ('Comments:  ',ablob[9])]
                text = ItemDisplay.itemDisplay(info)
                item.setText(text)
            else:
                item.setText(url)