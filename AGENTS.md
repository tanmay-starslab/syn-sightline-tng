# Repository Guidelines

## Project Structure & Modules
- `syn_sightline_tng/`: Python package (library entry point).
- `docs/` + `mkdocs.yml`: MkDocs site (built and deployed via GitHub Actions).
- `tests/`: Test suite placeholder (add `test_*.py` here).
- `.github/workflows/`: CI for docs deploy.
- Packaging: `pyproject.toml` (setuptools); Python >= 3.10.

## Build, Test, and Dev Commands
- Create env: `python -m venv .venv && source .venv/bin/activate`.
- Install (with docs/examples extras): `pip install -e .[docs,examples]`.
- Docs live-reload: `mkdocs serve` (or `uv run --extra docs mkdocs serve`).
- Docs build: `mkdocs build` (CI uses `uv run --extra docs mkdocs build`).
- Package locally: `python -m build` (optional, if `build` is installed).

## Coding Style & Naming
- Python style: PEP 8, 4-space indentation, 88–100 col target.
- Naming: modules/files `snake_case.py`; functions/vars `snake_case`; classes `PascalCase`.
- Types: use type hints and docstrings for public APIs.
- Imports: standard lib, third-party, local (grouped, newline-separated).

## Testing Guidelines
- Framework: pytest (recommended).
- Location: put tests under `tests/`; files named `test_*.py`.
- Run: `pytest -q` (add markers as needed).
- Coverage: target meaningful unit tests around data I/O and core ray-tracing utilities as they land; prefer small, deterministic fixtures.

## Commit & Pull Requests
- Commits: short, imperative subject (≤72 chars). Example: `fix docs nav paths`.
- Reference issues in body: `Fixes #12` or `Refs #12` when applicable.
- PRs: clear description of what/why, linked issues, minimal diff, and notes on docs/tests impact. Include before/after examples or screenshots for docs changes.
- Branches: `feature/<short-name>`, `fix/<short-name>`, `docs/<short-name>`.

## Docs & CI Notes
- Docs are deployed from `main` via `.github/workflows/deploy_docs.yml` using `uv` and MkDocs Material.
- Validate docs locally before PR: `mkdocs build --strict`.

## Security & Configuration
- Do not commit data secrets or large binaries. Keep example data under `syn_sightline_tng/data/` if needed and small.
- Pin heavy, optional tools in extras; keep core deps minimal (`numpy`, `h5py`).
