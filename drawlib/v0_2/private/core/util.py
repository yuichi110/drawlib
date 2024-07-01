# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Utility module for converting drawlib data to matplotlib data."""

import math
from typing import Any, Callable, Dict, Literal, Optional, Tuple, Union

from matplotlib.font_manager import FontProperties
from matplotlib.text import Text

from drawlib.v0_2.private.core.colors import Colors
from drawlib.v0_2.private.core.fonts import (
    FontBase,
    FontFile,
)
from drawlib.v0_2.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.core.model_system_default import (
    SYSTEM_DEFAULT_ICON_STYLE,
    SYSTEM_DEFAULT_IMAGE_STYLE,
    SYSTEM_DEFAULT_LINE_STYLE,
    SYSTEM_DEFAULT_SHAPE_STYLE,
    SYSTEM_DEFAULT_SHAPE_TEXT_STYLE,
    SYSTEM_DEFAULT_TEXT_STYLE,
)
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.download import download_if_not_exist


class ColorUtil:
    """A utility class for color conversion operations."""

    @staticmethod
    def get_mplot_rgba(
        rgb_or_rgba: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        alpha: Optional[float] = None,
    ) -> Tuple[float, float, float, float]:
        """Convert 0~255 RGB/RGBA to 0.0 ~ 1.0 RGBA for matplotlib.

        drawlib prefers 0~255 RGB/RGBA.
        matplotlib uses 0.0~1.0 RGB/RGBA.

        This function provides a converter from drawlib format to matplotlib format.
        The alpha channel is handled as follows:

        1. If the `alpha` argument is provided, use it.
        2. If the original data is RGBA, use its alpha value.
        3. Set alpha to 1.0 if not provided.

        Args:
            rgb_or_rgba (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                RGB or RGBA color tuple where components are in the range 0 to 255.
                If RGBA, the alpha component should be in the range 0.0 to 1.0.
            alpha (Optional[float]): Optional alpha value to override the input alpha.

        Returns:
            Tuple[float, float, float, float]: Tuple representing matplotlib's RGBA format.
        """
        r = round(rgb_or_rgba[0] / 255, 5)
        g = round(rgb_or_rgba[1] / 255, 5)
        b = round(rgb_or_rgba[2] / 255, 5)

        if alpha is not None:
            a = alpha
        elif len(rgb_or_rgba) == 3:
            a = 1.0
        else:
            a = rgb_or_rgba[3]

        return (r, g, b, a)

    @staticmethod
    def get_hexrgb(
        rgb_or_rgba: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
    ) -> str:
        """Convert RGB or RGBA tuple to hexadecimal color code.

        Args:
            rgb_or_rgba (Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
                RGB or RGBA color tuple where components are in the range 0 to 255.
                If RGBA, the alpha component should be in the range 0.0 to 1.0.

        Returns:
            str: Hexadecimal color code in the format "#RRGGBB" or "#RRGGBBAA" (if alpha < 1.0).

        Raises:
            ValueError: If RGB values are out of range (0-255).
        """
        r = rgb_or_rgba[0]
        g = rgb_or_rgba[1]
        b = rgb_or_rgba[2]
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("RGB values must be in the range 0 to 255.")
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        return hex_color

    @staticmethod
    def get_rgba_from_hex(hex_color: str) -> Tuple[int, int, int, float]:
        """Convert a hexadecimal color code to RGBA values.

        Args:
            hex_color (str): The hexadecimal color code (e.g., "#FF5733" or "#FFF").

        Returns:
            tuple[int, int, int, float]: A tuple containing the RGBA values (0-255 for R, G, B and 0.0-1.0 for A).

        Raises:
            ValueError: If the hex_color format is invalid.
        """
        # Remove the '#' prefix if present
        hex_color = hex_color.lstrip("#")

        # Determine the length of the hex color code
        hex_length = len(hex_color)

        # Convert the hex code to RGB values
        if hex_length == 3:  # Short hex format (#RGB)
            r = int(hex_color[0] * 2, 16)
            g = int(hex_color[1] * 2, 16)
            b = int(hex_color[2] * 2, 16)
            a = 1.0
        elif hex_length in {6, 8}:  # Full hex format (#RRGGBB)
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            if hex_length == 8:  # With alpha
                a = int(hex_color[6:8], 16)
            else:
                a = 1.0
        else:
            raise ValueError("Invalid hex color code format")

        return (r, g, b, a)


class IconUtil:
    """A utility class for handling icon styles."""

    @staticmethod
    def format_style(
        style: Union[IconStyle, str, None],
        default_icon_style: Optional[str] = None,
    ) -> IconStyle:
        """Format and retrieve an IconStyle object based on input parameters.

        Args:
            style (Union[IconStyle, str, None]):
                The style to format. Can be an IconStyle object, a style name (str),
                or None. If None, the default icon style from dtheme.iconstyles is used.
            default_icon_style (Optional[str]):
                Default style name to use if style is None or a string.

        Returns:
            IconStyle: The formatted IconStyle object.

        Raises:
            ValueError: If the input style parameter is invalid or cannot be formatted.

        Notes:
            - If default_icon_style is provided, it will override dtheme.iconstyles.get().
            - The returned style is a merged result of the input style, dtheme.iconstyles.get(),
              and SYSTEM_DEFAULT_ICON_STYLE.
        """
        if default_icon_style is None:
            ...
        elif isinstance(default_icon_style, str):
            ...
        else:
            raise ValueError()

        if style is None:
            style = dtheme.iconstyles.get()
        elif isinstance(style, str):
            style = dtheme.iconstyles.get(name=style)
        elif isinstance(style, IconStyle):
            ...
        else:
            raise ValueError()

        style = dtheme.iconstyles.get().merge(style)
        style = SYSTEM_DEFAULT_ICON_STYLE.merge(style)
        return style


class ImageUtil:
    """A utility class for handling image styles."""

    @staticmethod
    def format_style(style: Union[ImageStyle, str, None]) -> ImageStyle:
        """Format and retrieve an ImageStyle object based on input parameters.

        Args:
            style (Union[ImageStyle, str, None]):
                The style to format. Can be an ImageStyle object, a style name (str),
                or None. If None, the default image style from dtheme.imagestyles is used.

        Returns:
            ImageStyle: The formatted ImageStyle object.

        Raises:
            ValueError: If the input style parameter is invalid or cannot be formatted.

        Notes:
            - The returned style is a merged result of the input style, dtheme.imagestyles.get(),
              and SYSTEM_DEFAULT_IMAGE_STYLE.
            - If style is a string, it is treated as the name of the style to fetch from dtheme.imagestyles.
            - If style is an ImageStyle object, it will be copied before further processing to avoid
              modifying the original object.
        """
        if style is None:
            style = dtheme.imagestyles.get()
        elif isinstance(style, str):
            style = dtheme.imagestyles.get(name=style)
        elif isinstance(style, ImageStyle):
            style = style.copy()
        else:
            raise ValueError()

        style = dtheme.imagestyles.get().merge(style)
        style = SYSTEM_DEFAULT_IMAGE_STYLE.merge(style)
        return style


class LineUtil:
    """A utility class for handling line styles and options."""

    @staticmethod
    def format_style(
        style: Union[LineStyle, str, None],
    ) -> LineStyle:
        """Format and retrieve a LineStyle object based on input parameters.

        Args:
            style (Union[LineStyle, str, None]):
                The style to format. Can be a LineStyle object, a style name (str),
                or None. If None, the default line style from dtheme.linestyles is used.

        Returns:
            LineStyle: The formatted LineStyle object.

        Raises:
            ValueError: If the input style parameter is invalid or cannot be formatted.

        Notes:
            - The returned style is a merged result of the input style, dtheme.linestyles.get(),
              and SYSTEM_DEFAULT_LINE_STYLE.
        """
        if style is None:
            style = dtheme.linestyles.get()
        elif isinstance(style, str):
            style = dtheme.linestyles.get(name=style)
        elif isinstance(style, LineStyle):
            ...
        else:
            raise ValueError('Arg "style" type must be one of LineStyle, str, None.' f' But "{type(style)}" is given.')

        style = dtheme.linestyles.get().merge(style)
        style = SYSTEM_DEFAULT_LINE_STYLE.merge(style)
        return style

    @staticmethod
    def get_fancyarrowpatch_options(
        arrowhead: Literal["", "->", "<-", "<->"],
        style: LineStyle,
    ) -> Dict[str, Any]:
        """Convert drawlib's LineStyle to matplotlib's line options for fancy arrow patches.

        Matplotlib handles line style arguments in its function calls.
        This method converts drawlib's LineStyle into a dictionary suitable for
        matplotlib's function parameters.

        Args:
            arrowhead (Literal["", "->", "<-", "<->"]):
                The arrowhead style to apply. "" for no arrow, "->" for one-way arrow,
                "<-" for opposite one-way arrow, "<->" for two-way arrow.
            style (LineStyle):
                The LineStyle object containing line properties.

        Returns:
            Dict[str, Any]: A dictionary containing matplotlib's line options.

        Notes:
            - Apply the returned options dictionary to matplotlib's function calls,
              e.g., `Line2D(arg1, ..., **options)`, to apply LineStyle's style.
        """
        color = None if style.color is None else ColorUtil.get_mplot_rgba(style.color)
        options = {
            "linewidth": style.width,
            "linestyle": style.style,
            "color": color,
            "alpha": style.alpha,
        }

        if not arrowhead:
            options["arrowstyle"] = "-"

        else:
            options["mutation_scale"] = style.ahscale
            if style.ahfill:
                if arrowhead == "->":
                    options["arrowstyle"] = "-|>"
                elif arrowhead == "<-":
                    options["arrowstyle"] = "<|-"
                else:
                    options["arrowstyle"] = "<|-|>"
            else:
                options["arrowstyle"] = arrowhead

        return _get_dict_value_none_keys_removed(options)


class ShapeUtil:
    """A utility class for handling shape styles and options."""

    @staticmethod
    def format_styles(
        style: Union[ShapeStyle, str, None],  # type: ignore
        textstyle: Union[ShapeTextStyle, str, None],  # type: ignore
        get_style: Callable,
        get_textstyle: Callable,
    ) -> Tuple[ShapeStyle, ShapeTextStyle]:
        """Format and retrieve ShapeStyle and ShapeTextStyle objects based on input parameters.

        Args:
            style (Union[ShapeStyle, str, None]):
                The style for the shape. Can be a ShapeStyle object, a style name (str),
                or None. If None, the default shape style from get_style() is used.
            textstyle (Union[ShapeStyle, str, None]):
                The style for the shape's text. Can be a ShapeTextStyle object, a style name (str),
                or None. If None, the default shape text style from get_textstyle() is used.
            get_style (Callable):
                A function to retrieve a ShapeStyle object by name or default.
            get_textstyle (Callable):
                A function to retrieve a ShapeTextStyle object by name or default.

        Returns:
            Tuple[ShapeStyle, ShapeTextStyle]: The formatted ShapeStyle and ShapeTextStyle objects.

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
        xy: Tuple[float, float],
        width: float,
        height: float,
        angle: Optional[float],
        style: ShapeStyle,
        is_default_center: bool = False,
    ) -> Tuple[Tuple[float, float], ShapeStyle]:
        """Apply alignment adjustments to coordinates based on ShapeStyle alignment settings.

        Args:
            xy (Tuple[float, float]):
                The x, y coordinates to be adjusted.
            width (float):
                The width of the shape.
            height (float):
                The height of the shape.
            angle (Optional[float]):
                The angle of rotation for the shape.
            style (ShapeStyle):
                The ShapeStyle object containing alignment properties.
            is_default_center (bool, optional):
                Flag indicating if default center alignment should be applied.
                Defaults to False.

        Returns:
            Tuple[Tuple[float, float], ShapeStyle]: Adjusted coordinates and updated ShapeStyle object.

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
        xy: Tuple[float, float],
        angle: Optional[float],
        text: str,
        style: Optional[ShapeTextStyle] = None,
    ) -> Text:
        """Get text object which is drawn inside shape.

        Few shape objects can have text in its center.
        This function helps creating text object inside shape.
        Specifically, try to align to center of shapes.

        Args:
            xy (Tuple[float, float]):
                The x, y coordinates of the shape's center.
            angle (Optional[float]):
                The angle of rotation for the shape.
            text (str):
                The text content to be displayed.
            style (Optional[ShapeTextStyle], optional):
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
        style: Optional[ShapeStyle] = None,
        default_no_line: bool = True,
    ) -> Dict[str, Any]:
        """Convert drawlib's ShapeStyle to matplotlib's patches(shape) options.

        Args:
            style (Optional[ShapeStyle], optional):
                The ShapeStyle object containing shape style properties.
                Defaults to None.
            default_no_line (bool, optional):
                Flag indicating if default no line should be applied.
                Defaults to True.

        Returns:
            Dict[str, Any]: Dictionary of options suitable for matplotlib patches.

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
        options = {
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.lstyle,
            "linewidth": style.lwidth,
            "alpha": style.alpha,
        }

        if options["linewidth"] is None:
            if default_no_line:
                options["linewidth"] = 0

        return _get_dict_value_none_keys_removed(options)


class TextUtil:
    """A utility class for handling text styles and options."""

    @staticmethod
    def format_style(style: Union[TextStyle, str, None]) -> TextStyle:
        """Format and retrieve TextStyle object based on input parameters.

        Args:
            style (Union[TextStyle, str, None]):
                The style for the text. Can be a TextStyle object, a style name (str),
                or None. If None, the default text style from dtheme.textstyles.get() is used.

        Returns:
            TextStyle: The formatted TextStyle object.

        Raises:
            ValueError: If the input style parameter is invalid or cannot be formatted.

        Notes:
            - The returned style is a merged result of the input style, dtheme.textstyles.get(),
              SYSTEM_DEFAULT_TEXT_STYLE, and using TextStyle's merge function.
            - If style is a string, it is treated as the name of the style to fetch from dtheme.textstyles.get().
            - If style is a TextStyle object, further processing may be applied to it as needed.

        """
        if style is None:
            style = dtheme.textstyles.get()
        elif isinstance(style, str):
            style = dtheme.textstyles.get(name=style)
        elif isinstance(style, TextStyle):
            style = style.copy()
        else:
            raise ValueError()

        style = dtheme.textstyles.get().merge(style)
        system_default = SYSTEM_DEFAULT_TEXT_STYLE.copy()
        system_default.bgalpha = None
        system_default.bglcolor = None
        system_default.bglstyle = None
        system_default.bglwidth = None
        system_default.bgfcolor = None
        style = system_default.merge(style)
        return style

    @staticmethod
    def get_text_options(
        style: Union[TextStyle, ShapeTextStyle, None],
    ) -> Dict[str, Any]:
        """Convert drawlib's TextStyle or ShapeTextStyle to matplotlib's text options.

        Args:
            style (Union[TextStyle, ShapeTextStyle, None]):
                The TextStyle or ShapeTextStyle object containing text style properties.

        Returns:
            Dict[str, Any]: Dictionary of options suitable for matplotlib text handling.

        Notes:
            - If style is None, returns an empty dictionary.
            - Converts color, horizontalalignment, and verticalalignment properties
              from TextStyle or ShapeTextStyle to matplotlib compatible options.
        """
        if style is None:
            return {}

        # convert rgb -> matplot rgb
        color = None if style.color is None else ColorUtil.get_mplot_rgba(style.color)

        options = {
            "color": color,
            "horizontalalignment": style.halign,
            "verticalalignment": style.valign,
        }

        return _get_dict_value_none_keys_removed(options)

    @staticmethod
    def get_font_properties(  # noqa: C901
        style: Union[TextStyle, ShapeTextStyle],
    ) -> Optional[FontProperties]:
        """Create matplotlib's FontProperties object from TextStyle or ShapeTextStyle.

        Args:
            style (Union[TextStyle, ShapeTextStyle, None]):
                The TextStyle or ShapeTextStyle object containing font properties.

        Returns:
            Optional[FontProperties]: FontProperties object or None if style is None.

        Notes:
            - Returns FontProperties object based on TextStyle's font and size properties.
            - Handles default font settings and user-specified fonts.
        """
        if isinstance(style, TextStyle):
            default = dtheme.textstyles.get()
            if default.size is None:
                default.size = SYSTEM_DEFAULT_TEXT_STYLE.size
            if default.font is None:
                default.font = SYSTEM_DEFAULT_TEXT_STYLE.font

        elif isinstance(style, ShapeTextStyle):
            default = dtheme.shapetextstyles.get()
            if default.size is None:
                default.size = SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.size
            if default.font is None:
                default.font = SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.font

        else:
            raise ValueError()

        # use user font file
        if isinstance(style.font, FontFile):
            if style.size is None:
                style.size = default.size
            return FontProperties(size=style.size, fname=style.font.file)

        # use default font
        file_path, download_url, md5_hash = default.font.value  # type: ignore
        download_if_not_exist(file_path=file_path, download_url=download_url, md5_hash=md5_hash)

        if style is None:
            return FontProperties(size=default.size, fname=file_path)

        if style.font is None:
            if style.size is None:
                style.size = default.size
            return FontProperties(size=style.size, fname=file_path)

        # use specified font

        if isinstance(style.font, FontBase):
            # get True for all BaseFont subclasses
            if style.size is None:
                style.size = default.size

            file_path, download_url, md5_hash = style.font.value
            download_if_not_exist(file_path=file_path, download_url=download_url, md5_hash=md5_hash)
            return FontProperties(size=style.size, fname=file_path)

        raise ValueError(f"font type {type(style.font)} is not supported")

    @staticmethod
    def get_bbox_dict(
        style: Optional[TextStyle] = None,
    ) -> Optional[Dict[str, Any]]:
        """Convert drawlib's TextStyle to matplotlib's text background options.

        Args:
            style (Optional[TextStyle]):
                The TextStyle object containing text background style properties.

        Returns:
            Optional[Dict[str, Any]]: Dictionary of options suitable for matplotlib's text background.

        Notes:
            - Returns None if style is None or if all background properties are None.
            - Converts bgfcolor, bglcolor, bglstyle, bglwidth, and bgalpha properties
              from TextStyle to matplotlib compatible bbox options.
        """
        # {} doesn't mean no style.
        # requires returning None when no style.

        if style is None:
            return None

        all_none = True
        for e in [style.bgfcolor, style.bglcolor, style.bglstyle]:
            if e is not None:
                all_none = False
        if all_none:
            return None

        # background exist

        lcolor = None if style.bglcolor is None else ColorUtil.get_mplot_rgba(style.bglcolor)
        fcolor = None if style.bgfcolor is None else ColorUtil.get_mplot_rgba(style.bgfcolor)

        if lcolor is None:
            lcolor = Colors.Transparent
        if fcolor is None:
            fcolor = Colors.Transparent

        bbox_dict = {
            "boxstyle": "square",
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.bglstyle,
            "linewidth": style.bglwidth,
            "alpha": style.bgalpha,
        }
        if bbox_dict["linewidth"] is None:
            bbox_dict["linewidth"] = 0

        return _get_dict_value_none_keys_removed(bbox_dict)


def _get_dict_value_none_keys_removed(options: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in options.items() if value is not None}
