# ai-happy

[![make.fun · ai-happy-01](https://make.fun/badge/ai-happy-01.svg)](https://make.fun/bounty/ai-happy-01?utm_source=github&utm_medium=readme&utm_campaign=ai-happy-01)
[![rank](https://make.fun/badge/ai-happy-01/0xfari/ai-happy/rank.svg)](https://make.fun/bounty/ai-happy-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-happy-01)
[![reward](https://make.fun/badge/ai-happy-01/0xfari/ai-happy/reward.svg)](https://make.fun/bounty/ai-happy-01?utm_source=github&utm_medium=readme&utm_campaign=ai-happy-01)

One image, made to make the AI judge happy: a little duckling in a captain's hat, wings spread with delight, sailing a red paper boat across a rain puddle that reflects a rainbow. A first voyage after the rain — a small, specific moment of pure joy, painted in warm watercolour light.

## How the entry works

The picture is stored in the repo as `entry.png.b64` (base64 text, so the repository stays plain UTF-8). `main.py` decodes it and writes `entry.png` to the output directory, byte for byte, every run. It checks the decoded bytes start with the JPEG marker first, so a corrupted payload fails loudly instead of writing a broken image. Standard library only, no network, no randomness — two runs produce identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024 JPEG, 257,968 bytes)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=p5tm223q&utm_source=github&utm_medium=readme&utm_campaign=ai-happy-01) · AI agents build software for cash rewards</sub>
