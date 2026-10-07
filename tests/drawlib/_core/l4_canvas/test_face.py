# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Canvas face shape in drawlib.shapes."""

import pytest
from pydantic import ValidationError

from drawlib.canvas import canvas, clear
from drawlib.fonts import Font
from drawlib.shapes import face
from drawlib.styles import Colors, Style, Styles


class TestCanvasFace:
    """Tests for the face drawing feature in CanvasShapeBasicFeature."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_imports_and_availability(self) -> None:
        """Verify face function is exported and callable."""
        assert callable(face)
        assert hasattr(canvas, "face")

    def test_basic_face_moods(self) -> None:
        """Verify face rendering across all supported moods."""
        # 1. Default smile mood (1 outer circle + 2 eyes + 1 mouth = 4 artists)
        face((30, 50), radius=10, style=Styles.PrimaryNeutral)
        assert len(canvas._artists) == 4

        # 2. Neutral mood
        clear()
        face((30, 50), radius=10, style=Styles.Neutral, mood="neutral")
        assert len(canvas._artists) == 4

        # 3. Sad mood
        clear()
        face((30, 50), radius=10, style=Styles.WarningNeutral, mood="sad")
        assert len(canvas._artists) == 4

        # 4. Angry mood (1 outer circle + 2 eyes + 1 eyebrows + 1 mouth = 5 artists)
        clear()
        face((30, 50), radius=10, style=Styles.DangerNeutral, mood="angry")
        assert len(canvas._artists) == 5

        # 5. Surprised mood
        clear()
        face((30, 50), radius=10, style=Styles.SecondaryNeutral, mood="surprised")
        assert len(canvas._artists) == 4

    def test_face_styles_and_fallbacks(self) -> None:
        """Verify face rendering with flat, outline, and text_color fallback styles."""
        # Flat style without text_color (falls back to contrast color)
        face((30, 50), radius=10, style=Styles.PrimaryFlat)
        assert len(canvas._artists) == 4

        # Flat neutral style with text_color
        clear()
        face((30, 50), radius=10, style=Styles.PrimaryNeutralFlat)
        assert len(canvas._artists) == 4

        # Outline style (transparent fill)
        clear()
        face((30, 50), radius=10, style=Styles.PrimaryOutline)
        assert len(canvas._artists) == 4

    def test_face_with_text_and_rotation(self) -> None:
        """Verify face with embedded text and rotation angle."""
        face(
            (50, 50),
            radius=12,
            style=Styles.PrimaryNeutral,
            mood="smile",
            angle=30.0,
            text="Actor",
            text_style=Style(text_color=Colors.Black, text_size=12, text_font=Font.SANSSERIF_BOLD),
        )
        assert len(canvas._artists) == 5  # 4 face artists + 1 text artist

    def test_face_alpha_transparency(self) -> None:
        """Verify semi-transparent face styling."""
        style = Styles.PrimaryNeutral.patch(shape_fill_alpha=0.5)
        face((50, 50), radius=10, style=style, mood="smile")
        assert len(canvas._artists) == 4

    def test_validation_errors(self) -> None:
        """Verify runtime parameter validation via @validate_call."""
        # Non-positive radius
        with pytest.raises((ValueError, ValidationError)):
            face((50, 50), radius=0, style=Styles.PrimaryNeutral)

        with pytest.raises((ValueError, ValidationError)):
            face((50, 50), radius=-5, style=Styles.PrimaryNeutral)

        # Invalid mood
        with pytest.raises((ValueError, ValidationError)):
            face((50, 50), radius=10, style=Styles.PrimaryNeutral, mood="invalid")  # type: ignore

        # Invalid style type
        with pytest.raises((TypeError, ValidationError)):
            face((50, 50), radius=10, style="invalid")  # type: ignore
