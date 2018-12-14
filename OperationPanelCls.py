from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor

class OperationPanel(QWidget):
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
        self.setMinimumWidth(230)
        self.setMaximumWidth(230)

        p = QPalette()
        p.setColor(QPalette.Background, QColor.fromRgb(51, 51, 51))
        self.setAutoFillBackground(True)
        self.setPalette(p)


