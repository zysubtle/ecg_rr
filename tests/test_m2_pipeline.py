from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

from ecg_rr_tool.pipeline import load_bidmc_csv, resample_to_50hz


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
CSV_PATH = ROOT / "data/examples/bidmc_01_Signals_2500.csv"


def _env_with_src_path() -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    src_path = str(SRC)
    env["PYTHONPATH"] = f"{src_path}{os.pathsep}{existing}" if existing else src_path
    return env


def test_load_and_resample_smoke() -> None:
    raw = load_bidmc_csv(CSV_PATH)
    resampled = resample_to_50hz(raw)

    assert len(raw.time_s) == 2500
    assert 120.0 <= resampled.estimated_fs_hz <= 130.0
    assert 990 <= resampled.output_rows <= 1010
    assert (resampled.time_s[1:] - resampled.time_s[:-1] > 0).all()


def test_cli_generates_expected_output_columns(tmp_path: Path) -> None:
    out_csv = tmp_path / "m2_resampled.csv"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ecg_rr_tool.cli",
            str(CSV_PATH),
            "--output",
            str(out_csv),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=_env_with_src_path(),
    )

    assert result.returncode == 0, result.stderr
    assert out_csv.exists()

    df = pd.read_csv(out_csv)
    assert list(df.columns) == ["sample_index_50hz", "time_s", "ecg_50hz", "ppg_50hz"]
    assert 990 <= len(df) <= 1010
