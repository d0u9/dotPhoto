from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QGroupBox, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QPalette, QColor

import exifread
import GlobalVar as gVar

class ExifItem(QWidget):
    layout = None
    def __init__(self, key, val, index=0):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        keyBox = QLabel(key)
        keyBox.setWordWrap(True)
        keyBox.setMaximumWidth(100)
        keyBox.setMinimumWidth(100)
        keyBox.setStyleSheet('border-right: 1px solid rgb(64,64,64);')
        valBox = QLabel(val)
        valBox.setWordWrap(True)

        self.layout.addWidget(keyBox)
        self.layout.addWidget(valBox)

        self.setLayout(self.layout)

class ExifTable(QWidget):
    def __init__(self, dataDict={}):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        index = 0
        item = None
        for key, val in dataDict.items():
            item = ExifItem(key, val)
            if index % 2 != 0:
                item.setStyleSheet('background: rgb(49,49,49);')
            self.layout.addWidget(item)
        #  styleSheet = item.styleSheet() + 'border-bottom: 1px solid rgb(64,64,64);'
        #  item.setStyleSheet(styleSheet)

        self.setLayout(self.layout)


class ExifBox(QGroupBox):
    layout = None
    exifData = {}

    def __init__(self):
        super().__init__('Exif Info')
        gVar.exifBoxImageSelectedEvent = self.ImageSelectedEvent

        self.setStyleSheet("""
            QLabel {
                background: rgb(38,38,38);
                border-top: 1px solid rgb(64,64,64);
                padding: 1px 3px 1px 3px;
                font-size: 11px;
            }
            QGroupBox {
                padding-top: 25px;
            }
            QWidget {
                background: rgb(38,38,38);
            }
        """)

        self.table = ExifTable()

        layout = QHBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.table)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumHeight(300)
        self.scrollArea.setMaximumHeight(450)

        layout.addWidget(self.scrollArea)

        self.setLayout(layout)

    def ReloadExifPanel(self):
        t = ExifTable(self.exifData)
        self.scrollArea.setWidget(t)

    def LoadExif(self, path):
        f = open(path, 'rb')
        tags = exifread.process_file(f, details=False)
        self.exifData = {}
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                self.exifData[tag] = str(tags[tag])
        self.ReloadExifPanel()

    def ImageSelectedEvent(self, path):
        self.LoadExif(path)

class Histogram(QGroupBox):
    layout = None
    def __init__(self):
        super().__init__()
        super().__init__('Histogram')

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.layout.addWidget(QLabel('Test'))
        self.setLayout(self.layout)

        self.setMaximumHeight(230)
        self.setMinimumHeight(230)

class BasicInspectorPanel(QWidget):
    layout = None
    histogram = None
    exifBox = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.histogram = Histogram()
        self.exifBox = ExifBox()

        lineWidget = QWidget()
        lineWidget.setFixedHeight(1)
        lineWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lineWidget.setStyleSheet('background: rgb(51,51,51)')

        self.layout.addWidget(self.histogram)
        self.layout.addSpacing(8)
        self.layout.addWidget(lineWidget)
        self.layout.addSpacing(8)
        self.layout.addWidget(self.exifBox)

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
