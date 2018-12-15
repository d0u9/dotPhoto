from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor

class BasicInspectorPanel(QWidget):
    layout = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);
        self.layout.addWidget(QLabel('BasicInspectorPanel'))

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
