import numpy as np
from scipy.stats import poisson


def poisson_metric_value(distances: dict[tuple[int, int], float]) -> float:
    distance_values = np.array(list(distances.values()), dtype=np.float32)
    distance_values = np.sort(distance_values)
    dist_len = distance_values.size
    indices = np.arange(dist_len)
    weights = poisson.pmf(indices, dist_len)
    values = 2 * distance_values * weights
    return values.sum()


def diversity_metric(distances: dict) -> float:
    nearest = {}
    for (i, j), d in distances.items():
        nearest[i] = min(nearest.get(i, float("inf")), d)
        nearest[j] = min(nearest.get(j, float("inf")), d)
    return sum(nearest.values())
