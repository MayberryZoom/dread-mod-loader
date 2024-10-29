import qdarktheme
from PySide6.QtWidgets import QDialog

from dread_mod_loader.gui.generated.configuration_dialog_ui import Ui_ConfigurationDialog
from dread_mod_loader.qss import qss

themes = ["auto", "dark", "light"]

class ConfigurationDialog(QDialog, Ui_ConfigurationDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.mods_dir_button.line_edit = self.mods_dir_line_edit

        self.theme_combo_box.changed_callback = self._update_theme

    def _update_theme(self, index: int):
        qdarktheme.setup_theme(themes[index], additional_qss=qss)
