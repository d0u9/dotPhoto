from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor

class PerspectiveBar(QWidget):
    layout = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
        self.setMinimumWidth(55)
        self.setMaximumWidth(55)

        p = QPalette()
        p.setColor(QPalette.Background, QColor.fromRgb(38, 38, 38))
        self.setAutoFillBackground(True)
        self.setPalette(p)

