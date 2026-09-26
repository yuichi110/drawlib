# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Preset styles models module."""

from __future__ import annotations

from typing import Any, Generator, Self

from pydantic import BaseModel, ConfigDict

from drawlib._core.l2_types import TypeColor
from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import Style


class BasePresetStyles(BaseModel):
    """Base model for preset styles providing iteration, dictionary-like access, and autocompletion.

    Attributes:
        background_color (TypeColor): Default canvas background color for this preset style.
        sourcecode_font (FontSourceCode): Default sourcecode font for this preset style.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        frozen=True,
    )

    background_color: TypeColor = (255, 255, 255, 1.0)
    sourcecode_font: FontSourceCode = FontSourceCode.SOURCECODEPRO

    # Core semantic roles required across all preset catalogs
    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        """Yield (field_name, field_value) pairs for all fields in the preset style model.

        Returns:
            Generator[tuple[str, Any], None, None]: Generator yielding field name and value pairs.
        """
        for field_name in self.model_fields:
            yield field_name, getattr(self, field_name)

    def __getitem__(self, key: str) -> Any:  # noqa: ANN401
        """Allow dictionary-like item access by style name.

        Args:
            key (str): Field name or style name.

        Returns:
            Any: Value of the specified field.

        Raises:
            KeyError: If the specified key does not exist.
        """
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f'Style "{key}" is not found in {self.__class__.__name__}.')

    def get(self, key: str, default: Any = None) -> Any:  # noqa: ANN401
        """Safely retrieve a style or attribute with an optional default fallback.

        Args:
            key (str): Field name or style name.
            default (Any): Fallback value if field is not found. Defaults to None.

        Returns:
            Any: Field value or default fallback.
        """
        return getattr(self, key, default)

    def styles(self) -> dict[str, Style]:
        """Extract only Style objects defined on this preset as a dictionary.

        Returns:
            dict[str, Style]: Dictionary mapping style names to Style instances.
        """
        return {k: v for k, v in self if isinstance(v, Style)}

    def patch(self, **kwargs: Any) -> Self:  # noqa: ANN401
        """Create a new copy of preset styles with updated attributes.

        Args:
            **kwargs: Attributes to update.

        Returns:
            Self: New preset styles instance with updated attributes.
        """
        return self.model_copy(update=kwargs)


class DefaultStyles(BasePresetStyles):
    """Default preset styles with complete typing for IDE autocompletion."""

    # Semantic roles
    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style

    # Blue
    blue: Style
    blue_flat: Style
    blue_solid: Style
    blue_bold: Style
    blue_light: Style
    blue_dashed: Style

    # Red
    red: Style
    red_flat: Style
    red_solid: Style
    red_bold: Style
    red_light: Style
    red_dashed: Style

    # Green
    green: Style
    green_flat: Style
    green_solid: Style
    green_bold: Style
    green_light: Style
    green_dashed: Style

    # Black
    black: Style
    black_flat: Style
    black_solid: Style
    black_bold: Style
    black_light: Style
    black_dashed: Style

    # White
    white: Style
    white_flat: Style
    white_solid: Style
    white_bold: Style
    white_light: Style
    white_dashed: Style


class MonochromeStyles(BasePresetStyles):
    """Monochrome preset styles with complete typing for IDE autocompletion."""

    # Semantic roles
    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style

    # Colors: black, charcoal, graphite, gray, silver, snow, white
    black: Style
    black_flat: Style
    black_solid: Style
    black_bold: Style
    black_light: Style
    black_dashed: Style

    charcoal: Style
    charcoal_flat: Style
    charcoal_solid: Style
    charcoal_bold: Style
    charcoal_light: Style
    charcoal_dashed: Style

    graphite: Style
    graphite_flat: Style
    graphite_solid: Style
    graphite_bold: Style
    graphite_light: Style
    graphite_dashed: Style

    gray: Style
    gray_flat: Style
    gray_solid: Style
    gray_bold: Style
    gray_light: Style
    gray_dashed: Style

    silver: Style
    silver_flat: Style
    silver_solid: Style
    silver_bold: Style
    silver_light: Style
    silver_dashed: Style

    snow: Style
    snow_flat: Style
    snow_solid: Style
    snow_bold: Style
    snow_light: Style
    snow_dashed: Style

    white: Style
    white_flat: Style
    white_solid: Style
    white_bold: Style
    white_light: Style
    white_dashed: Style


class EssentialsStyles(BasePresetStyles):
    """Essentials preset styles with complete typing for IDE autocompletion."""

    # Semantic roles
    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style

    # Popular essentials colors
    red: Style
    red_flat: Style
    red_solid: Style
    red_bold: Style
    red_dashed: Style

    light_red: Style
    light_red_flat: Style
    light_red_solid: Style
    light_red_bold: Style

    green: Style
    green_flat: Style
    green_solid: Style
    green_bold: Style
    green_dashed: Style

    light_green: Style
    light_green_flat: Style
    light_green_solid: Style
    light_green_bold: Style

    blue: Style
    blue_flat: Style
    blue_solid: Style
    blue_bold: Style
    blue_dashed: Style

    light_blue: Style
    light_blue_flat: Style
    light_blue_solid: Style
    light_blue_bold: Style

    yellow: Style
    yellow_flat: Style
    yellow_solid: Style
    yellow_bold: Style

    purple: Style
    purple_flat: Style
    purple_solid: Style
    purple_bold: Style
    purple_dashed: Style

    orange: Style
    orange_flat: Style
    orange_solid: Style
    orange_bold: Style
    orange_dashed: Style

    navy: Style
    navy_flat: Style
    navy_solid: Style
    navy_bold: Style
    navy_dashed: Style

    pink: Style
    pink_flat: Style
    pink_solid: Style
    pink_bold: Style

    charcoal: Style
    charcoal_flat: Style
    charcoal_solid: Style
    charcoal_bold: Style
    charcoal_dashed: Style

    graphite: Style
    graphite_flat: Style
    graphite_solid: Style
    graphite_bold: Style

    gray: Style
    gray_flat: Style
    gray_solid: Style
    gray_bold: Style
    gray_dashed: Style

    silver: Style
    silver_flat: Style
    silver_solid: Style
    silver_bold: Style
    silver_dashed: Style

    snow: Style
    snow_flat: Style
    snow_solid: Style
    snow_bold: Style

    teal: Style
    teal_flat: Style
    teal_solid: Style
    teal_bold: Style
    teal_dashed: Style

    olive: Style
    olive_flat: Style
    olive_solid: Style
    olive_bold: Style

    brown: Style
    brown_flat: Style
    brown_solid: Style
    brown_bold: Style

    black: Style
    black_flat: Style
    black_solid: Style
    black_bold: Style

    white: Style
    white_flat: Style
    white_solid: Style
    white_bold: Style

    aqua: Style
    aqua_flat: Style
    aqua_solid: Style
    aqua_bold: Style

    green_yellow: Style
    green_yellow_flat: Style
    green_yellow_solid: Style
    green_yellow_bold: Style

    ivory: Style
    ivory_flat: Style
    ivory_solid: Style
    ivory_bold: Style

    steel: Style
    steel_flat: Style
    steel_solid: Style
    steel_bold: Style


PresetStyles = BasePresetStyles
