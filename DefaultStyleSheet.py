defaultStyleSheet = """
    * {
        color: rgb(216,216,216);
    }

    QToolBar {
        background: rgb(65,65,65);
        border: none;
        spacing: 3px; /* spacing between items in the tool bar */
    }

    QToolBar::handle {
        background: rgb(65,65,65);
        border: none;
    }

    QPushButton {
        background-color: rgb(92,92,92);
        padding: 0px;
        border-style: outset;
        border-radius: 5px;
    }

    QPushButton:pressed {
        background-color: rgb(117,117,117);
        border-style: inset;
    }

    QLineEdit {
        height: 20px;
        border: 3px solid rgb(255,255,255,0%);
        border-radius: 3px;
        padding: 0 8px;
        background: rgb(35,35,35);
        selection-background-color: darkgray;
        font-size: 12px;
    }

    QLineEdit:focus {
        border: 3px solid rgb(54,100,136);
    }

    QTreeView {
        background: rgb(35,35,35);
        font-size: 12px;
    }

    QScrollBar, QScrollBar:add-line, QScrollBar:sub-line {
        background: rgb(39,39,39);
        border: none;
    }

    QScrollBar:handle {
        background: rgb(151,151,148);
        border: 3px solid rgb(39,39,39);
        border-radius: 9px;
    }

    QGraphicsView {
        background: rgb(29,29,29);
    }




"""
