from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog, QInputDialog
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
import requests
import os
import subprocess
import sys
from zipfile import ZipFile
import shutil
import tempfile
from icons import styledark_rc
import win32com.client
import winreg
from pathlib import Path
from init_instances import inst

class Main():
    def __init__(self):
        # Init variables
        self.emulator = None  # Keep track of the selected emulator
        self.download_thread = None
        self.download_worker = None
        self.reg_result = None

    def initialize_app(self):
        version = "Refactor"
        app = QApplication(sys.argv)
        ui_main = inst.ui
        ui_main.show()
        sys.exit(app.exec())

    def update_reg_result(self):
        self.reg_result = self.checkreg()
        return self.reg_result

    # Set which emulator to use for the installer depeanding on the selected emulator
    def set_emulator(self):
        selected_item = inst.sel.emulatorTreeWidget.currentItem()
        if not selected_item or not selected_item.parent():
            QMessageBox.warning(inst.ui, "Selection Error", "Please select an emulator.")
            return False

        emulator_name = selected_item.text(0)
        if self.emulator != emulator_name:
            # Clear previous emulator settings
            inst.bar.labeldown.setText("Downloading: ")
            inst.bar.labelext.setText("Extracting: ")
            inst.act.actLabel.setText("")

            self.emulator = emulator_name

            emulator_data = inst.online.emulator_database

            # Construct the releases URL
            selected_emulator = next((em for em in emulator_data.values() if em['name'] == self.emulator), None)
            if selected_emulator:
                owner = selected_emulator['owner']
                repo = selected_emulator['repo']
                self.releases_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

        installed_emulator = "Not Installed" if self.reg_result is None else self.reg_result[1]
        inst.install.installationPathLineEdit.setText(os.path.join(os.environ['LOCALAPPDATA'], self.emulator))
        inst.bar.labeldown.setText(f"Downloading: {self.emulator}")
        inst.bar.labelext.setText(f"Extracting: {self.emulator}")
        inst.act.actLabel.setText(
            f'<big>Your currently selected emulator is <b>{self.emulator}</b> and current version is <b>{installed_emulator}</b>.</big>'
        )

        inst.ui.disable_qt_buttons_if_installed()
        return True # To avoid the function from switching index even on non-select item

    # Select installation path function
    def InstallPath(self):
        current_path = inst.install.installationPathLineEdit.text()
        selected_directory = QFileDialog.getExistingDirectory(inst.install, "Select Installation Directory", current_path)

        if selected_directory:
            install_dir = os.path.join(selected_directory, self.emulator)
            self.Install_Dir = os.path.normpath(install_dir)
            inst.install.installationPathLineEdit.setText(self.Install_Dir)

        return self.Install_Dir

    # Add the various version to the selection combobox
    def Add_releases_to_combobox(self):
        self.releases = inst.online.fetch_releases()

        # Clear the combo box before adding new items
        inst.install.installationSourceComboBox.clear()

        for release in self.releases:
            inst.install.installationSourceComboBox.addItem(release['tag_name'])

    # Updater function
    def emulator_updater(self):
        installed_emulator = self.reg_result[1]
        latest_release = inst.online.fetch_releases(latest=True)
        latest_tag = latest_release['tag_name']

        # Check for specific emulators that use a rolling-release
        if self.emulator in ['Vita3K', 'NooDS']: # TODOL Add this type to json database
            reply = QMessageBox.question(inst.ui, "Rolling-Release Emulator Detected", f"{self.emulator} uses rolling-releases instead of numbered releases. This means that the latest version may not be the one you have installed (We cannot detect the version). Would you like to proceed with the download anyway?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.install_mode = "Update"
                inst.ui.qt_index_switcher(4)
                self.Prepare_Download()
                return
            else:
                pass

        # TODO: Improve tag comparing
        if latest_tag > installed_emulator:
            reply = QMessageBox.question(inst.ui, "Update Found", "Would you like to update " + self.emulator + " to " +  latest_tag + "?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.install_mode = "Update"
                inst.ui.qt_index_switcher(4)
                self.Prepare_Download()
            else:
                pass
        else:
            QMessageBox.information(inst.ui, "No Update Found", f"You are up to date with the latest version of {self.emulator}", QMessageBox.StandardButton.Ok)

    # Preparing which file to downlaod
    def Prepare_Download(self):
        print (self.install_mode)
        if self.reg_result is not None:
            UpdateChannelValue = self.reg_result[1]
        else:
            UpdateChannelValue = None

        self.selection = inst.install.installationSourceComboBox.currentText()

        # Determine the installation path
        temp_file = tempfile.NamedTemporaryFile(delete=False).name
        if self.install_mode == "Install":
            self.installationPath = inst.install.installationPathLineEdit.text()
        elif self.install_mode == "Update":
            self.installationPath = self.reg_result[0]
        os.makedirs(self.installationPath, exist_ok=True)

        if self.install_mode == "Install":
            response = requests.get(self.releases_url)
            releases = response.json()
            for release in releases:
                if release['tag_name'] == self.selection:
                    windows_assets = [asset for asset in release['assets'] if ('_win' in asset['name'].lower() or 'win' in asset['name'].lower() or 'xenia' in asset['name'].lower()) and asset['name'].endswith('.zip') and not asset['name'].endswith('.7z')]
                    if len(windows_assets) > 1:
                        options = "\n".join([f"{idx + 1}: {asset['name']}" for idx, asset in enumerate(windows_assets)])
                        choice, ok = QInputDialog.getItem(inst.ui, "Select Version", "Multiple Windows versions found. Please select one:\n" + options, [asset['name'] for asset in windows_assets], 0, False)
                        if ok:
                            self.selected_asset = next(asset for asset in windows_assets if asset['name'] == choice)
                            self.selected_asset_name = self.selected_asset['name']
                            print(self.selected_asset_name)
                            self.target_download = self.selected_asset['browser_download_url']
                            self.url = self.target_download  # url for the download thread
                            self.start_download_thread(self.url, temp_file)
                            self.update_reg()
                        else:
                            sys.exit("No release selected. Exiting.")
                    elif len(windows_assets) == 1:
                        self.selected_asset_name = windows_assets[0]['name']
                        self.target_download = windows_assets[0]['browser_download_url']
                        print(self.target_download)
                        self.url = self.target_download  # url for the download thread
                        self.start_download_thread(self.url, temp_file)
                        self.update_reg()
                    else:
                        QMessageBox.critical(inst.ui, "Error", f"No suitable Windows download found for {self.emulator} {self.selection}. Please try another release.")
                        inst.ui.qt_index_switcher(3)
        elif self.install_mode == "Update":
            response = requests.get(self.releases_url + "/latest")
            latest_release = response.json()
            windows_assets = [asset for asset in latest_release['assets'] if ('_win' in asset['name'].lower() or 'win' in asset['name'].lower()) and asset['name'].endswith('.zip') and not asset['name'].endswith('.7z')]
            if windows_assets:
                if len(windows_assets) > 1:
                    options = "\n".join([f"{idx + 1}: {asset['name']}" for idx, asset in enumerate(windows_assets)])
                    choice, ok = QInputDialog.getItem(inst.ui, "Select Version", "Multiple Windows versions found. Please select one:\n" + options, [asset['name'] for asset in windows_assets], 0, False)
                    if ok:
                        latest_asset = next(asset for asset in windows_assets if asset['name'] == choice)
                    else:
                        sys.exit("No release selected. Exiting.")
                else:
                    latest_asset = windows_assets[0]

                self.target_download = latest_asset['browser_download_url']
                self.url = self.target_download  # url for the download thread
                print(f"Starting download for: {self.url}")

                # Ensure the download worker is a fresh instance
                self.start_download_thread(self.url, temp_file)

                self.selection = latest_release['tag_name']
                self.update_reg()
            else:
                QMessageBox.critical(inst.ui, "Error", f"No suitable Windows download found for {self.emulator} in the latest release. Please try another release or check for updates.")
    # Download function
    def start_download_thread(self, url, dest):
        if self.download_thread is not None:
            self.download_thread.quit()
            self.download_thread.wait()

        self.download_thread = QThread()
        self.download_worker = inst.download
        self.download_worker.set_task(url, dest)
        self.download_worker.moveToThread(self.download_thread)
        self.download_worker.progress.connect(inst.bar.downloadProgressBar.setValue)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_thread.started.connect(self.download_worker.run)
        self.download_thread.start()
    def on_download_finished(self):
        self.extract_and_install(self.download_worker.dest, self.installationPath)
        self.download_thread.quit()
        self.download_thread.wait()
        self.download_thread = None
        self.download_worker = None

    # Extract and install function
    def extract_and_install(self, temp_file, extract_to):
        zip_file_path = f"{temp_file}.zip"

        # Handle multiple asset versions
        if self.install_mode == "Update" and self.reg_result is not None:
            current_asset = self.reg_result[2]
            new_asset = self.target_download.split('/')[-1]

            if current_asset != new_asset:
                reply = QMessageBox.question(
                    inst.ui,
                    "Multiple Asset Versions Detected",
                    f"The version you're installing might be different from the currently installed version. "
                    "Would you like to delete all existing emulator [program files] files before Update (Yes RECOMMENDED)  or just replace them (No)?\n\n",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    try:
                        if os.path.exists(extract_to):
                            shutil.rmtree(extract_to)
                    except Exception as e:
                        QMessageBox.critical(inst.ui, "Error", f"Failed to delete existing installation: {str(e)}")
                        return

        try:
            os.rename(temp_file, zip_file_path)
            self.temp_extract_folder = tempfile.mkdtemp()

            try:
                with ZipFile(zip_file_path, 'r') as emu_zip:
                    # Extract all files first
                    emu_zip.extractall(self.temp_extract_folder)

                    # Handle nested zips
                    for nested_zip in [f for f in emu_zip.namelist() if f.endswith('.zip')]:
                        nested_path = os.path.join(self.temp_extract_folder, nested_zip)
                        with ZipFile(nested_path, 'r') as nested:
                            nested.extractall(self.temp_extract_folder)
                        os.remove(nested_path)
            except Exception as e:
                QMessageBox.critical(inst.ui, "Extraction Error", f"Failed to extract files: {str(e)}")
                return
            finally:
                os.remove(zip_file_path)
            self.move_files(self.installationPath)
        except Exception as e:
            QMessageBox.critical(inst.ui, "File Error", f"Failed to process downloaded file: {str(e)}")
            return

    def move_files(self, extract_to):
        try:
            # Find executable directory
            exe_root = next(
                (root for root, _, files in os.walk(self.temp_extract_folder)
                if any(file.endswith('.exe') for file in files)),
                self.temp_extract_folder
            )

            os.makedirs(extract_to, exist_ok=True)

            try:
                items = os.listdir(exe_root)
                for idx, item in enumerate(items):
                    try:
                        src = os.path.join(exe_root, item)
                        dest = os.path.join(extract_to, item)

                        if os.path.isdir(src):
                            shutil.copytree(src, dest, dirs_exist_ok=True)
                        else:
                            shutil.copy2(src, dest)

                        # Update extraction progress
                        progress = int((idx + 1) / len(items) * 100)
                        inst.bar.extractionProgressBar.setValue(progress)
                    except Exception as e:
                        QMessageBox.warning(inst.ui, "Copy Warning", f"Failed to copy {item}: {str(e)}")
                        continue
            except Exception as e:
                QMessageBox.critical(inst.ui, "Installation Error", f"Failed to install files: {str(e)}")
                return
            finally:
                shutil.rmtree(self.temp_extract_folder, ignore_errors=True)

            self.installation_complete()
        except Exception as e:
            QMessageBox.critical(inst.ui, "Installation Error", f"Failed to complete installation: {str(e)}")
            return

    # Install is complete
    def installation_complete(self):
        inst.bar.extractionProgressBar.setValue(100)

        # Fetch the executable path from the troppical_api data
        emulator_data = inst.online.emulator_database.get(self.emulator, {})
        exe_name = emulator_data.get('exe_path', '')
        executable_path = os.path.normpath(os.path.join(inst.install.installationPathLineEdit.text(), exe_name))
        print(executable_path)

        if not exe_name:
            QMessageBox.critical(inst.ui, "Error", f"Executable path not found for emulator: {self.emulator}")
            return

        if inst.install.desktopShortcutCheckbox.isChecked():
            self.define_shortcut(executable_path, 'desktop')
        if inst.install.startMenuShortcutCheckbox.isChecked():
            self.define_shortcut(executable_path, 'start_menu')
        inst.ui.qt_index_switcher(5)

    # Function to check the reg values
    def checkreg(self):
        try:
            self.registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}", 0, winreg.KEY_READ)
            self.instValue, regtype = winreg.QueryValueEx(self.registry_key, 'Install_Dir')
            self.updatevalue, regtype = winreg.QueryValueEx(self.registry_key, 'Version')
            self.asset_version, regtype = winreg.QueryValueEx(self.registry_key, 'Asset_version')
            winreg.CloseKey(self.registry_key)
            return self.instValue, self.updatevalue, self.asset_version
        except FileNotFoundError:
            pass
    # Function to create the reg values
    def update_reg (self):
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
        self.registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}", 0,
                                        winreg.KEY_WRITE)
        if self.install_mode == "Install":
            winreg.SetValueEx(self.registry_key, 'Install_Dir', 0, winreg.REG_SZ, inst.install.installationPathLineEdit.text())
            winreg.SetValueEx(self.registry_key, 'Asset_version', 0, winreg.REG_SZ, self.selected_asset_name)
        winreg.SetValueEx(self.registry_key, 'Version', 0, winreg.REG_SZ, self.selection)
        winreg.CloseKey(self.registry_key)

    # Function to create the shortcuts
    def define_shortcut(self, target, location_type):
        if location_type == 'desktop':
            path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        elif location_type == 'start_menu':
            path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')

        filename = f'{self.emulator}.lnk'
        shortcut_path = os.path.join(path, filename)

        # Verify the target exists
        if not os.path.exists(target):
            QMessageBox.critical(inst.ui, "Error", f"Shortcut target does not exist: {target}")
            return

        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.Description = ""
            shortcut.Arguments = ""
            shortcut.IconLocation = target  # You can customize this if needed
            shortcut.save()
        except Exception as e:
            QMessageBox.critical(inst.ui, "Error", f"Failed to create shortcut: {e}")

    # Uninstall function
    def uninstall(self):
        if self.reg_result[0] is not None:
            # Paths to the shortcuts
            desktopshortcut = os.path.join(os.environ['USERPROFILE'], 'Desktop', f'{self.emulator}.lnk')
            startmenushortcut = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', f'{self.emulator}.lnk')

            reply = QMessageBox.question(inst.ui, "Uninstall", f"Are you sure you want to uninstall {self.emulator} located on {self.instValue}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
            else:
                # Remove the shortcut and the, DIR and REG keys
                if os.path.exists(desktopshortcut):
                    os.remove(desktopshortcut)
                if os.path.exists(startmenushortcut):
                    os.remove(startmenushortcut)
                dirpath = Path(self.instValue)
                if dirpath.exists() and dirpath.is_dir():
                    shutil.rmtree(dirpath)
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
                    QMessageBox.information(inst.ui, "Uninstall", f"{self.emulator} has been successfully uninstalled.")
                    self.emulator = None
                    inst.ui.qt_index_switcher(1)
                else:
                    QMessageBox.critical(inst.ui, "Error", "The directory might have been moved or deleted. Please reinstall the program.")
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
                    inst.ui.updateButton.setEnabled(False)
                    inst.ui.uninstallButton.setEnabled(False)
                    inst.ui.installButton.setEnabled(True)
        else:
            QMessageBox.critical(inst.ui, "Error",("Failed to read the registry key. Try and reinstall again!"))
            inst.ui.qt_index_switcher(2)

if __name__ == "__main__":
    main = Main()
    main.initialize_app()

