"""GUI entry point placeholder for ECG RR Tool.

M1 scope: provide a minimal GUI module skeleton only.
Full GUI implementation is deferred to M5.
"""

from __future__ import annotations

import argparse
from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ecg-rr-tool-gui",
        description="GUI placeholder for ECG RR Tool. Full GUI implementation starts in M5.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
