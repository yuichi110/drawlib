# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""BoxTree implementation module."""

from __future__ import annotations

import dataclasses
from typing import Callable, Dict, List, Literal, Optional, Tuple, Union

from drawlib.v0_2.private.core.model import LineStyle, ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core_canvas.canvas import line, rectangle


class BoxTreeNode:
    """Class for rendering smart art Tree."""

    def __init__(
        self,
        text: str,
        boxsize: Optional[Tuple[float, float]] = None,
        boxstyle: Union[str, ShapeStyle, None] = None,
        box_r: Optional[float] = None,
        box_horizontal_margin: Optional[float] = None,
        box_vertical_margin: Optional[float] = None,
        textstyle: Union[str, ShapeTextStyle, None] = None,
        linestyle: Union[str, LineStyle, None] = None,
        line_horizontal_length: Optional[float] = None,
        line_vertical_length: Optional[float] = None,
        children: Optional[List[BoxTreeNode]] = None,
        default_boxsize: Optional[Tuple[float, float]] = None,
        default_boxstyle: Union[str, ShapeStyle, None] = None,
        default_box_r: Optional[float] = None,
        default_box_horizontal_margin: Optional[float] = None,
        default_box_vertical_margin: Optional[float] = None,
        default_textstyle: Union[str, ShapeTextStyle, None] = None,
        default_linestyle: Union[str, LineStyle, None] = None,
        default_line_horizontal_length: Optional[float] = None,
        default_line_vertical_length: Optional[float] = None,
    ) -> None:
        """Initialize class."""
        self._text = text

        self._boxsize = boxsize
        if isinstance(boxstyle, str):
            boxstyle = dtheme.rectanglestyles.get(boxstyle)
        self._boxstyle = boxstyle
        self._box_r = box_r
        self._box_horizontal_margin = box_horizontal_margin
        self._box_vertical_margin = box_vertical_margin

        if isinstance(textstyle, str):
            textstyle = dtheme.rectangletextstyles.get(textstyle)
        self._textstyle = textstyle
        if isinstance(linestyle, str):
            linestyle = dtheme.linestyles.get(linestyle)
        self._linestyle = linestyle

        self._line_horizontal_length = line_horizontal_length
        self._line_vertical_length = line_vertical_length

        if children is None:
            self._children: List[BoxTreeNode] = []
        else:
            self._children: List[BoxTreeNode] = children

        self._default_boxsize = default_boxsize
        if isinstance(default_boxstyle, str):
            default_boxstyle = dtheme.rectanglestyles.get(default_boxstyle)
        self._default_boxstyle = default_boxstyle
        self._default_box_r = default_box_r
        self._default_box_horizontal_margin = default_box_horizontal_margin
        self._default_box_vertical_margin = default_box_vertical_margin

        if isinstance(default_textstyle, str):
            default_textstyle = dtheme.rectangletextstyles.get(default_textstyle)
        self._default_textstyle: Union[ShapeTextStyle, None] = default_textstyle
        if isinstance(default_linestyle, str):
            default_linestyle = dtheme.linestyles.get(default_linestyle)
        self._default_linestyle: Union[LineStyle, None] = default_linestyle

        self._default_line_horizontal_length = default_line_horizontal_length
        self._default_line_vertical_length = default_line_vertical_length

        self._drawing_item_name: Optional[str] = None

    def draw(
        self,
        xy: Tuple[float, float],
        orientation: Literal["horizontal", "vertical"],
        align: Literal["top", "bottom", "center", "left", "right"],
    ) -> None:
        """Write docstring later."""

    def _draw_vertical_left(
        self,
        xy: Tuple[float, float],
        orientation: Literal["horizontal", "vertical"],
        align: Literal["top", "bottom", "center", "left", "right"],
        default_textstyle: ShapeTextStyle,
        default_linestyle: LineStyle,
        default_line_horizontal_margin: float,
        default_line_horizontal_length: float,
        default_line_vertical_margin: float,
    ) -> None:
        """Write doc string later."""
