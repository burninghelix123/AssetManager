'''Main Ui for Asset Manager'''
from PyQt4 import QtCore, QtGui
import base64
import os
from ..functions import OpenAsset
from ..functions import MainFunctions
from ..functions import DatabaseConnect
from ..functions import FileIO
import ConfigParser
import tempfile
from ..functions import OpenAsset
from ..ui import ManageApplications
from ..ui import DragAndDrop
from ..ui import CustomUi
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(QtGui.QMainWindow):
    '''Main application UI'''
    interfaceColor = 1
    copiedItems = []
    window = ''
    currentMode = ''
    database = ''
    mainWindow = ''
    propertiesWindow = ''
    interfaceColor = ''
    cur = ''
    ex = ''
    
    def __init__(self, mainWindow2, currentMode, database):
        super(Ui_MainWindow, self).__init__()
        Ui_MainWindow.database = database
        Ui_MainWindow.currentMode = currentMode
        Ui_MainWindow.mainWindow = mainWindow2
        self.declareUi()
        
    def declareUi(self):
        '''Declare all Ui Variables'''
        self.centralwidget = QtGui.QWidget(Ui_MainWindow.mainWindow)
        Ui_MainWindow.interfaceColor = 1
        Ui_MainWindow.window = self
        if Ui_MainWindow.currentMode == 1:
            Ui_MainWindow.currentMode, Ui_MainWindow.cur, Ui_MainWindow.ex = DatabaseConnect.loginPrep()
        MainWindowFunctions = MainFunctions.MainFunctions(Ui_MainWindow.window,
                                                          Ui_MainWindow.mainWindow,
                                                          Ui_MainWindow.currentMode,
                                                          Ui_MainWindow.database,
                                                          Ui_MainWindow.copiedItems,
                                                          Ui_MainWindow.propertiesWindow,
                                                          Ui_MainWindow.cur,
                                                          Ui_MainWindow.ex)
        self.main_tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.projects_tab, self.models_tab, self.shaders_tab, self.images_tab, self.videos_tab, self.audio_tab, self.scripts_tab, self.simulations_tab = QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget()
        self.projects_scrollArea, self.models_scrollArea, self.shaders_scrollArea, self.images_scrollArea, self.videos_scrollArea, self.audio_scrollArea, self.scripts_scrollArea, self.simulations_scrollArea = QtGui.QScrollArea(self.projects_tab), QtGui.QScrollArea(self.models_tab), QtGui.QScrollArea(self.shaders_tab), QtGui.QScrollArea(self.images_tab), QtGui.QScrollArea(self.videos_tab), QtGui.QScrollArea(self.audio_tab), QtGui.QScrollArea(self.scripts_tab), QtGui.QScrollArea(self.simulations_tab)
        self.scrollAreaWidgetContents_1, self.scrollAreaWidgetContents_2, self.scrollAreaWidgetContents_3, self.scrollAreaWidgetContents_4, self.scrollAreaWidgetContents_5, self.scrollAreaWidgetContents_6, self.scrollAreaWidgetContents_7, self.scrollAreaWidgetContents_8 = QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget(), QtGui.QWidget()
        self.gridLayout_1, self.gridLayout_2, self.gridLayout_3, self.gridLayout_4, self.gridLayout_5, self.gridLayout_6, self.gridLayout_7, self.gridLayout_8 = QtGui.QGridLayout(self.scrollAreaWidgetContents_1), QtGui.QGridLayout(self.scrollAreaWidgetContents_2), QtGui.QGridLayout(self.scrollAreaWidgetContents_3), QtGui.QGridLayout(self.scrollAreaWidgetContents_4), QtGui.QGridLayout(self.scrollAreaWidgetContents_5), QtGui.QGridLayout(self.scrollAreaWidgetContents_6), QtGui.QGridLayout(self.scrollAreaWidgetContents_7), QtGui.QGridLayout(self.scrollAreaWidgetContents_8)
        listViews = ['projects', 'models', 'shaders', 'images', 'videos', 'audio', 'scripts', 'simulations']
        self.projects_listView, self.models_listView, self.shaders_listView, self.images_listView, self.videos_listView, self.audio_listView, self.scripts_listView, self.simulations_listView = DragAndDrop.DragAndDrop(self, Ui_MainWindow.window), DragAndDrop.DragAndDrop(self, Ui_MainWindow.window), DragAndDrop.DragAndDrop(self, Ui_MainWindow.window), DragAndDrop.DragAndDrop(self, Ui_MainWindow.window), DragAndDrop.DragAndDrop(self, Ui_MainWindow.window), DragAndDrop.DragAndDrop(self, Ui_MainWindow.window), DragAndDrop.DragAndDrop(self, Ui_MainWindow.window), DragAndDrop.DragAndDrop(self, Ui_MainWindow.window)
        self.actionOpenProjects = QtGui.QAction("Open", self.projects_listView)        
        self.actionOpenWithProjects = QtGui.QAction("Open With", self.projects_listView)
        self.actionPreviewProjects = QtGui.QAction("Preview", self.projects_listView)
        self.actionPropertiesProjects = QtGui.QAction("Properties", self.projects_listView)
        self.actionImportProjects = QtGui.QAction("Import", self.projects_listView)
        self.actionDeleteProjects = QtGui.QAction("Delete", self.projects_listView)
        self.openWithProjects = QtGui.QMenu(self.projects_listView)
        self.actionOpenWithMayaProjects = QtGui.QAction("Maya", self.openWithProjects)
        self.actionOpenWithHoudiniProjects = QtGui.QAction("Houdini", self.openWithProjects)
        self.actionOpenWithNukeProjects = QtGui.QAction("Nuke", self.openWithProjects)
        self.actionOpenWithPhotoshopProjects = QtGui.QAction("Photoshop", self.openWithProjects)
        self.actionOpenWithTextEditorProjects = QtGui.QAction("Text Editor", self.openWithProjects)
        self.actionOpenWithImageViewerProjects = QtGui.QAction("Image Viewer", self.openWithProjects)
        self.actionOpenWithCustomProjects = QtGui.QAction("Add Custom", self.openWithProjects)
        self.actionOpenModels = QtGui.QAction("Open", self.models_listView)        
        self.actionOpenWithModels = QtGui.QAction("Open With", self.models_listView)
        self.actionPreviewModels = QtGui.QAction("Preview", self.models_listView)
        self.actionPropertiesModels = QtGui.QAction("Properties", self.models_listView)
        self.actionImportModels = QtGui.QAction("Import", self.models_listView)
        self.actionDeleteModels = QtGui.QAction("Delete", self.models_listView)
        self.openWithModels = QtGui.QMenu(self.models_listView)
        self.actionOpenWithMayaModels = QtGui.QAction("Maya", self.openWithModels)
        self.actionOpenWithHoudiniModels = QtGui.QAction("Houdini", self.openWithModels)
        self.actionOpenWithNukeModels = QtGui.QAction("Nuke", self.openWithModels)
        self.actionOpenWithPhotoshopModels = QtGui.QAction("Photoshop", self.openWithModels)
        self.actionOpenWithTextEditorModels = QtGui.QAction("Text Editor", self.openWithModels)
        self.actionOpenWithImageViewerModels = QtGui.QAction("Image Viewer", self.openWithModels)
        self.actionOpenWithCustomModels = QtGui.QAction("Add Custom", self.openWithModels)
        self.actionOpenShaders = QtGui.QAction("Open", self.shaders_listView)        
        self.actionOpenWithShaders = QtGui.QAction("Open With", self.shaders_listView)
        self.actionPreviewShaders = QtGui.QAction("Preview", self.shaders_listView)
        self.actionPropertiesShaders = QtGui.QAction("Properties", self.shaders_listView)
        self.actionImportShaders = QtGui.QAction("Import", self.shaders_listView)
        self.actionDeleteShaders = QtGui.QAction("Delete", self.shaders_listView)
        self.openWithShaders = QtGui.QMenu(self.shaders_listView)
        self.actionOpenWithMayaShaders = QtGui.QAction("Maya", self.openWithShaders)
        self.actionOpenWithHoudiniShaders = QtGui.QAction("Houdini", self.openWithShaders)
        self.actionOpenWithNukeShaders = QtGui.QAction("Nuke", self.openWithShaders)
        self.actionOpenWithPhotoshopShaders = QtGui.QAction("Photoshop", self.openWithShaders)
        self.actionOpenWithTextEditorShaders = QtGui.QAction("Text Editor", self.openWithShaders)
        self.actionOpenWithImageViewerShaders = QtGui.QAction("Image Viewer", self.openWithShaders)
        self.actionOpenWithCustomShaders = QtGui.QAction("Add Custom", self.openWithShaders)
        self.actionOpenImages = QtGui.QAction("Open", self.images_listView)        
        self.actionOpenWithImages = QtGui.QAction("Open With", self.images_listView)
        self.actionPreviewImages = QtGui.QAction("Preview", self.images_listView)
        self.actionPropertiesImages = QtGui.QAction("Properties", self.images_listView)
        self.actionImportImages = QtGui.QAction("Import", self.images_listView)
        self.actionDeleteImages = QtGui.QAction("Delete", self.images_listView)
        self.openWithImages = QtGui.QMenu(self.images_listView)
        self.actionOpenWithMayaImages = QtGui.QAction("Maya", self.openWithImages)
        self.actionOpenWithHoudiniImages = QtGui.QAction("Houdini", self.openWithImages)
        self.actionOpenWithNukeImages = QtGui.QAction("Nuke", self.openWithImages)
        self.actionOpenWithPhotoshopImages = QtGui.QAction("Photoshop", self.openWithImages)
        self.actionOpenWithTextEditorImages = QtGui.QAction("Text Editor", self.openWithImages)
        self.actionOpenWithImageViewerImages = QtGui.QAction("Image Viewer", self.openWithImages)
        self.actionOpenWithCustomImages = QtGui.QAction("Add Custom", self.openWithImages)
        self.actionOpenVideos = QtGui.QAction("Open", self.videos_listView)        
        self.actionOpenWithVideos = QtGui.QAction("Open With", self.videos_listView)
        self.actionPreviewVideos = QtGui.QAction("Preview", self.videos_listView)
        self.actionPropertiesVideos = QtGui.QAction("Properties", self.videos_listView)
        self.actionImportVideos = QtGui.QAction("Import", self.videos_listView)
        self.actionDeleteVideos = QtGui.QAction("Delete", self.videos_listView)
        self.openWithVideos = QtGui.QMenu(self.videos_listView)
        self.actionOpenWithMayaVideos = QtGui.QAction("Maya", self.openWithVideos)
        self.actionOpenWithHoudiniVideos = QtGui.QAction("Houdini", self.openWithVideos)
        self.actionOpenWithNukeVideos = QtGui.QAction("Nuke", self.openWithVideos)
        self.actionOpenWithPhotoshopVideos = QtGui.QAction("Photoshop", self.openWithVideos)
        self.actionOpenWithTextEditorVideos = QtGui.QAction("Text Editor", self.openWithVideos)
        self.actionOpenWithImageViewerVideos = QtGui.QAction("Image Viewer", self.openWithVideos)
        self.actionOpenWithCustomVideos = QtGui.QAction("Add Custom", self.openWithVideos)   
        self.actionOpenAudio = QtGui.QAction("Open", self.audio_listView)        
        self.actionOpenWithAudio = QtGui.QAction("Open With", self.audio_listView)
        self.actionPreviewAudio = QtGui.QAction("Preview", self.audio_listView)
        self.actionPropertiesAudio = QtGui.QAction("Properties", self.audio_listView)
        self.actionImportAudio = QtGui.QAction("Import", self.audio_listView)
        self.actionDeleteAudio = QtGui.QAction("Delete", self.audio_listView)
        self.openWithAudio = QtGui.QMenu(self.audio_listView)
        self.actionOpenWithMayaAudio = QtGui.QAction("Maya", self.openWithAudio)
        self.actionOpenWithHoudiniAudio = QtGui.QAction("Houdini", self.openWithAudio)
        self.actionOpenWithNukeAudio = QtGui.QAction("Nuke", self.openWithAudio)
        self.actionOpenWithPhotoshopAudio = QtGui.QAction("Photoshop", self.openWithAudio)
        self.actionOpenWithTextEditorAudio = QtGui.QAction("Text Editor", self.openWithAudio)
        self.actionOpenWithImageViewerAudio = QtGui.QAction("Image Viewer", self.openWithAudio)
        self.actionOpenWithCustomAudio = QtGui.QAction("Add Custom", self.openWithAudio)
        self.actionOpenScripts = QtGui.QAction("Open", self.scripts_listView)        
        self.actionOpenWithScripts = QtGui.QAction("Open With", self.scripts_listView)
        self.actionPreviewScripts = QtGui.QAction("Preview", self.scripts_listView)
        self.actionPropertiesScripts = QtGui.QAction("Properties", self.scripts_listView)
        self.actionImportScripts = QtGui.QAction("Import", self.scripts_listView)
        self.actionDeleteScripts = QtGui.QAction("Delete", self.scripts_listView)
        self.openWithScripts = QtGui.QMenu(self.scripts_listView)
        self.actionOpenWithMayaScripts = QtGui.QAction("Maya", self.openWithScripts)
        self.actionOpenWithHoudiniScripts = QtGui.QAction("Houdini", self.openWithScripts)
        self.actionOpenWithNukeScripts = QtGui.QAction("Nuke", self.openWithScripts)
        self.actionOpenWithPhotoshopScripts = QtGui.QAction("Photoshop", self.openWithScripts)
        self.actionOpenWithTextEditorScripts = QtGui.QAction("Text Editor", self.openWithScripts)
        self.actionOpenWithImageViewerScripts = QtGui.QAction("Image Viewer", self.openWithScripts)
        self.actionOpenWithCustomScripts = QtGui.QAction("Add Custom", self.openWithScripts)
        self.actionOpenSimulations = QtGui.QAction("Open", self.simulations_listView)        
        self.actionOpenWithSimulations = QtGui.QAction("Open With", self.simulations_listView)
        self.actionPreviewSimulations = QtGui.QAction("Preview", self.simulations_listView)
        self.actionPropertiesSimulations = QtGui.QAction("Properties", self.simulations_listView)
        self.actionImportSimulations = QtGui.QAction("Import", self.simulations_listView)
        self.actionDeleteSimulations = QtGui.QAction("Delete", self.simulations_listView)
        self.openWithSimulations = QtGui.QMenu(self.simulations_listView)
        self.actionOpenWithMayaSimulations = QtGui.QAction("Maya", self.openWithSimulations)
        self.actionOpenWithHoudiniSimulations = QtGui.QAction("Houdini", self.openWithSimulations)
        self.actionOpenWithNukeSimulations = QtGui.QAction("Nuke", self.openWithSimulations)
        self.actionOpenWithPhotoshopSimulations = QtGui.QAction("Photoshop", self.openWithSimulations)
        self.actionOpenWithTextEditorSimulations = QtGui.QAction("Text Editor", self.openWithSimulations)
        self.actionOpenWithImageViewerSimulations = QtGui.QAction("Image Viewer", self.openWithSimulations)
        self.actionOpenWithCustomSimulations = QtGui.QAction("Add Custom", self.openWithSimulations)
        self.setupUi(listViews, MainWindowFunctions)
        
    def setupUi(self, listViews, MainWindowFunctions):
        '''Setup Ui attributes'''
        Ui_MainWindow.mainWindow.setObjectName(_fromUtf8("MainWindow"))
        Ui_MainWindow.mainWindow.resize(783, 613)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.main_tabWidget.setGeometry(QtCore.QRect(210, 5, 570, 565))
        self.main_tabWidget.setObjectName(_fromUtf8("main_tabWidget"))
        self.main_tabWidget.setMovable(True)
        for index, listVar in enumerate(listViews):
            tab = getattr(self, listVar + '_tab')
            tab.setObjectName(_fromUtf8(listVar + '_tab'))
            scrollArea = getattr(self, listVar + '_scrollArea')
            scrollArea.setGeometry(QtCore.QRect(0, 0, 570, 545))
            scrollArea.setMinimumSize(QtCore.QSize(550, 520))
            scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            scrollArea.setWidgetResizable(True)
            scrollArea.setObjectName(_fromUtf8(listVar + '_scrollArea'))
            scrollAreaWidget = getattr(self, ('scrollAreaWidgetContents' + '_' + str(index + 1)))
            scrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 529, 516))
            scrollAreaWidget.setObjectName(_fromUtf8('scrollAreaWidgetContents' + '_' + str(index + 1)))
            gridLayout = getattr(self, ('gridLayout' + '_' + str(index + 1)))
            gridLayout.setObjectName(_fromUtf8('gridLayout' + '_' + str(index + 1)))
            view = getattr(self, listVar + '_listView')
            view.setObjectName(_fromUtf8(listVar))
            gridLayout.addWidget(view, 2, 2, 1, 1)
            scrollArea.setWidget(scrollAreaWidget)
            self.main_tabWidget.addTab(tab, _fromUtf8(""))
            view.setSortingEnabled(True)
        self.window.connect(self.projects_listView, QtCore.SIGNAL('dropped'),
                     (lambda links: MainWindowFunctions.itemDropped(links, self.projects_listView)))
        self.window.connect(self.models_listView, QtCore.SIGNAL('dropped'),
                     (lambda links: MainWindowFunctions.itemDropped(links, self.models_listView)))
        self.window.connect(self.shaders_listView, QtCore.SIGNAL('dropped'),
                     (lambda links: MainWindowFunctions.itemDropped(links, self.shaders_listView)))
        self.window.connect(self.images_listView, QtCore.SIGNAL('dropped'),
                     (lambda links: MainWindowFunctions.itemDropped(links, self.images_listView)))
        self.window.connect(self.videos_listView, QtCore.SIGNAL('dropped'),
                     (lambda links: MainWindowFunctions.itemDropped(links, self.videos_listView)))
        self.window.connect(self.audio_listView, QtCore.SIGNAL('dropped'),
                     (lambda links: MainWindowFunctions.itemDropped(links, self.audio_listView)))
        self.window.connect(self.scripts_listView, QtCore.SIGNAL('dropped'),
                     (lambda links: MainWindowFunctions.itemDropped(links, self.scripts_listView)))
        self.window.connect(self.simulations_listView, QtCore.SIGNAL('dropped'),
                     (lambda links: MainWindowFunctions.itemDropped(links, self.simulations_listView)))
        customPrograms = []
        customActions = []
        customName = []
        for index, listVars in enumerate(listViews):
            view = getattr(self, listVars + '_listView')
            listVars = listVars.title()
            actions = [(getattr(Ui_MainWindow.window, 'actionOpen' + listVars)), (getattr(Ui_MainWindow.window, 'actionOpenWith' + listVars)),
                       (getattr(Ui_MainWindow.window, 'actionPreview' + listVars)), (getattr(Ui_MainWindow.window, 'actionProperties' + listVars)),
                       (getattr(Ui_MainWindow.window, 'actionImport' + listVars)), (getattr(Ui_MainWindow.window, 'actionDelete' + listVars)),
                       (getattr(Ui_MainWindow.window, 'openWith' + listVars)), (getattr(Ui_MainWindow.window, 'actionOpenWithMaya' + listVars)),
                       (getattr(Ui_MainWindow.window, 'actionOpenWithHoudini' + listVars)), (getattr(Ui_MainWindow.window, 'actionOpenWithNuke' + listVars)),
                       (getattr(Ui_MainWindow.window, 'actionOpenWithPhotoshop' + listVars)), (getattr(Ui_MainWindow.window, 'actionOpenWithTextEditor' + listVars)),
                       (getattr(Ui_MainWindow.window, 'actionOpenWithImageViewer' + listVars)), (getattr(Ui_MainWindow.window, 'actionOpenWithCustom' + listVars))]
            self.contextActions(actions, self.main_tabWidget, view, MainWindowFunctions, customPrograms, customActions, customName, index)
        self.manageApplications()
        self.setupUiElements(MainWindowFunctions)

    def manageApplications(self):
        tempDir = tempfile.gettempdir()
        tempLocation = os.path.join(tempDir,'AssetManagerTemp')
        tempLocation = os.path.join(tempLocation,'ManageApplications.ini')
        if os.path.exists(tempLocation):
            config = ConfigParser.ConfigParser()
            config.read(tempLocation)
            programs = config.items('Programs')
            menus = ['openWithProjects', 'openWithModels', 'openWithShaders', 'openWithImages', 'openWithVideos', 'openWithAudio', 'openWithScripts', 'openWithSimulations']
            for menu in menus:
                actions = getattr(Ui_MainWindow.window, menu)
                actions = actions.actions()
                for program in programs:
                    for action in actions:
                        if program[0].title() == action.text():
                            state = program[1].title()
                            if state == 'True':
                                action.setVisible(True)
                            if state == 'False':
                                action.setVisible(False)
  
    def setupUiElements(self, MainWindowFunctions):
        '''Setup Ui elements attributes for sidebar'''
        self.settings_frame = QtGui.QFrame(self.centralwidget)
        self.settings_frame.setGeometry(QtCore.QRect(0, 0, 201, 200))
        self.settings_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.settings_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.settings_frame.setObjectName(_fromUtf8("settings_frame"))
        self.settings_label = QtGui.QLabel(self.settings_frame)
        self.settings_label.setGeometry(QtCore.QRect(65, 5, 145, 13))
        self.settings_label.setObjectName(_fromUtf8("settings_label"))
        self.address_label = QtGui.QLabel(self.settings_frame)
        self.address_label.setGeometry(QtCore.QRect(10, 20, 46, 13))
        self.address_label.setObjectName(_fromUtf8("address_label"))
        self.username_label = QtGui.QLabel(self.settings_frame)
        self.username_label.setGeometry(QtCore.QRect(10, 45, 60, 13))
        self.username_label.setObjectName(_fromUtf8("username_label"))
        self.password_label = QtGui.QLabel(self.settings_frame)
        self.password_label.setGeometry(QtCore.QRect(10, 70, 60, 13))
        self.password_label.setObjectName(_fromUtf8("password_label"))
        self.database_label = QtGui.QLabel(self.settings_frame)
        self.database_label.setGeometry(QtCore.QRect(10, 95, 60, 13))
        self.database_label.setObjectName(_fromUtf8("database_label"))        
        self.address_lineEdit = QtGui.QLineEdit(self.settings_frame)
        self.address_lineEdit.setGeometry(QtCore.QRect(80, 20, 113, 20))
        self.address_lineEdit.setObjectName(_fromUtf8("address_lineEdit"))
        self.username_lineEdit = QtGui.QLineEdit(self.settings_frame)
        self.username_lineEdit.setGeometry(QtCore.QRect(80, 45, 113, 20))
        self.username_lineEdit.setObjectName(_fromUtf8("username_lineEdit"))
        self.password_lineEdit = QtGui.QLineEdit(self.settings_frame)
        self.password_lineEdit.setGeometry(QtCore.QRect(80, 70, 113, 20))
        self.password_lineEdit.setObjectName(_fromUtf8("password_lineEdit"))
        self.password_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.database_lineEdit = QtGui.QLineEdit(self.settings_frame)
        self.database_lineEdit.setGeometry(QtCore.QRect(80, 95, 113, 20))
        self.database_lineEdit.setObjectName(_fromUtf8("database_lineEdit"))
        self.connect_pushButton = QtGui.QPushButton(self.settings_frame)
        self.connect_pushButton.setGeometry(QtCore.QRect(10, 120, 180, 23))
        self.connect_pushButton.setObjectName(_fromUtf8("connect_pushButton"))
        self.connect(self.connect_pushButton, QtCore.SIGNAL("clicked()"), MainWindowFunctions.connectToDB)  
        self.refresh_pushButton = QtGui.QPushButton(self.settings_frame)
        self.refresh_pushButton.setGeometry(QtCore.QRect(10, 147, 180, 23))
        self.refresh_pushButton.setObjectName(_fromUtf8("refresh_pushButton"))
        self.connect(self.refresh_pushButton, QtCore.SIGNAL("clicked()"), MainWindowFunctions.refreshItems)      
        self.projects_frame = QtGui.QFrame(self.centralwidget)
        self.projects_frame.setGeometry(QtCore.QRect(0, 170, 201, 420))
        self.projects_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.projects_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.projects_frame.setObjectName(_fromUtf8("projects_frame"))
        self.projectloc_label = QtGui.QLabel(self.projects_frame)
        self.projectloc_label.setGeometry(QtCore.QRect(65, 30, 91, 20))
        self.projectloc_label.setObjectName(_fromUtf8("projectloc_label"))
        self.projectloc_scrollArea = QtGui.QScrollArea(self.projects_frame)
        self.projectloc_scrollArea.setGeometry(QtCore.QRect(10, 50, 150, 170))
        self.projectloc_scrollArea.setMinimumSize(QtCore.QSize(180, 290))
        self.projectloc_scrollArea.setMaximumSize(QtCore.QSize(180, 290))
        self.projectloc_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.projectloc_scrollArea.setWidgetResizable(True)
        self.projectloc_scrollArea.setObjectName(_fromUtf8("projectloc_scrollArea"))
        self.setFolder_pushButton = QtGui.QPushButton(self.projects_frame)
        self.setFolder_pushButton.setGeometry(QtCore.QRect(10, 345, 180, 23))
        self.setFolder_pushButton.setObjectName(_fromUtf8("setFolder_pushButton"))
        self.addFile_pushButton = QtGui.QPushButton(self.projects_frame)
        self.addFile_pushButton.setGeometry(QtCore.QRect(10, 370, 90, 23))
        self.addFile_pushButton.setObjectName(_fromUtf8("addFile_pushButton"))
        self.removeFile_pushButton = QtGui.QPushButton(self.projects_frame)
        self.removeFile_pushButton.setGeometry(QtCore.QRect(100, 370, 90, 23))
        self.removeFile_pushButton.setObjectName(_fromUtf8("removeFile_pushButton"))
        self.connect(self.setFolder_pushButton, QtCore.SIGNAL("clicked()"), MainWindowFunctions.setFolder)  
        self.connect(self.addFile_pushButton, QtCore.SIGNAL("clicked()"), MainWindowFunctions.addFile)  
        self.setupUiMain(MainWindowFunctions)

    def setupUiMain(self, MainWindowFunctions):
        '''Setup Ui elements attributes for main window''' 
        uiColors = CustomUi.UiColors() 
        self.scrollAreaWidgetContents_10 = QtGui.QWidget()
        self.scrollAreaWidgetContents_10.setGeometry(QtCore.QRect(0, 0, 159, 218))
        self.scrollAreaWidgetContents_10.setObjectName(_fromUtf8("scrollAreaWidgetContents_10"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_10)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.listWidget_2 = QtGui.QListWidget(self.scrollAreaWidgetContents_10)
        self.listWidget_2.setMinimumSize(QtCore.QSize(140, 200))
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))
        self.connect(self.removeFile_pushButton, QtCore.SIGNAL("clicked()"), lambda : MainWindowFunctions.deleteItem(self.listWidget_2))
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.projectloc_scrollArea.setWidget(self.scrollAreaWidgetContents_10)
        Ui_MainWindow.mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 778, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuDisplay = QtGui.QMenu(self.menubar)
        self.menuDisplay.setObjectName(_fromUtf8("menuDisplay"))
        self.menuSort = QtGui.QMenu(self.menubar)
        self.menuSort.setObjectName(_fromUtf8("menuSort"))
        Ui_MainWindow.mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Ui_MainWindow.mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Ui_MainWindow.mainWindow.setStatusBar(self.statusbar)
        self.openAssetFileAction = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.openAssetFileAction.setObjectName(_fromUtf8("OpenAsset"))
        self.saveAssetFileAction = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.saveAssetFileAction.setObjectName(_fromUtf8("SaveAsset"))
        self.importAssetFileAction = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.importAssetFileAction.setObjectName(_fromUtf8("ImportAsset"))
        self.copyAction = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.copyAction.setObjectName(_fromUtf8("Copy"))
        self.pasteAction = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.pasteAction.setObjectName(_fromUtf8("Paste"))
        self.deleteAction = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.deleteAction.setObjectName(_fromUtf8("Delete"))        
        self.programPreferences = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.programPreferences.setObjectName(_fromUtf8("programPreferences"))
        self.interfaceColor1Action = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.interfaceColor1Action.setObjectName(_fromUtf8("color1"))
        self.interfaceColor2Action = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.interfaceColor2Action.setObjectName(_fromUtf8("color2"))
        self.interfaceColorCustomAction = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.interfaceColorCustomAction.setObjectName(_fromUtf8("colorCustom"))
        self.sortAscending = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.sortAscending.setObjectName(_fromUtf8("sortAscending"))
        self.sortDescending = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.sortDescending.setObjectName(_fromUtf8("sortDescending"))
        self.actionExit = QtGui.QAction(Ui_MainWindow.mainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.openAssetFileAction)
        self.menuFile.addAction(self.saveAssetFileAction)
        self.menuFile.addAction(self.importAssetFileAction)
        self.menuEdit.addAction(self.copyAction)
        self.menuEdit.addAction(self.pasteAction)
        self.menuEdit.addAction(self.deleteAction)
        self.menuDisplay.addAction(self.interfaceColor1Action)
        self.menuDisplay.addAction(self.interfaceColor2Action)
        self.menuDisplay.addAction(self.interfaceColorCustomAction)
        self.menuDisplay.addAction(self.programPreferences)
        self.menuSort.addAction(self.sortAscending)
        self.menuSort.addAction(self.sortDescending)
        self.interfaceColor1Action.triggered.connect(lambda : uiColors.interfaceColor1(Ui_MainWindow.window, Ui_MainWindow.mainWindow))
        self.interfaceColor2Action.triggered.connect(lambda : uiColors.interfaceColor2(Ui_MainWindow.window, Ui_MainWindow.mainWindow))
        self.interfaceColorCustomAction.triggered.connect(lambda : uiColors.interfaceColorCustom(Ui_MainWindow.window, Ui_MainWindow.mainWindow))
        self.openAssetFileAction.triggered.connect(lambda : MainWindowFunctions.openAssetFile(0))
        self.saveAssetFileAction.triggered.connect(MainWindowFunctions.saveAssetFile)
        self.importAssetFileAction.triggered.connect(lambda : MainWindowFunctions.importAssetFile(0))
        self.sortAscending.triggered.connect(lambda : MainWindowFunctions.sortAscending())
        self.sortDescending.triggered.connect(lambda : MainWindowFunctions.sortDescending())
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuDisplay.menuAction())
        self.menubar.addAction(self.menuSort.menuAction())
        self.main_tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Ui_MainWindow.mainWindow)
        self.listWidget_2.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.actionOpenAssetFile = QtGui.QAction("Open", self.listWidget_2)        
        self.listWidget_2.addAction(self.actionOpenAssetFile)
        self.actionOpenAssetFile.setStatusTip('Open asset file')
        self.actionOpenAssetFile.triggered.connect(lambda : MainWindowFunctions.openAssetFile(1))
        self.actionImportAssetFile = QtGui.QAction("Import", self.listWidget_2)        
        self.listWidget_2.addAction(self.actionImportAssetFile)
        self.actionImportAssetFile.setStatusTip('Import asset file')
        self.actionImportAssetFile.triggered.connect(lambda : MainWindowFunctions.importAssetFile(1))
        self.actionRemoveAssetFile = QtGui.QAction("Remove", self.listWidget_2)        
        self.listWidget_2.addAction(self.actionRemoveAssetFile)
        self.actionRemoveAssetFile.setStatusTip('Remove asset file')
        self.actionRemoveAssetFile.triggered.connect(lambda : MainWindowFunctions.deleteItem(self.listWidget_2))
        self.copyAction.triggered.connect(MainWindowFunctions.copyItem)
        self.pasteAction.triggered.connect(MainWindowFunctions.pasteItem)
        manageApplications = ManageApplications.ManageApplications(Ui_MainWindow.window)
        self.programPreferences.triggered.connect(lambda : ManageApplications.main(manageApplications))
        self.deleteAction.triggered.connect(lambda : MainWindowFunctions.deleteItem(self.main_tabWidget))
        self.listWidget_2.setDragDropMode(QtGui.QAbstractItemView.InternalMove);
        self.populateLoginInfo()
        uiColors.interfaceColor1(Ui_MainWindow.window, Ui_MainWindow.mainWindow)
        self.nameUiElements(MainWindowFunctions)
        
    def populateLoginInfo(self):
        '''Fills in login info if stored locally'''
        tempDir = tempfile.gettempdir()
        tempLocation = os.path.join(tempDir,'AssetManagerTemp')
        tempLocation = os.path.join(tempLocation,'LoginInfo.txt')
        if os.path.exists(tempLocation):
            data = FileIO.read(tempLocation)
            address = data['address']
            username = data['username']
            password = data['password']
            password = base64.b64decode(password)
            databasename = data['databasename']
            self.address_lineEdit.setText(address)
            self.username_lineEdit.setText(username)
            self.password_lineEdit.setText(password)
            self.database_lineEdit.setText(databasename)
            
    def contextActions(self, actions, tabWidget,listVar, MainWindowFunctions, customPrograms, customActions, customName, index):
        '''Setup actions for menus'''
        listVar.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        listVar.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        listVar.doubleClicked.connect(lambda : OpenAsset.openFile(self, listVar))
        actions[6].addAction(actions[7])
        actions[6].addAction(actions[8])
        actions[6].addAction(actions[9])
        actions[6].addAction(actions[10])
        actions[6].addAction(actions[11])
        actions[6].addAction(actions[12])
        actions[6].addAction(actions[13])
        actions[6].addSeparator()
        actions[1].setMenu(actions[6])
        actions[7].setStatusTip('Open file with Maya')
        actions[8].setStatusTip('Open file with Houdini')
        actions[9].setStatusTip('Open file with Nuke')
        actions[10].setStatusTip('Open file with Photoshop')
        actions[11].setStatusTip('Open file with Text Editor')
        actions[12].setStatusTip('Open file with Image Viewer')
        actions[13].setStatusTip('Add custom program to open with')
        windowObject = Ui_MainWindow.window
        actions[7].triggered.connect(lambda : OpenAsset.openFileWithApp(self, 'bin\maya.exe', listVar, 1, 1, ['Maya'], ['Maya 2014'], ['Maya 2013'], ['Maya 2012']))
        actions[8].triggered.connect(lambda : OpenAsset.openFileWithApp(self, 'bin\houdini.exe', listVar, 1, 1, ['Houdini'], ['Houdini 12'], ['Houdini 11'], ['Houdini 10']))
        actions[9].triggered.connect(lambda : OpenAsset.openFileWithApp(self, '', listVar, 1, 1, ['Nuke'], ['Nuke 7'], ['Nuke 6'], ['Nuke 5']))
        actions[10].triggered.connect(lambda : OpenAsset.openFileWithApp(self, 'Photoshop.exe', listVar, 1, 2, ['Photoshop'], ['Photoshop CS6'], ['Photoshop CS5'], ['Photoshop CS4']))
        actions[11].triggered.connect(lambda : OpenAsset.openFileWithTextEditor(self, listVar))
        actions[12].triggered.connect(lambda : OpenAsset.openFileWithImageViewer(self, listVar))
        actions[13].triggered.connect(lambda : OpenAsset.openFileWithCustom(self, listVar, customPrograms, customActions, customName, windowObject, None, 0, index))
        listVar.addAction(actions[0])
        listVar.addAction(actions[1])
        #listVar.addAction(actions[2]) //preview //Future Implementation
        listVar.addAction(actions[3])
        listVar.addAction(actions[4])
        listVar.addAction(actions[5])
        actions[0].setStatusTip('Open selected file with default program')
        actions[1].setStatusTip('Open selected file with chosen program')
        #actions[2].setStatusTip('Preview file if possible') //preview //Future Implementation
        actions[3].setStatusTip('View and edit properties of file')
        actions[4].setStatusTip('Import file into asset manager')
        actions[5].setStatusTip('Remove selected file/s from asset manager')
        actions[5].setShortcut('Delete')
        actions[0].triggered.connect(lambda : OpenAsset.openFile(self, listVar))
        actions[2].triggered.connect(lambda : MainWindowFunctions.previewFile(listVar))
        actions[3].triggered.connect(lambda : MainWindowFunctions.fileProperties(listVar))
        actions[5].triggered.connect(lambda : MainWindowFunctions.deleteItem(tabWidget))
        actions[4].triggered.connect(lambda : MainWindowFunctions.importEntry("Projects", listVar))
        actions[0].setEnabled(False)
        actions[1].setEnabled(False)
        #actions[2].setEnabled(False) //preview //Future Implementation
        actions[3].setEnabled(False)
        actions[5].setEnabled(False)
        tempDir = tempfile.gettempdir()
        tempLocation = os.path.join(tempDir,'AssetManagerTemp')
        tempLocation = os.path.join(tempLocation,'CustomMenuItems.ini')
        if os.path.exists(tempLocation):
            data = FileIO.read(tempLocation)
            customPrograms = data['programs']
            customActions = data['names']
            customName = customActions
            customPrograms = customPrograms.split('\n')
            customActions = customActions.split('\n')
            customName = customName.split('\n')
            actionSet = []
            itemName = []
            programSet = []
            url = []
            windowObject = Ui_MainWindow.window
            for number, item in enumerate(customPrograms):
                OpenAsset.openFileWithCustom(self, listVar, programSet, actionSet, itemName, windowObject, item, 1, index)
        
    def nameUiElements(self, MainWindowFunctions):
        '''Rename UI Elements'''
        Ui_MainWindow.mainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Asset Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.projects_tab), QtGui.QApplication.translate("MainWindow", "Projects", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.models_tab), QtGui.QApplication.translate("MainWindow", "Models", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.shaders_tab), QtGui.QApplication.translate("MainWindow", "Shaders", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.images_tab), QtGui.QApplication.translate("MainWindow", "Images", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.videos_tab), QtGui.QApplication.translate("MainWindow", "Videos", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.audio_tab), QtGui.QApplication.translate("MainWindow", "Audio", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.scripts_tab), QtGui.QApplication.translate("MainWindow", "Scripts", None, QtGui.QApplication.UnicodeUTF8))
        self.main_tabWidget.setTabText(self.main_tabWidget.indexOf(self.simulations_tab), QtGui.QApplication.translate("MainWindow", "Simulations", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_label.setText(QtGui.QApplication.translate("MainWindow", "Server Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.address_label.setText(QtGui.QApplication.translate("MainWindow", "Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.username_label.setText(QtGui.QApplication.translate("MainWindow", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.password_label.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.database_label.setText(QtGui.QApplication.translate("MainWindow", "Database:", None, QtGui.QApplication.UnicodeUTF8))
        self.connect_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Connect/Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Refresh Items", None, QtGui.QApplication.UnicodeUTF8))
        self.setFolder_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Add Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.addFile_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Add File", None, QtGui.QApplication.UnicodeUTF8))
        self.removeFile_pushButton.setText(QtGui.QApplication.translate("MainWindow", "Remove File", None, QtGui.QApplication.UnicodeUTF8))
        self.projectloc_label.setText(QtGui.QApplication.translate("MainWindow", "Project Files", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDisplay.setTitle(QtGui.QApplication.translate("MainWindow", "Display", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSort.setTitle(QtGui.QApplication.translate("MainWindow", "Sort", None, QtGui.QApplication.UnicodeUTF8))
        self.copyAction.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.pasteAction.setText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.programPreferences.setText(QtGui.QApplication.translate("MainWindow", "Manage Applications", None, QtGui.QApplication.UnicodeUTF8))        
        self.sortAscending.setText(QtGui.QApplication.translate("MainWindow", "Sort By Ascending", None, QtGui.QApplication.UnicodeUTF8))
        self.sortDescending.setText(QtGui.QApplication.translate("MainWindow", "Sort By Descending", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteAction.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.openAssetFileAction.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.saveAssetFileAction.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.importAssetFileAction.setText(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.interfaceColor1Action.setText(QtGui.QApplication.translate("MainWindow", "Interface Color Dark", None, QtGui.QApplication.UnicodeUTF8))
        self.interfaceColor2Action.setText(QtGui.QApplication.translate("MainWindow", "Interface Color Light", None, QtGui.QApplication.UnicodeUTF8))
        self.interfaceColorCustomAction.setText(QtGui.QApplication.translate("MainWindow", "Custom Interface Color", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
