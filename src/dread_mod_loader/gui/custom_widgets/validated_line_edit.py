from pathlib import Path
from typing import overload

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLineEdit, QWidget

from dread_mod_loader.settings import UserSettings, user_settings


class ValidatedLineEdit(QLineEdit):
    @overload
    def __init__(self, settings: UserSettings, text: str, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, text: str, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, parent: QWidget = None) -> None: ...

    def __init__(self, arg1, arg2 = None, arg3 = None) -> None:
        if isinstance(arg1, UserSettings):
            super().__init__(arg2, arg3)
            self.settings = arg1
        elif isinstance(arg1, str):
            super().__init__(arg1, arg2)
            self.settings = user_settings
        else:
            super().__init__(arg1)
            self.settings = user_settings

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.on_updated)

        self.objectNameChanged.connect(self._on_object_name_changed)

        self.update_callback = None

    def set_to_setting(self) -> None:
        self.setText(self.settings[self.setting_name])

    def _on_object_name_changed(self, text: str):
        self.setting_name = "default_" + text

        self.set_to_setting()

        self.textEdited.connect(self.timer.start)

    def on_updated(self) -> None:
        self.settings[self.setting_name] = self.text()

        if self.update_callback:
            self.update_callback()

    def set_valid(self, is_valid: bool) -> bool:
        """Sets styling
        @param is_valid: True for normal border, False for red border
        @returns: the value of is_valid"""
        if is_valid:
            self.setStyleSheet("")
        else:
            self.setStyleSheet("border: 1px solid red")

        return is_valid

    def validate_not_empty(self) -> bool:
        return self.set_valid(self.text() != "")

    def validate_files(self, files_to_check: list[str]) -> bool:
        path = Path(self.text())

        for file in files_to_check:
            if not (path / file).exists():
                return self.set_valid(False)

        return self.set_valid(True)
