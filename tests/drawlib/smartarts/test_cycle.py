# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.smartarts (Cycle)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from drawlib import canvas
from drawlib.smartarts import Cycle
from drawlib.styles import Styles

default_styles = Styles


class TestCycleUnit:
    """Unit tests for Cycle configuration and item manipulation."""

    def test_initialization(self) -> None:
        """Test default parameters of Cycle."""
        styles = default_styles
        c = Cycle(style=styles.PrimarySolid, text_style=styles.WhiteBold)
        assert c._clockwise is True
        assert c._start_angle == 90.0
        assert c._node_shape == "circle"
        assert c._node_radius == 8.0
        assert c._arrow_type == "arc"
        assert len(c.items) == 0

    def test_add_and_mutation(self) -> None:
        """Test adding items via add() and mutating returned CycleItem."""
        styles = default_styles
        c = Cycle(
            style=styles.PrimarySolid,
            text_style=styles.WhiteBold,
            description_style=styles.White,
            arrow_style=styles.PrimarySolid,
        )
        item1 = c.add("Plan", style=styles.PrimarySolid, description="Define goals")
        assert len(c.items) == 1
        assert c.items[0] is item1
        assert item1.text == "Plan"
        assert item1.description == "Define goals"
        assert item1.show is True

        item2 = c.add("Do", style=styles.PrimarySolid, description="Execute", show=False)
        item3 = c.add("Check", style=styles.PrimarySolid, description="Review")
        item4 = c.add("Act", style=styles.PrimarySolid, description="Improve")
        assert len(c.items) == 4
        assert item2.text == "Do"
        assert item2.show is False
        assert item3.text == "Check"
        assert item4.text == "Act"

        item2.show = True
        item2.style = styles.RedFlat
        assert c.items[1].show is True
        assert c.items[1].style == styles.RedFlat

    def test_set_center(self) -> None:
        """Test configuring center node for Radial Cycle."""
        styles = default_styles
        c = Cycle(style=styles.PrimarySolid, text_style=styles.WhiteBold)
        center = c.set_center(text="Core", style=styles.PrimarySolid, description="Central Hub", radius=12.0)
        assert c.center is center
        assert center.text == "Core"
        assert center.description == "Central Hub"
        assert center.radius == 12.0
        assert center.show is True

    def test_cycle_missing_style_raises_error(self) -> None:
        """Verify that missing mandatory styles raises ValidationError on __init__ or ValueError on draw."""
        with pytest.raises(ValidationError):
            Cycle()  # type: ignore

        styles = default_styles
        with pytest.raises(ValidationError):
            Cycle(style=styles.PrimarySolid)  # type: ignore

        with pytest.raises(ValidationError):
            Cycle(text_style=styles.WhiteBold)  # type: ignore

        c_no_arrow = Cycle(
            style=styles.PrimarySolid,
            text_style=styles.WhiteBold,
            arrow_color_mode="monochrome",
        )
        with pytest.raises(ValueError, match="Neither default 'arrow_style' nor item 'arrow_style' was provided"):
            c_no_arrow.add("Plan")

        c_no_desc = Cycle(
            style=styles.PrimarySolid,
            text_style=styles.WhiteBold,
            arrow_style=styles.PrimarySolid,
        )
        with pytest.raises(
            ValueError, match="Neither default 'description_style' nor item 'description_style' was provided"
        ):
            c_no_desc.add("Plan", description="Detail")


class TestCycleRendering:
    """Integration tests verifying full canvas rendering of Cycle."""

    def test_render_basic_cycle(self) -> None:
        """Test rendering basic circular PDCA cycle with arc arrows."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_basic.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                description_style=styles.White,
                arrow_style=styles.PrimarySolid,
            )
            c.add("Plan", style=styles.PrimarySolid, description="Define objectives")
            c.add("Do", style=styles.PrimarySolid, description="Implement plan")
            c.add("Check", style=styles.PrimarySolid, description="Verify outcomes")
            c.add("Act", style=styles.PrimarySolid, description="Standardize & scale")

            c.draw(xy=(50.0, 50.0), radius=32.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_with_center_node(self) -> None:
        """Test rendering radial cycle with a prominent center topic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_center.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                arrow_style=styles.PrimarySolid,
                center_text="PDCA",
                center_description="Loop",
                center_radius=11.0,
                center_style=styles.PrimarySolid,
                center_text_style=styles.WhiteBold,
                center_description_style=styles.White,
            )
            for label in ["Plan", "Do", "Check", "Act"]:
                c.add(label, style=styles.PrimarySolid)

            c.draw(xy=(50.0, 50.0), radius=34.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_outside_descriptions(self) -> None:
        """Test rendering cycle with descriptions positioned radially outside nodes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_outside.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                description_style=styles.Black,
                arrow_style=styles.PrimarySolid,
                description_placement="outside",
                node_radius=7.0,
            )
            c.add("Stage 1", style=styles.PrimarySolid, description="Discover")
            c.add("Stage 2", style=styles.PrimarySolid, description="Define")
            c.add("Stage 3", style=styles.PrimarySolid, description="Develop")
            c.add("Stage 4", style=styles.PrimarySolid, description="Deliver")

            c.draw(xy=(50.0, 50.0), radius=30.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_rectangle_nodes(self) -> None:
        """Test rendering cycle with rounded rectangle nodes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_rect.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                description_style=styles.White,
                arrow_style=styles.PrimarySolid,
                node_shape="rectangle",
                node_width=20.0,
                node_height=10.0,
                arrow_color_mode="monochrome",
            )
            c.add("Identify", style=styles.PrimarySolid, description="Pinpoint issues")
            c.add("Design", style=styles.PrimarySolid, description="Create blueprint")
            c.add("Execute", style=styles.PrimarySolid, description="Deploy solution")
            c.add("Review", style=styles.PrimarySolid, description="Measure impact")
            c.add("Iterate", style=styles.PrimarySolid, description="Refine process")

            c.draw(xy=(50.0, 50.0), radius=35.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_line_arrows(self) -> None:
        """Test rendering cycle with minimalist line arc arrows."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_lines.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                arrow_style=styles.PrimarySolid,
                arrow_type="line",
                arrow_width=2.5,
            )
            for label in ["Spring", "Summer", "Autumn", "Winter"]:
                c.add(label, style=styles.PrimarySolid)

            c.draw(xy=(50.0, 50.0), radius=30.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_counter_clockwise(self) -> None:
        """Test rendering cycle in counter-clockwise direction."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_ccw.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                arrow_style=styles.PrimarySolid,
                clockwise=False,
            )
            for label in ["A", "B", "C"]:
                c.add(label, style=styles.PrimarySolid)

            c.draw(xy=(50.0, 50.0), radius=28.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_two_items(self) -> None:
        """Test rendering a two-step cycle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_two.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                description_style=styles.White,
                arrow_style=styles.PrimarySolid,
            )
            c.add("Input", style=styles.PrimarySolid, description="Feedback")
            c.add("Output", style=styles.PrimarySolid, description="Response")

            c.draw(xy=(50.0, 50.0), radius=30.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_empty_and_single_item(self) -> None:
        """Test rendering empty cycle and single-item cycle does not crash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_empty.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                center_text="Empty Hub",
                center_style=styles.PrimarySolid,
                center_text_style=styles.WhiteBold,
            )
            c.draw(xy=(50.0, 50.0))

            c2 = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                arrow_style=styles.PrimarySolid,
            )
            c2.add("Solo", style=styles.PrimarySolid)
            c2.draw(xy=(50.0, 50.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_bottom_left_align(self) -> None:
        """Test rendering with bottom-left bounding alignment and scale."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_bottom_left.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                style=styles.PrimarySolid,
                text_style=styles.WhiteBold,
                arrow_style=styles.PrimarySolid,
            )
            c.add("Alpha", style=styles.GreenFlat)
            b = c.add("Beta", style=styles.BlueFlat, show=False)
            c.add("Gamma", style=styles.RedFlat)
            assert b.show is False

            c.draw(xy=(10.0, 10.0), radius=30.0, align="bottom_left", scale=0.8)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
