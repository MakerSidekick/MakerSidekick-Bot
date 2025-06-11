# Example code for (GY-521) MPU6050 Accelerometer/Gyro Module
# Write in MicroPython by Warayut Poomiwatracanont JAN 2023

from MPU6050 import MPU6050

from os import listdir, chdir
from machine import TouchPad,Pin
from time import sleep_ms

# Movement Definitions
mpu = MPU6050()
move_val = 0 # Track shake value
fragile = 2 # Number of shakes the buddy can handle

# Touch Definitions
capacitiveValue = 300
touch_threshold = 150 # Touch threshold to be adjusted
touch_pin = TouchPad(Pin(13))
headpat_val = 0 # Track value for headpats
headpat_threshold = 3

print("Starting Up! (˶ᵔ ᵕ ᵔ˶)")

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
    if mul_gforce >= 3000: # sudden frequent movement
        move_val+=1
    if mul_gforce <= 1500: # not moved in a while 
        move_val=0
    if move_val >= fragile: # check if we've exceeded the fragile threshold
        print("I'm shook! I'm dizzy! (⸝⸝๑﹏๑⸝⸝)")
        break
    
    # Touch Pins
    capacitiveValue = touch_pin.read()
    if capacitiveValue < touch_threshold:
        print("Headpat detected (っ´ω`)ﾉ(˵•́ ᴗ •̀˵)")
        headpat_val += 1
    if headpat_val > headpat_threshold:
        print("State Happy ( ˶ˆᗜˆ˵ )")
        headpat_val = 0
        continue

    print("\n")
    # Time Interval Delay in millisecond (ms)
    sleep_ms(100)