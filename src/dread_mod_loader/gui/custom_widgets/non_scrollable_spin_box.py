from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QDoubleSpinBox, QSpinBox


class NonScrollableSpinBox(QSpinBox):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Wheel:
            event.ignore()
            return True

        return super().eventFilter(watched, event)


class NonScrollableDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Wheel:
            event.ignore()
            return True

        return super().eventFilter(watched, event)
