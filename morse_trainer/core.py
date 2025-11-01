# morse_trainer/core.py
import os, json, random, string

SAVE = os.path.join(os.path.expanduser("~"), ".morse_stats.json")

MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
}

REV = {v: k for k, v in MORSE.items()}

WORDLIST = [
    "HELLO", "WORLD", "CODE", "PYTHON", "MORSE", "TRAINER", "NEON", "RADIO",
    "ROBOT", "DATA", "BEACON", "VECTOR", "LASER", "SOS", "ZEN", "ECHO",
]

def encode_text(text: str) -> str:
    out = []
    for word in text.upper().split():
        parts = [MORSE.get(c, "") for c in word if c in MORSE]
        out.append(" ".join(parts))
    return " / ".join(out)

def decode_morse(m: str) -> str:
    words = []
    for w in m.strip().split("/"):
        letters = [REV.get(token, "?") for token in w.strip().split()]
        words.append("".join(letters))
    return " ".join(words)

def load_stats():
    if not os.path.exists(SAVE):
        return {"sessions": 0, "correct": 0, "total": 0}
    try:
        return json.load(open(SAVE, "r", encoding="utf-8"))
    except Exception:
        return {"sessions": 0, "correct": 0, "total": 0}

def save_stats(stats):
    try:
        json.dump(stats, open(SAVE, "w", encoding="utf-8"), indent=2)
    except Exception:
        pass
