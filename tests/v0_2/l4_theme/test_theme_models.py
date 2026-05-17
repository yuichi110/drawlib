# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest
from pydantic import ValidationError

from drawlib.v0_2.private.l3_fonts import FontSourceCode
from drawlib.v0_2.private.l3_styles import (
    Colors,
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.l4_theme._theme_models import OfficialThemeStyle, ThemeStyles


class TestThemeStyles:
    """Unit tests for the ThemeStyles Pydantic model."""

    def test_theme_styles_default_none(self) -> None:
        """Verifies that all style fields in ThemeStyles default to None."""
        styles = ThemeStyles()
        assert styles.iconstyle is None
        assert styles.imagestyle is None
        assert styles.linestyle is None
        assert styles.shapestyle is None
        assert styles.shapetextstyle is None
        assert styles.textstyle is None

    def test_theme_styles_valid_assignment(self) -> None:
        """Verifies that assigning valid style objects works and maintains type validation."""
        icon = IconStyle(style="fill", color=Colors.Red)
        styles = ThemeStyles(iconstyle=icon)
        assert styles.iconstyle == icon

        # Valid assignments at runtime
        shape = ShapeStyle(lwidth=2.0)
        styles.shapestyle = shape
        assert styles.shapestyle == shape

    def test_theme_styles_invalid_type_raises(self) -> None:
        """Verifies that assigning invalid types raises ValidationError due to validate_assignment."""
        styles = ThemeStyles()
        with pytest.raises(ValidationError):
            styles.iconstyle = "invalid"  # type: ignore

        with pytest.raises(ValidationError):
            styles.shapestyle = 123  # type: ignore

    def test_theme_styles_extra_fields_forbidden(self) -> None:
        """Verifies that extra fields are forbidden during instantiation."""
        with pytest.raises(ValidationError):
            ThemeStyles(extra_field="not allowed")  # type: ignore


class TestOfficialThemeStyle:
    """Unit tests for the OfficialThemeStyle Pydantic model."""

    def test_official_theme_style_valid(self) -> None:
        """Verifies successful instantiation of OfficialThemeStyle with valid arguments."""
        default_styles = ThemeStyles(
            iconstyle=IconStyle(style="fill"),
            imagestyle=ImageStyle(lwidth=1),
            linestyle=LineStyle(width=2),
            shapestyle=ShapeStyle(lwidth=1.5),
            shapetextstyle=ShapeTextStyle(size=14),
            textstyle=TextStyle(size=14),
        )
        named = [("gold", ThemeStyles(shapestyle=ShapeStyle(lwidth=5.0)))]
        colors = [("red", (255, 0, 0))]
        bg = (255, 255, 255, 1.0)
        font = FontSourceCode.ROBOTO_MONO

        theme = OfficialThemeStyle(
            default_style=default_styles,
            named_styles=named,
            theme_colors=colors,
            backgroundcolor=bg,
            sourcecodefont=font,
        )

        assert theme.default_style == default_styles
        assert theme.named_styles == named
        assert theme.theme_colors == colors
        assert theme.backgroundcolor == bg
        assert theme.sourcecodefont == font

    def test_official_theme_style_invalid_raises(self) -> None:
        """Verifies that instantiation fails if any attribute violates type/config constraints."""
        default_styles = ThemeStyles()
        # Invalid background color type
        with pytest.raises(ValidationError):
            OfficialThemeStyle(
                default_style=default_styles,
                named_styles=[],
                theme_colors=[],
                backgroundcolor=123,  # type: ignore
                sourcecodefont=None,
            )

    def test_official_theme_style_extra_fields_forbidden(self) -> None:
        """Verifies that extra fields are forbidden on instantiation."""
        default_styles = ThemeStyles()
        with pytest.raises(ValidationError):
            OfficialThemeStyle(
                default_style=default_styles,
                named_styles=[],
                theme_colors=[],
                backgroundcolor=(255, 255, 255, 1.0),
                sourcecodefont=None,
                extra_attribute="forbidden",  # type: ignore
            )
