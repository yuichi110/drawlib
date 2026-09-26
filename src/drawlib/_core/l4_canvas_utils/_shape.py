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
from typing import Any

from matplotlib.text import Text

from drawlib._core.l2_models import StaticContainer
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas_utils._colors import ColorUtil
from drawlib._core.l4_canvas_utils._text import TextUtil
from drawlib._core.l4_canvas_utils._utils import get_dict_value_none_keys_removed


class ShapeUtil(StaticContainer):
    """A utility class for handling shape styles and options."""

    @staticmethod
    def validate_shape_style(style: Style) -> None:
        """Validate that the required shape properties are set in Style.

        Args:
            style: The Style instance to validate.

        Raises:
            ValueError: If any required shape property is None.
        """
        missing: list[str] = []
        if style.shape_fill_color is None:
            missing.append("shape_fill_color")
        if style.shape_line_color is None:
            missing.append("shape_line_color")
        if style.shape_line_width is None:
            missing.append("shape_line_width")

        if missing:
            raise ValueError(
                f"Shape drawing requires attributes {missing}, but they are None in the provided Style."
            )

    @staticmethod
    def format_styles(
        style: Style,
        textstyle: Style | None = None,
    ) -> tuple[Style, Style | None]:
        """Validate and format shape style and embedded textstyle.

        Args:
            style: Style object for the shape (must have shape_* core properties).
            textstyle: Optional Style object for embedded text.

        Returns:
            tuple[Style, Style | None]: Tuple of (shape_style, text_style).

        Raises:
            TypeError: If style or textstyle is not a Style instance.
            ValueError: If required core properties are missing.
        """
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')

        ShapeUtil.validate_shape_style(style)

        if textstyle is not None:
            if not isinstance(textstyle, Style):
                raise TypeError(f'Arg "textstyle" must be Style, but {type(textstyle)} given.')
            TextUtil.validate_text_style(textstyle)

        return (style, textstyle)

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
            xy (tuple[float, float]): The x, y coordinates to be adjusted.
            width (float): The width of the shape.
            height (float): The height of the shape.
            angle (float | None): The angle of rotation for the shape.
            style (Style): The Style object containing alignment properties.
            is_default_center (bool, optional): Flag indicating default center alignment.

        Returns:
            tuple[tuple[float, float], Style]: Adjusted coordinates and updated Style object.
        """
        x, y = xy
        text_halign = style.text_halign
        text_valign = style.text_valign

        if angle is None:
            if is_default_center:
                if text_halign is None:
                    text_halign = "center"
                if text_valign is None:
                    text_valign = "center"
            else:
                if text_halign is None:
                    text_halign = "left"
                if text_valign is None:
                    text_valign = "bottom"
        else:
            if text_halign is None:
                text_halign = "center"
            if text_valign is None:
                text_valign = "center"

        if is_default_center:
            if text_halign == "left":
                x += width / 2
            if text_halign == "right":
                x -= width / 2
            if text_valign == "bottom":
                y += height / 2
            if text_valign == "top":
                y -= height / 2
        else:
            if text_halign == "center":
                x -= width / 2
            if text_halign == "right":
                x -= width
            if text_valign == "center":
                y -= height / 2
            if text_valign == "top":
                y -= height

        return (x, y), style.patch(text_halign=text_halign, text_valign=text_valign)

    @staticmethod
    def get_shape_text(
        xy: tuple[float, float],
        angle: float | None,
        text: str,
        style: Style,
    ) -> Text:
        """Get text object drawn inside shape center."""
        shape_angle = angle if angle is not None else 0.0

        text_angle = style.text_angle if style.text_angle is not None else shape_angle
        if style.text_flip is not None and style.text_flip:
            text_angle = (text_angle + 180) % 360

        x, y = xy
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

        if style.text_xy_abs_shift is not None:
            x += style.text_xy_abs_shift[0]
            y += style.text_xy_abs_shift[1]

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
        style: Style,
    ) -> dict[str, Any]:
        """Convert drawlib's Style to matplotlib's patches(shape) options."""
        lcolor = None if style.shape_line_color is None else ColorUtil.get_mplot_rgba(style.shape_line_color)
        fcolor = None if style.shape_fill_color is None else ColorUtil.get_mplot_rgba(style.shape_fill_color)

        options: dict[str, Any] = {
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.shape_line_style if style.shape_line_style is not None else "solid",
            "linewidth": style.shape_line_width,
            "alpha": style.shape_fill_alpha,
        }

        return get_dict_value_none_keys_removed(options)
