from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal

class Indicator(QWidget):
    selected = False
    selectPalette = QPalette()
    unselectPalette = QPalette()

    def __init__(self, width, height, selected=False):
        super().__init__()
        self.width = width
        self.height = height
        self.selected = selected
        self.selectPalette.setColor(QPalette.Background, QColor.fromRgb(216, 85, 106))
        self.unselectPalette.setColor(QPalette.Background, QColor.fromRgba64(255, 255, 255, 0))

        self.Setup()

    def Setup(self):
        self.setMinimumWidth(self.width)
        self.setMaximumWidth(self.width)
        self.setMinimumHeight(self.height)
        self.setMaximumHeight(self.height)

        self.setAutoFillBackground(True)
        self.Select() if self.selected else self.Unselect()

    def Select(self):
        self.selected = True
        self.setPalette(self.selectPalette)

    def Unselect(self):
        self.selected = False
        self.setPalette(self.unselectPalette)


class ItemBox(QWidget):
    fontPalette = QPalette()
    def __init__(self, width, height, title):
        super().__init__()
        self.width = width
        self.height = height
        self.title = title
        self.fontPalette.setColor(QPalette.WindowText, QColor.fromRgb(229, 229, 229))

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0);

        label = QLabel(self.title, self)
        label.setAlignment(Qt.AlignCenter)
        label.setPalette(self.fontPalette)
        layout.addWidget(label)

        self.setLayout(layout)
        self.Setup()

    def Setup(self):
        self.setMinimumWidth(self.width)
        self.setMaximumWidth(self.width)
        self.setMinimumHeight(self.height)
        self.setMaximumHeight(self.height)


class PerspectiveItem(QWidget):
    indicator = None
    itemBox = None

    selected = False
    selectPalette = QPalette()
    unselectPalette = QPalette()

    clicked = pyqtSignal(object)

    def __init__(self, size, title='None', idx=0, selected=False):
        super().__init__()
        self.size = size
        self.title = title
        self.idx = idx
        self.selected = selected
        self.selectPalette.setColor(QPalette.Background, QColor.fromRgb(51,51,51))
        self.unselectPalette.setColor(QPalette.Background, QColor.fromRgba64(255,255,255,0))

        indicatorWidth = 5
        self.indicator = Indicator(indicatorWidth, self.size, selected=self.selected)
        self.itemBox = ItemBox(self.size - indicatorWidth, self.size, self.title)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0);
        layout.addWidget(self.indicator)
        layout.addWidget(self.itemBox)
        self.setLayout(layout)

        self.Setup()

    def Setup(self):
        self.setMinimumWidth(self.size)
        self.setMaximumWidth(self.size)
        self.setMinimumHeight(self.size)
        self.setMaximumHeight(self.size)

        self.setAutoFillBackground(True)
        self.Select() if self.selected else self.Unselect()

    def Select(self):
        self.selected = True
        self.setPalette(self.selectPalette)
        self.indicator.Select()

    def Unselect(self):
        self.selected = False
        self.setPalette(self.unselectPalette)
        self.indicator.Unselect()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.clicked.emit(self)


class PerspectiveBar(QWidget):
    layout = None
    width = 55

    basicPanelTab = None
    currentPanelTab = None

    def SelectPanel(self, panelTab):
        self.currentPanelTab.Unselect()
        panelTab.Select()
        self.currentPanelTab = panelTab
        self.perspectivePanelStack.setCurrentIndex(panelTab.idx)

    def __init__(self, perspectivePanelStack):
        super().__init__()
        self.perspectivePanelStack = perspectivePanelStack

        # Create widgets
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0);

        self.basicPanelTab = PerspectiveItem(self.width, 'Basic', idx=0, selected=True)
        self.currentPanelTab = self.basicPanelTab
        self.basicPanelTab.clicked.connect(self.SelectPanel)
        self.layout.addWidget(self.basicPanelTab)

        self.TestPanelTab = PerspectiveItem(self.width, 'Test', idx=1)
        self.TestPanelTab.clicked.connect(self.SelectPanel)
        self.layout.addWidget(self.TestPanelTab)

        self.Setup()


    def Setup(self):
        self.layout.addStretch()
        self.setLayout(self.layout)
        self.setMinimumWidth(self.width)
        self.setMaximumWidth(self.width)

        p = QPalette()
        p.setColor(QPalette.Background, QColor.fromRgb(38, 38, 38))
        self.setAutoFillBackground(True)
        self.setPalette(p)
