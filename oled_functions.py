from time import ticks_ms, ticks_diff

# OLED emoji animation state variables (module-global)
_last_blink_time = 0
_blinking = False
_shake_start = None
_headpat_start = None

BLINK_INTERVAL = 3000  # ms between blinks
BLINK_DURATION = 150   # ms duration of blink
SHAKE_DURATION = 800   # ms total shake animation
HEADPAT_DURATION = 500 # ms total headpat animation

SHAKE_FRAMES = ["@_@", "x_x", "@_@", "X_X"]
HEADPAT_FRAMES = [">_<", "^_^", "=^_^="]

EMOJI_STATES = {
    "really_excited": "^o^",
    "really_happy": "^_^",
    "happy": ":)",
    "curious": "o_o",
    "concerned": ">_<",
    "sad": "T_T",
    "very_sad": ";_;",
}

def _translate_emoji_blink(emoji):
    blink_map = {
        '^': '-', 'o': '-', 'O': '-', '@': '-', '.': '-', '*': '-',
        'T': '-', 'v': '-', '<': '-', '=': '-', 'X': '-', '>': '-',
        ';': '-', ':': '-'
    }
    return ''.join(blink_map.get(c, c) for c in emoji)


def get_emoji(mood, value=50, now_ms=None):
    global _shake_start, _headpat_start

    if now_ms is None:
        now_ms = ticks_ms()

    if mood == "shake":
        if _shake_start is None:
            _shake_start = now_ms
        elapsed = ticks_diff(now_ms, _shake_start)
        frame = (elapsed // 200) % len(SHAKE_FRAMES)
        emoji = SHAKE_FRAMES[frame]
        if elapsed > SHAKE_DURATION:
            _shake_start = None
            mood = "happy"
    elif mood == "headpat":
        if _headpat_start is None:
            _headpat_start = now_ms
        elapsed = ticks_diff(now_ms, _headpat_start)
        if elapsed < 200:
            emoji = HEADPAT_FRAMES[0]
        elif elapsed < 400:
            emoji = HEADPAT_FRAMES[1]
        elif elapsed < HEADPAT_DURATION:
            emoji = HEADPAT_FRAMES[2]
        else:
            _headpat_start = None
            mood = "happy"

    if mood == "happy":
        value = max(0, min(100, value))
        if value >= 95:
            emoji = EMOJI_STATES["really_excited"]
        elif value >= 80:
            emoji = EMOJI_STATES["really_happy"]
        elif value >= 60:
            emoji = EMOJI_STATES["happy"]
        elif value >= 40:
            emoji = EMOJI_STATES["curious"]
        elif value >= 20:
            emoji = EMOJI_STATES["concerned"]
        elif value >= 10:
            emoji = EMOJI_STATES["sad"]
        else:
            emoji = EMOJI_STATES["very_sad"]

    if mood not in ("happy", "headpat", "shake"):
        emoji = EMOJI_STATES["curious"]

    return emoji, mood


def update_oled(oled, mood="default", value=50):
    """Update the OLED display with the current emoji and animation."""

    global _last_blink_time, _blinking

    now = ticks_ms()

    if mood not in ("shake", "headpat"):
        if ticks_diff(now, _last_blink_time) > BLINK_INTERVAL:
            _blinking = True
            _last_blink_time = now

        if _blinking and ticks_diff(now, _last_blink_time) > BLINK_DURATION:
            _blinking = False

    emoji, effective_mood = get_emoji(mood, value, now)

    if _blinking and effective_mood not in ("shake", "headpat"):
        emoji = _translate_emoji_blink(emoji)

    # Render emoji centrally on screen
    oled.fill(0)
    x = (128 - (8 * len(emoji))) // 2
    oled.text(emoji, x, 28, 1)
    oled.show()

