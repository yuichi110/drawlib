# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Per-file CLI progress bar renderer for drawlib build commands."""

from __future__ import annotations

import os
from typing import Sequence

from drawlib._builder._common.progress import (
    BAR_WIDTH,
    FileBuildProgress,
    format_duplicate_output_error,
    format_progress_line,
)
from drawlib._builder.doc_builder.processor import extract_code_blocks, resolve_block_image_paths


def check_document_output_duplicates(
    tasks: Sequence[tuple[str, str, bool]],
    display_names: Sequence[str],
    image_format: str = "png",
    embed_images: bool = False,
) -> int:
    """Pre-check all document tasks and drawlib code blocks for duplicate output file paths.

    Args:
        tasks (Sequence[tuple[str, str, bool]]): Sequence of `(src_abs, dest_abs, is_md)` tuples.
        display_names (Sequence[str]): Corresponding display names (e.g. `/dir/file.md`).
        image_format (str): Default image format ('png' or 'webp').
        embed_images (bool): True if images are embedded as Data URLs (no image files written).

    Returns:
        int: Maximum number of drawlib image blocks in any single document in `tasks`.

    Raises:
        ValueError: If any two documents or drawlib blocks resolve to the same output file path.
    """
    seen_outputs: dict[str, str] = {}
    max_blocks = 0

    for (_, dest_abs, _), disp_name in zip(tasks, display_names):
        if dest_abs:
            norm_dest = os.path.abspath(dest_abs)
            if norm_dest in seen_outputs:
                raise ValueError(format_duplicate_output_error(norm_dest, seen_outputs[norm_dest], disp_name))
            seen_outputs[norm_dest] = disp_name

    for (src_abs, dest_abs, is_md), disp_name in zip(tasks, display_names):
        try:
            with open(src_abs, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError:
            continue

        blocks = extract_code_blocks(content, is_html=not is_md)
        max_blocks = max(max_blocks, len(blocks))

        if embed_images:
            continue

        output_dir = os.path.dirname(os.path.abspath(dest_abs)) if dest_abs else os.path.dirname(src_abs)
        doc_base_name = (
            os.path.splitext(os.path.basename(dest_abs))[0]
            if dest_abs
            else os.path.splitext(os.path.basename(src_abs))[0]
        )

        for block in blocks:
            _, target_img_path = resolve_block_image_paths(
                options=block.options,
                doc_base_name=doc_base_name,
                block_counter=block.index,
                default_format=image_format,
                output_dir=output_dir,
            )
            norm_img = os.path.abspath(target_img_path)
            block_label = f"{disp_name} (block #{block.index}, line {block.line_number})"
            if norm_img in seen_outputs:
                raise ValueError(format_duplicate_output_error(norm_img, seen_outputs[norm_img], block_label))
            seen_outputs[norm_img] = block_label

    return max_blocks


__all__ = [
    "BAR_WIDTH",
    "FileBuildProgress",
    "check_document_output_duplicates",
    "format_duplicate_output_error",
    "format_progress_line",
]
