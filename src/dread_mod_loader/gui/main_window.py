from pathlib import Path

from PySide6.QtWidgets import QMainWindow

from dread_mod_loader.gui.configuration_dialog import ConfigurationDialog
from dread_mod_loader.gui.generated.main_window_ui import Ui_MainWindow
from dread_mod_loader.load_mods import load_mods
from dread_mod_loader.settings import user_settings


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.refresh_mods()

    def refresh_mods(self) -> None:
        # Removing the mods in top down order causes weirdness, so reverse the range
        for i in reversed(range(self.mod_list_contents.layout().count())):
            self.mod_list_contents.layout().itemAt(i).widget().setParent(None)

        mods = load_mods(Path(user_settings["mods_dir"]))

        for mod_name, mod in mods.items():
            self.mod_list_contents.layout().addWidget(mod)

    def show_configuration_dialog(self) -> None:
        configuration_dialog = ConfigurationDialog(self)
        configuration_dialog.exec()
