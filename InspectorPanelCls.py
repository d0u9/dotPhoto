from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor

class InspectorPanel(QWidget):
    layout = None

    def __init__(self):
        super(QWidget, self).__init__()

        # Create widgets
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
        self.setMinimumWidth(300)
        self.setMaximumWidth(300)

        p = QPalette()
        p.setColor(QPalette.Background, QColor.fromRgb(38, 38, 38))
        self.setAutoFillBackground(True)
        self.setPalette(p)



