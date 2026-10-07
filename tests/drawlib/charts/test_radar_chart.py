# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.charts (RadarChart)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from drawlib import canvas
from drawlib._charts.radar_chart._renderer import _format_value
from drawlib._core.l3_styles import Style
from drawlib.charts.radar import RadarChart, Series


class TestRadarSeries:
    """Unit tests for Series data model in radar charts."""

    def test_series_initialization(self) -> None:
        """Test default attributes of Series."""
        style = Style(line_color=(50, 100, 200))
        s = Series("Warrior", [80.0, 90.0, 70.0, 60.0, 85.0], style=style)
        assert s.name == "Warrior"
        assert s.values == [80.0, 90.0, 70.0, 60.0, 85.0]
        assert s.style is style
        assert s.fill_alpha == 0.25
        assert s.line_width == 2.0
        assert s.line_style == "solid"
        assert s.point_shape == "circle"
        assert s.point_size == 0.8
        assert s.legend_text_style is None

    def test_series_custom_attributes(self) -> None:
        """Test customized attributes on Series."""
        custom_style = Style(line_width=3.0, line_color=(120, 80, 220))
        s = Series(
            name="Mage",
            values=[30.0, 20.0, 95.0, 80.0, 40.0],
            style=custom_style,
            fill_alpha=0.4,
            line_width=2.5,
            line_style="dashed",
            point_shape="square",
            point_size=1.2,
            legend_text_style=Style(text_size=11),
        )
        assert s.name == "Mage"
        assert s.style is custom_style
        assert s.fill_alpha == 0.4
        assert s.line_width == 2.5
        assert s.line_style == "dashed"
        assert s.point_shape == "square"
        assert s.point_size == 1.2
        assert s.legend_text_style is not None


class TestRadarChartConstruction:
    """Unit tests for RadarChart container and properties."""

    def test_minimum_categories_validation(self) -> None:
        """Test that fewer than 3 categories raises ValueError."""
        with pytest.raises(ValueError, match="at least 3 categories"):
            RadarChart(categories=["Speed", "Power"], axis_line_style=Style(line_color=(200, 200, 200)))

    def test_default_construction(self) -> None:
        """Test default values of RadarChart."""
        axis_line_style = Style(line_color=(200, 200, 200))
        chart = RadarChart(categories=["A", "B", "C", "D"], axis_line_style=axis_line_style)
        assert chart.categories == ["A", "B", "C", "D"]
        assert chart.axis_line_style is axis_line_style
        assert chart.radius == 25.0
        assert chart.min_value == 0.0
        assert chart.max_value is None
        assert chart.levels == 5
        assert chart.grid_shape == "polygon"
        assert chart.axis_text_style is None
        assert chart.grid_style is None
        assert chart.series == []

    def test_add_series(self) -> None:
        """Test registering series with RadarChart."""
        chart = RadarChart(categories=["Attack", "Defense", "Speed"], axis_line_style=Style(line_color=(200, 200, 200)))
        s1 = chart.add_series("P1", [80, 70, 90], style=Style(line_color=(50, 100, 200)))
        s2 = chart.add_series("P2", [60, 85, 75], style=Style(line_color=(255, 100, 50)))
        assert len(chart.series) == 2
        assert chart.series[0] is s1
        assert chart.series[1] is s2
        assert s1.name == "P1"
        assert s2.style.line_color == (255, 100, 50)

    def test_get_size_auto_and_custom(self) -> None:
        """Test auto dimension calculations and explicit dimensions."""
        c1 = RadarChart(
            categories=["A", "B", "C"],
            axis_line_style=Style(line_color=(200, 200, 200)),
            axis_text_style=Style(text_size=10),
            radius=20.0,
        )
        w1, h1 = c1.get_size()
        assert w1 == 40.0 + 16.0
        assert h1 == 40.0 + 16.0

        c2 = RadarChart(
            categories=["A", "B", "C"],
            axis_line_style=Style(line_color=(200, 200, 200)),
            axis_text_style=Style(text_size=10),
            radius=20.0,
            title="Skills",
            title_style=Style(text_size=12),
        )
        w2, h2 = c2.get_size()
        assert w2 == 40.0 + 16.0
        assert h2 == 40.0 + 16.0 + 6.0

        c3 = RadarChart(
            categories=["A", "B", "C"],
            axis_line_style=Style(line_color=(200, 200, 200)),
            radius=20.0,
            width=90.0,
            height=75.0,
        )
        assert c3.get_size() == (90.0, 75.0)


class TestRadarChartFormatting:
    """Unit tests for scale and value label formatting."""

    def test_format_string(self) -> None:
        """Test string formatter."""
        assert _format_value("{:.1f}", 42.67) == "42.7"
        assert _format_value("{:g}%", 80.0) == "80%"

    def test_format_callable(self) -> None:
        """Test callable formatter."""

        def fn(v: float) -> str:
            return f"[{v:.0f} pts]"

        assert _format_value(fn, 75.0) == "[75 pts]"


class TestRadarChartRendering:
    """Integration tests verifying full rendering pipeline on canvas."""

    def test_render_polygon_radar_chart(self) -> None:
        """Test rendering standard polygon grid radar chart to PNG."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "radar_polygon.png"
            canvas.clear()

            chart = RadarChart(
                categories=["Speed", "Power", "Defense", "Agility", "Stamina"],
                axis_line_style=Style(line_color=(203, 213, 225), line_width=1.0),
                axis_text_style=Style(text_size=10, text_color=(30, 41, 59)),
                grid_style=Style(line_color=(226, 232, 240), line_width=1.0),
                radius=25.0,
                title="Character Attributes Comparison",
                title_style=Style(text_size=12, text_color=(30, 41, 59)),
            )
            chart.add_series("Warrior", [85, 90, 80, 60, 75], style=Style(line_color=(50, 100, 200)))
            chart.add_series("Rogue", [95, 65, 50, 95, 70], style=Style(line_color=(200, 50, 100)))
            chart.draw(xy=(10.0, 10.0))
            chart.draw_legend(xy=(70.0, 35.0), text_style=Style(text_size=10, text_color=(30, 41, 59)))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_circle_grid_radar_chart(self) -> None:
        """Test rendering circular concentric grid radar chart with values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "radar_circle.png"
            canvas.clear()

            chart = RadarChart(
                categories=["Usability", "Performance", "Security", "Reliability", "Maintainability"],
                axis_line_style=Style(line_color=(203, 213, 225), line_width=1.0),
                axis_text_style=Style(text_size=10, text_color=(30, 41, 59)),
                grid_style=Style(line_color=(226, 232, 240), line_width=1.0),
                scale_text_style=Style(text_size=8, text_color=(148, 163, 184)),
                value_text_style=Style(text_size=9, text_color=(30, 41, 59)),
                radius=26.0,
                grid_shape="circle",
                levels=4,
                max_value=100.0,
                title="System Evaluation",
                title_style=Style(text_size=12, text_color=(30, 41, 59)),
            )
            chart.add_series("Product A", [90, 85, 95, 80, 75], style=Style(line_color=(50, 100, 200)))
            chart.add_series(
                "Product B", [70, 95, 80, 90, 85], style=Style(line_color=(200, 50, 100)), line_style="dashed"
            )
            chart.draw(xy=(15.0, 8.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_empty_radar_chart(self) -> None:
        """Test rendering radar chart with no registered series."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "radar_empty.png"
            canvas.clear()

            chart = RadarChart(
                categories=["A", "B", "C", "D"],
                axis_line_style=Style(line_color=(203, 213, 225)),
                radius=20.0,
            )
            chart.draw(xy=(10.0, 10.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_lifecycle_and_configure_axis(self) -> None:
        """Test RadarChart configure_axis, show, draw_ratio, and spatial overrides."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "radar_lifecycle.png"
            canvas.clear()

            chart = RadarChart(
                categories=["A", "B", "C", "D"],
                axis_line_style=Style(line_color=(203, 213, 225)),
                radius=20.0,
            )
            chart.configure_axis(min_value=10.0, max_value=100.0, levels=3, scale_format="{:.0f}")
            assert chart.min_value == 10.0
            assert chart.max_value == 100.0
            assert chart.levels == 3

            s1 = chart.add_series("S1", [80, 70, 90, 60], style=Style(line_color=(50, 100, 200)), draw_ratio=0.5)
            s2 = chart.add_series("S2", [50, 60, 70, 80], style=Style(line_color=(200, 50, 100)), show=False)
            assert s1.draw_ratio == 0.5
            assert s2.show is False

            orig_size = chart.get_size()
            chart.draw(xy=(10.0, 10.0), radius=15.0, width=45.0, height=45.0, scale=0.9)
            assert chart.radius == 20.0
            assert chart.get_size() == orig_size

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
