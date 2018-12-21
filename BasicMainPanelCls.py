from os import path
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimeLine, QPoint, QRectF, QFileInfo, QFile, QStandardPaths, pyqtSignal

import GlobalVar as gVar
from DirSelectWidgetCls import DirSelectWidget

class PicScene(QGraphicsScene):
    originImageRect = 0
    item = None

    imageLoaded = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        gVar.imageViewImageSelectedEvent = self.ImageSelectedEvent

    def ImageSelectedEvent(self, path):
        self.AddImageCenter(path)
        self.update()
        self.imageLoaded.emit()

    def AddImageCenter(self, path):
        if self.item is not None:
            self.removeItem(self.item)

        self.image = QPixmap(path)
        sceneRect = self.sceneRect()
        self.originImageRect = self.image.rect()
        self.originImageRect.moveCenter(sceneRect.toRect().center())
        self.item = QGraphicsPixmapItem(self.image)
        self.item.setOffset(self.originImageRect.x(), self.originImageRect.y())
        self.addItem(self.item)

    def ResizeEvent(self, factor):
        pass


class PicCanvas(QGraphicsView):
    scene = None
    item = None
    image = None
    _numScheduledScalings = 0
    factor = 1.0

    def __init__(self):
        super().__init__()
        self.scene = PicScene(self)
        self.scene.imageLoaded.connect(self.LoadImageEvent)

        self.Setup()

    def Setup(self):
        self.setScene(self.scene)

    def resizeEvent(self, event):
        print('resize')
        # TODO: check if pic is fully displayed,

        self.scene.ResizeEvent(self.factor)

    def showEvent(self, event):
        print(self.scene.sceneRect())
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        #  self.fitInView(0, 0, 2000, 2000)

    def wheelEvent(self, event):
        numDegrees = event.angleDelta() / 8
        print("wheel: {}".format(numDegrees))
        numSteps = numDegrees.y() / 15;
        self._numScheduledScalings += numSteps;
        if self._numScheduledScalings * numSteps < 0:
            self._numScheduledScalings = numSteps

        anim = QTimeLine(350, self)
        anim.setUpdateInterval(20);
        anim.valueChanged.connect(self.ScalingTime)
        anim.finished.connect(self.AnimFinished)
        anim.start()

    def ScalingTime(self, x):
        self.factor = 1.0 + self._numScheduledScalings / 300.0;
        self.scale(self.factor, self.factor)

    def AnimFinished(self):
        if self._numScheduledScalings > 0:
            self._numScheduledScalings -= 1;
        else:
            self._numScheduledScalings += 1;

    def LoadImageEvent(self):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)


class QuickOpsPanel(QWidget):
    layout = None
    imagePathBox = None
    imageFileSizeBox = None
    imageModifyTimeBox = None
    currentSelectPic = None
    rawDir = None
    rawSuffix = None
    messageBox = None
    moveToDirWidget = None

    def __init__(self):
        super().__init__()
        gVar.basicMainPanelOpsSelectedEvent = self.ImageSelectedEvent
        gVar.basicMainPanelOpsRawDirChangedEvent = self.RawDirChangedEvent
        gVar.basicMainPanelOpsRawSuffixChangedEvent = self.RawSuffixChangedEvent

        self.rawSuffix = [x.strip() for x in gVar.defaultRawSuffix.split(',')]
        self.rawDir = gVar.cwd

        self.setMaximumHeight(120)
        self.setMinimumHeight(120)
        self.setStyleSheet("""
            QPushButton {
                width: 200px;
                height: 60px;
            }
        """)

        layout = QHBoxLayout()
        self.imagePathBox = QLabel('')
        self.imagePathBox.setAlignment(Qt.AlignCenter);
        self.imageFileSizeBox = QLabel('55MB')
        self.imageFileSizeBox.setAlignment(Qt.AlignCenter)
        self.imageFileSizeBox.setMaximumWidth(100)
        self.imageFileSizeBox.setMinimumWidth(100)
        self.imageModifyTimeBox = QLabel('2018-12-22 12:32:12')
        self.imageModifyTimeBox.setAlignment(Qt.AlignCenter)
        self.imageModifyTimeBox.setMaximumWidth(200)
        self.imageModifyTimeBox.setMinimumWidth(200)

        layout.addWidget(self.imageFileSizeBox)
        layout.addWidget(self.imagePathBox)
        layout.addWidget(self.imageModifyTimeBox)

        self.layout = QVBoxLayout()
        moveToDir = cwd = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
        dirSelectDialogBox = DirSelectWidget(moveToDir, '...')
        dirSelectDialogBox.SetSize(350, 22, 22, 22)
        self.moveToDirWidget = dirSelectDialogBox

        label = QLabel('Save deleted file to:')

        layout2 = QGridLayout()
        layout2.addWidget(label, 0, 0)
        layout2.addWidget(dirSelectDialogBox, 0, 1)
        button1 = QPushButton('Delete RAW only')
        button1.clicked.connect(self.DeleteRawEvent)
        button2 = QPushButton('Delete Both JPEG and RAW')
        button2.clicked.connect(self.DeleteBothEvent)
        layout2.setColumnStretch(2, 20)
        layout2.addWidget(button1, 0, 3)
        layout2.addWidget(button2, 1, 3)

        self.messageBox = QLabel()
        layout2.addWidget(self.messageBox, 1, 0, 1, 2)

        self.layout.addLayout(layout)
        self.layout.addLayout(layout2)
        self.layout.addStretch()

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
        p = QPalette()
        p.setColor(QPalette.Background, QColor.fromRgb(38,38,38))
        self.setAutoFillBackground(True)
        self.setPalette(p)

    def ImageSelectedEvent(self, path):
        def HumanSize(size, decimal_places):
            for unit in ['','KB','MB','GB','TB']:
                if size < 1024.0:
                    break
                size /= 1024.0
            return f"{size:.{decimal_places}f} {unit}"

        finfo = QFileInfo(path)
        self.imagePathBox.setText(finfo.absoluteFilePath())
        self.imageFileSizeBox.setText(HumanSize(finfo.size(), 3))
        date = finfo.lastModified().toString('yyyy-dd-MM hh:mm:ss')
        self.imageModifyTimeBox.setText(date)
        self.currentSelectPic = finfo

    def DeleteRawEvent(self):
        if self.currentSelectPic is None:
            return
        baseName = self.currentSelectPic.baseName()
        foundSuffix = []
        for suffix in self.rawSuffix:
            fname = baseName + '.' + suffix
            rawPath = path.join(self.rawDir, fname)
            targetPath = path.join(self.moveToDirWidget.text(), fname)
            print(rawPath)
            d = QFile(rawPath)
            if d.exists():
                foundSuffix.append(suffix)
                d.rename(targetPath)

        if len(foundSuffix) == 0:
            self.messageBox.setText("Can't find raw file")
        else:
            files = [ baseName+'.'+x for x in foundSuffix]
            print(files)
            self.messageBox.setText("Delete raw:  " + ', '.join(files))

    def DeleteBothEvent(self):
        if self.currentSelectPic is None:
            return
        path = self.currentSelectPic.absoluteFilePath()
        print(path)

    def RawDirChangedEvent(self, path):
        self.rawDir = path

    def RawSuffixChangedEvent(self, suffix):
        self.rawSuffix = [x.strip() for x in suffix.split(',')]

class PicDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.picCanvas = PicCanvas()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0);
        layout.addWidget(self.picCanvas)
        self.setLayout(layout)


class BasicMainPanel(QWidget):
    layout = None
    picDisplay = None
    opsPanel = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.picDisplay = PicDisplay()
        self.opsPanel = QuickOpsPanel()
        gVar.basicMainPanelOps = self.opsPanel


        self.layout.addWidget(self.picDisplay)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.opsPanel)

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)

    def ImageSelectedEvent(self, path):
        pass



