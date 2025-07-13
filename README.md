# Windows Volume Control Plugin for Flow Launcher

A  Flow Launcher plugin for controlling Windows system volume 

---

## Key Features

- **Display Current Volume**  
  Instantly see your current master volume level.
- **Adjust Volume in 10% Increments**  
  Increase or decrease volume by 10% with `vol up` and `vol down`.
- **Set Absolute Volume**  
  Jump to any level (0–100%) via `vol 75` or `vol 50`.
- **Mute/Unmute Toggle**  
  Toggle mute state with `vol mute`.
- **Max Volume Shortcut**  
  Crank it to 100% instantly with `vol max`.

---

## Installation

### End User (Pre-built)

1. Download or clone the `Flow.Launcher.Plugin.VolumeControl` folder.  
2. Copy the these files and folders: `vol_control.exe`, `main.py`, `plugin.json`, and `Images` into Flow Launcher’s plugins directory:  
   `%APPDATA%\FlowLauncher\Plugins\`  
3. Restart Flow Launcher.  


### Developer (Build from Source)

1. Ensure **Rust** and **Python 3.x** are installed.  
2. Open a terminal in the plugin root, then:
   ```bash
   cd rust_source
   cargo build --release
   cd ..
   copy rust_source/target/release/vol_control.exe .
   ```
3. Restart Flow Launcher to pick up your new build.
4. (Optional) you can build using the provided `build.bat` or `build.sh` script:
   ```bash
   ./build.sh
   ```
    or on Windows:
    ```powershell
   ./build.bat
   ```

---

## Usage

Type `vol` in Flow Launcher to see available commands:

| Command       | Description                           |
| ------------- | ------------------------------------- |
| `vol`         | Show current volume level             |
| `vol up`      | Increase volume by 10%                |
| `vol down`    | Decrease volume by 10%                |
| `vol mute`    | Toggle mute on/off                    |
| `vol max`     | Set volume to 100%                    |
| `vol <0–100>` | Set volume to an exact percentage     |

You can also run the Rust executable directly:

```bash
vol_control.exe get
vol_control.exe set 30
vol_control.exe up
vol_control.exe down
vol_control.exe toggle-mute
vol_control.exe max
```

---

## How It Works

This plugin consists of two components:

1. **Rust Backend** (`vol_control.exe`)  
   Handles low-level Windows API calls for volume manipulation.
2. **Python Frontend** (`main.py`)  
   Interfaces with Flow Launcher, parsing user input and displaying results.

---

## Troubleshooting

- **Plugin Not Listed**  
  - Verify the folder is copied under `%APPDATA%\FlowLauncher\Plugins\`.  
  - Fully restart Flow Launcher.
- **Commands Fail**  
  - Confirm `vol_control.exe` is present alongside `main.py`.  
  - Ensure Python 3.x is installed and on your PATH.
- **Missing Icon**  
  - Add a 64×64 PNG named `icon.png` to `Images/`.  
  - The plugin functions without an icon but will use a default placeholder.

---

## THANKS
Special thanks to [Freepik](https://www.freepik.com) for the speaker icon used in this plugin.
[Speaker icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/speaker)

## License

MIT © 2025 Saif Al-zharani 
Contributions and feedback are welcome!
