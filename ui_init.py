# Page imports
from imports import *
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui"))
from selection_page import SelectionPage
from welcome_page import WelcomePage
from install_page import InstallPage
from progress_bar import ProgressBarPage
from finish_page import FinishPage
from stylesheet import Style

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
        self.selection_page = SelectionPage()
        self.welcome_page = WelcomePage()
        self.install_page = InstallPage()
        self.progress_bar_page = ProgressBarPage()
        self.finish_page = FinishPage()
        self.widget_2_layout()
        self.load_stylesheet()

    def widget_2_layout(self):
        self.layout.addWidget(self.selection_page.emulatorSelectPage)
        self.layout.addWidget(self.welcome_page.welcomePage)
        self.layout.addWidget(self.install_page.installPage)
        self.layout.addWidget(self.progress_bar_page.progressBarPage)
        self.layout.addWidget(self.finish_page.finishPage)

    def load_stylesheet(app):
        app.setStyleSheet(Style.dark_stylesheet)



