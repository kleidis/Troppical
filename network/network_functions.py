import requests
import os
import subprocess
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtCore import QByteArray, Qt

class Online():
    database_url = "https://raw.githubusercontent.com/kleidis/test/main/troppical-data.json"

    def __init__(self):
        self.troppical_database = self.fetch_data() # Fetch the data from troppical_dataabse JSON
        self.emulator_database = None  # Cache for filtered emulator data

    def fetch_data(self):
        response = requests.get(self.database_url)
        if response.status_code == 200:
            all_data = response.json()
            self.troppical_database = [item for item in all_data if item.get('emulator_platform') != 'android']
            return self.troppical_database
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    # Fetch and process the main icon of Troppical. Only used by the UI header
    def fetch_and_process_main_icon(self):
        self.main_logo_url = "https://raw.githubusercontent.com/kleidis/Troppical/refs/heads/master/icons/assets/Troppical.svg"

        response = requests.get(self.main_logo_url)
        if response.status_code == 200:
            image_bytes = response.content
            qimage = QImage.fromData(QByteArray(image_bytes))
            pixmap = QPixmap.fromImage(qimage).scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            return QIcon(pixmap)
        else:
            QMessageBox.critical(None, "Error", f"Failed to fetch icon: {response.status_code}")
            return QIcon()


    def fetch_logos(self):
        self.logos = {}
        for item in self.troppical_database:
            logo_url = item['emulator_logo']
            response = requests.get(logo_url)
            if response.status_code == 200:
                self.logos[item['emulator_name']] = response.content
            else:
                QMessageBox.critical(None, "Error", f"Failed to fetch logo for {item['emulator_name']}: {response.status_code}")
        return self.logos

    # TODO: Improve tihs  function, currently it's not used
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

        def fetch_icon(logo_url):
            response = requests.get(logo_url)
            if response.status_code == 200:
                image_bytes = response.content
                qimage = QImage.fromData(QByteArray(image_bytes))
                pixmap = QPixmap.fromImage(qimage).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                return QIcon(pixmap)
            return QIcon()  # Default icon if fetching fails

        self.emulator_database = {
            item['emulator_name']: {
                'name': item['emulator_name'],
                'system': item['emulator_system'],
                'description': item['emulator_desc'],
                'owner': item['emulator_owner'],
                'repo': item['emulator_repo'],
                'exe_path': item['exe_path'],
                'icon': fetch_icon(item['emulator_logo'])
            }
            for item in self.troppical_database
        }

        return self.emulator_database

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
            QMessageBox.critical(None, "Error", "Error during download.")
            self.finished.emit()
