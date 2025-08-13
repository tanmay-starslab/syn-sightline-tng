from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import numpy as np


@dataclass
class AABB:
    """Axis-aligned bounding box.

    Defined by min and max corners in 3D.
    """

    min: np.ndarray  # shape (3,)
    max: np.ndarray  # shape (3,)


def intersect_ray_aabb(origin: Sequence[float], direction: Sequence[float], box: AABB) -> Tuple[float, float] | None:
    """Compute parametric entry/exit of a ray through an AABB.

    Returns (tmin, tmax) if intersecting, otherwise None. This is a standard
    slab method and is a placeholder for spatial indexing acceleration.
    """

    o = np.asarray(origin, dtype=float)
    d = np.asarray(direction, dtype=float)
    inv_d = 1.0 / d
    t0s = (box.min - o) * inv_d
    t1s = (box.max - o) * inv_d
    tmin = np.maximum.reduce(np.minimum(t0s, t1s))
    tmax = np.minimum.reduce(np.maximum(t0s, t1s))
    if tmax >= max(tmin, 0.0):
        return float(tmin), float(tmax)
    return None


def intersect_ray_cells(
    origin: Sequence[float],
    direction: Sequence[float],
    centers: np.ndarray,
    half_sizes: np.ndarray,
) -> List[int]:
    """Return indices of cells (AABBs) intersected by a ray (naive loop).

    This is a correctness-oriented placeholder; replace with BVH/kD-tree
    acceleration for production.
    """

    boxes = [
        AABB(min=c - h, max=c + h) for c, h in zip(np.asarray(centers), np.asarray(half_sizes))
    ]
    hits: List[int] = []
    for i, box in enumerate(boxes):
        if intersect_ray_aabb(origin, direction, box) is not None:
            hits.append(i)
    return hits

