# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""BulletPoints implementation module."""

from typing import Callable

from pydantic import BaseModel

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeCoordinate,
    TypeFloat,
    TypeInt,
    TypePosFloat,
    TypeStr,
)
from drawlib._core.l3_styles import Colors, Style
from drawlib._core.l4_canvas import circle, text
from drawlib._preset_styles import get_style


class _BulletPointsShape(BaseModel):
    """Shape settings for a specific indent level."""

    function: Callable
    style: Style
    args: dict


class _BulletPointsText(BaseModel):
    """Text settings for a specific indent level."""

    indent: TypeInt
    text: TypeStr
    style: Style


class BulletPoints:
    """A class to draw a list of bullet points with customizable styles and indentation.

    Args:
        vertical_margin (float): The vertical space between bullet points.
        indent_width (float): The width of the indentation for each level.
        default_style (Union[str, Style, None]): The default text style for the bullet points.
    """

    @guarded
    def __init__(
        self,
        vertical_margin: TypePosFloat,
        indent_width: TypePosFloat,
        default_style: TypeStr | Style | None = None,
    ) -> None:
        """Initialize BulletPoints.

        Args:
            vertical_margin (float): The vertical space between bullet points.
            indent_width (float): The width of the indentation for each level.
            default_style (Union[str, Style, None]): The default text style for the bullet points.
        """
        self._vertical_margin = vertical_margin
        self._indent_width = indent_width
        self._default_style = get_style(default_style)

        self._indent_level = 0
        self._bullet_texts: list[_BulletPointsText] = []
        self._bullet_shape_map: dict[int, _BulletPointsShape] = {}

        # set default bullet styles
        text_color = self._default_style.text_color
        style1 = get_style()
        style1.line_color = text_color
        style1.fill_color = text_color
        style2 = get_style()
        style2.line_color = text_color
        style2.fill_color = Colors.Transparent
        self.set_bullet_style(1, circle, style1, args={"radius": 0.5})
        self.set_bullet_style(2, circle, style2, args={"radius": 0.5})

    @guarded
    def set_indent(self, level: TypeInt) -> None:
        self._indent_level = level

    @guarded
    def set_bullet_style(
        self,
        indent_level: TypeInt,
        function: Callable,
        style: TypeStr | Style,
        args: dict,
    ) -> None:
        if isinstance(style, str):
            style = get_style(style)
        style.text_halign = "center"
        style.text_valign = "center"

        item = _BulletPointsShape(
            function=function,
            style=style,
            args=args,
        )

        self._bullet_shape_map[indent_level] = item

    @guarded
    def add(
        self,
        text: TypeStr,
        style: TypeStr | Style | None = None,
    ) -> None:
        style_resolved = get_style(style) if style is not None else self._default_style
        style_resolved = get_style(style_resolved)
        style_resolved.text_halign = "left"
        style_resolved.text_valign = "center"

        self._bullet_texts.append(
            _BulletPointsText(
                indent=self._indent_level,
                text=text,
                style=style_resolved,
            )
        )

    @guarded
    def draw(
        self,
        xy: TypeCoordinate,
    ) -> None:
        """Draws the list of bullet points starting from the specified location.

        Args:
            xy (Tuple[float, float]): The starting point (x, y) to draw the bullet points.
        """
        y = xy[1]
        for bullet_text in self._bullet_texts:
            indent = bullet_text.indent
            text_ = bullet_text.text
            textstyle = bullet_text.style

            x = xy[0] + self._indent_width * indent
            text(
                xy=(x, y),
                text=text_,
                style=textstyle,
            )

            if indent == 0:
                ...
            elif indent not in self._bullet_shape_map:
                ...
            else:
                bps = self._bullet_shape_map[indent]
                function = bps.function
                shapestyle = bps.style
                args = bps.args

                x = xy[0] + self._indent_width * (indent - 0.5)
                args["xy"] = (x, y)
                args["style"] = shapestyle
                function(**args)

            y -= self._vertical_margin
