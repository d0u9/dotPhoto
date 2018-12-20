defaultStyleSheet = """
    * {
        color: rgb(216,216,216);
    }

    QToolBar {
        background: rgb(65,65,65);
        border: none;
        spacing: 3px; /* spacing between items in the tool bar */
        height: 55px;
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
        border: 3px solid rgb(255,255,255,0%);
        border-radius: 5px;
        border-style: outset;
        padding: 0 6px 0 6px;
        background: rgb(35,35,35);
        selection-background-color: darkgray;
        font-size: 12px;
        qproperty-frame: false;
    }

    QLineEdit:focus {
        border: 3px solid rgb(54,100,136);
    }

    QLineEdit:read-only {
        background: rgb(105,105,105);
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

    QCheckBox {
        spacing: 6px;
    }

    QCheckBox::indicator {
        width: 12px;
        height: 12px;
    }

    QCheckBox::indicator:unchecked {
        background: rgb(84,84,84);
    }


    QScrollArea {
        border: none;
        background: rgb(38,38,38);
        margin: 0;
        padding: 0;
    }

    QWidget {
        background-attachment: scroll;
    }

"""
