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

from drawlib.v0_2.private.l1_core import guarded
from drawlib.v0_2.private.l2_types import (
    TypeCoordinate,
    TypeFloat,
    TypeInt,
    TypePosFloat,
    TypeStr,
)
from drawlib.v0_2.private.l3_styles import Colors, ShapeStyle, TextStyle
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l5_canvas import circle, text


class _BulletPointsShape(BaseModel):
    """Shape settings for a specific indent level."""

    function: Callable
    style: ShapeStyle
    args: dict


class _BulletPointsText(BaseModel):
    """Text settings for a specific indent level."""

    indent: TypeInt
    text: TypeStr
    style: TextStyle


class BulletPoints:
    """A class to draw a list of bullet points with customizable styles and indentation.

    Args:
        vertical_margin (float): The vertical space between bullet points.
        indent_width (float): The width of the indentation for each level.
        default_style (Union[str, TextStyle, None]): The default text style for the bullet points.
    """

    @guarded
    def __init__(
        self,
        vertical_margin: TypePosFloat,
        indent_width: TypePosFloat,
        default_style: TypeStr | TextStyle | None = None,
    ) -> None:
        """Initialize BulletPoints.

        Args:
            vertical_margin (float): The vertical space between bullet points.
            indent_width (float): The width of the indentation for each level.
            default_style (Union[str, TextStyle, None]): The default text style for the bullet points.
        """
        self._vertical_margin = vertical_margin
        self._indent_width = indent_width
        if isinstance(default_style, str):
            default_style = dtheme.textstyles.get(default_style)
        if default_style is None:
            default_style = dtheme.textstyles.get()
        self._default_style = default_style

        self._indent_level = 0
        self._bullet_texts: list[_BulletPointsText] = []
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

    @guarded
    def set_indent(self, level: TypeInt) -> None:
        """Sets the indentation level for the next bullet point.

        Args:
            level (int): The indentation level.
        """
        self._indent_level = level

    @guarded
    def set_bullet_style(
        self,
        indent_level: TypeInt,
        function: Callable,
        style: TypeStr | ShapeStyle,
        args: dict,
    ) -> None:
        """Sets the style and function for drawing bullets at a specific indentation level.

        Args:
            indent_level (int): The indentation level to apply the style to.
            function (Callable): The function to draw the bullet shape.
            style (Union[str, ShapeStyle]): The style to apply to the bullet shape.
            args (dict): Additional arguments to pass to the drawing function.
        """
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

    @guarded
    def add(
        self,
        text: TypeStr,
        style: TypeStr | TextStyle | None = None,
    ) -> None:
        """Adds a bullet point with the specified text and style.

        Args:
            text (str): The text for the bullet point.
            style (Union[str, TextStyle, None]): The text style for the bullet point.
        """
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
                indent=self._indent_level,
                text=text,
                style=style,
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
