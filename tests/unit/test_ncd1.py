import unittest

from tsdm_src.ncd1 import c_of_concat, ncd1


class TestCOfConcat(unittest.TestCase):

    def test_single_byte_string(self):
        value = c_of_concat([b"hello world"])
        self.assertGreater(value, 0)

    def test_concat_matches_lzma_of_joined_bytes(self):
        import lzma

        parts = [b"alpha", b"beta", b"gamma"]
        expected = len(lzma.compress(b"".join(parts)))
        self.assertEqual(c_of_concat(parts), expected)

    def test_empty_list_returns_zero(self):
        self.assertEqual(c_of_concat([]), 0)


class TestNcd1Formula(unittest.TestCase):

    def test_identical_strings_give_zero_numerator(self):
        # NCD1 = (C(X) - min C(x)) / max C(X \ {x})
        # For identical strings, C(X) approx equals C(x_single) so numerator ~ 0.
        value = ncd1(c_full=100, min_c_single=100, max_c_without_i=100)
        self.assertEqual(value, 0.0)

    def test_regular_values(self):
        value = ncd1(c_full=200, min_c_single=50, max_c_without_i=150)
        self.assertAlmostEqual(value, (200 - 50) / 150, places=6)

    def test_zero_denominator_returns_zero(self):
        self.assertEqual(ncd1(c_full=200, min_c_single=50, max_c_without_i=0), 0.0)


if __name__ == "__main__":
    unittest.main()
