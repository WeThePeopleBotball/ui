from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QScrollArea, QStackedWidget,
    QPushButton, QComboBox, QTextEdit, QHBoxLayout, QFileDialog,
    QLabel, QStatusBar
)
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import pyqtSignal

from ui.stats_main import StatsMainPage
from ui.movables_page import MovablesPage
from ui.sensors_page import SensorsPage


class MainView(QWidget):
    folder_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("WeThePeople Dashboard")
        self.resize(800, 600)

        self.is_dark_mode = True
        self.load_stylesheet("dark.qss")

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

        self.stats_main.theme_toggled.connect(self.toggle_theme)
        self.stats_main.exit_requested.connect(self.close)

    def init_launcher_tab(self):
        layout = QVBoxLayout()

        # Folder & Program
        top_row = QHBoxLayout()
        self.load_folder_btn = QPushButton("Load Folder")
        self.program_selector = QComboBox()
        top_row.addWidget(self.load_folder_btn)
        top_row.addWidget(self.program_selector)
        layout.addLayout(top_row)

        # Output
        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        layout.addWidget(self.output_field)

        # Main Controls
        button_row = QHBoxLayout()
        self.run_button = QPushButton("Execute")
        self.stop_button = QPushButton("Stop")
        self.calibrate_button = QPushButton("Calibrate")
        button_row.addWidget(self.run_button)
        button_row.addWidget(self.stop_button)
        button_row.addWidget(self.calibrate_button)
        layout.addLayout(button_row)

        # Status Bar
        self.status_bar = QStatusBar()
        self.folder_status_label = QLabel("Folder: Not selected")
        self.battery_status_label = QLabel("")
        self.status_bar.addWidget(self.folder_status_label)
        self.status_bar.addPermanentWidget(self.battery_status_label)
        layout.addWidget(self.status_bar)

        self.launcher_tab.setLayout(layout)
        self.load_folder_btn.clicked.connect(self.select_folder)

    def init_stats_tab(self):
        self.stats_stack = QStackedWidget(self.stats_tab_widget)
        layout = QVBoxLayout(self.stats_tab_widget)
        layout.addWidget(self.stats_stack)

        self.stats_main = StatsMainPage()
        self.movables_page = MovablesPage()
        self.sensors_page = SensorsPage()

        self.stats_stack.addWidget(self.stats_main)
        self.stats_stack.addWidget(self.movables_page)
        self.stats_stack.addWidget(self.sensors_page)

        self.stats_main.movables_button.clicked.connect(
            lambda: self.stats_stack.setCurrentWidget(self.movables_page)
        )
        self.stats_main.sensors_button.clicked.connect(
            lambda: self.stats_stack.setCurrentWidget(self.sensors_page)
        )
        self.movables_page.back_button.clicked.connect(
            lambda: self.stats_stack.setCurrentWidget(self.stats_main)
        )
        self.sensors_page.back_button.clicked.connect(
            lambda: self.stats_stack.setCurrentWidget(self.stats_main)
        )

        self.stats_tab_scroll.setWidgetResizable(True)
        self.stats_tab_scroll.setWidget(self.stats_tab_widget)

    def append_output(self, html_line: str):
        cursor = self.output_field.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
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

    def update_stats(self, stats):
        self.stats_main.device_name_label.setText(stats["device_name"])
        self.stats_main.os_info_label.setText(stats["os_info"])
        self.stats_main.ssid_label.setText(stats["ssid"])
        self.stats_main.password_label.setText(stats["password"])
        self.stats_main.battery_label.setText(stats["battery"])
        self.battery_status_label.setText(stats["battery"])

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.load_stylesheet("dark.qss")
        else:
            self.load_stylesheet("light.qss")

    def load_stylesheet(self, path: str):
        try:
            with open(path, "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Failed to load stylesheet {path}: {e}")
