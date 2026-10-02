# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code block extraction and AST resolution from Markdown and HTML text."""

from __future__ import annotations

import os
import re
from typing import List, Optional

from drawlib._builder.doc_builder.detector import preserve_outer_fences
from drawlib._builder.doc_builder.processor.options import (
    DrawlibBlockOptions,
    ExtractedBlockInfo,
    parse_block_info,
)


def extract_code_blocks(
    text: str,
    is_html: bool = False,
    require_file: bool = False,
) -> List[ExtractedBlockInfo]:
    """Extract all drawlib code blocks from Markdown or HTML text.

    Args:
        text (str): Input Markdown or HTML text.
        is_html (bool): If True, extract <script type="text/drawlib"> blocks; otherwise extract ```drawlib blocks.
        require_file (bool): If True, raise ValueError if options.file is missing.

    Returns:
        List[ExtractedBlockInfo]: List of extracted code block information objects.

    Raises:
        ValueError: If require_file is True and any block lacks a 'file:<filename.ext>' option.
    """
    blocks: List[ExtractedBlockInfo] = []

    if is_html:
        pattern_script = re.compile(
            r"""<script\b([^>]*)type=["']text/drawlib["']([^>]*)>(.*?)</script>""",
            re.DOTALL | re.IGNORECASE,
        )
        for idx, match in enumerate(pattern_script.finditer(text), start=1):
            start_line = text[: match.start()].count("\n") + 1
            info_str = (match.group(1) + " " + match.group(2)).strip()
            code = match.group(3).strip()
            options = parse_block_info(info_str)
            ext = "webp" if (options.format == "webp") else "png"
            if options.file:
                fn = options.file if ("." in options.file) else f"{options.file}.{ext}"
            else:
                if require_file:
                    raise ValueError(
                        f"Missing required 'file:<filename.ext>' option in drawlib code block at line {start_line}. "
                        'Example: <script type="text/drawlib" file="my_diagram.png">'
                    )
                fn = f"{idx}.{ext}"

            blocks.append(
                ExtractedBlockInfo(
                    index=idx,
                    code=code,
                    info_str=info_str,
                    options=options,
                    file_name=fn,
                    line_number=start_line,
                )
            )
        return blocks

    masked_text, _ = preserve_outer_fences(text)
    lines = masked_text.splitlines()
    i = 0
    block_index = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"^[ \t]*```drawlib([^\n]*)", line)
        if match:
            block_index += 1
            start_line = i + 1
            info_str = match.group(1).strip()
            options = parse_block_info(info_str)
            code_lines = []
            i += 1
            while i < len(lines) and not re.match(r"^[ \t]*```", lines[i]):
                code_lines.append(lines[i])
                i += 1
            code = "\n".join(code_lines).strip()

            ext = "webp" if (options.format == "webp") else "png"
            if options.file:
                fn = options.file if ("." in options.file) else f"{options.file}.{ext}"
            else:
                if require_file:
                    raise ValueError(
                        f"Missing required 'file:<filename.ext>' option in drawlib code block at line {start_line}. "
                        "Example: ```drawlib file:my_diagram.png"
                    )
                fn = f"{block_index}.{ext}"

            blocks.append(
                ExtractedBlockInfo(
                    index=block_index,
                    code=code,
                    info_str=info_str,
                    options=options,
                    file_name=fn,
                    line_number=start_line,
                )
            )
        i += 1
    return blocks


def resolve_selected_block(
    blocks: List[ExtractedBlockInfo],
    target: str,
) -> Optional[ExtractedBlockInfo]:
    """Find matching ExtractedBlockInfo by 1-based index or filename.

    Args:
        blocks (List[ExtractedBlockInfo]): List of extracted code blocks.
        target (str): 1-based index string (e.g. '1', '-1') or filename (e.g. '1.png', 'my_image').

    Returns:
        Optional[ExtractedBlockInfo]: Matching block info or None.
    """
    if target.isdigit() or (target.startswith("-") and target[1:].isdigit()):
        idx = int(target)
        if idx < 0:
            idx = len(blocks) + idx + 1
        for b in blocks:
            if b.index == idx:
                return b
        return None

    target_clean = target.lower()
    for b in blocks:
        b_fn = b.file_name.lower()
        b_base = os.path.splitext(b_fn)[0]
        b_basename_only = os.path.basename(b_fn)
        b_basename_stem = os.path.splitext(b_basename_only)[0]
        if target_clean in {b_fn, b_base, b_basename_only, b_basename_stem}:
            return b
    return None


_resolve_selected_block = resolve_selected_block
