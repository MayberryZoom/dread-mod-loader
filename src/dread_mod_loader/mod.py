import shutil
from copy import deepcopy
from pathlib import Path

from mercury_engine_data_structures.file_tree_editor import OutputFormat
from open_dread_rando.dread_patcher import (
    LuaEditor,
    apply_patches,
    include_depackager,
    patch_exefs,
    validate,
)
from open_dread_rando.patcher_editor import PatcherEditor
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QWidget

from dread_mod_loader.gui.export_dialog import ExportDialog, ExportParams
from dread_mod_loader.gui.generated.mod_widget_ui import Ui_DreadMod
from dread_mod_loader.settings import UserSettings, user_settings_dir

room_names = ["NEVER", "ALWAYS", "WITH_FADE"]

disabled_settings_info = {
    # Display
    "display": {
        "settings": [
            "default_boss_lifebar_checkbox",
            "default_enemy_lifebar_checkbox",
            "default_player_damage_checkbox",
            "default_enemy_damage_checkbox",
            "default_death_counter_checkbox",
            "default_room_names_combo_box",
        ],
        "widgets": [
            "display_box",
            "boss_lifebar_checkbox",
            "enemy_lifebar_checkbox",
            "player_damage_checkbox",
            "enemy_damage_checkbox",
            "death_counter_checkbox",
            "room_names_combo_box",
        ],
    },
    "boss_lifebar": {
        "settings": ["default_boss_lifebar_checkbox",],
        "widgets": ["boss_lifebar_checkbox"],
    },
    "enemy_lifebar": {
        "settings": ["default_enemy_lifebar_checkbox",],
        "widgets": ["enemy_lifebar_checkbox"],
    },
    "player_damage": {
        "settings": ["default_player_damage_checkbox",],
        "widgets": ["player_damage_checkbox"],
    },
    "enemy_damage": {
        "settings": ["default_enemy_damage_checkbox",],
        "widgets": ["enemy_damage_checkbox"],
    },
    "death_counter": {
        "settings": ["default_death_counter_checkbox",],
        "widgets": ["death_counter_checkbox"],
    },
    "room_names": {
        "settings": ["default_room_names_combo_box",],
        "widgets": ["room_names_combo_box"],
    },

    # Volume
    "volume": {
        "settings": [
            "default_master_slider",
            "default_music_slider",
            "default_sfx_slider",
            "default_environment_slider",
            "default_speech_slider",
            "default_grunt_slider",
            "default_gui_slider",
        ],
        "widgets": [
            "volume_box",
            "Master",
            "Music",
            "SFX",
            "Environment",
            "Speech",
            "Grunt",
            "GUI",
        ],
    },
    "master_volume": {
        "settings": ["default_master_slider"],
        "widgets": ["Master"],
    },
    "music_volume": {
        "settings": ["default_music_slider"],
        "widgets": ["Music"],
    },
    "sfx_volume": {
        "settings": ["default_sfx_slider"],
        "widgets": ["SFX"],
    },
    "environment_volume": {
        "settings": ["default_environment_slider"],
        "widgets": ["Environment"],
    },
    "speech_volume": {
        "settings": ["default_speech_slider"],
        "widgets": ["Speech"],
    },
    "grunt_volume": {
        "settings": ["default_grunt_slider"],
        "widgets": ["Grunt"],
    },
    "gui_volume": {
        "settings": ["default_gui_slider"],
        "widgets": ["GUI"],
    },

    # Door covers
    "door": {
        "settings": [
            "default_diffusion_beam_radio_button_group",
            "default_ice_missile_radio_button_group",
            "default_storm_missile_radio_button_group",
            "default_bomb_radio_button_group",
            "default_cross_bomb_radio_button_group",
            "default_power_bomb_radio_button_group",
            "default_permanently_closed_radio_button_group",
        ],
        "widgets": [
            "doors_box",
            "Diffusion Beam",
            "Ice Missile",
            "Storm Missile",
            "Bomb",
            "Cross Bomb",
            "Power Bomb",
            "Permanently Closed",
        ],
    },
    "diffusion_beam_door": {
        "settings": ["default_diffusion_beam_radio_button_group"],
        "widgets": ["Diffusion Beam"],
    },
    "ice_missile_door": {
        "settings": ["default_ice_missile_radio_button_group"],
        "widgets": ["Ice Missile"],
    },
    "storm_missile_door": {
        "settings": ["default_storm_missile_radio_button_group"],
        "widgets": ["Storm Missile"],
    },
    "bomb_door": {
        "settings": ["default_bomb_radio_button_group"],
        "widgets": ["Bomb"],
    },
    "cross_bomb_door": {
        "settings": ["default_cross_bomb_radio_button_group"],
        "widgets": ["Cross Bomb"],
    },
    "power_bomb_door": {
        "settings": ["default_power_bomb_radio_button_group"],
        "widgets": ["Power Bomb"],
    },
    "permanently_closed_door": {
        "settings": ["default_permanently_closed_radio_button_group"],
        "widgets": ["Permanently Closed"],
    },
}

default_cosmetic_settings = {
    "default_boss_lifebar_checkbox": False,
    "default_enemy_lifebar_checkbox": False,
    "default_player_damage_checkbox": False,
    "default_enemy_damage_checkbox": False,
    "default_death_counter_checkbox": False,
    "default_room_names_combo_box": 0,
    "default_master_slider": 100,
    "default_music_slider": 100,
    "default_sfx_slider": 100,
    "default_environment_slider": 100,
    "default_speech_slider": 100,
    "default_grunt_slider": 100,
    "default_gui_slider": 100,
    "default_diffusion_beam_radio_button_group": "diffusion_beam_radio_default",
    "default_ice_missile_radio_button_group": "ice_missile_radio_default",
    "default_storm_missile_radio_button_group": "storm_missile_radio_default",
    "default_bomb_radio_button_group": "bomb_radio_default",
    "default_cross_bomb_radio_button_group": "cross_bomb_radio_default",
    "default_power_bomb_radio_button_group": "power_bomb_radio_default",
    "default_permanently_closed_radio_button_group": "permanently_closed_radio_default",
}

def delete_none_from_dict(dct) -> dict:
    for key, value in list(dct.items()):
        if isinstance(value, dict):
            delete_none_from_dict(value)
        elif value is None:
            del dct[key]

    return dct


class ModInfo:
    def __init__(self, identifier: str, name: str, author: str, version: str, description: str, thumbnail: Path,
                 mod_path: Path, assets_path: Path, settings_dialog_class: QDialog, default_settings: dict,
                 disabled_settings: list = []) -> None:
        self.identifier = identifier
        self.name = name
        self.author = author
        self.version = version
        self.description = description
        self.thumbnail = thumbnail
        self.mod_path = mod_path
        self.assets_path = assets_path
        self.settings_dialog_class = settings_dialog_class
        self.default_settings = default_settings
        self.disabled_settings = disabled_settings


class DreadMod(QWidget, Ui_DreadMod):
    def __init__(self, mod_info: ModInfo) -> None:
        super().__init__()
        self.setupUi(self)

        self.identifier = mod_info.identifier
        self.name = mod_info.name
        self.author = mod_info.author
        self.version = mod_info.version
        self.description = mod_info.description
        self.thumbnail = mod_info.thumbnail
        self.mod_path = mod_info.mod_path
        self.assets_path = mod_info.assets_path
        self.settings_dialog_class = mod_info.settings_dialog_class
        self.default_settings = deepcopy(default_cosmetic_settings)
        self.disabled_settings = []

        if "all" in mod_info.disabled_settings:
            for setting_info in disabled_settings_info.values():
                for setting in setting_info["settings"]:
                    self.default_settings.pop(setting)

                self.disabled_settings += setting_info["widgets"]
        else:
            for setting_name in mod_info.disabled_settings:
                for setting in disabled_settings_info[setting_name]["settings"]:
                    self.default_settings.pop(setting, None)

                self.disabled_settings += disabled_settings_info[setting_name]["widgets"]

        self.default_settings.update(mod_info.default_settings)

        self.settings = UserSettings(
            user_settings_dir / self.name.replace(" ", "") / f"v{self.version.replace(".", "_")}" / "settings.json",
            self.default_settings
        )

        self.name_label.setText(self.name)
        self.author_label.setText("By " + self.author)
        self.version_label.setText("Version " + self.version)
        self.description_label.setText(self.description)
        self.thumbnail_label.setPixmap(QPixmap(self.thumbnail))

        self.input_path = None
        self.editor = None
        self.lua_editor = None

    def mouseDoubleClickEvent(self, event) -> None:
        self.show_export_dialog()

    def show_export_dialog(self) -> None:
        self.export_dialog = ExportDialog(
            self.settings,
            self.settings_dialog_class,
            self.disabled_settings,
            self
        )
        self.export_dialog.setWindowTitle("Export " + self.name)
        self.export_dialog.exec()

    def apply_cosmetics(self, cosmetic_patches: dict) -> dict:
        to_update = {
            "lua": {
                "camera_names_dict": {}
            }
        }

        # Tunables
        config = {
            "AIManager": {
                "bShowBossLifebar": self.settings.get("default_boss_lifebar_checkbox", None),
                "bShowEnemyLife": self.settings.get("default_enemy_lifebar_checkbox", None),
                "bShowEnemyDamage": self.settings.get("default_enemy_damage_checkbox", None),
                "bShowPlayerDamage": self.settings.get("default_player_damage_checkbox", None),
            },
            "SoundSystemATK": {
                "fMainVolume": self.settings.get("default_master_slider", None),
                "fMusicVolume": self.settings.get("default_music_slider", None),
                "fSfxVolume": self.settings.get("default_sfx_slider", None),
                "fEnvironmentStreamsVolume": self.settings.get("default_environment_slider", None),
                "fSpeechVolume": self.settings.get("default_speech_slider", None),
                "fGruntVolume": self.settings.get("default_grunt_slider", None),
                "fGUIVolume": self.settings.get("default_gui_slider", None),
            }
        }

        for key, value in config["SoundSystemATK"].items():
            if value is not None:
                config["SoundSystemATK"][key] /= 100

        to_update["config"] = config

        # Custom init
        custom_init = {
            "enable_death_counter": self.settings.get("default_death_counter_checkbox", None),
        }

        room_names_index = self.settings.get("default_room_names_combo_box", None)
        if room_names_index is not None:
            custom_init["enable_room_name_display"] = room_names[room_names_index]

        to_update["lua"]["custom_init"] = custom_init

        # Shield covers
        shield_versions = {
            # Since the value will be in the format of
            # "diffusion_beam_radio_default" or "diffusion_beam_radio_alternate",
            # the string needs to be split by underscores in order to grab only "default" or "alternate"
            "diffusion_beam": self.settings.get("default_diffusion_beam_radio_button_group", None),
            "ice_missile": self.settings.get("default_ice_missile_radio_button_group", None),
            "storm_missile": self.settings.get("default_storm_missile_radio_button_group", None),
            "bomb": self.settings.get("default_bomb_radio_button_group", None),
            "cross_bomb": self.settings.get("default_cross_bomb_radio_button_group", None),
            "power_bomb": self.settings.get("default_power_bomb_radio_button_group", None),
            "closed": self.settings.get("default_permanently_closed_radio_button_group", None),
        }

        shield_versions = {key: value.split("_")[-1].upper()
                           for key, value
                           in shield_versions.items()
                           if value}

        to_update["shield_versions"] = shield_versions

        cosmetic_patches.update(delete_none_from_dict(to_update))
        return cosmetic_patches

    def add_assets(self, assets_path: Path) -> None:
        """Adds each file in assets_path to the mod
        @param assets_path: The directory to add files from"""
        for asset in assets_path.rglob("*"):
            asset_name = asset.relative_to(assets_path).as_posix()

            if asset.is_file and self.editor.does_asset_exists(asset_name):
                self.editor.replace_asset(asset_name, asset.read_bytes())

    def start(self, input_path: Path) -> None:
        """Initializes anything needed for patching, i.e. a PatcherEditor

        param input_path: a path to a Dread ROMFS"""
        self.input_path = input_path
        self.editor = PatcherEditor(self.input_path)
        # Initializing this even though it's never used by default, just in case. Might mislead devs?
        self.lua_editor = LuaEditor()

    def patch(self) -> None:
        """Contains all the actual game modifications. Must be overriden by a subclass"""
        raise NotImplementedError()

    def export(self, export_params: ExportParams) -> None:
        """Saves the game modifications using the provided ExportParams

        param export_params: the parameters for the export"""
        shutil.rmtree(export_params.romfs_path, ignore_errors=True)
        shutil.rmtree(export_params.exefs_path, ignore_errors=True)
        shutil.rmtree(export_params.exefs_patches_path, ignore_errors=True)

        if export_params.output_format == OutputFormat.ROMFS:
            include_depackager(export_params.exefs_path)

        # This causes issues if certain patches haven't been made, need a solution.
        # Maybe this can be called by the dev at the end of patch()?
        # self.lua_editor.save_modifications(self.editor)

        self.editor.flush_modified_assets()

        self.editor.save_modifications(export_params.romfs_path, export_params.output_format)


class JsonMod(DreadMod):
    def __init__(self, mod_info: ModInfo, configuration: dict) -> None:
        self.configuration = configuration

        super().__init__(mod_info)

    def start(self, input_path: Path) -> None:
        validate(self.configuration)

        self.input_path = input_path
        self.editor = PatcherEditor(self.input_path)
        self.lua_editor = LuaEditor()

    def patch(self) -> None:
        # ODR will insert values into the configuration while patching, so if the configuration isn't copied,
        # trying to export again will fail schema validation
        configuration = deepcopy(self.configuration)
        self.apply_cosmetics(self.configuration["cosmetic_patches"])

        apply_patches(self.editor, self.lua_editor, configuration)

        if self.assets_path:
            self.add_assets(self.assets_path)

    def export(self, export_params: ExportParams) -> None:
        shutil.rmtree(export_params.romfs_path, ignore_errors=True)
        shutil.rmtree(export_params.exefs_path, ignore_errors=True)
        shutil.rmtree(export_params.exefs_patches_path, ignore_errors=True)

        patch_exefs(export_params.exefs_patches_path, {})

        if export_params.output_format == OutputFormat.ROMFS:
            include_depackager(export_params.exefs_path)

        self.lua_editor.save_modifications(self.editor)

        self.editor.flush_modified_assets()

        self.editor.save_modifications(export_params.romfs_path, export_params.output_format)
