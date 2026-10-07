# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Swimlane definition for flow diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class Lane:
    """Represents a swimlane column or row in a flow diagram."""

    def __init__(
        self,
        title: str,
        size: float,
        style: Style | None = None,
        text_style: Style | None = None,
        header_size: float = 6.0,
        header_style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize Lane.

        Args:
            title: Header title of the swimlane (e.g. role, department, actor).
            size: Width of the lane (vertical orientation) or height (horizontal orientation).
            style: Style for the lane background fill and boundary stroke.
            text_style: Style for the header title text.
            header_size: Height of the header section in vertical mode (or width in horizontal mode). Defaults to 6.0.
            header_style: Optional specific Style for the header card background.
            show: Whether to render this swimlane. Defaults to True.
        """
        self.title = title
        self.size = float(size)
        self.style = style
        self.text_style = text_style
        self.header_size = float(header_size)
        self.header_style = header_style
        self.show = bool(show)
