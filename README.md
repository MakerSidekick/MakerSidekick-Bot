# MPU6050-MicroPython
A very simple portable "Sidekick" Bot powered by GY-521 IMU 3-axis Accelerometer/Gyro Module (MPU6050) on ESP32 using MicroPython

## Info
A simple expressive home-made Open-Source Buddy made with lying-around hobbyist parts, powered by an ESP32 Development Board. Thanks to this, it will be infinitely hackable, allowing end users to install their own firmware or features if they wish.

Loosely inspired by tamagotchi and community-made desk toys, it will react to its surroundings through gyro movement, and expresses itself accordingly through the display and more!

> [!NOTE] 
> Project state: Initial Planning/FAFO

Future home for the project: https://github.com/sounddrill31/Social-Buddy/

Project Code: https://github.com/MakerSidekick/MakerSidekick-Bot

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
SCL -> GPIO 22\
SDA -> GPIO 21

> [!TIP]
> (You can change SCL pin and SDA pin in file [MPU6050.py line 73](MPU6050.py#L73))

Pin assignment for ESP32 and Buzzer:\
GPIO 32 -> Buzzer Terminal\
GND -> Buzzer Terminal
> [!TIP]
> (You can change buzzer pin in file [buzzer_sounds.py line 4](buzzer_sounds.py#L4))

Pin assignment for ESP32 and Touch Pin(For registering headpats):\
GPIO 13 -> Metal Contact
> [!TIP]
> (You can change touch pin in file [main.py line 24](main.py#L24))

Pin assignment for ESP32 to Enable Pin(To start code execution, for debugging):\
GPIO 12 -> GND
> [!TIP]
> (You can change enable pin in file [main.py line 25](main.py#L25))
If you want the code to run without enable pin, uncomment [main.py's line 26](main.py#L26)