from pathlib import Path
from re import sub
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QLabel, QScrollArea, QSizePolicy, QVBoxLayout, QWidget

from dread_mod_loader import get_docs_path
from dread_mod_loader.gui.generated.help_ui import Ui_HelpDialog
from dread_mod_loader.gui.scrollable_markdown import ScrollableMarkdown
from dread_mod_loader.logger import LOG


class HelpDialog(QDialog, Ui_HelpDialog):
    def __init__(self, parent: QWidget = None, flags: Qt.WindowType = None):
        super().__init__(parent, flags)

        self.setupUi(self)

        for doc_path in get_docs_path().glob("*.md"):
            tab_name = sub("\d+-", "", doc_path.stem)
            self.help_tab_widget.addTab(ScrollableMarkdown(doc_path), tab_name)
