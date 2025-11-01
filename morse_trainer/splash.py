# morse_trainer/splash.py
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

