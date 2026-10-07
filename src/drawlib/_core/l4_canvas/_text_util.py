# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Text utility module for canvas operations."""

import contextlib
import functools
import hashlib
import os
import re
from typing import Any, NamedTuple

from matplotlib import ft2font
from matplotlib.font_manager import FontProperties

from drawlib._core.l1_core import FONT_DIR_PATH, FONT_ICON_DIR_PATH
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


class SvgFontInfo(NamedTuple):
    """Resolved SVG font family and bundling metadata for a font file."""

    unique_family: str
    ttf_family: str
    rel_bundle_path: str
    src_spec: str
    font_format: str


@functools.lru_cache(maxsize=256)
def _resolve_svg_font_info_cached(norm_abs: str, file_exists: bool) -> SvgFontInfo:
    """Internal cached resolver for SVG font metadata."""
    font_dir_abs = os.path.abspath(FONT_DIR_PATH)
    icon_dir_abs = os.path.abspath(FONT_ICON_DIR_PATH)

    if norm_abs.startswith(font_dir_abs + os.sep):
        rel_sub = os.path.relpath(norm_abs, font_dir_abs).replace("\\", "/")
        stem = os.path.splitext(rel_sub)[0]
        slug = re.sub(r"[^a-zA-Z0-9-]+", "-", stem).strip("-").lower()
        unique_family = f"drawlib-{slug}"
        rel_bundle_path = f"_assets/fonts/{rel_sub}"
        src_spec = f"builtin:fonts/{rel_sub}"
    elif norm_abs.startswith(icon_dir_abs + os.sep):
        rel_sub = os.path.relpath(norm_abs, icon_dir_abs).replace("\\", "/")
        stem = os.path.splitext(rel_sub)[0]
        slug = re.sub(r"[^a-zA-Z0-9-]+", "-", stem).strip("-").lower()
        unique_family = f"drawlib-{slug}"
        rel_bundle_path = f"_assets/fonts/{rel_sub}"
        src_spec = f"builtin:fonticons/{rel_sub}"
    else:
        h = hashlib.md5()  # noqa: S324
        if file_exists:
            with open(norm_abs, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
        else:
            h.update(norm_abs.encode("utf-8"))
        hash8 = h.hexdigest()[:8]
        base_name = os.path.basename(norm_abs)
        stem_clean = re.sub(r"[^a-zA-Z0-9-]+", "-", os.path.splitext(base_name)[0]).strip("-").lower() or "font"
        unique_family = f"drawlib-custom-{stem_clean}-{hash8}"
        rel_bundle_path = f"_assets/fonts/custom/{hash8}_{base_name}"
        src_spec = norm_abs

    ttf_family = ""
    if file_exists:
        with contextlib.suppress(Exception):
            ttf_family = str(ft2font.FT2Font(norm_abs).family_name or "").strip()

    ext = os.path.splitext(norm_abs)[1].lower()
    if ext == ".otf":
        font_format = "opentype"
    elif ext == ".woff2":
        font_format = "woff2"
    elif ext == ".woff":
        font_format = "woff"
    else:
        font_format = "truetype"

    return SvgFontInfo(
        unique_family=unique_family,
        ttf_family=ttf_family,
        rel_bundle_path=rel_bundle_path,
        src_spec=src_spec,
        font_format=font_format,
    )


def resolve_svg_font_info(abs_path: str) -> SvgFontInfo:
    """Resolve collision-free SVG font-family alias and bundle path metadata for a font file.

    Args:
        abs_path: Path to the font file (.ttf, .otf, .woff, .woff2).

    Returns:
        SvgFontInfo: Resolved metadata for SVG text styling and @font-face bundling.
    """
    norm_abs = os.path.abspath(abs_path)
    return _resolve_svg_font_info_cached(norm_abs, os.path.isfile(norm_abs))


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
            "linespacing": style.text_line_spacing,
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
            file_path = style.text_font.file
            info = resolve_svg_font_info(file_path)
            families = [info.unique_family]
            if info.ttf_family and info.ttf_family != info.unique_family:
                families.append(info.ttf_family)
            return FontProperties(family=families, size=style.text_size, fname=file_path)

        font_target = style.text_font
        if not isinstance(font_target, FontBase):
            raise ValueError(f"font {font_target} must be FontBase")

        meta = get_font_metadata(font_target)
        file_path, md5_hash = meta.abs_path, meta.md5
        download_if_not_exist(file_path=file_path, md5_hash=md5_hash)
        info = resolve_svg_font_info(file_path)
        families = [info.unique_family]
        if info.ttf_family and info.ttf_family != info.unique_family:
            families.append(info.ttf_family)
        return FontProperties(family=families, size=style.text_size, fname=file_path)

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
