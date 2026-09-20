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

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeCoordinate,
    TypeFloat,
    TypePosFloat,
    TypeStr,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import line, rectangle
from drawlib._theme import get_style


class BoxTreeNode:
    """Class for rendering smart art Tree."""

    @guarded
    def __init__(
        self,
        text: TypeStr,
        boxsize: tuple[TypeFloat, TypeFloat] | None = None,
        boxstyle: TypeStr | Style | None = None,
        box_r: TypeFloat | None = None,
        box_horizontal_margin: TypeFloat | None = None,
        box_vertical_margin: TypeFloat | None = None,
        textstyle: TypeStr | Style | None = None,
        linestyle: TypeStr | Style | None = None,
        line_horizontal_length: TypeFloat | None = None,
        line_vertical_length: TypeFloat | None = None,
        children: list[BoxTreeNode] | None = None,
        default_boxsize: tuple[TypeFloat, TypeFloat] | None = None,
        default_boxstyle: TypeStr | Style | None = None,
        default_box_r: TypeFloat | None = None,
        default_box_horizontal_margin: TypeFloat | None = None,
        default_box_vertical_margin: TypeFloat | None = None,
        default_textstyle: TypeStr | Style | None = None,
        default_linestyle: TypeStr | Style | None = None,
        default_line_horizontal_length: TypeFloat | None = None,
        default_line_vertical_length: TypeFloat | None = None,
    ) -> None:
        """Initialize class."""
        self._text = text

        self._boxsize = boxsize
        if isinstance(boxstyle, str):
            boxstyle = get_style(boxstyle)
        self._boxstyle = boxstyle
        self._box_r = box_r
        self._box_horizontal_margin = box_horizontal_margin
        self._box_vertical_margin = box_vertical_margin

        if isinstance(textstyle, str):
            textstyle = get_style(textstyle)
        self._textstyle = textstyle
        if isinstance(linestyle, str):
            linestyle = get_style(linestyle)
        self._linestyle = linestyle

        self._line_horizontal_length = line_horizontal_length
        self._line_vertical_length = line_vertical_length

        if children is None:
            self._children: list[BoxTreeNode] = []
        else:
            self._children: list[BoxTreeNode] = children

        self._default_boxsize = default_boxsize
        if isinstance(default_boxstyle, str):
            default_boxstyle = get_style(default_boxstyle)
        self._default_boxstyle = default_boxstyle
        self._default_box_r = default_box_r
        self._default_box_horizontal_margin = default_box_horizontal_margin
        self._default_box_vertical_margin = default_box_vertical_margin

        if isinstance(default_textstyle, str):
            default_textstyle = get_style(default_textstyle)
        self._default_textstyle: Style | None = default_textstyle
        if isinstance(default_linestyle, str):
            default_linestyle = get_style(default_linestyle)
        self._default_linestyle: Style | None = default_linestyle

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
        default_textstyle: Style,
        default_linestyle: Style,
        default_line_horizontal_margin: float,
        default_line_horizontal_length: float,
        default_line_vertical_margin: float,
    ) -> None:
        """Write doc string later."""
