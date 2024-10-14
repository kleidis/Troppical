from imports import *
from main import Logic as main
from header import Header

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
        self.installButton.clicked.connect(main.qt_button_click)
        self.updateButton = QPushButton('Check for Updates')
        self.updateButton.clicked.connect(main.qt_button_click)
        self.uninstallButton = QPushButton('Uninstall')
        self.uninstallButton.clicked.connect(main.qt_button_click)
        self.backButton = QPushButton("Back")
        self.backButton.setFixedSize(80, 30)
        self.backButton.clicked.connect(main.qt_button_click)
        ## Add widgets / layouts
        welcomerLayout.addLayout(self.header)
        welcomerLayout.addWidget(welcomerGroup)
        welcomerGroupLayout.addWidget(self.welcomerLabel)
        buttonsLayout.addWidget(self.installButton)
        buttonsLayout.addWidget(self.updateButton)
        buttonsLayout.addWidget(self.uninstallButton)
        welcomerLayout.addLayout(buttonsLayout)
        welcomerLayout.insertWidget(0, self.backButton)
