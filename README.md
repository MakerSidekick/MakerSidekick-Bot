# MPU6050-MicroPython
A very simple portable "Sidekick" Bot powered by GY-521 IMU 3-axis Accelerometer/Gyro Module (MPU6050) on ESP32 using MicroPython

## Info
A simple expressive home-made open source Buddy made with lying around hobbyist parts, powered by an esp32. Because of this, it will be infinitely hackable, allowing end users to install their own firmware or features if they wish.

Loosely inspired by tamagotchi and community-made desk toys, it will react to its surroundings through gyro movement, and expresses itself accordingly through the display and more!

> [!NOTE] 
> Project state: Initial Planning/FAFO

Future home for the project: https://github.com/sounddrill31/Social-Buddy/\
Project Code: https://github.com/MakerSidekick/MakerSidekick-Bot

## Wiring
Pin assignment for ESP32:\
VCC -> 3v3\
SCL -> GPIO 22\
SDA -> GPIO 21\
\
(You can change SCL pin and SDA pin in file MPU6050.py line 73)
