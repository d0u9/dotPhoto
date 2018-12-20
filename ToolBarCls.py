from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QFileDialog, QPushButton
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QFileInfo, QStandardPaths, QSize, pyqtSignal

from PyQt5.QtWidgets import QLabel

import GlobalVar as gVar

class DirSelectDialog(QFileDialog):
    def __init__(self):
        super().__init__()

class LineEdit(QLineEdit):
    pathChanged = pyqtSignal(str)

    def __init__(self, currentPath):
        super().__init__(currentPath)
        self.returnPressed.connect(self.ReturnPressed)
        gVar.workDirPathInputBoxPathChangeEvent = self.PathChangedEvent

        self.setFrame(True)
        self.setMaximumHeight(26)
        self.setMinimumHeight(26)

    def ReturnPressed(self):
        finfo = QFileInfo(self.text())
        if finfo.isDir() and finfo.exists():
            gVar.cwd = finfo.absoluteFilePath()
            self.pathChanged.emit(self.text())
        else:
            self.setStyleSheet('color: red')

    def keyPressEvent(self, event):
        self.setStyleSheet('color: rgb(235,235,235)');
        if event.key() == Qt.Key_Escape:
            self.setText(gVar.cwd)
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self.setText(gVar.cwd)
        self.setStyleSheet('color: rgb(235,235,235)');

    def PathChangedEvent(self):
        self.setText(gVar.cwd)

class OpenDirBtn(QWidget):
    pathChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        btn = QPushButton('Open')
        btn.setStyleSheet('width: 50px; height: 22px;')
        btn.clicked.connect(self.OpenDialog)

        self.layout.addWidget(btn)

        self.setLayout(self.layout)

    def OpenDialog(self):
        options = QFileDialog.Options()
        options = QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        gVar.cwd = QFileDialog.getExistingDirectory(self, 'Open Folder',
                gVar.cwd, options)
        self.pathChanged.emit()


class WorkDirPathBox(QWidget):
    inputBox = None;
    dirSelectDialogBtn = None

    pathChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        gVar.workDirPathBox = self

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.dirSelectDialogBtn = OpenDirBtn()

        self.inputBox = LineEdit(gVar.cwd)

        self.layout.addSpacing(10)
        self.layout.addWidget(self.inputBox, 0, Qt.AlignHCenter)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.dirSelectDialogBtn, 0, Qt.AlignHCenter)
        self.layout.addSpacing(10)

        self.dirSelectDialogBtn.pathChanged.connect(self.PathChangedEvent)
        self.dirSelectDialogBtn.pathChanged.connect(lambda : self.pathChanged.emit())
        self.inputBox.pathChanged.connect(self.PathChangedEvent)
        self.inputBox.pathChanged.connect(lambda : self.pathChanged.emit())

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
        self.setStyleSheet('QWidget { height: 36px; }')
        self.setMinimumWidth(400)
        self.setMaximumWidth(400)

    def PathChangedEvent(self):
        self.inputBox.PathChangedEvent()




class ToolBar(QWidget):
    layout = None
    pathInput = None
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.workDirPathBox = WorkDirPathBox()

        self.layout.addStretch()
        self.layout.addWidget(self.workDirPathBox)
        self.layout.addStretch()

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
        self.setMinimumHeight(36)
        self.setMaximumHeight(36)
        p = QPalette()
        p.setColor(QPalette.Background, QColor.fromRgb(42,42,42))
        self.setAutoFillBackground(True)
        self.setPalette(p)
        self.setStyleSheet("""
            ToolBar {
                color: rgb(220,220,220);
            }
            QLineEdit {
                background-color: rgb(58,58,58);
                width: 400px;
                color: rgb(235,235,235);
            }
        """)



