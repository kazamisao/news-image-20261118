"""Entry program for news-image-20261118 (stdlib only).

The picture itself sits next to this file as news.png: a one-page
broadsheet of the world news of Wednesday, 18 November 2026, drawn by
render.py (Pillow, run at build time) — the Kerch Bridge collapse as the
hero story, the Kyiv counter-strike, plus Bahrain, Trump in Manila,
Cyclone Akvan and Nvidia, with an "Also today" strip.

All this program does is deliver those bytes, untouched, to the output
path the harness expects. It runs with no network and writes the same
bytes on every run.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "news.png")
LIMIT = 1048576


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.png")


def main():
    # The gate rejects anything over 1 MiB, so fail loudly if the bundled
    # picture ever grows past the cap instead of writing a bad entry.
    if os.path.getsize(SOURCE) > LIMIT:
        raise SystemExit("news.png exceeds the 1 MiB entry limit")
    target = output_path()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(SOURCE, target)
    # The grader runs this twice and demands identical bytes: confirm the
    # copy landed whole — same hash, not just same size — before reporting
    # success.
    if sha256(target) != sha256(SOURCE):
        raise SystemExit("entry.png copy failed integrity check")


if __name__ == "__main__":
    main()
