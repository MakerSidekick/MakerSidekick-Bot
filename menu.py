from machine import Pin
from time import sleep_ms, ticks_ms, ticks_diff
from pin_values import code_debug_pin_value, buzzer_pin_value, led_pin_value

code_debug_pin = Pin(code_debug_pin_value, Pin.IN, Pin.PULL_UP)
led = Pin(led_pin_value, Pin.OUT)

def open_menu():
    print("Now in menu mode")
    while True:
        led.value(1)
        sleep_ms(250)
        led.value(0)
        sleep_ms(250)
        
        if code_debug_pin.value() == 0:  # Button pressed (active low)
            press_start = ticks_ms()
            # Wait while the button is held down
            while code_debug_pin.value() == 0:
                sleep_ms(10)
            press_duration = ticks_diff(ticks_ms(), press_start)
            
            if press_duration >= 3000:  # 3 seconds (3000 ms)
                print("Exiting Menu Mode!")
                return True
            else:
                print("Short press detected, ignoring for now.")
                # Pass for now, do nothing


