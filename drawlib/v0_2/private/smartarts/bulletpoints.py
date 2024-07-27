# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""GridLayout implementation module."""

import dataclasses
from typing import Callable, List, Optional, Tuple, Union

from drawlib.v0_2.private.core.colors import Colors
from drawlib.v0_2.private.core.model import ShapeStyle, TextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core_canvas.canvas import circle, text


class BulletPoints:
    def __init__(
        self,
        vertical_margin: float,
        indent_width: float,
        default_style: Union[str, TextStyle, None] = None,
    ) -> None:
        self._vertical_margin = vertical_margin
        self._indent_width = indent_width
        if isinstance(default_style, str):
            default_style = dtheme.textstyles.get(default_style)
        if default_style is None:
            default_style = dtheme.textstyles.get()
        self._default_style = default_style

        self._indent_level = 0
        self._bullet_texts: List[_BulletPointsText] = []
        self._bullet_shape_map: dict[int, _BulletPointsShape] = {}

        # set default bullet styles
        text_color = default_style.color
        style1 = dtheme.shapestyles.get()
        style1.lcolor = text_color
        style1.fcolor = text_color
        style2 = dtheme.shapestyles.get()
        style2.lcolor = text_color
        style2.fcolor = Colors.Transparent
        self.set_bullet_style(1, circle, style1, args={"radius": 0.5})
        self.set_bullet_style(2, circle, style2, args={"radius": 0.5})

    def set_indent(self, level: int) -> None:
        self._indent_level = level

    def set_bullet_style(
        self,
        indent_level: int,
        function: Callable,
        style: Union[str, ShapeStyle],
        args: dict,
    ):
        if isinstance(style, str):
            style = dtheme.shapestyles.get(style)
        style.halign = "center"
        style.valign = "center"

        item = _BulletPointsShape(
            function=function,
            style=style,
            args=args,
        )

        self._bullet_shape_map[indent_level] = item

    def add(self, text: str, style: Union[str, TextStyle, None] = None) -> None:
        if isinstance(style, str):
            style = dtheme.textstyles.get(style)
        elif style is None:
            style = self._default_style
        if style is None:
            style = dtheme.textstyles.get()
        style.halign = "left"
        style.valign = "center"

        self._bullet_texts.append(
            _BulletPointsText(
                self._indent_level,
                text,
                style,
            )
        )

    def draw(self, xy: Tuple[float, float]) -> None:
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


@dataclasses.dataclass
class _BulletPointsShape:
    function: Callable
    style: ShapeStyle
    args: dict


@dataclasses.dataclass
class _BulletPointsText:
    indent: int
    text: str
    style: TextStyle
