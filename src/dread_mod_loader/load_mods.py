import json
import sys
import tomllib
from importlib import import_module, reload
from pathlib import Path

from dread_mod_loader.assets import assets_path
from dread_mod_loader.gui.settings_dialog import SettingsDialog
from dread_mod_loader.logger import LOG
from dread_mod_loader.mod import DreadMod, JsonMod, ModInfo

placeholder_thumbnail = assets_path() / "placeholder_thumbnail.png"

def import_class_from_module(module_name: str, class_name: str):
    """Imports a class from a module

    param module_name: the name of the module, i.e. "dread_mod_loader.load_mods"
    param class_name: the name of the class"""
    # invalidate_caches()

    if module_name in sys.modules:
        module = reload(sys.modules[module_name])
    else:
        module = import_module(module_name)

    return getattr(module, class_name)

def load_mod(mod_path: Path) -> DreadMod:
    """Loads a DreadMod from the provided path

    param mod_path: a path to the folder containing the mod_info.toml"""
    # Inserting the mod directory into the Python
    # pat hallows it to be imported from directly
    sys.path.insert(1, str(mod_path.parent))

    with open(mod_path / "mod_info.toml", "rb") as mod_toml:
        mod_config = tomllib.load(mod_toml)

        patch_type = mod_config["patch_type"]

        if "thumbnail" in mod_config:
            mod_thumbnail = mod_path / mod_config["thumbnail"]
        else:
            mod_thumbnail = placeholder_thumbnail

        if "assets_path" in mod_config:
            assets_path = mod_path / mod_config["assets_path"]
        else:
            assets_path = None

        if "settings_dialog_class" in mod_config:
            settings_dialog_class = import_class_from_module(
                mod_path.stem + "." + ".".join((mod_config["settings_dialog_file"][:-3]).split("\\")),
                mod_config["settings_dialog_class"]
            )
        else:
            settings_dialog_class = SettingsDialog

        mod_info = ModInfo(
            mod_config["identifier"],
            mod_config.get("name", "Unknown"),
            mod_config.get("author", "Unknown"),
            mod_config.get("version", "Unknown"),
            mod_config.get("description", "No description."),
            mod_thumbnail,
            mod_path,
            assets_path,
            settings_dialog_class,
            mod_config.get("default_settings", {}),
            mod_config.get("disabled_settings", []),
        )

        if patch_type == "json":
            with open(mod_path / mod_config["patch_file"]) as configuration:
                return JsonMod(mod_info, json.load(configuration))

        elif patch_type == "py":
            # Import the mod
            mod_class = import_class_from_module(
                mod_path.stem + "." + ".".join((mod_config["patch_file"][:-3]).split("\\")),
                mod_config["patch_class"]
            )

            return mod_class(mod_info)

        else:
            LOG.warning("Invalid patch type!")

def load_mods(mods_directory: Path) -> dict[str, DreadMod]:
    LOG.info("Starting loading mods...")

    mods = {}

    for mod_path in mods_directory.glob("*"):
        try:
            mod = load_mod(mod_path)
            mods[getattr(mod, "identifier")] = mod
        except Exception as e:
            LOG.warning(f"{mod_path.stem}: {e}")

    LOG.info("Done loading mods!")
    return mods
