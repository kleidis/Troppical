from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from init_instances import inst
from ui.header import Header

class WelcomePage(QWidget,):
    def __init__(self):
        super().__init__()
        self.header = Header.header(self)
        # Welcome page
        self.welcomePage = QWidget()
        ## Layout and gorup
        welcomerLayout = QVBoxLayout()
        welcomerGroup = QGroupBox("")
        welcomerGroupLayout = QVBoxLayout()
        buttonsLayout = QHBoxLayout()
        welcomerGroup.setLayout(welcomerGroupLayout)
        self.welcomePage.setLayout(welcomerLayout) # Set the welcomepage layout
        ## Widgets
        self.welcomerLabel = QLabel()
        self.welcomerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.installButton = QPushButton('Install')
        self.updateButton = QPushButton('Check for Updates')
        self.uninstallButton = QPushButton('Uninstall')
        self.backButton = QPushButton("Back")
        self.backButton.setFixedSize(80, 30)
        ## Add widgets / layouts
        welcomerLayout.addLayout(self.header)
        welcomerLayout.addWidget(welcomerGroup)
        welcomerGroupLayout.addWidget(self.welcomerLabel)
        buttonsLayout.addWidget(self.installButton)
        buttonsLayout.addWidget(self.updateButton)
        buttonsLayout.addWidget(self.uninstallButton)
        welcomerLayout.addLayout(buttonsLayout)
        welcomerLayout.insertWidget(0, self.backButton)
