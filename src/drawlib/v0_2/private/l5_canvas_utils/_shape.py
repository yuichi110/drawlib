# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shape utility module for canvas operations."""

import math
from typing import Any, Callable

from matplotlib.text import Text

from drawlib.v0_2.private.l2_models import StaticContainer
from drawlib.v0_2.private.l3_styles import (
    SYSTEM_DEFAULT_SHAPE_STYLE,
    SYSTEM_DEFAULT_SHAPE_TEXT_STYLE,
    ShapeStyle,
    ShapeTextStyle,
)
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l5_canvas_utils._colors import ColorUtil
from drawlib.v0_2.private.l5_canvas_utils._text import TextUtil
from drawlib.v0_2.private.l5_canvas_utils._utils import get_dict_value_none_keys_removed


class ShapeUtil(StaticContainer):
    """A utility class for handling shape styles and options."""

    @staticmethod
    def format_styles(
        style: ShapeStyle | str | None,
        textstyle: ShapeTextStyle | str | None,
        get_style: Callable,
        get_textstyle: Callable,
    ) -> tuple[ShapeStyle, ShapeTextStyle]:
        """Format and retrieve ShapeStyle and ShapeTextStyle objects based on input parameters.

        Args:
            style (ShapeStyle | str | None):
                The style for the shape. Can be a ShapeStyle object, a style name (str),
                or None. If None, the default shape style from get_style() is used.
            textstyle (ShapeTextStyle | str | None):
                The style for the shape's text. Can be a ShapeTextStyle object, a style name (str),
                or None. If None, the default shape text style from get_textstyle() is used.
            get_style (Callable):
                A function to retrieve a ShapeStyle object by name or default.
            get_textstyle (Callable):
                A function to retrieve a ShapeTextStyle object by name or default.

        Returns:
            tuple[ShapeStyle, ShapeTextStyle]: The formatted ShapeStyle and ShapeTextStyle objects.

        Raises:
            ValueError: If the input style parameters are invalid or cannot be formatted.

        Notes:
            - The returned styles are merged results of the input styles, get_style(), get_textstyle(),
              SYSTEM_DEFAULT_SHAPE_STYLE, and SYSTEM_DEFAULT_SHAPE_TEXT_STYLE using corresponding merge functions.
            - If style or textstyle is a string, it is treated as the name of the style to fetch from get_style()
              or get_textstyle().
            - If style or textstyle is a ShapeStyle or ShapeTextStyle object, further processing may be applied
              to it as needed.
        """
        # ShapeStyle
        if style is None:
            style: ShapeStyle = get_style()
        elif isinstance(style, str):
            style: ShapeStyle = get_style(style)
        elif isinstance(style, ShapeStyle):
            style: ShapeStyle = style.copy()
        else:
            raise ValueError()
        style = get_style().merge(style)
        style = SYSTEM_DEFAULT_SHAPE_STYLE.merge(style)

        # ShapeTextStyle
        if textstyle is None:
            textstyle: ShapeTextStyle = get_textstyle()
        elif isinstance(textstyle, str):
            textstyle: ShapeTextStyle = get_textstyle(name=textstyle)
        elif isinstance(textstyle, ShapeTextStyle):
            textstyle: ShapeTextStyle = textstyle.copy()
        else:
            raise ValueError()
        textstyle = get_textstyle().merge(textstyle)
        textstyle = SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.merge(textstyle)

        return (style, textstyle)

    @staticmethod
    def apply_alignment(  # noqa: C901
        xy: tuple[float, float],
        width: float,
        height: float,
        angle: float | None,
        style: ShapeStyle,
        is_default_center: bool = False,
    ) -> tuple[tuple[float, float], ShapeStyle]:
        """Apply alignment adjustments to coordinates based on ShapeStyle alignment settings.

        Args:
            xy (tuple[float, float]):
                The x, y coordinates to be adjusted.
            width (float):
                The width of the shape.
            height (float):
                The height of the shape.
            angle (float | None):
                The angle of rotation for the shape.
            style (ShapeStyle):
                The ShapeStyle object containing alignment properties.
            is_default_center (bool, optional):
                Flag indicating if default center alignment should be applied.
                Defaults to False.

        Returns:
            tuple[tuple[float, float], ShapeStyle]: Adjusted coordinates and updated ShapeStyle object.

        """
        x, y = xy
        if angle is None:
            if is_default_center:
                if style.halign is None:
                    style.halign = "center"
                if style.valign is None:
                    style.valign = "center"
            else:
                if style.halign is None:
                    style.halign = "left"
                if style.valign is None:
                    style.valign = "bottom"
        else:
            if style.halign is None:
                style.halign = "center"
            if style.valign is None:
                style.valign = "center"

        if is_default_center:
            if style.halign == "left":
                x += width / 2
            if style.halign == "right":
                x -= width / 2
            if style.valign == "bottom":
                y += height / 2
            if style.valign == "top":
                y -= height / 2
        else:
            if style.halign == "center":
                x -= width / 2
            if style.halign == "right":
                x -= width
            if style.valign == "center":
                y -= height / 2
            if style.valign == "top":
                y -= height

        return (x, y), style

    @staticmethod
    def get_shape_text(
        xy: tuple[float, float],
        angle: float | None,
        text: str,
        style: ShapeTextStyle | None = None,
    ) -> Text:
        """Get text object which is drawn inside shape.

        Few shape objects can have text in its center.
        This function helps creating text object inside shape.
        Specifically, try to align to center of shapes.

        Args:
            xy (tuple[float, float]):
                The x, y coordinates of the shape's center.
            angle (float | None):
                The angle of rotation for the shape.
            text (str):
                The text content to be displayed.
            style (ShapeTextStyle | None, optional):
                The ShapeTextStyle object containing text style properties.
                Defaults to None.

        Returns:
            matplotlib.text.Text: Shape center text object.
        """
        if style is None:
            style = ShapeTextStyle()

        shape_angle = angle
        if shape_angle is None:
            shape_angle = 0.0

        if style.angle is not None:
            text_angle = style.angle
        else:
            text_angle = shape_angle
        if style.flip is not None and style.flip:
            text_angle = (text_angle + 180) % 360

        x, y = xy
        # shift
        if style.xy_shift is not None:
            x_shift, y_shift = style.xy_shift
            if shape_angle == 0:
                x += x_shift
                y += y_shift
            else:
                angle_rad = math.radians(shape_angle)
                rotated_x_shift = x_shift * math.cos(angle_rad) - y_shift * math.sin(angle_rad)
                rotated_y_shift = x_shift * math.sin(angle_rad) + y_shift * math.cos(angle_rad)
                x += rotated_x_shift
                y += rotated_y_shift

        # absolute shift
        if style.xy_abs_shift is not None:
            x += style.xy_abs_shift[0]
            y += style.xy_abs_shift[1]

        # only check color. ignore alignment
        options = TextUtil.get_text_options(style)
        if "horizontalalignment" in options:
            del options["horizontalalignment"]
        if "verticalalignment" in options:
            del options["verticalalignment"]

        return Text(
            x,
            y,
            text,
            rotation=text_angle,
            rotation_mode="anchor",
            horizontalalignment="center",
            verticalalignment="center",
            fontproperties=TextUtil.get_font_properties(style),
            **options,
        )

    @staticmethod
    def get_shape_options(
        style: ShapeStyle | None = None,
        default_no_line: bool = True,
    ) -> dict[str, Any]:
        """Convert drawlib's ShapeStyle to matplotlib's patches(shape) options.

        Args:
            style (ShapeStyle | None, optional):
                The ShapeStyle object containing shape style properties.
                Defaults to None.
            default_no_line (bool, optional):
                Flag indicating if default no line should be applied.
                Defaults to True.

        Returns:
            dict[str, Any]: Dictionary of options suitable for matplotlib patches.

        Notes:
            - If style is None and default_no_line is True, returns {"linewidth": 0}.
            - Returns an empty dictionary if style is None.
            - Otherwise, returns a dictionary containing facecolor, edgecolor, linestyle,
              linewidth, and alpha based on the ShapeStyle object.
        """
        if style is None:
            if default_no_line:
                return {"linewidth": 0}
            return {}

        lcolor = None if style.lcolor is None else ColorUtil.get_mplot_rgba(style.lcolor)
        fcolor = None if style.fcolor is None else ColorUtil.get_mplot_rgba(style.fcolor)

        # halign, valign will be used on shape. They are not in options.
        options: dict[str, Any] = {
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.lstyle,
            "linewidth": style.lwidth,
            "alpha": style.alpha,
        }

        if options["linewidth"] is None:
            if default_no_line:
                options["linewidth"] = 0

        return get_dict_value_none_keys_removed(options)
