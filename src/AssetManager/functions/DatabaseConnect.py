'''Modual to connect to database for AssetManager'''
from PyQt4 import QtCore, QtGui
import sys
import os
import base64


class Connect(QtGui.QWidget):
    '''Connect to SQL server'''
    def __init__(self):
        super(Connect, self).__init__()

    def connect(self):
        fileLocation = os.getcwd()
        fileLocation = fileLocation + '\\AssetManagerFiles\\LoginInfo.txt'
        addressui=AddressUi()
        address, ok = addressui.showDialog()
        if ok == False:
            sys.exit()
        usernameui = UsernameUi()
        username, ok = usernameui.showDialog()
        if ok == False:
            sys.exit()
        passwordui=PasswordUi()
        password, ok = passwordui.showDialog()
        if ok == False:
            sys.exit()
        databaseui=DatabaseUi()
        databasename, ok = databaseui.showDialog()
        if ok == False:
            sys.exit()
        storeloginui=StoreLoginUi()
        ok = storeloginui.showDialog()
        if ok == QtGui.QMessageBox.Yes:
            file = open(fileLocation, 'w+')
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
        else:
            pass
        return (username, address, password, databasename) 


class StoreLoginUi(QtGui.QWidget):
    '''Prompt to store login info'''
    def __init__(self):
        super(StoreLoginUi, self).__init__()

    def showDialog(self):
        msg = "Remember login info for next time?"
        ok = QtGui.QMessageBox.question(self, 'Login Info', 
                     msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        return (ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class UseStoredLoginUi(QtGui.QWidget):
    '''Prompt to use stored login info'''
    def __init__(self):
        super(UseStoredLoginUi, self).__init__()

    def showDialog(self):
        msg = "Login using stored information?"
        ok = QtGui.QMessageBox.question(self, 'Login Info', 
                     msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        return (ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class AddressUi(QtGui.QWidget):
    '''Prompt for server address'''
    def __init__(self):
        super(AddressUi, self).__init__()

    def showDialog(self):
        address = ''
        address, ok = QtGui.QInputDialog.getText(self, 'Server Address', 
            'Enter your server address:')
        return (address, ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class DatabaseUi(QtGui.QWidget):
    '''Prompt for database name'''
    def __init__(self):
        super(DatabaseUi, self).__init__()

    def showDialog(self):
        database = ''
        database, ok = QtGui.QInputDialog.getText(self, 'Database Name', 
            'Enter name of database to create table:')
        return (database, ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class PasswordUi(QtGui.QWidget):
    '''Prompt for server password'''
    def __init__(self):
        super(PasswordUi, self).__init__()

    def showDialog(self):
        password = ''
        password, ok = QtGui.QInputDialog.getText(self, 'Server Password', 
            'Enter your server password:', QtGui.QLineEdit.Password)
        return (password, ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

            
class UsernameUi(QtGui.QWidget):
    '''Prompt for server username'''
    def __init__(self):
        super(UsernameUi, self).__init__()
        
    def showDialog(self):
        username = ''
        username, ok = QtGui.QInputDialog.getText(self, 'Server Username', 
            'Enter your server username:')
        return (username, ok)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
