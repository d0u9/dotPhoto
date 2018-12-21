from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QFileDialog, QPushButton
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QFileInfo, QStandardPaths, QSize, pyqtSignal

from PyQt5.QtWidgets import QLabel

import GlobalVar as gVar

class DirSelectDialog(QFileDialog):
    def __init__(self):
        super().__init__()

class LineEdit(QLineEdit):
    curText = None
    pathChanged = pyqtSignal(str)
    fileFilter = None

    def __init__(self, currentPath):
        super().__init__(currentPath)
        self.curText = currentPath
        self.returnPressed.connect(self.ReturnPressed)
        self.fileFilter = self.defaultFileFilter

        self.setFrame(True)
        self.setMaximumHeight(26)
        self.setMinimumHeight(26)

    def setFileFilter(self, flt):
        self.fileFilter = flt

    def defaultFileFilter(self, finfo):
        if finfo.isDir() and finfo.exists():
            return True
        return False

    def ReturnPressed(self):
        finfo = QFileInfo(self.text())
        if self.fileFilter(finfo):
            self.curText = self.text()
            self.pathChanged.emit(self.curText)
        else:
            self.setStyleSheet('color: red')

    def keyPressEvent(self, event):
        self.setStyleSheet('color: rgb(235,235,235)');
        if event.key() == Qt.Key_Escape:
            self.setText(self.curText)
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self.setText(self.curText)
        self.setStyleSheet('color: rgb(235,235,235)');

    def PathChangedEvent(self, path):
        self.curText = path
        self.setText(path)

class OpenDirBtn(QWidget):
    pathChanged = pyqtSignal(str)
    btn = None
    curPath = None

    def __init__(self, buttonText, baseDir='/'):
        super().__init__()
        self.curPath = baseDir

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.btn = QPushButton(buttonText)
        self.btn.setStyleSheet('width: 50px; height: 22px;')
        self.btn.clicked.connect(self.OpenDialog)

        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)

    def OpenDialog(self):
        options = QFileDialog.Options()
        options = QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        self.curPath = QFileDialog.getExistingDirectory(self, 'Open Folder',
                       self.curPath, options)
        self.pathChanged.emit(self.curPath)


class DirSelectWidget(QWidget):
    lineEdit = None;
    dirSelectDialogBtn = None

    pathChanged = pyqtSignal(str)

    def __init__(self, baseDir='/', btnText='Open'):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.dirSelectDialogBtn = OpenDirBtn(btnText, baseDir)
        self.lineEdit = LineEdit(baseDir)

        self.layout.addWidget(self.lineEdit, 0, Qt.AlignLeft)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.dirSelectDialogBtn, 0, Qt.AlignRight)

        self.dirSelectDialogBtn.pathChanged.connect(self.PathChangedEvent)
        self.lineEdit.pathChanged.connect(self.PathChangedEvent)

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
        self.setStyleSheet('QWidget { height: 36px; }')

    def PathChangedEvent(self, path):
        self.lineEdit.PathChangedEvent(path)
        self.pathChanged.emit(path)

    def SetSize(self, totalW, totalH, btnW, btnH):
        self.setMinimumWidth(totalW)
        self.setMaximumWidth(totalW)
        self.setMinimumHeight(totalH)
        self.setMaximumHeight(totalH)
        self.lineEdit.setMinimumWidth(totalW - btnW - 10)
        self.lineEdit.setMaximumWidth(totalW - btnW - 10)
        self.lineEdit.setMinimumHeight(totalH)
        self.lineEdit.setMaximumHeight(totalH)
        self.dirSelectDialogBtn.btn.setStyleSheet('width: {}px; height: {}px'.format(btnW,btnH))

    def setReadOnly(self, state):
        self.lineEdit.setReadOnly(state)

    def text(self):
        return self.lineEdit.text()


