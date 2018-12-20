from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimeLine, QPoint, QRectF

import GlobalVar as gVar

class PicScene(QGraphicsScene):
    originImageRect = 0
    item = None

    def __init__(self, parent):
        super().__init__(parent)
        gVar.ChangePhotoEvent = self.ChangePhotoEvent

        self.AddImageCenter('/Users/doug/Downloads/test2.JPG')
        self.addLine(0,0,100,100)

    def ChangePhotoEvent(self, path):
        self.AddImageCenter(path)
        self.update()

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

        self.Setup()

    def Setup(self):
        self.setScene(self.scene)
        self.setStyleSheet('background-color: blue')

    def resizeEvent(self, event):
        print('resize')
        # TODO: check if pic is fully displayed,

        self.scene.ResizeEvent(self.factor)

    def showEvent(self, event):
        print(self.scene.sceneRect())
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        #  self.fitInView(0, 0, 2000, 2000)

    def wheelEvent(self, event):
        print('wheel')
        numDegrees = event.angleDelta() / 8
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


class BasicMainPanel(QWidget):
    layout = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.hlayout = QHBoxLayout()
        self.hlayout.setSpacing(0)
        self.hlayout.setContentsMargins(0,0,0,0);

        self.picCanvas = PicCanvas()

        self.hlayout.addStretch()
        self.hlayout.addWidget(self.picCanvas)
        self.hlayout.addStretch()

        self.layout.addStretch()
        self.layout.addLayout(self.hlayout)
        self.layout.addStretch()


        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)




