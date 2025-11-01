# Building Morse Trainer — A Step-by-Step Developer Guide

This document teaches you how to build the `morse_trainer` project from scratch. It is a developer-focused, step-by-step ebook that explains each design choice and shows the exact code you can add at each step.

Audience
- Developers who want to learn how to build a small CLI tool in Python that: encodes/decodes Morse, plays beeps, supports interactive drills, and persists simple stats.

Goals
- Walk through creating the package and source files.
- Explain the timing and audio logic for Morse playback.
- Show how to wire a user-friendly CLI with `argparse`.
- Add basic persistence and tests suggestions.

Prerequisites
- Python 3.8+ installed.
- Basic knowledge of Python programming.

Folder layout we will create

```
morse_trainer/
    __main__.py
    audio.py
    commands.py
    core.py
    splash.py
```

If you prefer to work inside a package directory, create `morse_trainer` as a folder and add the files below.

Step 0 — create the project folder

On Windows (cmd.exe) create the folder and open your editor:

```bat
mkdir morse_trainer
cd morse_trainer
rem create files using your editor or copy/paste the snippets in this ebook
```

Step 1 — core.py (encoding, decoding, and stats)

Create `core.py`. This module holds the Morse mapping, encoding/decoding helpers, a small test word list, and simple JSON-backed stats.

Add this content to `core.py`:

```python
import os, json

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
```

Explanation & design choices
- `MORSE` maps letters and digits to the dot/dash representation.
- `encode_text()` converts input text into groups of Morse tokens per letter, joins letters with spaces and words with ` / ` (slash) which is a common ASCII separator for words in linear morse text.
- `decode_morse()` reverses that mapping; unknown tokens become `?`.
- `load_stats()` and `save_stats()` use a simple JSON file in the user's home directory. This keeps the project dependency-free.

Step 2 — audio.py (playback)

Create `audio.py`. This module implements `beep()` (platform-aware) and `play_morse()` which interprets the code produced by `encode_text()`.

Add this content to `audio.py`:

```python
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
```

Explanation & notes
- WPM (words-per-minute) timing: the code uses an approximation where `dot = 1.2 / wpm` clamped to reasonable values, and a dash is 3× dot. These timings give a natural-sounding rhythm at different speeds.
- On Windows the code uses `winsound.Beep()`; on other OSes it emits the terminal bell `\a` as a fallback. For a more robust cross-platform audio, replace `beep()` with waveform playback (e.g., `simpleaudio` or `pydub`).

Step 3 — commands.py (CLI command handlers)

Create `commands.py`. This file contains functions that implement the behavior for each subcommand. It imports helpers from `core.py` and `audio.py`.

```python
import time, random
from .core import encode_text, decode_morse, WORDLIST, load_stats, save_stats
from .audio import play_morse

def cmd_encode(args):
    text = " ".join(args.text)
    print(encode_text(text))

def cmd_decode(args):
    code = " ".join(args.code)
    print(decode_morse(code))

def cmd_play(args):
    code = encode_text(" ".join(args.text))
    if not args.quiet:
        print(code)
    play_morse(code, wpm=args.wpm, freq=args.freq, quiet=args.quiet)

def cmd_drill(args):
    stats = load_stats()
    pool = WORDLIST[:]
    correct = 0
    for i in range(args.rounds):
        w = random.choice(pool)
        print(f"[{i+1}/{args.rounds}] listen")
        play_morse(encode_text(w), wpm=args.wpm, freq=args.freq, quiet=args.quiet)
        guess = input("> ").strip().upper()
        if guess == w:
            print("ok")
            correct += 1
        else:
            print(f"ans: {w}")
    stats["sessions"] += 1
    stats["correct"] += correct
    stats["total"] += args.rounds
    save_stats(stats)
    print(f"score: {correct}/{args.rounds}")

def cmd_speed(args):
    stats = load_stats()
    hits, tries = 0, 0
    t_end = time.time() + args.time
    while time.time() < t_end:
        w = random.choice(WORDLIST)
        play_morse(encode_text(w), wpm=args.wpm, freq=args.freq, quiet=args.quiet)
        guess = input("> ").strip().upper()
        tries += 1
        if guess == w:
            hits += 1
        print(f"ans: {w}")
    stats["sessions"] += 1
    stats["correct"] += hits
    stats["total"] += tries
    save_stats(stats)
    acc = (hits / tries * 100) if tries else 0
    print(f"done: hits={hits}, tries={tries}, acc={acc:.1f}%")

def cmd_stats(args):
    s = load_stats()
    print(f"sessions: {s['sessions']}")
    print(f"correct : {s['correct']}")
    print(f"total   : {s['total']}")
    acc = (s['correct']/s['total']*100) if s['total'] else 0
    print(f"accuracy: {acc:.1f}%")
```

Design notes
- `cmd_drill` and `cmd_speed` are interactive: they call `input()` and update the stats file.
- `play_morse()` is passed a `quiet` flag so tests or noisy environments can disable beeps.

Step 4 — splash.py (splash & quick start)

Create `splash.py`. This module prints an ASCII title and a short quick start guide when the program is run without arguments.

```python
import shutil, sys, os, time

RESET  = "\033[0m"
ORANGE = "\033[38;5;208m"
GREY   = "\033[38;5;244m"
CYAN   = "\033[38;5;51m"
BOLD   = "\033[1m"

TITLE = r"""
███╗   ███╗ ██████╗ ██████╗ ███████╗███████╗    ████████╗██████╗  █████╗ ██╗███╗   ██╗███████╗██████╗ 
████╗ ████║██╔═══██╗██╔══██╗██╔════╝██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██║████╗  ██║██╔════╝██╔══██╗
██╔████╔██║██║   ██║██████╔╝███████╗█████╗         ██║   ██████╔╝███████║██║██╔██╗ ██║█████╗  ██████╔╝
██║╚██╔╝██║██║   ██║██╔══██╗╚════██║██╔══╝         ██║   ██╔══██╗██╔══██║██║██║╚██╗██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║╚██████╔╝██║  ██║███████║███████╗       ██║   ██║  ██║██║  ██║██║██║ ╚████║███████╗██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
"""

TUTORIAL = f"""{GREY}{BOLD}
# Run the app (with splash screen)
python -m morse_trainer{GREY}

# Encode text
{RESET}python -m morse_trainer encode HELLO WORLD{GREY}

# Decode Morse
{RESET}python -m morse_trainer decode "... --- ... / .-- --- .-. .-.. -.."{GREY}

# Play sound
{RESET}python -m morse_trainer play "CQ CQ DE TEST" -w 18 -f 750{GREY}

# Drill & speed test
{RESET}python -m morse_trainer drill -n 5
python -m morse_trainer speed -t 60{RESET}
"""

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_splash():
    clear()
    cols = shutil.get_terminal_size((100, 30)).columns
    print()
    for line in TITLE.splitlines():
        print(ORANGE + line.center(cols) + RESET)
    print()
    print((GREY + "MORSE TRAINER research preview" + RESET).center(cols))
    print()
    print((CYAN + "NOTHING YET..." + RESET).center(cols))
    print()
    print(GREY + "Press Enter to Read Guide..." + RESET)
    input()
    print(ORANGE + BOLD + "Quick Start Guide".center(cols) + RESET)
    print("-" * cols)
    print(TUTORIAL)
    print(GREY + "Press Enter to start the program..." + RESET)
```

Step 5 — __main__.py (CLI wiring)

Create `__main__.py`. This file declares the command line interface using `argparse` and dispatches to functions defined in `commands.py`.

```python
import argparse, sys
from .commands import (
    cmd_encode, cmd_decode, cmd_play, cmd_drill, cmd_speed, cmd_stats
)
from .splash import show_splash

def build_parser():
    p = argparse.ArgumentParser(
        prog="morse_trainer",
        description="Morse Trainer CLI — retro terminal edition",
        add_help=True
    )
    sub = p.add_subparsers(dest="cmd")

    e = sub.add_parser("encode", help="text → morse")
    e.add_argument("text", nargs=argparse.REMAINDER)
    e.set_defaults(func=cmd_encode)

    d = sub.add_parser("decode", help="morse → text")
    d.add_argument("code", nargs=argparse.REMAINDER)
    d.set_defaults(func=cmd_decode)

    pl = sub.add_parser("play", help="play morse beeps")
    pl.add_argument("text", nargs=argparse.REMAINDER)
    pl.add_argument("-w","--wpm", type=int, default=20)
    pl.add_argument("-f","--freq", type=int, default=800)
    pl.add_argument("--quiet", action="store_true")
    pl.set_defaults(func=cmd_play)

    dr = sub.add_parser("drill", help="listen & type rounds")
    dr.add_argument("-w","--wpm", type=int, default=18)
    dr.add_argument("-f","--freq", type=int, default=800)
    dr.add_argument("-n","--rounds", type=int, default=5)
    dr.add_argument("--quiet", action="store_true")
    dr.set_defaults(func=cmd_drill)

    sp = sub.add_parser("speed", help="60s challenge")
    sp.add_argument("-w","--wpm", type=int, default=20)
    sp.add_argument("-f","--freq", type=int, default=800)
    sp.add_argument("-t","--time", type=int, default=60)
    sp.add_argument("--quiet", action="store_true")
    sp.set_defaults(func=cmd_speed)

    st = sub.add_parser("stats", help="show stats")
    st.set_defaults(func=cmd_stats)

    return p

def main():
    parser = build_parser()
    # No arguments → show splash + tutorial, then help
    if len(sys.argv) == 1:
        show_splash()
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
    except KeyboardInterrupt:
        print("\n^C")

if __name__ == "__main__":
    main()
```

Step 6 — run and test manually

Run the program from the directory containing the `morse_trainer` folder using the module mode:

```bat
python -m morse_trainer encode HELLO WORLD
python -m morse_trainer decode "... --- ..."
python -m morse_trainer play "TEST" -w 18 -f 750
```

Step 7 — tests (suggested)

Create a `tests/` directory at the project root and add a `test_core.py` to assert correctness of `encode_text()` and `decode_morse()`.

Example using `unittest` (save as `tests/test_core.py`):

```python
import unittest
from morse_trainer.core import encode_text, decode_morse

class TestCore(unittest.TestCase):
    def test_encode_simple(self):
        self.assertEqual(encode_text("SOS"), "... --- ...")

    def test_encode_words(self):
        self.assertEqual(encode_text("HI YOU"), ".... .. / -.-- --- ..-")

    def test_decode_unknown(self):
        self.assertIn("?", decode_morse("... .-.- ..."))

if __name__ == '__main__':
    unittest.main()
```

Run tests with:

```bat
python -m unittest discover
```

Step 8 — refinements & enhancements (ideas)

- Make the stats file location configurable and Windows-friendly. Example change in `core.py`:

```python
if os.name == 'nt':
    SAVE = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'morse_stats.json')
else:
    SAVE = os.path.join(os.path.expanduser('~'), '.morse_stats.json')
```

- Replace the ASCII bell in `audio.beep()` with a small waveform using `simpleaudio` for consistent cross-platform playback.
- Add a `--no-splash` flag to `__main__.py` or an environment variable to skip the interactive splash for automated runs.
- Allow loading a user wordlist from a JSON or text file so drills can be customized.

Exercises (build tasks)

1. Add punctuation support to the `MORSE` mapping and ensure `encode_text()` emits symbols for punctuation.
2. Implement a `--file` option for `play` that reads lines from a text file and plays them sequentially.
3. Add a `--reset-stats` command that zeroes the stats file after a confirmation prompt.

Appendix: how the timing works

- The Morse timing model used here derives a dot length from WPM using a simple formula: `dot = 1.2 / wpm`. This is based on the PARIS word standard for Morse timing and is a practical approximation for this small trainer.

Wrapping up

This guide gave you a reproducible path to build and extend the `morse_trainer` project. If you want, I can now:

- Add the `ebook.md` file into your repository (done).
- Create `tests/` and add the example unit tests and run them.
- Implement one of the enhancements listed above (stats path, audio backend, or config for wordlist).

Tell me which follow-up you prefer and I will implement it next.
