from __future__ import annotations

import argparse
from typing import Sequence, List

import numpy as np

from . import __version__
from .core import trace_ray, synthesize_spectrum
from .io import load_snapshot


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="syn-sightline-tng")
    parser.add_argument("--version", action="version", version=__version__)

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_trace = sub.add_parser("trace", help="sample a straight-line sightline")
    p_trace.add_argument("ox", type=float)
    p_trace.add_argument("oy", type=float)
    p_trace.add_argument("oz", type=float)
    p_trace.add_argument("dx", type=float)
    p_trace.add_argument("dy", type=float)
    p_trace.add_argument("dz", type=float)
    p_trace.add_argument("length", type=float)
    p_trace.add_argument("--n", type=int, default=128, help="number of samples")

    p_spec = sub.add_parser("spectrum", help="synthesize a spectrum from a straight sightline")
    p_spec.add_argument("snapshot", type=str, help="path to mock JSON or HDF5 snapshot")
    p_spec.add_argument("ox", type=float)
    p_spec.add_argument("oy", type=float)
    p_spec.add_argument("oz", type=float)
    p_spec.add_argument("dx", type=float)
    p_spec.add_argument("dy", type=float)
    p_spec.add_argument("dz", type=float)
    p_spec.add_argument("length", type=float)
    p_spec.add_argument("--n", type=int, default=256, help="number of samples")
    p_spec.add_argument("--lines", type=str, default="HI 1216", help="comma-separated line list")
    p_spec.add_argument("--png", type=str, default=None, help="save spectrum plot to PNG path")
    p_spec.add_argument("--csv", type=str, default=None, help="save wavelength,flux to CSV path")

    args = parser.parse_args(argv)
    if args.cmd == "trace":
        sl = trace_ray(
            origin=(args.ox, args.oy, args.oz),
            direction=(args.dx, args.dy, args.dz),
            length=args.length,
            n_samples=args.n,
        )
        print(sl.positions.shape[0])
        return 0

    if args.cmd == "spectrum":
        snap = load_snapshot(args.snapshot)
        sl = trace_ray(
            origin=(args.ox, args.oy, args.oz),
            direction=(args.dx, args.dy, args.dz),
            length=args.length,
            n_samples=args.n,
            metadata={"snapshot": args.snapshot, **({"meta": snap.get("meta")} if isinstance(snap, dict) else {})},
        )
        lines: List[str] = [s.strip() for s in str(args.lines).split(",") if s.strip()]
        spec = synthesize_spectrum(sl, lines=lines)
        wl = spec["wavelength"]
        fx = spec["flux"]
        print(f"samples={len(wl)} lines={len(lines)}")
        if args.csv:
            import csv
            with open(args.csv, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["wavelength", "flux"])
                for a, b in zip(wl, fx):
                    w.writerow([f"{a:.6f}", f"{b:.6f}"])
            print(f"wrote CSV: {args.csv}")
        if args.png:
            try:
                import matplotlib.pyplot as plt  # type: ignore
                plt.figure(figsize=(6, 3))
                plt.plot(wl, fx, lw=1)
                plt.xlabel("Angstrom")
                plt.ylabel("Flux")
                plt.tight_layout()
                plt.savefig(args.png, dpi=150)
                print(f"wrote PNG: {args.png}")
            except Exception as e:  # pragma: no cover
                print(f"plot skipped: {e}")
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
