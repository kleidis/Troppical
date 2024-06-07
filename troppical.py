import os
import sys
import requests
import json
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QCheckBox, QStackedLayout, QHBoxLayout, QGroupBox, QComboBox, QProgressBar, QLineEdit, QMessageBox, QFileDialog, QVBoxLayout, QInputDialog, QTreeWidget, QTreeWidgetItem
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QByteArray, QFile, pyqtSignal, pyqtSlot
from zipfile import ZipFile 
import shutil
import tempfile
from icons import styledark_rc
import win32com.client
import winreg
from stylesheet import Style
from pathlib import Path

class QtUi(QMainWindow, Style):
    def __init__(self):
        super().__init__()
        self.logic = Logic()
        self.logic.fetch_google_sheet_data()
        self.ui()  # Init UI
        self.load_stylesheet()

    # Logo Header
    def Header(self):
        # Header Layout
        self.headerLayout = QVBoxLayout()
        self.headerLayout.setContentsMargins(0, 20, 0, 0)
        # Icon Widget
        iconLabel = QLabel()
        icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        icon = QIcon(icon_path)
        pixmap = icon.pixmap(180, 180)  # Specify the size directly
        iconLabel.setPixmap(pixmap)
        # Text Widget
        label = QLabel("<b><font size='10'>Troppical</font></b>")
        # Set Widgets
        self.headerLayout.addWidget(iconLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.headerLayout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        return self.headerLayout
    
    # Widgets
    def ui(self):
        # Init Window
        self.setWindowTitle(f'Troppical - {version}')  # Window name with version        
        self.setCentralWidget(QWidget(self))  # Set a central widget
        self.layout = QStackedLayout(self.centralWidget())  # Set the layout on the central widget
        self.setMaximumSize(1000, 720)  # Set the maximum window size to 1280x720
        self.setMinimumSize(1000, 720)  # Set the minimum window size to 800x600
        # Set the window icon
        icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.selection_page()

    # Emulator Select Page
    def selection_page(self):
        self.emulatorSelectPage = QWidget()
        emulatorSelectLayout = QVBoxLayout()
        emulatorSelectGroup = QGroupBox("Select your emulator from the list")
        emulatorSelectGroupLayout = QVBoxLayout()

        # Create a QTreeWidget
        self.emulatorTreeWidget = QTreeWidget()
        self.emulatorTreeWidget.setHeaderHidden(True)
        self.emulatorTreeWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        
        emulatorSelectGroupLayout.addWidget(self.emulatorTreeWidget)

        # Keep track of emulator systems
        system_items = {}

        for troppical_api_data in self.logic.troppical_api:
            emulator_system = troppical_api_data['emulator_system']
            emulator_name = troppical_api_data['emulator_name']

            # Fetch and decode the logo
            logo_url = troppical_api_data['emulator_logo']
            response = requests.get(logo_url)
            if response.status_code == 200:
                image_bytes = response.content
                qimage = QImage.fromData(QByteArray(image_bytes))
                pixmap = QPixmap.fromImage(qimage).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                icon = QIcon(pixmap)
                print(logo_url)
            else:
                QMessageBox.critical(self, "Failed to fetch logo", f"Failed to fetch logo for {emulator_name}. Status code: {response.status_code}")
                icon = QIcon()

            # Check if the emulator system already has a tree item, if not create one
            if emulator_system not in system_items:
                system_item = QTreeWidgetItem(self.emulatorTreeWidget)
                system_item.setText(0, emulator_system)
                system_item.setExpanded(True)  # Uncollapse the category by default
                system_items[emulator_system] = system_item
            else:
                system_item = system_items[emulator_system]

            # Add the emulator to the appropriate tree item
            emulator_item = QTreeWidgetItem(system_item)
            emulator_item.setText(0, emulator_name)
            emulator_item.setIcon(0, icon)

        # Set layout for the group and add to the main layout
        emulatorSelectGroup.setLayout(emulatorSelectGroupLayout)
        emulatorSelectLayout.addWidget(emulatorSelectGroup)
        self.emulatorSelectPage.setLayout(emulatorSelectLayout)  # Set the layout for the emulator selection page
        self.layout.addWidget(self.emulatorSelectPage)

        # Next button to confirm selection
        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.logic.set_emulator)
        emulatorSelectLayout.addWidget(self.nextButton)

        # Welcome page
        self.welcomePage = QWidget()
        ## Layout and gorup
        welcomerLayout = QVBoxLayout()
        welcomerGroup = QGroupBox("")
        welcomerGroupLayout = QVBoxLayout()
        buttonsLayout = QHBoxLayout()
        welcomerGroup.setLayout(welcomerGroupLayout)
        self.welcomePage.setLayout(welcomerLayout) # Set the welcomepage layout
        ## Widgets
        self.welcomerLabel = QLabel()
        self.welcomerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.installButton = QPushButton('Install')
        self.installButton.clicked.connect(self.logic.qt_button_click)
        self.updateButton = QPushButton('Check for Updates')
        self.updateButton.clicked.connect(self.logic.qt_button_click)
        self.uninstallButton = QPushButton('Uninstall')
        self.uninstallButton.clicked.connect(self.logic.qt_button_click)
        self.backButton = QPushButton("Back")
        self.backButton.setFixedSize(80, 30) 
        self.backButton.clicked.connect(self.logic.qt_button_click)
        ## Add widgets / layouts
        welcomerLayout.addLayout(self.Header()) 
        welcomerLayout.addWidget(welcomerGroup)
        welcomerGroupLayout.addWidget(self.welcomerLabel)
        buttonsLayout.addWidget(self.installButton)
        buttonsLayout.addWidget(self.updateButton)
        buttonsLayout.addWidget(self.uninstallButton)
        welcomerLayout.addLayout(buttonsLayout)
        welcomerLayout.insertWidget(0, self.backButton)
        ## Add the welcome page to the layout
        self.layout.addWidget(self.welcomePage)

        # Install page
        self.installPage = QWidget()
        ## Layout and gorup
        installLayout = QVBoxLayout()
        checkboxLayout = QVBoxLayout()
        checkboxGroup = QGroupBox("Do you want to create shortcuts?") # Checkboxes
        checkboxGroup.setLayout(checkboxLayout) # Set the layout of Checkboxes
        pathSelectorLayout = QHBoxLayout() # Browse widget layout
        self.installPage.setLayout(installLayout) # Set the installpage layout
        ## Widgets
        InstalOpt = QLabel('<b>Installation Options')
        InstalOpt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.installationSourceComboBox = QComboBox() # Dropdown menu
        self.desktopShortcutCheckbox = QCheckBox("Create a desktop shortcut") # Checkboxes
        self.startMenuShortcutCheckbox = QCheckBox("Create a start menu shortcut")
        self.installationPathLineEdit = QLineEdit()  # Browse for installation path widget
        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.logic.InstallPath)
        self.install_emu_button = QPushButton('Install') # Install button
        self.install_emu_button.clicked.connect(self.logic.qt_button_click)
        ## Add widgets / layouts
        installLayout.addLayout(self.Header()) ### Icon self.header
        installLayout.addWidget(InstalOpt) ### Instalation Option Label
        installLayout.addWidget(self.installationSourceComboBox) ## Install Sorce Widget
        pathSelectorLayout.addWidget(self.installationPathLineEdit) ## Browse Widget
        pathSelectorLayout.addWidget(self.browseButton)
        installLayout.addLayout(pathSelectorLayout)
        checkboxLayout.addWidget(self.desktopShortcutCheckbox) # Checkboxes
        checkboxLayout.addWidget(self.startMenuShortcutCheckbox)
        installLayout.addWidget(checkboxGroup)
        installLayout.addWidget(self.install_emu_button)
        ## Add the install page to the layout
        self.layout.addWidget(self.installPage)

        # Progress bar page
        self.progressBarPage = QWidget()
        ## Layout and groups
        progressBarLayout = QVBoxLayout()
        self.progressBarPage.setLayout(progressBarLayout)
        ## Widgets
        self.downloadProgressBar = QProgressBar()
        self.downloadProgressBar.setRange(0, 100)  # Progress bar Widgets
        self.extractionProgressBar = QProgressBar()
        self.extractionProgressBar.setRange(0, 100)    
        self.labeldown = QLabel("Downloading: ")
        self.labelext = QLabel("Extracting: ")
        ## Add widgets / layouts
        progressBarLayout.addLayout(self.Header())  # Add the icon self.header
        progressBarLayout.addWidget(self.labeldown)
        progressBarLayout.addWidget(self.downloadProgressBar)
        progressBarLayout.addWidget(self.labelext)
        progressBarLayout.addWidget(self.extractionProgressBar)
        # Add the progress bar page to the layout
        self.layout.addWidget(self.progressBarPage)

        # Finish page
        self.finishPage = QWidget()
        ## Layout and groups
        finishLayout = QVBoxLayout()
        self.finishPage.setLayout(finishLayout)
        ## Widgets
        finishLabel = QLabel("<b>Installation Complete!")
        finishLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text horizontally
        finishButton = QPushButton("Finish")
        finishButton.clicked.connect(self.close)
        ## Add widgets / layouts
        finishLayout.addLayout(self.Header())  # Add the icon self.header
        finishLayout.addWidget(finishLabel)
        finishLayout.addWidget(finishButton)
        # Add the progress bar page to the layout
        self.layout.addWidget(self.finishPage)  
        
    def load_stylesheet(app):
            app.setStyleSheet(Style.dark_stylesheet)
            
class Logic:
    def __init__(self):
        self.regvalue = None  
        self.install_mode = None
   
    def fetch_google_sheet_data(self):
        url = "https://script.googleusercontent.com/macros/echo?user_content_key=Hw-G9S_OHELhOUAsT-oQr8ux2HPMIpva3U1w0Su7P1ZYrr1ngXyqlN6LBhfev1taFoRtJ07w_KDhWVbMaBaeJ3c86H4e0k8Xm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnL69XsVZDOhipZMwrhs3JioNozSVnp4Chm6SveAF_nlUSMgTaOh-zk0bQ5F9LtyaiRZKic-heYuYVV866SySaVfv-0TkTPKcCtz9Jw9Md8uu&lib=MmjrdpKGbUxdyxLDAqWkoFhoZjK-0W8qS"
        response = requests.get(url)
        if response.status_code == 200:
            all_data = response.json()
            self.troppical_api = [item for item in all_data if item.get('emulator_platform') != 'android']
            return self.troppical_api
        else:
            print("Failed to fetch data:", response.status_code)

    # Set which emulator to use for the installer depeanding on the selected emulator 
    def set_emulator(self, emulator):
        selected_item = qtui.emulatorTreeWidget.currentItem()
        if selected_item and selected_item.parent():
            emulator_name = selected_item.text(0)
        else:
            QMessageBox.warning(qtui, "Selection Error", "Please select an emulator.")


        self.emulator = emulator_name
        reg_result = self.checkreg()
        if reg_result is None:
            installed_emulator = "Not Installed"
        else:
            installed_emulator = reg_result[1]
        for selected_emulator in self.troppical_api:
            if selected_emulator['emulator_name'] == self.emulator:
                self.releases_url = f"https://api.github.com/repos/{selected_emulator['emulator_owner']}/{selected_emulator['emulator_repo']}/releases"
                if self.emulator in ["Panda3DS"]:
                    self.nightly_url = f"https://nightly.link/{selected_emulator['emulator_owner']}/{selected_emulator['emulator_repo']}/workflows/Qt_Build/master/Windows%20executable.zip"
                else:
                    self.nightly_url = f"https://nightly.link/{selected_emulator['emulator_owner']}/{selected_emulator['emulator_repo']}/workflows/build/master/windows-msvc.zip"

        qtui.installationPathLineEdit.setText(QLineEdit(os.path.join(os.environ['LOCALAPPDATA'], self.emulator)).text()) 
        qtui.labeldown.setText(qtui.labeldown.text() + self.emulator)
        qtui.labelext.setText(qtui.labelext.text() + self.emulator)
        qtui.welcomerLabel.setText(f'<big>Your currently selected emulator is <b>{self.emulator}</b> and current version is <b>{installed_emulator}</b>.</big>')

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

    # Welcome page buttons button clinking function
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

        # Remove or add items based on the emulator
        for release in self.releases: 
            qtui.installationSourceComboBox.addItem(release['tag_name'])
        
    # Update button function    
    def emulator_updates(self): 
        self.checkreg() # Initialise the reg value function
        installed_emulator = self.updatevalue
        response = requests.get(self.releases_url + "/latest")
        latest_release = response.json()
        latest_version = latest_release['tag_name']

        if latest_version > installed_emulator:
            reply = QMessageBox.question(qtui, "Update Found", "Would you like to update " + self.emulator + " to " +  latest_version + "?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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
                    windows_assets = [asset for asset in release['assets'] if 'windows' in asset['name'].lower() and asset['name'].endswith('.zip')]
                    if len(windows_assets) > 1:
                        options = "\n".join([f"{idx + 1}: {asset['name']}" for idx, asset in enumerate(windows_assets)])
                        choice, ok = QInputDialog.getItem(qtui, "Select Version", "Multiple Windows versions found. Please select one:\n" + options, [asset['name'] for asset in windows_assets], 0, False)
                        if ok:
                            self.selected_asset = next(asset for asset in windows_assets if asset['name'] == choice)
                            self.selected_asset_name = self.selected_asset['name']
                            print (self.selected_asset_name)
                            self.target_download = self.selected_asset['browser_download_url']
                            self.url = self.target_download  # url for the download thread
                            self.Download_Emulator()
                            self.createreg()
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
            windows_assets = [asset for asset in latest_release['assets'] if 'windows' in asset['name'].lower() and asset['name'].endswith('.zip')]
            if windows_assets:
                if len(windows_assets) > 1:
                    options = "\n".join([f"{idx + 1}: {asset['name']}" for idx, asset in enumerate(windows_assets)])
                    choice, ok = QInputDialog.getItem(qtui, "Select Version", "Multiple Windows versions found. Please select one:\n" + options, [asset['name'] for asset in windows_assets], 0, False)
                    if ok:
                        latest_asset = next(asset for asset in windows_assets if asset['name'] == choice)
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
        self.installationPath = self.regvalue or qtui.installationPathLineEdit.text()
        os.makedirs(self.installationPath, exist_ok=True)
        # Threads
        self.download_thread = QThread()
        self.download_worker = DownloadWorker(self.url, temp_file)
        self.download_worker.moveToThread(self.download_thread)
        self.download_thread.started.connect(self.download_worker.do_download)
        self.download_worker.progress.connect(qtui.downloadProgressBar.setValue)
        self.download_thread.start()
        self.download_worker.finished.connect(lambda: self.extract_and_install(temp_file, self.installationPath))

    # Extract and install function 
    def extract_and_install(self, temp_file, extract_to):
        # Clear the target directory before extracting new files
        if os.path.exists(extract_to):
            shutil.rmtree(extract_to)

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
            shutil.move(os.path.join(src_path, item), dest_path)
       
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
                    exit()
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
    version = "v1.1"
    app = QApplication(sys.argv)
    qtui = QtUi()
    qtui.show()
    self = Logic()
    sys.exit(app.exec())
