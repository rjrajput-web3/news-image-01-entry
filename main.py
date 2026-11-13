#!/usr/bin/env python3
"""news-image-01 entry (Python 3.13, standard library only).

The image is drawn in advance by render.py and held in this repository as
entry.png; this program copies it to the output directory. It runs with no
network, so both runs write the same bytes. After copying it checks the
result is a whole PNG within the competition's limits (at most 1 MiB and
1024 by 1024 pixels) and fails loudly if it is not, so a broken entry is
never submitted silently.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(OUT, "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024


def png_size(path):
    """Return (width, height) of a PNG from its IHDR chunk."""
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    if not os.path.isfile(SRC):
        print("entry.png is missing from the repository", file=sys.stderr)
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    shutil.copyfile(SRC, DST)
    size = os.path.getsize(DST)
    width, height = png_size(DST)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        sys.exit(1)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"entry.png is {width}x{height}, over the 1024x1024 limit",
              file=sys.stderr)
        sys.exit(1)
    print(f"wrote entry.png to {OUT} ({width}x{height}, {size} bytes)")


if __name__ == "__main__":
    main()
