# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.smartarts (Panel)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from drawlib import canvas
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Colors, Styles


class TestPanelUnit:
    """Unit tests for Panel configuration, style validation, and content box calculation."""

    def test_default_initialization(self) -> None:
        """Verify Panel explicit style initialization values."""
        p = Panel(
            "Service Group",
            style=Styles.Neutral,
            header_style=Styles.PrimaryFlat,
            text_style=Styles.WhiteBold,
        )
        assert p.text == "Service Group"
        assert p.description == ""
        assert p.header_variant == "filled"
        assert p.header_height == 8.0
        assert p.header_align == "left"
        assert p.show is True

    def test_missing_optional_element_styles_raise_error(self) -> None:
        """Verify displaying description, icon, or window dots without their Style raises ValueError."""
        with pytest.raises(ValueError, match="description_style"):
            Panel(
                "Panel",
                "Subtitle without style",
                style=Styles.Neutral,
                header_style=Styles.PrimaryFlat,
                text_style=Styles.WhiteBold,
            )

        with pytest.raises(ValueError, match="icon_style"):
            Panel(
                "Panel",
                style=Styles.Neutral,
                header_style=Styles.PrimaryFlat,
                text_style=Styles.WhiteBold,
                icon=phosphor.gear,
            )

        with pytest.raises(ValueError, match="dot_styles"):
            Panel(
                "Window Panel",
                style=Styles.Neutral,
                header_style=Styles.DarkFlat,
                text_style=Styles.WhiteBold,
                header_variant="window",
            )

        with pytest.raises(ValidationError):
            Panel(
                "Invalid Variant",
                style=Styles.Neutral,
                header_style=Styles.PrimaryFlat,
                text_style=Styles.WhiteBold,
                header_variant="unknown",  # ty: ignore[invalid-argument-type]
            )

    def test_post_init_mutation_validation_on_draw(self) -> None:
        """Verify mutating Panel attributes to display an element without its Style fails on draw()."""
        p = Panel(
            "Panel",
            style=Styles.Neutral,
            header_style=Styles.PrimaryFlat,
            text_style=Styles.WhiteBold,
        )
        p.description = "Added later without style"
        canvas.clear()
        with pytest.raises(ValueError, match="description_style"):
            p.draw((10, 10), width=80, height=50)

    def test_get_content_box_calculation(self) -> None:
        """Verify get_content_box returns accurate inner (xy, width, height) for scalar and tuple padding."""
        p = Panel(
            "Container",
            style=Styles.Neutral,
            header_style=Styles.PrimaryFlat,
            text_style=Styles.WhiteBold,
            header_height=10.0,
        )
        inner_xy, inner_w, inner_h = p.get_content_box(
            (10.0, 20.0),
            width=100.0,
            height=60.0,
            padding=(5.0, 4.0),
        )
        assert inner_xy == (15.0, 24.0)
        assert inner_w == 90.0
        assert inner_h == 42.0  # 60 - 10 - 4*2

        inner_xy_s, inner_w_s, inner_h_s = p.get_content_box(
            (10.0, 20.0),
            width=100.0,
            height=60.0,
            padding=5.0,
            scale=0.5,
        )
        assert inner_xy_s == (12.5, 22.5)
        assert inner_w_s == 45.0
        assert inner_h_s == 20.0


class TestPanelIntegration:
    """Integration tests rendering all 4 Panel variants onto a canvas."""

    def test_draw_all_variants_and_alignments(self) -> None:
        """Verify rendering filled, underline, floating, and window variants."""
        canvas.setup(width=180, height=120)

        # 1. Filled
        p_filled = Panel(
            "1. Filled Header",
            "Q1-Q2",
            style=Styles.Neutral,
            header_style=Styles.PrimaryFlat,
            text_style=Styles.WhiteBold,
            description_style=Styles.White,
            icon=phosphor.compass,
            icon_style=Styles.White,
            header_variant="filled",
        )
        p_filled.draw((8, 64), width=78, height=48)

        # 2. Underline (center aligned)
        p_underline = Panel(
            "2. Underline Header",
            "v2.0",
            style=Styles.SecondaryNeutral,
            header_style=Styles.SecondaryFlat,
            text_style=Styles.SecondaryBold,
            description_style=Styles.Muted,
            icon=phosphor.chart_line_up,
            icon_style=Styles.Secondary,
            header_variant="underline",
            header_align="center",
        )
        p_underline.draw((94, 64), width=78, height=48)

        # 3. Floating (center aligned + 4-tuple shape_r)
        p_floating = Panel(
            "3. Floating Badge",
            "Tag",
            style=Styles.AccentNeutral.patch(shape_r=(2.5, 2.5, 2.5, 2.5)),
            header_style=Styles.AccentFlat,
            text_style=Styles.WhiteBold,
            description_style=Styles.Muted,
            icon=phosphor.flag_banner,
            icon_style=Styles.White,
            header_variant="floating",
            header_align="center",
        )
        p_floating.draw((8, 8), width=78, height=48)

        # 4. Window (3 dot styles + single dot style)
        p_window = Panel(
            "4. Window Chrome",
            "bash",
            style=Styles.Neutral,
            header_style=Styles.DarkFlat,
            text_style=Styles.WhiteBold,
            description_style=Styles.Light,
            icon=phosphor.terminal_window,
            icon_style=Styles.White,
            dot_styles=(
                Styles.DangerFlat.patch(shape_line_width=0),
                Styles.WarningFlat.patch(shape_line_width=0),
                Styles.SuccessFlat.patch(shape_line_width=0),
            ),
            header_variant="window",
            header_align="center",
        )
        p_window.draw((94, 8), width=78, height=48)

        # 5. Window with single dot_style & show=False
        p_hidden = Panel(
            "Hidden",
            style=Styles.Neutral,
            header_style=Styles.DarkFlat,
            text_style=Styles.WhiteBold,
            dot_styles=Styles.PrimaryFlat.patch(shape_fill_color=Colors.Primary),
            header_variant="window",
            show=False,
        )
        p_hidden.draw((10, 10), width=40, height=30)

        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "panel_test.png"
            canvas.save(str(out))
            assert out.exists()
            assert out.stat().st_size > 0

    def test_panel_align_center(self) -> None:
        """Verify Panel.draw(align='center') and get_content_box(align='center', content_align=...)."""
        canvas.clear()
        canvas.setup(width=100, height=100)
        p = Panel(
            "Centered Panel",
            style=Styles.Neutral,
            header_style=Styles.PrimaryFlat,
            text_style=Styles.WhiteBold,
            header_height=10.0,
        )
        # align="center" defaults content_align to "center"
        c_xy, c_w, c_h = p.get_content_box((50, 50), width=60, height=40, padding=4.0, align="center")
        assert c_xy == pytest.approx((50.0, 45.0))
        assert c_w == pytest.approx(52.0)
        assert c_h == pytest.approx(22.0)

        # Explicit content_align="bottom_left" with align="center"
        bl_xy, bl_w, bl_h = p.get_content_box(
            (50, 50),
            width=60,
            height=40,
            padding=4.0,
            align="center",
            content_align="bottom_left",
        )
        assert bl_xy == pytest.approx((24.0, 34.0))
        assert bl_w == pytest.approx(52.0)
        assert bl_h == pytest.approx(22.0)

        p.draw((50, 50), width=60, height=40, align="center")
