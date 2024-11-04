from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QPushButton, QHBoxLayout, QLineEdit, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from init_instances import inst
import os

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.settingsPage = QWidget()
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.setContentsMargins(24, 0, 24, 0)
        self.settingsPage.setLayout(self.settingsLayout)

        self.add_header()

        self.add_settings_section("General", [
            {
                "type": "checkbox",
                "id": "launchAsAdminCheckbox",
                "title": "Launch as administrator",
                "description": "Run Troppical with elevated privileges"
            },
            {
                "type": "path",
                "id": "defaultInstallPath",
                "title": "Default installation path",
                "description": "Base directory for emulator installations",
                "default": os.path.join(os.environ['LOCALAPPDATA'])
            }
            # You can add more settings here as dictonaries
        ])

        self.settingsLayout.addStretch()
        self.add_apply_button()

    def add_header(self):
        """Add the settings page header"""
        titleLayout = QVBoxLayout()
        titleLayout.setSpacing(4)

        settingsLabel = QLabel("<font size='10'>Settings</font>")
        settingsLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        descLabel = QLabel("Configure Troppical's behavior")
        descLabel.setFont(QFont("Segoe UI", 9))
        descLabel.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        descLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        titleLayout.addWidget(settingsLabel)
        titleLayout.addWidget(descLabel)
        self.settingsLayout.addLayout(titleLayout)
        self.settingsLayout.addSpacing(24)

    def add_settings_section(self, title, settings):
        sectionLabel = QLabel(title)
        sectionLabel.setFont(QFont("Segoe UI", 16))
        self.settingsLayout.addWidget(sectionLabel)
        self.settingsLayout.addSpacing(8)

        # This is where you add the settings
        for setting in settings:
            if setting["type"] == "checkbox":
                self.add_checkbox_setting(setting)
            elif setting["type"] == "path":
                self.add_path_setting(setting)
            # Will add more setting types here (toggle, dropdown, etc. and so on)

        self.settingsLayout.addSpacing(16)

    def add_checkbox_setting(self, setting):
        checkbox = QCheckBox(setting["title"])
        checkbox.setFont(QFont("Segoe UI", 11))

        setattr(self, setting["id"], checkbox)  # This ensures the attribute exists

        description = QLabel(setting["description"])
        description.setFont(QFont("Segoe UI", 9))
        description.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        description.setContentsMargins(24, 0, 0, 0)

        self.settingsLayout.addWidget(checkbox)
        self.settingsLayout.addWidget(description)
        self.settingsLayout.addSpacing(16)

    def add_path_setting(self, setting):

        titleLabel = QLabel(setting["title"])
        titleLabel.setFont(QFont("Segoe UI", 11))

        pathLayout = QHBoxLayout()
        pathLayout.setSpacing(8)

        pathInput = QLineEdit(setting.get("default", ""))
        pathInput.setFont(QFont("Segoe UI", 11))
        setattr(self, setting["id"], pathInput)

        browseButton = QPushButton("Browse")
        browseButton.setFixedSize(80, 32)
        browseButton.setFont(QFont("Segoe UI", 11))
        browseButton.clicked.connect(lambda: self.browse_path(pathInput))

        pathLayout.addWidget(pathInput)
        pathLayout.addWidget(browseButton)

        description = QLabel(setting["description"])
        description.setFont(QFont("Segoe UI", 9))
        description.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        description.setContentsMargins(24, 0, 0, 0)

        self.settingsLayout.addWidget(titleLabel)
        self.settingsLayout.addLayout(pathLayout)
        self.settingsLayout.addWidget(description)
        self.settingsLayout.addSpacing(16)
    def browse_path(self, pathInput):
        currentPath = pathInput.text()
        selectedDirectory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            currentPath
        )
        if selectedDirectory:
            if not inst.main.check_admin(selectedDirectory):
                pathInput.setText(selectedDirectory)

    def add_apply_button(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        self.applyButton = QPushButton("Apply")
        self.applyButton.setFixedSize(80, 32)
        self.applyButton.setFont(QFont("Segoe UI", 11))
        buttonLayout.addWidget(self.applyButton)
        self.settingsLayout.addLayout(buttonLayout)