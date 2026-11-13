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


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Read width/height from the JPEG's Start-of-Frame segment.

    Walks the marker segments after SOI until a SOF0/SOF2 marker is
    found; its payload carries precision (1 byte) then height and
    width (2 bytes each, big-endian). Raises ValueError if no SOF
    segment is found, so a truncated payload fails loudly.
    """
    pos = 2  # past the SOI marker
    while pos + 9 <= len(data):
        if data[pos] != 0xFF:
            raise ValueError("corrupt JPEG marker stream")
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        size = int.from_bytes(data[pos + 2:pos + 4], "big")
        if marker in (0xC0, 0xC2):  # SOF0 / SOF2
            height = int.from_bytes(data[pos + 5:pos + 7], "big")
            width = int.from_bytes(data[pos + 7:pos + 9], "big")
            return width, height
        pos += 2 + size
    raise ValueError("no JPEG Start-of-Frame segment found")


def load_image_bytes() -> bytes:
    """Decode the stored artwork and sanity-check it is a JPEG."""
    source = Path(__file__).resolve().parent / SOURCE_NAME
    text = source.read_text(encoding="ascii").strip()
    data = base64.b64decode(text, validate=True)
    if not data.startswith(JPEG_SOI):
        raise ValueError("decoded payload is not a JPEG (bad SOI marker)")
    width, height = jpeg_dimensions(data)
    if width > 1024 or height > 1024:
        raise ValueError(f"image is {width}x{height}, over the 1024x1024 limit")
    print(f"decoded JPEG {width}x{height} ({len(data)} bytes)")
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
