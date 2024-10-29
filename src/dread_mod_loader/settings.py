import json
import os
from pathlib import Path
from typing import Any

from dread_mod_loader.logger import LOG


# Custom dict that overrides setters to always save to the settings file
class UserSettings(dict):
    def __init__(self, settings_path: Path, default_settings: dict[str, Any] = {}):
        super().__init__()

        self.default_settings = default_settings
        self.settings_path = settings_path

        self._load()

    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, value)

        LOG.info(f"{self.settings_path}: Setting {key} to {value}")
        self._save()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        self._save()

    def _save(self):
        LOG.info("Saving user settings")

        self.settings_path.parent.mkdir(parents=True, exist_ok=True)

        with self.settings_path.open("w+", encoding="UTF-8") as file:
            json.dump(self, file)

    def _load(self):
        LOG.info("Loading " + self.settings_path.as_posix())

        if self.settings_path.exists():
            with self.settings_path.open(encoding="UTF-8") as file:
                super().update(json.load(file))

            # If anything is missing from the user settings, default it
            for k, v in self.default_settings.items():
                if k not in self:
                    self[k] = v
        else:
            LOG.info("No user settings!")
            self.update(self.default_settings)

# General settings
user_settings_dir = Path(os.environ["APPDATA"] + "/Dread Mod Loader")

default_settings = {
    # General
    "default_mods_dir_line_edit": Path("./mods").resolve().as_posix(),
    "seen_help": False,

    # Preferences
    "default_theme_combo_box": 0,

    # Export window
    "default_export_combo_box": 0,
    "default_input_romfs_line_edit": "",
    "default_ryujinx_path_line_edit": Path(os.environ["APPDATA"] + "\\Ryujinx").as_posix(),
    "default_switch_method": 0,
    "default_smm_checkbox": True,
    "default_ftp_ip_line_edit": "",
    "default_ftp_port_line_edit": "",
    "default_ftp_username_line_edit": "",
    "default_ftp_password_line_edit": "",
    "default_ftp_anonymous_checkbox": True,
    "default_usb_combo_box": "",
    "default_advanced_romfs_line_edit": "",
    "default_advanced_exefs_line_edit": "",
    "default_advanced_exefs_patches_line_edit": "",
    "default_advanced_format_combo_box": 0,
}

user_settings = UserSettings(user_settings_dir / "settings.json", default_settings)
