"""Command-line entry point for ECG RR Tool."""

from __future__ import annotations

import argparse

from . import __version__
from .pipeline import load_bidmc_csv, resample_to_50hz, save_resampled_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ecg-rr-tool",
        description="ECG RR preprocessing pipeline for BIDMC CSV (M2: load/validate/resample).",
    )
    parser.add_argument("input_csv", nargs="?", help="Path to input BIDMC CSV file")
    parser.add_argument("--output", help="Path to M2 resampled output CSV")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.input_csv:
        return 0

    if not args.output:
        parser.error("--output is required when input_csv is provided")

    raw = load_bidmc_csv(args.input_csv)
    resampled = resample_to_50hz(raw)
    output_path = save_resampled_csv(resampled, args.output)

    print(
        "Processed CSV:",
        f"input_rows={resampled.input_rows}",
        f"output_rows={resampled.output_rows}",
        f"estimated_fs_hz={resampled.estimated_fs_hz:.3f}",
        f"output={output_path}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
