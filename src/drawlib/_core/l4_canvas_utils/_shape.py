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

from drawlib._core.l2_models import StaticContainer
from drawlib._core.l3_styles import (
    SYSTEM_DEFAULT_SHAPE_STYLE,
    SYSTEM_DEFAULT_SHAPE_TEXT_STYLE,
    Style,
)
from drawlib._core.l4_canvas_utils._colors import ColorUtil
from drawlib._core.l4_canvas_utils._text import TextUtil
from drawlib._core.l4_canvas_utils._utils import get_dict_value_none_keys_removed
from drawlib._preset_styles import get_style


class ShapeUtil(StaticContainer):
    """A utility class for handling shape styles and options."""

    @staticmethod
    def _resolve_style_item(
        val: Style | str | None,
        arg_name: str,
        getter: Callable | None = None,
    ) -> Style:
        if getter is not None:
            if val is None or isinstance(val, str):
                return getter(val if val is not None else "").copy()
            if isinstance(val, Style):
                return val.copy()
            raise ValueError(f'Arg "{arg_name}" must be Style or None, but {type(val)} given.')

        if val is None or isinstance(val, (Style, str)):
            return get_style(val).copy()
        raise ValueError(f'Arg "{arg_name}" must be Style or None, but {type(val)} given.')

    @staticmethod
    def format_styles(
        style: Style | str | None,
        textstyle: Style | str | None,
        get_style: Callable | None = None,
        get_textstyle: Callable | None = None,
    ) -> tuple[Style, Style]:
        formatted_style = ShapeUtil._resolve_style_item(style, "style", get_style)
        formatted_style = SYSTEM_DEFAULT_SHAPE_STYLE.merge(formatted_style)

        formatted_textstyle = ShapeUtil._resolve_style_item(textstyle, "textstyle", get_textstyle)
        formatted_textstyle = SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.merge(formatted_textstyle)

        return (formatted_style, formatted_textstyle)

    @staticmethod
    def apply_alignment(  # noqa: C901
        xy: tuple[float, float],
        width: float,
        height: float,
        angle: float | None,
        style: Style,
        is_default_center: bool = False,
    ) -> tuple[tuple[float, float], Style]:
        """Apply alignment adjustments to coordinates based on Style alignment settings.

        Args:
            xy (tuple[float, float]):
                The x, y coordinates to be adjusted.
            width (float):
                The width of the shape.
            height (float):
                The height of the shape.
            angle (float | None):
                The angle of rotation for the shape.
            style (Style):
                The Style object containing alignment properties.
            is_default_center (bool, optional):
                Flag indicating if default center alignment should be applied.
                Defaults to False.

        Returns:
            tuple[tuple[float, float], Style]: Adjusted coordinates and updated Style object.

        """
        x, y = xy
        if angle is None:
            if is_default_center:
                if style.text_halign is None:
                    style.text_halign = "center"
                if style.text_valign is None:
                    style.text_valign = "center"
            else:
                if style.text_halign is None:
                    style.text_halign = "left"
                if style.text_valign is None:
                    style.text_valign = "bottom"
        else:
            if style.text_halign is None:
                style.text_halign = "center"
            if style.text_valign is None:
                style.text_valign = "center"

        if is_default_center:
            if style.text_halign == "left":
                x += width / 2
            if style.text_halign == "right":
                x -= width / 2
            if style.text_valign == "bottom":
                y += height / 2
            if style.text_valign == "top":
                y -= height / 2
        else:
            if style.text_halign == "center":
                x -= width / 2
            if style.text_halign == "right":
                x -= width
            if style.text_valign == "center":
                y -= height / 2
            if style.text_valign == "top":
                y -= height

        return (x, y), style

    @staticmethod
    def get_shape_text(
        xy: tuple[float, float],
        angle: float | None,
        text: str,
        style: Style | None = None,
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
            style (Style | None, optional):
                The Style object containing text style properties.
                Defaults to None.

        Returns:
            matplotlib.text.Text: Shape center text object.
        """
        if style is None:
            style = Style()

        shape_angle = angle
        if shape_angle is None:
            shape_angle = 0.0

        if style.text_angle is not None:
            text_angle = style.text_angle
        else:
            text_angle = shape_angle
        if style.text_flip is not None and style.text_flip:
            text_angle = (text_angle + 180) % 360

        x, y = xy
        # shift
        if style.text_xy_shift is not None:
            x_shift, y_shift = style.text_xy_shift
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
        if style.text_xy_abs_shift is not None:
            x += style.text_xy_abs_shift[0]
            y += style.text_xy_abs_shift[1]

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
        style: Style | None = None,
        default_no_line: bool = True,
    ) -> dict[str, Any]:
        """Convert drawlib's Style to matplotlib's patches(shape) options.

        Args:
            style (Style | None, optional):
                The Style object containing shape style properties.
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
              linewidth, and alpha based on the Style object.
        """
        if style is None:
            if default_no_line:
                return {"linewidth": 0}
            return {}

        lcolor_val = style.get_line_color()
        fcolor_val = style.get_fill_color()
        lstyle_val = style.get_line_style()
        lwidth_val = style.get_line_width()

        lcolor = None if lcolor_val is None else ColorUtil.get_mplot_rgba(lcolor_val)
        fcolor = None if fcolor_val is None else ColorUtil.get_mplot_rgba(fcolor_val)

        # halign, valign will be used on shape. They are not in options.
        options: dict[str, Any] = {
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": lstyle_val,
            "linewidth": lwidth_val,
            "alpha": style.fill_alpha,
        }

        if options["linewidth"] is None:
            if default_no_line:
                options["linewidth"] = 0

        return get_dict_value_none_keys_removed(options)
