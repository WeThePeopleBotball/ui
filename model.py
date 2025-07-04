import os
import subprocess
from PyQt6.QtCore import QThread, pyqtSignal
import socket
import platform
import psutil
import glob


class OutputReader(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, process):
        super().__init__()
        self.process = process
        self.running = True

    def run(self):
        for line in self.process.stdout:
            if not self.running:
                break
            colored_line = self.colorize(line.rstrip())
            self.output_signal.emit(colored_line)


    def colorize(self, text: str) -> str:
        lowered = text.lower()
    
        error_keywords = [
            "error", "failed", "exception", "traceback", "critical", "fatal",
            "panic", "abort", "crash", "unhandled"
        ]
        warning_keywords = [
            "warning", "deprecated", "caution", "unsafe", "slow", "timeout", "missing"
        ]
        info_keywords = [
            "info", "initialized", "connected", "ready", "completed", "done", "started"
        ]
        debug_keywords = [
            "debug", "verbose", "trace", "log", "step", "state", "internal"
        ]
    
        if any(word in lowered for word in error_keywords):
            return f'<span style="color:red;">{text}</span>'
        elif any(word in lowered for word in warning_keywords):
            return f'<span style="color:yellow;">{text}</span>'
        elif any(word in lowered for word in debug_keywords):
            return f'<span style="color:lightblue;">{text}</span>'
        elif any(word in lowered for word in info_keywords):
            return f'<span style="color:lightgreen;">{text}</span>'
        else:
            return f'<span style="color:white;">{text}</span>'

    def stop(self):
        self.running = False


class AppModel:
    def __init__(self, app_dir=None):
        if app_dir is None:
            app_dir = os.path.join(os.path.expanduser("~"), "apps")
        self.app_dir = app_dir
        self.process = None
        self.reader_thread = None

    def get_programs(self):
        return [
            f for f in os.listdir(self.app_dir)
            if os.access(os.path.join(self.app_dir, f), os.X_OK)
        ]

    def run_program(self, program_name, output_callback):
        full_path = os.path.join(self.app_dir, program_name)
        if full_path.endswith(".py"):
            cmd = ["python3", "-u", full_path]
        else:
            cmd = [full_path]

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        self.reader_thread = OutputReader(self.process)
        self.reader_thread.output_signal.connect(output_callback)
        self.reader_thread.start()

    def stop_program(self):
        if self.process:
            self.process.terminate()
            self.process = None

        if self.reader_thread:
            self.reader_thread.stop()
            self.reader_thread.quit()
            self.reader_thread.wait()
            self.reader_thread = None

    def get_device_stats(self):
        ssid = self._get_ssid()
        return {
            "device_name": socket.gethostname(),
            "os_info": platform.platform(),
            "ssid": ssid or "N/A",
            "password": self._get_wifi_password(ssid) if ssid else "N/A",
            "battery": self._get_battery_status()
        }

    def _get_ssid(self):
        try:
            output = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"])
            lines = output.decode().splitlines()
            for line in lines:
                active, ssid = line.strip().split(":")
                if active == "yes":
                    return ssid
        except Exception:
            pass
        return None

    def _get_wifi_password(self, ssid: str):
        try:
            pattern = f"/etc/NetworkManager/system-connections/{ssid}*"
            files = glob.glob(pattern)
            for file in files:
                with open(file, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.strip().startswith("psk="):
                            return line.strip().split("=", 1)[1]
        except Exception as e:
            return f"(Error: {e})"
        return "Not found"

    def _get_battery_status(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = int(round(battery.percent))
                icon = self._get_battery_icon(percent)
                return f"{icon} {percent}% {'(Charging)' if battery.power_plugged else '(Not Charging)'}"
        except Exception:
            pass
        return "N/A"

    def _get_battery_icon(self, percent):
        if percent >= 80:
            return "🔋"  # Full
        elif percent >= 50:
            return "🔋"  # Medium
        elif percent >= 20:
            return "🪫"  # Low
        else:
            return "❗"  # Critical

    
    def get_app_dir(self) -> str:
        return self.app_dir
