# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Statistical summary model and deterministic jitter helpers for BoxChart."""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from drawlib._core.l1_core import validate_call

__all__ = [
    "BoxStats",
    "generate_jitter_offsets",
    "percentile_inclusive",
]


def _ensure_finite_float(val: object, name: str) -> float:
    """Validate and convert a scalar numeric input into a finite float."""
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise ValueError(f"{name} must be a finite number, got {val!r}.")
    f = float(val)
    if not math.isfinite(f):
        raise ValueError(f"{name} must be a finite number, got {val!r}.")
    return f


def percentile_inclusive(sorted_vals: Sequence[float], p: float) -> float:
    """Compute inclusive linear-interpolated percentile on an ascending sequence.

    Matches Python ``statistics.quantiles(..., method="inclusive")`` and
    NumPy/Pandas default ``linear`` interpolation while supporting ``N >= 1``.

    Args:
        sorted_vals: Non-empty sequence of finite floats sorted in ascending order.
        p: Percentile in the closed interval [0.0, 100.0].

    Returns:
        float: Interpolated percentile value.
    """
    if not sorted_vals:
        raise ValueError("sorted_vals must not be empty.")
    if p < 0.0 or p > 100.0 or not math.isfinite(p):
        raise ValueError(f"Percentile p must be in [0.0, 100.0], got {p!r}.")
    n = len(sorted_vals)
    if n == 1:
        return float(sorted_vals[0])
    idx = (p / 100.0) * (n - 1)
    lo = math.floor(idx)
    hi = math.ceil(idx)
    frac = idx - lo
    return float(sorted_vals[lo]) * (1.0 - frac) + float(sorted_vals[hi]) * frac


class BoxStats(BaseModel):
    """Summary statistics for a single box-plot category slot.

    Attributes:
        min: Lower whisker endpoint (e.g. minimum, 1.5*IQR fence, or p5).
        q1: First quartile (25th percentile).
        median: Median value (50th percentile).
        q3: Third quartile (75th percentile).
        max: Upper whisker endpoint (e.g. maximum, 1.5*IQR fence, or p95).
        mean: Optional arithmetic mean value.
        outliers: List of outlier values beyond the whisker endpoints.
        points: List of raw sample values for strip/jitter point rendering.
    """

    model_config = ConfigDict(extra="forbid")

    min: float
    q1: float
    median: float
    q3: float
    max: float
    mean: float | None = None
    outliers: list[float] = Field(default_factory=list)
    points: list[float] = Field(default_factory=list)

    @field_validator("min", "q1", "median", "q3", "max", mode="before")
    @classmethod
    def _validate_scalar_fields(cls, v: object, info: object) -> float:
        field_name = getattr(info, "field_name", "value")
        return _ensure_finite_float(v, str(field_name))

    @field_validator("mean", mode="before")
    @classmethod
    def _validate_mean_field(cls, v: object) -> float | None:
        if v is None:
            return None
        return _ensure_finite_float(v, "mean")

    @field_validator("outliers", "points", mode="before")
    @classmethod
    def _validate_seq_fields(cls, v: object, info: object) -> list[float]:
        if v is None:
            return []
        field_name = str(getattr(info, "field_name", "sequence"))
        if isinstance(v, (str, bytes)) or not isinstance(v, Sequence):
            raise ValueError(f"{field_name} must be a sequence of numbers.")
        return [_ensure_finite_float(item, field_name) for item in v]

    @model_validator(mode="after")
    def _validate_monotonic_order(self) -> BoxStats:
        if not (self.min <= self.q1 <= self.median <= self.q3 <= self.max):
            raise ValueError(
                "BoxStats requires min <= q1 <= median <= q3 <= max, got "
                f"min={self.min}, q1={self.q1}, median={self.median}, q3={self.q3}, max={self.max}."
            )
        return self

    @classmethod
    @validate_call
    def from_values(
        cls,
        values: Sequence[float],
        *,
        whisker_mode: Literal["iqr", "min_max", "percentile"] = "iqr",
        iqr_k: float = 1.5,
        whisker_percentiles: tuple[float, float] = (5.0, 95.0),
    ) -> BoxStats:
        """Compute BoxStats from a non-empty sequence of raw numerical samples.

        Args:
            values: Non-empty sequence of finite float samples.
            whisker_mode: Whisker calculation rule ("iqr", "min_max", or "percentile").
                Defaults to "iqr".
            iqr_k: Multiplier applied to IQR when ``whisker_mode="iqr"``. Defaults to 1.5.
            whisker_percentiles: ``(low_p, high_p)`` percentiles in [0.0, 100.0] used when
                ``whisker_mode="percentile"``. Defaults to ``(5.0, 95.0)``.

        Returns:
            BoxStats: Computed five-number summary, mean, outliers, and raw points.

        Raises:
            ValueError: If ``values`` is empty, contains non-finite numbers, or parameters
                are out of valid bounds.
        """
        if not values:
            raise ValueError("values must not be empty.")
        k = _ensure_finite_float(iqr_k, "iqr_k")
        if k < 0.0:
            raise ValueError(f"iqr_k must be >= 0.0, got {k}.")

        low_p = _ensure_finite_float(whisker_percentiles[0], "whisker_percentiles[0]")
        high_p = _ensure_finite_float(whisker_percentiles[1], "whisker_percentiles[1]")
        if not (0.0 <= low_p < high_p <= 100.0):
            raise ValueError(
                f"whisker_percentiles must satisfy 0.0 <= low < high <= 100.0, got ({low_p}, {high_p})."
            )

        raw_points = [_ensure_finite_float(v, "value") for v in values]
        sorted_vals = sorted(raw_points)

        q1 = percentile_inclusive(sorted_vals, 25.0)
        median = percentile_inclusive(sorted_vals, 50.0)
        q3 = percentile_inclusive(sorted_vals, 75.0)
        mean_val = sum(sorted_vals) / len(sorted_vals)

        if whisker_mode == "min_max":
            w_min = sorted_vals[0]
            w_max = sorted_vals[-1]
            outliers: list[float] = []
        elif whisker_mode == "iqr":
            iqr = q3 - q1
            low_fence = q1 - k * iqr
            high_fence = q3 + k * iqr
            inliers_low = [v for v in sorted_vals if v >= low_fence]
            inliers_high = [v for v in sorted_vals if v <= high_fence]
            w_min = min(q1, inliers_low[0]) if inliers_low else q1
            w_max = max(q3, inliers_high[-1]) if inliers_high else q3
            outliers = [v for v in sorted_vals if v < w_min or v > w_max]
        else:
            p_low = percentile_inclusive(sorted_vals, low_p)
            p_high = percentile_inclusive(sorted_vals, high_p)
            w_min = min(q1, p_low)
            w_max = max(q3, p_high)
            outliers = [v for v in sorted_vals if v < w_min or v > w_max]

        return cls(
            min=w_min,
            q1=q1,
            median=median,
            q3=q3,
            max=w_max,
            mean=mean_val,
            outliers=outliers,
            points=raw_points,
        )

    def extent_values(
        self,
        *,
        show_box: bool,
        show_points: bool,
        show_outliers: bool,
        show_mean: bool,
    ) -> list[float]:
        """Collect all numerical values contributing to axis domain scaling."""
        vals: list[float] = []
        if show_box:
            vals.extend([self.min, self.q1, self.median, self.q3, self.max])
            if show_outliers and not show_points:
                vals.extend(self.outliers)
        if show_points:
            vals.extend(self.points)
        if show_mean and self.mean is not None:
            vals.append(self.mean)
        if not vals:
            vals.append(self.median)
        return vals


def generate_jitter_offsets(
    count: int,
    *,
    jitter: float,
    jitter_seed: int,
    series_idx: int,
    category_idx: int,
) -> list[float]:
    """Generate deterministic normalized jitter offsets in ``[-0.5 * jitter, +0.5 * jitter]``.

    Uses fixed 32-bit prime mixing per ``(jitter_seed, series_idx, category_idx)``
    with a local ``random.Random`` instance so point coordinates are 100% invariant
    across processes and unaffected by hiding other series during animations.

    Args:
        count: Number of points in the slot.
        jitter: Normalized jitter spread width in [0.0, 1.0].
        jitter_seed: Base deterministic integer seed.
        series_idx: Zero-based series index.
        category_idx: Zero-based category index.

    Returns:
        list[float]: Normalized transverse offsets relative to individual box width.
    """
    if count <= 0:
        return []
    if jitter <= 0.0 or count == 1:
        return [0.0] * count

    s0 = (int(jitter_seed) & 0xFFFFFFFF) * 2654435761
    s1 = ((int(series_idx) + 1) & 0xFFFFFFFF) * 2246822519
    s2 = ((int(category_idx) + 1) & 0xFFFFFFFF) * 3266489917
    mixed_seed = (s0 ^ s1 ^ s2) & 0xFFFFFFFF

    rng = random.Random(mixed_seed)  # noqa: S311
    half = 0.5 * float(jitter)
    return [rng.uniform(-half, half) for _ in range(count)]
