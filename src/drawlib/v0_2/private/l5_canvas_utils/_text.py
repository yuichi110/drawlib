# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Text utility module for canvas operations."""

from typing import Any, Callable

from matplotlib.font_manager import FontProperties
from matplotlib.text import Text

from drawlib.v0_2.private.l2_models import StaticContainer
from drawlib.v0_2.private.l3_external import download_if_not_exist
from drawlib.v0_2.private.l3_fonts import (
    FontBase,
    FontFile,
    get_font_metadata,
)
from drawlib.v0_2.private.l3_styles import (
    SYSTEM_DEFAULT_SHAPE_TEXT_STYLE,
    SYSTEM_DEFAULT_TEXT_STYLE,
    Colors,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l5_canvas_utils._colors import ColorUtil
from drawlib.v0_2.private.l5_canvas_utils._utils import get_dict_value_none_keys_removed


class TextUtil(StaticContainer):
    """A utility class for handling text styles and options."""

    @staticmethod
    def format_style(style: TextStyle | str | None) -> TextStyle:
        """Format and retrieve TextStyle object based on input parameters.

        Args:
            style (TextStyle | str | None):
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
        style: TextStyle | ShapeTextStyle | None,
    ) -> dict[str, Any]:
        """Convert drawlib's TextStyle or ShapeTextStyle to matplotlib's text options.

        Args:
            style (TextStyle | ShapeTextStyle | None):
                The TextStyle or ShapeTextStyle object containing text style properties.

        Returns:
            dict[str, Any]: Dictionary of options suitable for matplotlib text handling.

        Notes:
            - If style is None, returns an empty dictionary.
            - Converts color, horizontalalignment, and verticalalignment properties
              from TextStyle or ShapeTextStyle to matplotlib compatible options.
        """
        if style is None:
            return {}

        # convert rgb -> matplot rgb
        color = None if style.color is None else ColorUtil.get_mplot_rgba(style.color)

        options: dict[str, Any] = {
            "color": color,
            "horizontalalignment": style.halign,
            "verticalalignment": style.valign,
        }

        return get_dict_value_none_keys_removed(options)

    @staticmethod
    def get_font_properties(  # noqa: C901
        style: TextStyle | ShapeTextStyle,
    ) -> FontProperties | None:
        """Create matplotlib's FontProperties object from TextStyle or ShapeTextStyle.

        Args:
            style (TextStyle | ShapeTextStyle | None):
                The TextStyle or ShapeTextStyle object containing font properties.

        Returns:
            FontProperties | None: FontProperties object or None if style is None.

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
        if not isinstance(default.font, FontBase):
            raise ValueError(f"default font {default.font} must be FontBase")

        meta = get_font_metadata(default.font)
        file_path, download_url, md5_hash = meta.abs_path, meta.url, meta.md5
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

            meta = get_font_metadata(style.font)
            file_path, download_url, md5_hash = meta.abs_path, meta.url, meta.md5
            download_if_not_exist(file_path=file_path, download_url=download_url, md5_hash=md5_hash)
            return FontProperties(size=style.size, fname=file_path)

        raise ValueError(f"font type {type(style.font)} is not supported")

    @staticmethod
    def get_bbox_dict(
        style: TextStyle | None = None,
    ) -> dict[str, Any] | None:
        """Convert drawlib's TextStyle to matplotlib's text background options.

        Args:
            style (TextStyle | None):
                The TextStyle object containing text background style properties.

        Returns:
            dict[str, Any] | None: Dictionary of options suitable for matplotlib's text background.

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

        bbox_dict: dict[str, Any] = {
            "boxstyle": "square",
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.bglstyle,
            "linewidth": style.bglwidth,
            "alpha": style.bgalpha,
        }
        if bbox_dict["linewidth"] is None:
            bbox_dict["linewidth"] = 0

        return get_dict_value_none_keys_removed(bbox_dict)
