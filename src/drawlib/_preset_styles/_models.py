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

from typing import Any, Generator

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
    )

    background_color: TypeColor = (255, 255, 255, 1.0)
    sourcecode_font: FontSourceCode = FontSourceCode.SOURCECODEPRO

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


class DefaultStyles(BasePresetStyles):
    """Default preset styles.

    Attributes:
        primary (Style): Primary emphasis style.
        light (Style): Light / subtle line style.
        bold (Style): Bold / heavy line style.
        flat (Style): Flat filled style with no border.
        solid (Style): Transparent fill style with solid border.
        dashed (Style): Transparent fill style with dashed border.
    """

    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style


class EssentialsStyles(BasePresetStyles):
    """Essentials preset styles.

    Attributes:
        primary (Style): Primary emphasis style.
        light (Style): Light / subtle line style.
        bold (Style): Bold / heavy line style.
        flat (Style): Flat filled style with no border.
        solid (Style): Transparent fill style with solid border.
        dashed (Style): Transparent fill style with dashed border.
    """

    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style


class MonochromeStyles(BasePresetStyles):
    """Monochrome preset styles.

    Attributes:
        primary (Style): Primary emphasis style.
        light (Style): Light / subtle line style.
        bold (Style): Bold / heavy line style.
        flat (Style): Flat filled style with no border.
        solid (Style): Transparent fill style with solid border.
        dashed (Style): Transparent fill style with dashed border.
    """

    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style


# Backward compatibility alias
PresetStyles = BasePresetStyles
