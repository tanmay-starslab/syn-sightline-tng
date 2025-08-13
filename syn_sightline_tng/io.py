from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Optional
import json


def load_snapshot(path: str | Path) -> Dict[str, Any]:
    """Load a snapshot (mock JSON or HDF5 placeholder).

    - If ``.json``: parse and return dict (used for examples/mock data).
    - If HDF5 (e.g., ``.hdf5``): return minimal handle info for now.
    """

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    if p.suffix.lower() == ".json":
        with p.open() as f:
            return json.load(f)
    if p.suffix.lower() in {".h5", ".hdf5"}:
        # Placeholder: only return top-level groups for now
        try:
            import h5py  # type: ignore
        except Exception:
            return {"error": "h5py not available", "path": str(p)}
        with h5py.File(p, "r") as f:  # type: ignore[name-defined]
            return {"h5_groups": list(f.keys())}
    return {"path": str(p.resolve())}


def load_arepo_snapshot(
    path: str | Path,
    fields: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """AREPO/TNG-oriented snapshot loader (stub).

    Expected responsibilities (to implement):
    - Map TNG/AREPO HDF5 layout to numpy arrays.
    - Only load requested ``fields`` to reduce memory.
    - Handle unit conversions via metadata.
    """

    data = load_snapshot(path)
    data.setdefault("meta", {})
    data["meta"].setdefault("loader", "arepo-stub")
    if fields:
        data["meta"]["requested_fields"] = list(fields)
    return data
