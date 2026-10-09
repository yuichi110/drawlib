# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Canvas cylinder shape in drawlib.shapes."""

import pytest
from pydantic import ValidationError

from drawlib.canvas import canvas, clear
from drawlib.fonts import Font
from drawlib.shapes import cylinder
from drawlib.styles import Colors, Style, Styles


class TestCanvasCylinder:
    """Tests for the cylinder drawing feature in CanvasShapeBasicFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_imports_and_availability(self) -> None:
        """Verify cylinder function is exported and callable."""
        assert callable(cylinder)
        assert hasattr(canvas, "cylinder")

    def test_basic_cylinder_rendering(self) -> None:
        """Verify basic cylinder rendering across flat, bordered, and outline styles."""
        # 1. Flat style (with automatic lighter top cap)
        cylinder((30, 50), width=20, height=30, style=Styles.PrimaryFlat)
        assert len(canvas._artists) == 2  # body + top cap

        # 2. Bordered style (body + top cap + outline path)
        clear()
        cylinder((30, 50), width=20, height=30, style=Styles.Primary)
        assert len(canvas._artists) == 3  # body + top cap + outline

        # 3. Outline style (transparent fill)
        clear()
        cylinder((30, 50), width=20, height=30, style=Styles.PrimaryOutline)
        assert len(canvas._artists) == 3

    def test_multi_disk_cylinder(self) -> None:
        """Verify multi-disk cylinder rendering for database visualization."""
        # Flat multi-disk (disks=3: body + top cap + 2 divider crease patches)
        cylinder((30, 50), width=20, height=30, style=Styles.PrimaryFlat, disks=3)
        assert len(canvas._artists) == 4  # 2 base + 2 divider patches

        # Bordered multi-disk (disks=3: body + top cap + outline + 2 divider stroke patches)
        clear()
        cylinder((30, 50), width=20, height=30, style=Styles.Primary, disks=3)
        assert len(canvas._artists) == 5  # 3 base + 2 divider patches

    def test_cylinder_with_text(self) -> None:
        """Verify cylinder with centered embedded text label."""
        cylinder(
            (50, 50),
            width=24,
            height=32,
            style=Styles.PrimaryFlat,
            text="PostgreSQL",
            text_style=Style(text_color=Colors.White, text_size=12, text_font=Font.SANSSERIF_BOLD),
        )
        assert len(canvas._artists) == 3  # 2 shape patches + 1 text artist

    def test_cylinder_rotation(self) -> None:
        """Verify cylinder rendering with rotation angles."""
        # Tilted 45 degrees
        cylinder((50, 50), width=20, height=30, style=Styles.Primary.patch(angle=45.0))
        assert len(canvas._artists) == 3

        # Horizontal cylinder (90 degrees)
        clear()
        cylinder((50, 50), width=20, height=30, style=Styles.PrimaryFlat.patch(angle=90.0))
        assert len(canvas._artists) == 2

    def test_cylinder_alpha_transparency(self) -> None:
        """Verify semi-transparent cylinder styling."""
        style = Styles.PrimaryFlat.patch(alpha=0.4)
        cylinder((50, 50), width=20, height=30, style=style)
        assert len(canvas._artists) == 2

    def test_validation_errors(self) -> None:
        """Verify runtime parameter validation via @validate_call and value checks."""
        # Non-positive width
        with pytest.raises((ValueError, ValidationError)):
            cylinder((50, 50), width=0, height=30, style=Styles.PrimaryFlat)

        with pytest.raises((ValueError, ValidationError)):
            cylinder((50, 50), width=-10, height=30, style=Styles.PrimaryFlat)

        # Non-positive height
        with pytest.raises((ValueError, ValidationError)):
            cylinder((50, 50), width=20, height=0, style=Styles.PrimaryFlat)

        # Invalid disks (< 1)
        with pytest.raises((ValueError, ValidationError)):
            cylinder((50, 50), width=20, height=30, disks=0, style=Styles.PrimaryFlat)

        # Invalid style type
        with pytest.raises((TypeError, ValidationError)):
            cylinder((50, 50), width=20, height=30, style="invalid")  # type: ignore
