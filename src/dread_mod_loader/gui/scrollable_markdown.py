from pathlib import Path
from re import match
from typing import overload

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QWidget

from dread_mod_loader.gui.generated.scrollable_markdown_ui import Ui_ScrollableMarkdown


class ScrollableMarkdown(QScrollArea, Ui_ScrollableMarkdown):
    @overload
    def __init__(self, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, markdown_path: Path, parent: QWidget = None) -> None: ...

    def __init__(self, arg1, arg2 = None) -> None:
        if isinstance(arg1, Path):
            markdown_path = arg1
            parent = arg2
        else:
            markdown_path = None
            parent = arg1

        super().__init__(parent)

        self.setupUi(self)

        if markdown_path:
            self.load_markdown(markdown_path)

    def add_text(self, text: str) -> None:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextFormat(Qt.TextFormat.MarkdownText)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.markdown_layout.addWidget(label)

    def add_image(self, image_path: Path) -> None:
        image = QPixmap(image_path)
        image.scaledToWidth(500)

        label = QLabel()
        label.setPixmap(image)

        self.markdown_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

    def load_markdown(self, md_path: Path) -> None:
        with md_path.open() as file:
            text = []

            for line in file.readlines():
                if line.startswith("!"):
                    matches = match(r"!\[(.+)\]\((.+)\)", line)

                    image_path = md_path.parent / matches[2]

                    self.add_text("\n".join(text))
                    self.add_image(image_path)

                    text = []
                else:
                    text.append(line)

            # Add any remaining text
            if text:
                self.add_text("\n".join(text))
