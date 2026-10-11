# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.smartarts (CardList)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from drawlib import canvas
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, CardListItem
from drawlib.styles import Styles


class TestCardListUnit:
    """Unit tests for CardList configuration, validation, and item mutation."""

    def test_default_initialization(self) -> None:
        """Verify default configuration values of CardList."""
        cl = CardList()
        assert cl._badge_shape == "rounded_rect"
        assert cl._direction == "vertical"
        assert cl._spacing == 2.5
        assert cl._show_arrows is False
        assert len(cl.items) == 0

    def test_invalid_init_arguments_raise_error(self) -> None:
        """Verify out-of-range or invalid parameters raise ValueError or ValidationError."""
        with pytest.raises(ValueError, match="spacing"):
            CardList(spacing=-0.5)

        with pytest.raises(ValueError, match="badge_palette"):
            CardList(badge_palette=[])

        with pytest.raises(ValidationError):
            CardList(badge_shape="invalid")  # ty: ignore[invalid-argument-type]

        with pytest.raises(ValidationError):
            CardList(direction="diagonal")  # ty: ignore[invalid-argument-type]

    def test_add_and_mutate_items(self) -> None:
        """Verify adding items, palette cycling, and mutating returned CardListItem instances."""
        palette = [(30, 100, 220), (15, 160, 110)]
        cl = CardList(badge_palette=palette)

        item1 = cl.add(
            "Edge Anycast Scrubbing",
            "Drop volumetric UDP/SYN floods at POPs",
            badge_text="L1",
            icon=phosphor.shield_check,
        )
        item2 = cl.add(
            "Cloud Armor Rate Limiting",
            "Throttle suspicious ASN & JA3 fingerprints",
            badge_text="L2",
            show=False,
        )
        item3 = cl.add(
            "Origin Zero-Trust mTLS",
            style=Styles.PrimaryNeutral,
        )

        assert len(cl.items) == 3
        assert isinstance(item1, CardListItem)
        assert item1.title == "Edge Anycast Scrubbing"
        assert item1.badge_text == "L1"
        assert item1.icon is phosphor.shield_check
        assert item1.show is True
        assert item1.badge_style is not None
        assert item1.badge_style.shape_fill_color == (30, 100, 220)

        assert item2.show is False
        assert item2.badge_style is not None
        assert item2.badge_style.shape_fill_color == (15, 160, 110)

        assert item3.style == Styles.PrimaryNeutral
        assert item3.badge_style is not None
        assert item3.badge_style.shape_fill_color == (30, 100, 220)

        # Mutate returned item
        item1.title = "Updated L1 Scrubbing"
        item1.show = False
        assert cl.items[0].title == "Updated L1 Scrubbing"
        assert cl.items[0].show is False


class TestCardListRendering:
    """Integration tests verifying canvas rendering across CardList layout modes."""

    def test_render_empty_is_noop(self) -> None:
        """Verify drawing an empty CardList instance succeeds without errors."""
        canvas.clear()
        cl = CardList()
        res = cl.draw(xy=(10.0, 10.0), width=80.0, height=50.0)
        assert res is cl

    def test_render_vertical_with_badges_and_arrows(self) -> None:
        """Test rendering vertical stack with icon+text badges and connecting arrows."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cardlist_vertical.png"
            canvas.clear()
            canvas.setup(width=120, height=85)

            cl = CardList(
                direction="vertical",
                badge_shape="rounded_rect",
                show_arrows=True,
                spacing=4.2,
            )
            cl.add(
                "Edge Anycast Scrubbing",
                "Drop volumetric UDP/SYN floods at POPs",
                badge_text="L1",
                icon=phosphor.shield_check,
            )
            cl.add(
                "Cloud Armor Rate Limiting",
                "Throttle suspicious ASN & JA3 fingerprints",
                badge_text="L2",
                icon=phosphor.funnel,
            )
            cl.add(
                "Origin Zero-Trust mTLS",
                "Verify cryptographic workload identity",
                badge_text="L3",
                icon=phosphor.lock_key,
            )

            cl.draw(xy=(10.0, 10.0), width=100.0, height=65.0)
            canvas.save(str(out_file))

            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_horizontal_with_circle_badges_and_visibility(self) -> None:
        """Test rendering horizontal step cards with circle badges, arrows, and item.show toggle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_all = Path(tmpdir) / "cardlist_horiz_all.png"
            file_hidden = Path(tmpdir) / "cardlist_horiz_hidden.png"

            cl = CardList(
                direction="horizontal",
                badge_shape="circle",
                show_arrows=True,
                spacing=4.5,
            )
            cl.add("1. Write Code", "Python API\nin Markdown", icon=phosphor.code)
            cl.add("2. Build Docs", "Headless SVG\n& HTML build", icon=phosphor.gear)
            item3 = cl.add("3. AI Review", "Grid check &\nself-healing", badge_text="3")

            canvas.clear()
            canvas.setup(width=130, height=60)
            cl.draw(xy=(10.0, 10.0), width=110.0, height=40.0, scale=0.95)
            canvas.save(str(file_all))

            item3.show = False
            canvas.clear()
            canvas.setup(width=130, height=60)
            cl.draw(xy=(10.0, 10.0), width=110.0, height=40.0, scale=0.95)
            canvas.save(str(file_hidden))

            assert file_all.exists()
            assert file_hidden.exists()
            assert file_all.read_bytes() != file_hidden.read_bytes()

    def test_render_without_badges(self) -> None:
        """Test rendering CardList when badge_shape='none' or no icons/badges are provided."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cardlist_nobadge.png"
            canvas.clear()
            canvas.setup(width=100, height=60)

            cl = CardList(badge_shape="none", direction="vertical")
            cl.add("Pure Vector Engine", "No external GUI handoffs")
            cl.add("Single Source of Truth")
            cl.draw(xy=(10.0, 10.0), width=80.0, height=40.0)
            canvas.save(str(out_file))

            assert out_file.exists()
            assert out_file.stat().st_size > 0
