## Morse Trainer — Tutorial

This project is a small command-line Morse code trainer written in pure Python. It supports encoding/decoding, playing Morse beeps, interactive drills, a timed speed challenge, and simple persistent stats.

This tutorial explains how the project is organized, how the main pieces work, and how to build or extend it.

### Prerequisites

- Python 3.8+ (3.10/3.11 recommended)
- On Windows, no extra packages are required (the stdlib `winsound` is used for beeps). On other OSes, the program falls back to printing the ASCII bell and timing sleeps.

### Project layout

```
morse_trainer/
    __main__.py      # CLI entrypoint
    audio.py         # beep() and play_morse()
    commands.py      # CLI command handlers
    core.py          # encoding/decoding and stats persistence
    splash.py        # splash screen and quick-start guide
    tutorial.md      # this file
```

### How it works — the pieces

- `core.py` contains the Morse table (`MORSE` and `REV`), `encode_text()` and `decode_morse()` which convert between plain text and Morse. It also implements `load_stats()` and `save_stats()` that read/write a JSON file in the user's home directory.

- `audio.py` provides `beep()` (platform-aware) and `play_morse()` which interprets `.` (dot), `-` (dash), space (letter gap) and `/` (word gap) and uses timing derived from the WPM (words-per-minute) setting.

- `commands.py` implements the CLI subcommands used by `__main__.py`. These include `encode`, `decode`, `play`, `drill`, `speed`, and `stats`. The interactive commands use `input()` to read user answers and update saved stats.

- `splash.py` prints an ASCII title and a short tutorial, and is shown when the program is started with no args.

- `__main__.py` builds the `argparse` subcommand parser and dispatches to functions in `commands.py`.

### Running the app (Windows cmd.exe)

From the project root (or any location where the package is visible), run:

```bat
python -m morse_trainer
```

Examples:

```bat
python -m morse_trainer encode HELLO WORLD
python -m morse_trainer decode "... --- ... / .-- --- .-. .-.. -.."
python -m morse_trainer play "TEST MESSAGE" -w 18 -f 750
python -m morse_trainer drill -n 5
python -m morse_trainer speed -t 60
python -m morse_trainer stats
```

Notes:
- `-w/--wpm` sets words-per-minute (affects dot/dash timing).
- `-f/--freq` sets beep frequency (Windows only for `winsound`).
- `--quiet` disables audible beeps and runs the timing only (useful for testing or noisy environments).

### Implementation tips & extension ideas

- Encoding/decoding
  - `encode_text()` uppercases and maps A-Z and 0-9; unsupported characters are currently dropped. If you need punctuation, extend the `MORSE` map and adjust `encode_text()` to either warn on dropped chars or represent them explicitly.

- Audio
  - On Windows `winsound.Beep()` produces clean beeps. On POSIX systems the code writes `\a` (bell) and sleeps for timing. For improved audio on Linux/macOS consider using a small dependency (e.g., `simpleaudio` or `pyaudio`) and replacing `beep()` with waveform playback.

- Stats storage
  - Stats are persisted to `~/.morse_stats.json`. On Windows you might prefer storing them under `%APPDATA%`—you can change the `SAVE` constant in `core.py` to use `os.environ.get('APPDATA')` when `os.name == 'nt'`.

- Testing
  - Add unit tests for `encode_text()` and `decode_morse()` (happy path and unknown tokens). Use Python's `unittest` or `pytest`.
  - For `play_morse()` you can mock `time.sleep()` and `beep()` to assert timings and call counts instead of producing real sound.

- UX improvements
  - Consider adding a `--no-splash` flag to skip the splash when called with no args in automated runs.
  - Provide a config or wordlist file so users can add their own drill words.

### Example: Add a test for encode/decode (concept)

Create `tests/test_core.py` and assert basic round-trips and known encodings. Mock file I/O for `load_stats()`/`save_stats()` if needed.

### Packaging & distribution

- This is a small package; to install locally for development:

```bat
pip install -e .
```

Add a minimal `pyproject.toml` or `setup.cfg`/`setup.py` if you plan to publish.

### Troubleshooting

- No sound on Windows: ensure you're running on Windows and have the default Python distribution which includes `winsound`.
- ANSI colors not showing: older Windows consoles may not render ANSI escapes; try using Windows Terminal or enable VT processing.
- Stats not saved: check file permission errors or if `SAVE` points to a directory you can't write.



This tutorial should help you understand how the project is built and where to make changes.