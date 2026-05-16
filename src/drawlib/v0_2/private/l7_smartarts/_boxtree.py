# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""BoxTree implementation module."""

from __future__ import annotations

from typing import Literal

from drawlib.v0_2.private.l1_core import guarded
from drawlib.v0_2.private.l2_types import (
    TypeCoordinate,
    TypeFloat,
    TypePosFloat,
    TypeStr,
)
from drawlib.v0_2.private.l3_styles import LineStyle, ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l5_canvas import line, rectangle


class BoxTreeNode:
    """Class for rendering smart art Tree."""

    @guarded
    def __init__(
        self,
        text: TypeStr,
        boxsize: tuple[TypeFloat, TypeFloat] | None = None,
        boxstyle: TypeStr | ShapeStyle | None = None,
        box_r: TypeFloat | None = None,
        box_horizontal_margin: TypeFloat | None = None,
        box_vertical_margin: TypeFloat | None = None,
        textstyle: TypeStr | ShapeTextStyle | None = None,
        linestyle: TypeStr | LineStyle | None = None,
        line_horizontal_length: TypeFloat | None = None,
        line_vertical_length: TypeFloat | None = None,
        children: list[BoxTreeNode] | None = None,
        default_boxsize: tuple[TypeFloat, TypeFloat] | None = None,
        default_boxstyle: TypeStr | ShapeStyle | None = None,
        default_box_r: TypeFloat | None = None,
        default_box_horizontal_margin: TypeFloat | None = None,
        default_box_vertical_margin: TypeFloat | None = None,
        default_textstyle: TypeStr | ShapeTextStyle | None = None,
        default_linestyle: TypeStr | LineStyle | None = None,
        default_line_horizontal_length: TypeFloat | None = None,
        default_line_vertical_length: TypeFloat | None = None,
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
            self._children: list[BoxTreeNode] = []
        else:
            self._children: list[BoxTreeNode] = children

        self._default_boxsize = default_boxsize
        if isinstance(default_boxstyle, str):
            default_boxstyle = dtheme.rectanglestyles.get(default_boxstyle)
        self._default_boxstyle = default_boxstyle
        self._default_box_r = default_box_r
        self._default_box_horizontal_margin = default_box_horizontal_margin
        self._default_box_vertical_margin = default_box_vertical_margin

        if isinstance(default_textstyle, str):
            default_textstyle = dtheme.rectangletextstyles.get(default_textstyle)
        self._default_textstyle: ShapeTextStyle | None = default_textstyle
        if isinstance(default_linestyle, str):
            default_linestyle = dtheme.linestyles.get(default_linestyle)
        self._default_linestyle: LineStyle | None = default_linestyle

        self._default_line_horizontal_length = default_line_horizontal_length
        self._default_line_vertical_length = default_line_vertical_length

        self._drawing_item_name: str | None = None

    @guarded
    def draw(
        self,
        xy: TypeCoordinate,
        orientation: Literal["horizontal", "vertical"],
        align: Literal["top", "bottom", "center", "left", "right"],
    ) -> None:
        """Write docstring later."""

    def _draw_vertical_left(
        self,
        xy: TypeCoordinate,
        orientation: Literal["horizontal", "vertical"],
        align: Literal["top", "bottom", "center", "left", "right"],
        default_textstyle: ShapeTextStyle,
        default_linestyle: LineStyle,
        default_line_horizontal_margin: float,
        default_line_horizontal_length: float,
        default_line_vertical_margin: float,
    ) -> None:
        """Write doc string later."""
