import unittest

from tsdm_src.cutoff import cutoff_pct_drop, cutoff_argmax, cutoff_kneedle


class TestCutoffPctDrop(unittest.TestCase):

    def test_empty_curve_returns_zero(self):
        self.assertEqual(cutoff_pct_drop([]), 0)

    def test_single_value_curve_returns_zero(self):
        self.assertEqual(cutoff_pct_drop([0.5]), 0)

    def test_curve_crossing_threshold_returns_last_safe_index(self):
        # initial = 1.0, threshold = 0.98.
        # k=0: 1.00 >= 0.98
        # k=1: 1.10 >= 0.98
        # k=2: 1.20 >= 0.98
        # k=3: 0.90 < 0.98  -> first violation at k=3, cutoff = 2.
        self.assertEqual(cutoff_pct_drop([1.0, 1.1, 1.2, 0.9, 0.8]), 2)

    def test_curve_never_crossing_threshold_returns_last_index(self):
        # initial = 1.0, threshold = 0.98. all values >= 0.98 -> cutoff = len-1.
        self.assertEqual(cutoff_pct_drop([1.0, 1.1, 1.2, 1.0, 0.99]), 4)

    def test_drop_at_k1_returns_zero(self):
        # initial = 1.0, threshold = 0.98, curve[1] = 0.5 < 0.98 -> cutoff = 0.
        self.assertEqual(cutoff_pct_drop([1.0, 0.5, 0.3]), 0)

    def test_plateau_at_initial_then_drop(self):
        # initial = 1.0, threshold = 0.98.
        # plateau k=0..4 (=1.0). drop at k=5 (=0.5). cutoff = 4.
        self.assertEqual(cutoff_pct_drop([1.0, 1.0, 1.0, 1.0, 1.0, 0.5]), 4)

    def test_custom_min_ratio_honored(self):
        # initial = 1.0, min_ratio = 0.5, threshold = 0.5.
        # k=0..2 above, k=3 = 0.4 < 0.5 -> cutoff = 2.
        self.assertEqual(cutoff_pct_drop([1.0, 0.9, 0.7, 0.4, 0.3], min_ratio=0.5), 2)


class TestCutoffArgmax(unittest.TestCase):

    def test_empty_curve_returns_zero(self):
        self.assertEqual(cutoff_argmax([]), 0)

    def test_single_value_curve_returns_zero(self):
        self.assertEqual(cutoff_argmax([0.5]), 0)

    def test_strictly_decreasing_curve_returns_zero(self):
        # peak at start.
        self.assertEqual(cutoff_argmax([1.0, 0.9, 0.8, 0.7]), 0)

    def test_strictly_increasing_curve_returns_last_index(self):
        # peak at end.
        self.assertEqual(cutoff_argmax([0.1, 0.2, 0.3, 0.4, 0.5]), 4)

    def test_peak_in_the_middle(self):
        # max value is 5 at index 2.
        self.assertEqual(cutoff_argmax([1.0, 3.0, 5.0, 4.0, 2.0]), 2)

    def test_ties_return_smallest_index(self):
        # max value 5 appears at indices 1 and 2; smallest index wins.
        self.assertEqual(cutoff_argmax([1.0, 5.0, 5.0, 3.0]), 1)


class TestCutoffKneedle(unittest.TestCase):

    def test_empty_curve_returns_zero(self):
        self.assertEqual(cutoff_kneedle([]), 0)

    def test_length_two_curve_returns_zero(self):
        # Below the kneefinder minimum; we short-circuit.
        self.assertEqual(cutoff_kneedle([1.0, 0.5]), 0)

    def test_linear_curve_does_not_raise_and_returns_in_range(self):
        # KneeFinder controls the answer; we only assert it's wired right
        # (returns an int in [0, len-1] without raising).
        curve = [1.0, 2.0, 3.0, 4.0, 5.0]
        k = cutoff_kneedle(curve)
        self.assertIsInstance(k, int)
        self.assertGreaterEqual(k, 0)
        self.assertLess(k, len(curve))

    def test_clear_elbow_curve_lands_in_elbow_region(self):
        # Hockey stick: flat tail then steep rise. KneeFinder controls the
        # exact index; assert only that it avoids both extremes.
        curve = [1.0, 1.0, 1.0, 1.0, 5.0, 9.0, 13.0, 17.0]
        k = cutoff_kneedle(curve)
        self.assertGreaterEqual(k, 1)
        self.assertLessEqual(k, len(curve) - 2)

    def test_all_equal_curve_returns_zero(self):
        # Degenerate input — kneefinder raises on a flat curve; the guard
        # in cutoff_kneedle catches it and returns 0.
        self.assertEqual(cutoff_kneedle([1.0, 1.0, 1.0]), 0)


if __name__ == "__main__":
    unittest.main()
