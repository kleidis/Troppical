# Page imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedLayout, QMessageBox, QLabel
from stylesheet import Style
import requests
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtCore import Qt, QByteArray, QObject, QThread, pyqtSignal
from init_instances import inst


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'Troppical - {"version"}')  # Window name with version
        self.setCentralWidget(QWidget(self))  # Set a central widget
        self.layout = QStackedLayout(self.centralWidget())  # Set the layout on the central widget
        self.setMaximumSize(1000, 720)  # Set the maximum window size to 1280x720
        self.setMinimumSize(1000, 720)  # Set the minimum window size to 800x600
        # Set the window icon
        #   icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        #   self.setWindowIcon(QIcon(icon_path))
        self.load_stylesheet()
        # Initialize the first page
        self.layout.addWidget(inst.wel.welcomePage)

        # Connect buttons after initialization
        self.connect_buttons()

        self.shared_thread = None  # Initialize shared_thread to None

    def connect_buttons(self):
        # Connect buttons to the qt_button_click method
        inst.wel.manageButton.clicked.connect(self.qt_button_click)
        inst.act.installButton.clicked.connect(self.qt_button_click)
        inst.act.updateButton.clicked.connect(self.qt_button_click)
        inst.act.uninstallButton.clicked.connect(self.qt_button_click)
        inst.install.install_emu_button.clicked.connect(self.qt_button_click)
        inst.act.backButton.clicked.connect(self.qt_button_click)

    def widget_2_layout(self):
        # Add actual pages instead of placeholders
        self.layout.addWidget(inst.sel.emulatorSelectPage)
        self.layout.addWidget(inst.wel.welcomePage)
        self.layout.addWidget(inst.install.installPage)
        self.layout.addWidget(inst.bar.progressBarPage)
        self.layout.addWidget(inst.finish.finishPage)

    def initialize_page(self, index):
        # Mapping of index to page attributes and instances
        page_map = {
            1: ('selection_page', inst.sel, 'emulatorSelectPage'),
            2: ('welcome_page', inst.wel, 'welcomePage'),
            3: ('install_page', inst.install, 'installPage'),
            4: ('progress_bar_page', inst.bar, 'progressBarPage'),
            5: ('finish_page', inst.finish, 'finishPage')
        }

        # Initialize and replace the widget for the given index
        if index in page_map:
            attr_name, instance, widget_name = page_map[index]
            setattr(self, attr_name, instance)
            widget = getattr(instance, widget_name)
            self.layout.replaceWidget(self.layout.widget(index), widget)
            self.layout.setCurrentIndex(index)
            print(f"Page {index} initialized: {attr_name}")

    def load_stylesheet(self):
        self.setStyleSheet(Style.dark_stylesheet)

    def qt_button_click(self):
        self.widget_2_layout()
        button = self.sender()

        # Define a mapping of buttons to their actions
        button_actions = {
            inst.wel.manageButton: 1,  # Assuming index 1 is the manage page
            inst.act.installButton: 2,
            inst.act.updateButton: inst.main.emulator_updates,
            inst.act.uninstallButton: self.handle_uninstall,
            inst.install.install_emu_button: 3,
            inst.act.backButton: self.handle_back
        }

        # Execute the corresponding action if the button is in the mapping
        action = button_actions.get(button)
        if isinstance(action, int):
            self.initialize_page(action)
        elif callable(action):
            action()

    def handle_manage(self):
        self.layout.setCurrentIndex(1)  # Assuming index 1 is the desired page
    def handle_install(self):
        inst.main.install_mode = "Install"
        self.layout.setCurrentIndex(2)
        inst.main.Add_releases_to_combobox()
    def handle_uninstall(self):
        inst.main.install_mode = "Uninstall"  # Unused for now
        inst.main.uninstall()
    def handle_install_emu(self):
        self.layout.setCurrentIndex(3)
        inst.main.Prepare_Download()
    def handle_back(self):
        current_index = self.layout.currentIndex()
        if current_index > 0:
            self.layout.setCurrentIndex(current_index - 1)

    def initialize_emulator_database(self):
        # Check if the message box is already shown
        if hasattr(self, 'initializing_msg') and self.initializing_msg.isVisible():
            return

        # Show initializing message
        self.initializing_msg = QMessageBox(self)
        self.initializing_msg.setWindowTitle("Troppical API")
        self.initializing_msg.setText("Getting emulator data...")
        self.initializing_msg.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.initializing_msg.show()

        # Start the secondary thread with the task and callback
        self.start_secondary_thread(inst.online.filter_emulator_data, lambda: inst.sel.populate_emulator_tree())

    def start_secondary_thread(self, task, callback, *args, **kwargs):
        if self.shared_thread is not None:
            self.shared_thread.quit()
            self.shared_thread.wait()

        self.shared_thread = QThread()
        worker = inst.secondary_thread
        worker.set_task(task, *args, **kwargs)
        worker.moveToThread(self.shared_thread)
        worker.finished.connect(callback)
        self.shared_thread.started.connect(worker.run)
        self.shared_thread.start()

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