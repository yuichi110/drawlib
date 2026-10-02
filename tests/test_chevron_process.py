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

import pytest

from drawlib import canvas
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

default_styles = Styles


class TestChevronProcessUnit:
    """Unit tests for ChevronProcess configuration and item manipulation."""

    def test_initialization(self) -> None:
        """Test default parameters of ChevronProcess."""
        cp = ChevronProcess()
        assert cp._corner_angle == 60.0
        assert cp._spacing == 1.5
        assert cp._flat_left_end is False
        assert len(cp.items) == 0

    def test_append_and_extend(self) -> None:
        """Test adding items via append and extend."""
        styles = default_styles
        cp = ChevronProcess(
            default_textstyle=styles.WhiteBold,
            default_description_style=styles.White,
        )
        cp.append("Step 1", style=styles.PrimarySolid, description="Init scope")
        assert len(cp.items) == 1
        assert cp.items[0].text == "Step 1"
        assert cp.items[0].description == "Init scope"

        cp.extend(["Step 2", "Step 3"], styles=styles.PrimarySolid, descriptions=["Dev", "QA"])
        assert len(cp.items) == 3
        assert cp.items[1].text == "Step 2"
        assert cp.items[1].description == "Dev"
        assert cp.items[2].text == "Step 3"
        assert cp.items[2].description == "QA"

    def test_insert(self) -> None:
        """Test inserting item at specific index."""
        styles = default_styles
        cp = ChevronProcess(
            default_textstyle=styles.WhiteBold,
            default_description_style=styles.White,
        )
        cp.append("Step 1", style=styles.PrimarySolid)
        cp.append("Step 3", style=styles.PrimarySolid)
        cp.insert(1, "Step 2", style=styles.PrimarySolid, description="Middle step")

        assert len(cp.items) == 3
        assert cp.items[0].text == "Step 1"
        assert cp.items[1].text == "Step 2"
        assert cp.items[1].description == "Middle step"
        assert cp.items[2].text == "Step 3"

    def test_missing_style_raises_error(self) -> None:
        """Verify that missing style and textstyle raises appropriate errors."""
        cp = ChevronProcess()
        with pytest.raises((TypeError, ValueError)):
            getattr(cp, "append")("Step 1")

        styles = default_styles
        cp_no_text = ChevronProcess()
        with pytest.raises(ValueError, match="Neither 'default_textstyle' nor 'textstyle' was provided"):
            cp_no_text.append("Step 1", style=styles.PrimarySolid)

        cp_no_desc = ChevronProcess(default_textstyle=styles.PrimaryBold)
        with pytest.raises(
            ValueError, match="Neither 'default_description_style' nor 'description_style' was provided"
        ):
            cp_no_desc.append("Step 1", style=styles.PrimarySolid, description="detail")


class TestChevronProcessRendering:
    """Integration tests verifying full canvas rendering of ChevronProcess."""

    def test_render_basic_process(self) -> None:
        """Test rendering basic sequential chevrons."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_basic.png"
            canvas.clear()

            styles = default_styles
            cp = ChevronProcess(
                default_textstyle=styles.WhiteBold,
            )
            cp.append("Requirements", style=styles.PrimarySolid)
            cp.append("Design", style=styles.PrimarySolid)
            cp.append("Implementation", style=styles.PrimarySolid)
            cp.append("Verification", style=styles.PrimarySolid)
            cp.append("Deployment", style=styles.PrimarySolid)

            cp.draw(xy=(5.0, 40.0), width=90.0, height=14.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_with_descriptions(self) -> None:
        """Test rendering chevrons with titles and multi-line descriptions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_desc.png"
            canvas.clear()

            styles = default_styles
            cp = ChevronProcess(
                default_textstyle=styles.WhiteBold,
                default_description_style=styles.White,
                corner_angle=50.0,
                spacing=2.0,
            )
            cp.append("Phase 1: Planning", style=styles.PrimarySolid, description="Scope & Specs")
            cp.append("Phase 2: Build", style=styles.PrimarySolid, description="Core & Unit Tests")
            cp.append("Phase 3: Ship", style=styles.PrimarySolid, description="Canary Release")

            cp.draw(xy=(10.0, 40.0), width=80.0, height=16.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_flat_left_end(self) -> None:
        """Test rendering process with flat left end on the first step."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_flat.png"
            canvas.clear()

            styles = default_styles
            cp = ChevronProcess(
                default_textstyle=styles.WhiteBold,
                flat_left_end=True,
                spacing=1.2,
            )
            cp.extend(["Step 1", "Step 2", "Step 3"], styles=styles.PrimarySolid)

            cp.draw(xy=(5.0, 40.0), width=90.0, height=12.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_custom_styles(self) -> None:
        """Test rendering with explicit styles for each step."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_custom.png"
            canvas.clear()

            styles = default_styles
            cp = ChevronProcess(
                default_textstyle=styles.WhiteBold,
            )
            cp.append("Alpha", style=styles.PrimaryFlat)
            cp.append(
                "Beta",
                style=styles.Primary.patch(shape_fill_color=(239, 68, 68, 1.0), shape_line_width=1.5),
            )
            cp.append("GA", style=styles.SuccessFlat)

            cp.draw(xy=(10.0, 45.0), width=80.0, height=12.0, item_width=22.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_empty_process(self) -> None:
        """Test rendering an empty ChevronProcess does not raise."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_empty.png"
            canvas.clear()

            cp = ChevronProcess()
            cp.draw(xy=(10.0, 40.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
