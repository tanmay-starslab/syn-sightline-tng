from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np
from .geometry import intersect_ray_cells


@dataclass
class Sightline:
    """Container for a sampled sightline.

    Attributes
    - positions: array of shape (N, 3) in code units.
    - metadata: free-form dictionary for configuration/context.
    """

    positions: np.ndarray
    metadata: dict


def _normalize(vec: Sequence[float]) -> np.ndarray:
    v = np.asarray(vec, dtype=float)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError("direction vector must be non-zero")
    return v / n


def trace_ray(
    origin: Sequence[float],
    direction: Sequence[float],
    length: float,
    n_samples: int = 128,
    *,
    metadata: Optional[dict] = None,
) -> Sightline:
    """Sample a straight-line ray in 3D space.

    This is a placeholder for a faster AREPO/TNG-aware implementation.
    It simply samples evenly along the ray segment.
    """

    if n_samples < 2:
        raise ValueError("n_samples must be >= 2")
    o = np.asarray(origin, dtype=float).reshape(1, 3)
    d = _normalize(direction).reshape(1, 3)
    ts = np.linspace(0.0, float(length), int(n_samples)).reshape(-1, 1)
    positions = o + ts * d
    return Sightline(positions=positions, metadata=metadata or {})


def intersect_with_mock_cells(
    origin: Sequence[float],
    direction: Sequence[float],
    centers: np.ndarray,
    half_sizes: np.ndarray,
) -> List[int]:
    """Convenience wrapper to intersect a ray with mock AABB cells.

    Use this for examples/mock data until full AREPO cell geometry is wired.
    """

    return intersect_ray_cells(origin, direction, centers, half_sizes)


def synthesize_spectrum(
    sightline: Sightline,
    lines: Optional[Iterable[str]] = None,
    *,
    resolution_kms: float = 10.0,
) -> dict:
    """Produce a dummy spectrum for the given sightline.

    Returns a dict with wavelengths (Angstrom) and flux (unitless),
    useful as a smoke test for downstream plotting/pipelines.
    """

    n = max(256, int(len(sightline.positions)))
    wl0 = 1200.0
    wavelengths = wl0 + np.arange(n, dtype=float)
    # Toy absorption feature
    center = wl0 + n / 2
    sigma = max(1.0, resolution_kms / 3.0)
    profile = np.exp(-0.5 * ((wavelengths - center) / sigma) ** 2)
    flux = 1.0 - 0.2 * profile
    return {
        "wavelength": wavelengths,
        "flux": flux,
        "lines": list(lines) if lines is not None else [],
        "meta": {"resolution_kms": resolution_kms, **(sightline.metadata or {})},
    }
