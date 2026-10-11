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
        """Verify CardList explicit style initialization values."""
        cl = CardList(
            style=Styles.Neutral,
            text_style=Styles.DarkBold,
        )
        assert cl._badge_shape == "rounded_rect"
        assert cl._direction == "vertical"
        assert cl._spacing == 2.5
        assert cl._show_arrows is False
        assert len(cl.items) == 0

    def test_invalid_init_and_add_arguments_raise_error(self) -> None:
        """Verify invalid spacing, direction, badge_shape, or missing required optional styles raise errors."""
        with pytest.raises(ValidationError):
            CardList(
                style=Styles.Neutral,
                text_style=Styles.DarkBold,
                spacing=-0.5,
            )

        with pytest.raises(ValueError, match="arrow_style"):
            CardList(
                style=Styles.Neutral,
                text_style=Styles.DarkBold,
                show_arrows=True,
            )

        with pytest.raises(ValidationError):
            CardList(
                style=Styles.Neutral,
                text_style=Styles.DarkBold,
                badge_shape="invalid",  # ty: ignore[invalid-argument-type]
            )

        with pytest.raises(ValidationError):
            CardList(
                style=Styles.Neutral,
                text_style=Styles.DarkBold,
                direction="diagonal",  # ty: ignore[invalid-argument-type]
            )

        cl = CardList(style=Styles.Neutral, text_style=Styles.DarkBold)
        with pytest.raises(ValueError, match="description_style"):
            cl.add("Title", "Description without description_style")

        with pytest.raises(ValueError, match="badge_style"):
            cl.add("Title", badge_text="L1", badge_text_style=Styles.WhiteBold)

        with pytest.raises(ValueError, match="badge_text_style"):
            cl.add("Title", badge_text="L1", badge_style=Styles.PrimaryFlat)

        with pytest.raises(ValueError, match="icon_style"):
            cl.add("Title", icon=phosphor.shield_check, badge_style=Styles.PrimaryFlat)

    def test_add_and_mutate_items(self) -> None:
        """Verify adding items, style overrides, and mutating CardListItem instances."""
        cl = CardList(
            style=Styles.Neutral,
            text_style=Styles.DarkBold,
            description_style=Styles.Muted,
            badge_style=Styles.SecondaryFlat,
            badge_text_style=Styles.WhiteBold,
            icon_style=Styles.White,
        )

        item1 = cl.add("Step 1", "Initialize project", badge_text="01")
        item2 = cl.add("Step 2", "Build diagrams", icon=phosphor.gear, show=False)
        item3 = cl.add(
            "Step 3",
            "Review output",
            badge_text="03",
            style=Styles.PrimaryNeutral,
            badge_style=Styles.PrimaryFlat,
        )

        assert len(cl.items) == 3
        assert isinstance(item1, CardListItem)
        assert item1.text == "Step 1"
        assert item1.description == "Initialize project"
        assert item1.badge_text == "01"
        assert item1.show is True
        assert item1.badge_style == Styles.SecondaryFlat

        assert item2.show is False
        assert item3.style == Styles.PrimaryNeutral
        assert item3.badge_style == Styles.PrimaryFlat

        item1.text = "1. Scaffold"
        item1.show = False
        assert cl.items[0].text == "1. Scaffold"
        assert cl.items[0].show is False


class TestCardListRendering:
    """Integration tests verifying canvas rendering across CardList layout modes."""

    def test_render_empty_is_noop(self) -> None:
        """Verify drawing an empty CardList instance succeeds without errors."""
        canvas.clear()
        cl = CardList(style=Styles.Neutral, text_style=Styles.DarkBold)
        res = cl.draw(xy=(10.0, 10.0), width=80.0, height=50.0)
        assert res is cl

    def test_render_vertical_with_badges_and_icons(self) -> None:
        """Test rendering vertical CardList with rounded_rect badges, icons, and badge_text."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cardlist_vertical.png"
            canvas.clear()
            canvas.setup(width=120, height=80)

            cl = CardList(
                style=Styles.Neutral,
                text_style=Styles.DarkBold.patch(text_size=10.5),
                description_style=Styles.Muted.patch(text_size=9.5),
                badge_shape="rounded_rect",
                badge_style=Styles.SecondaryFlat,
                badge_text_style=Styles.WhiteBold.patch(text_size=8.5),
                icon_style=Styles.White,
                direction="vertical",
                spacing=3.0,
            )
            cl.add(
                "Edge Anycast Scrubbing",
                "Drop volumetric UDP/SYN floods at POPs",
                badge_text="L1",
                icon=phosphor.shield_check,
                badge_style=Styles.PrimaryFlat,
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
            )

            cl.draw(xy=(10.0, 10.0), width=100.0, height=60.0)
            canvas.save(str(out_file))

            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_horizontal_with_arrows_and_visibility(self) -> None:
        """Test rendering horizontal CardList with circle badges, connecting arrows, and item.show."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_all = Path(tmpdir) / "cardlist_horiz_all.png"
            file_hidden = Path(tmpdir) / "cardlist_horiz_hidden.png"

            cl = CardList(
                style=Styles.Neutral,
                text_style=Styles.DarkBold.patch(text_size=10.5),
                description_style=Styles.Muted.patch(text_size=9.5),
                badge_shape="circle",
                badge_style=Styles.PrimaryFlat,
                icon_style=Styles.White,
                direction="horizontal",
                show_arrows=True,
                arrow_style=Styles.PrimaryBold,
                spacing=4.5,
            )
            cl.add("1. Write Code", "Python API\nin Markdown", icon=phosphor.code)
            cl.add("2. Build Docs", "Headless SVG\n& HTML build", icon=phosphor.gear)
            item3 = cl.add("3. AI Review", "Grid check &\nself-healing", icon=phosphor.eye)

            canvas.clear()
            canvas.setup(width=120, height=70)
            cl.draw(xy=(10.0, 10.0), width=100.0, height=50.0, scale=0.95)
            canvas.save(str(file_all))

            item3.show = False
            canvas.clear()
            canvas.setup(width=120, height=70)
            cl.draw(xy=(10.0, 10.0), width=100.0, height=50.0, scale=0.95)
            canvas.save(str(file_hidden))

            assert file_all.exists()
            assert file_hidden.exists()
            assert file_all.read_bytes() != file_hidden.read_bytes()

    def test_render_badge_shape_none_and_vertical_arrows(self) -> None:
        """Test rendering CardList with badge_shape='none' and vertical arrows."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "cardlist_nobadge.png"
            canvas.clear()
            canvas.setup(width=100, height=70)

            cl = CardList(
                style=Styles.Neutral,
                text_style=Styles.DarkBold.patch(text_size=10.5),
                badge_shape="none",
                badge_text_style=Styles.PrimaryBold.patch(text_size=10.5),
                icon_style=Styles.Primary,
                direction="vertical",
                show_arrows=True,
                arrow_style=Styles.PrimaryBold,
                spacing=4.5,
            )
            cl.add("Stage A", icon=phosphor.cube)
            cl.add("Stage B", badge_text="02")

            cl.draw(xy=(10.0, 10.0), width=80.0, height=50.0)
            canvas.save(str(out_file))

            assert out_file.exists()
            assert out_file.stat().st_size > 0
