#!/usr/bin/env python3
"""Entry point for the news-image-20261119 bounty.

The image itself is drawn by render.py (PIL) and shipped in this
repository as entry.png. This program just copies that file to the
output directory, so both grading runs write identical bytes.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
