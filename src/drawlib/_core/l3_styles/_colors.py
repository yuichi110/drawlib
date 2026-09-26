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

from typing import Final

from drawlib._core.l2_models import StaticContainer
from drawlib._core.l2_types import TypeColorRGBA


class ColorsBase(StaticContainer):
    """Base class for color-related classes, providing common attributes."""

    Transparent: Final[TypeColorRGBA] = (0, 0, 0, 0.0)


__all__ = [
    "ColorsBase",
]
