#!/usr/bin/env python3
"""Entrypoint: render the front page, then place it in the output folder."""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_image


def main():
    build_image.main()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
