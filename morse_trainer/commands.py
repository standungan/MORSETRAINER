# morse_trainer/commands.py
import time, random, string
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
