import subprocess
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog, QInputDialog
from PyQt6.QtCore import QThread
import os
import sys
from zipfile import ZipFile
import shutil
import tempfile
from icons import styledark_rc
import win32com.client
import winreg
from pathlib import Path
import pyuac
from init_instances import inst
from utils.dep_check import check_7zip_installed, get_7zip_path

class Main():
    def __init__(self):
        # Init variables
        self.emulator = None  # Keep track of the selected emulator
        self.downloadThread = None
        self.downloadWorker = None

    def initialize_app(self):
        app = QApplication(sys.argv)
        uiMain = inst.ui
        uiMain.show()
        sys.exit(app.exec())

    def update_reg_result(self):
        self.regResult = self.check_reg()
        return self.regResult

    # Set which emulator to use for the installer depeanding on the selected emulator
    def set_emulator(self):
        installReg = self.update_reg_result()

        selectedItem = inst.sel.emulatorTreeWidget.currentItem()
        if not selectedItem or not selectedItem.parent():
            QMessageBox.warning(inst.ui, "Selection Error", "Please select an emulator.")
            return False

        emulatorName = selectedItem.text(0)
        if self.emulator != emulatorName:
            # Clear previous emulator settings
            inst.bar.labeldown.setText("Downloading: ")
            inst.bar.labelext.setText("Extracting: ")
            inst.act.actLabel.setText("")

            self.emulator = emulatorName

            emulatorData = inst.online.emulatorDatabase

            # Construct the releases URL
            selectedEmulator = next((em for em in emulatorData.values() if em['name'] == self.emulator), None)
            if selectedEmulator:
                owner = selectedEmulator['owner']
                repo = selectedEmulator['repo']

                non_github_hosts = {
                    "Citron": {
                        "host_type": "gitea",
                        "api_url": "https://git.citron-emu.org/api/v1/repos/{owner}/{repo}/releases"
                    },
                }

                def set_releases_url(owner, repo):
                    if selectedEmulator['name'] in non_github_hosts:
                        host_info = non_github_hosts[selectedEmulator['name']]
                        releasesUrl = host_info['api_url'].format(owner=owner, repo=repo)
                    else:
                        # Default to GitHub if not in the dictionary
                        releasesUrl = f"https://api.github.com/repos/{owner}/{repo}/releases"

                    return releasesUrl
                self.releasesUrl = set_releases_url(owner, repo)

        installedEmulator = "Not Installed" if installReg is None else installReg[1]
        defaultPath = os.path.normpath(inst.config.get_setting('default_install_path'))
        inst.install.installationPathLineEdit.setText(
            os.path.join(defaultPath, self.emulator)
        )
        inst.bar.labeldown.setText(f"Downloading: {self.emulator}")
        inst.bar.labelext.setText(f"Extracting: {self.emulator}")
        inst.act.actLabel.setText(
            f'<big>Your currently selected emulator is <b>{self.emulator}</b> and current version is <b>{installedEmulator}</b>.</big>'
        )

        inst.ui.disable_qt_buttons_if_installed()
        return True # To avoid the function from switching index even on non-select item

    def InstallPath(self):
        currentPath = os.path.normpath(inst.install.installationPathLineEdit.text())
        selectedDirectory = QFileDialog.getExistingDirectory(inst.install, "Select Installation Directory", currentPath)

        if selectedDirectory:
            installDir = os.path.join(selectedDirectory, self.emulator)
            self.installDir = os.path.normpath(installDir)
            inst.install.installationPathLineEdit.setText(self.installDir)

    def Add_releases_to_combobox(self):
        self.releases = inst.online.fetch_releases()

        inst.install.installationSourceComboBox.clear()
        try:
            for release in self.releases:
                inst.install.installationSourceComboBox.addItem(release['tag_name'])
        except Exception as e:
            QMessageBox.critical(inst.ui, "Error", f"Failed to fetch releases: {str(e)}")
            inst.ui.qt_index_switcher(1)

    # Updater function
    def emulator_updater(self):
        reg = self.update_reg_result()
        installedEmulator = reg[1]
        latestRelease = inst.online.fetch_releases(latest=True)
        if not latestRelease:
            return
        latestTag = latestRelease['tag_name']

        # Check for specific emulators that use a rolling-release
        if self.emulator in ['Vita3K', 'NooDS', 'Duckstation']: # TODOL Add this type to json database
            reply = QMessageBox.question(inst.ui, "Rolling-Release Emulator Detected", f"{self.emulator} uses rolling-releases instead of numbered releases. This means that the latest version may not be the one you have installed (We cannot detect the version). Would you like to proceed with the download anyway?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.installMode = "Update"
                inst.ui.qt_index_switcher(4)
                self.Prepare_Download()
                return
            else:
                pass

        if inst.online.emulatorDatabase[self.emulator]['has_in_app_updater']:
            reply = QMessageBox.warning(
                inst.ui,
                "In-App Updater Detected",
                f"{self.emulator} has its own way of updating. Would you like to open the emulator and manually update it, or download the latest version from here?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    exePath = os.path.join(reg[0], inst.online.emulatorDatabase[self.emulator]['exe_path'])
                    subprocess.Popen([exePath])
                except Exception as e:
                    QMessageBox.critical(inst.ui, "Error", f"Failed to open emulator: {e}")
                return
            else:
                pass

        # TODO: Improve tag comparing
        if latestTag > installedEmulator:
            reply = QMessageBox.question(inst.ui, "Update Found", "Would you like to update " + self.emulator + " to " +  latestTag + "?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.installMode = "Update"
                inst.ui.qt_index_switcher(4)
                self.Prepare_Download()
            else:
                pass
        else:
            QMessageBox.information(inst.ui, "No Update Found", f"You are up to date with the latest version of {self.emulator}", QMessageBox.StandardButton.Ok)

    def Prepare_Download(self):
        self.selection = inst.install.installationSourceComboBox.currentText()
        regResult = self.update_reg_result()
        tempFile = tempfile.NamedTemporaryFile(delete=False).name

        if self.installMode == "Install":
            self.installationPath = inst.install.installationPathLineEdit.text()
            self.windowsAssets = inst.online.fetch_github_release(self.selection)
        elif self.installMode == "Update":
            self.installationPath = regResult[0]
            self.windowsAssets = inst.online.fetch_github_release("latest")

        if not self.windowsAssets:
            QMessageBox.critical(inst.ui, "Error", f"No suitable Windows download found for {self.emulator}. Please try another release.")
            inst.ui.qt_index_switcher(3)
            return

        if len(self.windowsAssets) > 1:
            options = "\n".join([f"{idx + 1}: {asset['name']}" for idx, asset in enumerate(self.windowsAssets)])
            choice, ok = QInputDialog.getItem(
                inst.ui,
                "Select Version",
                "Multiple Windows versions found. Please select one:\n" + options,
                [asset['name'] for asset in self.windowsAssets],
                # Make the selection non-editable
                0,
                False
            )
            if ok:
                selectedAsset = next(asset for asset in self.windowsAssets if asset['name'] == choice)
            else:
                QMessageBox.critical(inst.ui, "Error", "Please select an asset to download")
                inst.ui.qt_index_switcher(3)
                return
        else:
            selectedAsset = self.windowsAssets[0]

        self.selectedAssetName = selectedAsset['name']
        self.targetDownload = selectedAsset['browser_download_url']
        self.url = self.targetDownload
        self.start_download_thread(self.url, tempFile)

    def start_download_thread(self, url, dest):
        if self.downloadThread is not None:
            self.downloadThread.quit()
            self.downloadThread.wait()

        self.downloadThread = QThread()
        self.downloadWorker = inst.download
        self.downloadWorker.set_task(url, dest)
        self.downloadWorker.moveToThread(self.downloadThread)
        self.downloadWorker.progress.connect(inst.bar.downloadProgressBar.setValue)
        self.downloadWorker.finished.connect(self.on_download_finished)
        self.downloadThread.started.connect(self.downloadWorker.run)
        self.downloadThread.start()
    def on_download_finished(self):
        self.extract_and_install(self.downloadWorker.dest, self.installationPath)
        self.downloadThread.quit()
        self.downloadThread.wait()
        self.downloadThread = None
        self.downloadWorker = None

    def extract_and_install(self, tempFile, extractTo):
        sevenZip = get_7zip_path()
        if not sevenZip and self.selectedAssetName.endswith('.7z'):
            if not check_7zip_installed():
                return
            sevenZip = '7z'

        if self.selectedAssetName.endswith('.7z'):
            archiveFile = f"{tempFile}.7z"
            is7zip = True
        else:
            archiveFile = f"{tempFile}.zip"
            is7zip = False

        try:
            os.rename(tempFile, archiveFile)
            self.tempExtractFolder = tempfile.mkdtemp()

            try:
                if is7zip:
                    result = subprocess.run([sevenZip, 'x', archiveFile, f'-o{self.tempExtractFolder}', '-y'],
                                         capture_output=True, text=True)
                    if result.returncode != 0:
                        raise Exception(f"7zip extraction failed: {result.stderr}")
                else:
                    with ZipFile(archiveFile, 'r') as emuZip:
                        emuZip.extractall(self.tempExtractFolder)

                # Handle nested archives
                for root, _, files in os.walk(self.tempExtractFolder):
                    for file in files:
                        if file.endswith(('.zip', '.7z')):
                            nestedPath = os.path.join(root, file)
                            try:
                                if file.endswith('.7z'):
                                    result = subprocess.run([sevenZip, 'x', nestedPath, f'-o{root}', '-y'],
                                                         capture_output=True, text=True)
                                    if result.returncode != 0:
                                        raise Exception(f"7zip extraction failed: {result.stderr}")
                                else:
                                    with ZipFile(nestedPath, 'r') as nested:
                                        nested.extractall(root)
                                os.remove(nestedPath)
                            except Exception as e:
                                QMessageBox.warning(inst.ui, "Nested Archive Warning",
                                                 f"Failed to extract nested archive {file}: {str(e)}")
                                continue

            except Exception as e:
                QMessageBox.critical(inst.ui, "Extraction Error", f"Failed to extract files: {str(e)}")
                return
            finally:
                os.remove(archiveFile)
            self.move_files(self.installationPath)
        except Exception as e:
            QMessageBox.critical(inst.ui, "File Error", f"Failed to process downloaded file: {str(e)}")
            return

    def move_files(self, extractTo):
        try:
            exeRoot = next(
                (root for root, _, files in os.walk(self.tempExtractFolder)
                if any(file.endswith('.exe') for file in files)),
                self.tempExtractFolder
            )

            if self.check_admin(extractTo):
                shutil.rmtree(self.tempExtractFolder, ignore_errors=True)
                sys.exit()

            os.makedirs(extractTo, exist_ok=True)

            try:
                items = os.listdir(exeRoot)
                for idx, item in enumerate(items):
                    try:
                        src = os.path.join(exeRoot, item)
                        dest = os.path.join(extractTo, item)

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
                shutil.rmtree(self.tempExtractFolder, ignore_errors=True)

            self.installation_complete()
        except Exception as e:
            QMessageBox.critical(inst.ui, "Installation Error", f"Failed to complete installation: {str(e)}")
            return

    def installation_complete(self):
        self.create_reg() # Create the registry values
        if self.installMode == "Install":
            inst.config.handle_emulator_lst(self.emulator)

        installPath = self.update_reg_result()[0]
        inst.bar.extractionProgressBar.setValue(100)

        emulatorData = inst.online.emulatorDatabase.get(self.emulator, {})
        exeName = emulatorData.get('exe_path', '')
        executablePath = os.path.normpath(os.path.join(installPath, exeName))

        if not exeName:
            QMessageBox.critical(inst.ui, "Error", f"Executable path not found for emulator: {self.emulator}")
            return

        if inst.install.desktopShortcutCheckbox.isChecked():
            self.define_shortcut(executablePath, 'desktop')
        if inst.install.startMenuShortcutCheckbox.isChecked():
            self.define_shortcut(executablePath, 'start_menu')
        inst.ui.qt_index_switcher(5)

    def check_admin(self, path):
        testPath = os.path.join(path, "test_admin")
        if not os.path.exists(testPath):
            try:
                os.makedirs(testPath)
            except PermissionError:
                QMessageBox.critical(inst.ui, "Error", "You do not have the necessary permissions to uninstall from this directory. Please run the application as an administrator.")
                return True

        testFile = os.path.join(testPath, "test.txt")
        try:
            with open(testFile, 'w') as f:
                f.write("test")
        except PermissionError:
            QMessageBox.critical(inst.ui, "Error", "You do not have the necessary permissions to uninstall from this directory. Please run the application as an administrator.")
            return True
        try:
            os.remove(testFile)
            os.rmdir(testPath)
        except:
            pass

    def check_reg(self):
        try:
            self.registryKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}", 0, winreg.KEY_READ)
            self.instValue, regtype = winreg.QueryValueEx(self.registryKey, 'Install_Dir')
            self.updateValue, regtype = winreg.QueryValueEx(self.registryKey, 'Version')
            self.assetVersion, regtype = winreg.QueryValueEx(self.registryKey, 'Asset_version')
            winreg.CloseKey(self.registryKey)
            return self.instValue, self.updateValue, self.assetVersion
        except FileNotFoundError:
            pass
    def create_reg (self):
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
        self.registryKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}", 0,
                                        winreg.KEY_WRITE)
        if self.installMode == "Install":
            winreg.SetValueEx(self.registryKey, 'Install_Dir', 0, winreg.REG_SZ, inst.install.installationPathLineEdit.text())
            winreg.SetValueEx(self.registryKey, 'Asset_version', 0, winreg.REG_SZ, self.selectedAssetName)
        winreg.SetValueEx(self.registryKey, 'Version', 0, winreg.REG_SZ, self.selection)
        winreg.CloseKey(self.registryKey)

    def define_shortcut(self, target, locationType):
        if locationType == 'desktop':
            path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        elif locationType == 'start_menu':
            path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')

        filename = f'{self.emulator}.lnk'
        shortcutPath = os.path.join(path, filename)

        if not os.path.exists(target):
            QMessageBox.critical(inst.ui, "Error", f"Shortcut target does not exist: {target}")
            return

        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcutPath)
            shortcut.TargetPath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.Description = "" # TODO: Add description to database
            shortcut.Arguments = "" # TODO: Add arguments to database
            shortcut.IconLocation = target
            shortcut.save()
        except Exception as e:
            QMessageBox.critical(inst.ui, "Error", f"Failed to create shortcut: {e}")

    def uninstall(self):
        uninstallReg = self.update_reg_result()
        dirpath = Path(self.instValue)
        if self.check_admin(dirpath):
            shutil.rmtree(dirpath, ignore_errors=True)
            return

        if uninstallReg[0] is not None:
            desktopShortcut = os.path.join(os.environ['USERPROFILE'], 'Desktop', f'{self.emulator}.lnk')
            startMenuShortcut = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', f'{self.emulator}.lnk')

            reply = QMessageBox.question(inst.ui, "Uninstall", f"Are you sure you want to uninstall {self.emulator} located on {self.instValue}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
            else:
                try:
                    inst.config.handle_emulator_lst(self.emulator, uninstall=True)
                except Exception as e:
                    QMessageBox.critical(inst.ui, "Error", f"Failed to uninstall: {str(e)}")
                    return
                return
                for shortcut in [desktopShortcut, startMenuShortcut]:
                    if os.path.exists(shortcut):
                        os.remove(shortcut)

                if dirpath.exists() and dirpath.is_dir():
                    shutil.rmtree(dirpath)
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
                    QMessageBox.information(inst.ui, "Uninstall", f"{self.emulator} has been successfully uninstalled.")
                    self.emulator = None
                    inst.ui.qt_index_switcher(1)
                else:
                    QMessageBox.critical(inst.ui, "Error", "The directory might have been moved or deleted. Please reinstall the program.")
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
                    inst.act.updateButton.setEnabled(False)
                    inst.act.uninstallButton.setEnabled(False)
                    inst.act.installButton.setEnabled(True)
                    inst.ui.qt_index_switcher(1)
        else:
            QMessageBox.critical(inst.ui, "Error",("Failed to read the registry key. Try and reinstall again!"))
            inst.ui.qt_index_switcher(1)

if __name__ == "__main__":
    main = Main()
    if inst.config.get_setting('launch_as_admin'):
        if not pyuac.isUserAdmin():
            pyuac.runAsAdmin()
        else:
            main.initialize_app()
    else:
        main.initialize_app()


