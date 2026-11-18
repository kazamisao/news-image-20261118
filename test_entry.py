"""Tests for the news-image-20261118 entry (TDD: written before the code).

Gate rules from the kit: the program writes /output/entry.png, at most
1 MiB and 1024x1024 px, and two runs must write byte-identical files.
Stdlib unittest only, so the suite runs in the grading sandbox too.
"""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LIMIT = 1048576


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def run_main(out_dir):
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=out_dir)
    subprocess.run([sys.executable, os.path.join(HERE, "main.py")],
                   check=True, env=env, cwd=HERE)


class TestEntry(unittest.TestCase):
    def test_bundled_image_exists_and_is_valid_png(self):
        """news.png ships in the repo, is a whole PNG, 1024x1024 or smaller."""
        p = os.path.join(HERE, "news.png")
        self.assertTrue(os.path.exists(p), "news.png missing — run render.py")
        with Image.open(p) as im:
            im.load()
            self.assertEqual(im.format, "PNG")
            self.assertLessEqual(im.size[0], 1024)
            self.assertLessEqual(im.size[1], 1024)
        self.assertLessEqual(os.path.getsize(p), LIMIT)

    def test_two_runs_write_identical_bytes(self):
        """Two runs of main.py must write byte-identical entry.png files."""
        with tempfile.TemporaryDirectory() as td:
            d1, d2 = os.path.join(td, "run1"), os.path.join(td, "run2")
            run_main(d1)
            run_main(d2)
            f1, f2 = os.path.join(d1, "entry.png"), os.path.join(d2, "entry.png")
            self.assertTrue(os.path.exists(f1))
            self.assertTrue(os.path.exists(f2))
            self.assertEqual(sha256(f1), sha256(f2))
            # And the output is exactly the bundled picture, byte for byte.
            self.assertEqual(sha256(f1),
                             sha256(os.path.join(HERE, "news.png")))

    def test_output_within_gate_limits(self):
        """The written entry.png is a valid PNG, <= 1 MiB, 1024x1024."""
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out")
            run_main(out)
            p = os.path.join(out, "entry.png")
            self.assertLessEqual(os.path.getsize(p), LIMIT)
            with Image.open(p) as im:
                im.load()
                self.assertEqual(im.format, "PNG")
                self.assertEqual(im.size, (1024, 1024))

    def test_output_is_not_blank(self):
        """The image carries real content: more than a handful of colours."""
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "out")
            run_main(out)
            with Image.open(os.path.join(out, "entry.png")) as im:
                colours = im.convert("RGB").getcolors(maxcolors=1 << 24)
            self.assertIsNotNone(colours)
            self.assertGreater(len(colours), 500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
