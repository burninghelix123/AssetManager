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
me using the information that was above.

'''


from PyQt4 import QtCore, QtGui
import sys
import Logging
import MainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class changeMode(QtGui.QMessageBox):
    '''Switch between running locally and dynamically'''
    currentMode = 0
    mainWindow = ''
    database = ''
    def __init__(self):
        super(changeMode, self).__init__()
        self.initUI()
        
    def initUI(self):
        '''Setup UI'''
        msgBox = self
        msgBox.setWindowTitle('Manager Mode:')
        msgBox.setText('Would you like to run this locally or dynamically through a datbase?')
        btnYes = QtGui.QPushButton('Locally')
        msgBox.addButton(btnYes, QtGui.QMessageBox.YesRole)
        btnNo = QtGui.QPushButton('Dynamically')
        msgBox.addButton(btnNo, QtGui.QMessageBox.NoRole)
        msgBox.show()
        self.connect(btnYes, QtCore.SIGNAL('clicked()'), self.runLocally)
        self.connect(btnNo, QtCore.SIGNAL('clicked()'), self.runDynamically)
 
    def runLocally(self):
        '''Run locally on computer'''
        changeMode.currentMode = 0
        changeMode.mainWindow = QtGui.QMainWindow()
        self.ui = MainWindow.Ui_MainWindow(changeMode.mainWindow, changeMode.currentMode, changeMode.database)
        self.var = changeMode.mainWindow.show()
            
    def runDynamically(self):
        '''Run dynamically through SQL server'''
        changeMode.currentMode = 1
        changeMode.mainWindow = QtGui.QMainWindow()
        self.ui = MainWindow.Ui_MainWindow(changeMode.mainWindow, changeMode.currentMode, changeMode.database)
        self.var = changeMode.mainWindow.show()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    '''Start Logging and initiate UI'''
    logging = Logging.Logging()
    logging.logSetup()
    app = QtGui.QApplication(sys.argv)
    cm = changeMode()
    app.exec_()
    
if __name__ == "__main__":
    main()
