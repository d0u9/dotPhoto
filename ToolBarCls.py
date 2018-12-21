from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QFileDialog, QPushButton
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QFileInfo, QStandardPaths, QSize, pyqtSignal

from PyQt5.QtWidgets import QLabel

import GlobalVar as gVar
from DirSelectWidgetCls import DirSelectWidget

class ToolBar(QWidget):
    layout = None
    pathInput = None
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.workDirPathBox = DirSelectWidget(gVar.cwd)
        self.workDirPathBox.setMinimumWidth(400)
        self.workDirPathBox.setMaximumWidth(400)
        self.workDirPathBox.pathChanged.connect(self.SetGvarCwd)
        gVar.workDirPathBox = self.workDirPathBox
        gVar.workDirPathInputBoxPathChangeEvent = self.workDirPathBox.PathChangedEvent

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

    def SetGvarCwd(self, path):
        gVar.cwd = path


