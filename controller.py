from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from model import AppModel
from ui.view import MainView
from socks import SocksServer, send_unix

import sys
import asyncio
import threading


class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.model = AppModel()
        self.view = MainView()
        self.stats_timer = QTimer()
        self.socks_server = SocksServer("/tmp/wtp_ui.sock")

        self.setup()

    def setup(self):
        self.load_programs_from_folder(self.model.app_dir)

        self.view.run_button.clicked.connect(self.run_program)
        self.view.stop_button.clicked.connect(self.stop_program)
        self.view.stats_main.exit_button.clicked.connect(self.exit_app)
        self.view.folder_selected.connect(self.load_programs_from_folder)
        self.view.calibrate_button.clicked.connect(self.on_calibrate)

        # Refresh stats every 60 seconds
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(60000)
        self.update_stats()

        self.view.show()

        self.start_socks_server()

    def start_socks_server(self):
        self.socks_server.add_handler("set_button_text", self.handle_set_button_text)

        def run():
            asyncio.run(self.socks_server.start())

        threading.Thread(target=run, daemon=True).start()

    def handle_set_button_text(self, data):
        text = data.get("text", "")
        self.view.calibrate_button.setText(text)
        return {}

    def run_program(self):
        selected = self.view.program_selector.currentText()
        if selected:
            self.model.run_program(selected, self.view.append_output)

    def stop_program(self):
        self.model.stop_program()

    def exit_app(self):
        self.stop_program()
        self.app.quit()
        sys.exit(0)

    def load_programs_from_folder(self, folder_path):
        self.model.app_dir = folder_path
        self.view.update_program_list(self.model.get_programs())
        self.view.set_folder_path(folder_path)

    def update_stats(self):
        stats = self.model.get_device_stats()
        self.view.update_stats(stats)

    def run(self):
        sys.exit(self.app.exec_())  # Note: PyQt5 uses exec_()

    def on_calibrate(self):
        try:
            send_unix("button_pressed", {}, "/tmp/button.sock")
        except:
            pass
