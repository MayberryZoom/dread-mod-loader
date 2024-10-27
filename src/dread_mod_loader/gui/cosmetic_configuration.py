from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from dread_mod_loader.gui.custom_widgets.saved_checkbox import SavedCheckBox
from dread_mod_loader.gui.custom_widgets.saved_combo_box import SavedComboBox
from dread_mod_loader.gui.custom_widgets.saved_radio_button_group import (
    SavedRadioButtonGroup,
)
from dread_mod_loader.gui.custom_widgets.slider_with_spin_box import SliderWithSpinBox
from dread_mod_loader.gui.generated.cosmetic_configuration_ui import Ui_CosmeticConfiguration
from dread_mod_loader.settings import UserSettings


class CosmeticConfiguration(QWidget, Ui_CosmeticConfiguration):
    def __init__(self, parent: QWidget, settings: UserSettings, disabled: list = []) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.settings = settings

        # Make display checkboxes
        checkboxes = {
            "boss_lifebar_checkbox": "Boss lifebars",
            "enemy_lifebar_checkbox": "Enemy lifebars",
            "player_damage_checkbox": "Damage dealt by player",
            "enemy_damage_checkbox": "Damage dealt by enemies",
            "death_counter_checkbox": "Death counter",
        }

        for checkbox_name, checkbox_text in checkboxes.items():
            if checkbox_name not in disabled:
                checkbox = SavedCheckBox(self.settings, checkbox_text, self.display_box)
                checkbox.setObjectName(checkbox_name)

                setattr(self, checkbox_name, checkbox)
                self.display_layout.addWidget(checkbox)

        # Make room names combo box
        if "room_names_combo_box" not in disabled:
            self.room_names_layout = QHBoxLayout()
            self.room_names_layout.setObjectName("room_names_layout")

            self.room_names_label = QLabel("Room names on HUD", self.display_box)
            self.room_names_label.setObjectName("room_names_label")

            self.room_names_combo_box = SavedComboBox(self.settings, self.display_box)
            self.room_names_combo_box.addItems([
                "Never",
                "Always",
                "Fade Out",
            ])
            self.room_names_combo_box.setObjectName("room_names_combo_box")

            self.room_names_layout.addWidget(self.room_names_label)
            self.room_names_layout.addWidget(self.room_names_combo_box)
            self.display_layout.addLayout(self.room_names_layout)

        # Make volume sliders
        volume_sliders = [
            "Master",
            "Music",
            "SFX",
            "Environment",
            "Speech",
            "Grunt",
            "GUI",
        ]

        for slider_name in volume_sliders:
            if slider_name not in disabled:
                layout = SliderWithSpinBox(slider_name, self.settings, self)
                setattr(self, slider_name.replace(" ", "_").lower() + "_layout", layout)
                self.volume_layout.addLayout(layout)

        # Make door model radios
        door_covers = [
            "Diffusion Beam",
            "Ice Missile",
            "Storm Missile",
            "Bomb",
            "Cross Bomb",
            "Power Bomb",
            "Permanently Closed",
        ]

        for door_name in door_covers:
            if door_name not in disabled:
                layout = SavedRadioButtonGroup(door_name, ["Default", "Alternate"], self.settings, self)
                setattr(self, door_name.replace(" ", "_").lower() + "_layout", layout)
                self.doors_layout.addLayout(layout)

        # Remove disabled boxes
        if "display_box" in disabled:
            self.display_box.setParent(None)

        if "volume_box" in disabled:
            self.volume_box.setParent(None)

        if "doors_box" in disabled:
            self.doors_box.setParent(None)
