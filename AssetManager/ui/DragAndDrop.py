'''Modual adding drag and drop functionality to Asset Manager'''
from PyQt4 import QtCore, QtGui


class DragAndDrop(QtGui.QListWidget):
    '''Setup Drag and drop events'''
    window = ''
    def __init__(self, windowvar, parent):
        super(DragAndDrop, self).__init__(parent)
        DragAndDrop.window = windowvar
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(100, 100))
        self.itemClicked.connect(self.on_item_clicked)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
      
    def dragEnterEvent(self, event):
        '''Drag event when entering window'''
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            super(DragAndDrop, self).dragEnterEvent(event)
            
    def dragMoveEvent(self, event):
        '''Drag event when moving in window'''
        super(DragAndDrop, self).dragMoveEvent(event)
            
    def dropEvent(self, event):
        '''Drop event in window'''
        if event.mimeData().hasUrls():
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
            event.acceptProposedAction()
        else:
            super(DragAndDrop,self).dropEvent(event)

    def mousePressEvent(self, event):
        '''
        Mouse press event in window
        Enables/Disables menu actions
        '''
        self._mouse_button = event.button()
        super(DragAndDrop, self).mousePressEvent(event)
        propertiesActions = [DragAndDrop.window.actionOpenProjects,
                             DragAndDrop.window.actionOpenWithProjects,
                             DragAndDrop.window.actionPropertiesProjects,
                             DragAndDrop.window.actionPreviewProjects,
                             DragAndDrop.window.actionDeleteProjects,
                             DragAndDrop.window.actionOpenModels,
                             DragAndDrop.window.actionOpenWithModels,
                             DragAndDrop.window.actionPropertiesModels,
                             DragAndDrop.window.actionPreviewModels,
                             DragAndDrop.window.actionDeleteModels,
                             DragAndDrop.window.actionOpenAudio,
                             DragAndDrop.window.actionOpenWithAudio,
                             DragAndDrop.window.actionPropertiesAudio,
                             DragAndDrop.window.actionPreviewAudio,
                             DragAndDrop.window.actionDeleteAudio,
                             DragAndDrop.window.actionOpenVideos,
                             DragAndDrop.window.actionOpenWithVideos,
                             DragAndDrop.window.actionPropertiesVideos,
                             DragAndDrop.window.actionPreviewVideos,
                             DragAndDrop.window.actionDeleteVideos,
                             DragAndDrop.window.actionOpenImages,
                             DragAndDrop.window.actionOpenWithImages,
                             DragAndDrop.window.actionPropertiesImages,
                             DragAndDrop.window.actionPreviewImages,
                             DragAndDrop.window.actionDeleteImages,
                             DragAndDrop.window.actionOpenShaders,
                             DragAndDrop.window.actionOpenWithShaders,
                             DragAndDrop.window.actionPropertiesShaders,
                             DragAndDrop.window.actionPreviewShaders,
                             DragAndDrop.window.actionDeleteShaders,
                             DragAndDrop.window.actionOpenScripts,
                             DragAndDrop.window.actionOpenWithScripts,
                             DragAndDrop.window.actionPropertiesScripts,
                             DragAndDrop.window.actionPreviewScripts,
                             DragAndDrop.window.actionDeleteScripts,
                             DragAndDrop.window.actionOpenSimulations,
                             DragAndDrop.window.actionOpenWithSimulations,
                             DragAndDrop.window.actionPropertiesSimulations,
                             DragAndDrop.window.actionPreviewSimulations,
                             DragAndDrop.window.actionDeleteSimulations]
        items = self.count()
        rangedList =range(items)
        rangedList.reverse()
        numberSelected = 0
        for i in rangedList:
            if self.isItemSelected(self.item(i))==True:
                numberSelected += 1
        for action in propertiesActions:
            if numberSelected == 0:
                action.setEnabled(False)
            if numberSelected == 1:
                action.setEnabled(True)
            if numberSelected > 1:
                action.setEnabled(False)
        for action in range(4, len(propertiesActions), 5):
            if numberSelected > 1:
                propertiesActions[action].setEnabled(True)
        if self._mouse_button == 2:
            for action in propertiesActions:
                if numberSelected == 0:
                    action.setEnabled(False)
            
    def on_item_clicked(self, item):
        '''Future implementation'''
        pass
