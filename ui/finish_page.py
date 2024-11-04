from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from init_instances import inst

# Finish page
class FinishPage(QWidget):
        def __init__(self):
            super().__init__()
            self.finishPage = QWidget()

            finishLayout = QVBoxLayout()
            finishLayout.setContentsMargins(24, 0, 24, 0)
            self.finishPage.setLayout(finishLayout)

            # Add header
            finishLayout.addLayout(inst.header.header())

            # Center content vertically
            finishLayout.addStretch(1)

            # Success icon and message
            successLabel = QLabel("✓")
            successLabel.setFont(QFont("Segoe UI", 72))
            successLabel.setStyleSheet("color: #E81123;")
            successLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            finishLayout.addWidget(successLabel)
            finishLabel = QLabel("Installation Complete!")
            finishLabel.setFont(QFont("Segoe UI", 32))
            finishLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            finishLayout.addWidget(finishLabel)
            descLabel = QLabel("The emulator has been successfully installed on your system.")
            descLabel.setFont(QFont("Segoe UI", 13))
            descLabel.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
            descLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            finishLayout.addWidget(descLabel)

            # Add equal stretch to center content
            finishLayout.addStretch(1)

            buttonLayout = QHBoxLayout()
            buttonLayout.setSpacing(8)

            buttonLayout.addStretch()
            self.installAnotherButton = QPushButton("Install another emulator")
            self.installAnotherButton.setFixedHeight(32)
            self.installAnotherButton.setFont(QFont("Segoe UI", 11))
            buttonLayout.addWidget(self.installAnotherButton)
            self.finishButton = QPushButton("Finish")
            self.finishButton.setFixedSize(80, 32)
            self.finishButton.setFont(QFont("Segoe UI", 11))
            buttonLayout.addWidget(self.finishButton)
            finishLayout.addLayout(buttonLayout)
