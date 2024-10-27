import logging
import shutil
import sys
from pathlib import Path

import qdarktheme
from PySide6.QtWidgets import QApplication

from dread_mod_loader.gui.main_window import MainWindow
from dread_mod_loader.qss import qss
from dread_mod_loader.settings import user_settings

themes = ["auto", "dark", "light"]

logging.basicConfig(level=logging.INFO, format="[{asctime}] [{levelname}] [{name}] {message}", style="{")

shutil.rmtree(Path("temp"), True)

app = QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("Dread Mod Loader v0.0.0")
window.show()

qdarktheme.setup_theme(themes[user_settings["default_theme_combo_box"]], additional_qss=qss)

app.exec()
