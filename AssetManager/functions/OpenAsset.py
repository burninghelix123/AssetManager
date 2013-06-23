'''Module to handle opening assets for Asset Manager'''
import os
import re
import subprocess
from PyQt4 import QtCore, QtGui
from ..functions import RegistryLookup
import tempfile
import sys

def openFile(self, listVar):
    '''Open selected file with default application'''
    fileToOpen = findSelection(listVar)
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', str(fileToOpen)))
    elif os.name == 'nt':
        os.startfile(str(fileToOpen))
    elif os.name == 'posix':
        subprocess.call(('xdg-open', str(fileToOpen)))

def findSelection(listVar):
    '''Find selected item/asset'''
    items = listVar.count()
    fileToOpen = ''
    selectedItems=[]
    rangedList =range(items)
    for i in rangedList:
        if listVar.isItemSelected(listVar.item(i))==True:
            fileToOpen = listVar.item(i).statusTip()
    return(fileToOpen)
    
def openFileWithTextEditor(self, listVar):
    '''Open file with text editor'''
    fileToOpen = findSelection(listVar)
    fileToOpen = str(fileToOpen)
    subprocess.Popen("%s %s" % ('notepad', fileToOpen))
    
def openFileWithImageViewer(self, listVar):
    '''Open file with Image Viewer'''
    fileToOpen = findSelection(listVar)
    fileToOpen = str(fileToOpen)
    imageViewerPath = 'C:\\Windows\\System32\\rundll32.exe \"C:\\Program Files\\Windows Photo Viewer\\PhotoViewer.dll\", ImageView_Fullscreen ' + fileToOpen
    subprocess.Popen(imageViewerPath)
    
def openFileWithApp(self, exe, listVar, registryLookupNeeded, keyNumber, program, program2, program3, program4):
    '''Open file with Selected Application'''
    fileToOpen = findSelection(listVar)
    fileToOpen = str(fileToOpen)
    if registryLookupNeeded == 1:
        programPath = RegistryLookup.findPaths(keyNumber, program, program2, program3, program4)
        if program == ['Maya']:
            if len(programPath) > 1:
                for item in programPath:
                    if not re.search('FBX', item):
                        appPath = item + exe
        elif program == ['Nuke']:

            nukePath = os.path.split(programPath[0])
            nukePath = os.path.split(nukePath[0])
            nukeExe = nukePath[len(nukePath)-1]
            if re.search('v', nukeExe):
                nukeExe = (nukeExe.split('v', 1)[0]) + '.exe' 
            else:
                nukeExe = nukeExe + '.exe'           
            appPath = programPath[0] + nukeExe
        elif program == ['Houdini']:
            appPath = re.sub(r'Uninstall Houdini.exe','',programPath[0])
            appPath = appPath + exe
        else:
            appPath = programPath[0] + exe
    if registryLookupNeeded == 0:
        appPath = exe
    subprocess.Popen("%s %s" % (appPath, fileToOpen))
    
def openFileWithCustom(self, listVar, customPrograms, customActions, customName, window, url, noUrl, index):
    '''Add program to Open With list'''
    if noUrl == 0:
        url = QtGui.QFileDialog.getOpenFileName(self, 'Select a program to open with:')
    customPrograms += [url]
    url = customPrograms[-1]
    url = os.path.abspath(url)
    itemNameExt = os.path.split(url)
    itemNameExt = itemNameExt[1]
    itemName = (itemNameExt.split('.', 1)[0])
    itemName = itemName.title()
    customActions += [itemName]
    customName += [itemName]
    listViews = ['projects', 'models', 'shaders', 'images', 'videos', 'audio', 'scripts', 'simulations']    
    listVarText = listViews[index]
    listVarText = listVarText.title()    
    customActions[-1] = QtGui.QAction(itemName, getattr(window, 'openWith' + listVarText))    
    getattr(window, 'openWith' + listVarText).addAction(customActions[-1])
    customActions[-1].setStatusTip(itemName)
    customActions[-1].triggered.connect(lambda : openFileWithApp(self, url, listVar, 0, None, None, None, None, None))
    writeCustomToFile(customPrograms, customName)

def writeCustomToFile(customPrograms, customName):
    '''Store custom application information'''
    tempDir = tempfile.gettempdir()
    tempLocation = os.path.join(tempDir,'AssetManagerTemp')
    tempLocation = os.path.join(tempLocation,'CustomMenuItems.ini')
    file = open(tempLocation, 'w+')
    file.write('[CustomPrograms]\n')
    file.write('Items = \n')
    for item in customPrograms:
        file.write('\t')
        file.write(item)
        file.write('\n')
    file.write('[CustomName]\n')
    file.write('Items = \n')
    for item in customName:
        file.write('\t')
        file.write(item)
        file.write('\n')
    file.close()   