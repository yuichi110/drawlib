# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""PieSlice model representing a single sector in a pie or donut chart."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import ColorType

if TYPE_CHECKING:
    from drawlib._core.types import Style


class PieSlice:
    """Represents a single data slice in a pie or donut chart."""

    def __init__(
        self,
        name: str,
        value: float,
        color: ColorType | None = None,
        style: Style | None = None,
        explode: float = 0.0,
    ) -> None:
        """Initialize PieSlice.

        Args:
            name: Slice label displayed in legend and annotations.
            value: Numerical value determining slice proportion.
            color: Slice fill color.
            style: Optional Style overriding wedge appearance.
            explode: Distance to shift the slice outward from center. Defaults to 0.0.
        """
        self.name = name
        self.value = float(value)
        self.color: ColorType | None = color
        self.style: Style | None = style
        self.explode = float(explode)
