"""Entry point for the news-image-20261124 v2 broadsheet.

The front page is rendered ahead of time (see render.py) and stored in
this repository as entry.png. At grade time this script only moves
those bytes to the output directory the grader provides, using the
standard library alone: no network access, no extra packages, and the
same bytes on every run.

The grader expects /output/entry.png; local runs can point elsewhere
with MAKEFUN_OUTPUT_DIR.
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
IMAGE_NAME = "entry.png"


def entry_bytes() -> bytes:
    image_path = REPO_ROOT / IMAGE_NAME
    if not image_path.is_file():
        raise FileNotFoundError(
            "shipped front page is missing: %s" % image_path
        )
    return image_path.read_bytes()


def run() -> Path:
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME
    target.write_bytes(entry_bytes())
    return target


if __name__ == "__main__":
    written = run()
    print("wrote %s" % written)
