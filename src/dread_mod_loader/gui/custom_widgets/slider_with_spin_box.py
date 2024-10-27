from typing import overload

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget

from dread_mod_loader.gui.custom_widgets.non_scrollable_slider import (
    NonScrollableSlider,
)
from dread_mod_loader.gui.custom_widgets.non_scrollable_spin_box import NonScrollableDoubleSpinBox
from dread_mod_loader.settings import UserSettings


class SliderWithSpinBox(QHBoxLayout):
    @overload
    def __init__(self, name: str, settings: UserSettings, parent: QWidget = None) -> None: ...
    @overload
    def __init__(self, settings: UserSettings, parent: QWidget = None) -> None: ...

    def __init__(self, arg1, arg2, arg3 = None) -> None:
        if isinstance(arg1, str):
            super().__init__(arg3)
            parent = arg3
            self.settings = arg2
            name = arg1
        else:
            super().__init__(arg2)
            parent = arg2
            self.settings = arg1
            name = ""

        id = name.lower().replace(" ", "_")

        self.setObjectName(f"{id}_layout")

    # Label
        self.label = QLabel(name, parent)
        self.label.setObjectName(f"{id}_label")
        self.label.setMinimumSize(QSize(75, 0))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if parent:
            setattr(parent, self.label.objectName(), self.label)

    # Slider
        self.slider = NonScrollableSlider(Qt.Orientation.Horizontal, parent)
        self.slider.setObjectName(f"{id}_slider")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHeightForWidth(self.slider.sizePolicy().hasHeightForWidth())
        self.slider.setSizePolicy(sizePolicy)
        self.slider.setMaximum(100)
        self.slider.setSingleStep(1)

        if parent:
            setattr(parent, self.slider.objectName(), self.slider)

    # Spin box
        self.spin_box = NonScrollableDoubleSpinBox(parent)
        self.spin_box.setObjectName(f"{id}_spin_box")
        font = QFont()
        font.setPointSize(8)
        self.spin_box.setFont(font)
        self.spin_box.setDecimals(0)
        self.spin_box.setValue(100)
        self.spin_box.setSuffix("%")
        self.slider.setMaximum(100)
        self.slider.setSingleStep(1)

        if parent:
            setattr(parent, self.spin_box.objectName(), self.spin_box)

    # Add to layout
        self.addWidget(self.label)
        self.addWidget(self.slider)
        self.addWidget(self.spin_box)

    # Settings
        self.setting_name = "default_" + self.slider.objectName()

        # Saving settings should have a timer
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self._save_value)

        self.slider.setValue(self.settings[self.setting_name])
        self.spin_box.setValue(self.settings[self.setting_name])

        self.slider.valueChanged.connect(self._slider_value_changed)
        self.spin_box.valueChanged.connect(self._spin_box_value_changed)

    def _slider_value_changed(self, value: int) -> None:
        self.spin_box.blockSignals(True)
        self.spin_box.setValue(value)
        self.spin_box.blockSignals(False)

        self.timer.start()

    def _spin_box_value_changed(self, value: int) -> None:
        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.slider.blockSignals(False)

        self.timer.start()

    def _save_value(self) -> None:
        self.settings[self.setting_name] = self.slider.value()
