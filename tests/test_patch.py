
from pathlib import Path

import pytest

from dread_mod_loader.load_mods import load_mod

mod_paths = [
    "tests/test_files/ili_ferun_tar_hadar",
    "tests/test_files/testing_mod",
]


@pytest.mark.parametrize("mod_path", mod_paths)
def test_patch(qtbot, dread_path, mod_path):
    mod = load_mod(Path(mod_path))
    mod.start(dread_path)
    mod.patch()
