from PyQt5.QtWidgets import QWidget, QHBoxLayout

from PerspectiveBarCls import PerspectiveBar
from PerspectivePanelCls import PerspectivePanel

class CentralWidget(QWidget):
    layout = None
    perspectiveBar = None
    PerspectivePanel = None

    def __init__(self):
        super().__init__()

        # Create
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.perspectiveBar = PerspectiveBar()
        self.perspectivePanel = PerspectivePanel()

        self.layout.addWidget(self.perspectiveBar)
        self.layout.addWidget(self.perspectivePanel)

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)


