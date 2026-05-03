import os
import tempfile
import unittest
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from keep_diverse.knee import Knee


def _make_knee() -> Knee:
    # Five fake files with monotonically rising removal counts so KneeFinder
    # can pick a non-degenerate elbow.
    return Knee(Counter({f"/f{i}.sv": i for i in range(5)}))


class TestRenderKneeFigure(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.svg_path = os.path.join(self.tmp_dir.name, "knee.svg")

    def tearDown(self):
        plt.close("all")
        self.tmp_dir.cleanup()

    def test_renders_two_rows_when_knees_history_present(self):
        from experiments.plot_knee import render_knee_figure

        render_knee_figure(
            knee=_make_knee(),
            knees_history=[2, 3, 2, 3],
            files_count=5,
            output_path=self.svg_path,
            title="t",
        )

        self.assertTrue(os.path.exists(self.svg_path))
        with open(self.svg_path) as f:
            body = f.read()
        self.assertIn("<svg", body[:200])
        self.assertGreaterEqual(body.count("\"axes_"), 2)

    def test_renders_single_row_when_knees_history_empty(self):
        from experiments.plot_knee import render_knee_figure

        render_knee_figure(
            knee=_make_knee(),
            knees_history=[],
            files_count=5,
            output_path=self.svg_path,
        )

        self.assertTrue(os.path.exists(self.svg_path))
        with open(self.svg_path) as f:
            body = f.read()
        self.assertIn("<svg", body[:200])

    def test_title_appears_in_svg_when_provided(self):
        from experiments.plot_knee import render_knee_figure

        render_knee_figure(
            knee=_make_knee(),
            knees_history=[2, 3, 2, 3],
            files_count=5,
            output_path=self.svg_path,
            title="UNIQUE-TITLE-MARKER-123",
        )

        with open(self.svg_path) as f:
            body = f.read()
        self.assertIn("UNIQUE-TITLE-MARKER-123", body)


if __name__ == "__main__":
    unittest.main()
