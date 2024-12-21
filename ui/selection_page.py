from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from init_instances import inst


# Emulator Select Page
class SelectionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.emulatorSelectPage = QWidget()
        emulatorSelectLayout = QVBoxLayout()

        headerLayout = QHBoxLayout()

        titleLabel = QLabel("Select your emulator from the list")
        titleLabel.setFont(QFont("Segoe UI", 11))
        headerLayout.addWidget(titleLabel)

        # Add stretch to push search box to right
        headerLayout.addStretch()

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search emulators...")
        self.searchBar.setFixedWidth(200)
        self.searchBar.setFixedHeight(32)
        self.searchBar.textChanged.connect(self.filter_emulators)
        headerLayout.addWidget(self.searchBar)

        emulatorSelectLayout.addLayout(headerLayout)

        self.emulatorTreeWidget = QTreeWidget()
        self.emulatorTreeWidget.setHeaderHidden(True)
        self.emulatorTreeWidget.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        emulatorSelectLayout.addWidget(self.emulatorTreeWidget)

        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()

        self.nextButton = QPushButton("Install")
        self.nextButton.setFixedHeight(28)
        self.nextButton.setMinimumWidth(80)
        self.nextButton.setFont(QFont("Segoe UI", 11))

        bottomLayout.addWidget(self.nextButton)
        emulatorSelectLayout.addLayout(bottomLayout)

        self.emulatorSelectPage.setLayout(emulatorSelectLayout)

    def filter_emulators(self, search_text):
        search_text = search_text.lower()

        for i in range(self.emulatorTreeWidget.topLevelItemCount()):
            system_item = self.emulatorTreeWidget.topLevelItem(i)
            system_visible = False

            for j in range(system_item.childCount()):
                emulator_item = system_item.child(j)
                emulator_name = emulator_item.text(0).lower()

                if search_text in emulator_name:
                    emulator_item.setHidden(False)
                    system_visible = True
                else:
                    emulator_item.setHidden(True)

            system_item.setHidden(not system_visible)

    def populate_emulator_tree(self):
        # Iterate over each emulator item and add it to the tree
        for emulatorName, data in inst.online.emulatorDatabase.items():
            emulatorSystem = data["system"]
            emulatorDesc = data["description"]
            icon = data["icon"]

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
