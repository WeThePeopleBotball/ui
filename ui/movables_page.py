from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton,
    QHBoxLayout, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt

from ui.component.jump_slider import JumpSlider


class MovablesPage(QWidget):
    MOTOR_VELOCITY_MIN = -1500
    MOTOR_VELOCITY_MAX = 1500
    SERVO_POSITION_MIN = 0
    SERVO_POSITION_MAX = 2047

    def __init__(self):
        super(MovablesPage, self).__init__()

        self.motor_value_subscribers = []
        self.motor_selection_subscribers = []
        self.servo_value_subscribers = []
        self.servo_selection_subscribers = []

        layout = QVBoxLayout()

        # === Motor Section ===
        self.add_section_header(layout, "Motor Controls")

        motor_dropdown_row = QHBoxLayout()
        self.motor_dropdown = QComboBox()
        self.motor_dropdown.setFixedWidth(120)
        self.motor_dropdown.addItems([str(i + 1) for i in range(4)])
        self.motor_value_label = QLabel("0")
        motor_dropdown_row.addWidget(QLabel("Select motor:"))
        motor_dropdown_row.addWidget(self.motor_dropdown)
        motor_dropdown_row.addStretch()
        motor_dropdown_row.addWidget(QLabel("Current velocity:"))
        motor_dropdown_row.addWidget(self.motor_value_label)
        layout.addLayout(motor_dropdown_row)

        self.motor_dropdown.currentIndexChanged.connect(self._handle_motor_dropdown_change)

        motor_slider_row = QVBoxLayout()
        slider_label_row = QHBoxLayout()
        slider_label_row.addWidget(QLabel(str(self.MOTOR_VELOCITY_MIN)))
        slider_label_row.addStretch()
        slider_label_row.addWidget(QLabel(str(self.MOTOR_VELOCITY_MAX)))
        self.motor_slider = JumpSlider(Qt.Horizontal)
        self.motor_slider.setRange(self.MOTOR_VELOCITY_MIN, self.MOTOR_VELOCITY_MAX)
        self.motor_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.motor_slider.setMinimumHeight(40)
        self.motor_slider.valueChanged.connect(self._handle_motor_slider_change)
        motor_slider_row.addLayout(slider_label_row)
        motor_slider_row.addWidget(self.motor_slider)
        layout.addLayout(motor_slider_row)

        motor_ticks_row = QHBoxLayout()
        self.motor_ticks_label = QLabel("0")
        motor_ticks_row.addWidget(QLabel("Current ticks:"))
        motor_ticks_row.addWidget(self.motor_ticks_label)
        motor_ticks_row.addStretch()
        layout.addLayout(motor_ticks_row)

        layout.addSpacing(48)

        # === Servo Section ===
        self.add_section_header(layout, "Servo Controls")

        servo_dropdown_row = QHBoxLayout()
        self.servo_dropdown = QComboBox()
        self.servo_dropdown.setFixedWidth(120)
        self.servo_dropdown.addItems([str(i + 1) for i in range(4)])
        self.servo_value_label = QLabel("0")
        servo_dropdown_row.addWidget(QLabel("Select servo:"))
        servo_dropdown_row.addWidget(self.servo_dropdown)
        servo_dropdown_row.addStretch()
        servo_dropdown_row.addWidget(QLabel("Current position:"))
        servo_dropdown_row.addWidget(self.servo_value_label)
        layout.addLayout(servo_dropdown_row)

        self.servo_dropdown.currentIndexChanged.connect(self._handle_servo_dropdown_change)

        servo_slider_row = QVBoxLayout()
        slider_label_row = QHBoxLayout()
        slider_label_row.addWidget(QLabel(str(self.SERVO_POSITION_MIN)))
        slider_label_row.addStretch()
        slider_label_row.addWidget(QLabel(str(self.SERVO_POSITION_MAX)))
        self.servo_slider = JumpSlider(Qt.Horizontal)
        self.servo_slider.setRange(self.SERVO_POSITION_MIN, self.SERVO_POSITION_MAX)
        self.servo_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.servo_slider.setMinimumHeight(40)
        self.servo_slider.valueChanged.connect(self._handle_servo_slider_change)
        servo_slider_row.addLayout(slider_label_row)
        servo_slider_row.addWidget(self.servo_slider)
        layout.addLayout(servo_slider_row)

        layout.addStretch()
        self.back_button = QPushButton("Back")
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        self.setLayout(layout)

    def add_section_header(self, layout, title):
        title_row = QHBoxLayout()
        title_label = QLabel(f"── {title} ──")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; margin-bottom: 4px;")
        title_row.addWidget(title_label)
        layout.addLayout(title_row)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)
        line.setStyleSheet("color: #666; background-color: #666;")
        layout.addWidget(line)
        layout.addSpacing(12)

    def _handle_motor_slider_change(self, value):
        self.motor_value_label.setText(str(value))
        index = self.motor_dropdown.currentIndex()
        for callback in self.motor_value_subscribers:
            callback(index, value)

    def _handle_motor_dropdown_change(self, index):
        for callback in self.motor_selection_subscribers:
            callback(index)

    def _handle_servo_slider_change(self, value):
        self.servo_value_label.setText(str(value))
        index = self.servo_dropdown.currentIndex()
        for callback in self.servo_value_subscribers:
            callback(index, value)

    def _handle_servo_dropdown_change(self, index):
        for callback in self.servo_selection_subscribers:
            callback(index)

    def set_motor_velocity(self, value):
        value = max(self.MOTOR_VELOCITY_MIN, min(self.MOTOR_VELOCITY_MAX, value))
        self.motor_slider.setValue(value)
        self.motor_value_label.setText(str(value))

    def set_motor_ticks(self, ticks):
        self.motor_ticks_label.setText(str(ticks))

    def set_servo_position(self, value):
        value = max(self.SERVO_POSITION_MIN, min(self.SERVO_POSITION_MAX, value))
        self.servo_slider.setValue(value)
        self.servo_value_label.setText(str(value))

    def on_motor_value_change(self, callback):
        self.motor_value_subscribers.append(callback)

    def on_motor_selection_change(self, callback):
        self.motor_selection_subscribers.append(callback)

    def on_servo_value_change(self, callback):
        self.servo_value_subscribers.append(callback)

    def on_servo_selection_change(self, callback):
        self.servo_selection_subscribers.append(callback)
