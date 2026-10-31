# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Option models and path resolution for drawlib code blocks."""

from __future__ import annotations

import os
import re
import shlex
from typing import Literal

from pydantic import BaseModel

_QUOTE_OR_PAREN_RE = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|(\([^()]*\))')
_VALID_KEY_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def _collapse_unquoted_parens(match: re.Match[str]) -> str:
    """Remove whitespace inside unquoted parentheses so shlex treats tuples as single tokens."""
    if match.group(1) is not None:
        return re.sub(r"\s+", "", match.group(1))
    return match.group(0)


def tokenize_kv_pairs(info_str: str) -> list[tuple[str, str]]:
    """Parse space-separated key=value tokens while preserving whitespace in quotes and tuples.

    Args:
        info_str (str): Raw header option string.

    Returns:
        list[tuple[str, str]]: List of (key_lower, cleaned_value) pairs.
    """
    info = info_str.strip()
    if not info:
        return []

    normalized = _QUOTE_OR_PAREN_RE.sub(_collapse_unquoted_parens, info)
    try:
        tokens = shlex.split(normalized, posix=True)
    except ValueError:
        tokens = normalized.split()

    pairs: list[tuple[str, str]] = []
    for token in tokens:
        if "=" not in token:
            continue
        key, val = token.split("=", 1)
        key_clean = key.strip()
        if not _VALID_KEY_RE.match(key_clean):
            continue
        val_clean = val.strip().strip('"').strip("'")
        pairs.append((key_clean.lower(), val_clean))
    return pairs


class DrawlibBlockOptions(BaseModel):
    """Parsed options from ```drawlib header line or <script type='text/drawlib'> attributes."""

    width: str | None = None
    height: str | None = None
    align: str | None = None
    format: str | None = None
    caption: str | None = None
    css_class: str | None = None
    file: str | None = None
    code: Literal["hide", "show", "fold"] = "hide"
    no_cache: bool = False
    anim_trigger: Literal["auto", "click"] | None = None
    anim_loop: Literal["once", "infinite"] | None = None
    anim_pause: list[int] | None = None


class ExtractedBlockInfo(BaseModel):
    """Extracted code block information for show and export subcommands."""

    index: int
    code: str
    info_str: str
    options: DrawlibBlockOptions
    file_name: str
    line_number: int


def parse_block_info(info_str: str) -> DrawlibBlockOptions:
    """Parse space-separated key=value options from header line or tag attributes.

    Args:
        info_str (str): Info string following ```drawlib or <script type='text/drawlib'> attributes.

    Returns:
        DrawlibBlockOptions: Parsed options object.
    """
    options = DrawlibBlockOptions()
    for key_lower, val_clean in tokenize_kv_pairs(info_str):
        if key_lower == "type":
            continue
        elif key_lower == "code":
            val_code = val_clean.lower()
            if val_code == "show":
                options.code = "show"
            elif val_code == "fold":
                options.code = "fold"
            elif val_code == "hide":
                options.code = "hide"
        elif key_lower == "width":
            if val_clean:
                options.width = val_clean if (val_clean.endswith("px") or val_clean.endswith("%")) else f"{val_clean}px"
        elif key_lower == "height":
            if val_clean:
                options.height = (
                    val_clean if (val_clean.endswith("px") or val_clean.endswith("%")) else f"{val_clean}px"
                )
        elif key_lower == "align":
            if val_clean.lower() in {"left", "center", "right"}:
                options.align = val_clean.lower()
        elif key_lower == "format":
            fmt = val_clean.lower()
            if fmt in {"png", "webp", "svg", "apng"}:
                options.format = fmt
        elif key_lower == "caption":
            options.caption = val_clean
        elif key_lower in {"class", "css_class"}:
            options.css_class = val_clean
        elif key_lower == "file":
            options.file = val_clean
        elif key_lower == "no_cache":
            val_nc = val_clean.lower()
            if val_nc in {"true", "1", "yes", "on"}:
                options.no_cache = True
            elif val_nc in {"false", "0", "no", "off"}:
                options.no_cache = False
        elif key_lower == "anim_trigger":
            val_trig = val_clean.lower()
            if val_trig == "click":
                options.anim_trigger = "click"
            elif val_trig == "auto":
                options.anim_trigger = "auto"
        elif key_lower == "anim_loop":
            val_loop = val_clean.lower()
            if val_loop == "once":
                options.anim_loop = "once"
            elif val_loop == "infinite":
                options.anim_loop = "infinite"
        elif key_lower == "anim_pause":
            pauses: list[int] = []
            for part in val_clean.strip("()[]").split(","):
                part_s = part.strip()
                if not part_s:
                    continue
                try:
                    p_val = int(part_s)
                    if p_val > 0:
                        pauses.append(p_val)
                except ValueError:
                    pass
            if pauses:
                options.anim_pause = sorted(set(pauses))

    return options


def resolve_block_image_paths(
    options: DrawlibBlockOptions,
    doc_base_name: str,
    block_counter: int,
    default_format: str,
    output_dir: str | None,
    require_file: bool = False,
    line_number: int = 1,
    shared_images_dir: str | None = None,
) -> tuple[str, str]:
    """Resolve relative image reference path and target filesystem path for a drawlib block.

    Args:
        options (DrawlibBlockOptions): Parsed block options.
        doc_base_name (str): Base filename of the document (without extension).
        block_counter (int): 1-based block index.
        default_format (str): Default image format ('png' or 'webp' or 'svg').
        output_dir (Optional[str]): Target output directory for generated assets.
        require_file (bool): Whether to enforce that options.file is provided.
        line_number (int): Line number of the code block for error reporting.
        shared_images_dir (Optional[str]): Optional shared target directory for multi-locale sites.

    Returns:
        tuple[str, str]: (rel_img_path for HTML/Markdown src, target_img_path on disk).

    Raises:
        ValueError: If require_file is True and options.file is missing.
    """
    eff_format = options.format if options.format in {"png", "webp", "svg", "apng"} else default_format
    ext = eff_format if eff_format in {"svg", "webp", "apng"} else "png"

    if options.file:
        raw_file = options.file.strip()
        _, file_ext = os.path.splitext(raw_file)
        if file_ext.lower() in {".png", ".webp", ".svg", ".apng"}:
            img_name = raw_file
        else:
            img_name = f"{raw_file}.{ext}"

        if "/" in img_name or (os.sep in img_name):
            rel_img_path = img_name
        else:
            rel_img_path = f"{doc_base_name}_images/{img_name}"
    else:
        if require_file:
            raise ValueError(
                f"Missing required 'file=<filename.ext>' option in drawlib code block at line {line_number}. "
                "Example: ```drawlib file=my_diagram.png"
            )
        img_name = f"{block_counter}.{ext}"
        rel_img_path = f"{doc_base_name}_images/{img_name}"

    if shared_images_dir is not None:
        target_img_path = os.path.abspath(os.path.join(shared_images_dir, img_name))
        if output_dir:
            rel_img_path = os.path.relpath(target_img_path, os.path.abspath(output_dir)).replace(os.sep, "/")
        else:
            rel_img_path = os.path.join(shared_images_dir, img_name).replace(os.sep, "/")
        return rel_img_path, target_img_path

    if output_dir:
        target_img_path = os.path.join(output_dir, rel_img_path)
    else:
        target_img_path = rel_img_path

    return rel_img_path, target_img_path
