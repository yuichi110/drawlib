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
from typing import Final

from drawlib._builder.doc_builder.parser_md import parse_markdown_to_html
from drawlib._builder.doc_builder.processor.options import tokenize_kv_pairs

PATTERN_CONTAINER_BOX: Final[re.Pattern[str]] = re.compile(
    r"(?:\n|^)[ \t]*:::+[ \t]*block(?:\s+([^\n]*))?\n(.*?)\n[ \t]*:::+",
    re.DOTALL,
)

PATTERN_SLIDE_NOTE: Final[re.Pattern[str]] = re.compile(
    r"(?:\n|^)[ \t]*:::+[ \t]*note(?:[ \t]+[^\n]*)?\n(.*?)\n[ \t]*:::+",
    re.DOTALL | re.IGNORECASE,
)


def extract_slide_notes(text: str) -> tuple[str, str]:
    r"""Extract ::: note blocks from slide Markdown and render them to HTML.

    Multiple note blocks in the same slide are joined with a blank line ('\n\n')
    before converting Markdown to HTML.

    Args:
        text: Raw slide Markdown text.

    Returns:
        tuple[str, str]: (cleaned_markdown_without_notes, rendered_notes_html).
    """
    note_chunks: list[str] = []

    def replacer(match: re.Match[str]) -> str:
        chunk = match.group(1).strip()
        if chunk:
            note_chunks.append(chunk)
        return "\n"

    normalized = "\n" + text if not text.startswith("\n") else text
    cleaned_md = PATTERN_SLIDE_NOTE.sub(replacer, normalized).strip()
    if not note_chunks:
        return cleaned_md, ""

    combined_notes_md = "\n\n".join(note_chunks)
    rendered_notes_html = parse_markdown_to_html(combined_notes_md).strip()
    return cleaned_md, rendered_notes_html


def build_box_styles(
    x: float | None,
    y: float | None,
    w: float | None,
    h: float | None,
    font_size: str | None,
    align: str | None,
    z_index: int | None,
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


def _parse_xy_tuple(val_clean: str) -> tuple[float, float] | None:
    """Parse an '(x, y)' string into a float pair."""
    try:
        coords = [float(p.strip()) for p in val_clean.strip("()[]").split(",")]
        if len(coords) == 2:
            return coords[0], coords[1]
    except ValueError:
        pass
    return None


def _parse_px_float(val_clean: str) -> float | None:
    """Parse a numeric or '<num>px' string into a float."""
    try:
        num_str = val_clean[:-2].strip() if val_clean.lower().endswith("px") else val_clean
        return float(num_str)
    except ValueError:
        return None


def _parse_bool_flag(val_clean: str, current: bool) -> bool:
    """Parse a boolean option string ('true'/'false')."""
    val_cp = val_clean.lower()
    if val_cp in {"true", "1", "yes", "on"}:
        return True
    if val_cp in {"false", "0", "no", "off"}:
        return False
    return current


def _parse_int_opt(val_clean: str) -> int | None:
    """Parse an integer option string safely."""
    try:
        return int(val_clean)
    except ValueError:
        return None


def parse_box_options(
    header_opts: str,
) -> tuple[
    float | None,
    float | None,
    float | None,
    float | None,
    str | None,
    bool,
    str | None,
    int | None,
    list[str],
    list[str],
]:
    """Parse key=value options for a ::: block container.

    Args:
        header_opts: Raw header options string from ::: block.

    Returns:
        tuple: (x, y, w, h, font_size, compact, align, z_index, extra_classes, custom_styles).
    """
    kv = dict(tokenize_kv_pairs(header_opts))
    xy_pair = _parse_xy_tuple(kv["xy"]) if "xy" in kv else None
    x, y = xy_pair if xy_pair is not None else (None, None)
    w = _parse_px_float(kv["width"]) if "width" in kv else None
    h = _parse_px_float(kv["height"]) if "height" in kv else None
    font_size = kv.get("font_size") or None
    compact = _parse_bool_flag(kv["compact"], False) if "compact" in kv else False
    align_val = kv.get("align", "").lower()
    align = align_val if align_val in {"left", "center", "right"} else None
    z_index = _parse_int_opt(kv["z_index"]) if "z_index" in kv else None

    extra_class: list[str] = []
    custom_styles: list[str] = []
    for key_lower, val_clean in tokenize_kv_pairs(header_opts):
        if key_lower in {"class", "css_class"}:
            extra_class.extend(val_clean.split())
        elif key_lower == "style" and val_clean:
            custom_styles.append(val_clean)

    return x, y, w, h, font_size, compact, align, z_index, extra_class, custom_styles


def process_container_blocks(text: str) -> str:
    """Parse and convert ::: block ... ::: container syntax to positioned text box <div> elements.

    Args:
        text: Markdown text with potential ::: block containers.

    Returns:
        str: Transformed text with HTML container markup.
    """

    def replacer(match: re.Match[str]) -> str:
        header_opts = (match.group(1) or "").strip()
        content = match.group(2).strip()

        x, y, w, h, font_size, compact, align, z_index, extra_class, custom_styles = parse_box_options(header_opts)
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
