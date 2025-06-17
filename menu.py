# Call this if you want a menu. For now, this is a placeholder for an actual menu
# blinks the light 25 times

from machine import TouchPad, Pin
from time import sleep_ms

led = Pin(2, Pin.OUT)

def open_menu():
    print("Now in menu modde")
    for i in range(25):
        led.value(1)
        sleep_ms(250)
        led.value(0)
        sleep_ms(250)
    print("Exiting Menu Mode!")