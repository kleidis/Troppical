from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGroupBox, QComboBox, QCheckBox, QLineEdit
from PyQt6.QtCore import Qt
from init_instances import inst

class InstallPage(QWidget):
    def __init__(self):
        super().__init__()
        self.installPage = QWidget()

        installLayout = QVBoxLayout()
        checkboxLayout = QVBoxLayout()
        checkboxGroup = QGroupBox("Do you want to create shortcuts?")
        checkboxGroup.setLayout(checkboxLayout)
        pathSelectorLayout = QHBoxLayout()
        self.installPage.setLayout(installLayout)

        InstalOpt = QLabel('<b>Installation Options')
        InstalOpt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.installationSourceComboBox = QComboBox()
        self.desktopShortcutCheckbox = QCheckBox("Create a desktop shortcut")
        self.startMenuShortcutCheckbox = QCheckBox("Create a start menu shortcut")
        self.installationPathLineEdit = QLineEdit()
        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(inst.main.InstallPath)

        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()
        self.install_emu_button = QPushButton('Install')
        self.install_emu_button.setFixedWidth(120)
        bottomLayout.addWidget(self.install_emu_button)

        installLayout.addLayout(inst.header.header())
        installLayout.addWidget(InstalOpt)
        installLayout.addWidget(self.installationSourceComboBox)
        pathSelectorLayout.addWidget(self.installationPathLineEdit)
        pathSelectorLayout.addWidget(self.browseButton)
        installLayout.addLayout(pathSelectorLayout)
        checkboxLayout.addWidget(self.desktopShortcutCheckbox)
        checkboxLayout.addWidget(self.startMenuShortcutCheckbox)
        installLayout.addWidget(checkboxGroup)
        installLayout.addStretch()
        installLayout.addLayout(bottomLayout)
