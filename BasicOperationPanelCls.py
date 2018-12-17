from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QFileSystemModel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QDir, QStandardPaths

class FilePathBox(QWidget):
    prevBtn = None
    goToBtn = None
    layout = None
    filePathInput = None
    currentPath = None

    def __init__(self, currentPath='/'):
        super().__init__()
        self.currentPath = currentPath

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.setContentsMargins(0,8,0,8);

        self.prevBtn = QPushButton('<-')
        self.prevBtn.setStyleSheet('width: 30px; height: 24px;')
        self.layout.addWidget(self.prevBtn)

        self.filePathInput = QLineEdit(self.currentPath)
        self.filePathInput.setStyleSheet('margin: 0 10px 0 10px')
        self.layout.addWidget(self.filePathInput)

        self.goToBtn = QPushButton('->')
        self.goToBtn.setStyleSheet('width: 30px; height: 24px;')
        self.layout.addWidget(self.goToBtn)


        self.setLayout(self.layout)

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

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.filePathBox = FilePathBox(self.currentPath)
        self.layout.addWidget(self.filePathBox)

        self.fileTreeView = QTreeView()
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
