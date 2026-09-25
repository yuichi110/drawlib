# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.charts (BarChart)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from drawlib import canvas
from drawlib._charts._common._axis import Axis, calculate_axis_range_and_ticks, value_to_ratio
from drawlib._charts._common._legend import get_legend_size, resolve_legend_position
from drawlib._core.l3_styles import Style
from drawlib.charts import BarChart, BarSeries


class TestAxisCalculation:
    """Unit tests for Axis calculations, Nice Numbers, and Log Scale."""

    def test_linear_nice_numbers_auto(self) -> None:
        """Test automatic linear scale range and ticks calculation."""
        axis = Axis(scale="linear")
        eff_min, eff_max, ticks = calculate_axis_range_and_ticks(axis, data_min=0.0, data_max=85.0, is_bar=True)
        assert eff_min == 0.0
        assert eff_max >= 85.0
        assert len(ticks) >= 4
        assert ticks[0] == 0.0
        assert ticks[-1] >= 85.0

    def test_linear_custom_ticks(self) -> None:
        """Test user-defined explicit ticks on linear axis."""
        axis = Axis(ticks=[0.0, 25.0, 50.0, 75.0, 100.0])
        eff_min, eff_max, ticks = calculate_axis_range_and_ticks(axis, data_min=10.0, data_max=90.0, is_bar=True)
        assert eff_min == 0.0
        assert eff_max == 100.0
        assert ticks == [0.0, 25.0, 50.0, 75.0, 100.0]

    def test_linear_tick_step(self) -> None:
        """Test user-defined tick_step on linear axis."""
        axis = Axis(tick_step=20.0, min_value=0.0, max_value=100.0)
        eff_min, eff_max, ticks = calculate_axis_range_and_ticks(axis, data_min=0.0, data_max=95.0, is_bar=True)
        assert eff_min == 0.0
        assert eff_max == 100.0
        assert ticks == [0.0, 20.0, 40.0, 60.0, 80.0, 100.0]

    def test_log_scale_range_and_ticks(self) -> None:
        """Test logarithmic scale range and ticks calculation."""
        axis = Axis(scale="log")
        eff_min, eff_max, ticks = calculate_axis_range_and_ticks(axis, data_min=5.0, data_max=5000.0)
        assert eff_min <= 5.0
        assert eff_max >= 5000.0
        # Should include powers of 10: 1, 10, 100, 1000, 10000
        assert 10.0 in ticks
        assert 100.0 in ticks
        assert 1000.0 in ticks

    def test_axis_formatting_callable(self) -> None:
        """Test formatting numbers with a callable formatter."""
        axis = Axis(format=lambda v: f"${v:,.0f}", unit="USD")
        formatted = axis.format_value(1500.0)
        assert "$1,500" in formatted

    def test_axis_formatting_string(self) -> None:
        """Test formatting numbers with a format string template."""
        axis = Axis(format="{:.1f}", unit="ms")
        formatted = axis.format_value(42.345)
        assert formatted == "42.3 ms"

    def test_value_to_ratio_linear(self) -> None:
        """Test value mapping for linear axis."""
        assert value_to_ratio(50.0, 0.0, 100.0, scale="linear") == 0.5
        assert value_to_ratio(0.0, 0.0, 100.0, scale="linear") == 0.0
        assert value_to_ratio(100.0, 0.0, 100.0, scale="linear") == 1.0

    def test_value_to_ratio_log(self) -> None:
        """Test value mapping for logarithmic axis."""
        ratio = value_to_ratio(100.0, 10.0, 1000.0, scale="log")
        assert abs(ratio - 0.5) < 1e-4


class TestLegendLayout:
    """Unit tests for automatic legend position and size resolution."""

    def test_auto_single_series(self) -> None:
        """Verify legend is omitted for single-series charts in auto mode."""
        pos = resolve_legend_position("auto", series_count=1)
        assert pos == "none"
        w_margin, h_margin = get_legend_size(pos, ["Series A"], series_count=1)
        assert w_margin == 0.0
        assert h_margin == 0.0

    def test_auto_multiple_series(self) -> None:
        """Verify legend is automatically shown at top for multi-series charts."""
        pos = resolve_legend_position("auto", series_count=2)
        assert pos == "top"
        _, h_margin = get_legend_size(pos, ["A", "B"], series_count=2)
        assert h_margin > 0.0

    def test_explicit_right_position(self) -> None:
        """Verify legend margin when placed on the right."""
        w_margin, h_margin = get_legend_size("right", ["A", "B"], series_count=2)
        assert w_margin > 0.0
        assert h_margin == 0.0


class TestBarChartModel:
    """Unit tests for BarChart configuration and series management."""

    def test_barchart_initialization(self) -> None:
        """Verify default properties of BarChart."""
        chart = BarChart(categories=["Q1", "Q2", "Q3", "Q4"], width=80.0, height=50.0)
        assert chart.categories == ["Q1", "Q2", "Q3", "Q4"]
        assert chart.width == 80.0
        assert chart.height == 50.0
        assert chart.orientation == "vertical"
        assert chart.bar_mode == "group"
        assert chart.legend_position == "auto"
        assert len(chart.series) == 0

    def test_add_series(self) -> None:
        """Verify adding series to BarChart."""
        chart = BarChart(categories=["A", "B"])
        s1 = chart.add_series("Product 1", [10.0, 20.0], color=(50, 100, 200))
        assert isinstance(s1, BarSeries)
        assert len(chart.series) == 1
        assert chart.series[0].name == "Product 1"
        assert chart.series[0].values == [10.0, 20.0]
        assert chart.series[0].color == (50, 100, 200)

    def test_configure_axes(self) -> None:
        """Verify configure_y_axis and configure_x_axis methods."""
        chart = BarChart(categories=["X", "Y"])
        chart.configure_y_axis(
            scale="log",
            min_value=1.0,
            max_value=1000.0,
            unit="ms",
            label="Latency",
            show_grid=True,
        )
        assert chart.y_axis.scale == "log"
        assert chart.y_axis.min_value == 1.0
        assert chart.y_axis.max_value == 1000.0
        assert chart.y_axis.unit == "ms"
        assert chart.y_axis.label == "Latency"
        assert chart.y_axis.show_grid is True


class TestBarChartRendering:
    """Integration tests verifying rendering and image saving."""

    def test_render_vertical_grouped_chart(self) -> None:
        """Test rendering vertical grouped bar chart to canvas and saving image."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "vertical_grouped.png"
            canvas.initialize()

            chart = BarChart(
                categories=["2021", "2022", "2023"],
                width=80,
                height=50,
                title="Revenue by Division",
                show_values=True,
            )
            chart.add_series("Hardware", [45.0, 52.0, 60.0])
            chart.add_series("Software", [30.0, 48.0, 75.0])
            chart.configure_y_axis(unit="M$", show_grid=True)
            chart.draw(xy=(10.0, 15.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_horizontal_stacked_chart(self) -> None:
        """Test rendering horizontal stacked bar chart to canvas."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "horizontal_stacked.png"
            canvas.initialize()

            chart = BarChart(
                categories=["Team Alpha", "Team Beta", "Team Gamma"],
                width=80,
                height=50,
                orientation="horizontal",
                bar_mode="stack",
                title="Task Distribution",
                show_values=True,
            )
            chart.add_series("Completed", [12.0, 18.0, 15.0])
            chart.add_series("In Progress", [8.0, 5.0, 10.0])
            chart.add_series("Pending", [4.0, 7.0, 2.0])
            chart.configure_x_axis(unit="pts")
            chart.draw(xy=(10.0, 15.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_log_scale_chart(self) -> None:
        """Test rendering bar chart with logarithmic axis."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "log_scale.png"
            canvas.initialize()

            chart = BarChart(
                categories=["Query A", "Query B", "Query C"],
                width=80,
                height=50,
                title="Database Latency (Log Scale)",
            )
            chart.add_series("Latency", [2.5, 45.0, 3200.0])
            chart.configure_y_axis(scale="log", unit="ms")
            chart.draw(xy=(10.0, 15.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_custom_styles(self) -> None:
        """Test rendering with customized bar style and border radius."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "custom_style.png"
            canvas.initialize()

            custom_style = Style(
                shape_fill_color=(100, 200, 150, 0.8),
                shape_line_color=(40, 120, 80, 1.0),
                shape_line_width=1.5,
            )
            chart = BarChart(
                categories=["Mon", "Tue", "Wed"],
                width=70,
                height=45,
                r=1.5,
            )
            chart.add_series("Visitors", [120.0, 180.0, 240.0], style=custom_style)
            chart.draw(xy=(15.0, 15.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
