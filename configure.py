import configparser
import os
from init_instances import inst
from win32api import MessageBeep
from win32con import MB_OK


class Configure:
    def __init__(self):
        self.configDir = os.path.join(os.getenv("APPDATA"), "Troppical")
        self.configFile = os.path.join(self.configDir, "config.ini")
        self.defaultConfig = {
            "Settings": {
                "launch_as_admin": "false",
                "default_install_path": os.path.join(os.environ["LOCALAPPDATA"]),
            }
        }
        self.config = configparser.ConfigParser()
        self.currentConfig = self.load_config()

    def load_config(self):
        try:
            if not os.path.exists(self.configDir):
                os.makedirs(self.configDir)

            if os.path.exists(self.configFile):
                self.config.read(self.configFile)
            else:
                for section, values in self.defaultConfig.items():
                    if not self.config.has_section(section):
                        self.config.add_section(section)
                    for key, value in values.items():
                        self.config.set(section, key, str(value))
                self.save_config()

            return self.config
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.create_default_config()

    def create_default_config(self):
        self.config = configparser.ConfigParser()
        for section, values in self.defaultConfig.items():
            self.config.add_section(section)
            for key, value in values.items():
                self.config.set(section, key, str(value))
        return self.config

    def save_config(self):
        try:
            with open(self.configFile, "w") as f:
                self.config.write(f)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_setting(self, key, section="Settings"):
        try:
            value = self.config.get(section, key)
            if value.lower() in ("true", "false"):
                return value.lower() == "true"
            return value
        except:
            return self.defaultConfig

    def set_setting(self, key, value, section="Settings"):
        self.config.set(section, key, str(value))
        self.save_config()

    def apply_settings(self):
        inst.settings.launchAsAdminCheckbox.setChecked(
            self.get_setting("launch_as_admin")
        )
        inst.settings.defaultInstallPath.setText(
            self.get_setting("default_install_path")
        )

    def handle_settings_button_apply(self):
        self.set_setting(
            "launch_as_admin", inst.settings.launchAsAdminCheckbox.isChecked()
        )
        self.set_setting(
            "default_install_path", inst.settings.defaultInstallPath.text()
        )

        self.apply_settings()
        inst.ui.qt_index_switcher(0)

        MessageBeep(MB_OK)
