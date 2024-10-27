from typing import overload

from PySide6.QtWidgets import QCheckBox, QWidget

from dread_mod_loader.settings import UserSettings, user_settings


class SavedCheckBox(QCheckBox):
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

        self.objectNameChanged.connect(self._on_object_name_changed)

        self.clicked_callback = None

    def set_to_setting(self) -> None:
        self.setChecked(self.settings[self.setting_name])

    def _on_object_name_changed(self, text: str) -> None:
        self.setting_name = "default_" + text

        self.set_to_setting()

        self.toggled.connect(self._on_clicked)

    def _on_clicked(self, checked: bool) -> None:
        self.settings[self.setting_name] = checked

        if self.clicked_callback:
            self.clicked_callback(checked)
