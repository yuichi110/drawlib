# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest
from pydantic import BaseModel

from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import Style
from drawlib._preset_styles import (
    BaseStyles,
    DefaultStyles,
    GoogleStyles,
    MonochromeStyles,
)
from drawlib.types import BaseStyles as TypesBaseStyles

_ds_inst = DefaultStyles.get_default_instance()
assert isinstance(_ds_inst, DefaultStyles)
default_styles = _ds_inst

_gs_inst = GoogleStyles.get_default_instance()
assert isinstance(_gs_inst, GoogleStyles)
google_styles = _gs_inst


class TestPresetStyles:
    """Unit tests for the Pydantic-based PresetStyles models."""

    def test_default_styles_instantiation(self) -> None:
        """Verifies DefaultStyles provides valid styles and properties."""
        preset = default_styles

        assert isinstance(preset, BaseModel)
        assert isinstance(preset, BaseStyles)
        assert isinstance(preset, DefaultStyles)
        assert isinstance(preset.Primary, Style)
        assert isinstance(preset.PrimaryThin, Style)
        assert isinstance(preset.PrimaryBold, Style)
        assert isinstance(preset.PrimaryFlat, Style)
        assert isinstance(preset.PrimarySolid, Style)
        assert isinstance(preset.PrimaryDashed, Style)
        assert isinstance(preset.PrimaryDotted, Style)
        assert isinstance(preset.Warning, Style)
        assert isinstance(preset.WarningDotted, Style)
        assert isinstance(preset.Neutral, Style)
        assert isinstance(preset.NeutralFlat, Style)
        assert isinstance(preset.GrayNeutral, Style)
        assert isinstance(preset.GrayNeutralFlat, Style)
        assert isinstance(preset.PrimaryNeutral, Style)
        assert isinstance(preset.PrimaryNeutralFlat, Style)
        assert isinstance(preset.BlueNeutral, Style)
        assert isinstance(preset.BlueNeutralFlat, Style)
        assert preset.background_color == (255, 255, 255, 1.0)
        assert preset.sourcecode_font == FontSourceCode.SOURCECODEPRO

        # Verify snake_case raises AttributeError
        with pytest.raises(AttributeError):
            _ = preset.primary
        with pytest.raises(AttributeError):
            _ = preset.primary_flat

    def test_default_styles_completeness(self) -> None:
        """Verifies DefaultStyles provides all variants across all colors without omission."""
        preset = default_styles
        assert len(preset.styles()) == 2233
        variants = ["Flat", "Solid", "Dashed", "Bold", "Thin", "Dotted"]
        colors = [
            "Red",
            "Green",
            "Blue",
            "Yellow",
            "Purple",
            "Orange",
            "Navy",
            "Pink",
            "Cyan",
            "Magenta",
            "Lime",
            "Teal",
            "Olive",
            "Brown",
            "Gold",
            "Aqua",
            "GreenYellow",
            "Ivory",
            "Steel",
            "White",
            "Gray1",
            "Gray2",
            "Gray3",
            "Gray4",
            "Gray5",
            "Gray6",
            "Gray7",
            "Gray8",
            "Black",
        ]
        for c in colors:
            assert isinstance(getattr(preset, c), Style)
            for v in variants:
                assert isinstance(getattr(preset, f"{c}{v}"), Style)

    def test_google_styles_instantiation(self) -> None:
        """Verifies GoogleStyles provides valid styles, properties, and Google Sheets palette."""
        preset = google_styles

        assert isinstance(preset, BaseModel)
        assert isinstance(preset, BaseStyles)
        assert isinstance(preset, GoogleStyles)
        assert isinstance(preset.Primary, Style)
        assert isinstance(preset.PrimaryThin, Style)
        assert isinstance(preset.PrimaryBold, Style)
        assert isinstance(preset.PrimaryFlat, Style)
        assert isinstance(preset.PrimaryDashed, Style)
        assert isinstance(preset.PrimaryDotted, Style)
        assert isinstance(preset.Warning, Style)
        assert isinstance(preset.WarningDotted, Style)
        assert isinstance(preset.Neutral, Style)
        assert isinstance(preset.NeutralFlat, Style)
        assert isinstance(preset.GrayNeutral, Style)
        assert isinstance(preset.PrimaryNeutral, Style)
        assert isinstance(preset.BlueNeutral, Style)
        assert preset.background_color == (255, 255, 255, 1.0)
        assert preset.sourcecode_font == FontSourceCode.SOURCECODEPRO

        # Verify Google palette colors & variants
        assert isinstance(preset.CornflowerBlue, Style)
        assert isinstance(preset.CornflowerBlueFlat, Style)
        assert isinstance(preset.Blue1, Style)
        assert isinstance(preset.Blue1Flat, Style)
        assert isinstance(preset.Green5, Style)
        assert isinstance(preset.RedBerry, Style)
        assert isinstance(preset.Gray8, Style)
        assert isinstance(preset.GoogleBlue, Style)
        assert isinstance(preset.Teal, Style)
        assert isinstance(preset.CornflowerBlue3, Style)

        # Verify snake_case raises AttributeError
        with pytest.raises(AttributeError):
            _ = preset.google_blue
        with pytest.raises(AttributeError):
            _ = preset.cornflower_blue_flat

    def test_iteration_and_dict_access(self) -> None:
        """Verifies iteration, dictionary access, and styles helper on preset style models."""
        preset = default_styles

        # __iter__ test
        items = dict(preset)
        assert "Primary" in items
        assert items["Primary"] == preset.Primary
        assert "PrimaryThin" in items
        assert items["PrimaryThin"] == preset.PrimaryThin
        assert "background_color" in items

        # __getitem__ test
        assert preset["Primary"] == preset.Primary
        assert preset["PrimaryThin"] == preset.PrimaryThin

        # get test
        assert preset.get("Primary") == preset.Primary
        assert preset.get("unknown_key", "default_val") == "default_val"

        # styles() test (only Style instances)
        styles_dict = preset.styles()
        assert "Primary" in styles_dict
        assert "background_color" not in styles_dict

        # Verify snake_case raises KeyError
        with pytest.raises(KeyError):
            _ = preset["primary"]
        with pytest.raises(KeyError):
            _ = preset["primary_flat"]

    def test_custom_user_defined_styles(self) -> None:
        """Verifies that users can define arbitrary style fields with full autocomplete and iteration."""

        class MyCloudStyles(DefaultStyles):
            Vpc: Style
            Subnet: Style
            custom_note: str = "production"

        base = default_styles
        vpc_style = Style(line_color=(0, 100, 200, 1.0), line_width=2.0)
        subnet_style = Style(line_color=(50, 150, 250, 1.0), line_width=1.0)

        my_styles = MyCloudStyles(
            **base.model_dump(),
            Vpc=vpc_style,
            Subnet=subnet_style,
        )

        assert my_styles.Vpc == vpc_style
        assert my_styles.Subnet == subnet_style
        assert my_styles.custom_note == "production"

        style_map = dict(my_styles)
        assert style_map["Vpc"] == vpc_style
        assert style_map["Subnet"] == subnet_style
        assert style_map["custom_note"] == "production"
        assert my_styles["Vpc"] == vpc_style
        assert my_styles.get("Subnet") == subnet_style

    def test_import_from_types(self) -> None:
        """Verifies that BaseStyles can be imported from drawlib.types."""
        assert TypesBaseStyles is BaseStyles

    def test_styles_zero_argument_init(self) -> None:
        """Verifies that preset style classes can be instantiated without arguments."""
        d = DefaultStyles()
        assert isinstance(d, DefaultStyles)
        assert d.Primary is not None

        g = GoogleStyles()
        assert isinstance(g, GoogleStyles)
        assert g.Primary is not None
        assert g.GoogleBlue is not None

        m = MonochromeStyles()
        assert isinstance(m, MonochromeStyles)
        assert m.Primary is not None

    def test_styles_patch_instance_method(self) -> None:
        """Verifies that patch on preset style instances creates updated instances."""
        d = DefaultStyles()
        custom_primary = Style(line_color=(1, 2, 3, 1.0))
        p = d.patch(Primary=custom_primary, Width=200, BackgroundColor=(240, 240, 240))
        assert isinstance(p, DefaultStyles)
        assert p.Primary == custom_primary
        assert p.width == 200
        assert p.background_color == (240, 240, 240, 1.0)
        assert d.Primary != custom_primary

        g = GoogleStyles()
        custom_blue = Style(line_color=(4, 5, 6, 1.0))
        gp = g.patch(GoogleBlue=custom_blue)
        assert isinstance(gp, GoogleStyles)
        assert gp.GoogleBlue == custom_blue

        m = MonochromeStyles()
        custom_white = Style(line_color=(7, 8, 9, 1.0))
        mp = m.patch(White=custom_white)
        assert isinstance(mp, MonochromeStyles)
        assert mp.White == custom_white
