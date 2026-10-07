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
from pydantic import ValidationError

from drawlib import canvas
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles


class TestChevronProcessUnit:
    """Unit tests for ChevronProcess configuration and item manipulation."""

    def test_initialization(self) -> None:
        """Test default parameters of ChevronProcess."""
        cp = ChevronProcess(
            style=Styles.PrimarySolid,
            text_style=Styles.WhiteBold,
            description_style=Styles.White,
        )
        assert cp._corner_angle == 60.0
        assert cp._spacing == 1.5
        assert cp._flat_left_end is False
        assert len(cp.items) == 0

    def test_missing_style_raises_error(self) -> None:
        """Verify that omitting required styles in __init__ raises ValidationError."""
        with pytest.raises((ValidationError, TypeError)):
            ChevronProcess()  # ty: ignore[missing-argument]

        with pytest.raises((ValidationError, TypeError)):
            ChevronProcess(style=Styles.PrimarySolid)  # ty: ignore[missing-argument]

        with pytest.raises((ValidationError, TypeError)):
            ChevronProcess(  # ty: ignore[missing-argument]
                style=Styles.PrimarySolid,
                text_style=Styles.WhiteBold,
            )

    def test_add_and_mutate(self) -> None:
        """Test adding items via add() and mutating returned ChevronItem instances."""
        cp = ChevronProcess(
            style=Styles.PrimarySolid,
            text_style=Styles.WhiteBold,
            description_style=Styles.White,
        )
        s1 = cp.add("Step 1", description="Init scope")
        assert len(cp.items) == 1
        assert s1.text == "Step 1"
        assert s1.description == "Init scope"
        assert s1.style == Styles.PrimarySolid
        assert s1.text_style == Styles.WhiteBold
        assert s1.description_style == Styles.White
        assert s1.show is True

        s2 = cp.add("Step 2", description="Dev", style=Styles.AccentFlat)
        s3 = cp.add("Step 3", description="QA", show=False)
        assert len(cp.items) == 3
        assert s2.style == Styles.AccentFlat
        assert s3.show is False

        # Mutate returned item
        s2.style = Styles.SuccessFlat
        s2.text = "Step 2 Updated"
        assert cp.items[1].style == Styles.SuccessFlat
        assert cp.items[1].text == "Step 2 Updated"


class TestChevronProcessRendering:
    """Integration tests verifying full canvas rendering of ChevronProcess."""

    def test_render_basic_process(self) -> None:
        """Test rendering basic sequential chevrons."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_basic.png"
            canvas.clear()

            cp = ChevronProcess(
                style=Styles.PrimarySolid,
                text_style=Styles.WhiteBold,
                description_style=Styles.White,
            )
            cp.add("Requirements")
            cp.add("Design")
            cp.add("Implementation")
            cp.add("Verification")
            cp.add("Deployment")

            cp.draw(xy=(5.0, 40.0), width=90.0, height=14.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_with_descriptions(self) -> None:
        """Test rendering chevrons with titles and multi-line descriptions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_desc.png"
            canvas.clear()

            cp = ChevronProcess(
                style=Styles.PrimarySolid,
                text_style=Styles.WhiteBold,
                description_style=Styles.White,
                corner_angle=50.0,
                spacing=2.0,
            )
            cp.add("Phase 1: Planning", description="Scope & Specs")
            cp.add("Phase 2: Build", description="Core & Unit Tests")
            cp.add("Phase 3: Ship", description="Canary Release")

            cp.draw(xy=(10.0, 40.0), width=80.0, height=16.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_flat_left_end(self) -> None:
        """Test rendering process with flat left end on the first step."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_flat.png"
            canvas.clear()

            cp = ChevronProcess(
                style=Styles.PrimarySolid,
                text_style=Styles.WhiteBold,
                description_style=Styles.White,
                flat_left_end=True,
                spacing=1.2,
            )
            for t in ("Step 1", "Step 2", "Step 3"):
                cp.add(t)

            cp.draw(xy=(5.0, 40.0), width=90.0, height=12.0, scale=0.9)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_custom_styles(self) -> None:
        """Test rendering with explicit styles for each step."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_custom.png"
            canvas.clear()

            cp = ChevronProcess(
                style=Styles.PrimaryFlat,
                text_style=Styles.WhiteBold,
                description_style=Styles.White,
            )
            cp.add("Alpha")
            cp.add(
                "Beta",
                style=Styles.Primary.patch(shape_fill_color=(239, 68, 68, 1.0), shape_line_width=1.5),
            )
            cp.add("GA", style=Styles.SuccessFlat, show=False)

            cp.draw(xy=(10.0, 45.0), width=80.0, height=12.0, item_width=22.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_empty_process(self) -> None:
        """Test rendering an empty ChevronProcess does not raise."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "chevron_empty.png"
            canvas.clear()

            cp = ChevronProcess(
                style=Styles.PrimarySolid,
                text_style=Styles.WhiteBold,
                description_style=Styles.White,
            )
            cp.draw(xy=(10.0, 40.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
