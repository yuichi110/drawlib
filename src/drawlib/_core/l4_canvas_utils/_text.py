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

from drawlib._core.l2_models import StaticContainer
from drawlib._core.l3_external import download_if_not_exist
from drawlib._core.l3_fonts import (
    FontBase,
    FontFile,
    get_font_metadata,
)
from drawlib._core.l3_styles import (
    Colors,
    Style,
)
from drawlib._core.l4_canvas_utils._colors import ColorUtil
from drawlib._core.l4_canvas_utils._utils import get_dict_value_none_keys_removed


class TextUtil(StaticContainer):
    """A utility class for handling text styles and options."""

    @staticmethod
    def validate_text_style(style: Style) -> None:
        """Validate that the required text properties are set in Style.

        Args:
            style: The Style instance to validate.

        Raises:
            ValueError: If any required text property is None.
        """
        missing: list[str] = []
        if style.text_color is None:
            missing.append("text_color")
        if style.text_size is None:
            missing.append("text_size")
        if style.text_font is None:
            missing.append("text_font")

        if missing:
            raise ValueError(
                f"Text drawing requires attributes {missing}, but they are None in the provided Style."
            )

    @staticmethod
    def format_style(style: Style) -> Style:
        """Validate and format text style.

        Args:
            style: The Style instance for text drawing.

        Returns:
            Style: Validated Style instance.

        Raises:
            TypeError: If style is not a Style instance.
            ValueError: If required core properties are missing.
        """
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')

        TextUtil.validate_text_style(style)
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

        return get_dict_value_none_keys_removed(options)

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
        file_path, download_url, md5_hash = meta.abs_path, meta.url, meta.md5
        download_if_not_exist(file_path=file_path, download_url=download_url, md5_hash=md5_hash)
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
            lcolor = Colors.Transparent
        if fcolor is None:
            fcolor = Colors.Transparent

        bbox_dict: dict[str, Any] = {
            "boxstyle": "square",
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.text_bg_line_style if style.text_bg_line_style is not None else "solid",
            "linewidth": style.text_bg_line_width if style.text_bg_line_width is not None else 1.0,
            "alpha": style.text_bg_fill_alpha,
        }

        return get_dict_value_none_keys_removed(bbox_dict)
