# morse_trainer/__main__.py
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
