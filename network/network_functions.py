import requests
import os
import subprocess
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtCore import QByteArray, Qt
from init_instances import inst
import sys

class Online():
    databaseUrl = "https://raw.githubusercontent.com/kleidis/Troppical/refs/heads/master/network/troppical-database.json"

    def __init__(self):
        self.troppicalDatabase = self.fetch_data() # Fetch the data from troppical_dataabse JSON
        self.emulatorDatabase = None  # Cache for filtered emulator data

    def fetch_data(self):
        response = requests.get(self.databaseUrl)
        if response.status_code == 200:
            allData = response.json()
            self.troppicalDatabase = [item for item in allData if item.get('emulator_platform') != 'android']
            return self.troppicalDatabase
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    # Fetch and process the main icon of Troppical. Only used by the UI header
    def fetch_and_process_main_icon(self):
        self.mainLogoUrl = "https://raw.githubusercontent.com/kleidis/Troppical/refs/heads/master/icons/assets/Troppical.svg"

        response = requests.get(self.mainLogoUrl)
        if response.status_code == 200:
            imageBytes = response.content
            qimage = QImage.fromData(QByteArray(imageBytes))
            pixmap = QPixmap.fromImage(qimage).scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            return QIcon(pixmap)
        else:
            QMessageBox.critical(None, "Error", f"Failed to fetch icon: {response.status_code}")
            return QIcon()


    def fetch_logos(self):
        self.logos = {}
        for item in self.troppicalDatabase:
            logoUrl = item['emulator_logo']
            response = requests.get(logoUrl)
            if response.status_code == 200:
                self.logos[item['emulator_name']] = response.content
            else:
                QMessageBox.critical(None, "Error", f"Failed to fetch logo for {item['emulator_name']}: {response.status_code}")
        return self.logos

    def get_latest_git_tag(self):
        current_tag = "Local Build"
        home_url = "https://api.github.com/repos/kleidis/Troppical/releases/latest"
        if getattr(sys, 'frozen', False):
            try:
                with open(os.path.join(os.path.dirname(sys.executable), 'version.txt'), 'r') as f:
                    version = f.read().strip()
                    if len(version) == 7 and version[2] == '.' and version.replace('.','').isdigit():
                        current_tag = version
            except:
                pass

        try:
            response = requests.get(home_url)
            if response.status_code == 200:
                latest_tag = response.json()["tag_name"]
                if current_tag != "Local Build" and latest_tag > current_tag:
                    return latest_tag
            else:
                print(f"Failed to get latest GitHub release tag: {response.status_code}")
        except Exception as e:
            print(f"Failed to get latest GitHub release tag: {e}")
        return current_tag

    def filter_emulator_data(self):
        if self.emulatorDatabase is not None:
            return self.emulatorDatabase

        def fetch_icon(logoUrl):
            response = requests.get(logoUrl)
            if response.status_code == 200:
                imageBytes = response.content
                qimage = QImage.fromData(QByteArray(imageBytes))
                pixmap = QPixmap.fromImage(qimage).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                return QIcon(pixmap)
            return QIcon()  # Default icon if fetching fails

        self.emulatorDatabase = {
            item['emulator_name']: {
                'name': item['emulator_name'],
                'system': item['emulator_system'],
                'description': item['emulator_desc'],
                'owner': item['emulator_owner'],
                'repo': item['emulator_repo'],
                'exe_path': item['exe_path'],
                'icon': fetch_icon(item['emulator_logo'])
            }
            for item in self.troppicalDatabase
        }

        return self.emulatorDatabase

    def fetch_releases(self, latest=False):
        releasesUrl = inst.main.releasesUrl
        url = releasesUrl + "/latest" if latest else releasesUrl
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch releases: {response.status_code}")

    def fetch_github_release(self, callTag=None):
        try:
            if callTag == "latest":
                url = f"{inst.main.releasesUrl}/latest"
                response = requests.get(url)
                if response.status_code == 200:
                    release = response.json()
                    return self._filter_windows_assets(release)
            else:
                url = inst.main.releasesUrl
                response = requests.get(url)
                if response.status_code == 200:
                    releases = response.json()
                    if callTag:
                        # Find specific release by tag
                        for release in releases:
                            if release['tag_name'] == callTag:
                                return self._filter_windows_assets(release)
                        return None
                    return releases

            raise Exception(f"Failed to fetch release: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to fetch release information: {str(e)}")
            return None

    def _filter_windows_assets(self, release):
        # TODO: Improve this function
        return [
            asset for asset in release['assets']
            if ('_win' in asset['name'].lower() or 'win' in asset['name'].lower())
            and asset['name'].endswith('.zip')
            and not asset['name'].endswith('.7z')
        ]

# Worker thread used for downlaoding emulators
class DownloadWorker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.url = None
        self.dest = None

    def set_task(self, url, dest):
        self.url = url
        self.dest = dest

    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            totalSize = int(response.headers.get('content-length', 0))
            if totalSize == 0:
                print("The content-length of the response is zero.")
                return

            downloadedSize = 0
            with open(self.dest, 'wb') as file:
                for data in response.iter_content(1024):
                    downloadedSize += len(data)
                    file.write(data)
                    progressPercentage = (downloadedSize / totalSize) * 100
                    self.progress.emit(int(progressPercentage))
            self.finished.emit()
        except Exception as e:
            QMessageBox.critical(None, "Error", "Error during download.")
            self.finished.emit()

