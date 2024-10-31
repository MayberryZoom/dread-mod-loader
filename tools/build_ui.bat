cd src\dread_mod_loader\

mkdir gui\generated

for /r %%F in (*.ui) do (
    pyside6-uic %%F -o gui\generated\%%~nF_ui.py --star-imports
)

cd ..\..
