"""Command-line entry point for ECG RR Tool.

M1 scope: provide a minimal CLI skeleton only.
Full CSV processing is intentionally deferred to M2/M3.
"""

from __future__ import annotations

import argparse
from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ecg-rr-tool",
        description="ECG RR analysis tool skeleton. Full processing starts in later milestones.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
