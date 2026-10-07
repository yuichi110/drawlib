# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for LineChart and AreaChart."""

from __future__ import annotations

import tempfile
from pathlib import Path

from drawlib import canvas
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib.charts.area import AreaChart
from drawlib.charts.area import Series as AreaSeries
from drawlib.charts.line import LineChart
from drawlib.charts.line import Series as LineSeries

_DEFAULT_AXIS_LINE = Style(line_color=(148, 163, 184, 1.0), line_width=1.0)
_DEFAULT_TEXT = Style(text_size=10.0, text_color=(30, 41, 59, 1.0), text_font=Font.SANSSERIF_REGULAR)
_DEFAULT_GRID = Style(line_color=(226, 232, 240, 1.0), line_width=0.8, line_style="dashed")


class TestLineChartModel:
    """Unit tests for LineChart configuration and series management."""

    def test_line_chart_initialization(self) -> None:
        """Verify default properties of LineChart."""
        chart = LineChart(axis_line_style=_DEFAULT_AXIS_LINE, categories=["Jan", "Feb", "Mar"], width=75.0, height=45.0)
        assert chart.categories == ["Jan", "Feb", "Mar"]
        assert chart.width == 75.0
        assert chart.height == 45.0
        assert chart.show_points is True
        assert chart.point_shape == "circle"
        assert chart.smooth is False
        assert len(chart.series) == 0

    def test_add_series(self) -> None:
        """Verify adding LineSeries to LineChart."""
        chart = LineChart(axis_line_style=_DEFAULT_AXIS_LINE, categories=["A", "B", "C"])
        style = Style(line_color=(50, 100, 200, 1.0), line_width=2.5)
        s1 = chart.add_series("Series 1", [10.0, 25.0, 40.0], style=style, line_width=2.5, line_style="dashed")
        assert isinstance(s1, LineSeries)
        assert len(chart.series) == 1
        assert chart.series[0].name == "Series 1"
        assert chart.series[0].values == [10.0, 25.0, 40.0]
        assert chart.series[0].line_width == 2.5
        assert chart.series[0].line_style == "dashed"
        assert chart.series[0].point_shape == "circle"


class TestAreaChartModel:
    """Unit tests for AreaChart configuration and series management."""

    def test_area_chart_initialization(self) -> None:
        """Verify default properties of AreaChart."""
        chart = AreaChart(
            axis_line_style=_DEFAULT_AXIS_LINE, categories=["Q1", "Q2"], width=70.0, height=40.0, mode="stack"
        )
        assert chart.categories == ["Q1", "Q2"]
        assert chart.width == 70.0
        assert chart.height == 40.0
        assert chart.mode == "stack"
        assert chart.fill_alpha == 0.35
        assert len(chart.series) == 0

    def test_add_series(self) -> None:
        """Verify adding AreaSeries to AreaChart."""
        chart = AreaChart(axis_line_style=_DEFAULT_AXIS_LINE, categories=["X", "Y"])
        style = Style(shape_fill_color=(50, 100, 200, 1.0), shape_line_color=(0, 0, 0, 0.0), shape_line_width=0.0)
        s = chart.add_series("Bandwidth", [100.0, 200.0], style=style, fill_alpha=0.5)
        assert isinstance(s, AreaSeries)
        assert len(chart.series) == 1
        assert chart.series[0].name == "Bandwidth"
        assert chart.series[0].values == [100.0, 200.0]
        assert chart.series[0].fill_alpha == 0.5


class TestLineAndAreaRendering:
    """Integration tests verifying rendering and image saving."""

    def test_render_line_chart_straight(self) -> None:
        """Test rendering straight multi-series line chart."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "line_straight.png"
            canvas.clear()

            chart = LineChart(
                axis_line_style=_DEFAULT_AXIS_LINE,
                axis_text_style=_DEFAULT_TEXT,
                grid_style=_DEFAULT_GRID,
                value_text_style=_DEFAULT_TEXT,
                categories=["2020", "2021", "2022", "2023"],
                width=80.0,
                height=50.0,
                title="Annual Metric Trends",
                title_style=_DEFAULT_TEXT,
                show_points=True,
            )
            chart.add_series(
                "Project A", [12.0, 18.0, 29.0, 45.0], style=Style(line_color=(50, 100, 200, 1.0), line_width=2.0)
            )
            chart.add_series(
                "Project B",
                [20.0, 22.0, 25.0, 28.0],
                style=Style(line_color=(200, 100, 50, 1.0), line_width=2.0),
                line_style="dashed",
            )
            chart.configure_y_axis(unit="k", show_grid=True)
            chart.draw(xy=(10.0, 20.0))
            chart.draw_legend(xy=(10.0, 75.0), text_style=_DEFAULT_TEXT, orientation="horizontal")

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_line_chart_smooth(self) -> None:
        """Test rendering smooth curved line chart."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "line_smooth.png"
            canvas.clear()

            chart = LineChart(
                axis_line_style=_DEFAULT_AXIS_LINE,
                axis_text_style=_DEFAULT_TEXT,
                grid_style=_DEFAULT_GRID,
                categories=["Mon", "Tue", "Wed", "Thu", "Fri"],
                width=80.0,
                height=50.0,
                title="Server CPU Utilization",
                title_style=_DEFAULT_TEXT,
                smooth=True,
                point_shape="square",
            )
            chart.add_series(
                "Core 0", [25.0, 45.0, 30.0, 70.0, 55.0], style=Style(line_color=(50, 100, 200, 1.0), line_width=2.0)
            )
            chart.configure_y_axis(unit="%", show_grid=True)
            chart.draw(xy=(10.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_area_chart_overlap(self) -> None:
        """Test rendering overlapping semi-transparent area chart."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "area_overlap.png"
            canvas.clear()

            chart = AreaChart(
                axis_line_style=_DEFAULT_AXIS_LINE,
                axis_text_style=_DEFAULT_TEXT,
                grid_style=_DEFAULT_GRID,
                categories=["00h", "06h", "12h", "18h"],
                width=80.0,
                height=50.0,
                title="Traffic In/Out",
                title_style=_DEFAULT_TEXT,
                mode="overlap",
                fill_alpha=0.3,
            )
            chart.add_series(
                "Inbound",
                [100.0, 350.0, 800.0, 450.0],
                style=Style(
                    shape_fill_color=(50, 100, 200, 1.0), shape_line_color=(0, 0, 0, 0.0), shape_line_width=0.0
                ),
            )
            chart.add_series(
                "Outbound",
                [80.0, 200.0, 520.0, 310.0],
                style=Style(
                    shape_fill_color=(200, 100, 50, 1.0), shape_line_color=(0, 0, 0, 0.0), shape_line_width=0.0
                ),
            )
            chart.configure_y_axis(unit="MB/s", show_grid=True)
            chart.draw(xy=(10.0, 20.0))
            chart.draw_legend(xy=(10.0, 75.0), text_style=_DEFAULT_TEXT, orientation="horizontal")

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_area_chart_stack(self) -> None:
        """Test rendering cumulative stacked area chart."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "area_stack.png"
            canvas.clear()

            chart = AreaChart(
                axis_line_style=_DEFAULT_AXIS_LINE,
                axis_text_style=_DEFAULT_TEXT,
                grid_style=_DEFAULT_GRID,
                categories=["Q1", "Q2", "Q3", "Q4"],
                width=80.0,
                height=50.0,
                title="Cumulative Revenue Streams",
                title_style=_DEFAULT_TEXT,
                mode="stack",
                fill_alpha=0.6,
            )
            chart.add_series(
                "Subscription",
                [30.0, 45.0, 60.0, 80.0],
                style=Style(
                    shape_fill_color=(50, 100, 200, 1.0), shape_line_color=(0, 0, 0, 0.0), shape_line_width=0.0
                ),
            )
            chart.add_series(
                "Services",
                [20.0, 25.0, 30.0, 35.0],
                style=Style(
                    shape_fill_color=(100, 150, 250, 1.0), shape_line_color=(0, 0, 0, 0.0), shape_line_width=0.0
                ),
            )
            chart.add_series(
                "Hardware",
                [15.0, 12.0, 10.0, 8.0],
                style=Style(
                    shape_fill_color=(200, 100, 50, 1.0), shape_line_color=(0, 0, 0, 0.0), shape_line_width=0.0
                ),
            )
            chart.configure_y_axis(unit="M$", show_grid=True)
            chart.draw(xy=(10.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_custom_styles(self) -> None:
        """Test LineChart with customized Style object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "custom_style.png"
            canvas.clear()

            custom_style = Style(line_color=(220, 38, 38, 1.0), line_width=3.0)
            chart = LineChart(
                axis_line_style=_DEFAULT_AXIS_LINE,
                categories=["Low", "Medium", "High"],
                width=70.0,
                height=45.0,
            )
            chart.add_series("Alerts", [5.0, 18.0, 42.0], style=custom_style)
            chart.draw(xy=(15.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_lifecycle_and_spatial_overrides(self) -> None:
        """Test LineChart and AreaChart show, draw_ratio, draw_direction, and spatial overrides."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "line_area_lifecycle.png"
            canvas.clear()

            line_chart = LineChart(
                axis_line_style=_DEFAULT_AXIS_LINE,
                categories=["Jan", "Feb", "Mar", "Apr"],
                width=70.0,
                height=45.0,
            )
            l_style = Style(line_color=(50, 100, 200, 1.0), line_width=2.0)
            s1 = line_chart.add_series("A", [10.0, 30.0, 20.0, 40.0], style=l_style, draw_ratio=0.55)
            s2 = line_chart.add_series(
                "B",
                [15.0, 25.0, 35.0, 45.0],
                style=l_style,
                draw_ratio=0.5,
                draw_direction="bottom_to_top",
            )
            line_chart.add_series("Hidden", [50.0, 60.0, 70.0, 80.0], style=l_style, show=False)
            assert s1.draw_direction == "left_to_right"
            assert s2.draw_direction == "bottom_to_top"

            line_chart.draw(xy=(5.0, 10.0), width=40.0, height=35.0, scale=0.9)
            assert line_chart.get_size() == (70.0, 45.0)

            area_chart = AreaChart(
                axis_line_style=_DEFAULT_AXIS_LINE,
                categories=["Q1", "Q2", "Q3", "Q4"],
                width=70.0,
                height=45.0,
                mode="stack",
            )
            a_style = Style(shape_fill_color=(50, 100, 200, 1.0))
            area_chart.add_series("S1", [10.0, 20.0, 30.0, 40.0], style=a_style, draw_ratio=0.65)
            area_chart.add_series(
                "S2",
                [10.0, 15.0, 20.0, 25.0],
                style=a_style,
                draw_ratio=0.5,
                draw_direction="bottom_to_top",
            )
            area_chart.draw(xy=(50.0, 10.0), width=40.0, height=35.0, scale=0.9)
            assert area_chart.get_size() == (70.0, 45.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
