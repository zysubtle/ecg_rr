from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import resample_poly


class PipelineError(ValueError):
    """Raised when input data does not satisfy pipeline requirements."""


@dataclass(frozen=True)
class RawSignals:
    time_s: np.ndarray
    ecg_raw: np.ndarray
    ppg_raw: np.ndarray


@dataclass(frozen=True)
class ResampledSignals:
    sample_index_50hz: np.ndarray
    time_s: np.ndarray
    ecg_50hz: np.ndarray
    ppg_50hz: np.ndarray
    input_rows: int
    output_rows: int
    estimated_fs_hz: float


def _normalize_and_validate_columns(df: pd.DataFrame) -> dict[str, str]:
    normalized_to_original: dict[str, str] = {}
    for col in df.columns:
        normalized = col.strip()
        if normalized in normalized_to_original:
            other = normalized_to_original[normalized]
            raise PipelineError(
                f"Duplicate columns after strip normalization: {other!r}, {col!r} -> {normalized!r}"
            )
        normalized_to_original[normalized] = col

    required = ["Time [s]", "II", "PLETH"]
    missing = [name for name in required if name not in normalized_to_original]
    if missing:
        raise PipelineError(f"Missing required columns after strip normalization: {missing}")

    return normalized_to_original


def load_bidmc_csv(csv_path: str | Path) -> RawSignals:
    df = pd.read_csv(csv_path)
    columns = _normalize_and_validate_columns(df)

    time_s = df[columns["Time [s]"]].to_numpy(dtype=float)
    ecg_raw = df[columns["II"]].to_numpy(dtype=float)
    ppg_raw = df[columns["PLETH"]].to_numpy(dtype=float)

    if not (len(time_s) == len(ecg_raw) == len(ppg_raw)):
        raise PipelineError("Input columns have inconsistent lengths")

    if len(time_s) < 2:
        raise PipelineError("Input data must contain at least two samples")

    if np.any(np.diff(time_s) <= 0):
        raise PipelineError("Time [s] must be strictly monotonically increasing")

    return RawSignals(time_s=time_s, ecg_raw=ecg_raw, ppg_raw=ppg_raw)


def estimate_sampling_rate_hz(time_s: np.ndarray) -> float:
    dt = np.diff(time_s)
    median_dt = float(np.median(dt))
    if median_dt <= 0:
        raise PipelineError("Invalid timestamp delta; cannot estimate sampling rate")
    return 1.0 / median_dt


def resample_to_50hz(raw: RawSignals) -> ResampledSignals:
    fs_est = estimate_sampling_rate_hz(raw.time_s)
    if abs(fs_est - 125.0) > 5.0:
        raise PipelineError(
            f"Estimated sampling rate {fs_est:.3f} Hz is outside expected 125±5 Hz"
        )

    ecg_50hz = resample_poly(raw.ecg_raw, up=2, down=5)
    ppg_50hz = resample_poly(raw.ppg_raw, up=2, down=5)

    out_len = min(len(ecg_50hz), len(ppg_50hz))
    ecg_50hz = ecg_50hz[:out_len]
    ppg_50hz = ppg_50hz[:out_len]

    time_start = float(raw.time_s[0])
    time_50hz = time_start + np.arange(out_len, dtype=float) * 0.02

    return ResampledSignals(
        sample_index_50hz=np.arange(out_len, dtype=int),
        time_s=time_50hz,
        ecg_50hz=ecg_50hz,
        ppg_50hz=ppg_50hz,
        input_rows=len(raw.time_s),
        output_rows=out_len,
        estimated_fs_hz=fs_est,
    )


def save_resampled_csv(resampled: ResampledSignals, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(
        {
            "sample_index_50hz": resampled.sample_index_50hz,
            "time_s": resampled.time_s,
            "ecg_50hz": resampled.ecg_50hz,
            "ppg_50hz": resampled.ppg_50hz,
        }
    )
    df.to_csv(output, index=False)
    return output
