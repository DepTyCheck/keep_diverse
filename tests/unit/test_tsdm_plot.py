import os
import tempfile
import unittest
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from keep_diverse.knee import Knee
from tsdm_src.tsdm_plot import TsdmPlot, NoOutputTsdmPlot


def _make_knee(removes: dict[str, int]) -> Knee:
    return Knee(Counter(removes))


class TestTsdmPlot(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.svg_path = os.path.join(self.tmp_dir.name, "plot.svg")
        self.knee = _make_knee({f"/f{i}.sv": i for i in range(10)})

    def tearDown(self):
        plt.close("all")
        self.tmp_dir.cleanup()

    def test_title_omits_total_when_total_rounds_is_none(self):
        plot = TsdmPlot(output_file=self.svg_path, total_rounds=None)
        plot.draw(knee=self.knee, knees_history=[3, 4, 3], round_idx=3)

        self.assertTrue(os.path.exists(self.svg_path))
        with open(self.svg_path) as f:
            body = f.read()
        self.assertIn("Round 3", body)
        self.assertNotIn("Round 3 /", body)

    def test_title_includes_total_when_total_rounds_supplied(self):
        plot = TsdmPlot(output_file=self.svg_path, total_rounds=420)
        plot.draw(knee=self.knee, knees_history=[3, 4, 3], round_idx=3)

        self.assertTrue(os.path.exists(self.svg_path))
        with open(self.svg_path) as f:
            body = f.read()
        self.assertIn("Round 3 / 420", body)

    def test_title_includes_kept_count(self):
        plot = TsdmPlot(output_file=self.svg_path, total_rounds=None)
        plot.draw(knee=self.knee, knees_history=[1], round_idx=1)

        files_count = len(self.knee.y_values)
        kept = files_count - self.knee.value
        with open(self.svg_path) as f:
            body = f.read()
        self.assertIn(f"kept {kept} / {files_count}", body)

    def test_renders_two_panels(self):
        plot = TsdmPlot(output_file=self.svg_path, total_rounds=None)
        plot.draw(knee=self.knee, knees_history=[3, 4, 3], round_idx=3)

        with open(self.svg_path) as f:
            body = f.read()
        # Two distinct axes groups in the SVG.
        self.assertGreaterEqual(body.count("\"axes_"), 2)

    def test_does_not_raise_on_empty_history(self):
        plot = TsdmPlot(output_file=self.svg_path, total_rounds=None)
        plot.draw(knee=self.knee, knees_history=[], round_idx=0)

        self.assertTrue(os.path.exists(self.svg_path))

    def test_does_not_raise_on_single_element_history(self):
        plot = TsdmPlot(output_file=self.svg_path, total_rounds=10)
        plot.draw(knee=self.knee, knees_history=[5], round_idx=1)

        self.assertTrue(os.path.exists(self.svg_path))


class TestNoOutputTsdmPlot(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.svg_path = os.path.join(self.tmp_dir.name, "plot.svg")

    def tearDown(self):
        plt.close("all")
        self.tmp_dir.cleanup()

    def test_draw_writes_no_file(self):
        knee = _make_knee({f"/f{i}.sv": i for i in range(5)})
        plot = NoOutputTsdmPlot()
        plot.draw(knee=knee, knees_history=[1, 2], round_idx=2)

        self.assertFalse(os.path.exists(self.svg_path))


if __name__ == "__main__":
    unittest.main()
