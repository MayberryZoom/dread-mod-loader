import os
from pathlib import Path

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMainWindow

from dread_mod_loader import get_docs_path
from dread_mod_loader.gui.configuration_dialog import ConfigurationDialog
from dread_mod_loader.gui.generated.main_window_ui import Ui_MainWindow
from dread_mod_loader.gui.markdown_dialog import MarkdownDialog
from dread_mod_loader.load_mods import load_mods
from dread_mod_loader.settings import user_settings


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.refresh_mods()

        if not user_settings["seen_help"]:
            self._show_general_help()

            user_settings["seen_help"] = True

    def refresh_mods(self) -> None:
        # Removing the mods in top down order causes weirdness, so reverse the range
        for i in reversed(range(self.mod_list_contents.layout().count())):
            self.mod_list_contents.layout().itemAt(i).widget().setParent(None)

        self.mods = load_mods(Path(user_settings["default_mods_dir_line_edit"]))

        for mod_name, mod in self.mods.items():
            self.mod_list_contents.layout().addWidget(mod)

    def _open_mods_dir(self) -> None:
        mods_dir = os.path.realpath(user_settings["default_mods_dir_line_edit"])
        os.startfile(mods_dir)

    def show_configuration_dialog(self) -> None:
        configuration_dialog = ConfigurationDialog(self)
        configuration_dialog.exec()

    def _show_general_help(self) -> None:
        help_dialog = MarkdownDialog(get_docs_path() / "general", self, Qt.WindowType.Window)
        help_dialog.setWindowTitle("General Help")
        help_dialog.show()

    def _show_developer_help(self) -> None:
        help_dialog = MarkdownDialog(get_docs_path() / "dev", self, Qt.WindowType.Window)
        help_dialog.setWindowTitle("Developer Help")
        help_dialog.show()
