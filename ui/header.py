from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
class Header():
    def header(self):
        # Header Layout
        self.headerLayout = QVBoxLayout()
        self.headerLayout.setContentsMargins(0, 20, 0, 0)
        # Icon Widget
        iconLabel = QLabel()
    #      icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        #   icon = QIcon(icon_path)
        #   pixmap = icon.pixmap(180, 180)  # Specify the size directly
        #   iconLabel.setPixmap(pixmap)
        # Text Widget
        label = QLabel("<b><font size='10'>Troppical</font></b>")
        # Set Widgets
        self.headerLayout.addWidget(iconLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.headerLayout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        return self.headerLayout
