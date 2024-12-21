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
            background-color: #E81123;
            border: none;
            border-radius: 4px;
            margin: 8px;
            padding: 0 12px;
            color: white;
            min-height: 38px;
            max-height: 38px;
        }

        QPushButton:hover {
            background-color: #F23B4A;
        }

        QPushButton:pressed {
            background-color: #C41019;
        }

        QPushButton:disabled {
            color: rgb(150, 150, 150);
            background-color: rgba(255, 255, 255, 0.13);
        }
        QLabel, QCheckBox {
            color: #ffffff;
        }
        /*GROUPBOX*/
        QGroupBox {
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 36px;
            background-color: transparent;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            background-color: rgba(255, 255, 255, 0.06);
            padding: 7px 15px;
            margin-left: 5px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            color: rgba(255, 255, 255, 0.9);
        }

        QGroupBox::title::disabled {
            color: rgb(150, 150, 150)
        }
        /*COMBOBOX*/
        QComboBox {
            background-color: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            padding-left: 10px;
            min-height: 38px;
            max-height: 38px;
        }

        QComboBox:hover {
            background-color: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        QComboBox::pressed {
            background-color: rgba(255, 255, 255, 0.06);
            border: 1px solid #E81123;
            color: white;
        }

        QComboBox:focus {
            border: 1px solid #E81123;
        }

        QComboBox QAbstractItemView {
            background-color: rgba(45, 45, 45, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            selection-background-color: rgba(255, 255, 255, 0.06);
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
            border-color: #E81123;
            background-color: rgba(232, 17, 35, 0.1);
        }

        QCheckBox::indicator:pressed {
            border-color: #C41019;
            background-color: rgba(232, 17, 35, 0.15);
        }

        QCheckBox::indicator:checked {
            border-color: #E81123;
            background-color: #E81123;
            image: url(:/CheckBox/img dark/CheckBox.png);
        }

        QCheckBox::indicator:checked:hover {
            border-color: #F23B4A;
            background-color: #F23B4A;
        }

        QCheckBox::indicator:checked:pressed {
            border-color: #C41019;
            background-color: #C41019;
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
            background-color: rgba(255, 255, 255, 0.06);
            border: none;
            border-radius: 2px;
        }

        QProgressBar::chunk {
            background-color: #E81123;
            border-radius: 2px;
        }

        QProgressBar::chunk:hover {
            background-color: #F23B4A;
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
            background-color: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            padding: 5px 10px;
            color: white;
            font-size: 13px;
        }

        QLineEdit:hover {
            background-color: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        QLineEdit:focus {
            background-color: rgba(255, 255, 255, 0.06);
            border: 1px solid #E81123;
        }

        QLineEdit::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }

        /*TREEWIDGET*/
        QTreeWidget {
            background-color: transparent;
            color: white;
            font-size: 13px;
        }

        QTreeView {
            background-color: transparent;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0px;
            outline: 0;
            padding: 5px;
        }

        QTreeView::item {
            padding: 6px 8px;
            margin: 2px 0;
            border-radius: 0px;
        }

        QTreeView::item:selected {
            background-color: rgba(255, 255, 255, 0.06);
            border: none;
        }

        QTreeView::item:hover:!selected {
            background-color: rgba(255, 255, 255, 0.03);
        }

        QTreeView::branch:has-children:!has-siblings:closed,
        QTreeView::branch:closed:has-children:has-siblings {
            image: url(:/TreeView/img dark/TreeViewClose.png);
        }

        QTreeView::branch:open:has-children:!has-siblings,
        QTreeView::branch:open:has-children:has-siblings {
            image: url(:/TreeView/img dark/TreeViewOpen.png);
        }

        QTreeView::branch:has-children:!has-siblings,
        QTreeView::branch:has-children:has-siblings {
            padding-left: 4px;
        }

        QTreeView:disabled {
            color: rgba(255, 255, 255, 0.3);
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
