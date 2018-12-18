from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QFileSystemModel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QDir, QStandardPaths, QSize, pyqtSignal

class LineEdit(QLineEdit):
    canceled = pyqtSignal()
    commited = pyqtSignal(str)

    def __init__(self, currentPath):
        super().__init__(currentPath)
        self.returnPressed.connect(self.ReturnPressed)

    def ReturnPressed(self):
        self.commited.emit(self.text())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.canceled.emit()
        else:
            super().keyPressEvent(event)


class FileTreeView(QTreeView):
    _model = None
    currentPath = None

    pathChanged = pyqtSignal(str)

    def __init__(self, currentPath):
        super().__init__()
        self.currentPath = currentPath

        self._model = QFileSystemModel()
        self._model.setRootPath(self.currentPath)
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
        self.setRootIndex(self._model.index(self.currentPath))

    def mouseDoubleClickEvent(self, event):
        index = self.selectedIndexes()[0]
        self.setRootIndex(index)
        self.pathChanged.emit(self._model.filePath(index))

    def SetPath(self, path):
        self.currentPath = path
        self._model.setRootPath(self.currentPath)
        self.setRootIndex(self._model.index(self.currentPath))
        self.selectionModel().clearSelection()


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
        self.layout.addWidget(self.upperBtn)

        self.filePathInput = LineEdit(self.currentPath)
        self.filePathInput.setStyleSheet('margin: 0 0 0 10px')
        self.layout.addWidget(self.filePathInput)

        self.setLayout(self.layout)

        self.filePathInput.commited.connect(self.Goto)
        self.filePathInput.canceled.connect(lambda : self.filePathInput.setText(self.currentPath))
        self.upperBtn.clicked.connect(self.PrevBtnPressed)

    def Goto(self, newPath):
        if newPath == self.currentPath or not QDir(newPath).exists():
            self.filePathInput.setText(self.currentPath)
        else:
            self.filePathInput.setText(newPath)
            self.currentPath = newPath
            self.pathChanged.emit(newPath)

    def PrevBtnPressed(self):
        d = QDir(self.currentPath)
        if d.cdUp():
            self.Goto(d.absolutePath())

    def SetPath(self, path):
        self.currentPath = path
        self.filePathInput.setText(path)

class FileExlpore(QWidget):
    layout = None
    currentPath = None
    fileTreeView = None

    def __init__(self):
        super().__init__()
        self.currentPath = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.filePathBox = FilePathBox(self.currentPath)
        self.layout.addWidget(self.filePathBox)

        self.fileTreeView = FileTreeView(self.currentPath)
        self.layout.addWidget(self.fileTreeView)

        self.filePathBox.pathChanged.connect(self.fileTreeView.SetPath)
        self.fileTreeView.pathChanged.connect(self.filePathBox.SetPath)

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
