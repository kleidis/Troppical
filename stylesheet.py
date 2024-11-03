# Credit to QtWin11 project

class Style:
    dark_stylesheet = """
        QWidget {
            background-color: transparent;
            color: rgb(255, 255, 255);
            font-size: 17px;
            font-family: "Segoe UI Variable Small", serif;
            font-weight: 400;
        }
        /*PUSHBUTTON*/
        QPushButton {
            background-color: rgba(50, 50, 52, 0.7);
            border: 1px solid rgb(68, 68, 68);
            border-radius: 7px;
            min-height: 38px;
            max-height: 38px;
        }

        QPushButton:hover {
            background-color: rgba(100, 100, 100, 0.7);
            border: 1px solid rgba(255, 255, 255, 10);
        }

        QPushButton::pressed {
            background-color: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 13);
            color: rgba(255, 255, 255, 200);
        }

        QPushButton::disabled {
            color: rgb(150, 150, 150);
            background-color: rgba(255, 255, 255, 0.13);
        }
        QLabel, QCheckBox {
            color: #ffffff;
        }
        /*GROUPBOX*/
        QGroupBox {
            border-radius: 5px;
            border: 0px solid rgba(255, 255, 255, 13);
            margin-top: 36px;
            background-color: transparent;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            background-color: rgba(255, 255, 255, 0.16);
            padding: 7px 15px;
            margin-left: 5px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }

        QGroupBox::title::disabled {
            color: rgb(150, 150, 150)
        }
        /*COMBOBOX*/
        QComboBox {
            background-color: rgba(66, 66, 66, 0.7);
            border: 1px solid rgb(68, 68, 68);
            border-radius: 5px;
            padding-left: 10px;
            min-height: 38px;
            max-height: 38px;
        }

        QComboBox:hover {
            background-color: rgba(120, 120, 120, 0.7);
            border: 1px solid rgba(255, 255, 255, 10);
        }

        QComboBox::pressed {
            background-color: rgba(66, 66, 66, 0.7);
            border: 1px solid #0078D4;
            color: rgba(255, 255, 255, 200);
        }

        QComboBox::down-arrow {
            image: url(:/ComboBox/img dark/ComboBox.png);
        }

        QComboBox::drop-down {
            background-color: transparent;
            min-width: 50px;
        }

        QComboBox:disabled {
            color: rgb(150, 150, 150);
            background-color: rgba(255, 255, 255, 0.13);
            border: 1px solid rgba(255, 255, 255, 5);
        }

        QComboBox::down-arrow:disabled {
            image: url(:/ComboBox/img dark/ComboBoxDisabled.png);
        }
        /*CHECKBOX*/
        QCheckBox {
            min-height: 30px;
            max-height: 30px;
        }

        QCheckBox::indicator {
            width: 22px;
            height: 22px;
            border-radius: 5px;
            border: 2px solid #848484;
            background-color: transparent;
            margin-right: 5px;
        }

        QCheckBox::indicator:hover {
            background-color: rgba(255, 255, 255, 0.16);
        }

        QCheckBox::indicator:pressed {
            background-color: rgba(255, 255, 255, 0.20);
            border: 2px solid #434343;
        }

        QCheckBox::indicator:checked {
            background-color: #0078D4;
            border: 2px solid #0078D4;
            image: url(:/CheckBox/img dark/CheckBox.png);
        }

        QCheckBox::indicator:checked:pressed {
            image: url(:/CheckBox/img dark/CheckBoxPressed.png);
        }

        QCheckBox:disabled {
            color: rgb(150, 150, 150);
        }

        QCheckBox::indicator:disabled {
            border: 2px solid #646464;
            background-color: transparent;
        }
        /*PROGRESSBAR*/
        QProgressBar {
            background-color: qlineargradient(spread:reflect, x1:0.5, y1:0.5, x2:0.5, y2:1, stop:0.119403 rgba(255, 255, 255, 0.25), stop:0.273632 rgba(0, 0, 0, 0));
            border-radius: 2px;
            min-height: 4px;
            max-height: 4px;
        }

        QProgressBar::chunk {
            background-color: #0078D4;
            border-radius: 2px;
        }
        /*MENU*/
        QMenu {
            background-color: transparent;
            padding-left: 1px;
            padding-top: 1px;
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 13);
        }

        QMenu::item {
            background-color: transparent;
            padding: 5px 15px;
            border-radius: 5px;
            min-width: 60px;
            margin: 3px;
        }

        QMenu::item:selected {
            background-color: rgba(255, 255, 255, 0.16);
        }

        QMenu::item:pressed {
            background-color: rgba(255, 255, 255, 0.10);
        }

        QMenu::right-arrow {
            image: url(:/TreeView/img dark/TreeViewClose.png);
            min-width: 40px;
            min-height: 18px;
        }

        QMenuBar:disabled {
            color: rgb(150, 150, 150);
        }

        QMenu::item:disabled {
            color: rgb(150, 150, 150);
            background-color: transparent;
        }
        /*LINEEDIT*/
        QLineEdit {
            background-color: rgba(50, 50, 52, 0.7);
            border: 1px solid rgb(68, 68, 68);
            font-size: 16px;
            font-family: "Segoe UI", serif;
            font-weight: 500;
            border-radius: 7px;
            border-bottom: 1px solid rgba(255, 255, 255, 150);
            padding-top: 0px;
            padding-left: 5px;
        }

        QLineEdit:hover {
            background-color: rgba(120, 120, 120, 0.7);
            border: 1px solid rgba(255, 255, 255, 10);
            border-bottom: 1px solid rgba(255, 255, 255, 150);
        }

        QLineEdit:focus {
            border-bottom: 2px solid #0078D4;
            background-color: rgba(100, 100, 100, 0.7);
            border-top: 1px solid rgba(255, 255, 255, 13);
            border-left: 1px solid rgba(255, 255, 255, 13);
            border-right: 1px solid rgba(255, 255, 255, 13);
        }

        QLineEdit:disabled {
            color: rgb(150, 150, 150);
            background-color: rgba(255, 255, 255, 0.13);
            border: 1px solid rgba(255, 255, 255, 5);
        }
        /*TREEWIDGET*/
        QTreeWidget {
            background-color: transparent;
            color: white;
        }
        QTreeView {
            background-color: transparent;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 5px;
            outline: 0;
            padding-right: 5px;
        }

        QTreeView::item {
            padding: 7px;
            margin-top: 3px;
        }

        QTreeView::item:selected {
            background-color: rgba(45, 45, 45, 0.7);
            border-radius: 0px;
            margin-bottom: 3px;
            padding-left: 0px;
        }

        QTreeView::item:!selected:hover {
            background-color: rgba(255, 255, 255, 0.06);
            border-radius: 0px;
            margin-bottom: 3px;
            padding-left: 0px;
        }

        QTreeView::branch:has-children:!has-siblings:closed,
        QTreeView::branch:closed:has-children:has-siblings {
            image: url(:/TreeView/img dark/TreeViewClose.png);
        }

        QTreeView::branch:open:has-children:!has-siblings,
        QTreeView::branch:open:has-children:has-siblings {
            image: url(:/TreeView/img dark/TreeViewOpen.png);
        }

        QTreeView:disabled {
            color: rgb(150, 150, 150);
        }
        /*SCROLLVERTICAL*/
        QScrollBar:vertical {
            border: 6px solid transparent;
            margin: 14px 0px 14px 0px;
            width: 16px;
        }

        QScrollBar:vertical:hover {
            border: 5px solid transparent;
        }

        QScrollBar::handle:vertical {
            background-color: rgba(255, 255, 255, 0.51);
            border-radius: 2px;
            min-height: 25px;
        }

        QScrollBar::sub-line:vertical {
            image: url(:/ScrollVertical/img dark/ScrollTop.png);
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:vertical:hover {
            image: url(:/ScrollVertical/img dark/ScrollTopHover.png);
        }

        QScrollBar::sub-line:vertical:pressed {
            image: url(:/ScrollVertical/img dark/ScrollTopPressed.png);
        }

        QScrollBar::add-line:vertical {
            image: url(:/ScrollVertical/img dark/ScrollBottom.png);
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::add-line:vertical:hover {
            image: url(:/ScrollVertical/img dark/ScrollBottomHover.png);
        }

        QScrollBar::add-line:vertical:pressed {
            image: url(:/ScrollVertical/img dark/ScrollBottomPressed.png);
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

        /*SCROLLHORIZONTAL*/
        QScrollBar:horizontal {
            border: 6px solid transparent;
            margin: 0px 14px 0px 14px;
            height: 16px;
        }

        QScrollBar:horizontal:hover {
            border: 5px solid transparent;
        }

        QScrollBar::handle:horizontal {
            background-color: rgba(255, 255, 255, 0.51);
            border-radius: 2px;
            min-width: 25px;
        }

        QScrollBar::sub-line:horizontal {
            image: url(:/ScrollHorizontal/img dark/ScrollLeft.png);
            subcontrol-position: left;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:horizontal:hover {
            image: url(:/ScrollHorizontal/img dark/ScrollLeftHover.png);
        }

        QScrollBar::sub-line:horizontal:pressed {
            image: url(:/ScrollHorizontal/img dark/ScrollLeftPressed.png);
        }

        QScrollBar::add-line:horizontal {
            image: url(:/ScrollHorizontal/img dark/ScrollRight.png);
            subcontrol-position: right;
            subcontrol-origin: margin;
        }

        QScrollBar::add-line:horizontal:hover {
            image: url(:/ScrollHorizontal/img dark/ScrollRightHover.png);
        }

        QScrollBar::add-line:horizontal:pressed {
            image: url(:/ScrollHorizontal/img dark/ScrollRightPressed.png);
        }

        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        """

