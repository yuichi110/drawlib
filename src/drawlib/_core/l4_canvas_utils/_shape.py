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

from drawlib._core.l2_types import Size
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas_utils._colors import ColorUtil
from drawlib._core.l4_canvas_utils._text import TextUtil
from drawlib._core.l4_canvas_utils._utils import get_dict_value_none_keys_removed


class ShapeUtil:
    """A utility class for handling shape styles and options."""

    def __init__(self) -> None:
        """Raise TypeError to prevent instantiation of utility class."""
        raise TypeError(f"'{self.__class__.__name__}' is a static utility class and cannot be instantiated.")

    @staticmethod
    def validate_shape_style(style: Style) -> None:
        """Validate that the required shape properties are set in Style.

        Args:
            style: The Style instance to validate.

        Raises:
            ValueError: If style does not support shapes or any required shape property is None.
        """
        if "shape" not in style.supports:
            raise ValueError(f"Style cannot be used for shapes. Declared supports: {set(style.supports)}.")
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
    def resolve_embedded_text_style(
        shape_style: Style,
        textstyle: Style | None = None,
        textsize: Size | None = None,
    ) -> Style:
        """Resolve effective text style for embedded text in shapes with automatic contrast.

        Args:
            shape_style: The container shape's Style instance.
            textstyle: Optional explicit textstyle provided by the caller.
            textsize: Optional font size override.

        Returns:
            Style: Validated, complete text style for drawing embedded text.
        """
        if textstyle is not None:
            if not isinstance(textstyle, Style):
                raise TypeError(f'Arg "textstyle" must be Style, but {type(textstyle)} given.')
            effective = textstyle
            if textsize is not None:
                effective = effective.patch(text_size=textsize)
            TextUtil.validate_text_style(effective)
            return effective

        # Automatic contrast resolution
        fill_color = shape_style.shape_fill_color
        fill_alpha = shape_style.shape_fill_alpha

        if fill_color is None:
            is_transparent = True
            fill_rgba = (0.0, 0.0, 0.0, 0.0)
        else:
            fill_rgba = ColorUtil.get_mplot_rgba(fill_color, fill_alpha)
            is_transparent = fill_rgba[3] < 0.3 or fill_rgba == (0.0, 0.0, 0.0, 0.0)

        if is_transparent:
            if shape_style.shape_line_color is not None:
                text_col = shape_style.shape_line_color
            else:
                text_col = (40, 40, 40, 1.0)
        else:
            luminance = 0.299 * fill_rgba[0] + 0.587 * fill_rgba[1] + 0.114 * fill_rgba[2]
            if luminance > 0.6:
                text_col = (40, 40, 40, 1.0)
            else:
                text_col = (255, 255, 255, 1.0)

        size = (
            textsize
            if textsize is not None
            else (shape_style.text_size if shape_style.text_size is not None else 16)
        )
        font = shape_style.text_font if shape_style.text_font is not None else Font.SANSSERIF_REGULAR
        halign = shape_style.text_halign if shape_style.text_halign is not None else "center"
        valign = shape_style.text_valign if shape_style.text_valign is not None else "center"

        return Style(
            supports={"text"},
            text_color=text_col,
            text_size=size,
            text_font=font,
            text_halign=halign,
            text_valign=valign,
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
