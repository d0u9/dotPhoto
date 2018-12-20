from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QFileSystemModel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QDir, QStandardPaths, QSize, pyqtSignal, QFileInfo

import GlobalVar as gVar

class FileTreeView(QTreeView):
    _model = None
    currentPath = None

    pathChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._model = QFileSystemModel()
        self._model.setRootPath(gVar.cwd)
        self._model.setFilter(QDir.AllEntries | QDir.NoDot | QDir.AllDirs)
        self._model.setNameFilterDisables(False)
        self._model.setNameFilters(['*.jpg', '*.png'])

        self.Setup()

    def Setup(self):
        self.setExpandsOnDoubleClick(False)
        self.setIconSize(QSize(12, 12))
        self.setModel(self._model)
        self.setHeaderHidden(True)
        header = self.header()
        for i in range(1, header.count()):
            header.hideSection(i)
        self.setRootIndex(self._model.index(gVar.cwd))

    def mouseDoubleClickEvent(self, event):
        index = self.selectedIndexes()[0]
        finfo = QFileInfo(self._model.filePath(index))
        gVar.cwd = finfo.absoluteFilePath()
        self.PathChangedEvent()
        self.pathChanged.emit()

    def PathChangedEvent(self):
        self._model.setRootPath(gVar.cwd)
        self.setRootIndex(self._model.index(gVar.cwd))
        self.selectionModel().clearSelection()


class FileExlpore(QWidget):
    layout = None
    fileTreeView = None

    pathChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        gVar.fileExplorePathChangeEvent = self.PathChangedEvent
        gVar.fileExplore = self

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.fileTreeView = FileTreeView()
        self.fileTreeView.setMaximumHeight(300)
        self.fileTreeView.pathChanged.connect(lambda : self.pathChanged.emit())

        self.layout.addWidget(self.fileTreeView)
        self.layout.addStretch()

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)

    def PathChangedEvent(self):
        self.fileTreeView.PathChangedEvent()


class BasicOperationPanel(QWidget):
    layout = None
    fileExplore = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(8,8,8,8);

        self.fileExplore = FileExlpore()
        self.layout.addWidget(self.fileExplore)

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
