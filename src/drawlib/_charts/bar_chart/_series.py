# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Series model for bar charts."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style

__all__ = ["Series"]


class Series:
    """Represents a single data series in a bar chart."""

    def __init__(
        self,
        name: str,
        values: list[float],
        style: Style,
    ) -> None:
        """Initialize Series.

        Args:
            name: Series name shown in legend and tooltips.
            values: List of numerical values corresponding to chart categories.
            style: Style object defining bar outline and fill.
        """
        self.name = name
        self.values: list[float] = [float(v) for v in values]
        self.style: Style = style
