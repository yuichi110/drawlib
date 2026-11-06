# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and functional tests for drawlib.charts.box (BoxChart & BoxStats)."""

from __future__ import annotations

import math
import tempfile
from pathlib import Path

import pytest

import drawlib.charts as charts_pkg
from drawlib import canvas
from drawlib._charts.box_chart._stats import generate_jitter_offsets, percentile_inclusive
from drawlib.charts.box import Axis, BoxChart, BoxStats, Series
from drawlib.styles import Styles


class TestBoxStatsAndPercentiles:
    """Tests for inclusive percentile interpolation and BoxStats computation."""

    def test_percentile_inclusive_small_samples(self) -> None:
        assert percentile_inclusive([42.0], 25.0) == 42.0
        assert percentile_inclusive([42.0], 50.0) == 42.0
        assert percentile_inclusive([10.0, 20.0], 50.0) == 15.0
        assert percentile_inclusive([10.0, 20.0], 25.0) == 12.5
        assert percentile_inclusive([10.0, 20.0, 30.0, 40.0, 50.0], 25.0) == 20.0
        assert percentile_inclusive([10.0, 20.0, 30.0, 40.0, 50.0], 75.0) == 40.0

    def test_percentile_inclusive_errors(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            percentile_inclusive([], 50.0)
        with pytest.raises(ValueError, match="Percentile"):
            percentile_inclusive([1.0, 2.0], -1.0)
        with pytest.raises(ValueError, match="Percentile"):
            percentile_inclusive([1.0, 2.0], 101.0)

    def test_from_values_iqr_with_outliers(self) -> None:
        samples = [10.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 95.0, -30.0]
        st = BoxStats.from_values(samples, whisker_mode="iqr", iqr_k=1.5)
        assert st.q1 < st.median < st.q3
        assert st.min == 10.0
        assert st.max == 18.0
        assert sorted(st.outliers) == [-30.0, 95.0]
        assert st.mean == pytest.approx(sum(samples) / len(samples))
        assert st.points == samples

    def test_from_values_min_max_and_percentile(self) -> None:
        samples = [float(i) for i in range(1, 21)]  # 1.0 .. 20.0
        st_mm = BoxStats.from_values(samples, whisker_mode="min_max")
        assert st_mm.min == 1.0
        assert st_mm.max == 20.0
        assert st_mm.outliers == []

        st_pct = BoxStats.from_values(
            samples,
            whisker_mode="percentile",
            whisker_percentiles=(10.0, 90.0),
        )
        assert st_pct.min == pytest.approx(2.9)
        assert st_pct.max == pytest.approx(18.1)
        assert 1.0 in st_pct.outliers
        assert 20.0 in st_pct.outliers

    def test_from_values_single_and_constant(self) -> None:
        st_one = BoxStats.from_values([123.4])
        assert st_one.min == st_one.q1 == st_one.median == st_one.q3 == st_one.max == 123.4
        assert st_one.mean == 123.4
        assert st_one.outliers == []

        st_const = BoxStats.from_values([7.0, 7.0, 7.0, 7.0])
        assert st_const.min == st_const.q1 == st_const.median == st_const.q3 == st_const.max == 7.0
        assert st_const.outliers == []

    def test_box_stats_validation_errors(self) -> None:
        with pytest.raises(ValueError, match="min <= q1 <= median <= q3 <= max"):
            BoxStats(min=20.0, q1=10.0, median=15.0, q3=25.0, max=30.0)
        with pytest.raises(ValueError, match="finite"):
            BoxStats(min=1.0, q1=2.0, median=math.nan, q3=4.0, max=5.0)
        with pytest.raises(ValueError, match="finite"):
            BoxStats.from_values([1.0, math.inf, 3.0])
        with pytest.raises(ValueError, match="empty"):
            BoxStats.from_values([])


class TestDeterministicJitter:
    """Tests for deterministic, series-independent jitter offset generation."""

    def test_zero_jitter_and_single_point(self) -> None:
        assert generate_jitter_offsets(5, jitter=0.0, jitter_seed=42, series_idx=0, category_idx=0) == [0.0] * 5
        assert generate_jitter_offsets(1, jitter=0.6, jitter_seed=42, series_idx=0, category_idx=0) == [0.0]
        assert generate_jitter_offsets(0, jitter=0.6, jitter_seed=42, series_idx=0, category_idx=0) == []

    def test_reproducibility_and_bounds(self) -> None:
        offs_a = generate_jitter_offsets(20, jitter=0.5, jitter_seed=99, series_idx=1, category_idx=2)
        offs_b = generate_jitter_offsets(20, jitter=0.5, jitter_seed=99, series_idx=1, category_idx=2)
        assert offs_a == offs_b
        assert all(-0.25 <= v <= 0.25 for v in offs_a)

        offs_other = generate_jitter_offsets(20, jitter=0.5, jitter_seed=99, series_idx=0, category_idx=2)
        assert offs_other != offs_a


class TestBoxChartAPIAndRendering:
    """Tests for BoxChart public facade, validation, axes, and canvas rendering."""

    def test_lazy_package_export(self) -> None:
        assert "box" in dir(charts_pkg)
        assert charts_pkg.box.BoxChart is BoxChart

    def test_validation_errors(self) -> None:
        with pytest.raises(ValueError, match="show_box or show_points"):
            BoxChart(axis_line_style=Styles.MutedDashed, show_box=False, show_points=False)

        with pytest.raises(ValueError, match="whisker_percentiles"):
            BoxChart(axis_line_style=Styles.MutedDashed, whisker_percentiles=(90.0, 10.0))

        chart = BoxChart(axis_line_style=Styles.MutedDashed)
        with pytest.raises(ValueError, match="show_box or show_points"):
            chart.add_series("Invalid", [[1.0, 2.0]], style=Styles.Neutral, show_box=False, show_points=False)

        with pytest.raises(ValueError, match="without 'points'"):
            chart.add_series(
                "StripNoPoints",
                [BoxStats(min=1.0, q1=2.0, median=3.0, q3=4.0, max=5.0)],
                style=Styles.Neutral,
                show_box=False,
                show_points=True,
            )

    def test_axes_and_empty_slots(self) -> None:
        v_chart = BoxChart(
            axis_line_style=Styles.MutedDashed,
            categories=["A", "B", "C"],
            orientation="vertical",
        )
        assert isinstance(v_chart.value_axis, Axis)
        assert v_chart.value_axis is v_chart.y_axis
        assert v_chart.category_axis is v_chart.x_axis
        assert v_chart.get_size() == (68.0, 44.0)

        s = v_chart.add_series("S1", [[10.0, 12.0, 15.0], [], None], style=Styles.PrimaryNeutral)
        assert isinstance(s, Series)
        assert s.stats[0] is not None
        assert s.stats[1] is None
        assert s.stats[2] is None

        h_chart = BoxChart(axis_line_style=Styles.MutedDashed, orientation="horizontal")
        assert h_chart.value_axis is h_chart.x_axis
        assert h_chart.category_axis is h_chart.y_axis

    def test_render_vertical_box_strip_overlay_and_styles(self) -> None:
        canvas.setup(width=110, height=70)
        chart = BoxChart(
            axis_line_style=Styles.MutedDashed,
            categories=["Baseline", "Streaming", "Blocking"],
            width=88.0,
            height=50.0,
            show_box=True,
            show_points=True,
            show_mean=True,
            box_r=0.6,
            axis_text_style=Styles.Muted.patch(text_size=10.0),
            grid_style=Styles.MutedThin,
            value_text_style=Styles.DarkBold.patch(text_size=9.5),
            value_format="{:.0f}ms",
            background_style=Styles.Neutral,
            title="Latency Benchmark",
            title_style=Styles.BlackBold.patch(text_size=12.0),
        )
        chart.add_series(
            "Cold",
            [[120, 125, 132, 140, 210], [95, 102, 108, 115, 120], [180, 195, 205, 220, 310]],
            style=Styles.SecondaryNeutral,
        )
        chart.add_series(
            "Warm",
            [[82, 85, 88, 92, 95], [64, 68, 70, 73, 78], [110, 115, 118, 124, 130]],
            style=Styles.PrimaryFlat,
            point_shape="square",
        )
        chart.configure_y_axis(unit="ms", label="Response Time")
        chart.configure_x_axis(label="Execution Mode")
        chart.draw(xy=(10.0, 10.0))
        chart.draw_legend(xy=(24.0, 63.0), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal")

        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "box_overlay.png"
            canvas.save(str(out))
            assert out.is_file() and out.stat().st_size > 0
        canvas.clear()

    def test_render_horizontal_preaggregated_log_and_strip_only(self) -> None:
        canvas.setup(width=120, height=64)

        # Left: Horizontal BoxStats on log scale with outliers
        h_box = BoxChart(
            axis_line_style=Styles.MutedDashed,
            categories=["Gateway", "Auth", "VectorDB"],
            orientation="horizontal",
            width=52.0,
            height=46.0,
            axis_text_style=Styles.Muted.patch(text_size=10.0),
            grid_style=Styles.MutedThin,
        )
        h_box.add_series(
            "p5-p95",
            [
                BoxStats(min=8.0, q1=12.0, median=16.0, q3=25.0, max=60.0, outliers=[140.0]),
                BoxStats(min=10.0, q1=15.0, median=20.0, q3=32.0, max=85.0),
                BoxStats(min=35.0, q1=50.0, median=75.0, q3=130.0, max=450.0, outliers=[950.0]),
            ],
            style=Styles.PrimaryNeutral,
        )
        h_box.configure_x_axis(scale="log", unit="ms", label="Latency (log)")
        h_box.draw(xy=(30.0, 32.0), align="center")

        # Right: Strip-only plot with partial draw_ratio animation states
        strip = BoxChart(
            axis_line_style=Styles.MutedDashed,
            categories=["Run 1", "Run 2", "Run 3"],
            width=48.0,
            height=46.0,
            show_box=False,
            show_points=True,
            point_shape="rhombus",
            axis_text_style=Styles.Muted.patch(text_size=10.0),
        )
        s1 = strip.add_series(
            "Samples",
            [[10, 12, 14, 15], [18, 20, 21, 25], [12, 13, 15, 17]],
            style=Styles.PrimaryOutline,
            draw_ratio=0.65,
            draw_direction="left_to_right",
        )
        s2 = strip.add_series(
            "Hidden",
            [[5, 6, 7], [8, 9, 10], [6, 7, 8]],
            style=Styles.SecondaryNeutral,
            show=False,
        )
        assert not s2.show
        assert s1.draw_ratio == pytest.approx(0.65)
        strip.draw(xy=(64.0, 9.0), scale=0.95)

        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "box_horiz_and_strip.png"
            canvas.save(str(out))
            assert out.is_file() and out.stat().st_size > 0
        canvas.clear()
