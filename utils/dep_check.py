import os
import sys
import subprocess
from PyQt6.QtWidgets import QMessageBox
import webbrowser


def check_7zip_installed():
    try:
        result = subprocess.run(["7z", "--help"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        reply = QMessageBox.critical(
            None,
            "7-Zip Required",
            "7-Zip is required but not found. Would you like to open the 7-Zip download page?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            webbrowser.open("https://7-zip.org/download.html")
        return False


def get_7zip_path():
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        bundled7zip = os.path.join(os.path.dirname(sys.executable), "7z.exe")
    else:
        # Running as script
        bundled7zip = os.path.join(os.path.dirname(__file__), "7z.exe")

    if os.path.exists(bundled7zip):
        return bundled7zip

    try:
        result = subprocess.run(["7z", "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            return "7z"
    except FileNotFoundError:
        pass

    return None
