from win32mica import ApplyMica, MicaTheme, MicaStyle
from PyQt6.QtCore import Qt

def apply_mica(window):
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    hwnd = window.winId().__int__()

    mode = MicaTheme.DARK
    style = MicaStyle.DEFAULT

    # Enable extended composition
    ApplyMica(HWND=hwnd, Theme=mode, Style=style)

