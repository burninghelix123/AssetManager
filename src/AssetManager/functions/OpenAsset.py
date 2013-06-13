'''Module to handle opening assets for Asset Manager'''
import os
import subprocess
from ..functions import RegistryLookup

def openFile(self, listVar):
    '''Open selected file with default application'''
    fileToOpen = findSelection(listVar)
    os.startfile(str(fileToOpen))
    
def openFileWith(self, listVar):
    '''Future implementation for custom applications'''
    pass

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
    
def openFileWithApp(self, app, exe, listVar):
    '''Open file with Application'''
    fileToOpen = findSelection(listVar)
    fileToOpen = str(fileToOpen)
    registryLookup = RegistryLookup.RegistryLookup()
    appPath = getattr(registryLookup, app) + exe
    subprocess.Popen("%s %s" % (appPath, fileToOpen))
