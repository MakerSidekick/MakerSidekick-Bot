from machine import Pin, PWM
import time

buzzer_pin = 32  # Change to your actual buzzer pin
buzzer = PWM(Pin(buzzer_pin))
buzzer.duty_u16(0) # 0% duty cycle, no output

led = Pin(2, Pin.OUT)

def play_tone(freq, duration):
    led.value(1)
    buzzer.freq(freq)
    buzzer.duty_u16(32768)  # 50% duty cycle
    time.sleep_ms(duration)
    buzzer.duty_u16(0)
    led.value(0)

def happy_sound():
    # Bright, cheerful, and smooth for piezo buzzers
    notes = [2093, 2637, 3136, 3520, 3951]  # C7, E7, G7, A7, B7
    duration_per_note = 22  # ms
    for note in notes:
        play_tone(note, duration_per_note)

def angry_sound():
    """
    Angrier rapid, harsh descending melody with dissonant intervals.
    """
    notes = [1568, 1397, 1319, 1175, 1109, 1047, 1245]  # G6, F6, E6, D6, C#6, C6, D#6 (dissonant end)
    duration_per_note = 50  # ms for fast, aggressive feel
    for note in notes:
        play_tone(note, duration_per_note)

def shook_sound():
    """
    Anxious, trembling effect: rapid, dissonant jumps in the same range as angry_sound.
    Designed as a companion, with a zig-zag and stuttery feel.
    """
    notes = [1568, 1319, 1568, 1397, 1245, 1397, 1175, 1319]  # G6, E6, G6, F6, D#6, F6, D6, E6
    duration_per_note = 22  # ms for a jittery, nervous effect
    for note in notes:
        play_tone(note, duration_per_note)

def headpat_sound():
    # Distinct, happy, short upward chirp (like a "ding!")
    notes = [1319, 1397, 1568, 1760, 2093]  # E6, F6, G6, A6, C7
    duration_per_note = 40  # ms
    for note in notes:
        play_tone(note, duration_per_note)
        
def click_sound():
    notes = [2500, 3500]
    duration_per_note = 40  # ms
    for note in notes:
        play_tone(note, duration_per_note)

def startup_sound_main():
    # Gentle, welcoming major arpeggio
    notes = [1047, 1319, 1568, 2093]  # C6, E6, G6, C7
    durations = [60, 60, 60, 90]  # Slightly longer last note for a soft finish
    for note, dur in zip(notes, durations):
        play_tone(note, dur)

def startup_sequence():
    time.sleep_ms(50)
    click_sound()
    time.sleep_ms(150)
    startup_sound_main()
    click_sound()
    startup_sound_main()
    time.sleep_ms(15)
    click_sound()
    time.sleep_ms(70)
    headpat_sound()
    click_sound()

# For testing, only when run as the same file
if __name__ == "__main__":
    startup_sequence()
    time.sleep_ms(500)
    happy_sound()
    time.sleep_ms(500)
    angry_sound()
    time.sleep_ms(500)
    shook_sound()