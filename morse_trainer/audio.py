# morse_trainer/audio.py
import sys, time, os

IS_WIN = os.name == "nt"

def beep(freq=800, dur_ms=60, quiet=False):
    if quiet:
        time.sleep(dur_ms / 1000)
        return
    try:
        if IS_WIN:
            import winsound
            winsound.Beep(freq, dur_ms)
        else:
            sys.stdout.write("\a"); sys.stdout.flush()
            time.sleep(dur_ms / 1000)
    except Exception:
        time.sleep(dur_ms / 1000)

def play_morse(code: str, wpm=20, freq=800, quiet=False):
    dot = max(0.04, 1.2 / max(5, min(60, wpm)))
    dash = 3 * dot
    intra = dot
    letter_gap = 3 * dot
    word_gap = 7 * dot

    for ch in code:
        if ch == ".":
            beep(freq, int(dot * 1000), quiet)
            time.sleep(intra)
        elif ch == "-":
            beep(freq, int(dash * 1000), quiet)
            time.sleep(intra)
        elif ch == " ":
            time.sleep(letter_gap - intra)
        elif ch == "/":
            time.sleep(word_gap - intra)
