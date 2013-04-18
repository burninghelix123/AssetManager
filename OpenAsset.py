'''Module to handle opening assets for Asset Manager'''
import os
import subprocess
import RegistryLookup

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

def openFileWithMaya(self, listVar):
    '''Open file with Maya'''
    fileToOpen = findSelection(listVar)
    fileToOpen = str(fileToOpen)
    registryLookup = RegistryLookup.RegistryLookup()
    mayaPath = registryLookup.mayaPath + 'bin\maya.exe'
    subprocess.Popen("%s %s" % (mayaPath, fileToOpen))
    
def openFileWithHoudini(self, listVar):
    '''Open file with Houdini'''
    fileToOpen = findSelection(listVar)
    fileToOpen = str(fileToOpen)
    registryLookup = RegistryLookup.RegistryLookup()
    houdiniPath = registryLookup.houdiniPath + 'bin\houdini.exe'
    subprocess.Popen("%s %s" % (houdiniPath, fileToOpen))
    
def openFileWithNuke(self, listVar):
    '''Open file with Nuke'''
    fileToOpen = findSelection(listVar)
    fileToOpen = str(fileToOpen)
    registryLookup = RegistryLookup.RegistryLookup()
    nukePath = registryLookup.nukePath
    subprocess.Popen("%s %s" % (nukePath, fileToOpen))
    
def openFileWithPhotoshop(self, listVar):
    '''Open file with Photoshop'''
    fileToOpen = findSelection(listVar)
    fileToOpen = str(fileToOpen)
    registryLookup = RegistryLookup.RegistryLookup()
    photoshopPath = registryLookup.photoshopPath + 'Photoshop.exe'
    subprocess.Popen("%s %s" % (photoshopPath, fileToOpen))
    
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
