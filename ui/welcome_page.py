from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


# Welcome page
class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.welcomePage = QWidget()

        welcomeLayout = QVBoxLayout()
        welcomeLayout.setSpacing(2)
        welcomeLayout.setContentsMargins(24, 0, 24, 0)  # Added left/right padding
        self.welcomePage.setLayout(welcomeLayout)

        welcomeLabel = QLabel("<font size='10'>Troppical</font>")
        welcomeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        welcomeLayout.addWidget(welcomeLabel)
        welcomeLayout.addSpacing(24)

        self.manageButton = self.create_nav_button(
            "Manage",
            "Install a new emulator or Update / Uninstall your installed emulators",
        )
        # Configure navigation area
        self.configureButton = self.create_nav_button(
            "Configure", "Create and modify emulator settings (Coming Soon!)"
        )
        self.configureButton.setEnabled(False)

        welcomeLayout.addWidget(self.manageButton)
        welcomeLayout.addWidget(self.configureButton)
        welcomeLayout.addStretch()

        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()

        self.settingsButton = self.create_settings_button()
        bottomLayout.addWidget(self.settingsButton)

        welcomeLayout.addLayout(bottomLayout)

    def create_nav_button(self, text, tooltip):
        button = QPushButton()

        contentLayout = QVBoxLayout()
        contentLayout.setSpacing(8)
        contentLayout.setContentsMargins(30, 13, 30, 13)
        button.setLayout(contentLayout)

        # Add text with description
        titleLabel = QLabel(text)
        titleLabel.setFont(
            QFont("Segoe UI", 13)
        )  # Less bold, using font weight instead
        titleLabel.setStyleSheet("color: #FFFFFF;")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        descLabel = QLabel(tooltip)
        descLabel.setFont(QFont("Segoe UI", 9))
        descLabel.setStyleSheet("color: #AAAAAA;")
        descLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        descLabel.setWordWrap(True)

        contentLayout.addWidget(titleLabel)
        contentLayout.addWidget(descLabel)
        contentLayout.addStretch()

        # Style the button
        button.setFixedHeight(140)
        button.setToolTip(tooltip)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.06);
                border: none;
                border-radius: 4px;
                margin: 4px 12px;
                padding: 16px 0;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.12);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.09);
            }
            QPushButton:disabled {
                background-color: rgba(30, 30, 30, 0.5);
                border: 1px solid rgba(80, 80, 80, 0.3);
            }
            QPushButton:disabled * {
                color: rgba(255, 255, 255, 0.3);
            }
        """
        )

        return button

    def create_settings_button(self):
        button = QPushButton("Settings")
        button.setFixedHeight(28)
        button.setMinimumWidth(80)
        button.setToolTip("Settings")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button
