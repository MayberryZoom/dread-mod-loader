from open_dread_rando.dread_patcher import patch_text

from dread_mod_loader.mod import DreadMod


class MyMod(DreadMod):
    def patch(self):
        patch_text(self.editor, "GUI_COMPANY_TITLE_SCREEN", "My Mod")
