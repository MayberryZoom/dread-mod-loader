from PySide6.QtWidgets import QWidget

from dread_mod_loader.gui.custom_widgets.saved_checkbox import SavedCheckBox
from dread_mod_loader.gui.settings_dialog import SettingsDialog
from dread_mod_loader.settings import UserSettings


class MySettings(SettingsDialog):
    def __init__(self, parent: QWidget, settings: UserSettings, disabled: list = []):
        super().__init__(parent, settings, disabled)

        test_checkbox = SavedCheckBox(settings, "Testing setting")
        test_checkbox.setObjectName("test_checkbox")
        self.cosmetic_tab.display_layout.addWidget(test_checkbox)
