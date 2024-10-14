
from imports import *
from main import Logic as main
from header import Header

# Finish page
class FinishPage(QWidget):
        def __init__(self):
            super().__init__()
            self.Header = Header.header(self)
            self.finishPage = QWidget()
            ## Layout and groups
            finishLayout = QVBoxLayout()
            self.finishPage.setLayout(finishLayout)
            ## Widgets
            finishLabel = QLabel("<b>Installation Complete!")
            finishLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text horizontally
            finishButton = QPushButton("Finish")
            finishButton.clicked.connect(self.close)
            installAnotherButton = QPushButton("Install another emulator")
            installAnotherButton.clicked.connect(lambda: (
                self.layout.setCurrentIndex(0),
                self.downloadProgressBar.setValue(0),
                self.extractionProgressBar.setValue(0),
                setattr(main, 'install_mode', None),
                setattr(main, 'selection', None)
            ))
            ## Add widgets / layouts
            finishLayout.addLayout(self.Header)  # Add the icon self.header
            finishLayout.addWidget(finishLabel)
            # Create a horizontal layout for the buttons
            buttonLayout = QHBoxLayout()
            buttonLayout.addWidget(finishButton)
            buttonLayout.addWidget(installAnotherButton)
            finishLayout.addLayout(buttonLayout)
