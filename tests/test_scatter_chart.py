# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.charts (ScatterChart)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from drawlib import canvas
from drawlib._core.l3_styles import Style
from drawlib.charts import ScatterChart


class TestScatterChartUnit:
    """Unit tests for ScatterChart container and points."""

    def test_initialization(self) -> None:
        """Test default attributes of ScatterChart."""
        chart = ScatterChart(width=90.0, height=60.0, title="Benchmark")
        assert chart.width == 90.0
        assert chart.height == 60.0
        assert chart.title == "Benchmark"
        assert len(chart.points) == 0
        assert len(chart.series) == 0
        assert chart.get_size() == (90.0, 60.0)

    def test_add_point(self) -> None:
        """Test adding individual data points via add()."""
        chart = ScatterChart()
        p1 = chart.add(xy=(10.5, 25.0), radius=1.5, label="Point A")
        assert p1.xy == (10.5, 25.0)
        assert p1.radius == 1.5
        assert p1.label == "Point A"
        assert p1.shape == "circle"

        p2 = chart.add(xy=(30.0, 45.0), shape="square")
        assert p2.shape == "square"
        assert len(chart.points) == 2

    def test_add_series(self) -> None:
        """Test adding series with 2-tuples and 3-tuples (bubble size)."""
        chart = ScatterChart()
        s1 = chart.add_series(
            name="Alpha",
            data=[(10.0, 20.0), (30.0, 40.0)],
            radius=1.2,
            shape="triangle",
        )
        assert s1.name == "Alpha"
        assert len(s1.points) == 2
        assert s1.points[0].xy == (10.0, 20.0)
        assert s1.points[0].radius == 1.2

        s2 = chart.add_series(
            name="Beta (Bubble)",
            data=[(15.0, 25.0, 3.5), (35.0, 55.0, 5.0)],
        )
        assert len(s2.points) == 2
        assert s2.points[0].radius == 3.5
        assert s2.points[1].radius == 5.0

    def test_axis_configuration(self) -> None:
        """Test chaining configuration for X and Y axes."""
        chart = ScatterChart()
        chart.configure_x_axis(label="Throughput", unit="rps", min_value=0.0, max_value=100.0)
        chart.configure_y_axis(label="Latency", unit="ms", min_value=0.0, max_value=50.0)

        assert chart.x_axis.label == "Throughput"
        assert chart.x_axis.unit == "rps"
        assert chart.x_axis.min_value == 0.0
        assert chart.x_axis.max_value == 100.0

        assert chart.y_axis.label == "Latency"
        assert chart.y_axis.unit == "ms"
        assert chart.y_axis.min_value == 0.0
        assert chart.y_axis.max_value == 50.0


class TestScatterChartRendering:
    """Integration tests verifying full canvas rendering of ScatterChart."""

    def test_render_standalone_and_series(self) -> None:
        """Test rendering chart with both standalone points and named series."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "scatter_basic.png"
            canvas.initialize()

            chart = ScatterChart(
                width=88.0,
                height=55.0,
                title="Service Benchmark",
            )
            chart.configure_x_axis(label="Load (rps)", min_value=0)
            chart.configure_y_axis(label="Response Time (ms)", min_value=0)

            # Standalone points with labels
            chart.add(xy=(100, 15.0), radius=1.2, label="v1.0 Baseline")
            chart.add(xy=(500, 28.0), radius=1.8, style="red_flat", label="v1.5")
            chart.add(xy=(900, 19.5), radius=2.2, style="blue_flat", label="v2.0")

            # Named series
            chart.add_series(
                name="Cluster A",
                data=[(200, 22.0), (400, 35.0), (700, 60.0)],
                shape="square",
            )
            chart.add_series(
                name="Cluster B",
                data=[(150, 18.0), (350, 26.0), (600, 42.0)],
                shape="rhombus",
            )

            chart.draw(xy=(6.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_bubble_chart(self) -> None:
        """Test rendering bubble chart with variable radius points."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "scatter_bubble.png"
            canvas.initialize()

            chart = ScatterChart(
                width=80.0,
                height=50.0,
                title="Market Share & Growth",
            )
            chart.configure_x_axis(label="Market Size ($M)")
            chart.configure_y_axis(label="YoY Growth (%)")

            chart.add_series(
                name="Tech",
                data=[(20.0, 15.0, 1.5), (50.0, 35.0, 3.2), (80.0, 20.0, 4.5)],
            )
            chart.add_series(
                name="Finance",
                data=[(30.0, 10.0, 2.0), (60.0, 18.0, 3.8), (90.0, 8.0, 5.2)],
            )

            chart.draw(xy=(10.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_custom_styles_and_shapes(self) -> None:
        """Test rendering points with custom styles, triangles, and squares."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "scatter_shapes.png"
            canvas.initialize()

            chart = ScatterChart(width=70.0, height=45.0)
            c_style = Style(line_width=1.5, fill_color=(16, 185, 129, 0.7))
            chart.add(xy=(1, 2), shape="triangle", style=c_style, radius=2.0)
            chart.add(xy=(3, 4), shape="rhombus", radius=2.0)
            chart.add(xy=(5, 6), shape="square", radius=2.0)

            chart.draw(xy=(10.0, 10.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_empty_chart(self) -> None:
        """Test rendering empty ScatterChart without points does not raise."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "scatter_empty.png"
            canvas.initialize()

            chart = ScatterChart()
            chart.draw(xy=(10.0, 10.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
