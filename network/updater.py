import os
import sys
import tempfile
import requests
from PyQt6.QtWidgets import QProgressDialog, QMessageBox
from PyQt6.QtCore import QThread
from version import version
from init_instances import inst


class Updater:
    def check_for_update(self):
        currentVersion = version
        update = inst.online.get_git_tag()[0]

        if update > currentVersion:
            reply = QMessageBox.question(
                None,
                "Update Available",
                f"Version {update} is available. Current version is {currentVersion}. Would you like to update?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                return self.download_update()
            return False
        return False

    def download_update(self):
        try:

            assets = inst.online.get_git_tag()[1]
            exeAsset = next(
                (asset for asset in assets if asset["name"] == "troppical.exe"), None
            )

            if not exeAsset:
                QMessageBox.critical(
                    None, "Error", "No executable found in latest release"
                )
                return False

            tempExe = os.path.join(tempfile.gettempdir(), "troppical.exe.new")

            progress = QProgressDialog("Downloading update...", "Cancel", 0, 100)
            progress.setWindowTitle("Updating Troppical")
            progress.setMinimumDuration(0)
            progress.setModal(True)

            self.thread = QThread()
            self.worker = inst.download
            self.worker.set_task(exeAsset["browser_download_url"], tempExe)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.progress.connect(progress.setValue)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(progress.close)
            self.thread.finished.connect(self.finish_update)
            self.thread.start()
            progress.exec()

            if progress.wasCanceled():
                self.thread.quit()
                if os.path.exists(tempExe):
                    os.remove(tempExe)
                return False

            return True

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Update failed: {e}")
            return False

    def finish_update(self):
        try:
            currentExe = sys.executable
            tempExe = os.path.join(tempfile.gettempdir(), "troppical.exe.new")
            if not os.path.exists(tempExe):
                return

            batchContent = f"""@echo off
:wait
tasklist /FI "IMAGENAME eq {os.path.basename(currentExe)}" 2>NUL | find /I /N "{os.path.basename(currentExe)}" >NUL
if "%ERRORLEVEL%"=="0" (
    timeout /t 1 /nobreak >nul
    goto wait
)
move /Y "{tempExe}" "{currentExe}" >nul
del "%~f0"
"""
            batchFile = os.path.join(tempfile.gettempdir(), "troppical_update.bat")
            with open(batchFile, "w") as f:
                f.write(batchContent)

            QMessageBox.information(
                None,
                "Update Ready",
                "Update has been downloaded. The application will close now.\nPlease restart Troppical after the update is complete.",
                QMessageBox.StandardButton.Ok,
            )

            os.startfile(batchFile)
            sys.exit(0)

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to complete update: {e}")
