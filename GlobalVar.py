from PyQt5.QtCore import Qt, QDir, QStandardPaths, QSize, pyqtSignal

appName = "dotPhoto"
cwd = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)


# All widgets which have singal sent to global have to be registered here
# and be assigned when its instance is created.

# ToolbarCls.py
workDirPathBox = None

# BasicOperationPanelCls.py
fileExplore = None


# All widgets have global observers have to be registered here

# ToolbarCls.py
workDirPathInputBoxPathChangeEvent = None

# BasicOperationPanelCls.py
fileExplorePathChangeEvent = None

# BasicMainPanelCls.py
ChangePhotoEvent = None


def SignalConnection():
    workDirPathBox.pathChanged.connect  (fileExplorePathChangeEvent)
    fileExplore.pathChanged.connect     (workDirPathInputBoxPathChangeEvent)
    fileExplore.fileSelected.connect    (ChangePhotoEvent)

