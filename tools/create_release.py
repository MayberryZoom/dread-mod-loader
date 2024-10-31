from os import chdir
from shutil import make_archive
from subprocess import call

from PyInstaller.__main__ import run

from dread_mod_loader.version import version

call(r"tools\build_ui.bat")

run([
    "src/dread_mod_loader/__main__.py",
    "--name", "Dread Mod Loader-" + version,
    "--add-data", "src/dread_mod_loader/data:data",
    "--add-data", "docs:data/docs",
    "--exclude-module", "mods",
    "--noconsole",
    "--clean",
    "--noconfirm",
])

chdir("dist")

make_archive("Dread Mod Loader-" + version, "zip", "Dread Mod Loader-" + version)

chdir("..")
