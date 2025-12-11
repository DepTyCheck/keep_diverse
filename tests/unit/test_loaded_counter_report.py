import unittest
import tempfile
import os
from experiments.loaded_counter_report import LoadedCounterReport


class TestLoadedCounterReport(unittest.TestCase):

    def test_load_data(self):
        # Create a dummy file
        content = """{
      "/path/to/file1.sv": 40,
      "/path/to/file2.sv": 54
    }"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            report = LoadedCounterReport(tmp_path)
            data = report.sorted_values()

            expected_data = {
                "/path/to/file1.sv": 40,
                "/path/to/file2.sv": 54,
            }

            self.assertListEqual(data, [54, 40])
            self.assertDictEqual(report.data, expected_data)

        finally:
            os.remove(tmp_path)
