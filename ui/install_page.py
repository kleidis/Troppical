 # Install page
from imports import *
from main import Logic as main
from header import Header

class InstallPage(QWidget):
    def __init__(self):
        super().__init__()
        self.header = Header.header(self)
        self.installPage = QWidget()
        ## Layout and gorup
        installLayout = QVBoxLayout()
        checkboxLayout = QVBoxLayout()
        checkboxGroup = QGroupBox("Do you want to create shortcuts?") # Checkboxes
        checkboxGroup.setLayout(checkboxLayout) # Set the layout of Checkboxes
        pathSelectorLayout = QHBoxLayout() # Browse widget layout
        self.installPage.setLayout(installLayout) # Set the installpage layout
        ## Widgets
        InstalOpt = QLabel('<b>Installation Options')
        InstalOpt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.installationSourceComboBox = QComboBox() # Dropdown menu
        self.desktopShortcutCheckbox = QCheckBox("Create a desktop shortcut") # Checkboxes
        self.startMenuShortcutCheckbox = QCheckBox("Create a start menu shortcut")
        self.installationPathLineEdit = QLineEdit()  # Browse for installation path widget
        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(main.InstallPath)
        self.install_emu_button = QPushButton('Install') # Install button
        self.install_emu_button.clicked.connect(main.qt_button_click)
        ## Add widgets / layouts
        installLayout.addLayout(self.header) ### Icon self.header
        installLayout.addWidget(InstalOpt) ### Instalation Option Label
        installLayout.addWidget(self.installationSourceComboBox) ## Install Sorce Widget
        pathSelectorLayout.addWidget(self.installationPathLineEdit) ## Browse Widget
        pathSelectorLayout.addWidget(self.browseButton)
        installLayout.addLayout(pathSelectorLayout)
        checkboxLayout.addWidget(self.desktopShortcutCheckbox) # Checkboxes
        checkboxLayout.addWidget(self.startMenuShortcutCheckbox)
        installLayout.addWidget(checkboxGroup)
        installLayout.addWidget(self.install_emu_button)
