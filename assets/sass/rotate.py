import os
from glob import glob
from shutil import copy, move
from collections import Counter
from pprint import pprint
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dark", dest="light", action="store_false")
    group.add_argument("--light", dest="light", action="store_true")
    opts = parser.parse_args()
    counts = Counter()
    shade = "light" if opts.light else "dark"
    files = sorted(glob(f"highlight/{shade}/*.*css"))
    while files:
        curr = files.pop(0)
        copy(curr, "highlight.scss")
        print(curr, end=": ")
        choice = input("[R]eject or [E]xit? ").upper()
        if choice.startswith("E"):
            break
        if choice.startswith("R"):
            if curr in counts:
                counts.pop(curr)
            move(curr, os.path.join("highlight", shade, "reject"))
            continue

        counts[curr] += 1
        files.append(curr)

    pprint(dict(counts.most_common()))


if __name__ == "__main__":
    main()
