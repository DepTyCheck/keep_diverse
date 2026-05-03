import unittest

from .test_file_compression import TestFileCompression
from .test_files_reading import TestFilesReading
from .test_filtration_round import TestFiltrationRound
from .test_subset_filter import TestSubsetFilter
from .test_pct_filter import TestPCTFilter
from .test_metric import TestMetric
from .test_counter_report_resume import TestCounterReportSave, TestLoadedCounterReportNewFormat

from .test_ncd1 import TestCOfConcat, TestNcd1Formula
from .test_cutoff import TestCutoffPctDrop, TestCutoffArgmax, TestCutoffKneedle
from .test_tsdm1 import TestTsdm1Sequence
from .test_chunk_round import TestRunChunkRound
from .test_tsdm_filtration_round import TestFiltrationRound as TestTsdmFiltrationRound
from .test_tsdm_end_to_end import TestTsdmEndToEnd
from .test_tsdm_filtration_runner import TestTsdmFiltrationRunner


if __name__ == "__main__":
    suite = unittest.TestSuite()

    loader = unittest.TestLoader()
    test_cases = [
        TestFileCompression,
        TestFilesReading,
        TestFiltrationRound,
        TestSubsetFilter,
        TestPCTFilter,
        TestMetric,
        TestCounterReportSave,
        TestLoadedCounterReportNewFormat,
        TestCOfConcat,
        TestNcd1Formula,
        TestCutoffPctDrop,
        TestCutoffArgmax,
        TestCutoffKneedle,
        TestTsdm1Sequence,
        TestRunChunkRound,
        TestTsdmFiltrationRound,
        TestTsdmEndToEnd,
        TestTsdmFiltrationRunner,
    ]

    for test_case in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_case))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
