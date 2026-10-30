"""The one QApplication of the process (1.14.2: out of qt_window, so the splash screen can make it before the heavy
modules – the pages, PIL, numpy, the OCR – are even imported; qt_window re-exports ``application``)."""
from __future__ import annotations

import os
import sys

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

FIRA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "FiraSans-ExtraBold.ttf")   # = mapimage.FONT


def application() -> QApplication:
    """The one QApplication of the process (main thread, before any widget)."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv[:1])
        app.setStyle("Fusion")
        app.setQuitOnLastWindowClosed(False)          # closing goes through the App (quit / tray)
        QFontDatabase.addApplicationFont(FIRA)         # map names like on the map pictures
    return app
