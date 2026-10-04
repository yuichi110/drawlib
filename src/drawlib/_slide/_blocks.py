# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Container block parser and HTML transformer for slide stage layouts."""

from __future__ import annotations

import re
import shlex
from typing import Final, Optional

from drawlib._builder.doc_builder.parser_md import parse_markdown_to_html

PATTERN_CONTAINER_BOX: Final[re.Pattern[str]] = re.compile(
    r"(?:\n|^)[ \t]*:::+[ \t]*(?:block|box)(?:\s+([^\n]*))?\n(.*?)\n[ \t]*:::+",
    re.DOTALL,
)


def parse_box_coordinates(
    header_opts: str,
) -> tuple[Optional[float], Optional[float], Optional[float], Optional[float], str]:
    """Extract (x, y) and (w, h) bounding box coordinates from container options.

    Args:
        header_opts: Raw header options string from ::: box.

    Returns:
        tuple[Optional[float], Optional[float], Optional[float], Optional[float], str]:
            (x, y, w, h, remaining_options_string).
    """
    x: Optional[float] = None
    y: Optional[float] = None
    w: Optional[float] = None
    h: Optional[float] = None

    tuple_pattern = r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)"
    tuple_matches = list(re.finditer(tuple_pattern, header_opts))
    if len(tuple_matches) >= 1:
        x = float(tuple_matches[0].group(1))
        y = float(tuple_matches[0].group(2))
    if len(tuple_matches) >= 2:
        w = float(tuple_matches[1].group(1))
        h = float(tuple_matches[1].group(2))

    cleaned_opts = re.sub(tuple_pattern, " ", header_opts).strip()
    return x, y, w, h, cleaned_opts


def build_box_styles(
    x: Optional[float],
    y: Optional[float],
    w: Optional[float],
    h: Optional[float],
    font_size: Optional[str],
    align: Optional[str],
    z_index: Optional[int],
    custom_styles: list[str],
) -> list[str]:
    """Construct inline CSS style declarations for a positioned text box.

    Args:
        x: Left coordinate in pixels.
        y: Top coordinate in pixels.
        w: Width in pixels.
        h: Height in pixels.
        font_size: Optional font size override.
        align: Optional text alignment.
        z_index: Optional z-index layer.
        custom_styles: Additional inline CSS rules.

    Returns:
        list[str]: CSS style statements.
    """
    styles: list[str] = []
    actual_x = x if x is not None else 80.0
    actual_y = y if y is not None else 140.0
    actual_w = w if w is not None else 1760.0
    actual_h = h if h is not None else 840.0
    styles.append("position: absolute;")
    styles.append(f"left: {actual_x}px; top: {actual_y}px;")
    styles.append(f"width: {actual_w}px; height: {actual_h}px;")
    if font_size:
        fs = font_size if any(font_size.endswith(u) for u in ("px", "rem", "em", "%", "pt")) else f"{font_size}px"
        styles.append(f"font-size: {fs};")
    if align:
        styles.append(f"text-align: {align};")
    if z_index is not None:
        styles.append(f"z-index: {z_index};")
    for cs in custom_styles:
        clean = cs.strip().rstrip(";")
        if clean:
            styles.append(f"{clean};")
    return styles


def handle_keyed_box_token(
    k: str,
    v: str,
    extra_class: list[str],
    custom_styles: list[str],
) -> tuple[Optional[str], Optional[int], Optional[str]]:
    """Handle a key:value token for box options."""
    k_lower = k.lower()
    if k_lower in {"font", "font-size", "fontsize", "fs"}:
        return v, None, None
    elif k_lower in {"z", "z_index", "z-index"}:
        try:
            return None, int(v), None
        except ValueError:
            return None, None, None
    elif k_lower in {"align", "text-align"}:
        return None, None, v.lower()
    elif k_lower in {"class", "css_class"}:
        extra_class.extend(v.split())
    elif k_lower in {"style", "css"}:
        custom_styles.append(v)
    return None, None, None


def handle_pos_box_token(arg: str) -> tuple[Optional[str], bool, Optional[str]]:
    """Handle standalone keyword argument without key prefix."""
    kw_lower = arg.lower()
    if kw_lower == "compact":
        return None, True, None
    elif kw_lower in {"center", "left", "right"}:
        return None, False, kw_lower
    elif re.match(r"^\d+(px|rem|em|%)$", kw_lower):
        return arg, False, None
    return None, False, None


def parse_box_tokens(
    cleaned_opts: str,
) -> tuple[Optional[str], bool, Optional[str], Optional[int], list[str], list[str]]:
    """Parse key:value tokens for a ::: box container.

    Args:
        cleaned_opts: Options string stripped of coordinate tuples.

    Returns:
        tuple: (font_size, compact, align, z_index, extra_classes, custom_styles).
    """
    font_size: Optional[str] = None
    compact: bool = False
    align: Optional[str] = None
    z_index: Optional[int] = None
    extra_class: list[str] = []
    custom_styles: list[str] = []

    try:
        tokens = shlex.split(cleaned_opts, posix=True)
    except ValueError:
        tokens = cleaned_opts.split()

    for token in tokens:
        if ":" in token or "=" in token:
            sep = ":" if ":" in token else "="
            k, v = token.split(sep, 1)
            v_clean = v.strip().strip('"').strip("'")
            fs, z, al = handle_keyed_box_token(k.strip(), v_clean, extra_class, custom_styles)
            if fs:
                font_size = fs
            if z is not None:
                z_index = z
            if al:
                align = al
        else:
            v_clean = token.strip().strip('"').strip("'")
            fs, cp, al = handle_pos_box_token(v_clean)
            if fs:
                font_size = fs
            if cp:
                compact = True
            if al:
                align = al

    return font_size, compact, align, z_index, extra_class, custom_styles


def process_container_blocks(text: str) -> str:
    """Parse and convert ::: box ... ::: container syntax to positioned text box <div> elements.

    Args:
        text: Markdown text with potential ::: box blocks.

    Returns:
        str: Transformed text with HTML container markup.
    """

    def replacer(match: re.Match[str]) -> str:
        header_opts = (match.group(1) or "").strip()
        content = match.group(2).strip()

        x, y, w, h, cleaned_opts = parse_box_coordinates(header_opts)
        font_size, compact, align, z_index, extra_class, custom_styles = parse_box_tokens(cleaned_opts)
        styles = build_box_styles(x, y, w, h, font_size, align, z_index, custom_styles)

        classes = ["slide-block", "slide-text-box"]
        if compact:
            classes.append("compact")
        classes.extend(extra_class)

        rendered_inner = parse_markdown_to_html(content)
        style_attr = f' style="{" ".join(styles)}"' if styles else ""
        class_attr = f' class="{" ".join(classes)}"'

        return f"\n<div{class_attr}{style_attr}>\n{rendered_inner}\n</div>\n"

    return PATTERN_CONTAINER_BOX.sub(replacer, text)
