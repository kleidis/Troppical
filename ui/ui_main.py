import os
import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QStackedLayout, QMessageBox
from stylesheet import Style
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from init_instances import inst
from utils.mica import apply_mica
import version

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sharedThread = None  # Thread used for secondary function purposes

        self.setWindowTitle(f'Troppical - {version.version}')  # Window name. TODO: Add version
        self.setCentralWidget(QWidget(self))
        self.layout = QStackedLayout(self.centralWidget())  # Set the layout on the central widget
        self.setMaximumSize(1000, 720)  # Set the maximum window size to 1280x720
        self.setMinimumSize(1000, 720)  # Set the minimum window size to 800x600
        icon = inst.online.fetch_and_process_main_icon()
        self.setWindowIcon(icon)

        self.segoe_ui = QFont("Segoe UI", 10)
        self.setFont(self.segoe_ui)
        self.load_stylesheet()
        if getattr(sys, 'frozen', False):
            inst.updater.check_for_update()
        self.widget_2_layout()
        self.connect_buttons()
        self.init_settings()

    def connect_buttons(self):
        inst.header.header()
        inst.wel.configureButton.clicked.connect(self.qt_button_click)
        inst.wel.manageButton.clicked.connect(self.qt_button_click)
        inst.sel.nextButton.clicked.connect(self.qt_button_click)
        inst.act.installButton.clicked.connect(self.qt_button_click)
        inst.act.updateButton.clicked.connect(self.qt_button_click)
        inst.act.uninstallButton.clicked.connect(self.qt_button_click)
        inst.install.install_emu_button.clicked.connect(self.qt_button_click)
        inst.act.backButton.clicked.connect(self.qt_button_click)
        inst.finish.finishButton.clicked.connect(self.qt_button_click)
        inst.finish.installAnotherButton.clicked.connect(self.qt_button_click)
        inst.wel.settingsButton.clicked.connect(self.qt_button_click)
        inst.settings.applyButton.clicked.connect(self.qt_button_click)

    def widget_2_layout(self):
        self.layout.addWidget(inst.wel.welcomePage)
        self.layout.addWidget(inst.sel.emulatorSelectPage)
        self.layout.addWidget(inst.act.actPage)
        self.layout.addWidget(inst.install.installPage)
        self.layout.addWidget(inst.bar.progressBarPage)
        self.layout.addWidget(inst.finish.finishPage)
        self.layout.addWidget(inst.settings.settingsPage)

    def qt_index_switcher(self, index):
        # Mapping of index to page attributes and instances
        pageMap = {
            0: ('welcome_page', inst.wel, 'welcomePage'),
            1: ('selection_page', inst.sel, 'emulatorSelectPage'),
            2: ('act_page', inst.act, 'actPage'),
            3: ('install_page', inst.install, 'installPage'),
            4: ('progress_bar_page', inst.bar, 'progressBarPage'),
            5: ('finish_page', inst.finish, 'finishPage'),
            6: ('settings_page', inst.settings, 'settingsPage')
        }

        if index in pageMap:
            attrName, instance, widgetName = pageMap[index]
            setattr(self, attrName, instance)
            widget = getattr(instance, widgetName)
            self.layout.replaceWidget(self.layout.widget(index), widget)
            self.layout.setCurrentIndex(index)

    def load_stylesheet(self):
        if sys.getwindowsversion().build >= 22000:
            apply_mica(self)
        self.setStyleSheet(Style.dark_stylesheet)

    def init_settings(self):
        try:
            inst.config.load_config()

            settings_map = {
                'launch_as_admin': inst.settings.launchAsAdminCheckbox,
                'default_install_path': inst.settings.defaultInstallPath
            }

            for setting_key, ui_element in settings_map.items():
                if hasattr(ui_element, 'setChecked'):  # For checkboxes
                    ui_element.setChecked(inst.config.get_setting(setting_key))
                elif hasattr(ui_element, 'setText'):  # For text inputs
                    ui_element.setText(inst.config.get_setting(setting_key))
        except Exception as e:
            print(f"Error initializing settings: {e}")


    def qt_button_click(self):
        button = self.sender()

        # Define a mapping of buttons to their actions
        buttonActions = {
            inst.wel.manageButton: self.handle_manage,
            inst.wel.configureButton: self.handle_settings,
            inst.sel.nextButton: self.handle_select,
            inst.act.installButton: self.handle_install,
            inst.act.updateButton: inst.main.emulator_updater,
            inst.act.uninstallButton: self.handle_uninstall,
            inst.install.install_emu_button: self.handle_install_emu,
            inst.finish.finishButton: self.handle_finish,
            inst.finish.installAnotherButton: self.handle_finish,
            inst.act.backButton: self.handle_back,
            inst.wel.settingsButton: self.handle_settings,
            inst.settings.applyButton: inst.config.handle_settings_button_apply,
        }

        action = buttonActions.get(button)
        if isinstance(action, int):
            self.qt_index_switcher(action)
        elif callable(action):
            action()

    def handle_manage(self):
        if not hasattr(self, 'emulatorDatabaseInitialized') or not self.emulatorDatabaseInitialized:
            self.initialize_emulator_database()
            self.emulatorDatabaseInitialized = True
        inst.ui.qt_index_switcher(1)
    def handle_select(self):
        if inst.main.set_emulator():
            inst.ui.qt_index_switcher(2)
    def handle_install(self):
        inst.main.installMode = "Install"
        inst.ui.qt_index_switcher(3)
        inst.main.Add_releases_to_combobox()
    def handle_uninstall(self):
        inst.main.installMode = "Uninstall"  # Unused for now
        inst.main.uninstall()
    def handle_install_emu(self):
        inst.ui.qt_index_switcher(4)
        inst.main.Prepare_Download()
    def handle_finish(self):
        button = self.sender()
        if button == inst.finish.installAnotherButton:
            self.layout.setCurrentIndex(0)
            inst.bar.downloadProgressBar.setValue(0)
            inst.bar.extractionProgressBar.setValue(0)
            setattr(inst.main, 'installMode', None)
            setattr(inst.main, 'selection', None)
            inst.install.desktopShortcutCheckbox.setChecked(False)
            inst.install.startMenuShortcutCheckbox.setChecked(False)
        elif button == inst.finish.finishButton:
            self.close()
    def handle_back(self):
        currentIndex = self.layout.currentIndex()
        if currentIndex > 0:
            self.layout.setCurrentIndex(currentIndex - 1)
    def handle_settings(self):
        inst.ui.qt_index_switcher(6)

    def initialize_emulator_database(self):
        # Check if the message box is already shown
        if hasattr(self, 'initializingMsg') and self.initializingMsg.isVisible():
            return

        # Show initializing message
        self.initializingMsg = QMessageBox(self)
        self.initializingMsg.setWindowTitle("Troppical API")
        self.initializingMsg.setText("Getting emulator data...")
        self.initializingMsg.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.initializingMsg.show()

        # Start the secondary thread with the task and callback
        self.start_secondary_thread(inst.online.filter_emulator_data, lambda: inst.sel.populate_emulator_tree())

    def start_secondary_thread(self, task, callback, *args, **kwargs):
        if self.sharedThread is not None:
            self.sharedThread.quit()
            self.sharedThread.wait()

        self.sharedThread = QThread()
        worker = inst.secondary_thread
        worker.set_task(task, *args, **kwargs)
        worker.moveToThread(self.sharedThread)
        worker.finished.connect(callback)
        self.sharedThread.started.connect(worker.run)
        self.sharedThread.start()

    # Disable buttons depanding on if it the program is already installed
    def disable_qt_buttons_if_installed(self):
        installationStatus = inst.main.update_reg_result()

        if installationStatus is None:
            inst.act.installButton.setEnabled(True)
            inst.act.updateButton.setEnabled(False)
            inst.act.uninstallButton.setEnabled(False)
        else:
            inst.act.installButton.setEnabled(False)
            inst.act.updateButton.setEnabled(True)
            inst.act.uninstallButton.setEnabled(True)

class Worker(QObject):
    finished = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.task = None
        self.args = ()
        self.kwargs = {}

    def set_task(self, task, *args, **kwargs):
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if self.task is not None:
            result = self.task(*self.args, **self.kwargs)
            self.finished.emit(result)

