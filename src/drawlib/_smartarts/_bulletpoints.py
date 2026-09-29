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

from pydantic import BaseModel, validate_call

from drawlib._core.shapes import circle
from drawlib._core.text import text
from drawlib._core.types import Coordinate, PosFloat, Style


class _BulletPointsShape(BaseModel):
    """Shape settings for a specific indent level."""

    function: Callable
    style: Style
    args: dict


class _BulletPointsText(BaseModel):
    """Text settings for a specific indent level."""

    indent: int
    text: str
    style: Style


class BulletPoints:
    """A class to draw a list of bullet points with customizable styles and indentation.

    Args:
        vertical_margin (float): The vertical space between bullet points.
        indent_width (float): The width of the indentation for each level.
        default_style (Style, optional): The default text style for the bullet points.
    """

    @validate_call
    def __init__(
        self,
        *,
        vertical_margin: PosFloat,
        indent_width: PosFloat,
        default_style: Style | None = None,
    ) -> None:
        """Initialize BulletPoints.

        Args:
            vertical_margin (float): The vertical space between bullet points.
            indent_width (float): The width of the indentation for each level.
            default_style (Style, optional): The default text style for the bullet points.
        """
        self._vertical_margin = vertical_margin
        self._indent_width = indent_width
        self._default_style = default_style

        self._indent_level = 0
        self._bullet_texts: list[_BulletPointsText] = []
        self._bullet_shape_map: dict[int, _BulletPointsShape] = {}

        if default_style is not None:
            self._ensure_default_bullets(default_style)

    def _ensure_default_bullets(self, ref_style: Style) -> None:
        """Register default circle bullet shapes using text color."""
        text_color = ref_style.text_color
        style1 = Style(shape_line_color=text_color, shape_fill_color=text_color, shape_line_width=1.0)
        style2 = Style(shape_line_color=text_color, shape_fill_color=(0, 0, 0, 0.0), shape_line_width=1.0)
        if 1 not in self._bullet_shape_map:
            self.set_bullet_style(1, circle, style1, args={"radius": 0.5})
        if 2 not in self._bullet_shape_map:
            self.set_bullet_style(2, circle, style2, args={"radius": 0.5})

    @validate_call
    def set_indent(self, level: int) -> None:
        self._indent_level = level

    @validate_call
    def set_bullet_style(
        self,
        indent_level: int,
        function: Callable,
        style: Style,
        args: dict,
    ) -> None:
        style = style.patch(text_halign="center", text_valign="center")

        item = _BulletPointsShape(
            function=function,
            style=style,
            args=args,
        )

        self._bullet_shape_map[indent_level] = item

    @validate_call
    def add(
        self,
        text: str,
        style: Style | None = None,
    ) -> None:
        style_resolved = style if style is not None else self._default_style
        if style_resolved is None:
            raise ValueError(f"Neither 'default_style' nor 'style' was provided for item '{text}'.")

        self._ensure_default_bullets(style_resolved)
        style_resolved = style_resolved.patch(text_halign="left", text_valign="center")

        self._bullet_texts.append(
            _BulletPointsText(
                indent=self._indent_level,
                text=text,
                style=style_resolved,
            )
        )

    @validate_call
    def draw(
        self,
        xy: Coordinate,
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
