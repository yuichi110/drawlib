# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""MS PowerPoint (.pptx) presentation compiler for Drawlib slide decks."""

from __future__ import annotations

import os
import tempfile
from typing import Literal

from drawlib._slide.compiler import build_slide


def _resolve_pptx_dest(input_abs: str, output_file: str | None) -> str:
    """Resolve destination .pptx file path from source directory and optional output path."""
    dir_name = os.path.basename(input_abs.rstrip(os.sep))
    base_name = dir_name[:-4] if dir_name.endswith("_src") else dir_name
    if not base_name:
        base_name = "slide"

    if output_file:
        if os.path.isdir(output_file) or output_file.endswith(os.sep) or output_file.endswith("/"):
            return os.path.abspath(os.path.join(output_file, f"{base_name}.pptx"))
        return os.path.abspath(output_file)
    return os.path.join(os.path.dirname(input_abs), f"{base_name}.pptx")


def build_pptx(
    input_dir: str,
    output_file: str | None = None,
    *,
    title: str | None = None,
    theme: str | None = None,
    dpi: int = 240,
    anim_frame: Literal["first", "last"] = "last",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str:
    """Compile a Markdown slide presentation directory into a native MS PowerPoint (.pptx) deck.

    Renders all embedded ```drawlib diagrams as high-DPI static PNGs, measures exact 1920x1080
    stage layout and computed typography via Headless Chromium, and writes native editable
    16:9 PowerPoint shapes, text boxes, tables, cards, and speaker notes at 0.5x (960x540 pt) scale.

    Args:
        input_dir: Directory containing Markdown (.md) slide files and presentation assets.
        output_file: Destination .pptx file path (defaults to '<base_name>.pptx').
        title: Optional presentation title override.
        theme: CSS theme preset name ('google', 'default', 'google-dark', 'default-dark', etc.).
        dpi: Rasterization DPI for embedded drawlib diagrams. Defaults to 240.
        anim_frame: Frame ('first' or 'last') extracted from multi-frame Animation() diagrams.
        styles_path: Optional path to custom styles.py script.
        utils_path: Optional path to custom utils.py script.
        no_cache: If True, disable reading/writing the SQLite build image cache.
        timestamp: If True, include current build timestamp in OpenXML metadata.

    Returns:
        str: Absolute path to the generated .pptx file.

    Raises:
        ValueError: If input_dir is invalid, dpi <= 0, or anim_frame is invalid.
        RuntimeError: If Playwright, Chromium, or python-pptx fails.
    """
    if not input_dir:
        raise ValueError("No input directory specified for build_pptx.")
    input_abs = os.path.abspath(input_dir)
    if not os.path.isdir(input_abs):
        raise ValueError(f"Input directory does not exist: '{input_dir}'")
    if dpi <= 0:
        raise ValueError(f"dpi must be a positive integer, got {dpi}.")
    if anim_frame not in {"first", "last"}:
        raise ValueError(f"anim_frame must be 'first' or 'last', got '{anim_frame}'.")

    from drawlib._slide._pptx_dom import extract_deck_dom  # noqa: PLC0415
    from drawlib._slide._pptx_writer import write_deck_to_pptx  # noqa: PLC0415

    dest_abs = _resolve_pptx_dest(input_abs, output_file)
    dest_parent = os.path.dirname(dest_abs)
    if dest_parent:
        os.makedirs(dest_parent, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_root:
        html_out_dir = os.path.join(tmp_root, "html_stage")
        scratch_dir = os.path.join(tmp_root, "pptx_scratch")
        os.makedirs(scratch_dir, exist_ok=True)

        index_html = build_slide(
            input_dir=input_abs,
            output_dir=html_out_dir,
            title=title,
            theme=theme,
            image_format="png",
            dpi=dpi,
            force_image_format=True,
            static_anim_frame=anim_frame,
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
        )
        deck_spec = extract_deck_dom(index_html, svg_capture_dir=scratch_dir)
        return write_deck_to_pptx(
            deck=deck_spec,
            output_path=dest_abs,
            scratch_dir=scratch_dir,
            title=title,
            anim_frame=anim_frame,
            timestamp=timestamp,
        )
