import json
import os
import random
import tempfile
import unittest
from collections import Counter

from keep_diverse.counter_report import CounterReport
from keep_diverse.filtered_files_list import FilteredFilesList
from keep_diverse.stop import DontStop

from tsdm_src.tsdm_keep_diverse import tsdm_keep_diverse
from tsdm_src.tsdm_plot import NoOutputTsdmPlot


def _make_test_pool(tmpdir: str) -> list[str]:
    # 5 distinct files + 5 near-duplicates of file #0 (redundant).
    paths = []
    for i in range(5):
        p = os.path.join(tmpdir, f"unique_{i}.txt")
        content = (f"topic-{i}-" + chr(ord("a") + i) * 300).encode("utf-8")
        with open(p, "wb") as f:
            f.write(content)
        paths.append(p)

    unique_0_content = open(paths[0], "rb").read()
    for i in range(5):
        p = os.path.join(tmpdir, f"duplicate_of_0_{i}.txt")
        with open(p, "wb") as f:
            f.write(unique_0_content)
        paths.append(p)

    return paths


class TestTsdmEndToEnd(unittest.TestCase):

    def test_duplicates_accumulate_in_counter(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_paths = _make_test_pool(tmp)

            kept_path = os.path.join(tmp, "kept.txt")
            report_path = os.path.join(tmp, "report.json")
            filtered = FilteredFilesList(kept_files_path=kept_path)
            report = CounterReport(
                counter_report_path=report_path,
                filter_args={"split_by": 10, "filter_rounds": 5},
            )

            random.seed(0)
            tsdm_keep_diverse(
                file_paths=file_paths,
                filter_rounds=5,
                split_by=10,
                knee_plot=NoOutputTsdmPlot(),
                filtered_files_list=filtered,
                counter_report=report,
                stop=DontStop(),
                processes_count=1,
                start_round=0,
                initial_counter=None,
            )

            with open(report_path) as f:
                data = json.load(f)
            self.assertEqual(data["rounds_completed"], 5)

            counter = Counter(data["counter"])
            dup_total = sum(
                count for path, count in counter.items() if "duplicate_of_0" in path
            )
            unique_total = sum(
                count for path, count in counter.items() if "unique_" in path
            )
            # Duplicates should be removed more often on average than unique files.
            self.assertGreater(dup_total, unique_total)


if __name__ == "__main__":
    unittest.main()
