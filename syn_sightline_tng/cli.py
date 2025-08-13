from __future__ import annotations

import argparse
from typing import Sequence

import numpy as np

from . import __version__
from .core import trace_ray


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

    parser.error("unknown command")
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

