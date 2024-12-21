# Lazy initialization using properties


class inst:
    _main = None  # main.py
    _online = None  # network_functions.py
    _download = None  # network_functions.py
    _ui = None  # ui_main.py
    _secondary_thread = None  # ui_main.py
    _header = None  # header.py
    _wel = None  # welcome.py
    _sel = None  # selection_page.py
    _act = None  # act_page.py
    _install = None  # install_page.py
    _bar = None  # progress_bar.py
    _finish = None  # finish_page.py
    _settings = None  # settings_page.py
    _config = None  # configure.py
    _updater = None  # updater.py

    @property
    def main(self):
        if self._main is None:
            from main import Main

            self._main = Main()
        return self._main

    @property
    def online(self):
        if self._online is None:
            from network.network_functions import (
                Online,
            )

            self._online = Online()
        return self._online

    @property
    def download(self):
        from network.network_functions import DownloadWorker

        return DownloadWorker()

    @property
    def ui(self):
        if self._ui is None:
            from ui.ui_main import MainWindow

            self._ui = MainWindow()
        return self._ui

    @property
    def secondary_thread(self):
        if self._secondary_thread is None:
            from ui.ui_main import Worker

            self._secondary_thread = Worker()
        return self._secondary_thread

    @property
    def header(self):
        if self._header is None:
            from ui.header import Header

            self._header = Header()
        return self._header

    @property
    def wel(self):
        if self._wel is None:
            from ui.welcome_page import (
                WelcomePage,
            )

            self._wel = WelcomePage()
        return self._wel

    @property
    def sel(self):
        if self._sel is None:
            from ui.selection_page import (
                SelectionPage,
            )

            self._sel = SelectionPage()
        return self._sel

    @property
    def act(self):
        if self._act is None:
            from ui.act_page import ActPage

            self._act = ActPage()
        return self._act

    @property
    def install(self):
        if self._install is None:
            from ui.install_page import (
                InstallPage,
            )

            self._install = InstallPage()
        return self._install

    @property
    def bar(self):
        if self._bar is None:
            from ui.progress_bar import (
                ProgressBarPage,
            )

            self._bar = ProgressBarPage()
        return self._bar

    @property
    def finish(self):
        if self._finish is None:
            from ui.finish_page import FinishPage

            self._finish = FinishPage()
        return self._finish

    @property
    def settings(self):
        if self._settings is None:
            from ui.settings_page import (
                SettingsPage,
            )

            self._settings = SettingsPage()
        return self._settings

    @property
    def config(self):
        if self._config is None:
            from configure import Configure

            self._config = Configure()
        return self._config

    @property
    def updater(self):
        if self._updater is None:
            from network.updater import Updater

            self._updater = Updater()
        return self._updater


inst = inst()
