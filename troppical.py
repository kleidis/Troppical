import os
import sys
import requests
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QCheckBox, QStackedLayout, QHBoxLayout, QGroupBox, QComboBox, QProgressBar, QLineEdit, QMessageBox, QFileDialog, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QByteArray, QFile, pyqtSignal, pyqtSlot
from zipfile import ZipFile 
import shutil
import tempfile
from icons import styledark_rc
import win32com.client
import winreg
import base64
from Citra_Logo_base64 import image_data as citra
from LimeLogo_base64 import image_data as lime
from CitraEnhanced_base64 import image_data as citra_enh
from installer_logo_base64 import image_data as logo
from yuzu_base64 import image_data as yuzu

from stylesheet import Style
from pathlib import Path

class QtUi(QMainWindow, Style):
    def __init__(self):
        super().__init__()
        self.logic = Logic()
        self.ui()  # Init UI
        self.load_stylesheet()
        
    # Logo Header
    def Header(self):
        # Header Layout
        self.headerLayout = QVBoxLayout()
        self.headerLayout.setContentsMargins(0, 20, 0, 0)
        # Icon Widget
        CEicon = QLabel()
        image_bytes = base64.b64decode(logo)
        image = QImage.fromData(QByteArray(image_bytes))
        pixmap = QPixmap.fromImage(image)
        ## Scale the pixmap
        scaledPixmap = pixmap.scaled(180, 180,)
        CEicon.setPixmap(scaledPixmap)
        # Text Widget
        CElabel = QLabel("<b><font size='10'>Troppical</font></b>")
        # Set Widgets
        self.headerLayout.addWidget(CEicon, alignment=Qt.AlignmentFlag.AlignCenter)
        self.headerLayout.addWidget(CElabel, alignment=Qt.AlignmentFlag.AlignCenter)
        return self.headerLayout
    
    # Widgets
    def ui(self):
        # Init Window
        self.setWindowTitle('Troppical') # Window name
        self.setCentralWidget(QWidget(self))  # Set a central widget
        self.layout = QStackedLayout(self.centralWidget())  # Set the layout on the central widget
        image_bytes = base64.b64decode(logo)
        # Window icon from base64 file to keep all into one executable
        image = QImage.fromData(QByteArray(image_bytes))
        pixmap = QPixmap.fromImage(image)
        # Set the window icon
        self.setWindowIcon(QIcon(pixmap))

        # Emulator Select Page
        self.emulatorSelectPage = QWidget()
        emulatorSelectLayout = QHBoxLayout()  # Changed to horizontal layout
        emulatorSelectGroup = QGroupBox("Emulators")
        emulatorSelectGroupLayout = QVBoxLayout()  # Changed to vertical layout for stacking icons
        # Layouts and griups
        descriptionGroup = QGroupBox("Emulator Descriptions")
        descriptionGroupLayout = QVBoxLayout()
        self.emulatorSelectPage.setLayout(emulatorSelectLayout)
        emulatorSelectGroup.setLayout(emulatorSelectGroupLayout)
        descriptionGroup.setLayout(descriptionGroupLayout)
        # Widgets
        # Yuzu
        yuzu_image_bytes = base64.b64decode(yuzu)
        yuzu_qimage = QImage.fromData(QByteArray(yuzu_image_bytes))
        yuzu_pixmap = QPixmap.fromImage(yuzu_qimage).scaled(112, 112, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        yuzu_label = QLabel()
        yuzu_label.setPixmap(yuzu_pixmap)
        yuzu_label.setStyleSheet("QLabel:hover { background-color: rgba(255, 255, 255, 50); }")
        yuzu_label.mousePressEvent = lambda event: self.logic.set_emulator('sudachi')
        yuzu_desc = QLabel("Sudachi is a continuation of Yuzu by a unfiliated developer \n that already has some fixes/enhancements that were not in the original.")
        yuzu_desc.setFixedHeight(112)
        yuzu_desc.setStyleSheet("background-color: rgba(255, 255, 255, 16); color: white; border-radius: 5px; padding: 5px;")
        ## Citra-Enhanced Emulator
        citra_enh_image_bytes = base64.b64decode(citra_enh)
        citra_enh_qimage = QImage.fromData(QByteArray(citra_enh_image_bytes))
        citra_enh_pixmap = QPixmap.fromImage(citra_enh_qimage).scaled(112, 112, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        citra_enh_label = QLabel()
        citra_enh_label.setPixmap(citra_enh_pixmap)
        citra_enh_label.setStyleSheet("QLabel:hover { background-color: rgba(255, 255, 255, 50); }")
        citra_enh_label.mousePressEvent = lambda event: self.logic.set_emulator('Citra-Enhanced')
        citra_enh_desc = QLabel("Citra-Enhanced offers improved performance for games at the cost of stability and bugs.")
        citra_enh_desc.setFixedHeight(112)
        citra_enh_desc.setStyleSheet("background-color: rgba(255, 255, 255, 16); color: white; border-radius: 5px; padding: 5px;")
        # Lime3DS Emulator
        lime_image_bytes = base64.b64decode(lime)
        lime_qimage = QImage.fromData(QByteArray(lime_image_bytes))
        lime_pixmap = QPixmap.fromImage(lime_qimage).scaled(112, 112, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        lime_label = QLabel()
        lime_label.setPixmap(lime_pixmap)
        lime_label.setStyleSheet("QLabel:hover { background-color: rgba(255, 255, 255, 50); }")
        lime_label.mousePressEvent = lambda event: self.logic.set_emulator('Lime3DS')
        lime_desc = QLabel("Lime3DS is an open source 3DS emulator that aims to revive and continue work on Citra.<br><b>It is generally more stable than Citra-Enhanced.</b>")
        lime_desc.setFixedHeight(112)
        lime_desc.setStyleSheet("background-color: rgba(255, 255, 255, 16); color: white; border-radius: 5px; padding: 5px; line-height: 1.6;")
        # Citra PabloMK7 Emulator
        citra_image_bytes = base64.b64decode(citra)
        citra_qimage = QImage.fromData(QByteArray(citra_image_bytes))
        citra_pixmap = QPixmap.fromImage(citra_qimage).scaled(112, 112, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        citra_label = QLabel()
        citra_label.setPixmap(citra_pixmap)
        citra_label.setStyleSheet("QLabel:hover { background-color: rgba(255, 255, 255, 50); }")
        citra_label.mousePressEvent = lambda event: self.logic.set_emulator('Citra')
        citra_desc = QLabel("Pablo's fork is the closets to Citra since it has former devs working on it.")
        citra_desc.setFixedHeight(112)
        citra_desc.setStyleSheet("background-color: rgba(255, 255, 255, 16); color: white; border-radius: 5px; padding: 5px;")
        # Adding widgets to the layout
        ## Images
        emulatorSelectGroupLayout.addWidget(yuzu_label)
        emulatorSelectGroupLayout.addWidget(lime_label)
        emulatorSelectGroupLayout.addWidget(citra_enh_label)        
        emulatorSelectGroupLayout.addWidget(citra_label)
        ## Descriptions
        descriptionGroupLayout.addWidget(yuzu_desc)
        descriptionGroupLayout.addWidget(lime_desc)
        descriptionGroupLayout.addWidget(citra_enh_desc)
        descriptionGroupLayout.addWidget(citra_desc)
        emulatorSelectLayout.addWidget(emulatorSelectGroup)
        emulatorSelectLayout.addWidget(descriptionGroup)
        # Add the page to the layout
        self.layout.addWidget(self.emulatorSelectPage)

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

    # Set which emulator to use for the installer depeanding on the selected emulator 
    def set_emulator(self, emulator):
        self.emulator = emulator
        reg_result = self.checkreg()
        if reg_result is None:
            current_version = "Not Installed"
        else:
            _, current_version = reg_result

        if self.emulator == "Citra":
            self.releases_url = "https://api.github.com/repos/PabloMK7/citra/releases"
            self.nightly_url = "https://nightly.link/PabloMK7/citra/workflows/build/master/windows-msvc.zip"
        elif self.emulator == "Lime3DS":
            self.releases_url = "https://api.github.com/repos/Lime3DS/Lime3DS/releases"
            self.nightly_url = "https://nightly.link/Lime3DS/Lime3DS/workflows/build/master/windows-msvc.zip"
        elif self.emulator == "Citra-Enhanced":
            self.releases_url = "https://api.github.com/repos/CitraEnhanced/citra/releases"
            self.nightly_url = "https://nightly.link/CitraEnhanced/citra/workflows/build/master/windows-msvc.zip"
        elif self.emulator == "sudachi":
            self.releases_url = "https://api.github.com/repos/sudachi-emu/sudachi/releases"
            self.nightly_url = None
    

        # Set widgets to emulator value
        qtui.installationPathLineEdit.setText(QLineEdit(os.path.join(os.environ['LOCALAPPDATA'], self.emulator)).text()) 
        qtui.labeldown.setText(qtui.labeldown.text() + self.emulator)
        qtui.labelext.setText(qtui.labelext.text() + self.emulator)
        qtui.welcomerLabel.setText(f'<big>Your currently selected emulator is <b>{self.emulator}</b> and current version is <b>{current_version}</b>.</big>')

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
            self.check_for_updates()
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
        response = requests.get(self.releases_url)
        self.releases = response.json()[:10] 

        for release in self.releases:
            qtui.installationSourceComboBox.addItem(release['tag_name'])
        
        qtui.installationSourceComboBox.insertSeparator(len(self.releases))

        if self.emulator != "sudachi":
            # Add the latest CI action run option to the combobox
            qtui.installationSourceComboBox.addItem("Latest Nightly")

        
    # Update button function    
    def check_for_updates(self): 
        self.checkreg() # Initialise the reg value function
        current_Version = self.updatevalue
        response = requests.get(self.releases_url + "/latest")
        latest_release = response.json()
        latest_version = latest_release['tag_name']

        if current_Version == "Latest Nightly":
            reply = QMessageBox.question(qtui, "Update nightly builds", f"Due to the way nightly builds work, we cannot fetch the latest version. Check our Github page to see what changed. Would you like to update {self.emulator} to the latest nightly build?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.install_mode = "Update"
                qtui.layout.setCurrentIndex(3)
                self.Prepare_Download()
        elif latest_version > current_Version:
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
            _, UpdateChannelValue = reg_key
        else:
            UpdateChannelValue = None  

        self.selection = qtui.installationSourceComboBox.currentText()

        if self.install_mode == "Install":
            if self.selection == "Latest Nightly":
                self.target_download = self.nightly_url
                self.url = self.target_download # url for the downlaod thread
                self.Download_Emulator()
                print (self.url)
                self.createreg()
                return              
            else:
                response = requests.get(self.releases_url)
                releases = response.json()
            for release in releases:
                if release['tag_name'] == self.selection:
                    for asset in release['assets']:
                        if 'windows-msvc' in asset['name'] or f"{self.selection}-windows.zip" in asset['name']:
                            if asset['name'].endswith('.zip'):
                                self.target_download = asset['browser_download_url']
                                print (self.target_download)
                                self.url = self.target_download # url for the downlaod thread
                                self.Download_Emulator()
                                self.createreg()
                            elif asset == None:
                                QMessageBox.critical(qtui, "Error", f"No suitable download found for {self.emulator} {self.selection} Please try another release.")
                                qtui.layout.setCurrentIndex(2)
        elif self.install_mode == "Update":
            if UpdateChannelValue == "Latest Nightly":
                self.target_download = self.nightly_url
                self.url = self.target_download # url for the downlaod thread
                self.Download_Emulator()
                print (self.url)
                return
            else:
                response = requests.get(self.releases_url + "/latest")
                latest_release = response.json()
                for asset in latest_release['assets']:
                    if 'windows-msvc' in asset['name'] or f"{self.selection}-windows.zip" in asset['name']:
                        if asset['name'].endswith('.zip'):
                            self.target_download = asset['browser_download_url']
                            self.url = self.target_download # url for the downlaod thread
                            self.Download_Emulator()
                            self.selection = latest_release['tag_name'] # The mathod of updating the reg value is bound to chnage on the update method
                            self.createreg()

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
            for file in emu_zip.namelist():
                if file.endswith('.zip'):
                    nested_zip_path = os.path.join(self.temp_extract_folder, file)
                    with ZipFile(nested_zip_path, 'r') as nested_zip:
                        nested_zip.extractall(self.temp_extract_folder)
                    os.remove(nested_zip_path)
        os.remove(zip_file_path)

        self.move_files(extract_to)

    # Move extartced files function (There is a bug with this if you select ci builds the etartced nested archive might also move with the files)
    def move_files(self, extract_to):
        dir_path = os.path.join(self.temp_extract_folder)
        src_path = os.path.join(dir_path)
        if self.emulator == "sudachi":
            dest_path = os.path.join(extract_to, '')
            os.makedirs(dest_path, exist_ok=True)
        else:
            dest_path = os.path.join(extract_to)
        for p in os.listdir(src_path):
            shutil.move(os.path.join(src_path, p), dest_path)
       
        # Mark the installation as complete
        self.installation_complete()

    # Install is complete
    def installation_complete(self):
        qtui.extractionProgressBar.setValue(100)
        if self.emulator == "Lime3DS":
            executable_path = os.path.normpath(os.path.join(qtui.installationPathLineEdit.text(), 'lime3ds-gui.exe'))
        elif self.emulator == "Citra" or self.emulator == "Citra-Enhanced":           
            executable_path = os.path.normpath(os.path.join(qtui.installationPathLineEdit.text(), 'citra-qt.exe')) # Declare exe path for the shortcuts
        elif self.emulator == "sudachi":
            executable_path = os.path.normpath(os.path.join(qtui.installationPathLineEdit.text(), 'sudachi.exe'))    
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
            winreg.CloseKey(self.registry_key)
            return self.regvalue, self.updatevalue  
        except FileNotFoundError:         
            pass
    # Function to create the reg values            
    def createreg (self):   
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}")
        self.registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.emulator}", 0, 
                                        winreg.KEY_WRITE)
        if self.install_mode == "Install":
            winreg.SetValueEx(self.registry_key, 'Install_Dir', 0, winreg.REG_SZ, qtui.installationPathLineEdit.text())
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
    app = QApplication(sys.argv)
    qtui = QtUi()
    qtui.show()
    self = Logic()
    sys.exit(app.exec())



