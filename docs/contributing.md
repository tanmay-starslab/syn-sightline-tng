# Contributing

Thanks for helping improve syn-sightline-tng! Start here:

- Read the repository guidelines in AGENTS.md for project structure, style, and PR process:
  https://github.com/tanmay-starslab/syn-sightline-tng/blob/main/AGENTS.md
- Local docs: `mkdocs serve`; strict build: `mkdocs build --strict`.
- Tests: `pytest -q`; put tests in `tests/test_*.py`.

Quickstart example

```python
import syn_sightline_tng as sst
sl = sst.trace_ray(origin=(0,0,0), direction=(1,0,0), length=10.0, n_samples=128)
spec = sst.synthesize_spectrum(sl, lines=["HI 1216"])  # placeholder API
```

Planned architecture (high level)
- I/O: thin wrappers for AREPO/TNG snapshots (h5py-based).
- Ray tracing: fast sightline sampling/intersection (vectorized, chunked I/O).
- Spectra: line lists, Voigt profiles, instrumental LSF.
- CLI: reproducible runs and benchmarks.

Open a draft PR early to discuss scope and interfaces.
