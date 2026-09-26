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
import sys
from typing import Callable, Sequence

from drawlib._builder.doc_builder.processor import _resolve_block_image_paths, extract_code_blocks
from drawlib._core.utils import dutil_settings

BAR_WIDTH = 20


def format_duplicate_output_error(
    output_path: str,
    source_a: str,
    source_b: str,
) -> str:
    """Format a user-friendly error message when two sources produce the same output file.

    Args:
        output_path (str): The colliding output file path.
        source_a (str): First source file or block identifier.
        source_b (str): Second source file or block identifier.

    Returns:
        str: Formatted multi-line error message.
    """
    return (
        f'Duplicate output file detected: "{output_path}"\n'
        f"  - Source A: {source_a}\n"
        f"  - Source B: {source_b}\n"
        f'"{source_a}" と "{source_b}" の出力ファイルが重複しています。重複しないように修正してください。'
    )


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
            _, target_img_path = _resolve_block_image_paths(
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


def format_progress_line(
    file_index: int,
    total_files: int,
    completed_steps: int,
    total_steps: int,
    done: bool = False,
    file_name: str = "",
    name_width: int = 0,
    image_width: int = 1,
) -> str:
    """Format a single per-file progress line: `file:x/y <padded_file_name> images:x/y : <bar> <percent>%`.

    Args:
        file_index (int): 1-based index of the current file.
        total_files (int): Total number of files in the build.
        completed_steps (int): Number of completed blocks/images in the current file.
        total_steps (int): Total number of blocks/images in the current file.
        done (bool): True if the current file has completely finished building.
        file_name (str): Display file path (e.g. `/dir/file.py`).
        name_width (int): Width to pad `file_name` to so columns align vertically.
        image_width (int): Digit width for `images:x/y` counts so colons align vertically.

    Returns:
        str: Formatted progress string (e.g. `file: 1/17 /file.md     images: 2/ 2 : #################### 100%`).
    """
    idx_width = len(str(max(total_files, 1)))
    file_col = f"file:{file_index:>{idx_width}}/{total_files}"
    width = max(name_width, len(file_name))
    name_col = f" {file_name:<{width}}" if file_name else ""
    img_w = max(image_width, len(str(max(total_steps, completed_steps, 0))), 1)
    img_col = f" images:{completed_steps:>{img_w}}/{total_steps:>{img_w}}"

    if done:
        bar = "#" * BAR_WIDTH
        pct = 100
    else:
        ratio = max(0.0, min(1.0, completed_steps / total_steps)) if total_steps > 0 else 0.0
        pct = int(round(ratio * 100))
        if pct >= 100:
            pct = 99
        filled = min(BAR_WIDTH - 1, int(BAR_WIDTH * ratio))
        bar = ("#" * filled) + "." + (" " * (BAR_WIDTH - filled - 1))

    return f"{file_col}{name_col}{img_col} : {bar} {pct:>3d}%"


class FileBuildProgress:
    """Manages in-place terminal progress updates for a single file out of `total_files`."""

    def __init__(
        self,
        file_index: int,
        total_files: int,
        file_name: str = "",
        name_width: int = 0,
        image_width: int = 1,
    ) -> None:
        """Initialize progress tracker for `file_index` / `total_files`."""
        self.file_index = file_index
        self.total_files = total_files
        self.file_name = file_name
        self.name_width = name_width
        self.image_width = image_width
        self._quiet = dutil_settings.get_logging_mode() == "quiet"
        self._is_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    def update(self, completed_steps: int, total_steps: int, done: bool = False) -> None:
        """Render progress update to stdout.

        Args:
            completed_steps (int): Completed blocks/images in the current file.
            total_steps (int): Total blocks/images in the current file.
            done (bool): True when the file is 100% complete.
        """
        if self._quiet:
            return

        line = format_progress_line(
            file_index=self.file_index,
            total_files=self.total_files,
            completed_steps=completed_steps,
            total_steps=total_steps,
            done=done,
            file_name=self.file_name,
            name_width=self.name_width,
            image_width=self.image_width,
        )

        if self._is_tty:
            end_char = "\n" if done else ""
            sys.stdout.write(f"\r{line}{end_char}")
            sys.stdout.flush()
        elif done:
            print(line, flush=True)

    def as_callback(self) -> Callable[[int, int, bool], None]:
        """Return a callback function `(completed_steps, total_steps, done)`."""
        return self.update
