# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Text utility module for canvas operations."""

from typing import Any

from matplotlib.font_manager import FontProperties

from drawlib._core.l3_colors import (
    BaseColors,
    ColorUtil,
)
from drawlib._core.l3_external import download_if_not_exist
from drawlib._core.l3_fonts import (
    FontBase,
    FontFile,
    get_font_metadata,
)
from drawlib._core.l3_styles import (
    Style,
)


class TextUtil:
    """A utility class for handling text styles and options."""

    def __init__(self) -> None:
        """Raise TypeError to prevent instantiation of utility class."""
        raise TypeError(f"'{self.__class__.__name__}' is a static utility class and cannot be instantiated.")

    @staticmethod
    def validate_text_style(style: Style) -> None:
        """Validate that the Style supports text drawing."""
        style.validate_for("text")

    @staticmethod
    def format_style(style: Style) -> Style:
        """Validate and return text style."""
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')
        style.validate_for("text")
        return style

    @staticmethod
    def get_text_options(
        style: Style | None,
    ) -> dict[str, Any]:
        """Extract text options from Style."""
        if style is None or style.text_color is None:
            return {}

        color = ColorUtil.get_mplot_rgba(style.text_color)
        options: dict[str, Any] = {
            "color": color,
            "horizontalalignment": style.text_halign if style.text_halign is not None else "center",
            "verticalalignment": style.text_valign if style.text_valign is not None else "center",
        }

        return {k: v for k, v in options.items() if v is not None}

    @staticmethod
    def get_font_properties(
        style: Style,
    ) -> FontProperties:
        """Get matplotlib FontProperties from Style."""
        if not isinstance(style, Style):
            raise TypeError(f"style must be Style, but {type(style)} given")

        if style.text_font is None or style.text_size is None:
            raise ValueError("text_font and text_size must be set in Style.")

        if isinstance(style.text_font, FontFile):
            return FontProperties(size=style.text_size, fname=style.text_font.file)

        font_target = style.text_font
        if not isinstance(font_target, FontBase):
            raise ValueError(f"font {font_target} must be FontBase")

        meta = get_font_metadata(font_target)
        file_path, md5_hash = meta.abs_path, meta.md5
        download_if_not_exist(file_path=file_path, md5_hash=md5_hash)
        return FontProperties(size=style.text_size, fname=file_path)

    @staticmethod
    def get_bbox_dict(
        style: Style | None = None,
    ) -> dict[str, Any] | None:
        """Convert drawlib's Style to matplotlib's text background options."""
        if style is None:
            return None

        all_none = True
        for e in [style.text_bg_fill_color, style.text_bg_line_color, style.text_bg_line_style]:
            if e is not None:
                all_none = False
        if all_none:
            return None

        lcolor = None if style.text_bg_line_color is None else ColorUtil.get_mplot_rgba(style.text_bg_line_color)
        fcolor = None if style.text_bg_fill_color is None else ColorUtil.get_mplot_rgba(style.text_bg_fill_color)

        if lcolor is None:
            lcolor = BaseColors.Transparent
        if fcolor is None:
            fcolor = BaseColors.Transparent

        bbox_dict: dict[str, Any] = {
            "boxstyle": "square",
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.text_bg_line_style if style.text_bg_line_style is not None else "solid",
            "linewidth": style.text_bg_line_width if style.text_bg_line_width is not None else 1.0,
            "alpha": style.text_bg_fill_alpha,
        }

        return {k: v for k, v in bbox_dict.items() if v is not None}
