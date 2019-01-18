#!/usr/bin/env python3
"""
Generates [style].scss files for Chroma styles available in Hugo.
"""
from argparse import ArgumentParser, SUPPRESS
from pathlib import Path
from shutil import which
from subprocess import run
from sys import exit, stderr

STYLES = [
    "abap", "algol", "algol_nu", "api", "arduino", "autumn", "borland", "bw",
    "colorful", "dracula", "emacs", "friendly", "fruity", "github", "igor",
    "lovelace", "manni", "monokai", "monokailight", "murphy", "native",
    "paraiso-dark", "paraiso-light", "pastie", "perldoc", "pygments",
    "rainbow_dash", "rrt", "solarized-dark", "solarized-dark256",
    "solarized-light", "swapoff", "tango", "trac", "vim", "vs", "xcode"
]

DESC = f"{__doc__} Available styles are: {', '.join(STYLES[:-1])} and {STYLES[-1]}."


def main():
    parser = ArgumentParser(description=DESC)
    parser.add_argument(
        "-s", "--styles",
        nargs="*",
        choices=STYLES,
        help="space seperated styles to include",
        metavar="STYLE")
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="overwrite existing styles",
    )
    opts = parser.parse_args()
    opts.styles = opts.styles or STYLES
    
    cmd = which("hugo")
    if not cmd:
        print("fatal error: no Hugo install found", file=stderr)
        exit(1)

    highlight = "../assets/sass/highlight"
    directory = Path(__file__).parent.resolve().joinpath(highlight).resolve()
    if not directory.is_dir():
        print(f"fatal error: {highlight} is not a directory", file=stderr)
        exit(2)
    
    for style in opts.styles:
        dst = directory.joinpath(f"{style}.scss")
        if dst.exists() and not opts.force:
            print(f"skipping {dst.name}: use --force to overwrite", file=stderr)
            continue
        ps = run([cmd, "gen", "chromastyles", f"--style={style}"], capture_output=True)
        ps.check_returncode()
        dst.write_bytes(ps.stdout)
        print(dst)
    

if __name__ == "__main__":
    main()
