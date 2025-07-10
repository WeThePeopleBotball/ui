from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QComboBox, QTextEdit,
    QHBoxLayout, QFileDialog, QLabel, QStatusBar, QTabWidget,
    QFormLayout, QSlider, QTableWidget, QTableWidgetItem,
    QHeaderView, QScrollArea, QFrame, QStackedWidget, QSizePolicy
)
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import pyqtSignal, Qt, QPropertyAnimation, QRect, QEasingCurve


class MainView(QWidget):
    folder_selected = pyqtSignal(str)

    def __init__(self):
        super(MainView, self).__init__()
        self.setWindowTitle("WTP")
        self.resize(800, 600)

        self.tabs = QTabWidget(self)
        self.launcher_tab = QWidget()
        self.stats_tab_scroll = QScrollArea()
        self.stats_tab_widget = QWidget()

        self.init_launcher_tab()
        self.init_stats_tab()

        self.tabs.addTab(self.launcher_tab, "Launcher")
        self.tabs.addTab(self.stats_tab_scroll, "Stats")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)

    def init_launcher_tab(self):
        layout = QVBoxLayout()

        top_row = QHBoxLayout()
        self.load_folder_btn = QPushButton("Load Folder")
        self.program_selector = QComboBox()
        top_row.addWidget(self.load_folder_btn)
        top_row.addWidget(self.program_selector)
        layout.addLayout(top_row)

        self.load_folder_btn.clicked.connect(self.select_folder)

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        self.output_field.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.output_field)

        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Execute")
        self.stop_button = QPushButton("Stop")
        self.exit_button = QPushButton("Exit")
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.exit_button)
        layout.addLayout(button_layout)

        self.status_bar = QStatusBar()
        self.folder_status_label = QLabel("Folder: Not selected")
        self.battery_status_label = QLabel("")
        self.status_bar.addWidget(self.folder_status_label)
        self.status_bar.addPermanentWidget(self.battery_status_label)
        layout.addWidget(self.status_bar)

        self.launcher_tab.setLayout(layout)

    def append_output(self, html_line):
        cursor = self.output_field.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(html_line + "<br />")
        self.output_field.setTextCursor(cursor)
        self.output_field.ensureCursorVisible()

    def update_program_list(self, programs):
        self.program_selector.clear()
        self.program_selector.addItems(programs)

    def set_folder_path(self, folder):
        self.folder_status_label.setText(f"Folder: {folder}")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Executable Folder")
        if folder:
            self.folder_selected.emit(folder)
            self.set_folder_path(folder)

    def init_stats_tab(self):
        self.stats_stack = QStackedWidget(self.stats_tab_widget)
        outer_layout = QVBoxLayout(self.stats_tab_widget)
        outer_layout.addWidget(self.stats_stack)

        # === Main Stats Page ===
        self.stats_main_page = QWidget()
        main_layout = QVBoxLayout(self.stats_main_page)

        form_layout = QFormLayout()
        self.device_name_label = QLabel()
        self.os_info_label = QLabel()
        self.ssid_label = QLabel()
        self.password_label = QLabel()
        self.battery_label = QLabel()

        form_layout.addRow("Device Name:", self.device_name_label)
        form_layout.addRow("OS Info:", self.os_info_label)
        form_layout.addRow("SSID:", self.ssid_label)
        form_layout.addRow("Wi-Fi Password:", self.password_label)
        form_layout.addRow("Battery:", self.battery_label)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self._hline())

        nav_buttons = QHBoxLayout()
        self.movables_button = QPushButton("Movables")
        self.sensors_button = QPushButton("Sensors")
        nav_buttons.addWidget(self.movables_button)
        nav_buttons.addWidget(self.sensors_button)
        main_layout.addLayout(nav_buttons)

        self.stats_stack.addWidget(self.stats_main_page)

        # === Movables Page ===
        self.movables_page = QWidget()
        movables_layout = QVBoxLayout(self.movables_page)

        motor_row = QHBoxLayout()
        motor_row.addWidget(QLabel("Motor:"))
        self.motor_dropdown = QComboBox()
        self.motor_dropdown.addItems([str(i + 1) for i in range(4)])
        self.motor_slider = QSlider(Qt.Horizontal)
        self.motor_slider.setRange(0, 100)
        motor_row.addWidget(self.motor_dropdown)
        motor_row.addWidget(self.motor_slider)
        movables_layout.addLayout(motor_row)

        servo_row = QHBoxLayout()
        servo_row.addWidget(QLabel("Servo:"))
        self.servo_dropdown = QComboBox()
        self.servo_dropdown.addItems([str(i + 1) for i in range(4)])
        self.servo_slider = QSlider(Qt.Horizontal)
        self.servo_slider.setRange(0, 180)
        servo_row.addWidget(self.servo_dropdown)
        servo_row.addWidget(self.servo_slider)
        movables_layout.addLayout(servo_row)

        back_btn_m = QPushButton("Back")
        back_btn_m.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_btn_m.clicked.connect(lambda: self.animate_stats_transition(self.stats_main_page, "right"))
        movables_layout.addWidget(self._hline())
        movables_layout.addWidget(back_btn_m)
        self.stats_stack.addWidget(self.movables_page)

        # === Sensors Page ===
        self.sensors_page = QWidget()
        sensors_layout = QVBoxLayout(self.sensors_page)

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

        self.sensor_table.horizontalHeader().setStretchLastSection(True)
        self.sensor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sensor_table.verticalHeader().setVisible(False)
        self.sensor_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sensor_table.setSelectionMode(QTableWidget.NoSelection)

        sensors_layout.addWidget(QLabel("Sensors:"))
        sensors_layout.addWidget(self.sensor_table)

        back_btn_s = QPushButton("Back")
        back_btn_s.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_btn_s.clicked.connect(lambda: self.animate_stats_transition(self.stats_main_page, "right"))
        sensors_layout.addWidget(self._hline())
        sensors_layout.addWidget(back_btn_s)
        self.stats_stack.addWidget(self.sensors_page)

        self.movables_button.clicked.connect(lambda: self.animate_stats_transition(self.movables_page, "left"))
        self.sensors_button.clicked.connect(lambda: self.animate_stats_transition(self.sensors_page, "left"))

        self.stats_tab_scroll.setWidgetResizable(True)
        self.stats_tab_scroll.setWidget(self.stats_tab_widget)

    def animate_stats_transition(self, target_widget, direction="left"):
        current_index = self.stats_stack.currentIndex()
        target_index = self.stats_stack.indexOf(target_widget)
        if current_index == target_index:
            return

        current_widget = self.stats_stack.currentWidget()
        self.stats_stack.setCurrentWidget(target_widget)

        w = self.stats_stack.width()
        h = self.stats_stack.height()
        offset = w if direction == "left" else -w

        target_widget.setGeometry(QRect(offset, 0, w, h))

        anim_old = QPropertyAnimation(current_widget, b"geometry", self)
        anim_new = QPropertyAnimation(target_widget, b"geometry", self)

        anim_old.setDuration(300)
        anim_new.setDuration(300)
        anim_old.setStartValue(QRect(0, 0, w, h))
        anim_old.setEndValue(QRect(-offset, 0, w, h))
        anim_new.setStartValue(QRect(offset, 0, w, h))
        anim_new.setEndValue(QRect(0, 0, w, h))

        anim_old.setEasingCurve(QEasingCurve.InOutCubic)
        anim_new.setEasingCurve(QEasingCurve.InOutCubic)

        self._animations = (anim_old, anim_new)
        anim_old.start()
        anim_new.start()

    def update_stats(self, stats):
        self.device_name_label.setText(stats["device_name"])
        self.os_info_label.setText(stats["os_info"])
        self.ssid_label.setText(stats["ssid"])
        self.password_label.setText(stats["password"])
        self.battery_label.setText(stats["battery"])
        self.battery_status_label.setText(stats["battery"])

    def _hline(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("margin-top: 12px; margin-bottom: 12px;")
        return line
