# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base data structures for modular slide stage components."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BoundingBox:
    """A rectangular bounding box on the slide stage (typically 1920x1080).

    Attributes:
        x: The horizontal coordinate of the top-left corner in stage pixels.
        y: The vertical coordinate of the top-left corner in stage pixels.
        width: The width of the bounding box in stage pixels.
        height: The height of the bounding box in stage pixels.
    """

    x: float
    y: float
    width: float
    height: float
