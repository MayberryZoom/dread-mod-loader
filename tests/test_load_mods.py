from pathlib import Path

import pytest

from dread_mod_loader.load_mods import load_mod

mod_paths = [
    "tests/test_files/ili_ferun_tar_hadar",
    "tests/test_files/testing_mod",
]

mod_info_keys = [
    "identifier",
    "name",
    "author",
    "version",
    "description",
    "thumbnail",
    "mod_path",
    "assets_path",
    "settings_dialog_class",
    "disabled_settings",
]


@pytest.mark.parametrize("path_to_mod", mod_paths)
def test_load_mod(qtbot, path_to_mod):
    mod = load_mod(Path(path_to_mod))

    for key in mod_info_keys:
        assert hasattr(mod, key)


def test_invalid_patch_type(qtbot):
    load_mod(Path("tests/test_files/invalid_mod"))
