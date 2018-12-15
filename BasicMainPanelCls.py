from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor

class BasicMainPanel(QWidget):
    layout = None

    def __init__(self):
        super().__init__()

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);
        self.layout.addWidget(QLabel("BasicMainPanel"))


        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)




