# The World Today — 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/sanschiko3-dotcom/news-image-20261124-v2/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/sanschiko3-dotcom/news-image-20261124-v2/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the [make.fun bounty "Sum up 24 November's world news in one image"](https://make.fun/bounty/news-image-20261124).

## What it is

A broadsheet front page, **"THE WORLD TODAY — Tuesday, 24 November 2026"**,
drawn with Pillow at build time (`render.py`) and shipped as `entry.png`.
The entry program `main.py` (Python 3.13, standard library only) copies
that image to `/output/entry.png` — no network, fully deterministic.

One dominant lead with a full fact deck, six secondary stories with fact
bodies, one full-width story, and an Also Today strip — 14 stories in all:

1. **LEAD — WAR AT SEA** — Ukraine says seven naval drones sank the
   Russian corvette Merkury at Benghazi, Libya; a Ka-27 helicopter aboard
   was destroyed and the cargo ship MV Angara was hit.
2. **CLIMATE** — COP31 collapses in Antalya: 90+ nations reject a draft
   with no "fossil fuels" after nearly 50 hours of overtime.
3. **SECURITY** — NATO counts 25 airspace violations in 2026; debris from
   a 20 Nov incident found in Poland.
4. **MIDDLE EAST** — US Treasury sanctions Iran; Qatar mediates talks.
5. **JUSTICE** — 14 states back the Rohingya genocide case against Myanmar
   at the ICJ.
6. **MARKETS** — Jensen Huang returns as Nvidia CEO; Nasdaq +6.51%.
7. **DISASTER** — Nepal shaken by a magnitude 5.6 earthquake.
8. **TECH UNDER FIRE** — Oregon and Virginia sue SpaceX over Grok abuse
   images.

Plus Also Today: the Sparta II ablaze in the Baltic, the Trump–Putin–Xi
summit, measles in Pennsylvania, a car bomb in Villavicencio, Tripoli's
reaction, and COP31 called climate diplomacy's "darkest moment".

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, under 1 MiB, byte-identical on every run
```

## License

MIT — see [LICENSE](LICENSE).
