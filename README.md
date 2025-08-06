# MPU6050-MicroPython
A very simple portable "Sidekick" Bot powered by GY-521 IMU 3-axis Accelerometer/Gyro Module (MPU6050) on ESP32 using MicroPython

## Info
A simple expressive home-made Open-Source Buddy made with lying-around hobbyist parts, powered by an ESP32 Development Board. Thanks to this, it will be infinitely hackable, allowing end users to install their own firmware or features if they wish.

Loosely inspired by tamagotchi and community-made desk toys, it will react to its surroundings through gyro movement, and expresses itself accordingly through the display and more!

> [!NOTE] 
> Project state: Initial Planning/FAFO

<!--Future home for the project: https://github.com/sounddrill31/Social-Buddy/-->

Project Code: https://github.com/MakerSidekick/code

## Automatic Setup/Flash

### Prepare this repo:
```bash
git clone https://github.com/MakerSidekick/MakerSidekick-Bot
```

### Enter the Folder: 
```bash
cd MakerSidekick-Bot
```

### Setup Prerequisites:
Install `pixi` tool from the official link: https://pixi.sh/latest/#installation

Easy Setup Commands(Subject to change)
- Linux/MacOS (Close and Reopen shell after it's done installing)
    ```bash
    curl -fsSL https://pixi.sh/install.sh | sh
    ```
- Windows
    ```cmd
    powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
    ```

    OR

    Releases(has installer packages): https://github.com/prefix-dev/pixi/releases/latest

    x86_64 Installer: https://github.com/prefix-dev/pixi/releases/latest/download/pixi-x86_64-pc-windows-msvc.msi

### Setup Environment:
```bash
pixi install
```
### Upload:
```bash
pixi run upload
```

## Manual Setup/Flash

### Prepare this repo:
```bash
git clone https://github.com/MakerSidekick/MakerSidekick-Bot
```

### Enter the Folder: 
```bash
cd MakerSidekick-Bot
```

### Clone Libraries:
```bash 
git clone https://github.com/stlehmann/micropython-ssd1306 lib/
```

### Cleanup to save space: 
```
lib/.gitignore
lib/README.md
lib/sdist_upip.py
lib/setup.py
lib/.git
```

(adjust commands for other systems/shells)

Bash:
```bash 
rm -rf lib/.git lib/.gitignore lib/README.md lib/sdist_upip.py lib/setup.py
```

Cmd/Powershell: 
```
rmdir /s /q "lib\.git"
del "lib\.gitignore"
del "lib\README.md"
del "lib\sdist_upip.py"
del "lib\setup.py"
```

### Next Steps:
> [!TIP]
> Automating this with mpremote would be prudent. Check out upload-to-esp32.py in this folder.

- Open Folder in Thonny
- Upload lib folder
- Upload `.py` files

## Modes
### Normal Mode 
<!-- Attach Pic -->
Social Buddy, the Maker's Sidekick! It will react to surroundings 

### Menu Mode 
<!-- Attach Pic-->
Select Options. Placeholder for now, it just blinks led 25 times

Eventually will be able to launch user's custom code! 
<!-- ### Custom Code Mode-->


## Wiring
Pin assignment for ESP32 and MPU6050:\
VCC -> 3v3\
GND -> GND\
SCL -> GPIO A0\
SDA -> GPIO A1

> [!TIP]
> (You can change SCL pin and SDA pin in file [main.py line 17](main.py#L17))

Pin assignment for ESP32 and Buzzer:\
GPIO 8 -> Buzzer Terminal\
GND -> Buzzer Terminal
> [!TIP]
> (You can change buzzer pin in file [pin_values.py line 6](pin_values.py#L6))

> [!WARNING]
> Touch pin isn't working as expected :( 
    It works as a touch pin but it's not super good at sensing values, especially when the device is far-ish away! 

Pin assignment for ESP32 and Touch Pin(For registering headpats):\
GND --(Resistor with 220k to 560k Ohm)--> Pin A2 -> Metal Contact

> [!TIP]
> (You can change touch pin in file [pin_values.py line 4](pin_values.py#L4)) 

Pin assignment for ESP32 to Debug Pin(<!--To start code execution-->, for debugging):\
GPIO 8 -> GND
> [!TIP]
> (You can change enable pin in file [pin_values.py line 5](pin_values.py#L5))
If this button is pressed in main mode, it stops execution. If it is pressed in debug mode, it exits the menu and goes back to main mode. 
