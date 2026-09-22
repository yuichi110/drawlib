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
from drawlib._core.l3_styles import Style
from drawlib.charts import AreaChart, AreaSeries, LineChart, LineSeries


class TestLineChartModel:
    """Unit tests for LineChart configuration and series management."""

    def test_line_chart_initialization(self) -> None:
        """Verify default properties of LineChart."""
        chart = LineChart(categories=["Jan", "Feb", "Mar"], width=75.0, height=45.0)
        assert chart.categories == ["Jan", "Feb", "Mar"]
        assert chart.width == 75.0
        assert chart.height == 45.0
        assert chart.show_points is True
        assert chart.point_shape == "circle"
        assert chart.smooth is False
        assert len(chart.series) == 0

    def test_add_series(self) -> None:
        """Verify adding LineSeries to LineChart."""
        chart = LineChart(categories=["A", "B", "C"])
        s1 = chart.add_series("Series 1", [10.0, 25.0, 40.0], line_width=2.5, line_style="dashed")
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
        chart = AreaChart(categories=["Q1", "Q2"], width=70.0, height=40.0, mode="stack")
        assert chart.categories == ["Q1", "Q2"]
        assert chart.width == 70.0
        assert chart.height == 40.0
        assert chart.mode == "stack"
        assert chart.fill_alpha == 0.35
        assert len(chart.series) == 0

    def test_add_series(self) -> None:
        """Verify adding AreaSeries to AreaChart."""
        chart = AreaChart(categories=["X", "Y"])
        s = chart.add_series("Bandwidth", [100.0, 200.0], fill_alpha=0.5)
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
            canvas.initialize()

            chart = LineChart(
                categories=["2020", "2021", "2022", "2023"],
                width=80.0,
                height=50.0,
                title="Annual Metric Trends",
                show_points=True,
                show_values=True,
            )
            chart.add_series("Project A", [12.0, 18.0, 29.0, 45.0])
            chart.add_series("Project B", [20.0, 22.0, 25.0, 28.0], line_style="dashed")
            chart.configure_y_axis(unit="k", show_grid=True)
            chart.draw(xy=(10.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_line_chart_smooth(self) -> None:
        """Test rendering smooth curved line chart."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "line_smooth.png"
            canvas.initialize()

            chart = LineChart(
                categories=["Mon", "Tue", "Wed", "Thu", "Fri"],
                width=80.0,
                height=50.0,
                title="Server CPU Utilization",
                smooth=True,
                point_shape="square",
            )
            chart.add_series("Core 0", [25.0, 45.0, 30.0, 70.0, 55.0])
            chart.configure_y_axis(unit="%", show_grid=True)
            chart.draw(xy=(10.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_area_chart_overlap(self) -> None:
        """Test rendering overlapping semi-transparent area chart."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "area_overlap.png"
            canvas.initialize()

            chart = AreaChart(
                categories=["00h", "06h", "12h", "18h"],
                width=80.0,
                height=50.0,
                title="Traffic In/Out",
                mode="overlap",
                fill_alpha=0.3,
            )
            chart.add_series("Inbound", [100.0, 350.0, 800.0, 450.0])
            chart.add_series("Outbound", [80.0, 200.0, 520.0, 310.0])
            chart.configure_y_axis(unit="MB/s", show_grid=True)
            chart.draw(xy=(10.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_area_chart_stack(self) -> None:
        """Test rendering cumulative stacked area chart."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "area_stack.png"
            canvas.initialize()

            chart = AreaChart(
                categories=["Q1", "Q2", "Q3", "Q4"],
                width=80.0,
                height=50.0,
                title="Cumulative Revenue Streams",
                mode="stack",
                fill_alpha=0.6,
            )
            chart.add_series("Subscription", [30.0, 45.0, 60.0, 80.0])
            chart.add_series("Services", [20.0, 25.0, 30.0, 35.0])
            chart.add_series("Hardware", [15.0, 12.0, 10.0, 8.0])
            chart.configure_y_axis(unit="M$", show_grid=True)
            chart.draw(xy=(10.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_custom_styles(self) -> None:
        """Test LineChart with customized Style object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "custom_style.png"
            canvas.initialize()

            custom_style = Style(line_color=(220, 38, 38, 1.0), line_width=3.0)
            chart = LineChart(
                categories=["Low", "Medium", "High"],
                width=70.0,
                height=45.0,
            )
            chart.add_series("Alerts", [5.0, 18.0, 42.0], style=custom_style)
            chart.draw(xy=(15.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
