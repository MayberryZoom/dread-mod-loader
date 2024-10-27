from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractButton,
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QWidget,
)

from dread_mod_loader.settings import UserSettings


class SavedRadioButtonGroup(QHBoxLayout):
    def __init__(self, group_name: str, radios: list[str], settings: UserSettings, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.settings = settings

        group_id = group_name.lower().replace(" ", "_")

        self.setObjectName(f"{group_id}_layout")

        self.label = QLabel(group_name, parent)
        self.label.setObjectName(f"{group_id}_radio_label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if parent:
            setattr(parent, self.label.objectName(), self.label)

        self.addWidget(self.label)

        self.button_group = QButtonGroup(parent)
        self.button_group.setObjectName(f"{group_id}_radio_button_group")

        for radio_name in radios:
            radio_id = radio_name.lower().replace(" ", "_")

            radio_button = QRadioButton(radio_name, parent)
            radio_button.setObjectName(f"{group_id}_radio_{radio_id}")

            self.button_group.addButton(radio_button)
            self.addWidget(radio_button)

            setattr(self, radio_button.objectName(), radio_button)
            if parent:
                setattr(parent, radio_button.objectName(), radio_button)

        getattr(self, self.settings["default_" + self.button_group.objectName()]).setChecked(True)

        self.button_group.buttonClicked.connect(self._on_button_clicked)

    def _on_button_clicked(self, button: QAbstractButton) -> None:
        self.settings["default_" + self.button_group.objectName()] = button.objectName()
