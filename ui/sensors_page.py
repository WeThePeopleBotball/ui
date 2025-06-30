from PyQt6.QtWidgets import (
    QSizePolicy, QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
)
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtCore import Qt


class SensorsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Sensors:"))
        self.sensor_table = QTableWidget(14, 2)
        self.sensor_table.setHorizontalHeaderLabels(["Sensor", "Value"])

        sensor_names = [
            "Analog 1", "Analog 2", "Analog 3", "Analog 4",
            "Digital 1", "Digital 2", "Digital 3", "Digital 4",
            "Gyro X", "Gyro Y", "Gyro Z",
            "Accel X", "Accel Y", "Accel Z"
        ]
        for i, name in enumerate(sensor_names):
            self.sensor_table.setItem(i, 0, QTableWidgetItem(name))
            self.sensor_table.setItem(i, 1, QTableWidgetItem("—"))

        # Header config
        h_header = self.sensor_table.horizontalHeader()
        if h_header is not None:
            h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        v_header = self.sensor_table.verticalHeader()
        if v_header is not None:
            v_header.setVisible(False)

        self.sensor_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.sensor_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.sensor_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(self.sensor_table)

        self.back_button = QPushButton("Back")
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)

    def resizeEvent(self, a0: QResizeEvent | None):
        super().resizeEvent(a0)
        self.adjust_row_heights()

    def adjust_row_heights(self):
        """Fill vertical space only if rows fit; otherwise allow scrolling."""
        row_count = self.sensor_table.rowCount()
        if row_count == 0:
            return

        viewport = self.sensor_table.viewport()
        if viewport is None:
            return  # Table not fully initialized

        total_height = viewport.height()

        v_header = self.sensor_table.verticalHeader()
        default_row_height = v_header.defaultSectionSize() if v_header else 30
        required_height = default_row_height * row_count

        if total_height > required_height:
            row_height = total_height // row_count
            for i in range(row_count):
                self.sensor_table.setRowHeight(i, row_height)
        else:
            for i in range(row_count):
                self.sensor_table.setRowHeight(i, default_row_height)

    def set_sensor_value(self, name: str, value: str):
        """Update the value for the row with the given sensor name."""
        for row in range(self.sensor_table.rowCount()):
            item = self.sensor_table.item(row, 0)
            if item and item.text() == name:
                self.sensor_table.setItem(row, 1, QTableWidgetItem(value))
                break
