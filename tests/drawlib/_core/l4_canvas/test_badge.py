# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasShapeBadgeFeature shapes."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from drawlib.canvas import canvas, clear, save
from drawlib.shapes import (
    bubblespeech,
    checkmark,
    explosion,
    forbidden,
    pin,
    ribbon,
    shield,
    tag,
)
from drawlib.styles import Colors, Styles

default_styles = Styles
OUTPUT_DIR = "../../../../output_tests/_core/l4_canvas/badge/"


class TestBubblespeech:
    """Tests for the bubblespeech drawing function."""

    def test_validation_ratio_order(self) -> None:
        """Verify error when tail_start_ratio >= tail_end_ratio."""
        styles = default_styles
        with pytest.raises(ValueError, match="tail_start_ratio must be smaller than tail_end_ratio"):
            bubblespeech(
                xy=(30, 30),
                width=50,
                height=40,
                tail_edge="left",
                tail_start_ratio=0.7,
                tail_vertex_xy=(10, 50),
                tail_end_ratio=0.3,
                style=styles.Primary,
            )

        with pytest.raises(ValueError, match="tail_start_ratio must be smaller than tail_end_ratio"):
            bubblespeech(
                xy=(30, 30),
                width=50,
                height=40,
                tail_edge="left",
                tail_start_ratio=0.5,
                tail_vertex_xy=(10, 50),
                tail_end_ratio=0.5,
                style=styles.Primary,
            )

    def test_validation_ratio_bounds(self) -> None:
        """Verify validation errors when ratio is outside [0.0, 1.0]."""
        styles = default_styles
        with pytest.raises(ValidationError):
            bubblespeech(
                xy=(30, 30),
                width=50,
                height=40,
                tail_edge="left",
                tail_start_ratio=-0.1,  # type: ignore[arg-type]
                tail_vertex_xy=(10, 50),
                tail_end_ratio=0.5,
                style=styles.Primary,
            )

        with pytest.raises(ValidationError):
            bubblespeech(
                xy=(30, 30),
                width=50,
                height=40,
                tail_edge="left",
                tail_start_ratio=0.2,
                tail_vertex_xy=(10, 50),
                tail_end_ratio=1.2,  # type: ignore[arg-type]
                style=styles.Primary,
            )

    def test_tail_left(self) -> None:
        """Verify bubblespeech tail rendered on the left edge."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="left",
            tail_start_ratio=0.2,
            tail_vertex_xy=(10, 50),
            tail_end_ratio=0.6,
            style=styles.Primary,
        )
        save(f"{OUTPUT_DIR}test_tail_left.png")

    def test_tail_top(self) -> None:
        """Verify bubblespeech tail rendered on the top edge."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="top",
            tail_start_ratio=0.2,
            tail_vertex_xy=(50, 90),
            tail_end_ratio=0.6,
            style=styles.Primary,
        )
        save(f"{OUTPUT_DIR}test_tail_top.png")

    def test_tail_right(self) -> None:
        """Verify bubblespeech tail rendered on the right edge."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="right",
            tail_start_ratio=0.2,
            tail_vertex_xy=(95, 50),
            tail_end_ratio=0.6,
            style=styles.Primary,
        )
        save(f"{OUTPUT_DIR}test_tail_right.png")

    def test_tail_bottom(self) -> None:
        """Verify bubblespeech tail rendered on the bottom edge."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="bottom",
            tail_start_ratio=0.2,
            tail_vertex_xy=(50, 10),
            tail_end_ratio=0.6,
            style=styles.Primary,
        )
        save(f"{OUTPUT_DIR}test_tail_bottom.png")

    def test_with_text_and_style(self) -> None:
        """Verify bubblespeech drawing with formatted text and custom Style."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="left",
            tail_start_ratio=0.2,
            tail_vertex_xy=(10, 50),
            tail_end_ratio=0.6,
            style=styles.Primary,
            text="Hello Drawlib\nHello Python World!!",
            text_style=styles.Primary.patch(text_color=Colors.Red, text_size=28),
        )
        save(f"{OUTPUT_DIR}test_with_text_style.png")


class TestExpandedBadgeShapes:
    """Tests for badge shapes in CanvasShapeBadgeFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_exports(self) -> None:
        """Verify badge shapes are exported on drawlib.shapes and canvas."""
        for fn, name in (
            (forbidden, "forbidden"),
            (checkmark, "checkmark"),
            (shield, "shield"),
            (ribbon, "ribbon"),
            (pin, "pin"),
            (explosion, "explosion"),
            (tag, "tag"),
        ):
            assert callable(fn)
            assert hasattr(canvas, name)

    def test_forbidden_and_checkmark(self) -> None:
        """Test forbidden and checkmark across all variants, styles, and text."""
        for fv in ("slash", "standard", "backslash", "cross", "no_entry", "minus"):
            forbidden(
                (30, 50),
                radius=12,
                variant=fv,
                thickness_ratio=0.22,
                style=Styles.DangerFlat.patch(angle=15),
                text="No",
            )
        for cv in ("standard", "check", "circle", "solid_circle"):
            checkmark(
                (70, 50),
                width=20,
                height=20,
                variant=cv,
                thickness_ratio=0.22,
                style=Styles.SuccessFlat.patch(shape_r=0.4, angle=-10),
                text="OK",
            )
        # Checkmark with height=None (defaults to width)
        checkmark((70, 20), width=18, style=Styles.SuccessNeutral)
        assert len(canvas._artists) >= 21

        with pytest.raises((ValueError, ValidationError)):
            forbidden((50, 50), radius=10, thickness_ratio=0.0, style=Styles.Danger)
        with pytest.raises((ValueError, ValidationError)):
            checkmark((50, 50), width=20, height=20, thickness_ratio=1.0, style=Styles.Success)

    def test_shield_and_ribbon(self) -> None:
        """Test shield and ribbon across all variants."""
        for sv in ("classic", "standard", "flat", "heater", "round"):
            shield(
                (25, 50),
                width=20,
                height=24,
                variant=sv,
                style=Styles.PrimaryNeutral.patch(angle=10),
                text="Sec",
            )
        for rv in ("down", "standard", "up", "flat", "banner"):
            ribbon(
                (50, 50),
                width=30,
                height=14,
                variant=rv,
                tail_width_ratio=0.2,
                drop_ratio=0.18,
                style=Styles.AccentFlat.patch(angle=5),
                text="v1.0",
            )
        assert len(canvas._artists) >= 20

        with pytest.raises((ValueError, ValidationError)):
            ribbon((50, 50), width=30, height=12, tail_width_ratio=0.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            ribbon((50, 50), width=30, height=12, drop_ratio=1.0, style=Styles.Primary)

    def test_pin_tag_explosion(self) -> None:
        """Test pin, tag, and explosion across all variants and validation."""
        for pv in ("pointer", "standard", "teardrop", "drop", "pin", "badge"):
            pin(
                (20, 50),
                width=16,
                height=22,
                variant=pv,
                hole_ratio=0.35,
                style=Styles.DangerFlat.patch(angle=20),
                text="P",
            )
        for tv in ("angled", "standard", "chamfered", "beveled", "rounded"):
            tag(
                (50, 50),
                width=28,
                height=14,
                variant=tv,
                mirror=(tv == "beveled"),
                hole_ratio=0.22,
                style=Styles.PrimaryNeutral.patch(shape_r=0.5, angle=25),
                text="v2.0",
            )
        for ev in ("standard", "irregular", "heavy", "wild", "curved", "comic"):
            explosion(
                (80, 50),
                width=28,
                height=24,
                variant=ev,
                style=Styles.DangerFlat.patch(shape_r=0.4, angle=-10),
                text="Boom!",
            )
        assert len(canvas._artists) == 34  # 17 shapes + 17 texts

        with pytest.raises((ValueError, ValidationError)):
            pin((50, 50), width=16, height=22, hole_ratio=1.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            tag((50, 50), width=24, height=12, hole_ratio=0.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            tag((50, 50), width=24, height=12, hole_ratio=1.0, style=Styles.Primary)
