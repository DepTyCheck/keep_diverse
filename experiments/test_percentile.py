import numpy as np


def test_percentile():
    arr = [2, 3, 5]  # np.zeros(1_000)
    arr[-1] = 1

    p = np.percentile(arr, 0.13)
    print(f"Max value: {np.max(arr)}")
    print(f"0.13 percentile: {p}")


if __name__ == "__main__":
    test_percentile()
