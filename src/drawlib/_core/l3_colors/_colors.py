# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color base definition module."""

from __future__ import annotations

from typing import Any, Callable, ClassVar, Concatenate, Generator, Generic, ParamSpec, Self, TypeVar, overload

from pydantic import BaseModel, ConfigDict

from drawlib._core.l3_colors._color import Color, ColorType


def _resolve_color_field_name(cls: type[BaseColors], name: str) -> str:
    """Resolve color field name matching model attributes regardless of casing.

    Args:
        cls (type[BaseColors]): Preset color class.
        name (str): Field or color name.

    Returns:
        str: Resolved field name matching cls.model_fields if found, else original name.
    """
    fields = getattr(cls, "model_fields", {})
    if name in fields:
        return name
    cap_name = name.capitalize()
    if cap_name in fields:
        return cap_name
    for f in fields:
        if f.lower() == name.lower():
            return f
    return name


class _BaseColorsMeta(type(BaseModel)):
    """Metaclass allowing class-level attribute access for color fields."""

    def __getattribute__(cls, name: str) -> Any:  # noqa: ANN401
        attr = super().__getattribute__(name)
        if isinstance(attr, property):
            cap_name = name.capitalize()
            if cap_name != name:
                fields = cls.__dict__.get("__pydantic_fields__", {})
                if cap_name in fields and fields[cap_name].default is not None:
                    return fields[cap_name].default
                if hasattr(cls, cap_name):
                    return getattr(cls, cap_name)
        return attr

    def __getattr__(cls, name: str) -> Any:  # noqa: ANN401
        if name.lower() == "transparent":
            return cls.Transparent
        fields = cls.__dict__.get("__pydantic_fields__")
        if fields:
            if name in fields:
                default = fields[name].default
                if default is not None:
                    return default
                return None
            cap_name = name.capitalize()
            if cap_name in fields:
                default = fields[cap_name].default
                if default is not None:
                    return default
        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")

    def __getitem__(cls, key: str) -> Color:
        if not isinstance(key, str):
            raise KeyError(f"Invalid key type: {type(key)}")
        if hasattr(cls, key):
            val = getattr(cls, key)
            if isinstance(val, Color):
                return val
        cap_key = key.capitalize()
        if hasattr(cls, cap_key):
            val = getattr(cls, cap_key)
            if isinstance(val, Color):
                return val
        raise KeyError(f'Color "{key}" is not found in {cls.__name__}.')

    def __iter__(cls) -> Generator[tuple[str, Color], None, None]:
        for field_name in cls.model_fields:
            val = getattr(cls, field_name, None)
            if isinstance(val, Color):
                yield field_name, val


class BaseColors(BaseModel, metaclass=_BaseColorsMeta):
    """Base model for preset colors providing iteration, dictionary-like access, and patching."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        frozen=True,
    )

    Transparent: ClassVar[Color] = Color(0, 0, 0, 0.0)

    Primary: Color | None = None
    Secondary: Color | None = None
    Accent: Color | None = None
    Muted: Color | None = None
    Light: Color | None = None
    Dark: Color | None = None
    Danger: Color | None = None
    Success: Color | None = None
    Canvas: Color | None = None

    @property
    def primary(self) -> Color:
        """Return primary semantic color."""
        if self.Primary is None:
            raise AttributeError(f"{self.__class__.__name__} has no Primary color.")
        return self.Primary

    @property
    def secondary(self) -> Color:
        """Return secondary semantic color."""
        if self.Secondary is None:
            raise AttributeError(f"{self.__class__.__name__} has no Secondary color.")
        return self.Secondary

    @property
    def accent(self) -> Color:
        """Return accent semantic color."""
        if self.Accent is None:
            raise AttributeError(f"{self.__class__.__name__} has no Accent color.")
        return self.Accent

    @property
    def muted(self) -> Color:
        """Return muted semantic color."""
        if self.Muted is None:
            raise AttributeError(f"{self.__class__.__name__} has no Muted color.")
        return self.Muted

    @property
    def light(self) -> Color:
        """Return light semantic color."""
        if self.Light is None:
            raise AttributeError(f"{self.__class__.__name__} has no Light color.")
        return self.Light

    @property
    def dark(self) -> Color:
        """Return dark semantic color."""
        if self.Dark is None:
            raise AttributeError(f"{self.__class__.__name__} has no Dark color.")
        return self.Dark

    @property
    def canvas(self) -> Color:
        """Return canvas semantic background color."""
        if self.Canvas is None:
            raise AttributeError(f"{self.__class__.__name__} has no Canvas color.")
        return self.Canvas

    @property
    def danger(self) -> Color:
        """Return danger semantic color."""
        if self.Danger is None:
            raise AttributeError(f"{self.__class__.__name__} has no Danger color.")
        return self.Danger

    @property
    def success(self) -> Color:
        """Return success semantic color."""
        if self.Success is None:
            raise AttributeError(f"{self.__class__.__name__} has no Success color.")
        return self.Success

    def __iter__(self) -> Generator[tuple[str, Color], None, None]:
        """Yield (field_name, field_value) pairs for all color fields in the preset color model.

        Returns:
            Generator[tuple[str, Color], None, None]: Generator yielding field name and Color pairs.
        """
        for field_name in self.__class__.model_fields:
            val = getattr(self, field_name)
            if isinstance(val, Color):
                yield field_name, val

    def __getitem__(self, key: str) -> Color:
        """Allow dictionary-like item access by color name.

        Args:
            key (str): Field name or color name.

        Returns:
            Color: Value of the specified color field.

        Raises:
            KeyError: If the specified key does not exist.
        """
        if key.lower() == "transparent":
            return self.Transparent
        fields = self.__class__.model_fields
        if key in fields:
            val = getattr(self, key)
            if isinstance(val, Color):
                return val
        cap_key = key.capitalize()
        if cap_key in fields:
            val = getattr(self, cap_key)
            if isinstance(val, Color):
                return val
        raise KeyError(f'Color "{key}" is not found in {self.__class__.__name__}.')

    def __getattr__(self, name: str) -> Any:  # noqa: ANN401
        """Allow fallback resolution for transparent and lowercase color names on instances."""
        if name.startswith("__"):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        if name.lower() == "transparent":
            return self.Transparent
        cap_name = name.capitalize()
        if cap_name != name and hasattr(self, cap_name):
            val = getattr(self, cap_name)
            if isinstance(val, Color):
                return val
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def get(self, key: str, default: Any = None) -> Any:  # noqa: ANN401
        """Safely retrieve a color or attribute with an optional default fallback.

        Args:
            key (str): Field name or color name.
            default (Any): Fallback value if field is not found. Defaults to None.

        Returns:
            Any: Field value or default fallback.
        """
        return getattr(self, key, default)

    def colors(self) -> dict[str, Color]:
        """Extract only Color objects defined on this preset as a dictionary.

        Returns:
            dict[str, Color]: Dictionary mapping color names to Color instances.
        """
        return {k: v for k, v in self}

    def patch(self, **kwargs: Any) -> Self:  # noqa: ANN401
        """Create a new copy of preset colors with updated attributes.

        Args:
            **kwargs: Color attributes to update (accepts PascalCase, snake_case, or lowercase).

        Returns:
            Self: New preset colors instance with updated attributes.
        """
        updates: dict[str, Any] = {}
        for k, v in kwargs.items():
            if v is not None:
                target_key = _resolve_color_field_name(self.__class__, k)
                try:
                    updates[target_key] = v if isinstance(v, Color) else Color(v)
                except Exception:
                    updates[target_key] = v

        merged = {**self.__dict__, **updates}
        return self.__class__.model_validate(merged)


__all__ = [
    "BaseColors",
]
