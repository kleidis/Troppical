from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from init_instances import inst
class Header():
    def header(self):
        # Header Layout
        self.headerLayout = QVBoxLayout()
        self.headerLayout.setContentsMargins(0, 20, 0, 0)
        # Icon Widget
        iconLabel = QLabel()
        icon = inst.online.fetch_and_process_main_icon()
        pixmap = icon.pixmap(180, 180)  # Specify the size directly
        iconLabel.setPixmap(pixmap)  # Set the pixmap to the label
        # Text Widget
        label = QLabel("<b><font size='10'>Troppical</font></b>")
        # Set Widgets
        self.headerLayout.addWidget(iconLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.headerLayout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        return self.headerLayout
