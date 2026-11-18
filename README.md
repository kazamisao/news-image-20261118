# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/kazamisao/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/kazamisao/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page broadsheet of the world news of Wednesday, 18 November 2026, drawn in code with Pillow: the Kerch Bridge collapse as the hero story, the Russian counter-strike on Kyiv's Dnipro bridges, plus Iranian drones over Bahrain, Trump landing in Manila, Cyclone Akvan, and Nvidia's Jensen Huang open to returning — with an "Also today" strip on UK sanctions, Canada–China trade, Dhoni's IPL retirement, and the Hormuz tanker attack. `render.py` draws the image at 3x and downscales it to `news.png`; `main.py` (stdlib only) copies it to the output path, byte-identical on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Tests

```sh
python3 test_entry.py
```

The suite checks the gate rules: `news.png` is a valid PNG of 1024x1024 and under 1 MiB, and two runs of `main.py` write byte-identical files.

---

<sub>Entered on [make.fun](https://make.fun/?ref=p5dwa49p&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
