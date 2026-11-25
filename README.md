# The World in One Day — 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/hailaobao2026/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/hailaobao2026/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A newspaper front page summing up the world's news of Tuesday 24
November 2026, drawn from scratch by `main.py` — pure Python 3.13
standard library, no network, no fonts, no image libraries.

## The day's news

- **Nvidia** — a day after his reinstatement as CEO, Jensen Huang tells
  staff he made "terrible mistakes" and is in therapy, as the comeback
  rally fades.
- **Gaza** — an Israeli strike kills Hamas security chief Naeem Abu Nahal
  and six others, despite the ceasefire.
- **Ukraine** — a Russian overnight attack on a Zaporizhzhia apartment
  block kills 2 and wounds 40, four of them children.
- **Britain** — two men held after a break-in at Prince William's Norfolk
  home, Anmer Hall.
- **Saudi Arabia** — the Riyadh PIF tower hit twice in a week; Saudi
  Arabia condemns a "terrorist attack".
- **Russia** — hacked data suggests nearly 500,000 Russian soldiers dead.
- Also today: Trump gives Giuliani the Medal of Freedom; NATO answers
  reports of a nuclear-armed satellite; the landmine toll hits a 5-year
  high of 7,000; Seoul offers $375,000 to catch AI exam cheats.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024x1024, PNG). Two runs write byte-identical
output. Tested grader-style: read-only repo, run as uid 65534 into an
empty output directory owned by someone else — exits 0.
