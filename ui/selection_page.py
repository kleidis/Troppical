from imports import *
from main import Online
from main import Logic

 # Emulator Select Page

class SelectionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.troppical_database = Online.fetch_data(self)
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

        for troppical_api_data in self.troppical_database:
            emulator_system = troppical_api_data['emulator_system']
            emulator_name = troppical_api_data['emulator_name']
            emulator_desc = troppical_api_data.get('emulator_desc', '')

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
            emulator_item.setToolTip(0, emulator_desc)

        # Sort the systems and emulators alphabetically
        self.emulatorTreeWidget.sortItems(0, Qt.SortOrder.AscendingOrder)
        for i in range(self.emulatorTreeWidget.topLevelItemCount()):
            system_item = self.emulatorTreeWidget.topLevelItem(i)
            system_item.sortChildren(0, Qt.SortOrder.AscendingOrder)

        # Set layout for the group and add to the main layout
        emulatorSelectGroup.setLayout(emulatorSelectGroupLayout)
        emulatorSelectLayout.addWidget(emulatorSelectGroup)
        self.emulatorSelectPage.setLayout(emulatorSelectLayout)  # Set the layout for the emulator selection page

        # Next button to confirm selection
        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(Logic.set_emulator)
        emulatorSelectLayout.addWidget(self.nextButton)

    def get_selected_emulator(self):
        selected_item = self.emulatorTreeWidget.currentItem()
        print(selected_item)
        if not selected_item or not selected_item.parent():
            QMessageBox.warning(self, "Selection Error", "Please select an emulator.")
            print("Please select an emulator.")
            return None
        return selected_item
