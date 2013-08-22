from PyQt4 import QtCore, QtGui
import sys
import os
import base64
import tempfile
import MySQLdb as mysql
from ..functions import FileIO
from ..ui import MessageDialog
from ..ui import InputDialog
import tempfile
import warnings

def connect(username, address, password, databasename):
    '''Connects to a mysql server with the provided login info'''
    cur = ''
    ex = ''
    warnings.filterwarnings('ignore')
    try:
        database = mysql.connect(user=str(username),
                                               host=str(address),
                                               passwd=str(password),
                                               db=str(databasename))
        connected = 1
    except:
        QtGui.QMessageBox.critical(None,
                    'Error','Could not connect to database!\nPlease check '
                                   'login info on left and retry!')
        connected = 0
    try:
        cur = database.cursor()
        ex = cur.execute
    except:
        pass
    try:
        ex('CREATE TABLE IF NOT EXISTS AssetManager (P_Id int NOT NULL AUTO_INCREMENT, '
           'Settings text, Bookmarks text, Shots text, Projects text, Models text, '
           'Shaders text, Images text, Videos text, Audio text, Scripts text, '
           'Simulations text, PRIMARY KEY(P_Id))')
    except:
        pass
    try:
        ex('CREATE TABLE IF NOT EXISTS Properties (File VARCHAR(100), Location text, '
           'Name text, Category text, Tags text, Status text, Date text, Author text, '
           'Version text, Comments text, PRIMARY KEY(File))')
    except:
        pass
    try:
        ex('CREATE TABLE IF NOT EXISTS Icons (Name VARCHAR(100), Location text, '
           'Data LONGBLOB, PRIMARY KEY(Name))')
    except:
        pass
    return(connected, cur, ex)

def loginPrep():
    '''Checks for saved login info and sets temp location'''
    warnings.filterwarnings('ignore')
    connected = ''
    tempDir = tempfile.gettempdir()
    tempLocation = os.path.join(tempDir,'AssetManagerTemp')
    tempLocation = os.path.join(tempLocation,'LoginInfo.txt')
    if os.path.exists(tempLocation):
        input = MessageDialog.Dialog('Use Stored Login Info?', 'Would you like to use the login info stored previously?', 'Yes', 'No')
        input = input.exec_()
        if input == 0:
            connected, cur, ex = useStored(tempLocation, connected)    
        if input == 1:
            connected, cur, ex = dontUseStored(connected)        
    else:
        username, address, password, databasename = loginToDB()
        connected, cur, ex = connect(username, address, password, databasename)
    return(connected, cur, ex)

def loginToDB():
    '''Requests login info from user'''
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
            for item in (username, password, address, databasename):
                if str(item).strip():
                    validLogin = True
                else: 
                    QtGui.QMessageBox.information(None,'Error','All fields are required!')
                    validLogin = False
                    break
    if not username == None:
        input = MessageDialog.Dialog('Store Login Info:', 'Would you like to store the login info for the server?', 'Yes', 'No')
        MessageDialog.Dialog.msgBox.connect(MessageDialog.Dialog.btnYes, QtCore.SIGNAL('clicked()'), lambda : storeLogin(username, address, password, databasename))
        input.exec_()
    return (username, address, password, databasename) 

def useStored(tempLocation, connected):
    '''Reads login info from file'''
    data = FileIO.read(tempLocation)
    address = data['address']
    username = data['username']
    password = data['password']
    password = base64.b64decode(password)
    databasename = data['databasename']
    connected, cur, ex = connect(username, address, password, databasename)
    return(connected, cur, ex)

def dontUseStored(connected):
    username, address, password, databasename = loginToDB()
    connected, cur, ex = connect(username, address, password, databasename)
    return(connected, cur, ex)

def storeLogin(username, address, password, databasename):
    '''Stores login info to file'''
    tempDir = tempfile.gettempdir()
    tempLocation = os.path.join(tempDir,'AssetManagerTemp')
    tempLocation = os.path.join(tempLocation,'LoginInfo.txt')
    encPassword = base64.b64encode(str(password))
    data = '#Login Information:'
    section = ['Address', 'Username', 'Password', 'DatabaseName']
    key = ['Address', '\n', 'Username', '\n', 'Password', '\n', 'DatabaseName']
    value = [str(address), '\n', str(username), '\n', str(encPassword), '\n', str(databasename)]
    data = FileIO.build(data, section, key, value)
    FileIO.write(data, tempLocation)
