from PyQt5.QtCore import Qt, QDir, QStandardPaths, QSize, pyqtSignal

appName = "dotPhoto"
cwd = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
defaultRawSuffix = 'CR2, RAF'



# All widgets which have singal sent to global have to be registered here
# and be assigned when its instance is created.

# ToolbarCls.py
workDirPathBox = None

# BasicOperationPanelCls.py
fileExplore = None
rawFileSuffix = None
rawFileDir = None

# BasicMainPanelCls.py
basicMainPanelOps = None


# All widgets have global observers have to be registered here

# ToolbarCls.py
workDirPathInputBoxPathChangeEvent = None

# BasicOperationPanelCls.py
fileExplorePathChangeEvent = None

# BasicMainPanelCls.py
imageViewImageSelectedEvent = None
basicMainPanelOpsSelectedEvent = None
basicMainPanelOpsRawDirChangedEvent = None
basicMainPanelOpsRawSuffixChangedEvent = None

# BasicInspectorPanel
exifBoxImageSelectedEvent = None


def SignalConnection():
    workDirPathBox.pathChanged.connect  (fileExplorePathChangeEvent)
    fileExplore.pathChanged.connect     (workDirPathInputBoxPathChangeEvent)
    fileExplore.fileSelected.connect    (imageViewImageSelectedEvent)
    fileExplore.fileSelected.connect    (exifBoxImageSelectedEvent)
    fileExplore.fileSelected.connect    (basicMainPanelOpsSelectedEvent)
    rawFileDir.pathChanged.connect      (basicMainPanelOpsRawDirChangedEvent)
    rawFileSuffix.suffixChanged.connect (basicMainPanelOpsRawSuffixChangedEvent)


