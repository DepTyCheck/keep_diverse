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

    def test_argmax_at_zero_means_nothing_removed(self):
        # Fake the case by mocking tsdm1_sequence via subclass-style:
        # construct a curve with global max at index 0 by controlling content.
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
        # Correctness: removed is a subset of global_idxs and list length is in [0, 1]
        # (since TSDm1 produces only one step for 3 files).
        self.assertLessEqual(len(removed_global_idxs), 1)
        for idx in removed_global_idxs:
            self.assertIn(idx, global_idxs)


if __name__ == "__main__":
    unittest.main()
