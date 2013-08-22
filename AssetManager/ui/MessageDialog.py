from PyQt4 import QtCore, QtGui

class Dialog(QtGui.QMessageBox):
    '''Dialog Template for two button dialog'''
    msgbox = ''
    btnYes = ''
    btnNo = ''
    
    def __init__(self, title, text, yesText, noText):
        super(Dialog, self).__init__()
        self.initUI(title, text, yesText, noText)
    
    def initUI(self, title, text, yesText, noText):
        '''Setup UI'''
        Dialog.msgBox = self
        Dialog.msgBox.setWindowTitle(title)
        Dialog.msgBox.setText(text)
        Dialog.btnYes = QtGui.QPushButton(yesText)
        Dialog.msgBox.addButton(Dialog.btnYes, QtGui.QMessageBox.YesRole)
        Dialog.btnNo = QtGui.QPushButton(noText)
        Dialog.msgBox.addButton(Dialog.btnNo, QtGui.QMessageBox.NoRole)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
if __name__ == '__main__':
    import sys 
    app2 = QtGui.QApplication(sys.argv)
    input = Dialog('Store Login Info:', 'Would you like to store the login info for the server?', 'Yes', 'No')
    Dialog.msgBox.connect(Dialog.btnYes, QtCore.SIGNAL('clicked()'), lambda : storeLogin(username, address, password, databasename))
    input.exec_()    
    app2.exec_()      
    