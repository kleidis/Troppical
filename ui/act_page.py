from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from init_instances import inst


class ActPage(QWidget):
    def __init__(self):
        super().__init__()
        self.actPage = QWidget()

        actLayout = QVBoxLayout()
        actLayout.setSpacing(2)
        actLayout.setContentsMargins(24, 0, 24, 0)
        self.actPage.setLayout(actLayout)

        headerLayout = QHBoxLayout()
        headerLayout.setSpacing(16)

        self.backButton = QPushButton("Back")
        self.backButton.setFixedSize(80, 28)
        self.backButton.setFont(QFont("Segoe UI", 11))
        headerLayout.addWidget(self.backButton)

        titleLayout = QVBoxLayout()
        titleLayout.setSpacing(4)

        titleLabel = QLabel("<font size='10'>Troppical</font>")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.actLabel = QLabel()
        self.actLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.actLabel.setFont(QFont("Segoe UI", 9))
        self.actLabel.setStyleSheet("color: rgba(255, 255, 255, 0.7);")

        titleLayout.addWidget(titleLabel)
        titleLayout.addWidget(self.actLabel)

        headerLayout.addLayout(titleLayout)
        headerLayout.addStretch()

        actLayout.addLayout(headerLayout)
        actLayout.addSpacing(24)

        self.installButton = self.create_nav_button(
            "Install", "Install the selected emulator"
        )

        self.updateButton = self.create_nav_button(
            "Check for Updates", "Check and install available updates for your emulator"
        )

        self.uninstallButton = self.create_nav_button(
            "Uninstall", "Remove the installed emulator from your system"
        )

        actLayout.addWidget(self.installButton)
        actLayout.addWidget(self.updateButton)
        actLayout.addWidget(self.uninstallButton)
        actLayout.addStretch()

    def create_nav_button(self, text, tooltip):
        button = QPushButton()

        contentLayout = QVBoxLayout()
        contentLayout.setSpacing(8)
        contentLayout.setContentsMargins(30, 13, 30, 13)
        button.setLayout(contentLayout)

        titleLabel = QLabel(text)
        titleLabel.setFont(QFont("Segoe UI", 13))
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
