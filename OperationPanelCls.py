from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor

class OperationPanel(QWidget):
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
        self.setMinimumWidth(300)
        self.setMaximumWidth(300)

        p = QPalette()
        p.setColor(QPalette.Background, QColor.fromRgb(51, 51, 51))
        self.setAutoFillBackground(True)
        self.setPalette(p)

    def SetWidget(self, widget):
        self.layout.addWidget(widget)


