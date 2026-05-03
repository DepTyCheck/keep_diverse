import json
import os
import tempfile
import unittest
from collections import Counter

from keep_diverse.counter_report import CounterReport, NoCounterReport
from experiments.loaded_counter_report import LoadedCounterReport


class TestCounterReportSave(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        os.remove(self.path)

    def test_save_includes_rounds_completed_and_filter_args(self):
        filter_args = {"split_by": 50, "relative_eps": 0.00001}
        report = CounterReport(self.path, filter_args=filter_args)
        counter = Counter({"/a.sv": 3, "/b.sv": 7})

        report.save(counter, rounds_completed=5)

        with open(self.path) as f:
            data = json.load(f)

        self.assertEqual(data["rounds_completed"], 5)
        self.assertEqual(data["filter_args"], filter_args)
        self.assertEqual(data["counter"], {"/a.sv": 3, "/b.sv": 7})

    def test_save_without_filter_args_defaults_to_empty_dict(self):
        report = CounterReport(self.path)
        report.save(Counter({"/a.sv": 1}), rounds_completed=1)

        with open(self.path) as f:
            data = json.load(f)

        self.assertEqual(data["filter_args"], {})

    def test_load_new_format(self):
        payload = {
            "filter_args": {"split_by": 50},
            "rounds_completed": 23,
            "counter": {"/x.sv": 10, "/y.sv": 5},
        }
        with open(self.path, "w") as f:
            json.dump(payload, f)

        loaded = CounterReport.load(self.path)

        self.assertEqual(loaded["rounds_completed"], 23)
        self.assertEqual(loaded["filter_args"], {"split_by": 50})
        self.assertEqual(loaded["counter"], {"/x.sv": 10, "/y.sv": 5})

    def test_roundtrip(self):
        filter_args = {"split_by": 25, "filter_rounds": 100}
        report = CounterReport(self.path, filter_args=filter_args)
        counter = Counter({"/file1.sv": 12, "/file2.sv": 0, "/file3.sv": 7})

        report.save(counter, rounds_completed=42)
        loaded = CounterReport.load(self.path)

        self.assertEqual(loaded["rounds_completed"], 42)
        self.assertEqual(loaded["filter_args"], filter_args)
        self.assertEqual(Counter(loaded["counter"]), counter)

    def test_no_counter_report_save_is_noop(self):
        noop = NoCounterReport()
        # Should not raise
        noop.save(Counter({"/a.sv": 1}), rounds_completed=3)

    def test_save_includes_knees_history_when_provided(self):
        report = CounterReport(self.path, filter_args={})
        counter = Counter({"/a.sv": 1})

        report.save(counter, rounds_completed=3, knees_history=[10, 12, 11])

        with open(self.path) as f:
            data = json.load(f)

        self.assertEqual(data["knees_history"], [10, 12, 11])

    def test_save_omits_knees_history_when_not_provided(self):
        report = CounterReport(self.path, filter_args={})
        counter = Counter({"/a.sv": 1})

        report.save(counter, rounds_completed=1)

        with open(self.path) as f:
            data = json.load(f)

        self.assertNotIn("knees_history", data)

    def test_loaded_report_exposes_knees_history(self):
        report = CounterReport(self.path, filter_args={})
        report.save(Counter({"/a.sv": 1}), rounds_completed=2, knees_history=[7, 9])

        loaded = LoadedCounterReport(self.path)
        self.assertEqual(loaded.knees_history, [7, 9])

    def test_loaded_report_defaults_knees_history_to_empty(self):
        payload = {
            "filter_args": {},
            "rounds_completed": 1,
            "counter": {"/a.sv": 1},
        }
        with open(self.path, "w") as f:
            json.dump(payload, f)

        loaded = LoadedCounterReport(self.path)
        self.assertEqual(loaded.knees_history, [])


class TestLoadedCounterReportNewFormat(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        os.remove(self.path)

    def test_reads_new_format_fields(self):
        payload = {
            "filter_args": {"split_by": 50, "filter_rounds": 100},
            "rounds_completed": 23,
            "counter": {"/a.sv": 10, "/b.sv": 3},
        }
        with open(self.path, "w") as f:
            json.dump(payload, f)

        report = LoadedCounterReport(self.path)

        self.assertEqual(report.rounds_completed, 23)
        self.assertEqual(report.filter_args, {"split_by": 50, "filter_rounds": 100})
        self.assertEqual(report.data, {"/a.sv": 10, "/b.sv": 3})
        self.assertEqual(report.sorted_values(), [10, 3])

