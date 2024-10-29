from pathlib import Path
from re import sub

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QWidget

from dread_mod_loader.gui.generated.markdown_dialog_ui import Ui_MarkdownDialog
from dread_mod_loader.gui.scrollable_markdown import ScrollableMarkdown


class MarkdownDialog(QDialog, Ui_MarkdownDialog):
    def __init__(self, docs_path: Path, parent: QWidget = None, flags: Qt.WindowType = None) -> None:
        super().__init__(parent, flags)

        self.setupUi(self)

        for doc_path in docs_path.glob("*"):
            tab_name = sub(r"\d+-", "", doc_path.stem)
            self.markdown_tab_widget.addTab(ScrollableMarkdown(doc_path), tab_name)
