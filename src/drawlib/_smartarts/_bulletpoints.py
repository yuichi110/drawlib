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

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle, text


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
    """A class to draw a list of bullet points with customizable styles and indentation."""

    @validate_call
    def __init__(
        self,
        *,
        text_style: Style,
        vertical_margin: PosFloat,
        indent_width: PosFloat,
    ) -> None:
        """Initialize BulletPoints.

        Args:
            text_style: The default text style for the bullet points.
            vertical_margin: The vertical space between bullet points.
            indent_width: The width of the indentation for each level.
        """
        self._text_style = text_style
        self._vertical_margin = vertical_margin
        self._indent_width = indent_width

        self._indent_level = 0
        self._bullet_texts: list[_BulletPointsText] = []
        self._bullet_shape_map: dict[int, _BulletPointsShape] = {}
        self._ensure_default_bullets(text_style)

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
        """Set the current indentation level.

        Args:
            level: The indentation level (0 for top-level, 1 for first sub-bullet, etc.).
        """
        self._indent_level = level

    @validate_call
    def set_bullet_style(
        self,
        indent_level: int,
        function: Callable,
        style: Style,
        args: dict,
    ) -> None:
        """Configure bullet shape style for a specific indent level.

        Args:
            indent_level: Indent level to assign the bullet shape to.
            function: Shape drawing function (e.g. circle, rectangle).
            style: Style for the bullet shape.
            args: Additional arguments passed to the drawing function.
        """
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
        *,
        text_style: Style | None = None,
    ) -> None:
        """Add a bullet point text item.

        Args:
            text: Text to display for this bullet point.
            text_style: Custom style for this bullet point text. If None, default text_style is used.
        """
        style_resolved = text_style if text_style is not None else self._text_style
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
            xy: The starting point (x, y) to draw the bullet points.
        """
        y = xy[1]
        for bullet_text in self._bullet_texts:
            indent = bullet_text.indent
            text_ = bullet_text.text
            text_style = bullet_text.style

            x = xy[0] + self._indent_width * indent
            text(
                xy=(x, y),
                text=text_,
                style=text_style,
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
