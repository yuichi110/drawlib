# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib code block processor package."""

from __future__ import annotations

from drawlib._builder.doc_builder.processor.options import (
    DrawlibBlockOptions,
    ExtractedBlockInfo,
    parse_block_info,
    resolve_block_image_paths,
)
from drawlib._builder.doc_builder.processor.parser import (
    extract_code_blocks,
    resolve_selected_block,
)
from drawlib._builder.doc_builder.processor.processor import DrawlibBlockProcessor
from drawlib._builder.doc_builder.processor.viewer import (
    display_image_file,
    export_code_block,
    render_code_with_context,
    show_code_block,
)

__all__ = [
    "DrawlibBlockOptions",
    "DrawlibBlockProcessor",
    "ExtractedBlockInfo",
    "display_image_file",
    "export_code_block",
    "extract_code_blocks",
    "parse_block_info",
    "render_code_with_context",
    "resolve_block_image_paths",
    "resolve_selected_block",
    "show_code_block",
]
