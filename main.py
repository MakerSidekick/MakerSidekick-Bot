# Based on Example code for (GY-521) MPU6050 Accelerometer/Gyro Module
# Written in MicroPython by Warayut Poomiwatracanont JAN 2023
# Base Code: https://github.com/Lezgend/MPU6050-MicroPython/blob/main/main.py
# Current Project: https://github.com/MakerSidekick/MakerSidekick-Bot/blob/main/main.py

from MPU6050 import MPU6050

from os import listdir, chdir
from machine import Pin, ADC#, TouchPad
from time import sleep_ms
from buzzer_sounds import startup_sequence, happy_sound, angry_sound, shook_sound, headpat_sound, startup_shush, curious_scared_sound
from happy_meter import meter as get_happy
from menu import open_menu
from pin_values import touch_pin_value, code_debug_pin_value

# Silence the buzzer during startup
startup_shush()

# Movement Definitions
mpu = MPU6050()
move_val = 0 # Track sudden movement value
shook_value = 0 # Track number of shakes
shook_threshold = 7 # Exceed this and the buddy feels extremely distrustful
fragile = 2 # Number of shakes the buddy can handle

# Touch Definitions

ADCtouchValue = 0
touch_threshold = 1000 # Touch threshold to be adjusted
#touch_pin = TouchPad(Pin(touch_pin_value))
touch_pin = ADC(Pin(touch_pin_value))

code_debug_pin = Pin(code_debug_pin_value, Pin.IN, Pin.PULL_UP) # This is a button that can interrupt running program

headpat_val = 0 # Track value for headpats
headpat_threshold = 4

print("Starting Up! (˶ᵔ ᵕ ᵔ˶)")
startup_sequence() #TODO: IMPLEMENT MUTE MODE

Happy_value = 35

while True:
    # Accelerometer Data
    accel = mpu.read_accel_data() # read the accelerometer [ms^-2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]
    print("x: " + str(aX) + " y: " + str(aY) + " z: " + str(aZ))
  
    # Gyroscope Data
    gyro = mpu.read_gyro_data()   # read the gyro [deg/s]
    gX = gyro["x"]
    gY = gyro["y"]
    gZ = gyro["z"]
    print("x:" + str(gX) + " y:" + str(gY) + " z:" + str(gZ))

    # Rough Temperature
    temp = mpu.read_temperature()   # read the device temperature [degC]
    print("Temperature: " + str(temp) + "°C")

    # G-Force
    gforce = mpu.read_accel_abs(g=True) # read the absolute acceleration magnitude
    mul_gforce = gforce * 1000 # make the tiny value more pronounced by multiplying with 1000
    print("G-Force: " + str(gforce))
    print("Multiplied G-Force:" + str(mul_gforce))
       
    if mul_gforce <= 1300: # moved suddenly 
        move_val=0
    if move_val >= fragile: # check if we've exceeded the fragile threshold
        print("I'm shook! I'm dizzy! (⸝⸝๑﹏๑⸝⸝)")
        shook_sound()
        sleep_ms(150)
        shook_sound()
        sleep_ms(200)
        shook_value += 1
        if shook_value >= shook_threshold:
            Happy_value = 0 # Lose all trust, you've shaken me too many times!
            print("All Trust Lost! Bot is extremely dizzy...") # In the future, this action will take us to menu
            #print("Bot will enter debug/menu mode!!")
            #print("	┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻")
            shook_value = 0
            sleep_ms(2500)
            #open_menu()
            startup_sequence() # Give the illusion of starting up again, since we're back from menu

        #break
        #continue
    if 2000 < mul_gforce < 2500:
        pass # TODO: Implement curious state, silent observer
    if mul_gforce >= 2500: # sudden frequent movement
        move_val+=1
        if Happy_value < 75: # if the bot is overall happy, it will endure assuming that this was a mistake but still become unhappy
            angry_sound()
            print("Whoa, what was that for! ヽ(｀Д´)ﾉ")
        else:
            curious_scared_sound() # Bot trusts, but is still shaken
            print("Whoa, are you taking me somewhere? Oo")
        Happy_value = get_happy("reduce", Happy_value) # We're sad! Human shook us!

    # Touch Pins
    ADCtouchValue = touch_pin.read()
    print("Touch Pin ADC Value: " + str(ADCtouchValue))
    if headpat_val > headpat_threshold: # check if we've exceeded the headpat threshold
        print("State Happy ( ˶ˆᗜˆ˵ )")
        happy_sound()
        sleep_ms(150)
        happy_sound()
        headpat_val = 0
        Happy_value = get_happy("add", Happy_value) # We're happy!
        shook_value = 0

        if Happy_value >= 75:
            for i in range(3):
                happy_sound() # It's really happy!
        sleep_ms(200)
        continue
    if ADCtouchValue > touch_threshold: # check if we've hit the threshold to count the touch
        print("Headpat detected (っ´ω`)ﾉ(˵•́ ᴗ •̀˵)")
        sleep_ms(225)
        headpat_sound()
        Happy_value = get_happy("add", Happy_value, 0.2) # We're a little happier!
        sleep_ms(250)
        headpat_val += 1

    print("\n")

    if code_debug_pin.value() == 0:  # Returns 0 when grounded
        #break # If code_debug_pin is grounded, kill the loop and allow finishing execution
        open_menu()
        startup_sequence() # Give the illusion of starting up again, since we're back from menu
    sleep_ms(1)

    # Time Interval Delay in millisecond (ms)
    sleep_ms(150)

