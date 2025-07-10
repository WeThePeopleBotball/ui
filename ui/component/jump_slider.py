from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent


class JumpSlider(QSlider):
    def mousePressEvent(self, ev: QMouseEvent):
        if ev and ev.button() == Qt.LeftButton:
            value = self.minimum() + (self.maximum() - self.minimum()) * ev.x() / self.width()
            self.setValue(int(value))
            ev.accept()
        super().mousePressEvent(ev)
