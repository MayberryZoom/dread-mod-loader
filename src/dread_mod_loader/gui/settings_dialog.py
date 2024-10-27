from PySide6.QtWidgets import QDialog, QWidget

from dread_mod_loader.gui.cosmetic_configuration import CosmeticConfiguration
from dread_mod_loader.gui.generated.settings_dialog_ui import Ui_SettingsDialog
from dread_mod_loader.settings import UserSettings


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent: QWidget, settings: UserSettings, disabled: list = []) -> None:
        super().__init__(parent)

        self.setupUi(self)

        self.settings = settings

        self.cosmetic_tab = CosmeticConfiguration(self, self.settings, disabled)
        self.tabs.addTab(self.cosmetic_tab, "Cosmetic")
