import os
from typing import overload

from PySide6.QtWidgets import QComboBox, QWidget

from dread_mod_loader.settings import UserSettings, user_settings


class USBComboBox(QComboBox):
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

        self.addItems(os.listdrives())
        self.objectNameChanged.connect(self._on_object_name_changed)

        self.changed_callback = None

    def mousePressEvent(self, event) -> None:
        self.clear()
        self.addItems(os.listdrives())

        super().mousePressEvent(event)

    def _on_object_name_changed(self, text: str) -> None:
        self.setting_name = "default_" + text

        self.setCurrentText(self.settings[self.setting_name])

        self.currentTextChanged.connect(self._on_changed)

    def _on_changed(self, text: str) -> None:
        self.settings[self.setting_name] = text

        if self.changed_callback:
            self.changed_callback(text)
