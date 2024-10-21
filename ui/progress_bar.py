from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel
from ui.header import Header

 # Progress bar page
class ProgressBarPage(QWidget):
    def __init__(self):
        super().__init__()
        self.Header = Header.header(self)
        self.progressBarPage = QWidget()
        ## Layout and groups
        progressBarLayout = QVBoxLayout()
        self.progressBarPage.setLayout(progressBarLayout)
        ## Widgets
        self.downloadProgressBar = QProgressBar()
        self.downloadProgressBar.setRange(0, 100)  # Progress bar Widgets
        self.extractionProgressBar = QProgressBar()
        self.extractionProgressBar.setRange(0, 100)
        self.labeldown = QLabel("Downloading: ")
        self.labelext = QLabel("Extracting: ")
        ## Add widgets / layouts
        progressBarLayout.addLayout(self.Header)  # Add the icon self.header
        progressBarLayout.addWidget(self.labeldown)
        progressBarLayout.addWidget(self.downloadProgressBar)
        progressBarLayout.addWidget(self.labelext)
        progressBarLayout.addWidget(self.extractionProgressBar)
