from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

import GlobalConfig as gConfig
from CentralWidgetCls import CentralWidget

class Window(QMainWindow):
    centerWidget = None
    toolBar = None

    def __init__(self):
        super().__init__()
        self.Setup()

        # Create widgets
        self.centerWidget = CentralWidget()

        helpMenu = self.menuBar().addMenu('Help')
        testToolBar = self.addToolBar('&Test')

        aboutAction = helpMenu.addAction('About dotPhoto')
        aboutAction.setStatusTip('About ' + gConfig.appName)
        aboutAction.setMenuRole(QAction.ApplicationSpecificRole);
        aboutAction.triggered.connect(lambda x: print("Hello World"))
        testToolBar.addAction(aboutAction)

        self.Setup()

    def Setup(self):
        self.setGeometry(0, 0, 1200, 600)
        self.setWindowTitle(gConfig.appName)
        self.setCentralWidget(self.centerWidget)

    def ShowAll(self):
        pass

class Application(QApplication):
    window = None

    def __init__(self, argv):
        super().__init__(argv)

        # Create widgets
        self.window = Window()

        self.Setup()
        self.ShowAll()

    def Setup(self):
        self.setOrganizationName('dot')
        self.setApplicationName('dotPhoto')
        self.setApplicationVersion('0.1')

    def ShowAll(self):
        self.window.show()

