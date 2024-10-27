from typing import overload

from PySide6.QtCore import QEvent, QObject
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QSlider, QWidget


class NonScrollableSlider(QSlider):
    @overload
    def __init__(self, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, orientation: Qt.Orientation, parent: QWidget = None) -> None: ...

    def __init__(self, arg1, arg2 = None) -> None:
        if isinstance(arg1, Qt.Orientation):
            super().__init__(arg1, arg2)
        else:
            super().__init__(arg1)

        self.installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Wheel:
            event.ignore()
            return True

        return super().eventFilter(watched, event)
