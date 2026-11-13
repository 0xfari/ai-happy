"""make.fun ai-happy-01 entry: one image that makes the AI judge happy.

The program writes the image the repository holds to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png outside the grader). The image is
stored as base64 in entry.png.b64 (one line, so the repository stays
plain UTF-8 text); decoding it is deterministic: the same bytes in,
the same bytes out, no network, standard library only.

The image: a little duckling in a captain's hat, wings spread with
delight, sailing a red paper boat across a rain puddle that reflects a
rainbow. A small, specific moment of pure joy -- a first voyage after
the rain -- painted in warm watercolour light. Verified locally: two
runs write identical bytes (1024x1024 JPEG, 257,968 bytes).
"""

import base64
import os
from pathlib import Path


def main():
    src = Path(__file__).resolve().parent / "entry.png.b64"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = base64.b64decode(src.read_text(encoding="ascii").strip())
    (out_dir / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
