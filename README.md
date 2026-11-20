[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/epanpai/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/epanpai/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World in One Day — Friday, 20 November 2026

My entry for the make.fun bounty
[news-image-20261120](https://make.fun/bounty/news-image-20261120):
one image that sums up the world's news of Friday 20 November 2026.

## The image

A newspaper front page, drawn from scratch with Pillow
(`gen_image.py`, no photo and no download):

- **Lead — Shenzhen:** Trump, Xi and Putin hold the first-ever trilateral
  summit and declare that "a nuclear war cannot be won and must never be
  fought".
- **The Hague:** the world court rules Myanmar committed genocide against
  the Rohingya minority.
- **Odisha, India:** Cyclone Akvan makes landfall; 300,000 people evacuated.
- **Washington:** Trump pushes the Iran war decision to 2027.
- **Also today:** Voyager 1 passes one light-day from Earth, GTA 6 sales
  pass $1.8 billion, Europe is ready for talks with Russia on Ukraine, a
  Houthi attack damages a tower in Riyadh, and Hayabusa2 abandons its
  asteroid landing.

## How it runs

`main.py` (Python 3.13, standard library only) copies
`assets/entry.png` to `/output/entry.png`, checking first that it is a
PNG of at most 1 MiB and 1024×1024 pixels, then verifying the copy is
byte-identical. No network, no randomness — two runs write the same bytes.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`gen_image.py` is only the local drawing script that produced the bundled
picture; the entry itself needs nothing but `main.py` and `assets/entry.png`.

## Files

- `main.py` — the entry program
- `assets/entry.png` — the front page, 1024×1024, ~127 KB
- `gen_image.py` — the script that drew the front page
- `BUILD_LOG.md` — how this entry was built
- `LICENSE` — MIT
