import os
from glob import glob
from shutil import copy

def main():
    files = sorted(glob(f"highlight/*.*css"))
    while files:
        curr = files.pop(0)
        copy(curr, "highlight.scss")
        print(curr, end=": ")
        choice = input("[S]ight or [D]ark? ").upper()
        if choice.startswith("S"):
            copy(curr, os.path.join("highlight", "light"))
            continue
        if choice.startswith("D"):
            copy(curr, os.path.join("highlight", "dark"))
            continue
        files.append(curr)


if __name__ == "__main__":
    main()
