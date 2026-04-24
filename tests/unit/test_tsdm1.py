import unittest

from tsdm_src.tsdm1 import tsdm1_sequence


def _len_lzma(data: bytes) -> int:
    import lzma
    return len(lzma.compress(data))


class TestTsdm1Sequence(unittest.TestCase):

    def test_three_files_produces_one_step(self):
        # Y0 = {A, B, C}, Y1 = Y0 \ {argmax}, stop (|Y| == 2).
        chunk_bytes = [b"aaaaaaaaaaaaaa", b"bbbbbbbbbbbbbb", b"cccccccccccccc"]
        singleton_lens = [_len_lzma(b) for b in chunk_bytes]
        removal_order, ncd1_curve = tsdm1_sequence(chunk_bytes, singleton_lens)
        self.assertEqual(len(removal_order), 1)
        self.assertEqual(len(ncd1_curve), 1)
        self.assertIn(removal_order[0], {0, 1, 2})

    def test_five_files_produces_three_steps(self):
        chunk_bytes = [
            b"alpha-content-one",
            b"beta-content-two",
            b"gamma-content-three",
            b"delta-content-four",
            b"epsilon-content-five",
        ]
        singleton_lens = [_len_lzma(b) for b in chunk_bytes]
        removal_order, ncd1_curve = tsdm1_sequence(chunk_bytes, singleton_lens)
        self.assertEqual(len(removal_order), 3)
        self.assertEqual(len(ncd1_curve), 3)
        self.assertEqual(len(set(removal_order)), 3)  # no repeats

    def test_duplicate_gets_removed_first(self):
        # Three distinct high-entropy payloads plus an exact duplicate of the
        # first. With incompressible inputs, removing one of the duplicate
        # copies leaves three all-distinct blocks (large C), while removing
        # any of the unique blocks leaves the duplicate pair in (smaller C
        # thanks to LZMA dedup). So the greedy max-residual step must pick
        # one of the duplicate indices first.
        import hashlib

        def _payload(seed: int, size: int = 2048) -> bytes:
            out = bytearray()
            h = hashlib.sha256(seed.to_bytes(4, "big")).digest()
            while len(out) < size:
                h = hashlib.sha256(h).digest()
                out.extend(h)
            return bytes(out[:size])

        unique_a = _payload(1)
        unique_b = _payload(2)
        unique_c = _payload(3)
        dup_of_a = bytes(unique_a)  # exact copy
        chunk_bytes = [unique_a, unique_b, unique_c, dup_of_a]
        singleton_lens = [_len_lzma(b) for b in chunk_bytes]
        removal_order, _ = tsdm1_sequence(chunk_bytes, singleton_lens)
        # First removed should be index 0 or 3 (the duplicates).
        self.assertIn(removal_order[0], {0, 3})

    def test_too_few_files_returns_empty(self):
        # 2 files: nothing to remove, empty sequence.
        chunk_bytes = [b"one", b"two"]
        singleton_lens = [_len_lzma(b) for b in chunk_bytes]
        removal_order, ncd1_curve = tsdm1_sequence(chunk_bytes, singleton_lens)
        self.assertEqual(removal_order, [])
        self.assertEqual(ncd1_curve, [])


if __name__ == "__main__":
    unittest.main()
