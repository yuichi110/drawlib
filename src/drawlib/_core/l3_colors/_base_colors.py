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

from typing import Any, ClassVar, Generator, Self

from pydantic import BaseModel, ConfigDict

from drawlib._core.l3_colors._color import Color


class _BaseColorsMeta(type(BaseModel)):
    """Metaclass allowing class-level attribute access for color fields."""

    def __getattr__(cls, name: str) -> Any:  # noqa: ANN401
        if name.startswith("__"):
            raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")
        fields = cls.__dict__.get("__pydantic_fields__")
        if fields and name in fields:
            default = fields[name].default
            if default is not None:
                return default
            return None
        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")

    def __getitem__(cls, key: str) -> Color:
        if not isinstance(key, str):
            raise KeyError(f"Invalid key type: {type(key)}")
        if hasattr(cls, key):
            val = getattr(cls, key)
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
        extra="forbid",
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
    Warning: Color | None = None
    Neutral: Color | None = None
    Canvas: Color | None = None

    # Semantic Neutral Colors (Fill tones)
    GrayNeutral: Color | None = None
    PrimaryNeutral: Color | None = None
    SecondaryNeutral: Color | None = None
    AccentNeutral: Color | None = None
    WarningNeutral: Color | None = None
    DangerNeutral: Color | None = None
    SuccessNeutral: Color | None = None
    MutedNeutral: Color | None = None

    # Named Color Neutral Colors (Fill tones)
    BlueNeutral: Color | None = None
    GreenNeutral: Color | None = None
    RedNeutral: Color | None = None
    OrangeNeutral: Color | None = None
    AmberNeutral: Color | None = None
    PurpleNeutral: Color | None = None
    TealNeutral: Color | None = None
    PinkNeutral: Color | None = None
    CyanNeutral: Color | None = None
    YellowNeutral: Color | None = None
    MagentaNeutral: Color | None = None

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
        if key == "Transparent":
            return self.Transparent
        fields = self.__class__.model_fields
        if key in fields:
            val = getattr(self, key)
            if isinstance(val, Color):
                return val
        raise KeyError(f'Color "{key}" is not found in {self.__class__.__name__}.')

    def __getattr__(self, name: str) -> Any:  # noqa: ANN401
        """Raise AttributeError for missing attributes."""
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
            **kwargs: Color attributes to update (in PascalCase).

        Returns:
            Self: New preset colors instance with updated attributes.
        """
        updates: dict[str, Any] = {}
        for k, v in kwargs.items():
            if k != "__class__" and v is not None:
                try:
                    updates[k] = v if isinstance(v, Color) else Color(v)
                except Exception:
                    updates[k] = v

        merged = {**self.__dict__, **updates}
        return self.__class__.model_validate(merged)


__all__ = [
    "BaseColors",
]
