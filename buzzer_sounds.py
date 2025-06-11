from machine import Pin, PWM
import time

buzzer_pin = 32  # Change to your actual buzzer pin
buzzer = PWM(Pin(buzzer_pin))
buzzer.duty_u16(0) # 0% duty cycle, no output

def play_tone(freq, duration):
    buzzer.freq(freq)
    buzzer.duty_u16(32768)  # 50% duty cycle
    time.sleep_ms(duration)
    buzzer.duty_u16(0)

def shook_sound():
    # Scared/anxious: rapid, dissonant jumps
    freq_sequence = [700, 750, 680, 720, 690, 740]
    duration_per_tone = 30  # ms
    for freq in freq_sequence:
        play_tone(freq, duration_per_tone)

def angry_sound():
    # Pokémon villain: short, descending, menacing
    notes = [880, 830, 780]
    duration_per_note = 50  # ms
    for note in notes:
        play_tone(note, duration_per_note)

def happy_sound():
    # Short, cheerful
    notes = [440, 550]
    duration_per_note = 25  # ms
    for note in notes:
        play_tone(note, duration_per_note)

def headpat_sound():
    # Distinct, happy, short upward chirp (like a "ding!")
    notes = [660, 880]  # E5, A5
    duration_per_note = 35  # ms
    for note in notes:
        play_tone(note, duration_per_note)

def startup_sound():
    # quick, bright, and welcoming arpeggio
    notes = [523, 659, 784, 1047]
    duration_per_note = 50  # ms
    for note in notes:
        play_tone(note, duration_per_note)

# For testing, only when run as the same file
if __name__ == "__main__":
    startup_sound()
    time.sleep_ms(500)
    happy_sound()
    time.sleep_ms(500)
    angry_sound()
    time.sleep_ms(500)
    shook_sound()