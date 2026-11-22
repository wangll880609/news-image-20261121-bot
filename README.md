[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/wangll880609/news-image-20261121-bot/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/wangll880609/news-image-20261121-bot/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The Daily Front Page — Saturday 21 November 2026

Entry for the make.fun competition **news-image-20261121**: sum up the
world's news of Saturday 21 November 2026 in one image.

## What it does

`main.py` (Python 3.13, standard library only, no network, fully
deterministic) draws a newspaper front page — 1024x1024 PNG — with 43
verified stories from 21 November 2026: a lead on Iran striking US bases
in Bahrain, plus World, Markets, Science and Sport sections, each story a
headline and a one-line summary.

## Run

```sh
mkdir -p /tmp/out
OUTPUT_DIR=/tmp/out python3 main.py
# writes /tmp/out/entry.png
```

Run it twice and the two files are byte-identical.

## Sources

One Turn day digest for 21 November 2026 (106 stories; BBC, Reuters,
Guardian, France 24, Al Jazeera, CBS, NPR, UPI and others) and the Majik
Morning Brief for the same day. Every headline and figure on the page was
checked against reports published on 21 November 2026.

## License

MIT — see LICENSE.
