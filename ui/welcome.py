from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from ui.header import Header
from init_instances import inst

# Welcome page
class InitPage(QWidget):
    def __init__(self):
        super().__init__()
        self.welcomePage = QWidget()

        # Layout and groups
        welcomeLayout = QVBoxLayout()
        self.welcomePage.setLayout(welcomeLayout)

        # Add header
        #    self.Header = Header().header()  # Initialize the header
        #    welcomeLayout.addLayout(self.Header)

        # Welcome label
        welcomeLabel = QLabel("<b><font size='12'>Welcome to Troppical Installer!</font></b>")
        welcomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text horizontally
        welcomeLayout.addWidget(welcomeLabel)

        # Create a horizontal layout for the buttons
        buttonLayout = QHBoxLayout()

        # Manage button
        self.manageButton = QPushButton("Manage")
        self.manageButton.setFixedSize(200, 100)  # Set size for large rectangular shape

        # Configure button
        self.configureButton = QPushButton("Configure")
        self.configureButton.setFixedSize(200, 100)  # Set size for large rectangular shape
        self.configureButton.setToolTip("WIP: Coming soon!")
        self.configureButton.setEnabled(False)  # Set the button to be grayed out

        # Add buttons to the layout
        buttonLayout.addWidget(self.manageButton)
        buttonLayout.addWidget(self.configureButton)

        # Add button layout to the main layout
        welcomeLayout.addLayout(buttonLayout)