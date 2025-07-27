# Based on Example code for (GY-521) MPU6050 Accelerometer/Gyro Module
# Written in MicroPython by Warayut Poomiwatracanont JAN 2023
# Base Code: https://github.com/Lezgend/MPU6050-MicroPython/blob/main/main.py
# Current Project: https://github.com/MakerSidekick/MakerSidekick-Bot/blob/main/main.py

from MPU6050 import MPU6050
from machine import Pin, ADC, I2C
from time import sleep_ms
from buzzer_sounds import (
    startup_shush, startup_sequence, happy_sound,
    angry_sound, shook_sound, headpat_sound, curious_scared_sound
)
from happy_meter import meter as get_happy
from menu import open_menu
from pin_values import touch_pin_value, code_debug_pin_value
import ssd1306
import oled_functions

# === OLED & I2C Initialization ===
i2c_bus = I2C(0, scl=Pin(0), sda=Pin(1), freq=100_000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c_bus)

# === DEVICES/SENSORS ===
mpu = MPU6050(i2c_bus)
touch_sensor = ADC(Pin(touch_pin_value))
debug_button = Pin(code_debug_pin_value, Pin.IN, Pin.PULL_UP)

# === EMOTIONAL STATE COUNTERS ===
happy_level = 35
headpat_count = 0
shake_count = 0
movement_count = 0

# === Constants ===
HEADPAT_THRESHOLD = 4
SHAKE_THRESHOLD = 7
MOVEMENT_SENSITIVITY = 2
GENTLE_MOVEMENT = 1300  # Below = "still"
ROUGH_MOVEMENT = 2500   # Above = "agitated"

# === STARTUP/INTRO ===
print("🤖 Robot Pet Starting Up! (˶ᵔ ᵕ ᵔ˶)")
startup_shush()
oled_functions.update_oled(oled, "happy", 85)
startup_sequence()
print("🎮 Robot Pet Ready! (っ´ω`)ﾉ")

# === MAIN LOOP ===
while True:
    try:
        # Read all sensors
        acceleration = mpu.read_accel_data()
        movement_force = mpu.read_accel_abs(g=True) * 1000
        touch_value = touch_sensor.read()

        # Shake reactions
        if movement_count >= MOVEMENT_SENSITIVITY:
            print("😵 I'm getting dizzy! (⸝⸝๑﹏๑⸝⸝)")
            oled_functions.update_oled(oled, "shake")
            shook_sound()
            sleep_ms(100)
            shook_sound()
            shake_count += 1
            movement_count = 0
            if shake_count >= SHAKE_THRESHOLD:
                happy_level = 0
                shake_count = 0
                print("💔 All trust lost! I'm extremely dizzy and sad...")
                sleep_ms(150)
                oled_functions.update_oled(oled, "happy", 10)
            continue

        # Movement logic
        if movement_force <= GENTLE_MOVEMENT:
            movement_count = 0

        if movement_force >= ROUGH_MOVEMENT:
            movement_count += 1
            if happy_level < 75:
                angry_sound()
                print("😠 Hey! What was that for! ヽ(｀Д´)ﾉ")
            else:
                curious_scared_sound()
                print("😮 Whoa, are you taking me somewhere? (ﾟοﾟ)")
            happy_level = get_happy("reduce", happy_level)

        # Touch/headpat reactions
        if touch_value > 1000:
            print("😊 Headpat detected! (っ´ω`)ﾉ(˵•́ ᴗ •̀˵)")
            headpat_sound()
            happy_level = get_happy("add", happy_level, 0.2)
            headpat_count += 1
            oled_functions.update_oled(oled, "headpat")
            sleep_ms(250)
            if headpat_count > HEADPAT_THRESHOLD:
                print("💖 I'm so happy! ( ˶ˆᗜˆ˵ )")
                oled_functions.update_oled(oled, "headpat")
                happy_sound()
                sleep_ms(150)
                happy_sound()
                if happy_level >= 75:
                    for _ in range(3):
                        happy_sound()
                        sleep_ms(50)
                headpat_count = 0
                shake_count = 0
                happy_level = get_happy("add", happy_level)

        # Regular mood display
        oled_functions.update_oled(oled, "happy", happy_level)

        # Debug menu access
        if debug_button.value() == 0:
            open_menu()
            startup_sequence()
            oled_functions.update_oled(oled, "happy", 85)

        sleep_ms(150)

    except Exception as e:
        print("Error in main loop:", e)
        sleep_ms(1000)