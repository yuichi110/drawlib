# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for hole_ratio and expanded shapes in drawlib.shapes."""

import pytest
from pydantic import ValidationError

from drawlib.canvas import canvas, clear
from drawlib.fonts import Font
from drawlib.shapes import (
    checkmark,
    circle,
    clock,
    ellipse,
    explosion,
    forbidden,
    funnel,
    heart,
    lightning,
    moon,
    parallelogram,
    pin,
    plaque,
    rectangle,
    regularpolygon,
    rhombus,
    ribbon,
    shield,
    sun,
    tag,
    trapezoid,
    triangle,
)
from drawlib.styles import Colors, Style, Styles


class TestHoleRatioShapes:
    """Tests for hole_ratio parameter across basic and polygon shapes."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_basic_shapes_hole_ratio(self) -> None:
        """Verify hole_ratio rendering on circle, ellipse, rectangle, and regularpolygon."""
        circle((25, 50), radius=15, hole_ratio=0.5, style=Styles.PrimaryNeutral, text="C")
        ellipse((50, 50), width=30, height=20, hole_ratio=0.4, style=Styles.SecondaryNeutral.patch(angle=20), text="E")
        rectangle(
            (75, 50),
            width=24,
            height=18,
            hole_ratio=0.5,
            style=Styles.AccentNeutral.patch(shape_r=1.5),
            text="R",
        )
        regularpolygon(
            (50, 20),
            radius=14,
            num_vertex=6,
            hole_ratio=0.5,
            style=Styles.SuccessNeutral.patch(shape_r=1.0, angle=15),
            text="P",
        )
        assert len(canvas._artists) == 8  # 4 hollow PathPatches + 4 Text artists

    def test_polygon_shapes_hole_ratio(self) -> None:
        """Verify hole_ratio rendering on triangle, parallelogram, trapezoid, and rhombus."""
        triangle(
            (20, 50),
            width=24,
            height=20,
            hole_ratio=0.4,
            style=Styles.PrimaryNeutral.patch(shape_r=1.0),
            text="T",
        )
        parallelogram(
            (45, 50),
            width=24,
            height=18,
            corner_angle=65,
            hole_ratio=0.45,
            style=Styles.SecondaryNeutral.patch(shape_r=(0.5, 1.0, 0.5, 1.0)),
            text="Pa",
        )
        trapezoid(
            (70, 50),
            bottomedge_width=26,
            height=18,
            topedge_width=16,
            hole_ratio=0.4,
            style=Styles.WarningNeutral.patch(angle=10),
            text="Tr",
        )
        rhombus(
            (50, 20),
            width=24,
            height=18,
            hole_ratio=0.5,
            style=Styles.DangerNeutral.patch(shape_r=1.0),
            text="Rh",
        )
        assert len(canvas._artists) == 8  # 4 hollow PathPatches + 4 Text artists

    def test_hole_ratio_validation_errors(self) -> None:
        """Verify hole_ratio boundary validation errors."""
        for bad_ratio in (0.0, 1.0, -0.2, 1.5):
            with pytest.raises((ValueError, ValidationError)):
                circle((50, 50), radius=10, hole_ratio=bad_ratio, style=Styles.Neutral)
            with pytest.raises((ValueError, ValidationError)):
                ellipse((50, 50), width=20, height=10, hole_ratio=bad_ratio, style=Styles.Neutral)
            with pytest.raises((ValueError, ValidationError)):
                rectangle((50, 50), width=20, height=10, hole_ratio=bad_ratio, style=Styles.Neutral)
            with pytest.raises((ValueError, ValidationError)):
                regularpolygon((50, 50), radius=10, num_vertex=5, hole_ratio=bad_ratio, style=Styles.Neutral)
            with pytest.raises((ValueError, ValidationError)):
                triangle((50, 50), width=20, height=15, hole_ratio=bad_ratio, style=Styles.Neutral)
            with pytest.raises((ValueError, ValidationError)):
                parallelogram(
                    (50, 50),
                    width=20,
                    height=15,
                    corner_angle=60,
                    hole_ratio=bad_ratio,
                    style=Styles.Neutral,
                )
            with pytest.raises((ValueError, ValidationError)):
                trapezoid(
                    (50, 50),
                    bottomedge_width=20,
                    height=15,
                    topedge_width=12,
                    hole_ratio=bad_ratio,
                    style=Styles.Neutral,
                )
            with pytest.raises((ValueError, ValidationError)):
                rhombus((50, 50), width=20, height=15, hole_ratio=bad_ratio, style=Styles.Neutral)


class TestExpandedBasicShapes:
    """Tests for the 10 new basic shapes in CanvasShapeBasicFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_exports(self) -> None:
        """Verify all 10 new basic shapes are exported on drawlib.shapes and canvas."""
        for fn, name in (
            (forbidden, "forbidden"),
            (checkmark, "checkmark"),
            (shield, "shield"),
            (ribbon, "ribbon"),
            (funnel, "funnel"),
            (pin, "pin"),
            (heart, "heart"),
            (sun, "sun"),
            (moon, "moon"),
            (clock, "clock"),
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

    def test_shield_ribbon_funnel(self) -> None:
        """Test shield, ribbon, and funnel across all variants."""
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
        for fnv in ("standard", "flat", "3d", "cylinder", "curved"):
            funnel(
                (75, 50),
                width=24,
                height=22,
                variant=fnv,
                neck_width_ratio=0.3,
                neck_height_ratio=0.35,
                style=Styles.SecondaryNeutral.patch(angle=-5),
                text="Filter",
            )
        assert len(canvas._artists) > 20

        with pytest.raises((ValueError, ValidationError)):
            ribbon((50, 50), width=30, height=12, tail_width_ratio=0.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            ribbon((50, 50), width=30, height=12, drop_ratio=1.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            funnel((50, 50), width=20, height=20, neck_width_ratio=1.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            funnel((50, 50), width=20, height=20, neck_height_ratio=0.0, style=Styles.Primary)

    def test_pin_heart_sun_moon(self) -> None:
        """Test pin, heart, sun, and moon across all variants."""
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
        for hv in ("standard", "classic", "broken"):
            heart(
                (40, 50),
                width=20,
                height=18,
                variant=hv,
                style=Styles.DangerNeutral.patch(angle=-15),
                text="H",
            )
        for suv in ("rays", "standard", "ring", "beams"):
            sun(
                (60, 50),
                radius=14,
                variant=suv,
                num_rays=10,
                style=Styles.WarningFlat.patch(angle=30),
                text="S",
            )
        for mv in ("crescent", "standard", "thin", "waxing", "half"):
            moon(
                (80, 50),
                width=18,
                height=22,
                variant=mv,
                mirror=True,
                style=Styles.AccentNeutral.patch(angle=10),
                text="M",
            )
        assert len(canvas._artists) >= 36

        with pytest.raises((ValueError, ValidationError)):
            pin((50, 50), width=16, height=22, hole_ratio=1.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            sun((50, 50), radius=12, num_rays=2, style=Styles.Warning)

    def test_clock_all_variants(self) -> None:
        """Test clock across all variants including font-free digital 7-segment rendering."""
        tstyle = Style(text_color=Colors.Black, text_size=10, text_font=Font.SANSSERIF_BOLD)
        for cv in ("standard", "ticks", "dial", "stopwatch", "timer", "alarm", "digital"):
            clock(
                (50, 50),
                radius=14,
                variant=cv,
                hour=23,
                minute=48,
                style=Styles.PrimaryNeutral.patch(angle=15),
                text="SLA",
                text_style=tstyle,
            )
        assert len(canvas._artists) > 14

        # Digital clock covering all digits 0-9
        clear()
        clock((30, 50), radius=12, variant="digital", hour=10, minute=56, style=Styles.SecondaryFlat)
        clock((70, 50), radius=12, variant="digital", hour=47, minute=89, style=Styles.Neutral)
        assert len(canvas._artists) >= 4


class TestExpandedPolygonShapes:
    """Tests for the 4 new polygon shapes in CanvasShapePolygonFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_exports(self) -> None:
        """Verify lightning, explosion, tag, and plaque are exported."""
        for fn, name in (
            (lightning, "lightning"),
            (explosion, "explosion"),
            (tag, "tag"),
            (plaque, "plaque"),
        ):
            assert callable(fn)
            assert hasattr(canvas, name)

    def test_lightning_and_explosion(self) -> None:
        """Test lightning and explosion across all variants, shape_r, rotation, and text."""
        for lv in ("standard", "flat", "double", "flat_double", "angled", "slanted"):
            lightning(
                (30, 50),
                width=18,
                height=26,
                variant=lv,
                mirror=(lv == "angled"),
                style=Styles.WarningFlat.patch(shape_r=0.4, angle=15),
                text="Zap",
            )
        for ev in ("standard", "irregular", "heavy", "wild", "curved", "comic"):
            explosion(
                (70, 50),
                width=28,
                height=24,
                variant=ev,
                style=Styles.DangerFlat.patch(shape_r=0.4, angle=-10),
                text="Boom!",
            )
        assert len(canvas._artists) == 24  # 12 shapes + 12 texts

    def test_tag_and_plaque(self) -> None:
        """Test tag and plaque across all variants, hole_ratio, cut_ratio, and text."""
        for tv in ("angled", "standard", "chamfered", "beveled", "rounded"):
            tag(
                (30, 50),
                width=28,
                height=14,
                variant=tv,
                mirror=(tv == "beveled"),
                hole_ratio=0.22,
                style=Styles.PrimaryNeutral.patch(shape_r=0.5, angle=25),
                text="v2.0",
            )

        for pv in ("concave", "standard", "chamfered", "octagon", "notched"):
            plaque(
                (70, 50),
                width=30,
                height=18,
                variant=pv,
                cut_ratio=0.2,
                style=Styles.SecondaryNeutral.patch(shape_r=0.4, angle=-10),
                text="VIP",
            )
        assert len(canvas._artists) == 20

        with pytest.raises((ValueError, ValidationError)):
            tag((50, 50), width=24, height=12, hole_ratio=0.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            tag((50, 50), width=24, height=12, hole_ratio=1.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            plaque((50, 50), width=24, height=16, cut_ratio=1.0, style=Styles.Primary)
        with pytest.raises((ValueError, ValidationError)):
            plaque((50, 50), width=24, height=16, cut_ratio=0.0, style=Styles.Primary)
