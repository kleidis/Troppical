from imports import *
from ui_init import *

class Online:
    def init (self):
        self.troppical_database = self.fetch_data()

    def fetch_data(self):
        url = "https://raw.githubusercontent.com/kleidis/test/main/troppical-data.json"
        response = requests.get(url)
        if response.status_code == 200:
            all_data = response.json()
            self.troppical_database = [item for item in all_data if item.get('emulator_platform') != 'android']
            return self.troppical_database
        else:
            print("Failed to fetch data:", response.status_code)

    def get_latest_git_tag():
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

class Logic:
    def __init__(self):
        self.regvalue = None
        self.install_mode = None
        self.emulator = None

    # Set which emulator to use for the installer depeanding on the selected emulator
    def set_emulator(self):
        selected_item =  MainWindow.instances().selection_page.emulatorTreeWidget.currentItem()
        print (selected_item)
        if not selected_item or not selected_item.parent():
            QMessageBox.warning(SelectionPage.window, "Selection Error", "Please select an emulator.")
            print ("Please select an emulator.")
            return

        emulator_name = selected_item.text(0)
        if self.emulator != emulator_name:
            # Clear previous emulator settings
            qtui.labeldown.setText("Downloading: ")
            qtui.labelext.setText("Extracting: ")
            qtui.welcomerLabel.setText("")

            # Set new emulator
            self.emulator = emulator_name

        for selected_emulator in self.troppical_api:
            if selected_emulator['emulator_name'] == self.emulator:
                self.releases_url = f"https://api.github.com/repos/{selected_emulator['emulator_owner']}/{selected_emulator['emulator_repo']}/releases"

        # Update UI components with new emulator settings
        reg_result = self.checkreg()
        installed_emulator = "Not Installed" if reg_result is None else reg_result[1]
        qtui.installationPathLineEdit.setText(os.path.join(os.environ['LOCALAPPDATA'], self.emulator))
        qtui.labeldown.setText("Downloading: " + self.emulator)
        qtui.labelext.setText("Extracting: " + self.emulator)
        qtui.welcomerLabel.setText(f'<big>Your currently selected emulator is <b>{self.emulator}</b> and current version is <b>{installed_emulator}</b>.</big>')

        print (self.emulator)
        self.checkreg()
        self.disable_qt_buttons_if_installed()
        qtui.layout.setCurrentIndex(1)

    # Disable buttons depanding on if it the program is already installed
    def disable_qt_buttons_if_installed(self):
        regvalue = self.checkreg()
        if regvalue is None:
            qtui.installButton.setEnabled(True)
            qtui.updateButton.setEnabled(False)
            qtui.uninstallButton.setEnabled(False)
        else:
            qtui.installButton.setEnabled(False)
            qtui.updateButton.setEnabled(True)
            qtui.uninstallButton.setEnabled(True)

    # Button clinking function
    def qt_button_click(self):
        button = qtui.sender()
        if button is qtui.installButton:
            self.install_mode = "Install"
            qtui.layout.setCurrentIndex(2)
            self.Add_releases_to_combobox()
        elif button is qtui.updateButton:
            self.emulator_updates()
        elif button is qtui.uninstallButton:
            self.install_mode = "Uninstall" # Unused for now
            self.uninstall()
        if button is qtui.install_emu_button:
            qtui.layout.setCurrentIndex(3)
            self.Prepare_Download()
        if button is qtui.backButton:
            current_index = qtui.layout.currentIndex()
            if current_index > 0:
                qtui.layout.setCurrentIndex(current_index - 1)
        return self.install_mode

    # Select installation path function
    def InstallPath(self):
        self.Install_Dir = qtui.installationPathLineEdit.text()
        selectedDirectory = QFileDialog.getExistingDirectory(qtui, "Select Installation Directory", qtui.installationPathLineEdit.text())
        # Check if a directory was selected
        if selectedDirectory:
        # Set Emulator name to the selected directory path
            self.Install_Dir = os.path.join(selectedDirectory, self.emulator)
            qtui.installationPathLineEdit.setText(self.Install_Dir)
        return self.Install_Dir

    # Add the various version to the selection combobox
    def Add_releases_to_combobox(self):
        print (self.releases_url)
        response = requests.get(self.releases_url)
        self.releases = response.json()[:5]

        # Clear the combo box before adding new items
        qtui.installationSourceComboBox.clear()

        # Remove or add items based on the emulator
        for release in self.releases:
            qtui.installationSourceComboBox.addItem(release['tag_name'])

    # Update button function
    def emulator_updates(self):
        self.checkreg() # Initialise the reg value function
        installed_emulator = self.updatevalue
        response = requests.get(self.releases_url + "/latest")
        latest_release = response.json()
        latest_tag = latest_release['tag_name']

        # Check for specific emulators that use a rolling-release
        if self.emulator in ['Vita3K', 'NooDS']:
            reply = QMessageBox.question(qtui, "Rolling-Release Emulator Detected", f"{self.emulator} uses rolling-releases instead of numbered releases. This means that the latest version may not be the one you have installed (We cannot detect the version). Would you like to proceed with the download anyway?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.install_mode = "Update"
                qtui.layout.setCurrentIndex(3)
                self.Prepare_Download()
                return
            else:
                pass

        if latest_tag > installed_emulator:
            reply = QMessageBox.question(qtui, "Update Found", "Would you like to update " + self.emulator + " to " +  latest_tag + "?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.install_mode = "Update"
                qtui.layout.setCurrentIndex(3)
                self.Prepare_Download()
            else:
                pass
        else:
            QMessageBox.information(qtui, "No Update Found", f"You are up to date with the latest version of {self.emulator}", QMessageBox.StandardButton.Ok)

    # Preparing which file to downlaod
    def Prepare_Download(self):
        print (self.install_mode)
        reg_key = self.checkreg()
        if reg_key is not None:
            UpdateChannelValue = reg_key[1]
        else:
            UpdateChannelValue = None

        self.selection = qtui.installationSourceComboBox.currentText()

        if self.install_mode == "Install":
            response = requests.get(self.releases_url)
            releases = response.json()
            for release in releases:
                if release['tag_name'] == self.selection:
                    windows_assets = [asset for asset in release['assets'] if ('_win' in asset['name'].lower() or 'win' in asset['name'].lower() or 'xenia' in asset['name'].lower()) and asset['name'].endswith('.zip') and not asset['name'].endswith('.7z')]
                    if len(windows_assets) > 1:
                        options = "\n".join([f"{idx + 1}: {asset['name']}" for idx, asset in enumerate(windows_assets)])
                        choice, ok = QInputDialog.getItem(qtui, "Select Version", "Multiple Windows versions found. Please select one:\n" + options, [asset['name'] for asset in windows_assets], 0, False)
                        if ok:
                            self.selected_asset = next(asset for asset in windows_assets if asset['name'] == choice)
                            self.selected_asset_name = self.selected_asset['name']
                            print(self.selected_asset_name)
                            self.target_download = self.selected_asset['browser_download_url']
                            self.url = self.target_download  # url for the download thread
                            self.Download_Emulator()
                            self.createreg()
                        else:
                            sys.exit("No release selected. Exiting.")
                    elif len(windows_assets) == 1:
                        self.selected_asset_name = windows_assets[0]['name']
                        self.target_download = windows_assets[0]['browser_download_url']
                        print(self.target_download)
                        self.url = self.target_download  # url for the download thread
                        self.Download_Emulator()
                        self.createreg()
                    else:
                        QMessageBox.critical(qtui, "Error", f"No suitable Windows download found for {self.emulator} {self.selection}. Please try another release.")
                        qtui.layout.setCurrentIndex(2)
        elif self.install_mode == "Update":
            response = requests.get(self.releases_url + "/latest")
            latest_release = response.json()
            windows_assets = [asset for asset in latest_release['assets'] if ('_win' in asset['name'].lower() or 'win' in asset['name'].lower()) and asset['name'].endswith('.zip') and not asset['name'].endswith('.7z')]
            if windows_assets:
                if len(windows_assets) > 1:
                    options = "\n".join([f"{idx + 1}: {asset['name']}" for idx, asset in enumerate(windows_assets)])
                    choice, ok = QInputDialog.getItem(qtui, "Select Version", "Multiple Windows versions found. Please select one:\n" + options, [asset['name'] for asset in windows_assets], 0, False)
                    if ok:
                        latest_asset = next(asset for asset in windows_assets if asset['name'] == choice)
                    else:
                        sys.exit("No release selected. Exiting.")
                else:
                    latest_asset = windows_assets[0]

                self.target_download = latest_asset['browser_download_url']
                self.url = self.target_download  # url for the download thread
                print(self.url)
                self.Download_Emulator()
                self.selection = latest_release['tag_name']
                self.createreg()
            else:
                QMessageBox.critical(qtui, "Error", f"No suitable Windows download found for {self.emulator} in the latest release. Please try another release or check for updates.")
    # Download function
    def Download_Emulator(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False).name
        if self.install_mode == "Install":
            self.installationPath = qtui.installationPathLineEdit.text()
        elif self.install_mode == "Update":
            self.installationPath = self.regvalue
        os.makedirs(self.installationPath, exist_ok=True)
        # Threads
        self.download_thread = QThread()
        self.download_worker = DownloadWorker(self.url, temp_file)
        self.download_worker.moveToThread(self.download_thread)
        self.download_thread.started.connect(self.download_worker.do_download)
        self.download_worker.progress.connect(qtui.downloadProgressBar.setValue)
        self.download_thread.start()
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.finished.connect(self.download_thread.quit)
        self.download_worker.finished.connect(self.download_worker.deleteLater)
        self.download_thread.finished.connect(self.download_thread.deleteLater)
    def on_download_finished(self):
        self.extract_and_install(self.download_worker.dest, self.installationPath)

    # Extract and install function
    def extract_and_install(self, temp_file, extract_to):
        extract_to = self.installationPath
        # Rename the temporary file to have a .zip extension and create a temporary extraction folder
        zip_file_path = f"{temp_file}.zip"
        os.rename(temp_file, zip_file_path)
        self.temp_extract_folder = tempfile.mkdtemp()

        with ZipFile(zip_file_path, 'r') as emu_zip:
            emu_zip.extractall(self.temp_extract_folder)
            # Check for nested zip files and extract them
            nested_zips = [f for f in emu_zip.namelist() if f.endswith('.zip')]
            for nested_zip in nested_zips:
                nested_zip_path = os.path.join(self.temp_extract_folder, nested_zip)
                with ZipFile(nested_zip_path, 'r') as nested_zip_file:
                    nested_zip_file.extractall(self.temp_extract_folder)
                os.remove(nested_zip_path)
        os.remove(zip_file_path)

        self.move_files(extract_to)

    def move_files(self, extract_to):
        # Find the first directory containing an executable
        for root, dirs, files in os.walk(self.temp_extract_folder):
            if any(file.endswith('.exe') for file in files):
                src_path = root
                break
        else:
            src_path = self.temp_extract_folder  # Fallback if no .exe is found

        dest_path = extract_to
        os.makedirs(dest_path, exist_ok=True)
        for item in os.listdir(src_path):
            src_item_path = os.path.join(src_path, item)
            dest_item_path = os.path.join(dest_path, item)
            if os.path.isdir(src_item_path):
                shutil.copytree(src_item_path, dest_item_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_item_path, dest_item_path)

        # Mark the installation as complete
        self.installation_complete()

    # Install is complete
    def installation_complete(self):
        qtui.extractionProgressBar.setValue(100)

        # Fetch the executable path from the troppical_api data
        for troppical_api_data in self.troppical_api:
            if troppical_api_data['emulator_name'] == self.emulator:
                exe_name = troppical_api_data.get('exe_path', '')
                executable_path = os.path.normpath(os.path.join(qtui.installationPathLineEdit.text(), exe_name))
                print (executable_path)
        if executable_path is None:
            QMessageBox.critical(qtui, "Error", f"Executable path not found for emulator: {self.emulator}")
            return

        if qtui.desktopShortcutCheckbox.isChecked():
            self.define_shortcut(executable_path, 'desktop')
        if qtui.startMenuShortcutCheckbox.isChecked():
            self.define_shortcut(executable_path, 'start_menu')
        self.checkreg()
        qtui.layout.setCurrentIndex(4)

    # Function to check the reg values
    def checkreg(self):
        try:
            self.registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}", 0, winreg.KEY_READ)
            self.regvalue, regtype = winreg.QueryValueEx(self.registry_key, 'Install_Dir')
            self.updatevalue, regtype = winreg.QueryValueEx(self.registry_key, 'Version')
            self.asset_version, regtype = winreg.QueryValueEx(self.registry_key, 'Asset_version')
            winreg.CloseKey(self.registry_key)
            return self.regvalue, self.updatevalue, self.asset_version
        except FileNotFoundError:
            pass
    # Function to create the reg values
    def createreg (self):
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
        self.registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}", 0,
                                        winreg.KEY_WRITE)
        if self.install_mode == "Install":
            winreg.SetValueEx(self.registry_key, 'Install_Dir', 0, winreg.REG_SZ, qtui.installationPathLineEdit.text())
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
            QMessageBox.critical(qtui, "Error", f"Shortcut target does not exist: {target}")
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
            QMessageBox.critical(qtui, "Error", f"Failed to create shortcut: {e}")

    # Uninstall function
    def uninstall(self):
        self.checkreg()
        print (self.regvalue)
        if self.regvalue is not None:
            # Paths to the shortcuts
            desktopshortcut = os.path.join(os.environ['USERPROFILE'], 'Desktop', f'{self.emulator}.lnk')
            startmenushortcut = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', f'{self.emulator}.lnk')

            reply = QMessageBox.question(qtui, "Uninstall", f"Are you sure you want to uninstall {self.emulator} located on {self.regvalue}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
            else:
                # Remove the shortcut and the, DIR and REG keys
                if os.path.exists(desktopshortcut):
                    os.remove(desktopshortcut)
                if os.path.exists(startmenushortcut):
                    os.remove(startmenushortcut)
                dirpath = Path(self.regvalue)
                if dirpath.exists() and dirpath.is_dir():
                    shutil.rmtree(dirpath)
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
                    QMessageBox.information(qtui, "Uninstall", f"{self.emulator} has been successfully uninstalled.")
                    self.emulator = None
                    qtui.layout.setCurrentIndex(0)
                else:
                    QMessageBox.critical(qtui, "Error", "The directory might have been moved or deleted. Please reinstall the program.")
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
                    qtui.updateButton.setEnabled(False)
                    qtui.uninstallButton.setEnabled(False)
                    qtui.installButton.setEnabled(True)
        else:
            QMessageBox.critical(qtui, "Error",("Failed to read the registry key. Try and reinstall again!"))
            qtui.layout.setCurrentIndex(1)

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
            QMessageBox.critical(QtUi, "Error",("Error doing download."))
            self.finished.emit()

if __name__ == "__main__":
    version = Online.get_latest_git_tag()
    app = QApplication(sys.argv)
    ui_window = MainWindow()
    ui_window.show()
    sys.exit(app.exec())
