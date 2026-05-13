import shutil
import tempfile
import unittest
from pathlib import Path

from tsdm_src.cutoff import cutoff_argmax
from tsdm_src.tsdm_filtration_runner import run_tsdm_filtration

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_50 = REPO_ROOT / "tests" / "data_50"


class TestCutoffFnThreading(unittest.TestCase):

    def test_run_tsdm_filtration_accepts_and_threads_cutoff_fn(self):
        out_dir = Path(tempfile.mkdtemp())
        try:
            report_path = run_tsdm_filtration(
                directory=DATA_50,
                output_dir=out_dir,
                tag="t",
                filter_rounds=1,
                split_by=10,
                processes_count=1,
                cutoff_fn=cutoff_argmax,
            )
            self.assertTrue(report_path.exists())
            self.assertTrue((out_dir / "t.json").exists())
            self.assertTrue((out_dir / "t_kept.txt").exists())
        finally:
            shutil.rmtree(out_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
