#!/usr/bin/python
# -*- coding: utf-8 -*-

# AssetManager.py
# 2013 April 8

'''AssetManager.py is a program I created to manage and organize
assets and files either locally on a computer or dynamically on
an SQL server.

===========================================
Copyright © 2013 Craig Barnett
===========================================

This program is to be distributed only by the owner, it was created
in the hope that it will be useful to artists, but WITHOUT ANY WARRANTY.

===========================================
Craig Barnett,
302 W 40th St Apt A, Savannah, Ga 31401
mailto: craigbme@hotmail.com
http://www.bhvfx.com
===========================================

This script allows the user to import files and add a variety of properties
and information to them along with custom icons. The asset manager can
either run locally, storing all of the information on your computer,
or dynamically through a SQL database. It has options for opening files
with Maya, Houdini, Nuke, Photoshop, Text Editor, Photo Viewer, and
the default application. It has 8 categories to organize files by and
some basic custom ui options. (Python, PyQt, MySQLdb)

The program can be used in two different ways. The first, locally where
all of the information is stored on the harddisk in either the
installation folder or the current working folder. The second, dynamically
where all of the information is stored on a SQL server and can be shared
and modified by other users.

To connect to a server the user will need to enter a server address, a
database name, a username, and a password.

The following server information is my own personal server provided for
testing purposes. In no way will this server be guarenteed to always be
online or available:
Address:         mysql.bhvfx.com
Database Name:   burninghelix123
Username:        exampleuser123
Password:        password

For any additional information, problems, or advice feel free to contact
me using the information that was above.0

'''


from PyQt4 import QtCore, QtGui
import sys
import os
import tempfile
from ui import MainWindow
from ui import MessageDialog
from functions import CreateLogs
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


def runLocally():
    '''Run locally on computer'''
    currentMode = 0
    database = ''
    mainWindow = QtGui.QMainWindow()
    ui = MainWindow.Ui_MainWindow(mainWindow, currentMode, database)
    var = mainWindow.show()
        
def runDynamically():
    '''Run dynamically through SQL server'''
    currentMode = 1
    database = ''
    mainWindow = QtGui.QMainWindow()
    ui = MainWindow.Ui_MainWindow(mainWindow, currentMode, database)
    var = mainWindow.show()
    
def main():
    '''Start Logging and initiate UI'''
    tempDir = tempfile.gettempdir()
    tempLocation = os.path.join(tempDir,'AssetManagerTemp')   
    tempLocationProperties =  os.path.join(tempLocation,'Properties')
    tempLocationImages =  os.path.join(tempLocation,'Images')
    if not os.path.exists(tempLocation):
        os.makedirs(tempLocation)
    if not os.path.exists(tempLocationProperties):
        os.makedirs(tempLocationProperties)
    if not os.path.exists(tempLocationImages):
        os.makedirs(tempLocationImages)
    #logging = CreateLogs.logSetup('AssetManagerLogs', tempLocation)
    app = QtGui.QApplication(sys.argv)
    cm = MessageDialog.Dialog('Select Mode:', 'Select which mode you would like to run the Asset Manager in:\nLocally on one computer or Dynamically through an SQL server', 'Run Locally', 'Run Dynamically')
    MessageDialog.Dialog.msgBox.connect(MessageDialog.Dialog.btnYes, QtCore.SIGNAL('clicked()'), runLocally)
    MessageDialog.Dialog.msgBox.connect(MessageDialog.Dialog.btnNo, QtCore.SIGNAL('clicked()'), runDynamically)
    cm.exec_()
    app.exec_()

if __name__ == '__main__':
    main()