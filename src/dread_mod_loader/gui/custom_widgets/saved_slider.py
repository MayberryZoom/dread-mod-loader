from typing import overload

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget

from dread_mod_loader.gui.custom_widgets.non_scrollable_slider import (
    NonScrollableSlider,
)
from dread_mod_loader.settings import UserSettings, user_settings


class SavedSlider(NonScrollableSlider):
    @overload
    def __init__(self, settings: UserSettings, orientation: Qt.Orientation, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, orientation: Qt.Orientation, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, parent: QWidget = None) -> None: ...

    def __init__(self, arg1, arg2 = None, arg3 = None) -> None:
        if isinstance(arg1, UserSettings):
            super().__init__(arg2, arg3)
            self.settings = arg1
        elif isinstance(arg1, Qt.Orientation):
            super().__init__(arg1, arg2)
            self.settings = user_settings
        else:
            super().__init__(arg1)
            self.settings = user_settings

        self.objectNameChanged.connect(self._on_object_name_changed)

        self.value_changed_callback = None

    def set_to_setting(self) -> None:
        self.setValue(self.settings[self.setting_name])

    def _on_object_name_changed(self, text: str) -> None:
        self.setting_name = "default_" + text

        self.set_to_setting()

        self.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value: int) -> None:
        self.settings[self.setting_name] = value

        if self.value_changed_callback:
            self.value_changed_callback(value)
