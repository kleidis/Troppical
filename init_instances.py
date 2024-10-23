# Lazy initialization using properties
class inst:
    _main = None #main.py
    _online = None #network_functions.py
    _download = None #network_functions.py
    _ui = None #ui_main.py
    _secondary_thread = None #ui_main.py
    _header = None #header.py
    _wel = None #welcome.py
    _sel = None #selection_page.py
    _act = None #act_page.py
    _install = None #install_page.py
    _bar = None #progress_bar.py
    _finish = None #finish_page.py

    @property
    def main(self):
        if self._main is None:
            from main import Main  # Import Main only when needed
            self._main = Main()
        return self._main

    @property
    def online(self):
        if self._online is None:
            from network.network_functions import Online  # Import Online from network_functions
            self._online = Online()
        return self._online

    @property
    def download(self):
        from network.network_functions import DownloadWorker
        return DownloadWorker()  # Always return a new instance to reset the thread

    @property
    def ui(self):
        if self._ui is None:
            from ui.ui_main import MainWindow  # Import MainWindow only when needed
            self._ui = MainWindow()
        return self._ui

    @property
    def secondary_thread(self):
        if self._secondary_thread is None:
            from ui.ui_main import Worker  # Import Worker only when needed
            self._secondary_thread = Worker()
        return self._secondary_thread

    @property
    def header(self):
        if self._header is None:
            from ui.header import Header  # Import Header only when needed
            self._header = Header()
        return self._header

    @property
    def wel(self):
        if self._wel is None:
            from ui.welcome_page import WelcomePage  # Import WelcomePage only when needed
            self._wel = WelcomePage()
        return self._wel

    @property
    def sel(self):
        if self._sel is None:
            from ui.selection_page import SelectionPage  # Import SelectionPage only when needed
            self._sel = SelectionPage()
        return self._sel

    @property
    def act(self):
        if self._act is None:
            from ui.act_page import ActPage  # Import WelcomePage only when needed
            self._act = ActPage()
        return self._act

    @property
    def install(self):
        if self._install is None:
            from ui.install_page import InstallPage  # Import InstallPage only when needed
            self._install = InstallPage()
        return self._install

    @property
    def bar(self):
        if self._bar is None:
            from ui.progress_bar import ProgressBarPage  # Import ProgressBarPage only when needed
            self._bar = ProgressBarPage()
        return self._bar

    @property
    def finish(self):
        if self._finish is None:
            from ui.finish_page import FinishPage  # Import FinishPage only when needed
            self._finish = FinishPage()
        return self._finish

# Create a single instance of the inst class
inst = inst()





