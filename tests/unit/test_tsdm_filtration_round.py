import os
import tempfile
import unittest

import numpy as np

from tsdm_src.filtration_round import filtration_round


def _make_fixture_files(tmpdir: str, count: int) -> list[str]:
    paths = []
    for i in range(count):
        path = os.path.join(tmpdir, f"file_{i}.txt")
        content = (f"seed-{i}-" + "x" * (100 + i * 10)).encode("utf-8")
        with open(path, "wb") as f:
            f.write(content)
        paths.append(path)
    return paths


class TestFiltrationRound(unittest.TestCase):

    def test_returns_removed_indices_and_curves(self):
        import lzma

        with tempfile.TemporaryDirectory() as tmp:
            file_paths = _make_fixture_files(tmp, 10)

            singleton_lens = []
            for p in file_paths:
                with open(p, "rb") as f:
                    singleton_lens.append(len(lzma.compress(f.read())))

            lens_path = os.path.join(tmp, "singleton_lens.npy")
            np.save(lens_path, np.array(singleton_lens, dtype=np.int64))

            files_to_remove, ncd1_curves = filtration_round(
                file_paths=file_paths,
                split_by=5,
                singleton_lens_file_path=lens_path,
                processes_count=1,
            )

            for p in files_to_remove:
                self.assertIn(p, file_paths)
            # Two chunks of 5 files => two NCD1 curves.
            self.assertEqual(len(ncd1_curves), 2)


if __name__ == "__main__":
    unittest.main()
