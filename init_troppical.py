# Depacrated. Will be remvoed if possible

import sys
import os
import requests
import tempfile
import subprocess
from zipfile import ZipFile
from PyQt6.QtWidgets import QApplication, QMessageBox
import shutil

def download_and_launch():
    url = 'https://nightly.link/kleidis/Troppical/workflows/build/master/troppical-windows.zip'
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Create a temporary file for the ZIP
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
            for chunk in response.iter_content(chunk_size=8192):
                temp_zip.write(chunk)

        # Extract the ZIP file
        with ZipFile(temp_zip.name, 'r') as zip_ref:
            temp_dir = tempfile.mkdtemp()
            zip_ref.extractall(temp_dir)

        exe_path = None
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith('.exe'):
                    exe_path = os.path.join(root, file)
                    break
            if exe_path:
                break

        if not exe_path:
            QMessageBox.critical(None, "Execution Error", "Executable file not found in the archive.")
            return False

        # Display launching message
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("Troppical is initializing...")
        msg_box.show()
        QApplication.processEvents()

        # Launch the downloaded executable
        process = subprocess.Popen([exe_path], close_fds=True)
        msg_box.close()

        process.wait()

        # Clean up the temporary files and directory
        os.unlink(temp_zip.name)
        shutil.rmtree(temp_dir)

        return True
    else:
        QMessageBox.critical(None, "Download Error", "Failed to download the update.")
        return False

def main():
    app = QApplication(sys.argv)
    success = download_and_launch()
    if success:
        QMessageBox.information(None, "Bye!", "Thanks for using Troppical.")
    app.quit()

if __name__ == '__main__':
    main()
    sys.exit(0)
