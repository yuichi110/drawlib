# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.charts (PieChart and DonutChart)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from drawlib import canvas
from drawlib._charts.pie_chart._renderer import _format_slice_label
from drawlib._core.l3_styles import Style
from drawlib.charts import PieChart, PieSlice


class TestPieSlice:
    """Unit tests for PieSlice data model."""

    def test_slice_initialization(self) -> None:
        """Test initialization and default attributes of PieSlice."""
        s = PieSlice("Mobile", 45.0)
        assert s.name == "Mobile"
        assert s.value == 45.0
        assert s.color is None
        assert s.style is None
        assert s.explode == 0.0

    def test_slice_custom_attributes(self) -> None:
        """Test custom color, style, and explode on PieSlice."""
        style = Style(fill_color=(100, 150, 200, 1.0))
        s = PieSlice("Desktop", 55.0, color=(200, 100, 50), style=style, explode=2.5)
        assert s.name == "Desktop"
        assert s.value == 55.0
        assert s.color == (200, 100, 50)
        assert s.style is style
        assert s.explode == 2.5


class TestPieChartConstruction:
    """Unit tests for PieChart container and properties."""

    def test_default_construction(self) -> None:
        """Test default values of PieChart."""
        chart = PieChart()
        assert chart.radius == 20.0
        assert chart.hole_ratio == 0.0
        assert chart.title == ""
        assert chart.center_text == ""
        assert chart.start_angle == 90.0
        assert chart.clockwise is True
        assert chart.show_values is True
        assert chart.slices == []

    def test_hole_ratio_clamping(self) -> None:
        """Test hole_ratio clamped between 0.0 and 0.9."""
        c1 = PieChart(hole_ratio=-0.5)
        assert c1.hole_ratio == 0.0
        c2 = PieChart(hole_ratio=1.5)
        assert c2.hole_ratio == 0.9

    def test_add_slice(self) -> None:
        """Test adding slices and retrieving slice list."""
        chart = PieChart()
        s1 = chart.add_slice("Chrome", 65.0)
        s2 = chart.add_slice("Safari", 20.0, explode=1.5)
        assert len(chart.slices) == 2
        assert chart.slices[0] is s1
        assert chart.slices[1] is s2
        assert s1.name == "Chrome"
        assert s2.explode == 1.5

    def test_get_size_auto_and_custom(self) -> None:
        """Test auto dimension calculations and explicit dimensions."""
        c1 = PieChart(radius=25.0, legend_position="right")
        w1, h1 = c1.get_size()
        assert w1 == 50.0 + 20.0  # diameter + 20
        assert h1 == 50.0 + 8.0

        c2 = PieChart(radius=20.0, legend_position="bottom", title="Market Share")
        w2, h2 = c2.get_size()
        assert w2 == 40.0 + 8.0
        assert h2 == 40.0 + 6.0 + 10.0

        c3 = PieChart(radius=20.0, width=100.0, height=80.0)
        assert c3.get_size() == (100.0, 80.0)


class TestPieChartFormatting:
    """Unit tests for slice percentage/value formatting."""

    def test_format_string(self) -> None:
        """Test string formatter."""
        assert _format_slice_label("{:.0f}%", 42.67, 100.0) == "43%"
        assert _format_slice_label("{:.2f}%", 42.67, 100.0) == "42.67%"

    def test_format_callable(self) -> None:
        """Test callable formatter."""

        def fn(v: float) -> str:
            return f"[{v:.1f}]"

        assert _format_slice_label(fn, 25.4, 50.0) == "[25.4]"


class TestPieChartRendering:
    """Integration tests verifying full rendering pipeline on canvas."""

    def test_render_standard_pie_chart(self) -> None:
        """Test rendering standard pie chart to a PNG file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "pie_standard.png"
            canvas.initialize()

            chart = PieChart(radius=22.0, title="Browser Market Share")
            chart.add_slice("Chrome", 65.0)
            chart.add_slice("Safari", 20.0)
            chart.add_slice("Edge", 10.0)
            chart.add_slice("Firefox", 5.0)
            chart.draw(xy=(15.0, 15.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_donut_chart_with_badge(self) -> None:
        """Test rendering donut chart with center text badge."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "donut_badge.png"
            canvas.initialize()

            chart = PieChart(
                radius=25.0,
                hole_ratio=0.6,
                center_text="100%\nTotal",
                title="Revenue by Division",
            )
            chart.add_slice("Cloud", 120.0)
            chart.add_slice("Hardware", 80.0)
            chart.add_slice("Services", 50.0)
            chart.draw(xy=(10.0, 10.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_exploded_slices(self) -> None:
        """Test rendering slices with explode offsets."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "pie_explode.png"
            canvas.initialize()

            chart = PieChart(radius=20.0, title="Campaign Status")
            chart.add_slice("Won", 55.0, explode=2.0)
            chart.add_slice("Lost", 30.0)
            chart.add_slice("Pending", 15.0)
            chart.draw(xy=(15.0, 15.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_empty_chart(self) -> None:
        """Test that empty or zero-value chart does not fail."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "pie_empty.png"
            canvas.initialize()

            chart = PieChart(radius=20.0)
            chart.draw(xy=(10.0, 10.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
