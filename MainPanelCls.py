from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor

class MainPanel(QWidget):
    layout = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(8,8,8,8);

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)

        p = QPalette()
        p.setColor(QPalette.Background, QColor.fromRgb(29, 29, 29))
        self.setAutoFillBackground(True)
        self.setPalette(p)

    def SetWidget(self, widget):
        self.layout.addWidget(widget)




