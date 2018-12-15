from PyQt5.QtWidgets import QWidget, QHBoxLayout, QStackedWidget

from PerspectiveBarCls import PerspectiveBar
from PerspectivePanelCls import PerspectivePanel
from BasicPerspectivePanelCls import BasicPerspectivePanel

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

        self.perspectivePanelBasic = BasicPerspectivePanel()
        self.perspectivePanelTest = PerspectivePanel()

        self.perspectivePanelStack = QStackedWidget()
        self.perspectivePanelStack.addWidget(self.perspectivePanelBasic)
        self.perspectivePanelStack.addWidget(self.perspectivePanelTest)

        self.perspectiveBar = PerspectiveBar(self.perspectivePanelStack)

        self.layout.addWidget(self.perspectiveBar)
        self.layout.addWidget(self.perspectivePanelStack)

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)



