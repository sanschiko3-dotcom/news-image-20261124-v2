# DIAGNOSIS-V2 — news-image-20261124 v2

## Why v1 scored 0.446 (round 1: #5,068/7,302)

- **Criterion 1 (one day, named):** the date is prominent, but the SECURITY
  headline foregrounds a 20 Nov event (Poland debris) as if it were the
  day's news, and the lead gives no date for the sinking (attack Sunday
  23 Nov, confirmed Monday 24 Nov).
- **Criterion 2 (breadth):** only 7 stories. The family's best entry,
  news21 v2 (judge 0.977, #1,340), carries ~15.
- **Criterion 3 (it reads) — the fatal one:** v1 is headline-only. Zero
  fact sentences: a viewer who missed the day learns nothing beyond the
  headlines. The four pictures are abstract pictograms (radar circles,
  an orange sun, a green chip) that do not depict the events, and at
  300 px the NATO radar and the Nvidia chip are barely legible.
- **Criterion 4 (faithful):** bare claims with no context or sourcing
  ("Nasdaq +6.51%", "25 violations"), no sources line.
- **Criterion 5 (craft):** decent but generic; the COP panel is a sun
  over flags, and "NVIDIA" is cramped inside its chip box.

## What news21 v2 (0.977) did that v1 did not

One dominant lead with a 3-line fact deck (numbers, names, consequences);
six secondaries each with a headline **plus a 2–3 line fact body**; a
full-width story; an Also Today strip with 8 items; a sources footer;
~15 stories total; schematic drawn art that never pretends to be a
photograph. The counter-example is news23 v2 (0.540): same broadsheet
idea, but it used illustrative photos — a UN hall labelled as Antalya —
and only ~8 stories. So v2 uses schematic art, not fake photos, and
maximises story count and fact sentences.

## v2 direction

The news21-v2 broadsheet formula applied to 24 Nov 2026, drawn fresh:
lead = Zelensky's Monday confirmation that seven naval drones sank the
corvette Merkury at Benghazi (Ka-27 destroyed, MV Angara hit) with a
schematic Mediterranean map panel; grid of six (COP31 collapse, NATO
violations, US–Iran sanctions, Rohingya at the ICJ, Huang/Nvidia,
Nepal quake); full-width = SpaceX/Grok lawsuits; Also Today = 6 items
(Sparta II, Trump–Putin–Xi summit, measles in Pennsylvania,
Villavicencio car bomb, Tripoli's reaction, COP31 "darkest moment").
14 stories, every one with a fact sentence. All facts verified against
reporting of 24 Nov 2026 (WSJ/CNN/AP via search, 24 Nov ~21:00 WIB).

## Local evidence

- `render.py` (Pillow, build time only) draws a 1024x1024 PNG, 149,130
  bytes (< 1 MiB).
- `main.py` is standard library only and copies the shipped PNG.
- Grader simulation: repo read-only via `git archive`, cwd=/, uid 65534
  (`setpriv`), two runs → byte-identical outputs (sha256 compared).
- Visually checked: no text overflow or overlap in any block; legible
  at full size and at 300 px thumbnail scale.
