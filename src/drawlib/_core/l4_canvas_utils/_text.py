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

from drawlib._core.l2_models import StaticContainer
from drawlib._core.l3_external import download_if_not_exist
from drawlib._core.l3_fonts import (
    FontBase,
    FontFile,
    get_font_metadata,
)
from drawlib._core.l3_styles import (
    SYSTEM_DEFAULT_SHAPE_TEXT_STYLE,
    SYSTEM_DEFAULT_TEXT_STYLE,
    Colors,
    Style,
)
from drawlib._core.l4_canvas_utils._colors import ColorUtil
from drawlib._core.l4_canvas_utils._utils import get_dict_value_none_keys_removed
from drawlib._preset_styles import get_style


class TextUtil(StaticContainer):
    """A utility class for handling text styles and options."""

    @staticmethod
    def format_style(style: Style | str | None) -> Style:
        if style is None or isinstance(style, (Style, str)):
            formatted_style = get_style(style).copy()
        else:
            raise ValueError(f'Arg "style" must be Style or None, but {type(style)} given.')

        system_default = SYSTEM_DEFAULT_TEXT_STYLE.copy()
        system_default.text_bg_fill_alpha = None
        system_default.text_bg_line_color = None
        system_default.text_bg_line_style = None
        system_default.text_bg_line_width = None
        system_default.text_bg_fill_color = None
        formatted_style = system_default.merge(formatted_style)
        return formatted_style

    @staticmethod
    def get_text_options(
        style: Style | None,
    ) -> dict[str, Any]:
        if style is None:
            return {}

        color_val = style.text_color if style.text_color is not None else style.get_fill_color()
        color = None if color_val is None else ColorUtil.get_mplot_rgba(color_val)

        options: dict[str, Any] = {
            "color": color,
            "horizontalalignment": style.text_halign,
            "verticalalignment": style.text_valign,
        }

        return get_dict_value_none_keys_removed(options)

    @staticmethod
    def get_font_properties(
        style: Style,
    ) -> FontProperties | None:
        if not isinstance(style, Style):
            raise ValueError(f"style must be Style, but {type(style)} given")
        default = get_style(None)

        if isinstance(style.text_font, FontFile):
            size = (
                style.text_size
                if style.text_size is not None
                else (default.text_size if default.text_size is not None else 16)
            )
            return FontProperties(size=size, fname=style.text_font.file)

        default_font = default.text_font if default.text_font is not None else SYSTEM_DEFAULT_TEXT_STYLE.text_font
        font_target = style.text_font if style.text_font is not None else default_font
        size_target = (
            style.text_size
            if style.text_size is not None
            else (default.text_size if default.text_size is not None else 16)
        )

        if not isinstance(font_target, FontBase):
            raise ValueError(f"font {font_target} must be FontBase")

        meta = get_font_metadata(font_target)
        file_path, download_url, md5_hash = meta.abs_path, meta.url, meta.md5
        download_if_not_exist(file_path=file_path, download_url=download_url, md5_hash=md5_hash)
        return FontProperties(size=size_target, fname=file_path)

    @staticmethod
    def get_bbox_dict(
        style: Style | None = None,
    ) -> dict[str, Any] | None:
        """Convert drawlib's Style to matplotlib's text background options.

        Args:
            style (Style | None):
                The Style object containing text background style properties.

        Returns:
            dict[str, Any] | None: Dictionary of options suitable for matplotlib's text background.

        Notes:
            - Returns None if style is None or if all background properties are None.
            - Converts bgfcolor, bglcolor, bglstyle, bglwidth, and bgalpha properties
              from Style to matplotlib compatible bbox options.
        """
        # {} doesn't mean no style.
        # requires returning None when no style.

        if style is None:
            return None

        all_none = True
        for e in [style.text_bg_fill_color, style.text_bg_line_color, style.text_bg_line_style]:
            if e is not None:
                all_none = False
        if all_none:
            return None

        # background exist

        lcolor = None if style.text_bg_line_color is None else ColorUtil.get_mplot_rgba(style.text_bg_line_color)
        fcolor = None if style.text_bg_fill_color is None else ColorUtil.get_mplot_rgba(style.text_bg_fill_color)

        if lcolor is None:
            lcolor = Colors.Transparent
        if fcolor is None:
            fcolor = Colors.Transparent

        bbox_dict: dict[str, Any] = {
            "boxstyle": "square",
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.text_bg_line_style,
            "linewidth": style.text_bg_line_width,
            "alpha": style.text_bg_fill_alpha,
        }
        if bbox_dict["linewidth"] is None:
            bbox_dict["linewidth"] = 0

        return get_dict_value_none_keys_removed(bbox_dict)
