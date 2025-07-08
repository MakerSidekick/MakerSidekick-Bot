from machine import Pin, PWM
import time

from pin_values import buzzer_pin_value, led_pin_value

# Initialize PWM for the buzzer and digital output for the LED
buzzer = PWM(Pin(buzzer_pin_value))
buzzer.duty_u16(0)  # Ensure buzzer is silent at startup

led = Pin(led_pin_value, Pin.OUT)
led.value(0)        # Ensure LED is off at startup

def startup_shush():
    """Ensure the buzzer is silent at startup."""
    buzzer.duty_u16(0)

def play_tone(freq, duration):
    """Play a tone at the given frequency (Hz) and duration (ms)."""
    led.value(1)
    buzzer.freq(freq)
    buzzer.duty_u16(32768)  # 50% duty cycle
    time.sleep_ms(duration)
    buzzer.duty_u16(0)
    led.value(0)

def happy_sound():
    notes = [1319, 1568, 1760, 2093, 2349, 2637]
    durations = [18, 18, 18, 18, 18, 40]
    for note, dur in zip(notes, durations):
        play_tone(note, dur)

def angry_sound():
    notes = [1865, 1760, 1661, 1568, 1479, 1397, 1245]
    duration_per_note = 30
    for note in notes:
        play_tone(note, duration_per_note)

def shook_sound():
    notes = [1568, 1245, 1568, 1319, 1568, 1175, 1568, 1319]  # G6, D#6, G6, E6, G6, D6, G6, E6
    duration_per_note = 12
    # Repeat the sequence twice for a trembling effect
    for _ in range(3):
        for note in notes:
            play_tone(note, duration_per_note)

def headpat_sound():
    notes = [1175, 1397, 1760, 2093, 2637]  # D6, F6, A6, C7, E7
    durations = [15, 15, 15, 15, 80]        # Last note is much longer
    for note, dur in zip(notes, durations):
        play_tone(note, dur)

def click_sound():
    """
    Redesigned: Two sharp, percussive blips separated by a brief silence.
    """
    play_tone(3000, 20)
    time.sleep_ms(30)
    play_tone(4000, 20)

def startup_sequence():
    """
    Redesigned: Four quick clicks, each with increasing pitch, followed by the new headpat sound.
    """
    click_notes = [2000, 2500, 3000, 3500]
    for note in click_notes:
        play_tone(note, 15)
        time.sleep_ms(20)
    headpat_sound()

def curious_scared_sound():

    intro_notes = [1319, 1568, 1760]
    for note in intro_notes:
        play_tone(note, 18)
    time.sleep_ms(30)
    shook_sound()

# Run test sequence if the script is executed directly
if __name__ == "__main__":
    startup_shush()
    startup_sequence()
    time.sleep_ms(500)
    happy_sound()
    time.sleep_ms(500)
    angry_sound()
    time.sleep_ms(500)
    shook_sound()
    time.sleep_ms(500)
    curious_scared_sound()

