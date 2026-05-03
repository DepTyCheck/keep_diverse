import json
import os
import tempfile
import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.plot_knee import plot_knee_from_report


def _write_report(path: str, payload: dict) -> None:
    with open(path, "w") as f:
        json.dump(payload, f)


class TestPlotKneeFromReport(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.report_path = os.path.join(self.tmp_dir.name, "report.json")
        self.svg_path = os.path.join(self.tmp_dir.name, "knee.svg")

    def tearDown(self):
        plt.close("all")
        self.tmp_dir.cleanup()

    def test_renders_two_rows_when_knees_history_present(self):
        _write_report(self.report_path, {
            "filter_args": {"split_by": 50},
            "rounds_completed": 4,
            "counter": {f"/f{i}.sv": i for i in range(5)},
            "knees_history": [2, 3, 2, 3],
        })

        plot_knee_from_report(self.report_path, self.svg_path)

        self.assertTrue(os.path.exists(self.svg_path))
        self.assertGreater(os.path.getsize(self.svg_path), 1024)
        with open(self.svg_path) as f:
            head = f.read(200)
        self.assertIn("<svg", head)

        # Force the test to actually verify the 2-row branch by inspecting
        # the SVG body for two distinct subplot groups.
        with open(self.svg_path) as f:
            body = f.read()
        self.assertGreaterEqual(body.count("\"axes_"), 2)

    def test_renders_single_row_when_no_knees_history(self):
        _write_report(self.report_path, {
            "filter_args": {"split_by": 50},
            "rounds_completed": 4,
            "counter": {f"/f{i}.sv": i for i in range(5)},
        })

        plot_knee_from_report(self.report_path, self.svg_path)

        self.assertTrue(os.path.exists(self.svg_path))
        self.assertGreater(os.path.getsize(self.svg_path), 512)
        with open(self.svg_path) as f:
            head = f.read(200)
        self.assertIn("<svg", head)

    def test_renders_single_row_when_knees_history_empty(self):
        _write_report(self.report_path, {
            "filter_args": {"split_by": 50},
            "rounds_completed": 0,
            "counter": {f"/f{i}.sv": i for i in range(5)},
            "knees_history": [],
        })

        plot_knee_from_report(self.report_path, self.svg_path)

        self.assertTrue(os.path.exists(self.svg_path))
        with open(self.svg_path) as f:
            head = f.read(200)
        self.assertIn("<svg", head)


if __name__ == "__main__":
    unittest.main()
