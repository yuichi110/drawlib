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

from drawlib import canvas
from drawlib.smartarts import Cycle
from drawlib.styles import Styles

default_styles = Styles


class TestCycleUnit:
    """Unit tests for Cycle configuration and item manipulation."""

    def test_initialization(self) -> None:
        """Test default parameters of Cycle."""
        c = Cycle()
        assert c._clockwise is True
        assert c._start_angle == 90.0
        assert c._node_shape == "circle"
        assert c._node_radius == 8.0
        assert c._arrow_type == "arc"
        assert len(c.items) == 0

    def test_append_and_extend(self) -> None:
        """Test adding items via append and extend."""
        styles = default_styles
        c = Cycle(
            default_textstyle=styles.WhiteBold,
            default_description_style=styles.White,
            default_arrow_style=styles.PrimarySolid,
        )
        c.append("Plan", style=styles.PrimarySolid, description="Define goals")
        assert len(c.items) == 1
        assert c.items[0].text == "Plan"
        assert c.items[0].description == "Define goals"

        c.extend(["Do", "Check", "Act"], styles=styles.PrimarySolid, descriptions=["Execute", "Review", "Improve"])
        assert len(c.items) == 4
        assert c.items[1].text == "Do"
        assert c.items[1].description == "Execute"
        assert c.items[2].text == "Check"
        assert c.items[2].description == "Review"
        assert c.items[3].text == "Act"
        assert c.items[3].description == "Improve"

    def test_insert(self) -> None:
        """Test inserting item at specific index."""
        styles = default_styles
        c = Cycle(
            default_textstyle=styles.WhiteBold,
            default_description_style=styles.White,
            default_arrow_style=styles.PrimarySolid,
        )
        c.append("Plan", style=styles.PrimarySolid)
        c.append("Act", style=styles.PrimarySolid)
        c.insert(1, "Do", style=styles.PrimarySolid, description="Intermediate step")

        assert len(c.items) == 3
        assert c.items[0].text == "Plan"
        assert c.items[1].text == "Do"
        assert c.items[1].description == "Intermediate step"
        assert c.items[2].text == "Act"

    def test_set_center(self) -> None:
        """Test configuring center node for Radial Cycle."""
        styles = default_styles
        c = Cycle()
        c.set_center(text="Core", style=styles.PrimarySolid, description="Central Hub", radius=12.0)
        assert c._center_text == "Core"
        assert c._center_description == "Central Hub"
        assert c._center_radius == 12.0

    def test_cycle_missing_style_raises_error(self) -> None:
        """Verify that missing style, textstyle, etc. raises appropriate errors."""
        c = Cycle()
        with pytest.raises((TypeError, ValueError)):
            getattr(c, "append")("Plan")

        styles = default_styles
        c_no_text = Cycle()
        with pytest.raises(ValueError, match="Neither 'default_textstyle' nor 'textstyle' was provided"):
            c_no_text.append("Plan", style=styles.PrimarySolid)

        c_no_arrow = Cycle(default_textstyle=styles.WhiteBold, arrow_color_mode="monochrome")
        with pytest.raises(ValueError, match="Neither 'default_arrow_style' nor 'arrow_style' was provided"):
            c_no_arrow.append("Plan", style=styles.PrimarySolid)

        c_no_desc = Cycle(
            default_textstyle=styles.WhiteBold,
            default_arrow_style=styles.PrimarySolid,
        )
        with pytest.raises(
            ValueError, match="Neither 'default_description_style' nor 'description_style' was provided"
        ):
            c_no_desc.append("Plan", style=styles.PrimarySolid, description="Detail")


class TestCycleRendering:
    """Integration tests verifying full canvas rendering of Cycle."""

    def test_render_basic_cycle(self) -> None:
        """Test rendering basic circular PDCA cycle with arc arrows."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_basic.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                default_textstyle=styles.WhiteBold,
                default_description_style=styles.White,
                default_arrow_style=styles.PrimarySolid,
            )
            c.append("Plan", style=styles.PrimarySolid, description="Define objectives")
            c.append("Do", style=styles.PrimarySolid, description="Implement plan")
            c.append("Check", style=styles.PrimarySolid, description="Verify outcomes")
            c.append("Act", style=styles.PrimarySolid, description="Standardize & scale")

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
                default_textstyle=styles.WhiteBold,
                default_arrow_style=styles.PrimarySolid,
                center_text="PDCA",
                center_description="Loop",
                center_radius=11.0,
                center_style=styles.PrimarySolid,
                center_textstyle=styles.WhiteBold,
                center_description_style=styles.White,
            )
            c.extend(["Plan", "Do", "Check", "Act"], styles=styles.PrimarySolid)

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
                default_textstyle=styles.WhiteBold,
                default_description_style=styles.Black,
                default_arrow_style=styles.PrimarySolid,
                description_placement="outside",
                node_radius=7.0,
            )
            c.append("Stage 1", style=styles.PrimarySolid, description="Discover")
            c.append("Stage 2", style=styles.PrimarySolid, description="Define")
            c.append("Stage 3", style=styles.PrimarySolid, description="Develop")
            c.append("Stage 4", style=styles.PrimarySolid, description="Deliver")

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
                default_textstyle=styles.WhiteBold,
                default_description_style=styles.White,
                default_arrow_style=styles.PrimarySolid,
                node_shape="rectangle",
                node_size=(20.0, 10.0),
                arrow_color_mode="monochrome",
            )
            c.append("Identify", style=styles.PrimarySolid, description="Pinpoint issues")
            c.append("Design", style=styles.PrimarySolid, description="Create blueprint")
            c.append("Execute", style=styles.PrimarySolid, description="Deploy solution")
            c.append("Review", style=styles.PrimarySolid, description="Measure impact")
            c.append("Iterate", style=styles.PrimarySolid, description="Refine process")

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
                default_textstyle=styles.WhiteBold,
                default_arrow_style=styles.PrimarySolid,
                arrow_type="line",
                arrow_width=2.5,
            )
            c.extend(["Spring", "Summer", "Autumn", "Winter"], styles=styles.PrimarySolid)

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
                default_textstyle=styles.WhiteBold,
                default_arrow_style=styles.PrimarySolid,
                clockwise=False,
            )
            c.extend(["A", "B", "C"], styles=styles.PrimarySolid)

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
                default_textstyle=styles.WhiteBold,
                default_description_style=styles.White,
                default_arrow_style=styles.PrimarySolid,
            )
            c.append("Input", style=styles.PrimarySolid, description="Feedback")
            c.append("Output", style=styles.PrimarySolid, description="Response")

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
                center_text="Empty Hub",
                center_style=styles.PrimarySolid,
                center_textstyle=styles.WhiteBold,
            )
            c.draw(xy=(50.0, 50.0))

            c2 = Cycle(
                default_textstyle=styles.WhiteBold,
                default_arrow_style=styles.PrimarySolid,
            )
            c2.append("Solo", style=styles.PrimarySolid)
            c2.draw(xy=(50.0, 50.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_bottom_left_align(self) -> None:
        """Test rendering with bottom-left bounding alignment."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_bottom_left.png"
            canvas.clear()

            styles = default_styles
            c = Cycle(
                default_textstyle=styles.WhiteBold,
                default_arrow_style=styles.PrimarySolid,
            )
            c.extend(["Alpha", "Beta", "Gamma"], styles=[styles.GreenFlat, styles.BlueFlat, styles.RedFlat])

            c.draw(xy=(10.0, 10.0), radius=30.0, align="bottom_left")

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
