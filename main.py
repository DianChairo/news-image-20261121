#!/usr/bin/env python3
"""Copy the pre-rendered entry.png into the output directory.

The image is already committed in this repository; this program only
copies it to the grader's output directory. It never writes into the
repository directory, never re-renders anything, and needs no network.
"""

import argparse
import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy entry.png to the output directory."
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output directory (overrides MAKEFUN_OUTPUT_DIR).",
    )
    args = parser.parse_args()

    out_dir = args.out or os.environ.get("MAKEFUN_OUTPUT_DIR") or "./output"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, SOURCE_NAME)

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, SOURCE_NAME)
    shutil.copyfile(source, dest)

    # The grader reads exactly the bytes in the output file, so confirm
    # the copy is complete before reporting success.
    expected = os.path.getsize(source)
    actual = os.path.getsize(dest)
    if actual != expected:
        print(
            f"error: incomplete copy: {dest} is {actual} bytes, "
            f"expected {expected} bytes from {source}",
            file=sys.stderr,
        )
        return 1

    print(f"copied {source} -> {dest} ({actual} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
