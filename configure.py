import configparser
import os
from init_instances import inst
from win32api import MessageBeep
from win32con import MB_OK

class Configure:
    def __init__(self):
        self.config_dir = os.path.join(os.getenv('APPDATA'), 'Troppical')
        self.config_file = os.path.join(self.config_dir, 'config.ini')
        self.default_config = {
            'Settings': {
                'launch_as_admin': 'false',
                'default_install_path': os.path.join(os.environ['LOCALAPPDATA'])
            }
        }
        self.config = configparser.ConfigParser()
        self.current_config = self.load_config()

    def load_config(self):
        try:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)

            if os.path.exists(self.config_file):
                self.config.read(self.config_file)
            else:
                for section, values in self.default_config.items():
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
        for section, values in self.default_config.items():
            self.config.add_section(section)
            for key, value in values.items():
                self.config.set(section, key, str(value))
        return self.config

    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                self.config.write(f)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_setting(self, key, section='Settings'):
        try:
            value = self.config.get(section, key)
            # Convert string 'true'/'false' to boolean if needed
            if value.lower() in ('true', 'false'):
                return value.lower() == 'true'
            return value
        except:
            return self.default_config

    def set_setting(self, key, value, section='Settings'):
        self.config.set(section, key, str(value))
        self.save_config()

    def apply_settings(self):
        inst.settings.launchAsAdminCheckbox.setChecked(
            self.get_setting('launch_as_admin')
        )
        inst.settings.defaultInstallPath.setText(
            self.get_setting('default_install_path')
        )

    def handle_settings_button_apply(self):
        self.set_setting('launch_as_admin',
                        inst.settings.launchAsAdminCheckbox.isChecked())
        self.set_setting('default_install_path',
                        inst.settings.defaultInstallPath.text())

        self.apply_settings()
        inst.ui.qt_index_switcher(0)

        MessageBeep(MB_OK)