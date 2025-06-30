# Venti BotUI

This application provides a graphical interface for launching executables from a folder and controlling a bot via dropdowns, sliders, and sensor feedback.

## Features

- Select and launch executables from a folder
- Real-time output streaming with color-coded logs (info, warning, error, etc.)
- Control motors and servos using dropdown and slider pairs
- Monitor system stats:
  - Device name and OS info
  - Wi-Fi SSID and password
  - Battery status with icon
  - Sensor data (Analog, Digital, Gyro)

## Getting Started

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Launch the application:

```
python main.py
```

The application will start with a graphical user interface and is ready to use.

---

## Warning: Wi-Fi Password Access

To retrieve the current Wi-Fi password, the application reads from:

```
/etc/NetworkManager/system-connections/
```

This only works on Linux systems that use **NetworkManager** and store connection profiles locally.

### Requirements

- Your system must use `NetworkManager` to manage Wi-Fi.
- The current user must have read access to the connection files (root by default).

### To enable password access:

1. Run the application with elevated privileges:

   ```
   sudo python main.py
   ```

   This ensures it can read from `/etc/NetworkManager/system-connections/`.

2. **Or**, change permissions manually (less secure):

   Make the connection files readable (use with caution):

   ```bash
   sudo chmod +r /etc/NetworkManager/system-connections/*
   sudo chmod +x /etc/NetworkManager/system-connections
   ```

   > Note: This may expose your saved Wi-Fi passwords to all users. Use only in trusted environments.
