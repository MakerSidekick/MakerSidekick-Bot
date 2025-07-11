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
SCL -> GPIO 5\
SDA -> GPIO 4

> [!TIP]
> (You can change SCL pin and SDA pin in file [MPU6050.py line 73](MPU6050.py#L73))

Pin assignment for ESP32 and Buzzer:\
GPIO 3 -> Buzzer Terminal\
GND -> Buzzer Terminal
> [!TIP]
> (You can change buzzer pin in file [pin_values.py line 6](pin_values.py#L6))

Pin assignment for ESP32 and Touch Pin(For registering headpats):\
GND --(Resistor with 220k to 560k Ohm)--> Pin A2 -> Metal Contact
> [!TIP]
> (You can change touch pin in file [pin_values.py line 4](pin_values.py#L4))

Pin assignment for ESP32 to Debug Pin(To start code execution, for debugging):\
GPIO 8 -> GND
> [!TIP]
> (You can change enable pin in file [pin_values.py line 5](pin_values.py#L5))
If this button is pressed in main mode, it stops execution. If it is pressed in debug mode, it exits the menu and goes back to main mode. 