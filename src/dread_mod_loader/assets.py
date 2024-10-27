from os import getcwd
from pathlib import Path


def assets_path() -> Path:
    assets_path = Path(getcwd()) / "src/dread_mod_loader/assets"

    if assets_path.exists():
        return assets_path
    else:
        return Path(getcwd()) / "_internal/assets"
