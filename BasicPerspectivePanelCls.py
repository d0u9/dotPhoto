from PyQt5.QtWidgets import QWidget, QHBoxLayout

from PerspectivePanelCls import PerspectivePanel
from BasicOperationPanelCls import BasicOperationPanel
from BasicMainPanelCls import BasicMainPanel
from BasicInspectorPanelCls import BasicInspectorPanel


class BasicPerspectivePanel(PerspectivePanel):
    basicOperationPanel = None
    basicMainPanel = None
    basicInspectorPanel = None

    def __init__(self):
        super().__init__()
        self.basicOperationPanel = BasicOperationPanel()
        self.operationPanel.SetWidget(self.basicOperationPanel)
        self.basicMainPanel = BasicMainPanel()
        self.mainPanel.SetWidget(self.basicMainPanel)
        self.basicInspectorPanel = BasicInspectorPanel()
        self.inspectorPanel.SetWidget(self.basicInspectorPanel)





