from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from init_instances import inst

# Finish page
class FinishPage(QWidget):
        def __init__(self):
            super().__init__()
            self.finishPage = QWidget()
            ## Layout and groups
            finishLayout = QVBoxLayout()
            self.finishPage.setLayout(finishLayout)
            ## Widgets
            finishLabel = QLabel("<b>Installation Complete!")
            finishLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text horizontally
            self.finishButton = QPushButton("Finish")
            self.installAnotherButton = QPushButton("Install another emulator")
            ## Add widgets / layouts
            finishLayout.addLayout(inst.header.header())
            finishLayout.addWidget(finishLabel)
            # Create a horizontal layout for the buttons
            buttonLayout = QHBoxLayout()
            buttonLayout.addWidget(self.finishButton)
            buttonLayout.addWidget(self.installAnotherButton)
            finishLayout.addLayout(buttonLayout)
