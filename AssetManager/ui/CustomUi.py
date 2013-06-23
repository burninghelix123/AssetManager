'''Module to Setup Ui options for Asset Manager''' 
from PyQt4 import QtCore, QtGui


class UiColors(QtGui.QDialog):
    '''Set different Ui Colors'''
    window1 = ''
    window2 = ''
    col = QtGui.QColor(0, 0, 0)
    col1 = QtGui.QColor(0, 0, 0) 
    col2 = QtGui.QColor(0, 0, 0) 
    col3 = QtGui.QColor(0, 0, 0)
    col4 = QtGui.QColor(0, 0, 0)
    interfaceColor = ''
    
    def interfaceColor1(self, window1, window2):
        '''Set interface color to dark'''
        UiColors.window1 = window1
        UiColors.window2 = window2
        UiColors.window1.projects_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        UiColors.window1.models_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        UiColors.window1.shaders_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        UiColors.window1.images_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        UiColors.window1.videos_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        UiColors.window1.audio_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        UiColors.window1.scripts_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        UiColors.window1.simulations_listView.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {border: 2px solid darkgrey; background-color: rgb(200,200,200); color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        UiColors.window2.setStyleSheet('background-color: darkgrey')
        UiColors.window1.address_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        UiColors.window1.username_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        UiColors.window1.password_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        UiColors.window1.database_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: rgb(200,200,200); color:black}')
        UiColors.window1.connect_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        UiColors.window1.setFolder_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        UiColors.window1.addFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        UiColors.window1.removeFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        UiColors.window1.listWidget_2.setStyleSheet('background-color: rgb(200,200,200)')
        UiColors.window1.statusbar.setStyleSheet('background-color: rgb(200,200,200)')
        UiColors.window1.menubar.setStyleSheet('QMenuBar {background-color: rgb(200,200,200)} QMenuBar::item {background-color: transparent;} QMenuBar::item:selected {background-color: rgb(240,240,240);} QMenuBar::item:inactive{color: black}')
        UiColors.window1.menuFile.setStyleSheet('QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;}')
        UiColors.window1.menuEdit.setStyleSheet('QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;}')
        UiColors.window1.menuDisplay.setStyleSheet('QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;}')
        UiColors.window1.menuSort.setStyleSheet('QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;}')
        UiColors.window1.listWidget_2.setStyleSheet('QListView {background-color: rgb(200,200,200); border: 0px} QMenu {background-color: rgb(200,200,200); border: 2px solid darkgrey; color: black} QMenu::item:selected {background-color: rgb(245,245,245); color: black;} QListWidget:item:selected:active { background: rgb(240,240,240); color:black} QListWidget:item:hover { background: rgb(240,240,240); color:black}')
        UiColors.window1.main_tabWidget.setStyleSheet('QTabWidget::pane {border: 1px solid grey;} QTabWidget {border: 1px solid grey; padding: 0px;} QTabBar::tab {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D8D8D8, stop: 0.4 #C5C5C5, stop: 0.5 #B6B6B6, stop: 1.0 #A2A2A2); border: 2px solid #C4C4C3; border-bottom-color: #C2C7CB;  border-top-left-radius: 4px; border-top-right-radius: 4px; min-width: 21ex; padding: 2px;} QTabBar::tab:selected, QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}')
        UiColors.window1.simulations_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.scripts_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.audio_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.videos_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.images_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.shaders_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.models_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.projects_scrollArea.setStyleSheet('border: 0px;')
        UiColors.interfaceColor = 1
        ColorPicker.icolor = 0
        return (UiColors.interfaceColor)
        
    def interfaceColor2(self, window1, window2):
        '''Set interface color to light'''
        UiColors.window1 = window1
        UiColors.window2 = window2
        UiColors.window1.projects_listView.setStyleSheet('QListView {border: 0px} QMenu {border: 2px solid darkgrey; color: black} QMenu::item:selected {color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {color:black} QListWidget:item:hover {color:black}')
        UiColors.window1.models_listView.setStyleSheet('QListView {border: 0px} QMenu {border: 2px solid darkgrey; color: black} QMenu::item:selected {color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {color:black} QListWidget:item:hover {color:black}')
        UiColors.window1.shaders_listView.setStyleSheet('QListView {border: 0px} QMenu {border: 2px solid darkgrey; color: black} QMenu::item:selected {color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {color:black} QListWidget:item:hover {color:black}')
        UiColors.window1.images_listView.setStyleSheet('QListView {border: 0px} QMenu {border: 2px solid darkgrey; color: black} QMenu::item:selected {color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {color:black} QListWidget:item:hover {color:black}')
        UiColors.window1.videos_listView.setStyleSheet('QListView {border: 0px} QMenu {border: 2px solid darkgrey; color: black} QMenu::item:selected {color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {color:black} QListWidget:item:hover {color:black}')
        UiColors.window1.audio_listView.setStyleSheet('QListView {border: 0px} QMenu {border: 2px solid darkgrey; color: black} QMenu::item:selected {color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {color:black} QListWidget:item:hover {color:black}')
        UiColors.window1.scripts_listView.setStyleSheet('QListView {border: 0px} QMenu {border: 2px solid darkgrey; color: black} QMenu::item:selected {color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {color:black} QListWidget:item:hover {color:black}')
        UiColors.window1.simulations_listView.setStyleSheet('QListView {border: 0px} QMenu {border: 2px solid darkgrey; color: black} QMenu::item:selected {color: black;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active {color:black} QListWidget:item:hover {color:black}')
        UiColors.window2.setStyleSheet('')
        UiColors.window1.address_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; ; color:black}')
        UiColors.window1.username_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; ; color:black}')
        UiColors.window1.password_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; ; color:black}')
        UiColors.window1.database_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; ; color:black}')
        UiColors.window1.connect_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        UiColors.window1.setFolder_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        UiColors.window1.addFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        UiColors.window1.removeFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}')
        UiColors.window1.listWidget_2.setStyleSheet('')
        UiColors.window1.statusbar.setStyleSheet('')
        UiColors.window1.menubar.setStyleSheet('QMenuBar {background-color: rgb(240,240,240)} QMenuBar::item {background-color: transparent;} QMenuBar::item:selected {background-color: rgb(200,200,200);} QMenuBar::item:inactive{color: black}')
        UiColors.window1.menuFile.setStyleSheet('QMenu {background-color: rgb(240,240,240); border: 2px solid lightgrey; color: black} QMenu::item:selected {background-color: rgb(200,200,200); color: black;}')
        UiColors.window1.menuEdit.setStyleSheet('QMenu {background-color: rgb(240,240,240); border: 2px solid lightgrey; color: black} QMenu::item:selected {background-color: rgb(200,200,200); color: black;}')
        UiColors.window1.menuDisplay.setStyleSheet('QMenu {background-color: rgb(240,240,240); border: 2px solid lightgrey; color: black} QMenu::item:selected {background-color: rgb(200,200,200); color: black;}')
        UiColors.window1.menuSort.setStyleSheet('QMenu {background-color: rgb(240,240,240); border: 2px solid lightgrey; color: black} QMenu::item:selected {background-color: rgb(200,200,200); color: black;}')
        UiColors.window1.listWidget_2.setStyleSheet('QListView {border: 0px} QMenu {border: 2px solid darkgrey; color: black} QMenu::item:selected { color: black;} QListWidget:item:selected:active {color:black} QListWidget:item:hover {color:black}')
        UiColors.window1.main_tabWidget.setStyleSheet('QTabWidget::pane {border: 1px solid grey;} QTabWidget {border: 1px solid grey; padding: 0px;} QTabBar::tab {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #FFFFFF, stop: 0.4 #EEEEEE, stop: 0.5 #DDDDDD, stop: 1.0 #CCCCCC); border: 2px solid #C4C4C3; border-bottom-color: #C2C7CB; border-top-left-radius: 4px; border-top-right-radius: 4px; min-width: 21ex; padding: 2px;} QTabBar::tab:selected, QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}')
        UiColors.window1.simulations_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.scripts_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.audio_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.videos_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.images_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.shaders_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.models_scrollArea.setStyleSheet('border: 0px;')
        UiColors.window1.projects_scrollArea.setStyleSheet('border: 0px;')
        UiColors.interfaceColor = 2
        ColorPicker.icolor = 0
        return (UiColors.interfaceColor)
    
    def interfaceColorCustom(self, window1, window2):
        '''Set custom interface color'''
        ui = ColorPicker(window1, window2)
        ui.exec_()
        if ColorPicker.icolor == 3:
            UiColors.interfaceColor = 3
            return (UiColors.interfaceColor,ColorPicker.col,ColorPicker.col1,ColorPicker.col2,ColorPicker.col3,ColorPicker.col4)

class ColorPicker(QtGui.QDialog):
    '''Color picker for custom interface color'''
    col = QtGui.QColor(0, 0, 0)
    col1 = QtGui.QColor(0, 0, 0) 
    col2 = QtGui.QColor(0, 0, 0) 
    col3 = QtGui.QColor(0, 0, 0)
    col4 = QtGui.QColor(0, 0, 0)
    icolor = 0
    
    def __init__(self, window1, window2):
        super(ColorPicker, self).__init__()        
        self.initUI()
        ColorPicker.window1 = window1
        ColorPicker.window2 = window2
        
    def initUI(self):
        '''Setup UI for custom colors'''
        self.bgbtn = QtGui.QPushButton('Background Color', self)
        self.bgbtn.setGeometry(QtCore.QRect(20, 20, 100, 23))
        self.fgbtn = QtGui.QPushButton('Foreground Color', self)
        self.fgbtn.setGeometry(QtCore.QRect(20, 44, 100, 23))
        self.d1btn = QtGui.QPushButton('Detail Color 1', self)
        self.d1btn.setGeometry(QtCore.QRect(20, 68, 100, 23))
        self.d2btn = QtGui.QPushButton('Detail Color 2', self)
        self.d2btn.setGeometry(QtCore.QRect(20, 92, 100, 23))
        self.tbtn = QtGui.QPushButton('Text Color', self)
        self.tbtn.setGeometry(QtCore.QRect(20, 116, 100, 23))
        self.bgbtn.clicked.connect(self.showDialog)
        self.fgbtn.clicked.connect(self.showDialog1)
        self.d1btn.clicked.connect(self.showDialog2)
        self.d2btn.clicked.connect(self.showDialog3)
        self.tbtn.clicked.connect(self.showDialog4)
        self.okbtn = QtGui.QPushButton('Apply', self)
        self.okbtn.setGeometry(QtCore.QRect(20, 150, 100, 23))
        self.cancelbtn = QtGui.QPushButton('Close', self)
        self.cancelbtn.setGeometry(QtCore.QRect(130, 150, 100, 23))
        self.okbtn.clicked.connect(lambda : self.ok(ColorPicker.col,
                                                    ColorPicker.col1,
                                                    ColorPicker.col2))
        self.cancelbtn.clicked.connect(self.cancel)
        self.frm = QtGui.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col.name())
        self.frm.setGeometry(130, 22, 100, 20)            
        self.frm1 = QtGui.QFrame(self)
        self.frm1.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col1.name())
        self.frm1.setGeometry(130, 44, 100, 20)
        self.frm2 = QtGui.QFrame(self)
        self.frm2.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col2.name())
        self.frm2.setGeometry(130, 66, 100, 20)
        self.frm3 = QtGui.QFrame(self)
        self.frm3.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col3.name())
        self.frm3.setGeometry(130, 88, 100, 20)
        self.frm4 = QtGui.QFrame(self)
        self.frm4.setStyleSheet("QWidget { background-color: %s }" 
            % ColorPicker.col4.name())
        self.frm4.setGeometry(130, 110, 100, 20) 
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')

    def ok(self, col, col1, col2):
        '''Sets colors'''
        ColorPicker.window1.projects_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.models_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.shaders_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.images_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.videos_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.audio_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.scripts_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.simulations_listView.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {border: 2px solid darkgrey; background-color: %(color1)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QMenu::item:disabled {color: rgb(130, 130, 130)} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window2.setStyleSheet('background-color: %(color)s;  color: %(color4)s' % {'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.address_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.username_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.password_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.database_lineEdit.setStyleSheet('QLineEdit {border: 1px solid gray; border-radius: 5px; padding: 0 3px; background-color: %(color1)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.connect_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 6px; padding: 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}'  % {'color4': ColorPicker.col4.name()})
        ColorPicker.window1.setFolder_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}'  % {'color4': ColorPicker.col4.name()})
        ColorPicker.window1.addFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}'  % {'color4': ColorPicker.col4.name()})
        ColorPicker.window1.removeFile_pushButton.setStyleSheet('QPushButton {border: 1px solid gray; border-radius: 20px; padding: 0 6px; qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); color: %(color4)s;}'  % {'color4': ColorPicker.col4.name()})
        ColorPicker.window1.listWidget_2.setStyleSheet('background-color: %(color1)s; color: %(color4)s' % {'color1': ColorPicker.col.name(),'color4': ColorPicker.col.name()})
        ColorPicker.window1.statusbar.setStyleSheet('background-color: %(color1)s; color: %(color4)s' % {'color1': ColorPicker.col.name(),'color4': ColorPicker.col.name()})
        ColorPicker.window1.menubar.setStyleSheet('QMenuBar {background-color: %(color1)s} QMenuBar::item {background-color: transparent;} QMenuBar::item:selected {background-color: %(color3)s;} QMenuBar::item:inactive{color: %(color4)s}' % {'color1': ColorPicker.col1.name(),'color3': ColorPicker.col3.name(), 'color4': ColorPicker.col4.name()})
        ColorPicker.window1.menuFile.setStyleSheet('QMenu {background-color: %(color1)s; border: 2px solid %(color)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.menuEdit.setStyleSheet('QMenu {background-color: %(color1)s; border: 2px solid %(color)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.menuDisplay.setStyleSheet('QMenu {background-color: %(color1)s; border: 2px solid %(color)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.menuSort.setStyleSheet('QMenu {background-color: %(color1)s; border: 2px solid %(color)s; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color': ColorPicker.col.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.listWidget_2.setStyleSheet('QListView {background-color: %(color1)s; border: 0px} QMenu {background-color: %(color1)s; border: 2px solid darkgrey; color: %(color4)s} QMenu::item:selected {background-color: %(color2)s; color: %(color4)s;} QListWidget:item:selected:active { background: %(color3)s; color:%(color4)s} QListWidget:item:hover { background: %(color3)s; color:%(color4)s}' % {'color1': ColorPicker.col1.name(),'color2': ColorPicker.col2.name(),'color3': ColorPicker.col3.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.main_tabWidget.setStyleSheet('QTabWidget::pane {border: 1px solid grey;} QTabWidget {border: 1px solid grey; padding: 0px;} QTabBar::tab {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 %(color1)s, stop: 0.4 #C5C5C5, stop: 0.5 #B6B6B6, stop: 1.0 %(color)s); border: 2px solid #C4C4C3; border-bottom-color: #C2C7CB;  border-top-left-radius: 4px; border-top-right-radius: 4px; min-width: 21ex; padding: 2px;} QTabBar::tab:selected, QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa); color: %(color4)s;}' % {'color': ColorPicker.col.name(),'color1': ColorPicker.col1.name(),'color4': ColorPicker.col4.name()})
        ColorPicker.window1.simulations_scrollArea.setStyleSheet('border: 0px;')
        ColorPicker.window1.scripts_scrollArea.setStyleSheet('border: 0px;')
        ColorPicker.window1.audio_scrollArea.setStyleSheet('border: 0px;')
        ColorPicker.window1.videos_scrollArea.setStyleSheet('border: 0px;')
        ColorPicker.window1.images_scrollArea.setStyleSheet('border: 0px;')
        ColorPicker.window1.shaders_scrollArea.setStyleSheet('border: 0px;')
        ColorPicker.window1.models_scrollArea.setStyleSheet('border: 0px;')
        ColorPicker.window1.projects_scrollArea.setStyleSheet('border: 0px;')
        UiColors.interfaceColor = 3
        ColorPicker.icolor = 3
        return (UiColors.interfaceColor)
        
    def cancel(self):
        self.close()
        
    def showDialog(self):
        '''Dialog for first color'''
        ColorPicker.col = QtGui.QColorDialog.getColor()
        if ColorPicker.col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col.name())
        
    def showDialog1(self):
        '''Dialog for second color'''
        ColorPicker.col1 = QtGui.QColorDialog.getColor()
        if ColorPicker.col1.isValid():
            self.frm1.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col1.name())
        
    def showDialog2(self):
        '''Dialog for third color'''
        ColorPicker.col2 = QtGui.QColorDialog.getColor()
        if ColorPicker.col2.isValid():
            self.frm2.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col2.name())
            
    def showDialog3(self):
        '''Dialog for fourth color'''
        ColorPicker.col3 = QtGui.QColorDialog.getColor()
        if ColorPicker.col3.isValid():
            self.frm3.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col3.name())
            
    def showDialog4(self):
        '''Dialog for fith color'''
        ColorPicker.col4 = QtGui.QColorDialog.getColor()
        if ColorPicker.col4.isValid():
            self.frm4.setStyleSheet("QWidget { background-color: %s }"
                % ColorPicker.col4.name())
