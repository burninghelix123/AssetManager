'''Module to connect to database for AssetManager'''
from PyQt4 import QtCore, QtGui
import sys
import os
import base64
import tempfile
from ..ui import MessageDialog
from ..ui import InputDialog

class Connect(QtGui.QWidget):
    '''Connect to SQL server'''
    def __init__(self):
        super(Connect, self).__init__()
        
    def connect(self):
        validLogin = False
        while validLogin == False:
            ui = InputDialog.Input_Dialog()
            ui.exec_()
            username = InputDialog.Input_Dialog.username
            password = InputDialog.Input_Dialog.password
            address = InputDialog.Input_Dialog.address
            databasename = InputDialog.Input_Dialog.database
            if InputDialog.Input_Dialog.cancel == True:
                validLogin = True
            if validLogin == False:
                if (username == '' or username == ' ' or password == '' or password == ' ' 
                    or address == '' or address == ' ' or databaseName == '' or databaseName == ' '):  
                    QtGui.QMessageBox.information(self,'Error','All fields are required!')
                else:
                    validLogin = True
        if not(username == 'Invalid' and password == 'Invalid' and address == 'Invalid' and databaseName == 'Invalid'):  
            input = MessageDialog.Dialog('Store Login Info:', 'Would you like to store the login info for the server?', 'Yes', 'No')
            MessageDialog.Dialog.msgBox.connect(MessageDialog.Dialog.btnYes, QtCore.SIGNAL('clicked()'), lambda : self.storeLogin(username, address, password, databasename))
            input.exec_()
        return (username, address, password, databasename) 
    
    def storeLogin(self, username, address, password, databasename):
        tempDir = tempfile.gettempdir()
        tempLocation = os.path.join(tempDir,'AssetManagerTemp')
        tempLocation = os.path.join(tempLocation,'LoginInfo.txt')
        file = open(tempLocation, 'w+')
        file.write('[Address]\n')
        file.write('Address = ' + address + '\n\n')
        file.write('[Username]\n')
        file.write('Username = ' + username + '\n\n')       
        file.write('[Password]\n')
        encPassword = base64.b64encode(str(password))
        file.write('Password = ' + encPassword + '\n\n')
        file.write('[DatabaseName]\n')
        file.write('DatabaseName = ' + databasename + '\n\n')
        file.close