# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from pydantic import BaseModel

from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import Style
from drawlib._preset_styles import (
    BasePresetStyles,
    DefaultStyles,
    EssentialsStyles,
    MonochromeStyles,
    PresetStyles,
    default_styles,
)
from drawlib.types import BasePresetStyles as TypesBasePresetStyles
from drawlib.types import PresetStyles as TypesPresetStyles


class TestPresetStyles:
    """Unit tests for the Pydantic-based PresetStyles models."""

    def test_default_styles_instantiation(self) -> None:
        """Verifies DefaultStyles provides valid styles and properties."""
        preset = default_styles

        assert isinstance(preset, BaseModel)
        assert isinstance(preset, BasePresetStyles)
        assert isinstance(preset, PresetStyles)
        assert isinstance(preset, DefaultStyles)
        assert isinstance(preset.primary, Style)
        assert isinstance(preset.light, Style)
        assert isinstance(preset.bold, Style)
        assert isinstance(preset.flat, Style)
        assert isinstance(preset.solid, Style)
        assert isinstance(preset.dashed, Style)
        assert preset.background_color == (255, 255, 255, 1.0)
        assert preset.sourcecode_font == FontSourceCode.SOURCECODEPRO

    def test_iteration_and_dict_access(self) -> None:
        """Verifies iteration, dictionary access, and styles helper on preset style models."""
        preset = default_styles

        # __iter__ test
        items = dict(preset)
        assert "primary" in items
        assert items["primary"] == preset.primary
        assert items["light"] == preset.light
        assert "background_color" in items

        # __getitem__ test
        assert preset["primary"] == preset.primary
        assert preset["light"] == preset.light

        # get test
        assert preset.get("primary") == preset.primary
        assert preset.get("unknown_key", "default_val") == "default_val"

        # styles() test (only Style instances)
        styles_dict = preset.styles()
        assert "primary" in styles_dict
        assert "background_color" not in styles_dict

    def test_custom_user_defined_styles(self) -> None:
        """Verifies that users can define arbitrary style fields with full autocomplete and iteration."""

        class MyCloudStyles(BasePresetStyles):
            vpc: Style
            subnet: Style
            custom_note: str = "production"

        base = default_styles
        vpc_style = Style(line_color=(0, 100, 200, 1.0), line_width=2.0)
        subnet_style = Style(line_color=(50, 150, 250, 1.0), line_width=1.0)

        my_styles = MyCloudStyles(
            **base.model_dump(),
            vpc=vpc_style,
            subnet=subnet_style,
        )

        assert my_styles.vpc == vpc_style
        assert my_styles.subnet == subnet_style
        assert my_styles.custom_note == "production"

        style_map = dict(my_styles)
        assert style_map["vpc"] == vpc_style
        assert style_map["subnet"] == subnet_style
        assert style_map["custom_note"] == "production"
        assert my_styles["vpc"] == vpc_style
        assert my_styles.get("subnet") == subnet_style

    def test_import_from_types(self) -> None:
        """Verifies that BasePresetStyles and PresetStyles can be imported from drawlib.types."""
        assert TypesBasePresetStyles is BasePresetStyles
        assert TypesPresetStyles is PresetStyles
