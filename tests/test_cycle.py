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

from drawlib import canvas
from drawlib._core.l2_types import TypeColor
from drawlib._core.l3_styles import Style
from drawlib.smartarts import Cycle


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
        c = Cycle()
        c.append("Plan", description="Define goals")
        assert len(c.items) == 1
        assert c.items[0].text == "Plan"
        assert c.items[0].description == "Define goals"

        c.extend(["Do", "Check", "Act"], descriptions=["Execute", "Review", "Improve"])
        assert len(c.items) == 4
        assert c.items[1].text == "Do"
        assert c.items[1].description == "Execute"
        assert c.items[2].text == "Check"
        assert c.items[2].description == "Review"
        assert c.items[3].text == "Act"
        assert c.items[3].description == "Improve"

    def test_insert(self) -> None:
        """Test inserting item at specific index."""
        c = Cycle()
        c.append("Plan")
        c.append("Act")
        c.insert(1, "Do", description="Intermediate step")

        assert len(c.items) == 3
        assert c.items[0].text == "Plan"
        assert c.items[1].text == "Do"
        assert c.items[1].description == "Intermediate step"
        assert c.items[2].text == "Act"

    def test_set_center(self) -> None:
        """Test configuring center node for Radial Cycle."""
        c = Cycle()
        c.set_center(text="Core", description="Central Hub", radius=12.0)
        assert c._center_text == "Core"
        assert c._center_description == "Central Hub"
        assert c._center_radius == 12.0


class TestCycleRendering:
    """Integration tests verifying full canvas rendering of Cycle."""

    def test_render_basic_cycle(self) -> None:
        """Test rendering basic circular PDCA cycle with auto palette and arc arrows."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_basic.png"
            canvas.initialize()

            c = Cycle()
            c.append("Plan", description="Define objectives")
            c.append("Do", description="Implement plan")
            c.append("Check", description="Verify outcomes")
            c.append("Act", description="Standardize & scale")

            c.draw(xy=(50.0, 50.0), radius=32.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_with_center_node(self) -> None:
        """Test rendering radial cycle with a prominent center topic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_center.png"
            canvas.initialize()

            c = Cycle(center_text="PDCA", center_description="Loop", center_radius=11.0)
            c.extend(["Plan", "Do", "Check", "Act"])

            c.draw(xy=(50.0, 50.0), radius=34.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_outside_descriptions(self) -> None:
        """Test rendering cycle with descriptions positioned radially outside nodes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_outside.png"
            canvas.initialize()

            c = Cycle(description_placement="outside", node_radius=7.0)
            c.append("Stage 1", description="Discover")
            c.append("Stage 2", description="Define")
            c.append("Stage 3", description="Develop")
            c.append("Stage 4", description="Deliver")

            c.draw(xy=(50.0, 50.0), radius=30.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_rectangle_nodes(self) -> None:
        """Test rendering cycle with rounded rectangle nodes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_rect.png"
            canvas.initialize()

            c = Cycle(
                node_shape="rectangle",
                node_size=(20.0, 10.0),
                arrow_color_mode="monochrome",
            )
            c.append("Identify", description="Pinpoint issues")
            c.append("Design", description="Create blueprint")
            c.append("Execute", description="Deploy solution")
            c.append("Review", description="Measure impact")
            c.append("Iterate", description="Refine process")

            c.draw(xy=(50.0, 50.0), radius=35.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_line_arrows(self) -> None:
        """Test rendering cycle with minimalist line arc arrows."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_lines.png"
            canvas.initialize()

            c = Cycle(arrow_type="line", arrow_width=2.5)
            c.extend(["Spring", "Summer", "Autumn", "Winter"])

            c.draw(xy=(50.0, 50.0), radius=30.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_counter_clockwise(self) -> None:
        """Test rendering cycle in counter-clockwise direction."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_ccw.png"
            canvas.initialize()

            c = Cycle(clockwise=False)
            c.extend(["A", "B", "C"])

            c.draw(xy=(50.0, 50.0), radius=28.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_two_items(self) -> None:
        """Test rendering a two-step cycle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_two.png"
            canvas.initialize()

            c = Cycle()
            c.append("Input", description="Feedback")
            c.append("Output", description="Response")

            c.draw(xy=(50.0, 50.0), radius=30.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_empty_and_single_item(self) -> None:
        """Test rendering empty cycle and single-item cycle does not crash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_empty.png"
            canvas.initialize()

            c = Cycle(center_text="Empty Hub")
            c.draw(xy=(50.0, 50.0))

            c2 = Cycle()
            c2.append("Solo")
            c2.draw(xy=(50.0, 50.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_bottom_left_align(self) -> None:
        """Test rendering with bottom-left bounding alignment."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cycle_bottom_left.png"
            canvas.initialize()

            palette: list[TypeColor] = [(34, 197, 94), (59, 130, 246), (239, 68, 68)]
            c = Cycle(palette=palette)
            c.extend(["Alpha", "Beta", "Gamma"])

            c.draw(xy=(10.0, 10.0), radius=30.0, align="bottom_left")

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
