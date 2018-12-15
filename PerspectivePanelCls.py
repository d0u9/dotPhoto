from PyQt5.QtWidgets import QWidget, QHBoxLayout

from OperationPanelCls import OperationPanel
from MainPanelCls import MainPanel
from InspectorPanelCls import InspectorPanel

class PerspectivePanel(QWidget):
    layout = None
    operationPanel = None
    mainPanel = None
    inspectorPanel = None

    def __init__(self):
        super(QWidget, self).__init__()

        # Create widgets
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.operationPanel = OperationPanel()
        self.layout.addWidget(self.operationPanel)
        self.mainPanel = MainPanel()
        self.layout.addWidget(self.mainPanel)
        self.inspectorPanel = InspectorPanel()
        self.layout.addWidget(self.inspectorPanel)

        self.Setup()

    def Setup(self):
        self.setLayout(self.layout)
        self.setMinimumWidth(960)


