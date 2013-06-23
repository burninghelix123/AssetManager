from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class Input_Dialog(QtGui.QDialog):
    '''Dialog for login information'''
    cancel = False
    username = ''
    password = ''
    address = ''
    database = ''
    dialog = ''
    
    def __init__(self):
        super(Input_Dialog, self).__init__()
        self.initUI()
    
    def initUI(self):
        '''Setup UI'''
        self.setObjectName(_fromUtf8("Dialog"))
        self.resize(210, 171)
        Input_Dialog.dialog = self
        Input_Dialog.buttonBox = QtGui.QDialogButtonBox(self)
        Input_Dialog.buttonBox.setGeometry(QtCore.QRect(0, 130, 191, 32))
        Input_Dialog.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        Input_Dialog.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        Input_Dialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        Input_Dialog.usernameLabel = QtGui.QLabel(self)
        Input_Dialog.usernameLabel.setGeometry(QtCore.QRect(5, 10, 61, 16))
        Input_Dialog.usernameLabel.setObjectName(_fromUtf8("label"))
        Input_Dialog.usernameField = QtGui.QLineEdit(self)
        Input_Dialog.usernameField.setGeometry(QtCore.QRect(62, 10, 131, 20))
        Input_Dialog.usernameField.setObjectName(_fromUtf8("lineEdit"))
        Input_Dialog.passwordLabel = QtGui.QLabel(self)
        Input_Dialog.passwordLabel.setGeometry(QtCore.QRect(5, 40, 61, 16))
        Input_Dialog.passwordLabel.setObjectName(_fromUtf8("label_2"))
        Input_Dialog.passwordField = QtGui.QLineEdit(self)
        Input_Dialog.passwordField.setGeometry(QtCore.QRect(62, 40, 131, 20))
        Input_Dialog.passwordField.setText(_fromUtf8(""))
        Input_Dialog.passwordField.setEchoMode(QtGui.QLineEdit.Password)
        Input_Dialog.passwordField.setPlaceholderText(_fromUtf8(""))
        Input_Dialog.passwordField.setObjectName(_fromUtf8("lineEdit_2"))
        Input_Dialog.addressLabel = QtGui.QLabel(self)
        Input_Dialog.addressLabel.setGeometry(QtCore.QRect(5, 70, 61, 16))
        Input_Dialog.addressLabel.setObjectName(_fromUtf8("label_3"))
        Input_Dialog.addressField = QtGui.QLineEdit(self)
        Input_Dialog.addressField.setGeometry(QtCore.QRect(62, 70, 131, 20))
        Input_Dialog.addressField.setObjectName(_fromUtf8("lineEdit_3"))
        Input_Dialog.databaseLabel = QtGui.QLabel(self)
        Input_Dialog.databaseLabel.setGeometry(QtCore.QRect(5, 100, 61, 16))
        Input_Dialog.databaseLabel.setObjectName(_fromUtf8("label_4"))        
        Input_Dialog.databaseField = QtGui.QLineEdit(self)
        Input_Dialog.databaseField.setGeometry(QtCore.QRect(62, 100, 131, 20))
        Input_Dialog.databaseField.setObjectName(_fromUtf8("lineEdit_4"))
        self.setWindowTitle(QtGui.QApplication.translate("self", "Enter Login Info:", None, QtGui.QApplication.UnicodeUTF8))
        Input_Dialog.usernameLabel.setText(QtGui.QApplication.translate("Dialog", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        Input_Dialog.passwordLabel.setText(QtGui.QApplication.translate("Dialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        Input_Dialog.addressLabel.setText(QtGui.QApplication.translate("Dialog", "Address:", None, QtGui.QApplication.UnicodeUTF8))
        Input_Dialog.databaseLabel.setText(QtGui.QApplication.translate("Dialog", "Database:", None, QtGui.QApplication.UnicodeUTF8))
        QtCore.QObject.connect(Input_Dialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accept)
        QtCore.QObject.connect(Input_Dialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
    
    def closeEvent(self, event):
        Input_Dialog.cancel = True
        Input_Dialog.username = 'Invalid'
        Input_Dialog.password = 'Invalid'
        Input_Dialog.address = 'Invalid'
        Input_Dialog.database = 'Invalid'
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to cancel and run in local mode?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
                    
    def accept(self):
        Input_Dialog.username = Input_Dialog.usernameField.text()
        Input_Dialog.password = Input_Dialog.passwordField.text()
        Input_Dialog.address = Input_Dialog.addressField.text()
        Input_Dialog.database = Input_Dialog.databaseField.text()
        Input_Dialog.cancel = False
        Input_Dialog.dialog.done(1)
        
    def reject(self):
        Input_Dialog.cancel = True
        Input_Dialog.username = 'Invalid'
        Input_Dialog.password = 'Invalid'
        Input_Dialog.address = 'Invalid'
        Input_Dialog.database = 'Invalid'
        Input_Dialog.dialog.close()
   
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Input_Dialog()
    ui.exec_()
    sys.exit(app.exec_())