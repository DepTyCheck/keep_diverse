import json
import os
import random
import tempfile
import unittest
from pathlib import Path


class TestTsdmFiltrationRunner(unittest.TestCase):

    def _make_tiny_dataset(self, tmpdir: str) -> Path:
        data_dir = Path(tmpdir) / "data"
        data_dir.mkdir()
        for i in range(6):
            body = (f"topic-{i}-" + chr(ord("a") + i) * 200).encode("utf-8")
            (data_dir / f"file_{i:02d}.txt").write_bytes(body)
        return data_dir

    def test_runner_writes_report_and_kept_list(self):
        from tsdm_src.tsdm_filtration_runner import run_tsdm_filtration

        with tempfile.TemporaryDirectory() as tmp:
            data_dir = self._make_tiny_dataset(tmp)
            output_dir = Path(tmp) / "output"
            output_dir.mkdir()

            random.seed(0)
            report_path = run_tsdm_filtration(
                directory=data_dir,
                output_dir=output_dir,
                tag="t",
                filter_rounds=2,
                split_by=50,
                processes_count=1,
            )

            self.assertEqual(report_path, output_dir / "t.json")
            self.assertTrue(report_path.exists())
            self.assertTrue((output_dir / "t_kept.txt").exists())

            with open(report_path) as f:
                data = json.load(f)
            self.assertEqual(data["rounds_completed"], 2)
            self.assertEqual(len(data["counter"]), 6)
            self.assertEqual(data["filter_args"]["split_by"], 50)
            self.assertEqual(data["filter_args"]["filter_rounds"], 2)

    def test_runner_follows_symlinked_directory(self):
        from tsdm_src.tsdm_filtration_runner import run_tsdm_filtration

        with tempfile.TemporaryDirectory() as tmp:
            real_dir = self._make_tiny_dataset(tmp)
            linked_dir = Path(tmp) / "linked_data"
            os.symlink(real_dir, linked_dir)

            output_dir = Path(tmp) / "output"
            output_dir.mkdir()

            random.seed(0)
            report_path = run_tsdm_filtration(
                directory=linked_dir,
                output_dir=output_dir,
                tag="link",
                filter_rounds=1,
                split_by=50,
                processes_count=1,
            )

            with open(report_path) as f:
                data = json.load(f)
            self.assertEqual(len(data["counter"]), 6)


    def test_runner_accepts_custom_stop(self):
        from tsdm_src.tsdm_filtration_runner import run_tsdm_filtration

        class _RecordingStop:
            def __init__(self):
                self.calls = 0

            def should_stop(self, knees_list):
                self.calls += 1
                return False

        with tempfile.TemporaryDirectory() as tmp:
            data_dir = self._make_tiny_dataset(tmp)
            output_dir = Path(tmp) / "output"
            output_dir.mkdir()

            recording_stop = _RecordingStop()

            random.seed(0)
            report_path = run_tsdm_filtration(
                directory=data_dir,
                output_dir=output_dir,
                tag="custom_stop",
                filter_rounds=2,
                split_by=50,
                processes_count=1,
                stop=recording_stop,
            )

            self.assertTrue(report_path.exists())
            # Stop.should_stop is called once per completed round.
            self.assertEqual(recording_stop.calls, 2)

            # Default path still works (omitting stop=).
            random.seed(0)
            default_report = run_tsdm_filtration(
                directory=data_dir,
                output_dir=output_dir,
                tag="default_stop",
                filter_rounds=1,
                split_by=50,
                processes_count=1,
            )
            self.assertTrue(default_report.exists())
            with open(default_report) as f:
                default_data = json.load(f)
            self.assertEqual(default_data["rounds_completed"], 1)


    def test_runner_writes_knees_history_in_report(self):
        from tsdm_src.tsdm_filtration_runner import run_tsdm_filtration

        with tempfile.TemporaryDirectory() as tmp:
            data_dir = self._make_tiny_dataset(tmp)
            output_dir = Path(tmp) / "output"
            output_dir.mkdir()

            random.seed(0)
            report_path = run_tsdm_filtration(
                directory=data_dir,
                output_dir=output_dir,
                tag="khist",
                filter_rounds=3,
                split_by=50,
                processes_count=1,
            )

            with open(report_path) as f:
                data = json.load(f)

            self.assertIn("knees_history", data)
            self.assertEqual(len(data["knees_history"]), 3)
            for v in data["knees_history"]:
                self.assertIsInstance(v, int)


if __name__ == "__main__":
    unittest.main()
