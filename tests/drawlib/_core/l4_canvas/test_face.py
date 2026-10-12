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

    def test_basic_face_variants(self) -> None:
        """Verify face rendering across all supported variants."""
        # 1. Default smile variant (1 outer circle + 2 eyes + 1 mouth = 4 artists)
        face((30, 50), radius=10, style=Styles.PrimaryNeutral)
        assert len(canvas._artists) == 4

        # 2. Neutral variant
        clear()
        face((30, 50), radius=10, style=Styles.Neutral, variant="neutral")
        assert len(canvas._artists) == 4

        # 3. Sad variant
        clear()
        face((30, 50), radius=10, style=Styles.WarningNeutral, variant="sad")
        assert len(canvas._artists) == 4

        # 4. Angry variant (1 outer circle + 2 eyes + 1 eyebrows + 1 mouth = 5 artists)
        clear()
        face((30, 50), radius=10, style=Styles.DangerNeutral, variant="angry")
        assert len(canvas._artists) == 5

        # 5. Surprised variant
        clear()
        face((30, 50), radius=10, style=Styles.SecondaryNeutral, variant="surprised")
        assert len(canvas._artists) == 4

        # 6. Dizzy variant (1 outer circle + 1 X-eyes path + 1 mouth = 3 artists)
        clear()
        face((30, 50), radius=10, style=Styles.WarningNeutral, variant="dizzy")
        assert len(canvas._artists) == 3

        # 7. Dead variant (1 outer circle + 1 X-eyes path + 1 mouth/tongue path = 3 artists)
        clear()
        face((30, 50), radius=10, style=Styles.DangerNeutral, variant="dead")
        assert len(canvas._artists) == 3

        # 8. Skull variant (1 skull silhouette + 2 eye sockets + 1 nasal + 1 teeth = 5 artists)
        clear()
        face((30, 50), radius=10, style=Styles.Neutral, variant="skull")
        assert len(canvas._artists) == 5

        # 9. Devil variant (1 head/horns path + 2 eyes + 1 eyebrows + 1 mouth = 5 artists)
        clear()
        face((30, 50), radius=10, style=Styles.DangerFlat, variant="devil")
        assert len(canvas._artists) == 5

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
            style=Styles.PrimaryNeutral.patch(angle=30.0),
            variant="smile",
            text="Actor",
            text_style=Style(text_color=Colors.Black, text_size=12, text_font=Font.SANSSERIF_BOLD),
        )
        assert len(canvas._artists) == 5  # 4 face artists + 1 text artist

    def test_face_alpha_transparency(self) -> None:
        """Verify semi-transparent face styling."""
        style = Styles.PrimaryNeutral.patch(alpha=0.5)
        face((50, 50), radius=10, style=style, variant="smile")
        assert len(canvas._artists) == 4

    def test_validation_errors(self) -> None:
        """Verify runtime parameter validation via @validate_call."""
        # Non-positive radius
        with pytest.raises((ValueError, ValidationError)):
            face((50, 50), radius=0, style=Styles.PrimaryNeutral)

        with pytest.raises((ValueError, ValidationError)):
            face((50, 50), radius=-5, style=Styles.PrimaryNeutral)

        # Invalid variant
        with pytest.raises((ValueError, ValidationError)):
            face((50, 50), radius=10, style=Styles.PrimaryNeutral, variant="invalid")  # type: ignore

        # Invalid style type
        with pytest.raises((TypeError, ValidationError)):
            face((50, 50), radius=10, style="invalid")  # type: ignore
