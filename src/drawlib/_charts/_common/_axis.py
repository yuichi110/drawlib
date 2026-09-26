# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Axis model and scaling engine for charts."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from drawlib._charts._common._types import FormatterType, ScaleType

if TYPE_CHECKING:
    from drawlib._core.types import Style


class Axis:
    """Represents a coordinate axis (value axis or category axis) of a chart."""

    def __init__(
        self,
        scale: ScaleType = "linear",
        min_value: float | None = None,
        max_value: float | None = None,
        ticks: list[float] | None = None,
        tick_step: float | None = None,
        format: FormatterType = None,  # noqa: A002
        unit: str = "",
        label: str = "",
        show_grid: bool = True,
        grid_style: Style | None = None,
        show_axis_line: bool = True,
        line_style: Style | None = None,
        show_ticks: bool = True,
        tick_label_style: Style | None = None,
        tick_label_angle: float = 0.0,
    ) -> None:
        """Initialize Axis.

        Args:
            scale: Scaling type ("linear" or "log"). Defaults to "linear".
            min_value: Explicit minimum axis value.
            max_value: Explicit maximum axis value.
            ticks: Explicit list of tick values.
            tick_step: Explicit step size between ticks.
            format: Formatter string (e.g. "{:g}") or formatting function.
            unit: Axis unit label or suffix (e.g. "ms", "$").
            label: Descriptive axis title.
            show_grid: Whether to render gridlines along ticks. Defaults to True.
            grid_style: Optional Style for gridlines.
            show_axis_line: Whether to render the baseline axis stroke. Defaults to True.
            line_style: Optional Style for the baseline stroke.
            show_ticks: Whether to render tick labels. Defaults to True.
            tick_label_style: Optional Style for tick label typography.
            tick_label_angle: Rotation angle in degrees for tick labels. Defaults to 0.0.
        """
        self.scale: ScaleType = scale
        self.min_value: float | None = float(min_value) if min_value is not None else None
        self.max_value: float | None = float(max_value) if max_value is not None else None
        self.ticks: list[float] | None = [float(t) for t in ticks] if ticks is not None else None
        self.tick_step: float | None = float(tick_step) if tick_step is not None else None
        self.format: FormatterType = format
        self.unit: str = unit
        self.label: str = label
        self.show_grid: bool = show_grid
        self.grid_style: Style | None = grid_style
        self.show_axis_line: bool = show_axis_line
        self.line_style: Style | None = line_style
        self.show_ticks: bool = show_ticks
        self.tick_label_style: Style | None = tick_label_style
        self.tick_label_angle: float = float(tick_label_angle)

    def configure(
        self,
        scale: ScaleType | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
        ticks: list[float] | None = None,
        tick_step: float | None = None,
        format: FormatterType = None,  # noqa: A002
        unit: str | None = None,
        label: str | None = None,
        show_grid: bool | None = None,
        grid_style: Style | None = None,
        show_axis_line: bool | None = None,
        line_style: Style | None = None,
        show_ticks: bool | None = None,
        tick_label_style: Style | None = None,
        tick_label_angle: float | None = None,
    ) -> None:
        """Update multiple axis configuration options in place.

        Args:
            scale: Scaling type ("linear" or "log").
            min_value: Explicit minimum value.
            max_value: Explicit maximum value.
            ticks: Explicit list of tick values.
            tick_step: Explicit step size between ticks.
            format: Formatter string or formatting function.
            unit: Axis unit label.
            label: Descriptive axis title.
            show_grid: Whether to render gridlines.
            grid_style: Optional Style for gridlines.
            show_axis_line: Whether to render baseline stroke.
            line_style: Optional Style for baseline stroke.
            show_ticks: Whether to render tick labels.
            tick_label_style: Optional Style for tick label typography.
            tick_label_angle: Rotation angle in degrees for tick labels.
        """
        opts: dict[str, object] = {
            "scale": scale,
            "min_value": float(min_value) if min_value is not None else None,
            "max_value": float(max_value) if max_value is not None else None,
            "ticks": [float(t) for t in ticks] if ticks is not None else None,
            "tick_step": float(tick_step) if tick_step is not None else None,
            "format": format,
            "unit": unit,
            "label": label,
            "show_grid": show_grid,
            "grid_style": grid_style,
            "show_axis_line": show_axis_line,
            "line_style": line_style,
            "show_ticks": show_ticks,
            "tick_label_style": tick_label_style,
            "tick_label_angle": float(tick_label_angle) if tick_label_angle is not None else None,
        }
        for k, v in opts.items():
            if v is not None:
                setattr(self, k, v)

    def format_value(self, value: float) -> str:
        """Format a numeric value into a display label string.

        Args:
            value: Float value to format.

        Returns:
            Formatted string representation.
        """
        if isinstance(self.format, str):
            try:
                formatted = self.format.format(value)
            except Exception:
                formatted = f"{value:g}"
        elif callable(self.format):
            return str(self.format(value))
        elif abs(value - round(value)) < 1e-6:
            formatted = f"{int(round(value))}"
        else:
            formatted = f"{value:g}"

        if self.unit and self.unit not in formatted:
            return f"{formatted} {self.unit}".strip()
        return formatted


def calculate_axis_range_and_ticks(
    axis: Axis,
    data_min: float,
    data_max: float,
    is_bar: bool = True,
) -> tuple[float, float, list[float]]:
    """Calculate effective min, max, and tick values for an axis.

    Args:
        axis: Axis configuration.
        data_min: Minimum data value present in series.
        data_max: Maximum data value present in series.
        is_bar: True if chart is a bar chart (anchors base at 0 for linear scale).

    Returns:
        Tuple of (effective_min, effective_max, list_of_ticks).
    """
    if axis.scale == "log":
        return _calculate_log_range_and_ticks(axis, data_min, data_max)
    return _calculate_linear_range_and_ticks(axis, data_min, data_max, is_bar)


def _get_nice_step(span: float, target_ticks: int = 5) -> float:
    """Calculate human-friendly step using the Nice Numbers algorithm."""
    raw_step = span / target_ticks
    exponent = math.floor(math.log10(raw_step))
    fraction = raw_step / (10**exponent)

    if fraction < 1.5:
        nice_fraction = 1.0
    elif fraction < 3.0:
        nice_fraction = 2.0
    elif fraction < 7.0:
        nice_fraction = 5.0
    else:
        nice_fraction = 10.0

    return nice_fraction * (10**exponent)


def _build_stepped_ticks(eff_min: float, eff_max: float, step: float) -> list[float]:
    """Generate rounded ticks between eff_min and eff_max spaced by step."""
    ticks: list[float] = []
    cur = math.floor(eff_min / step) * step
    while cur <= eff_max + 1e-6:
        if cur >= eff_min - 1e-6:
            ticks.append(round(cur, 8))
        cur += step
    return ticks


def _calculate_linear_range_and_ticks(
    axis: Axis,
    data_min: float,
    data_max: float,
    is_bar: bool,
) -> tuple[float, float, list[float]]:
    """Calculate range and ticks for linear scale using Nice Numbers."""
    # User-specified explicit ticks take highest precedence
    if axis.ticks is not None and len(axis.ticks) >= 2:
        sorted_ticks = sorted(axis.ticks)
        eff_min = axis.min_value if axis.min_value is not None else sorted_ticks[0]
        eff_max = axis.max_value if axis.max_value is not None else sorted_ticks[-1]
        return (eff_min, eff_max, sorted_ticks)

    # Determine base min and max
    if axis.min_value is not None:
        eff_min = axis.min_value
    elif is_bar and data_min >= 0:
        eff_min = 0.0
    else:
        eff_min = data_min

    eff_max = axis.max_value if axis.max_value is not None else (data_max if data_max > eff_min else eff_min + 10.0)
    span = max(10.0, eff_max - eff_min) if (eff_max - eff_min) <= 1e-6 else eff_max - eff_min

    if axis.tick_step is not None and axis.tick_step > 0:
        ticks = _build_stepped_ticks(eff_min, eff_max, axis.tick_step)
        if axis.max_value is None and ticks:
            eff_max = max(eff_max, ticks[-1])
        return (eff_min, eff_max, ticks)

    step = _get_nice_step(span, target_ticks=5)
    if axis.min_value is None:
        eff_min = math.floor(eff_min / step) * step
    if axis.max_value is None:
        eff_max = math.ceil(eff_max / step) * step

    ticks = _build_stepped_ticks(eff_min, eff_max, step)
    return (eff_min, eff_max, ticks)


def _calculate_log_range_and_ticks(
    axis: Axis,
    data_min: float,
    data_max: float,
) -> tuple[float, float, list[float]]:
    """Calculate range and ticks for logarithmic (log10) scale."""
    if axis.ticks is not None and len(axis.ticks) >= 2:
        sorted_ticks = sorted(axis.ticks)
        eff_min = axis.min_value if axis.min_value is not None else sorted_ticks[0]
        eff_max = axis.max_value if axis.max_value is not None else sorted_ticks[-1]
        return (max(1e-6, eff_min), max(eff_min * 1.1, eff_max), sorted_ticks)

    safe_data_min = max(1e-6, data_min if data_min > 0 else 1.0)
    safe_data_max = max(safe_data_min * 1.1, data_max if data_max > 0 else 10.0)

    eff_min = axis.min_value if axis.min_value is not None and axis.min_value > 0 else safe_data_min
    eff_max = axis.max_value if axis.max_value is not None and axis.max_value > eff_min else safe_data_max

    # Align to power of 10
    min_exp = math.floor(math.log10(eff_min))
    max_exp = math.ceil(math.log10(eff_max))

    if axis.min_value is None:
        eff_min = 10**min_exp
    if axis.max_value is None:
        eff_max = 10**max_exp

    ticks: list[float] = []
    order_diff = max_exp - min_exp

    if order_diff <= 2:
        # Dense ticks: 1, 2, 5 * 10^k
        for exp in range(min_exp, max_exp + 1):
            for mult in (1.0, 2.0, 5.0):
                val = mult * (10**exp)
                if eff_min - 1e-6 <= val <= eff_max + 1e-6:
                    ticks.append(round(val, 8))
    else:
        # Standard power of 10 ticks
        for exp in range(min_exp, max_exp + 1):
            val = float(10**exp)
            if eff_min - 1e-6 <= val <= eff_max + 1e-6:
                ticks.append(round(val, 8))

    return (eff_min, eff_max, ticks)


def value_to_ratio(value: float, min_val: float, max_val: float, scale: ScaleType = "linear") -> float:
    """Map a data value to normalized 0.0 - 1.0 plotting ratio.

    Args:
        value: Data value.
        min_val: Minimum axis value.
        max_val: Maximum axis value.
        scale: "linear" or "log".

    Returns:
        Normalized ratio in [0.0, 1.0].
    """
    if scale == "log":
        safe_min = max(1e-6, min_val)
        safe_max = max(safe_min * 1.0001, max_val)
        safe_v = max(safe_min, value)
        log_min = math.log10(safe_min)
        log_max = math.log10(safe_max)
        log_v = math.log10(safe_v)
        return max(0.0, min(1.0, (log_v - log_min) / (log_max - log_min)))

    span = max_val - min_val
    if span <= 1e-6:
        return 0.0
    return max(0.0, min(1.0, (value - min_val) / span))
