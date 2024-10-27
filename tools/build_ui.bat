cd src\dread_mod_loader\

for /r %%F in (*.ui) do (
    pyside6-uic %%F -o gui\generated\%%~nF_ui.py --star-imports
)

cd ..\..
