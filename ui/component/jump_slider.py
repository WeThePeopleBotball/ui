from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent


class JumpSlider(QSlider):
    def mousePressEvent(self, ev: QMouseEvent | None):
        if ev and ev.button() == Qt.MouseButton.LeftButton:
            value = self.minimum() + (self.maximum() - self.minimum()) * ev.position().x() / self.width()
            self.setValue(int(value))
            ev.accept()
        super().mousePressEvent(ev)
