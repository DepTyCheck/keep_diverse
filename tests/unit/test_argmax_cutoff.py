import unittest

from tsdm_src.argmax_cutoff import argmax_cutoff


class TestArgmaxCutoff(unittest.TestCase):

    def test_monotonic_increasing_curve(self):
        self.assertEqual(argmax_cutoff([0.1, 0.2, 0.3, 0.4]), 3)

    def test_monotonic_decreasing_curve(self):
        self.assertEqual(argmax_cutoff([0.4, 0.3, 0.2, 0.1]), 0)

    def test_peaked_curve(self):
        self.assertEqual(argmax_cutoff([0.1, 0.5, 0.9, 0.4, 0.2]), 2)

    def test_ties_return_smallest_k(self):
        self.assertEqual(argmax_cutoff([0.2, 0.9, 0.9, 0.9, 0.1]), 1)

    def test_empty_curve_returns_zero(self):
        self.assertEqual(argmax_cutoff([]), 0)

    def test_single_value_curve(self):
        self.assertEqual(argmax_cutoff([0.5]), 0)


if __name__ == "__main__":
    unittest.main()
