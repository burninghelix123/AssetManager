'''Adds the capability to manage what programs display in the open with menu'''

from PyQt4 import QtCore
from PyQt4 import QtGui
import sys
import tempfile
import os
from ..ui import CustomUi

class ManageApplications(QtGui.QListView):
    '''Class for building the window for managing visible applications'''
    window = ''
    def __init__(self, window):
        QtGui.QListView.__init__(self)
        ManageApplications.window = window
        
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def itemClicked(self, item):
        '''Action for checking or unchecking a program'''
        menus = ['openWithProjects', 'openWithModels', 'openWithShaders', 'openWithImages', 'openWithVideos', 'openWithAudio', 'openWithScripts', 'openWithSimulations']
        state = ['UNCHECKED', 'TRISTATE',  'CHECKED'][item.checkState()]
        for menu in menus:
            actions = getattr(ManageApplications.window, menu)
            actions = actions.actions()
            if state == 'CHECKED':
                actions[item.row()].setVisible(True)
            if state == 'UNCHECKED':
                actions[item.row()].setVisible(False)
                
    def setupUi(self, model, appManager):
        '''Sets up checkboxes and visibility'''
        programs = []
        actions = ManageApplications.window.openWithSimulations.actions()
        for action in actions:
            visible = action.isVisible()
            text = str(action.text())
            if text.strip():
                item = QtGui.QStandardItem(action.text())
                if CustomUi.UiColors.interfaceColor == 3:
                    item.setForeground(CustomUi.ColorPicker.col4)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                check = QtCore.Qt.Checked if visible == True else QtCore.Qt.Unchecked
                item.setCheckState(check)
                item.setCheckable(True)
                model.appendRow(item)
        self.setupUiColor(appManager)
        
    def setupUiColor(self, appManager):
        '''Color interface based on main application window'''
        if CustomUi.UiColors.interfaceColor == 1: #UI Dark Layout
            appManager.setStyleSheet('background-color:darkgrey;')
        if CustomUi.UiColors.interfaceColor == 2: #UI Light Layout
            appManager.setStyleSheet('') 
        if CustomUi.UiColors.interfaceColor == 3: #UI Custom Layout
            appManager.setStyleSheet('background-color: %(color)s;' % {'color':CustomUi.ColorPicker.col.name()})
        
    def writeToFile(self):
        '''Saves visible and hidden programs to file to be loaded on next program start'''
        actions = ManageApplications.window.openWithSimulations.actions()
        programs = []
        tempDir = tempfile.gettempdir()
        tempLocation = os.path.join(tempDir,'AssetManagerTemp')
        tempLocation = os.path.join(tempLocation,'ManageApplications.ini')
        file = open(tempLocation, 'w+')
        file.write('[Programs]\n')
        for action in actions:
            visible = action.isVisible()
            file.write(action.text() + ' = ' + str(visible) + '\n')
        file.close()   
        
    def closeEvent(self, event):
        self.writeToFile()
        event.accept()

            
def main(appManager):
    '''Creates and shows window'''
    model = QtGui.QStandardItemModel()
    appManager.setModel(model)
    appManager.setupUi(model, appManager)
    appManager.setWindowTitle('Application Manager')
    appManager.setMinimumSize(300,200)
    appManager.setMaximumSize(300,250)
    appManager.show()
    model.itemChanged.connect(appManager.itemClicked)
