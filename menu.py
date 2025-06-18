# Call this if you want a menu. For now, this is a placeholder for an actual menu
# blinks the light 25 times

from machine import TouchPad, Pin
from time import sleep_ms
from pin_values import code_debug_pin_value, buzzer_pin_value, led_pin_value #, touch_pin_value

#touch_pin = TouchPad(Pin(touch_pin_value))
code_debug_pin = Pin(code_debug_pin_value, Pin.IN, Pin.PULL_UP) # This is a button that can jump from menu mode back to main mode
led = Pin(led_pin_value, Pin.OUT)

def open_menu():
    print("Now in menu modde")
    while True:
        led.value(1)
        sleep_ms(250)
        led.value(0)
        sleep_ms(250)
        if code_debug_pin.value() == 0:
            print("Exiting Menu Mode!")
            return True