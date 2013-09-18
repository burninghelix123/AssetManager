'''Module to handle opening assets for Asset Manager'''
import os
import re
import subprocess
import tempfile
import sys
import FileIO
from PyQt4 import QtCore, QtGui
from ..functions import RegistryLookup
from ..functions import MainFunctions
from ..functions import FindSelection

def openFile(self, listVar):
    '''Open selected file with default application'''
    fileToOpen = FindSelection.findSelection(listVar)
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', str(fileToOpen)))
    elif os.name == 'nt':
        os.startfile(str(fileToOpen))
    elif os.name == 'posix':
        subprocess.call(('xdg-open', str(fileToOpen)))

def openFileWithTextEditor(self, listVar):
    '''Open file with text editor'''
    fileToOpen = FindSelection.findSelection(listVar)
    fileToOpen = str(fileToOpen)
    subprocess.Popen('%s %s' % ('notepad', fileToOpen))
    
def openFileWithImageViewer(self, listVar):
    '''Open file with Image Viewer'''
    fileToOpen = FindSelection.findSelection(listVar)
    fileToOpen = str(fileToOpen)
    imageViewerPath = 'C:\\Windows\\System32\\rundll32.exe \'C:\\Program Files\\Windows Photo Viewer\\PhotoViewer.dll\', ImageView_Fullscreen ' + fileToOpen
    subprocess.Popen(imageViewerPath)
    
def openFileWithApp(self, exe, listVar, registryLookupNeeded, keyNumber, program, program2, program3, program4):
    '''Open file with Selected Application'''
    fileToOpen = FindSelection.findSelection(listVar)
    fileToOpen = str(fileToOpen)
    if registryLookupNeeded == 1:
        programPath = RegistryLookup.findPaths(keyNumber, program, program2, program3, program4)
        for item in programPath:
            if re.search('\\\\', item):
                if not re.search('FBX', item):
                    if not re.search('Setup.exe', item):
                        if not re.search('MayaPlugIn', item):
                            if not re.search('unins000', item):
                                if program[0] == 'Maya':
                                    appPath = item + exe
                                if program[0] == 'Houdini':
                                    appPath = re.sub(r'Uninstall Houdini.exe','',item)
                                    appPath = appPath + exe
                                if program[0] == 'Nuke':
                                    nukePath = os.path.split(item)
                                    nukePath = os.path.split(nukePath[0])
                                    nukeExe = nukePath[len(nukePath)-1]
                                    if re.search('v', nukeExe):
                                        nukeExe = (nukeExe.split('v', 1)[0]) + '.exe' 
                                    else:
                                        nukeExe = nukeExe + '.exe'           
                                    appPath = item + nukeExe
    if registryLookupNeeded == 0:
        appPath = exe
    try:
        subprocess.Popen('%s %s' % (appPath, fileToOpen))
    except:
        pass
def openFileWithCustom(self, listVar, customPrograms, customActions, customName, window, url, noUrl, index):
    '''Add program to Open With list'''
    if noUrl == 0:
        url = QtGui.QFileDialog.getOpenFileName(self, 'Select a program to open with:')
    customPrograms += [url]
    url = customPrograms[-1]
    url = os.path.abspath(str(url))
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
    data = '#Custom Application:'
    section = ['CustomPrograms', 'CustomName']
    key = ['Programs', '\n', 'Names']
    value = []
    for item in customPrograms:
        value.append(item)
    value.append('\n')
    for item in customName:
        value.append(item)
    data = FileIO.build(data, section, key, value)
    FileIO.write(data, tempLocation)