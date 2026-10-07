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
from typing import Literal, Optional

from pydantic import BaseModel


class DrawlibBlockOptions(BaseModel):
    """Parsed options from ```drawlib header line or <script type='text/drawlib'> attributes."""

    width: Optional[str] = None
    height: Optional[str] = None
    align: Optional[str] = None
    format: Optional[str] = None
    caption: Optional[str] = None
    css_class: Optional[str] = None
    file: Optional[str] = None
    code: Literal["hide", "show", "fold"] = "hide"
    slot: Optional[str] = None
    xy: Optional[tuple[float, float]] = None
    size: Optional[tuple[float, float]] = None
    z_index: Optional[int] = None
    no_cache: bool = False
    anim_trigger: Optional[Literal["auto", "click"]] = None
    anim_loop: Optional[Literal["once", "infinite"]] = None
    anim_pause: Optional[list[int]] = None


class ExtractedBlockInfo(BaseModel):
    """Extracted code block information for show and export subcommands."""

    index: int
    code: str
    info_str: str
    options: DrawlibBlockOptions
    file_name: str
    line_number: int


def parse_block_info(info_str: str) -> DrawlibBlockOptions:
    """Parse space-separated key:value / key=value and shorthand options from header line or tag attributes.

    Args:
        info_str (str): Info string following ```drawlib or <script type='text/drawlib'> attributes.

    Returns:
        DrawlibBlockOptions: Parsed options object.
    """
    options = DrawlibBlockOptions()
    info = info_str.strip()
    if not info:
        return options

    # 1. Pre-process explicit xy: (...) / pos: (...) and size: (...) / dim: (...) and anim-pause
    xy_m = re.search(r"(?:xy|pos|position):\s*\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)", info, re.I)
    if xy_m:
        options.xy = (float(xy_m.group(1)), float(xy_m.group(2)))
        info = info[: xy_m.start()] + " " + info[xy_m.end() :]

    size_m = re.search(r"(?:size|dim|dimensions):\s*\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)", info, re.I)
    if size_m:
        options.size = (float(size_m.group(1)), float(size_m.group(2)))
        info = info[: size_m.start()] + " " + info[size_m.end() :]

    pause_m = re.search(
        r"(?:anim[-_])?pause[=:]\s*[\(\[]?\s*([0-9]+(?:\s*,\s*[0-9]+)*)\s*[\)\]]?",
        info,
        re.I,
    )
    if pause_m:
        raw_pauses = [
            int(p.strip())
            for p in pause_m.group(1).split(",")
            if p.strip().isdigit() and int(p.strip()) > 0
        ]
        if raw_pauses:
            options.anim_pause = sorted(set(raw_pauses))
        info = info[: pause_m.start()] + " " + info[pause_m.end() :]

    # 2. Pre-process standalone tuple shorthands: (x, y) and (w, h)
    tuple_pattern = r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)"
    tuple_matches = list(re.finditer(tuple_pattern, info))
    if tuple_matches:
        if options.xy is None and len(tuple_matches) >= 1:
            options.xy = (float(tuple_matches[0].group(1)), float(tuple_matches[0].group(2)))
        if options.size is None and len(tuple_matches) >= 2:
            options.size = (float(tuple_matches[1].group(1)), float(tuple_matches[1].group(2)))
        info = re.sub(tuple_pattern, " ", info)

    try:
        tokens = shlex.split(info, posix=True)
    except ValueError:
        tokens = info.split()

    for token in tokens:
        if ":" in token:
            key, val = token.split(":", 1)
        elif "=" in token:
            key, val = token.split("=", 1)
        else:
            key, val = "", token

        key_lower = key.strip().lower()
        val_clean = val.strip().strip('"').strip("'")

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
        elif key_lower in {"width", "w"}:
            options.width = (
                val_clean if (val_clean.endswith("px") or val_clean.endswith("%")) else f"{val_clean}px"
            )
        elif key_lower in {"height", "h"}:
            options.height = (
                val_clean if (val_clean.endswith("px") or val_clean.endswith("%")) else f"{val_clean}px"
            )
        elif key_lower in {"align", "a"}:
            if val_clean.lower() in {"left", "center", "right"}:
                options.align = val_clean.lower()
        elif key_lower in {"format", "fmt"}:
            fmt = val_clean.lower()
            if fmt in {"png", "webp", "svg", "apng"}:
                options.format = fmt
        elif key_lower in {"slot", "s"}:
            options.slot = val_clean.lower()
        elif key_lower in {"xy", "pos", "position"}:
            try:
                coords = [float(p.strip()) for p in val_clean.strip("()[]").split(",")]
                if len(coords) == 2:
                    options.xy = (coords[0], coords[1])
            except ValueError:
                pass
        elif key_lower in {"size", "dim", "dimensions"}:
            try:
                dims = [float(p.strip()) for p in val_clean.strip("()[]").split(",")]
                if len(dims) == 2:
                    options.size = (dims[0], dims[1])
            except ValueError:
                pass
        elif key_lower == "caption":
            options.caption = val_clean
        elif key_lower in {"class", "css_class"}:
            options.css_class = val_clean
        elif key_lower == "file":
            options.file = val_clean
        elif key_lower in {"cache", "caching"}:
            options.no_cache = val_clean.lower() in {"false", "0", "no", "off"}
        elif key_lower in {"no-cache", "no_cache", "nocache"}:
            options.no_cache = val_clean.lower() not in {"false", "0", "no", "off"}
        elif key_lower in {"z", "z_index", "z-index"}:
            try:
                options.z_index = int(val_clean)
            except ValueError:
                pass
        elif key_lower in {"anim-trigger", "anim_trigger", "anim"}:
            val_trig = val_clean.lower()
            if val_trig in {"click", "manual"}:
                options.anim_trigger = "click"
            elif val_trig == "auto":
                options.anim_trigger = "auto"
        elif key_lower in {"anim-loop", "anim_loop", "loop"}:
            val_loop = val_clean.lower()
            if val_loop in {"once", "1", "false", "no"}:
                options.anim_loop = "once"
            elif val_loop in {"infinite", "loop", "0", "true", "yes"}:
                options.anim_loop = "infinite"
        elif key_lower in {"anim-pause", "anim_pause", "pause"}:
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
        elif not key_lower:
            val_lower = val_clean.lower()
            if val_lower in {"no-cache", "no_cache", "nocache"}:
                options.no_cache = True
            elif val_lower in {"show-code", "show_code"}:
                options.code = "show"
            elif val_lower in {"fold-code", "fold_code"}:
                options.code = "fold"
            elif val_lower in {"hide-code", "hide_code"}:
                options.code = "hide"
            elif val_lower in {"left", "center", "right"}:
                options.align = val_lower
            elif val_lower in {"png", "webp", "svg", "apng"}:
                options.format = val_lower
            elif val_lower.startswith("slot:"):
                options.slot = val_lower[5:].strip()
            elif re.match(r"^\d+(px|%)$", val_lower) or val_lower.isdigit():
                has_unit = val_lower.endswith("px") or val_lower.endswith("%")
                options.width = val_clean if has_unit else f"{val_clean}px"

    return options


def resolve_block_image_paths(
    options: DrawlibBlockOptions,
    doc_base_name: str,
    block_counter: int,
    default_format: str,
    output_dir: Optional[str],
    require_file: bool = False,
    line_number: int = 1,
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
                f"Missing required 'file:<filename.ext>' option in drawlib code block at line {line_number}. "
                "Example: ```drawlib file:my_diagram.png"
            )
        img_name = f"{block_counter}.{ext}"
        rel_img_path = f"{doc_base_name}_images/{img_name}"

    if output_dir:
        target_img_path = os.path.join(output_dir, rel_img_path)
    else:
        target_img_path = rel_img_path

    return rel_img_path, target_img_path
