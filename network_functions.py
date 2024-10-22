import requests
import os
import subprocess
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtCore import QByteArray, Qt

class Online():
    def __init__(self):
        self.troppical_database = self.fetch_data() # Fetch the data from troppical_dataabse JSON
        self.emulator_database = None  # Cache for filtered emulator data

    def fetch_data(self):
        url = "https://raw.githubusercontent.com/kleidis/test/main/troppical-data.json"
        response = requests.get(url)
        if response.status_code == 200:
            all_data = response.json()
            self.troppical_database = [item for item in all_data if item.get('emulator_platform') != 'android']
            return self.troppical_database
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def fetch_logos(self):
        self.logos = {}
        for item in self.troppical_database:
            logo_url = item['emulator_logo']
            response = requests.get(logo_url)
            if response.status_code == 200:
                self.logos[item['emulator_name']] = response.content
            else:
                print(f"Failed to fetch logo for {item['emulator_name']}: {response.status_code}")
        return self.logos

    def get_latest_git_tag(self):
        tag = "1.0"
        github_token = os.getenv("GITHUB_TOKEN", "")
        try:
            command = f"GH_TOKEN={github_token} gh release list --limit 1 --json tagName --jq '.[0].tagName'"
            process = subprocess.Popen(['bash', '-c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if process.returncode == 0:
                tag = out.decode('utf-8').strip()
                if tag.startswith("v"):
                    tag = tag[1:]
            else:
                print(f"Failed to get latest GitHub release tag: {err.decode('utf-8')}")
        except Exception as e:
            print(f"Failed to get latest GitHub release tag: {e}")
        return tag

    def filter_emulator_data(self):
        if self.emulator_database is not None:
            return self.emulator_database

        emulator_data = {}
        for troppical_api_data in self.troppical_database:
            emulator_name = troppical_api_data['emulator_name']
            emulator_system = troppical_api_data['emulator_system']
            emulator_desc = troppical_api_data['emulator_desc']
            emulator_owner = troppical_api_data['emulator_owner']
            emulator_repo = troppical_api_data['emulator_repo']
            exe_path = troppical_api_data['exe_path']
            logo_url = troppical_api_data['emulator_logo']

            # Fetch the logo
            response = requests.get(logo_url)
            if response.status_code == 200:
                image_bytes = response.content
                qimage = QImage.fromData(QByteArray(image_bytes))
                pixmap = QPixmap.fromImage(qimage).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                icon = QIcon(pixmap)
            else:
                icon = QIcon()  # Default icon if fetching fails

            emulator_data[emulator_name] = {
                'name': emulator_name,
                'system': emulator_system,
                'description': emulator_desc,
                'owner': emulator_owner,
                'repo': emulator_repo,
                'exe_path': exe_path,
                'icon': icon
            }

        self.emulator_database = emulator_data  # Store the data for later use throughout the codebase
        return emulator_data


# Download Worker class to download the files
class DownloadWorker(QThread):
    progress = pyqtSignal(int)

    def __init__(self, url, dest):
        super().__init__()
        self.url = url
        self.dest = dest


    @pyqtSlot()
    def do_download(self):
        try:
            response = requests.get(self.url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            if total_size == 0:
                print("The content-length of the response is zero.")
                return

            downloaded_size = 0
            with open(self.dest, 'wb') as file:
                for data in response.iter_content(1024):
                    downloaded_size += len(data)
                    file.write(data)
                    progress_percentage = (downloaded_size / total_size) * 100
                    self.progress.emit(int(progress_percentage))
            self.finished.emit()
        except Exception as e:
            QMessageBox.critical(self, "Error",("Error doing download."))
            self.finished.emit()
