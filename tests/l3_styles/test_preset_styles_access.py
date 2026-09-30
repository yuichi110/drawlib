# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for PascalCase class and instance access for Styles and Colors."""

import drawlib.styles as ds
from drawlib._core.types import Color, Style
from drawlib._preset_colors import (
    DefaultColors,
    GoogleColors,
    MonochromeColors,
)
from drawlib._preset_styles import (
    DefaultStyles,
    GoogleStyles,
    MonochromeStyles,
)

default_colors = DefaultColors()
google_colors = GoogleColors()
monochrome_colors = MonochromeColors()

_ds_inst = DefaultStyles.get_default_instance()
assert isinstance(_ds_inst, DefaultStyles)
default_styles = _ds_inst

_gs_inst = GoogleStyles.get_default_instance()
assert isinstance(_gs_inst, GoogleStyles)
google_styles = _gs_inst

_ms_inst = MonochromeStyles.get_default_instance()
assert isinstance(_ms_inst, MonochromeStyles)
monochrome_styles = _ms_inst


class TestPresetStylesPascalCaseAccess:
    """Test cases for PascalCase and class-level access on preset styles."""

    def test_default_styles_class_access(self) -> None:
        """Test DefaultStyles class attributes access in PascalCase and snake_case."""
        assert isinstance(DefaultStyles.RedFlat, Style)
        assert DefaultStyles.RedFlat == default_styles.red_flat
        assert DefaultStyles.red_flat == default_styles.red_flat
        assert DefaultStyles.Primary == default_styles.primary
        assert DefaultStyles.primary == default_styles.primary
        assert DefaultStyles.Blue1Flat == default_styles.blue1_flat
        assert DefaultStyles.PrimaryOutlineBold == default_styles.primary_outline_bold
        assert DefaultStyles.CanvasFlat == default_styles.canvas_flat
        assert DefaultStyles.width == 140
        assert DefaultStyles.height == 70

    def test_default_styles_dict_and_dir(self) -> None:
        """Test dictionary and dir() reflection for PascalCase style names."""
        assert DefaultStyles["RedFlat"] == default_styles.red_flat
        assert default_styles["RedFlat"] == default_styles.red_flat
        assert "RedFlat" in dir(DefaultStyles)
        assert "RedFlat" in dir(default_styles)
        assert "Primary" in dir(DefaultStyles)

    def test_google_styles_class_access(self) -> None:
        """Test GoogleStyles class attributes access."""
        assert isinstance(GoogleStyles.BlueFlat, Style)
        assert GoogleStyles.BlueFlat == google_styles.blue_flat
        assert GoogleStyles.CornflowerBlue1DashedLight == google_styles.cornflower_blue1_dashed_light
        assert GoogleStyles.Primary == google_styles.primary

    def test_monochrome_styles_class_access(self) -> None:
        """Test MonochromeStyles class attributes access."""
        assert isinstance(MonochromeStyles.Primary, Style)
        assert MonochromeStyles.Primary == monochrome_styles.primary
        assert MonochromeStyles.Gray5Flat == monochrome_styles.gray5_flat

    def test_styles_module_facade(self) -> None:
        """Test drawlib.styles active facade with Styles and Colors."""
        orig_s, orig_c = ds.Styles, ds.Colors
        try:
            ds.Styles = DefaultStyles
            ds.Colors = DefaultColors
            # Default theme
            assert ds.Styles.RedFlat == default_styles.red_flat
            assert ds.Colors.Red == default_colors.Red
            assert ds.Colors.Transparent == Color(0, 0, 0, 0.0)
            assert ds.Colors.Primary == default_colors.Primary

            # Switch to Google theme via classes
            ds.Styles = GoogleStyles
            ds.Colors = GoogleColors
            assert ds.Styles.BlueFlat == google_styles.blue_flat
            assert ds.Colors.Red == google_colors.Red
            assert ds.Colors.Transparent == Color(0, 0, 0, 0.0)
        finally:
            ds.Styles = orig_s
            ds.Colors = orig_c


class TestPresetColorsPascalCaseAccess:
    """Test cases for PascalCase and class-level access on preset colors."""

    def test_default_colors_class_access(self) -> None:
        """Test DefaultColors class attributes in PascalCase and lowercase."""
        assert isinstance(DefaultColors.Red, Color)
        assert DefaultColors.Red == (255, 23, 23)
        assert DefaultColors.red == (255, 23, 23)
        assert DefaultColors.Primary == (72, 98, 218)
        assert DefaultColors.primary == (72, 98, 218)
        assert DefaultColors.Transparent == (0, 0, 0, 0.0)
        assert DefaultColors.transparent == (0, 0, 0, 0.0)
        assert DefaultColors.Blue1 == (232, 242, 255)
        assert DefaultColors.blue1 == (232, 242, 255)
        assert DefaultColors.Blue4 == (72, 98, 218)
        assert DefaultColors.blue4 == (72, 98, 218)
        assert DefaultColors.Blue6 == (18, 32, 95)
        assert DefaultColors.blue6 == (18, 32, 95)

    def test_default_colors_dict_and_dir(self) -> None:
        """Test dictionary access on class and instance."""
        assert DefaultColors["Red"] == (255, 23, 23)
        assert DefaultColors["red"] == (255, 23, 23)
        assert default_colors["Red"] == (255, 23, 23)
        assert default_colors["red"] == (255, 23, 23)
        assert DefaultColors["Transparent"] == (0, 0, 0, 0.0)
        assert DefaultColors["transparent"] == (0, 0, 0, 0.0)
