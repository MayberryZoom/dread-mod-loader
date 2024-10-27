from typing import overload

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QFileDialog, QPushButton, QWidget


class FileDialogButton(QPushButton):
    @overload
    def __init__(self, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, text: str, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, icon: QIcon | QPixmap, text: str, parent: QWidget = None) -> None: ...

    def __init__(self, arg1, arg2 = None, arg3 = None) -> None:
        if isinstance(arg1, QIcon):
            super().__init__(arg1, arg2, arg3)
            parent = arg3
        elif isinstance(arg1, str):
            super().__init__(arg1, arg2)
            parent = arg2
        else:
            super().__init__(arg1)
            parent = arg1

        self.line_edit = None

        self.file_dialog = QFileDialog(parent)
        self.file_dialog.setFileMode(QFileDialog.FileMode.Directory)

        self.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self) -> None:
        self.file_dialog.setDirectory(self.line_edit.text())

        if self.file_dialog.exec():
            self.line_edit.setText(self.file_dialog.selectedFiles()[0])

            self.line_edit.on_updated()
