from typing import overload

from PySide6.QtWidgets import QComboBox, QWidget

from dread_mod_loader.settings import UserSettings, user_settings


class SavedComboBox(QComboBox):
    @overload
    def __init__(self, settings: UserSettings, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, parent: QWidget = None) -> None: ...

    def __init__(self, arg1, arg2 = None) -> None:
        if isinstance(arg1, UserSettings):
            parent = arg2
            self.settings = arg1
        else:
            parent = arg2
            self.settings = user_settings

        super().__init__(parent)

        self.objectNameChanged.connect(self._on_object_name_changed)

        self.changed_callback = None

    def set_to_setting(self) -> None:
        self.setCurrentIndex(self.settings[self.setting_name])

    def _on_object_name_changed(self, text: str):
        self.setting_name = "default_" + text

        self.set_to_setting()

        self.currentIndexChanged.connect(self._on_changed)

    def _on_changed(self, index: int) -> None:
        self.settings[self.setting_name] = index

        if self.changed_callback:
            self.changed_callback(index)
