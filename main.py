#!/usr/bin/env python3
"""Copy entry.png into the output directory.

Usage: python3 main.py [--out DIR]
Defaults to ./output, or $MAKEFUN_OUTPUT_DIR when set.
"""

import argparse
import os
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Copy entry.png to the output directory.")
    parser.add_argument(
        "--out",
        default=os.environ.get("MAKEFUN_OUTPUT_DIR", "output"),
        help="output directory (default: ./output)")
    args = parser.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print(f"error: {src} not found", file=sys.stderr)
        return 1

    os.makedirs(args.out, exist_ok=True)
    dst = os.path.join(args.out, "entry.png")
    shutil.copyfile(src, dst)
    # Validate the copy: must be a PNG of the expected 1024x1024 size.
    with open(dst, "rb") as fh:
        header = fh.read(8)
    if header != b"\x89PNG\r\n\x1a\n":
        print(f"error: {dst} is not a PNG", file=sys.stderr)
        return 1
    if os.path.getsize(dst) != os.path.getsize(src):
        print(f"error: {dst} size mismatch after copy", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
