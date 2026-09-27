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

from drawlib._core.l2_models import Color


class BaseColors(BaseModel):
    """Base model for preset colors providing iteration, dictionary-like access, and patching."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        frozen=True,
    )

    Transparent: ClassVar[Color] = Color(0, 0, 0, 0.0)

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
        if hasattr(self, key):
            val = getattr(self, key)
            if isinstance(val, Color):
                return val
        raise KeyError(f'Color "{key}" is not found in {self.__class__.__name__}.')

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
            **kwargs: Color attributes to update.

        Returns:
            Self: New preset colors instance with updated attributes.
        """
        merged = {**self.__dict__, **kwargs}
        return self.__class__.model_validate(merged)


__all__ = [
    "BaseColors",
]
