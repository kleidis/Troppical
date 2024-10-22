from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTreeWidget, QTreeWidgetItem, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from init_instances import inst

# Emulator Select Page

class SelectionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.emulatorSelectPage = QWidget()
        emulatorSelectLayout = QVBoxLayout()
        emulatorSelectGroup = QGroupBox("Select your emulator from the list")
        emulatorSelectGroupLayout = QVBoxLayout()

        # Create a QTreeWidget
        self.emulatorTreeWidget = QTreeWidget()
        self.emulatorTreeWidget.setHeaderHidden(True)
        self.emulatorTreeWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        emulatorSelectGroupLayout.addWidget(self.emulatorTreeWidget)

        # Set layout for the group and add to the main layout
        emulatorSelectGroup.setLayout(emulatorSelectGroupLayout)
        emulatorSelectLayout.addWidget(emulatorSelectGroup)
        self.emulatorSelectPage.setLayout(emulatorSelectLayout)  # Set the layout for the emulator selection page

        # Next button to confirm selection
        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(lambda: inst.main.set_emulator(self))
        emulatorSelectLayout.addWidget(self.nextButton)

        inst.ui.initialize_emulator_database()

    def populate_emulator_tree(self,):
        # Iterate over each emulator item and add it to the tree
        for emulator_name, data in inst.online.emulator_database.items():
            emulator_system = data['system']
            emulator_desc = data['description']
            icon = data['icon']
            print(f"Fetching data for {emulator_name}")

            # Check if the emulator system already has a tree item, if not create one
            system_item = None
            for i in range(self.emulatorTreeWidget.topLevelItemCount()):
                item = self.emulatorTreeWidget.topLevelItem(i)
                if item.text(0) == emulator_system:
                    system_item = item
                    break

            if not system_item:
                system_item = QTreeWidgetItem(self.emulatorTreeWidget)
                system_item.setText(0, emulator_system)
                system_item.setExpanded(True)
                # Make the system item unselectable
                system_item.setFlags(system_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)

            # Add the emulator to the appropriate tree item
            emulator_item = QTreeWidgetItem(system_item)
            emulator_item.setText(0, emulator_name)
            emulator_item.setIcon(0, icon)
            emulator_item.setToolTip(0, emulator_desc)

            # Close the initializing message
            inst.ui.initializing_msg.hide()

        # Sort the systems and emulators alphabetically
        self.emulatorTreeWidget.sortItems(0, Qt.SortOrder.AscendingOrder)
        for i in range(self.emulatorTreeWidget.topLevelItemCount()):
            system_item = self.emulatorTreeWidget.topLevelItem(i)
            system_item.sortChildren(0, Qt.SortOrder.AscendingOrder)



    def get_selected_emulator(self):
        selected_item = self.emulatorTreeWidget.currentItem()
        print(selected_item)
        if not selected_item or not selected_item.parent():
            QMessageBox.warning(self, "Selection Error", "Please select an emulator.")
            print("Please select an emulator.")
            return None
        return selected_item
