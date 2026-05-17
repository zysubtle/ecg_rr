from __future__ import annotations

import csv
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def _env_with_src_path() -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    src_path = str(SRC)
    env["PYTHONPATH"] = (
        f"{src_path}{os.pathsep}{existing}" if existing else src_path
    )
    return env


def test_required_project_files_exist() -> None:
    required = [
        "README.md",
        "AGENTS.md",
        "docs/00_PROJECT_BRIEF.md",
        "docs/01_DECISION_LOG.md",
        "docs/02_MILESTONE_PLAN.md",
        "docs/03_ALGORITHM_SCOPE.md",
        "docs/04_IO_CONTRACT.md",
        "docs/09_CODEX_RUNBOOK.md",
        "docs/10_CODEX_NEXT_TASK.md",
        "data/examples/bidmc_01_Signals_2500.csv",
        "pyproject.toml",
        "src/ecg_rr_tool/__init__.py",
        "src/ecg_rr_tool/cli.py",
        "src/ecg_rr_tool/gui.py",
    ]

    missing = [path for path in required if not (ROOT / path).exists()]
    assert not missing, f"Missing required project files: {missing}"


def test_example_csv_has_required_columns_after_strip() -> None:
    csv_path = ROOT / "data/examples/bidmc_01_Signals_2500.csv"
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)

    normalized = {col.strip() for col in header}
    assert "Time [s]" in normalized
    assert "II" in normalized
    assert "PLETH" in normalized


def test_cli_help_runs() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ecg_rr_tool.cli", "--help"],
        cwd=ROOT,
        env=_env_with_src_path(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "ECG RR preprocessing pipeline" in result.stdout


def test_gui_help_runs() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ecg_rr_tool.gui", "--help"],
        cwd=ROOT,
        env=_env_with_src_path(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "GUI placeholder" in result.stdout
