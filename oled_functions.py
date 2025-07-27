from time import ticks_ms, ticks_diff
import framebuf
import random

# --- Animation state ---
_last_blink_time = 0
_blinking = False
_next_blink_interval = None
_shake_start = None
_headpat_start = None

# --- Timing constants (ms) ---
BLINK_DURATION = 140
SHAKE_DURATION = 1400
HEADPAT_DURATION = 1200
SWAY_PERIOD = 1800

# --- ASCII-only, single-line, horizontal faces ---
FACES = {
    "happy":        ["(^_^)", "('-')", "(=^.^=)"],
    "really_happy": ["(^o^)", "(*^_^*)"],
    "curious":      ["(o_o)", "(-_-?)", "(._.)"],
    "concerned":    ["(>_<)", "(._.)"],
    "sad":          ["(T_T)", "(';_;)"],
    "sleepy":       ["(-_-)", "(u_u)"],
    "mischief":     ["(¬‿¬)", "(^_~)"],
    "surprised":    ["(O_O)", "(o_O)"],
    "angry":        ["(>_<)", "(>:[)"],
    "cool":         ["(-_-)", "(B-)"],
    "love":         ["(^3^)", "(^.^)"],
    "headpat":      ["(^_^)", "(^_^*)"],   # Second one gets 'blush'
    "shake":        ["(@_@)", "(x_x)", "(O_o)"]
}

def _get_blink_interval():
    # 3-6s random blink interval in ms
    return random.randint(3000, 6000)

def _translate_emoji_blink(face):
    return (face
            .replace('^', '-')
            .replace('o', '-')
            .replace('O', '-')
            .replace('x', '-')
            .replace('_', '-'))

def _draw_ascii(oled, text, x, y):
    oled.text(text, x, y, 1)

def _centered_x(face):
    w = len(face) * 8
    return max((128 - w) // 2, 0)

def get_face_and_x(mood, now, anim_state):
    # Pick face and animate X for current mood
    if mood == "happy":
        idx = (now // 2000) % len(FACES["happy"])
        face = FACES["happy"][idx]
    elif mood == "really_happy":
        idx = (now // 1700) % len(FACES["really_happy"])
        face = FACES["really_happy"][idx]
    elif mood == "shake":
        # 3 frames, rapid jerk, off-center
        phase_len = 210
        frame = ((ticks_diff(now, anim_state["start"]) // phase_len) % 3)
        face = FACES["shake"][frame]
        offset_seq = [-11, 0, 10]
        x = _centered_x(face) + offset_seq[frame]
        return face, x
    elif mood == "headpat":
        # 2-frame, gentle with blush
        elapsed = ticks_diff(now, anim_state["start"])
        phase = (elapsed // 400) % 2
        face = FACES["headpat"][phase]
        x = _centered_x(face) + (2 if phase else -3)
        if phase == 1:
            face = face.replace(')', '*)', 1)
        return face, x
    else:
        # Sway for everything else
        period = SWAY_PERIOD
        try:
            from math import sin, pi
            t = (now % period) / period
            swing = int(7 * sin(2 * pi * t))
        except Exception:
            swing = 0
        key = FACES.get(mood, FACES["curious"])
        idx = (now // 2600) % len(key)
        face = key[idx]
        x = _centered_x(face) + swing
        return face, x

    # Default centering
    x = _centered_x(face)
    return face, x

def update_oled(oled, mood="happy", value=50):
    global _last_blink_time, _blinking, _next_blink_interval, _shake_start, _headpat_start
    now = ticks_ms()
    anim_state = {}

    # --- Animation stateful setup ---
    if mood == "shake":
        if _shake_start is None:
            _shake_start = now
        anim_state["start"] = _shake_start
        if ticks_diff(now, _shake_start) > SHAKE_DURATION:
            _shake_start = None
            mood = "happy"
    else:
        _shake_start = None
    if mood == "headpat":
        if _headpat_start is None:
            _headpat_start = now
        anim_state["start"] = _headpat_start
        if ticks_diff(now, _headpat_start) > HEADPAT_DURATION:
            _headpat_start = None
            mood = "happy"
    else:
        _headpat_start = None

    # --- Blinking logic (random interval, never during shake/headpat) ---
    blinkable = mood not in ("shake", "headpat")
    if _next_blink_interval is None:
        _next_blink_interval = _get_blink_interval()
    if blinkable:
        if ticks_diff(now, _last_blink_time) > _next_blink_interval:
            _blinking = True
            _last_blink_time = now
            _next_blink_interval = _get_blink_interval()
        if _blinking and ticks_diff(now, _last_blink_time) > BLINK_DURATION:
            _blinking = False

    face, x = get_face_and_x(mood, now, anim_state)
    if blinkable and _blinking:
        face = _translate_emoji_blink(face)
    oled.fill(0)
    _draw_ascii(oled, face, x, 27)
    oled.show()

def demo_emotions(oled):
    from time import sleep_ms
    loop = [
        "happy", "curious", "mischief",
        "surprised", "cool", "sad", "shake", "headpat"
    ]
    for mood in loop:
        frames = 26 if mood in ("shake", "headpat") else 18
        for _ in range(frames):
            update_oled(oled, mood)
            sleep_ms(68)

# Example usage:
# oled_functions.update_oled(oled, "shake")
# Call update_oled() regularly (e.g., inside your main loop or timer).
