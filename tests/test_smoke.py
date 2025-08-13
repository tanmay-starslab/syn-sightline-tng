import numpy as np

import syn_sightline_tng as sst
from syn_sightline_tng.io import load_snapshot
from syn_sightline_tng.core import intersect_with_mock_cells
from syn_sightline_tng.cli import main as cli_main


def test_version_string():
    assert isinstance(sst.__version__, str) and len(sst.__version__) > 0


def test_trace_ray_shapes():
    sl = sst.trace_ray(origin=(0, 0, 0), direction=(1, 0, 0), length=10.0, n_samples=11)
    assert sl.positions.shape == (11, 3)
    # first and last points
    assert np.allclose(sl.positions[0], (0, 0, 0))
    assert np.allclose(sl.positions[-1], (10, 0, 0))


def test_synthesize_spectrum_fields():
    sl = sst.trace_ray(origin=(0, 0, 0), direction=(0, 1, 0), length=5.0, n_samples=5)
    spec = sst.synthesize_spectrum(sl, lines=["HI 1216"]) 
    assert set(spec.keys()) >= {"wavelength", "flux", "lines", "meta"}
    assert spec["wavelength"].shape == spec["flux"].shape
    assert "resolution_kms" in spec["meta"]


def test_example_mock_snapshot_load_and_intersection():
    data = load_snapshot("examples/mock_data/snapshot_mock.json")
    centers = np.array(data["cells"]["center"], dtype=float)
    half = np.array(data["cells"]["half_size"], dtype=float)
    hits = intersect_with_mock_cells(origin=(0, 0, 0), direction=(1, 0, 0), centers=centers, half_sizes=half)
    assert isinstance(hits, list)
    assert len(hits) >= 1


def test_cli_spectrum_runs(tmp_path):
    png = tmp_path / "spec.png"
    csv = tmp_path / "spec.csv"
    code = cli_main([
        "spectrum",
        "examples/mock_data/snapshot_mock.json",
        "0", "0", "0",
        "1", "0", "0",
        "10",
        "--n", "64",
        "--lines", "HI 1216, CIV 1548",
        "--png", str(png),
        "--csv", str(csv),
    ])
    assert code == 0 and png.exists() and csv.exists()
