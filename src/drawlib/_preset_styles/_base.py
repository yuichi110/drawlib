# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base model for preset styles."""

from __future__ import annotations

from typing import Any, Generator, Self

from pydantic import BaseModel, ConfigDict, validate_call

from drawlib._core.fonts import FontBase, FontFile, FontSourceCode
from drawlib._core.types import ColorType, Style
from drawlib._preset_styles._utils import _resolve_target_font


class BaseStyles(BaseModel):
    """Base model for preset styles providing iteration, dictionary-like access, and autocompletion.

    Attributes:
        background_color (ColorType): Default canvas background color for this preset style.
        sourcecode_font (FontSourceCode): Default sourcecode font for this preset style.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        frozen=True,
    )

    background_color: ColorType = (255, 255, 255, 1.0)
    sourcecode_font: FontSourceCode = FontSourceCode.SOURCECODEPRO

    # 4 Core semantic roles required across all preset catalogs (10 variants each)
    primary: Style
    primary_bordered: Style
    primary_bold: Style
    primary_light: Style
    primary_flat: Style
    primary_outline: Style
    primary_outline_bold: Style
    primary_outline_light: Style
    primary_dashed: Style
    primary_dashed_bold: Style
    primary_dashed_light: Style

    secondary: Style
    secondary_bordered: Style
    secondary_bold: Style
    secondary_light: Style
    secondary_flat: Style
    secondary_outline: Style
    secondary_outline_bold: Style
    secondary_outline_light: Style
    secondary_dashed: Style
    secondary_dashed_bold: Style
    secondary_dashed_light: Style

    accent: Style
    accent_bordered: Style
    accent_bold: Style
    accent_light: Style
    accent_flat: Style
    accent_outline: Style
    accent_outline_bold: Style
    accent_outline_light: Style
    accent_dashed: Style
    accent_dashed_bold: Style
    accent_dashed_light: Style

    muted: Style
    muted_bordered: Style
    muted_bold: Style
    muted_light: Style
    muted_flat: Style
    muted_outline: Style
    muted_outline_bold: Style
    muted_outline_light: Style
    muted_dashed: Style
    muted_dashed_bold: Style
    muted_dashed_light: Style

    @property
    def light(self) -> Style:
        """Backwards compatibility alias for primary_light."""
        return self.primary_light

    @property
    def bold(self) -> Style:
        """Backwards compatibility alias for primary_bold."""
        return self.primary_bold

    @property
    def flat(self) -> Style:
        """Backwards compatibility alias for primary_flat."""
        return self.primary_flat

    @property
    def solid(self) -> Style:
        """Backwards compatibility alias for primary_outline."""
        return self.primary_outline

    @property
    def dashed(self) -> Style:
        """Backwards compatibility alias for primary_dashed."""
        return self.primary_dashed

    @property
    def primary_solid(self) -> Style:
        """Backwards compatibility alias for primary_outline."""
        return self.primary_outline

    @property
    def secondary_solid(self) -> Style:
        """Backwards compatibility alias for secondary_outline."""
        return self.secondary_outline

    @property
    def accent_solid(self) -> Style:
        """Backwards compatibility alias for accent_outline."""
        return self.accent_outline

    @property
    def muted_solid(self) -> Style:
        """Backwards compatibility alias for muted_outline."""
        return self.muted_outline

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

    @validate_call
    def patch_font(
        self,
        regular: FontBase | FontFile | None = None,
        *,
        bold: FontBase | FontFile | None = None,
        light: FontBase | FontFile | None = None,
        sourcecode: FontSourceCode | None = None,
    ) -> Self:
        """Create a new copy of preset styles with updated font configurations.

        Args:
            regular (FontBase | FontFile | None): Default baseline font applied to all styles.
                If provided without explicit bold/light overrides, it is also applied as fallback
                for bold and light variants.
            bold (FontBase | FontFile | None): Font override for bold style variants ('bold', '*_bold').
            light (FontBase | FontFile | None): Font override for light style variants ('light', '*_light').
            sourcecode (FontSourceCode | None): Monospace source code font override.

        Returns:
            Self: New preset styles instance with updated font attributes.
        """
        updates: dict[str, Any] = {}

        if sourcecode is not None:
            updates["sourcecode_font"] = sourcecode

        for field_name in self.model_fields:
            val = getattr(self, field_name)
            if not isinstance(val, Style):
                continue

            target_font = _resolve_target_font(field_name, regular, bold, light)
            if target_font is not None:
                updates[field_name] = val.patch(text_font=target_font)

        return self.model_copy(update=updates)


__all__ = [
    "BaseStyles",
]
