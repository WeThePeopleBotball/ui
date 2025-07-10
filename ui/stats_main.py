from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QPushButton, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal


def create_label(text=None):
    label = QLabel(text)
    label.setWordWrap(True)
    return label


class StatsMainPage(QWidget):
    theme_toggled = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self):
        super(StatsMainPage, self).__init__()

        self.device_name_label = create_label()
        self.os_info_label = create_label()
        self.ssid_label = create_label()
        self.password_label = create_label()
        self.battery_label = create_label()

        layout = QVBoxLayout()

        # Limit label width in QFormLayout
        form = QFormLayout()

        form.addRow(create_label("Device Name:"), self.device_name_label)
        form.addRow(create_label("OS Info:"), self.os_info_label)
        form.addRow(create_label("SSID:"), self.ssid_label)
        form.addRow(create_label("Wi-Fi Password:"), self.password_label)
        form.addRow(create_label("Battery:"), self.battery_label)
        layout.addLayout(form)

        layout.addSpacing(24)

        # Theme + Exit row
        theme_exit_row = QHBoxLayout()
        self.toggle_theme_button = QPushButton("Toggle Theme")
        self.exit_button = QPushButton("Exit")
        self.toggle_theme_button.clicked.connect(self.theme_toggled.emit)
        self.exit_button.clicked.connect(self.exit_requested.emit)

        for btn in (self.toggle_theme_button, self.exit_button):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        theme_exit_row.addWidget(self.toggle_theme_button)
        theme_exit_row.addWidget(self.exit_button)
        layout.addLayout(theme_exit_row)

        layout.addStretch()

        # Navigation buttons
        button_row = QHBoxLayout()
        self.movables_button = QPushButton("Movables")
        self.sensors_button = QPushButton("Sensors")

        for btn in (self.movables_button, self.sensors_button):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        button_row.addWidget(self.movables_button)
        button_row.addWidget(self.sensors_button)
        layout.addLayout(button_row)

        self.setLayout(layout)
