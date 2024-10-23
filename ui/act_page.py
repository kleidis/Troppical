from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from init_instances import inst
from ui.header import Header

class ActPage(QWidget,):
    def __init__(self):
        super().__init__()
        self.header = Header.header(self)
        # Act page
        self.actPage = QWidget()
        ## Layout and gorup
        actLayout = QVBoxLayout()
        actGroup = QGroupBox("")
        actGroupLayout = QVBoxLayout()
        buttonsLayout = QHBoxLayout()
        actGroup.setLayout(actGroupLayout)
        self.actPage.setLayout(actLayout) # Set the actpage layout
        ## Widgets
        self.actLabel = QLabel()
        self.actLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.installButton = QPushButton('Install')
        self.updateButton = QPushButton('Check for Updates')
        self.uninstallButton = QPushButton('Uninstall')
        self.backButton = QPushButton("Back")
        self.backButton.setFixedSize(80, 30)
        ## Add widgets / layouts
        actLayout.addLayout(self.header)
        actLayout.addWidget(actGroup)
        actGroupLayout.addWidget(self.actLabel)
        buttonsLayout.addWidget(self.installButton)
        buttonsLayout.addWidget(self.updateButton)
        buttonsLayout.addWidget(self.uninstallButton)
        actLayout.addLayout(buttonsLayout)
        actLayout.insertWidget(0, self.backButton)
