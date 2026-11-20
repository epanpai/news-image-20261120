#!/usr/bin/env python3
"""Entry for make.fun news-image-20261120.

Copies the finished front page for Friday 20 November 2026 into the
grader's output folder. The picture lives in this repository, the program
only moves it, so the run needs no network and always writes the same
bytes: run it twice and the two files are identical.

Usage:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
from __future__ import annotations

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

ARTWORK = Path(__file__).resolve().parent / "assets" / "entry.png"
LIMIT_BYTES = 1_048_576
LIMIT_SIDE = 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def die(msg: str) -> None:
    print(f"main.py: {msg}", file=sys.stderr)
    raise SystemExit(1)


def check_png(blob: bytes) -> tuple[int, int]:
    """Confirm the blob is a PNG within the size limits; return its size."""
    if len(blob) > LIMIT_BYTES:
        die(f"artwork is {len(blob)} bytes, over the 1 MiB limit")
    if blob[:8] != PNG_SIG:
        die("artwork does not start with the PNG signature")
    if len(blob) < 24 or blob[12:16] != b"IHDR":
        die("artwork has no PNG IHDR chunk")
    width, height = struct.unpack(">II", blob[16:24])
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        die(f"artwork is {width}x{height}, over the 1024x1024 limit")
    return width, height


def main() -> int:
    blob = ARTWORK.read_bytes()
    width, height = check_png(blob)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    with ARTWORK.open("rb") as src, target.open("wb") as dst:
        shutil.copyfileobj(src, dst)
    written = target.read_bytes()
    if written != blob:
        die("copy differs from the artwork in the repository")

    digest = hashlib.sha256(written).hexdigest()
    print(f"entry.png: {width}x{height}, {len(written)} bytes, sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
