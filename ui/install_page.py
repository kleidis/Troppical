from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGroupBox, QComboBox, QCheckBox, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
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

        headerLayout = QHBoxLayout()
        headerLayout.setSpacing(16)

        self.backButton = QPushButton("Back")
        self.backButton.setFixedSize(80, 28)
        self.backButton.setFont(QFont("Segoe UI", 11))
        self.backButton.clicked.connect(lambda: inst.ui.qt_index_switcher(1))
        headerLayout.addWidget(self.backButton)

        titleLayout = QVBoxLayout()
        titleLayout.setSpacing(4)

        titleLabel = QLabel("<font size='10'>Troppical</font>")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        titleLayout.addWidget(titleLabel)

        headerLayout.addLayout(titleLayout)
        headerLayout.addStretch()

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

        installLayout.addLayout(headerLayout)
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
