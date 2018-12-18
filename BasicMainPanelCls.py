from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt

class PicCanvas(QGraphicsView):
    scene = None
    item = None

    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.item = QGraphicsPixmapItem(QPixmap('/Users/doug/Downloads/test2.JPG'))
        self.scene.addItem(self.item)

        self.Setup()

    def Setup(self):
        self.setScene(self.scene)

    def showEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

class BasicMainPanel(QWidget):
    layout = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.picCanvas = PicCanvas()
        self.layout.addWidget(self.picCanvas)


        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)




