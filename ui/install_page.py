from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGroupBox, QComboBox, QCheckBox, QLineEdit
from PyQt6.QtCore import Qt
from init_instances import inst
from ui.header import Header

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
        self.browseButton.clicked.connect(inst.main.InstallPath)
        self.install_emu_button = QPushButton('Install') # Install button        ## Add widgets / layouts
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
