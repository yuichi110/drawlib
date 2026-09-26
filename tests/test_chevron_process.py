# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.smartarts (ChevronProcess)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from drawlib import canvas
from drawlib._core.l2_types import TypeColor
from drawlib._core.l3_styles import Style
from drawlib.preset_styles import default_styles
from drawlib.smartarts import ChevronProcess


class TestChevronProcessUnit:
    """Unit tests for ChevronProcess configuration and item manipulation."""

    def test_initialization(self) -> None:
        """Test default parameters of ChevronProcess."""
        styles = default_styles
        cp = ChevronProcess(styles=styles)
        assert cp._corner_angle == 60.0
        assert cp._spacing == 1.5
        assert cp._flat_left_end is False
        assert len(cp.items) == 0

    def test_append_and_extend(self) -> None:
        """Test adding items via append and extend."""
        styles = default_styles
        cp = ChevronProcess(styles=styles)
        cp.append("Step 1", description="Init scope")
        assert len(cp.items) == 1
        assert cp.items[0].text == "Step 1"
        assert cp.items[0].description == "Init scope"

        cp.extend(["Step 2", "Step 3"], descriptions=["Dev", "QA"])
        assert len(cp.items) == 3
        assert cp.items[1].text == "Step 2"
        assert cp.items[1].description == "Dev"
        assert cp.items[2].text == "Step 3"
        assert cp.items[2].description == "QA"

    def test_insert(self) -> None:
        """Test inserting item at specific index."""
        styles = default_styles
        cp = ChevronProcess(styles=styles)
        cp.append("Step 1")
        cp.append("Step 3")
        cp.insert(1, "Step 2", description="Middle step")

        assert len(cp.items) == 3
        assert cp.items[0].text == "Step 1"
        assert cp.items[1].text == "Step 2"
        assert cp.items[1].description == "Middle step"
        assert cp.items[2].text == "Step 3"


class TestChevronProcessRendering:
    """Integration tests verifying full canvas rendering of ChevronProcess."""

    def test_render_basic_process(self) -> None:
        """Test rendering basic sequential chevrons with auto palette."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_basic.png"
            canvas.initialize()

            styles = default_styles
            cp = ChevronProcess(styles=styles)
            cp.append("Requirements")
            cp.append("Design")
            cp.append("Implementation")
            cp.append("Verification")
            cp.append("Deployment")

            cp.draw(xy=(5.0, 40.0), width=90.0, height=14.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_with_descriptions(self) -> None:
        """Test rendering chevrons with titles and multi-line descriptions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_desc.png"
            canvas.initialize()

            styles = default_styles
            cp = ChevronProcess(styles=styles, corner_angle=50.0, spacing=2.0)
            cp.append("Phase 1: Planning", description="Scope & Specs")
            cp.append("Phase 2: Build", description="Core & Unit Tests")
            cp.append("Phase 3: Ship", description="Canary Release")

            cp.draw(xy=(10.0, 40.0), width=80.0, height=16.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_flat_left_end(self) -> None:
        """Test rendering process with flat left end on the first step."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_flat.png"
            canvas.initialize()

            styles = default_styles
            cp = ChevronProcess(styles=styles, flat_left_end=True, spacing=1.2)
            cp.extend(["Step 1", "Step 2", "Step 3"])

            cp.draw(xy=(5.0, 40.0), width=90.0, height=12.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_custom_styles_and_palette(self) -> None:
        """Test rendering with explicit style and custom palette."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_custom.png"
            canvas.initialize()

            styles = default_styles
            palette: list[TypeColor] = [(59, 130, 246), (16, 185, 129), (245, 158, 11)]
            cp = ChevronProcess(styles=styles, palette=palette)
            cp.append("Alpha")
            cp.append(
                "Beta",
                style=styles.primary.patch(shape_fill_color=(239, 68, 68, 1.0), shape_line_width=1.5),
            )
            cp.append("GA")

            cp.draw(xy=(10.0, 45.0), width=80.0, height=12.0, item_width=22.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_empty_process(self) -> None:
        """Test rendering an empty ChevronProcess does not raise."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_empty.png"
            canvas.initialize()

            styles = default_styles
            cp = ChevronProcess(styles=styles)
            cp.draw(xy=(10.0, 40.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
