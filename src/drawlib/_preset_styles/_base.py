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

    width: int = 140
    height: int = 70
    dpi: int = 100
    background_color: ColorType = (255, 255, 255, 1.0)
    sourcecode_font: FontSourceCode = FontSourceCode.SOURCECODEPRO
    colors: Any = None

    # 4 Core semantic roles required across all preset catalogs (10 variants each)
    primary: Style
    primary_bordered: Style | None = None
    primary_bold: Style | None = None
    primary_light: Style | None = None
    primary_flat: Style | None = None
    primary_outline: Style | None = None
    primary_outline_bold: Style | None = None
    primary_outline_light: Style | None = None
    primary_dashed: Style | None = None
    primary_dashed_bold: Style | None = None
    primary_dashed_light: Style | None = None

    secondary: Style | None = None
    secondary_bordered: Style | None = None
    secondary_bold: Style | None = None
    secondary_light: Style | None = None
    secondary_flat: Style | None = None
    secondary_outline: Style | None = None
    secondary_outline_bold: Style | None = None
    secondary_outline_light: Style | None = None
    secondary_dashed: Style | None = None
    secondary_dashed_bold: Style | None = None
    secondary_dashed_light: Style | None = None

    accent: Style | None = None
    accent_bordered: Style | None = None
    accent_bold: Style | None = None
    accent_light: Style | None = None
    accent_flat: Style | None = None
    accent_outline: Style | None = None
    accent_outline_bold: Style | None = None
    accent_outline_light: Style | None = None
    accent_dashed: Style | None = None
    accent_dashed_bold: Style | None = None
    accent_dashed_light: Style | None = None

    muted: Style | None = None
    muted_bordered: Style | None = None
    muted_bold: Style | None = None
    muted_light: Style | None = None
    muted_flat: Style | None = None
    muted_outline: Style | None = None
    muted_outline_bold: Style | None = None
    muted_outline_light: Style | None = None
    muted_dashed: Style | None = None
    muted_dashed_bold: Style | None = None
    muted_dashed_light: Style | None = None

    # Extended semantic roles (10 variants each)
    light: Style | None = None
    light_bordered: Style | None = None
    light_bold: Style | None = None
    light_light: Style | None = None
    light_flat: Style | None = None
    light_outline: Style | None = None
    light_outline_bold: Style | None = None
    light_outline_light: Style | None = None
    light_dashed: Style | None = None
    light_dashed_bold: Style | None = None
    light_dashed_light: Style | None = None

    dark: Style | None = None
    dark_bordered: Style | None = None
    dark_bold: Style | None = None
    dark_light: Style | None = None
    dark_flat: Style | None = None
    dark_outline: Style | None = None
    dark_outline_bold: Style | None = None
    dark_outline_light: Style | None = None
    dark_dashed: Style | None = None
    dark_dashed_bold: Style | None = None
    dark_dashed_light: Style | None = None

    danger: Style | None = None
    danger_bordered: Style | None = None
    danger_bold: Style | None = None
    danger_light: Style | None = None
    danger_flat: Style | None = None
    danger_outline: Style | None = None
    danger_outline_bold: Style | None = None
    danger_outline_light: Style | None = None
    danger_dashed: Style | None = None
    danger_dashed_bold: Style | None = None
    danger_dashed_light: Style | None = None

    success: Style | None = None
    success_bordered: Style | None = None
    success_bold: Style | None = None
    success_light: Style | None = None
    success_flat: Style | None = None
    success_outline: Style | None = None
    success_outline_bold: Style | None = None
    success_outline_light: Style | None = None
    success_dashed: Style | None = None
    success_dashed_bold: Style | None = None
    success_dashed_light: Style | None = None

    canvas: Style | None = None
    canvas_flat: Style | None = None

    @property
    def bold(self) -> Style:
        """Backwards compatibility alias for primary_bold."""
        if self.primary_bold is not None:
            return self.primary_bold
        if self.__pydantic_extra__ and "bold" in self.__pydantic_extra__:
            val = self.__pydantic_extra__["bold"]
            if isinstance(val, Style):
                return val
        return self.primary

    @property
    def flat(self) -> Style:
        """Backwards compatibility alias for primary_flat."""
        if self.primary_flat is not None:
            return self.primary_flat
        if self.__pydantic_extra__ and "flat" in self.__pydantic_extra__:
            val = self.__pydantic_extra__["flat"]
            if isinstance(val, Style):
                return val
        return self.primary

    @property
    def solid(self) -> Style:
        """Backwards compatibility alias for primary_outline."""
        if self.primary_outline is not None:
            return self.primary_outline
        if self.__pydantic_extra__ and "solid" in self.__pydantic_extra__:
            val = self.__pydantic_extra__["solid"]
            if isinstance(val, Style):
                return val
        return self.primary

    @property
    def dashed(self) -> Style:
        """Backwards compatibility alias for primary_dashed."""
        if self.primary_dashed is not None:
            return self.primary_dashed
        if self.__pydantic_extra__ and "dashed" in self.__pydantic_extra__:
            val = self.__pydantic_extra__["dashed"]
            if isinstance(val, Style):
                return val
        return self.primary

    @property
    def primary_solid(self) -> Style:
        """Backwards compatibility alias for primary_outline."""
        return self.solid

    @property
    def secondary_solid(self) -> Style | None:
        """Backwards compatibility alias for secondary_outline."""
        return self.secondary_outline

    @property
    def accent_solid(self) -> Style | None:
        """Backwards compatibility alias for accent_outline."""
        return self.accent_outline

    @property
    def muted_solid(self) -> Style | None:
        """Backwards compatibility alias for muted_outline."""
        return self.muted_outline

    @property
    def danger_solid(self) -> Style | None:
        """Backwards compatibility alias for danger_outline."""
        return self.danger_outline

    @property
    def success_solid(self) -> Style | None:
        """Backwards compatibility alias for success_outline."""
        return self.success_outline

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        """Yield (field_name, field_value) pairs for all fields in the preset style model.

        Returns:
            Generator[tuple[str, Any], None, None]: Generator yielding field name and value pairs.
        """
        for field_name in self.model_fields:
            try:
                val = getattr(self, field_name)
            except AttributeError:
                continue
            if val is not None:
                yield field_name, val

    def __getitem__(self, key: str) -> Any:  # noqa: ANN401
        """Allow dictionary-like item access by style name.

        Args:
            key (str): Field name or style name.

        Returns:
            Any: Value of the specified field.

        Raises:
            KeyError: If the specified key does not exist.
        """
        try:
            if hasattr(self, key):
                val = getattr(self, key)
                if val is not None:
                    return val
        except AttributeError:
            pass
        raise KeyError(f'Style "{key}" is not found in {self.__class__.__name__}.')

    def get(self, key: str, default: Any = None) -> Any:  # noqa: ANN401
        """Safely retrieve a style or attribute with an optional default fallback.

        Args:
            key (str): Field name or style name.
            default (Any): Fallback value if field is not found. Defaults to None.

        Returns:
            Any: Field value or default fallback.
        """
        try:
            val = getattr(self, key, default)
            return default if val is None else val
        except AttributeError:
            return default

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
            try:
                val = getattr(self, field_name)
            except AttributeError:
                continue
            if not isinstance(val, Style):
                continue

            target_font = _resolve_target_font(field_name, regular, bold, light)
            if target_font is not None:
                updates[field_name] = val.patch(text_font=target_font)

        return self.model_copy(update=updates)


BasePresetStyles = BaseStyles
PresetStyles = BaseStyles

__all__ = [
    "BasePresetStyles",
    "BaseStyles",
    "PresetStyles",
]
