import unittest

from tsdm_src.chunk_round import run_chunk_round


def _len_lzma(data: bytes) -> int:
    import lzma
    return len(lzma.compress(data))


class TestRunChunkRound(unittest.TestCase):

    def test_returns_files_to_remove_as_global_indices(self):
        # Three distinct files with global indices 100, 200, 300.
        chunk_bytes = [b"alpha-only", b"beta-only", b"gamma-only"]
        singleton_lens = [_len_lzma(b) for b in chunk_bytes]
        global_idxs = [100, 200, 300]

        removed_global_idxs, ncd1_curve = run_chunk_round(
            global_idxs=global_idxs,
            chunk_bytes=chunk_bytes,
            singleton_lens=singleton_lens,
        )

        for idx in removed_global_idxs:
            self.assertIn(idx, global_idxs)
        self.assertEqual(len(ncd1_curve), 1)

    def test_chunk_of_two_returns_empty(self):
        chunk_bytes = [b"only-two", b"only-two-more"]
        singleton_lens = [_len_lzma(b) for b in chunk_bytes]
        global_idxs = [5, 7]

        removed_global_idxs, ncd1_curve = run_chunk_round(
            global_idxs=global_idxs,
            chunk_bytes=chunk_bytes,
            singleton_lens=singleton_lens,
        )

        self.assertEqual(removed_global_idxs, [])
        self.assertEqual(ncd1_curve, [])

    def test_three_file_chunk_returns_no_removal(self):
        # With three files the greedy curve has length 1, and cutoff() always
        # returns 0 for a length-1 curve, so no files are removed.
        # Use three very different, dense random-looking strings.
        chunk_bytes = [
            bytes(range(200)),
            bytes(range(200, 400)) if max(range(200, 400)) < 256 else bytes([x % 256 for x in range(200, 400)]),
            bytes([(i * 37) % 256 for i in range(200)]),
        ]
        singleton_lens = [_len_lzma(b) for b in chunk_bytes]
        global_idxs = [10, 11, 12]

        removed_global_idxs, _ = run_chunk_round(
            global_idxs=global_idxs,
            chunk_bytes=chunk_bytes,
            singleton_lens=singleton_lens,
        )
        self.assertEqual(removed_global_idxs, [])


    def test_cutoff_fn_overrides_removal_count(self):
        # 4-file chunk -> tsdm1 greedy curve has length 2 (n - 2).
        chunk_bytes = [b"alpha-content", b"beta-content", b"gamma-content", b"delta-content"]
        singleton_lens = [_len_lzma(b) for b in chunk_bytes]
        global_idxs = [10, 20, 30, 40]

        seen_curves = []

        def fake_cutoff(curve):
            seen_curves.append(list(curve))
            return len(curve)  # remove the entire greedy prefix

        removed, ncd1_curve = run_chunk_round(
            global_idxs=global_idxs,
            chunk_bytes=chunk_bytes,
            singleton_lens=singleton_lens,
            cutoff_fn=fake_cutoff,
        )

        self.assertEqual(seen_curves, [ncd1_curve])
        self.assertEqual(len(removed), len(ncd1_curve))
        for idx in removed:
            self.assertIn(idx, global_idxs)

    def test_default_cutoff_is_kneedle(self):
        # 4-file chunk -> curve length 2 -> cutoff_kneedle short-circuits to 0,
        # so the default behaviour removes nothing.
        chunk_bytes = [b"alpha-content", b"beta-content", b"gamma-content", b"delta-content"]
        singleton_lens = [_len_lzma(b) for b in chunk_bytes]
        global_idxs = [10, 20, 30, 40]

        removed, ncd1_curve = run_chunk_round(
            global_idxs=global_idxs,
            chunk_bytes=chunk_bytes,
            singleton_lens=singleton_lens,
        )

        self.assertEqual(len(ncd1_curve), 2)
        self.assertEqual(removed, [])


if __name__ == "__main__":
    unittest.main()
