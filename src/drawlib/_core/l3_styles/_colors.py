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

from typing import Any, Final

from drawlib._core.l2_models import Color, StaticContainer


class ColorsBase(StaticContainer):
    """Base class for color-related classes, providing common attributes."""

    Transparent: Final[Color] = Color(0, 0, 0, 0.0)

    def __init_subclass__(cls, **kwargs: Any) -> None:  # noqa: ANN401
        """Automatically convert color attributes on subclasses to Color instances."""
        super().__init_subclass__(**kwargs)
        for key, val in list(cls.__dict__.items()):
            if isinstance(val, (tuple, list)) and len(val) in {3, 4}:
                setattr(cls, key, Color(val))
            elif isinstance(val, str) and val.strip().startswith("#"):
                setattr(cls, key, Color.from_hex(val))


__all__ = [
    "ColorsBase",
]
