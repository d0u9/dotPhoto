from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QFileSystemModel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QDir, QStandardPaths, QSize, pyqtSignal

class LineEdit(QLineEdit):
    currentPath = None

    canceled = pyqtSignal()

    def __init__(self, currentPath):
        super().__init__(currentPath)
        self.currentPath = currentPath

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.setText(self.currentPath)
        else:
            super().keyPressEvent(event)


class FilePathBox(QWidget):
    upperBtn = None
    layout = None
    filePathInput = None
    currentPath = None

    pathChanged = pyqtSignal(str)

    def __init__(self, currentPath='/'):
        super().__init__()
        self.currentPath = currentPath

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.setContentsMargins(0,8,0,8);

        self.upperBtn = QPushButton('<-')
        self.upperBtn.setStyleSheet('width: 30px; height: 24px;')
        self.upperBtn.clicked.connect(self.PrevBtnPressed)
        self.layout.addWidget(self.upperBtn)

        self.filePathInput = LineEdit(self.currentPath)
        self.filePathInput.setStyleSheet('margin: 0 0 0 10px')
        self.filePathInput.returnPressed.connect(self.Goto)
        self.layout.addWidget(self.filePathInput)

        self.setLayout(self.layout)

    def Goto(self):
        newPath = self.filePathInput.text()
        if newPath == self.currentPath or not QDir(newPath).exists():
            return
        self.currentPath = newPath
        self.pathChanged.emit(newPath)

    def PrevBtnPressed(self):
        d = QDir(self.currentPath)
        if not d.cdUp():
            return
        self.filePathInput.setText(d.absolutePath())
        self.Goto()

class FileExlpore(QWidget):
    layout = None
    currentPath = None
    fileTreeView = None
    _fileModel = None

    def __init__(self):
        super().__init__()

        self.currentPath = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        self._fileModel = QFileSystemModel()
        self._fileModel.setRootPath(self.currentPath)
        self._fileModel.setNameFilterDisables(False)
        self._fileModel.setNameFilters(['*.jpg', '*.png'])

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.filePathBox = FilePathBox(self.currentPath)
        self.filePathBox.pathChanged.connect(self.SetNewPath)
        self.layout.addWidget(self.filePathBox)

        self.fileTreeView = QTreeView()
        self.fileTreeView.setIconSize(QSize(12, 12))
        self.fileTreeView.setModel(self._fileModel)
        self.fileTreeView.setHeaderHidden(True)
        header = self.fileTreeView.header()
        for i in range(1, header.count()):
            header.hideSection(i)
        self.fileTreeView.setRootIndex(self._fileModel.index(self.currentPath))
        self.layout.addWidget(self.fileTreeView)

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)

    def SetNewPath(self, newPath):
        print(newPath)
        self._fileModel.setRootPath(newPath)
        self.fileTreeView.setRootIndex(self._fileModel.index(newPath))


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
