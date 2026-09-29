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

import re
from typing import Any, Generator, Self

from pydantic import BaseModel, ConfigDict, validate_call

from drawlib._core.l2_types import Color, ColorType, FontBase, FontFile
from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles._style_models import Style


def _resolve_target_font(
    field_name: str,
    regular: FontBase | FontFile | None,
    bold: FontBase | FontFile | None,
    light: FontBase | FontFile | None,
) -> FontBase | FontFile | None:
    """Resolve target font for a specific style field based on naming convention.

    Args:
        field_name (str): Style attribute name.
        regular (FontBase | FontFile | None): Base font.
        bold (FontBase | FontFile | None): Bold font.
        light (FontBase | FontFile | None): Light font.

    Returns:
        FontBase | FontFile | None: Target font to apply.
    """
    if field_name == "bold" or field_name.endswith("_bold"):
        return bold if bold is not None else regular
    if field_name.endswith("_light"):
        return light if light is not None else regular
    return regular


def _pascal_to_snake(name: str) -> str:
    """Convert PascalCase string to snake_case.

    Args:
        name (str): Identifier in PascalCase.

    Returns:
        str: Converted identifier in snake_case.
    """
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    return s.lower()


def _snake_to_pascal(name: str) -> str:
    """Convert snake_case string to PascalCase.

    Args:
        name (str): Identifier in snake_case.

    Returns:
        str: Converted identifier in PascalCase.
    """
    return "".join(word.capitalize() for word in name.split("_"))


def _resolve_style_field_name(cls: type[BaseStyles], name: str, value: Any = None) -> str:  # noqa: ANN401
    """Resolve style field name matching model attributes regardless of casing or aliases.

    Args:
        cls (type[BaseStyles]): Preset style class.
        name (str): Style or attribute name.
        value (Any): Optional value to distinguish style vs color for aliases like 'canvas'.

    Returns:
        str: Resolved field name matching cls.model_fields if found, else original name.
    """
    lower = name.lower()
    if lower in {"bg_color", "background", "background_color"}:
        return "background_color"
    if lower == "colors":
        return "colors"
    fields = getattr(cls, "model_fields", {})
    if name in fields:
        return name
    snake_name = _pascal_to_snake(name)
    if snake_name in fields:
        return snake_name
    for f in fields:
        if f.lower() == lower:
            return f
    return name


class _BaseStylesMeta(type(BaseModel)):
    """Metaclass allowing class-level attribute access for preset styles."""

    _default_instances: dict[type, BaseStyles] = {}

    def register_default_instance(cls, instance: BaseStyles) -> None:
        """Register the default singleton instance for this style class.

        Args:
            instance (BaseStyles): Default preset style instance.
        """
        _BaseStylesMeta._default_instances[cls] = instance

    def get_default_instance(cls) -> BaseStyles | None:
        """Get the registered default instance for this style class or its superclasses.

        Returns:
            BaseStyles | None: The registered instance or None if not found.
        """
        if cls in _BaseStylesMeta._default_instances:
            return _BaseStylesMeta._default_instances[cls]
        for registered_cls, inst in _BaseStylesMeta._default_instances.items():
            if issubclass(cls, registered_cls) or issubclass(registered_cls, cls):
                return inst
        return None

    def __getattribute__(cls, name: str) -> Any:  # noqa: ANN401
        val = super().__getattribute__(name)
        if isinstance(val, property):
            inst = cls.get_default_instance()
            if inst is not None and val.fget is not None:
                return val.fget(inst)
        if name in {"patch_font", "copy"}:
            inst = cls.get_default_instance()
            if inst is not None:
                return val.__get__(inst, cls)
        return val

    def __getattr__(cls, name: str) -> Any:  # noqa: ANN401
        if name.startswith("__"):
            raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")
        inst = cls.get_default_instance()
        if inst is not None:
            if name in cls.model_fields:
                return getattr(inst, name)
            snake_name = _pascal_to_snake(name)
            if snake_name in cls.model_fields:
                return getattr(inst, snake_name)
            if hasattr(inst, name):
                return getattr(inst, name)
            if snake_name != name and hasattr(inst, snake_name):
                return getattr(inst, snake_name)
        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")

    def __getitem__(cls, key: str) -> Style:
        inst = cls.get_default_instance()
        if inst is not None:
            return inst[key]
        raise KeyError(f'Style "{key}" is not found in {cls.__name__}.')

    def __dir__(cls) -> list[str]:
        attrs = set(super().__dir__())
        for field in cls.model_fields:
            attrs.add(field)
            attrs.add(_snake_to_pascal(field))
        return sorted(attrs)


class BaseStyles(BaseModel, metaclass=_BaseStylesMeta):
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

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize preset styles instance.

        If called without arguments (or with partial overrides), missing fields are
        automatically populated from the registered default singleton instance for this class.
        """
        normalized: dict[str, Any] = {}
        for k, v in kwargs.items():
            target_key = _resolve_style_field_name(self.__class__, k, v)
            if target_key == "background_color" and v is not None:
                try:
                    normalized[target_key] = v if isinstance(v, Color) else Color(v)
                except Exception:
                    normalized[target_key] = v
            else:
                normalized[target_key] = v

        default_inst = self.__class__.get_default_instance()
        if default_inst is not None:
            merged = {**default_inst.__dict__, **normalized}
            super().__init__(**merged)
        else:
            super().__init__(**normalized)

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
            snake_key = _pascal_to_snake(key)
            if hasattr(self, snake_key):
                val = getattr(self, snake_key)
                if val is not None:
                    return val
        except AttributeError:
            pass
        raise KeyError(f'Style "{key}" is not found in {self.__class__.__name__}.')

    def __getattr__(self, name: str) -> Any:  # noqa: ANN401
        """Allow fallback resolution for PascalCase style names and extra fields on instances."""
        if name.startswith("__"):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        extra = getattr(self, "__pydantic_extra__", None)
        if extra is not None and name in extra:
            return extra[name]
        snake_name = _pascal_to_snake(name)
        if snake_name != name:
            if hasattr(self.__class__, snake_name):
                return getattr(self, snake_name)
            if snake_name in self.__class__.model_fields:
                return getattr(self, snake_name)
            if extra is not None and snake_name in extra:
                return extra[snake_name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __dir__(self) -> list[str]:
        """Include both snake_case and PascalCase style attribute names."""
        attrs = set(super().__dir__())
        for field in self.__class__.model_fields:
            attrs.add(field)
            attrs.add(_snake_to_pascal(field))
        return sorted(attrs)

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
            **kwargs: Style attributes to update (accepts PascalCase, snake_case, or aliases).

        Returns:
            Self: New preset styles instance with updated attributes.
        """
        updates: dict[str, Any] = {}
        for k, v in kwargs.items():
            if v is not None:
                target_key = _resolve_style_field_name(self.__class__, k, v)
                if target_key == "background_color":
                    try:
                        updates[target_key] = v if isinstance(v, Color) else Color(v)
                    except Exception:
                        updates[target_key] = v
                else:
                    updates[target_key] = v
        return self.model_copy(update=updates)

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


__all__ = [
    "BaseStyles",
]
