from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QGroupBox
from PyQt5.QtWidgets import QFileSystemModel, QCheckBox, QLabel, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt, QDir, QStandardPaths, QSize, pyqtSignal, QFileInfo, QFile, QDirIterator, QModelIndex, QRegExp
from PyQt5.QtGui import QRegExpValidator, QIntValidator

import GlobalVar as gVar
from DirSelectWidgetCls import DirSelectWidget

class RawFormatLineEdit(QLineEdit):
    suffixChanged = pyqtSignal(str)
    #  regx = '.*'
    regx = '^\s*([A-Z0-9]+,\s*)+([A-Z0-9]+,?)\s*$'
    validator = None

    def __init__(self):
        super().__init__(gVar.defaultRawSuffix)

        self.validator = QRegExpValidator(QRegExp(self.regx, Qt.CaseInsensitive))
        self.setValidator(self.validator)

        self.returnPressed.connect(self.RawFormatUpdatedEvent)

    def focusOutEvent(self, event):
        self.suffixChanged.emit(self.text())

    def RawFormatUpdatedEvent(self):
        self.suffixChanged.emit(self.text())


class RawPathSetBox(QGroupBox):
    layout = None
    checkBox = None
    suffixBox = None
    rawPathBox = None

    def __init__(self):
        super().__init__('Raw file location')

        layout0 = QHBoxLayout()
        layout0.setSpacing(0)
        layout0.setContentsMargins(0,0,0,0);
        layout1 = QHBoxLayout()
        layout1.setSpacing(0)
        layout1.setContentsMargins(0,0,0,0);
        layout2 = QHBoxLayout()
        layout2.setSpacing(0)
        layout2.setContentsMargins(0,0,0,0);

        self.checkBox = QCheckBox('Raw file in same directory', self)
        self.checkBox.setCheckState(Qt.Checked)
        layout0.addWidget(self.checkBox)

        label1 = QLabel('Suffix:')
        input1 = RawFormatLineEdit()
        input1.setMinimumWidth(225)
        gVar.rawFileSuffix = input1

        label2 = QLabel('Path:')
        input2 = DirSelectWidget(gVar.cwd, '...')
        gVar.rawFileDir = input2
        input2.setReadOnly(True)
        input2.SetSize(225, 22, 22, 22)

        self.suffixBox = input1
        self.rawPathBox = input2

        self.checkBox.stateChanged.connect(self.CheckBoxChanged)

        layout1.addWidget(label1)
        layout1.addWidget(input1, 0, Qt.AlignRight | Qt.AlignVCenter)
        layout2.addWidget(label2)
        layout2.addWidget(input2, 0, Qt.AlignRight | Qt.AlignVCenter)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(5,10,5,10);

        self.layout.addSpacing(5)
        self.layout.addLayout(layout0)
        self.layout.addSpacing(5)
        self.layout.addLayout(layout1)
        self.layout.addSpacing(5)
        self.layout.addLayout(layout2)

        self.setLayout(self.layout)
        self.setContentsMargins(0,0,0,0)

    def CheckBoxChanged(self, state):
        if state == Qt.Unchecked: self.rawPathBox.setReadOnly(False)
        else:
            self.rawPathBox.setReadOnly(True)


class BasicFileSystemModel(QFileSystemModel):
    def __init__(self):
        super().__init__()


class FileTreeView(QTreeView):
    _model = None
    currentPath = None
    baseDir = None

    pathChanged = pyqtSignal(str)
    fileSelected = pyqtSignal(str)

    def __init__(self, baseDir='/'):
        super().__init__()
        self.baseDir = baseDir

        self._model = BasicFileSystemModel()
        self._model.setRootPath(baseDir)
        self._model.setFilter(QDir.AllEntries | QDir.NoDot | QDir.AllDirs)
        self._model.setNameFilterDisables(False)
        self._model.setNameFilters(['*.jpg', '*.png'])

        self.clicked.connect(self.ClickedEvent)

        self.Setup()

    def Setup(self):
        self.setExpandsOnDoubleClick(False)
        self.setIconSize(QSize(12, 12))
        self.setModel(self._model)
        self.setHeaderHidden(True)
        header = self.header()
        for i in range(1, header.count()):
            header.hideSection(i)
        self.setRootIndex(self._model.index(self.baseDir))

    def mouseDoubleClickEvent(self, event):
        index = self.selectedIndexes()[0]
        finfo = QFileInfo(self._model.filePath(index))
        if finfo.isDir():
            self.baseDir = finfo.absoluteFilePath()
            self.PathChangedEvent(self.baseDir)
            self.pathChanged.emit(self.baseDir)

    def ClickedEvent(self, event):
        validSuffix = ['jpg', 'png']
        index = self.selectedIndexes()[0]
        finfo = QFileInfo(self._model.filePath(index))

        if finfo.suffix().lower() not in validSuffix:
            return

        if finfo.isFile() and finfo.isReadable():
            self.fileSelected.emit(finfo.absoluteFilePath())

    def PathChangedEvent(self, path):
        self.baseDir = path
        self._model.setRootPath(path)
        self.setRootIndex(self._model.index(path))
        self.selectionModel().clearSelection()


class FileExlpore(QGroupBox):
    layout = None
    fileTreeView = None

    pathChanged = pyqtSignal(str)
    fileSelected = pyqtSignal(str)

    def __init__(self, baseDir='/'):
        super().__init__('File')
        gVar.fileExplorePathChangeEvent = self.PathChangedEvent
        gVar.fileExplore = self

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(5,10,5,10);

        self.fileTreeView = FileTreeView(baseDir)

        self.fileTreeView.pathChanged.connect(lambda x: self.pathChanged.emit(x))
        self.fileTreeView.fileSelected.connect(lambda x: self.fileSelected.emit(x))

        self.layout.addWidget(self.fileTreeView)

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
        self.setMaximumHeight(300)

    def PathChangedEvent(self, path):
        gVar.cwd = path
        self.fileTreeView.PathChangedEvent(path)


class BasicOperationPanel(QWidget):
    layout = None
    fileExplore = None
    rawPathSetBox = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(8,8,8,8);

        self.fileExplore = FileExlpore(gVar.cwd)
        self.rawPathSetBox = RawPathSetBox()

        lineWidget = QWidget()
        lineWidget.setFixedHeight(1)
        lineWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lineWidget.setStyleSheet('background: rgb(96,96,96)')
        lineWidget.setContentsMargins(0,0,0,0)

        self.layout.addWidget(self.fileExplore)
        self.layout.addSpacing(6)
        self.layout.addWidget(lineWidget)
        self.layout.addWidget(self.rawPathSetBox)
        self.layout.addStretch()

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
