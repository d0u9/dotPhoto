from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor

class BasicOperationPanel(QWidget):
    layout = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(8,8,8,8);
        self.layout.addWidget(QLabel('Basic'))

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
