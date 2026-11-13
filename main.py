#!/usr/bin/env python3
"""ai-happy-01 entry: an image that makes the AI judge happy.

What this program does is deliberately tiny. The artwork lives in this
repository as a base64 text file (``entry.png.b64``) so the whole entry
stays plain UTF-8. At run time the program decodes that file and writes
the image out to ``entry.png`` inside the output directory the grader
points at (``$MAKEFUN_OUTPUT_DIR``, falling back to ``/output``).

There is no network access, no randomness, and no dependency beyond the
standard library, so two runs of this program always produce exactly the
same bytes. Before writing, the decoded data is checked for the JPEG
start-of-image marker, so a corrupted payload fails loudly instead of
silently producing a broken file.

The picture itself: a small duckling wearing a captain's hat, wings
spread wide with delight, sailing a red paper boat over a rain puddle
that catches a rainbow. A first voyage after the rain — a small,
specific moment of pure joy, painted in warm watercolour light.
"""

import base64
import os
import sys
from pathlib import Path

SOURCE_NAME = "entry.png.b64"
OUTPUT_NAME = "entry.png"
# JPEG files begin with the SOI marker FF D8 FF.
JPEG_SOI = b"\xff\xd8\xff"


def output_directory() -> Path:
    """Where the grader wants the image (env var, else /output)."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def load_image_bytes() -> bytes:
    """Decode the stored artwork and sanity-check it is a JPEG."""
    source = Path(__file__).resolve().parent / SOURCE_NAME
    text = source.read_text(encoding="ascii").strip()
    data = base64.b64decode(text, validate=True)
    if not data.startswith(JPEG_SOI):
        raise ValueError("decoded payload is not a JPEG (bad SOI marker)")
    return data


def write_entry(data: bytes) -> Path:
    """Write the image and report where it went and how big it is."""
    out_dir = output_directory()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    target.write_bytes(data)
    print(f"wrote {target} ({len(data)} bytes)")
    return target


def main() -> int:
    write_entry(load_image_bytes())
    return 0


if __name__ == "__main__":
    sys.exit(main())
