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
        emulatorSelectLayout.addWidget(self.nextButton)


    def populate_emulator_tree(self,):
        # Iterate over each emulator item and add it to the tree
        for emulatorName, data in inst.online.emulatorDatabase.items():
            emulatorSystem = data['system']
            emulatorDesc = data['description']
            icon = data['icon']

            # Check if the emulator system already has a tree item, if not create one
            systemItem = None
            for i in range(self.emulatorTreeWidget.topLevelItemCount()):
                item = self.emulatorTreeWidget.topLevelItem(i)
                if item.text(0) == emulatorSystem:
                    systemItem = item
                    break

            if not systemItem:
                systemItem = QTreeWidgetItem(self.emulatorTreeWidget)
                systemItem.setText(0, emulatorSystem)
                systemItem.setExpanded(True)
                # Make the system item unselectable
                systemItem.setFlags(systemItem.flags() & ~Qt.ItemFlag.ItemIsSelectable)

            # Add the emulator to the appropriate tree item
            emulatorItem = QTreeWidgetItem(systemItem)
            emulatorItem.setText(0, emulatorName)
            emulatorItem.setIcon(0, icon)
            emulatorItem.setToolTip(0, emulatorDesc)

            # Close the initializing message
            inst.ui.initializingMsg.hide()

        # Sort the systems and emulators alphabetically
        self.emulatorTreeWidget.sortItems(0, Qt.SortOrder.AscendingOrder)
        for i in range(self.emulatorTreeWidget.topLevelItemCount()):
            systemItem = self.emulatorTreeWidget.topLevelItem(i)
            systemItem.sortChildren(0, Qt.SortOrder.AscendingOrder)