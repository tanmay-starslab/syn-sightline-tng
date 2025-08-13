"""Top-level package for syn-sightline-tng.

Lightweight stubs to enable development and testing while
the core ray tracing and spectral synthesis are implemented.
"""

from .core import Sightline, trace_ray, synthesize_spectrum

__all__ = [
    "Sightline",
    "trace_ray",
    "synthesize_spectrum",
]

__version__ = "0.1.1a1"
