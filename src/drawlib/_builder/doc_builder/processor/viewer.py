# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""CLI viewer and block export functionality for drawlib code blocks."""

from __future__ import annotations

import os
import sys
import tempfile
from typing import Optional

from drawlib._builder.doc_builder.detector import detect_document_type
from drawlib._builder.doc_builder.processor.options import ExtractedBlockInfo
from drawlib._builder.doc_builder.processor.parser import extract_code_blocks, resolve_selected_block


def render_code_with_context(
    code: str,
    dest_abs: str,
    source_filename: str,
    file_dir: str,
    styles_path: Optional[str],
    utils_path: Optional[str],
    grid: bool,
    no_cache: bool = False,
) -> None:
    """Execute code block and render directly to destination path under directory context."""
    from drawlib._builder.doc_builder.processor.processor import DrawlibBlockProcessor

    processor = DrawlibBlockProcessor(styles_path=styles_path, utils_path=utils_path, no_cache=no_cache)
    orig_cwd = os.getcwd()
    sys_path_added = False
    try:
        os.chdir(file_dir)
        if file_dir not in sys.path:
            sys.path.insert(0, file_dir)
            sys_path_added = True

        processor.render_block_to_file(code, dest_abs, source_filename=source_filename, grid=grid)
    finally:
        os.chdir(orig_cwd)
        if sys_path_added and file_dir in sys.path:
            sys.path.remove(file_dir)


def export_code_block(
    file_path: Optional[str] = None,
    target: Optional[str] = None,
    output_path: Optional[str] = None,
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    grid: bool = False,
    no_cache: bool = False,
) -> str:
    """Execute target code block from Markdown, HTML, or Python file and export image."""
    if not file_path:
        raise ValueError("No file path provided.")

    if not os.path.exists(file_path):
        raise ValueError(f"File '{file_path}' does not exist.")

    target_path = file_path
    abs_path = os.path.abspath(target_path)
    file_dir = os.path.dirname(abs_path)

    if target_path.endswith(".py"):
        with open(target_path, "r", encoding="utf-8") as f:
            code = f.read()

        dest = output_path if output_path else f"{os.path.splitext(os.path.basename(target_path))[0]}.png"
        dest_abs = os.path.abspath(dest)
        render_code_with_context(
            code=code,
            dest_abs=dest_abs,
            source_filename=abs_path,
            file_dir=file_dir,
            styles_path=styles_path,
            utils_path=utils_path,
            grid=grid,
            no_cache=no_cache,
        )
        print(f"Successfully exported Python script to: {dest_abs}")
        return dest_abs

    doc_base_name = os.path.splitext(os.path.basename(target_path))[0]
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(target_path, content)
    blocks = extract_code_blocks(content, is_html=doc_info.is_html)
    if not blocks:
        raise ValueError(f"No drawlib code blocks found in '{target_path}' (detected type: {doc_info.doc_type}).")

    if not target:
        print(f"Available drawlib code blocks in '{target_path}':")
        print(f"{'Index':<7} {'Line':<7} {'File Target':<28} {'Header Options'}")
        print("-" * 65)
        for b in blocks:
            target_rel_path = b.file_name if ("/" in b.file_name) else f"{doc_base_name}_images/{b.file_name}"
            opts = b.info_str if b.info_str else "-"
            print(f"{b.index:<7} L{b.line_number:<6} {target_rel_path:<28} {opts}")
        return ""

    selected_block = resolve_selected_block(blocks, target)
    if not selected_block:
        raise ValueError(f"Could not find block matching '{target}' in '{target_path}'.")

    if output_path:
        if os.path.isdir(output_path) or output_path.endswith(os.sep) or output_path.endswith("/"):
            dest = os.path.join(output_path, os.path.basename(selected_block.file_name))
        else:
            dest = output_path
    else:
        dest = os.path.basename(selected_block.file_name)

    dest_abs = os.path.abspath(dest)
    render_code_with_context(
        code=selected_block.code,
        dest_abs=dest_abs,
        source_filename=abs_path,
        file_dir=file_dir,
        styles_path=styles_path,
        utils_path=utils_path,
        grid=grid,
        no_cache=no_cache,
    )
    print(f"Successfully exported block #{selected_block.index} to: {dest_abs}")
    return dest_abs


def display_image_file(image_path: str) -> None:
    """Open and display image file using PIL Image.show() unless disabled."""
    print(f"Rendered successfully to temp file: {image_path}")
    from PIL import Image

    img = Image.open(image_path)
    if os.environ.get("DRAWLIB_SHOW_NO_DISPLAY") != "1":
        img.show()


def show_code_block(
    file_path: Optional[str] = None,
    target: Optional[str] = None,
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    grid: bool = False,
    output_path: Optional[str] = None,
    no_cache: bool = False,
) -> None:
    """Execute target code block from Markdown/HTML file or Python script and display output image."""
    if output_path:
        export_code_block(
            file_path=file_path,
            target=target,
            output_path=output_path,
            styles_path=styles_path,
            utils_path=utils_path,
            grid=grid,
            no_cache=no_cache,
        )
        return

    if not file_path:
        print("Error: No file path provided.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    target_path = file_path

    if target_path.endswith(".py"):
        print(f"Executing Python script '{target_path}'" + (" with grid overlay..." if grid else "..."))
        with open(target_path, "r", encoding="utf-8") as f:
            code = f.read()

        abs_file = os.path.abspath(target_path)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        base, ext = os.path.splitext(tmp_path)
        grid_path = f"{base}_grid{ext}"
        render_code_with_context(
            code=code,
            dest_abs=tmp_path,
            source_filename=abs_file,
            file_dir=os.path.dirname(abs_file),
            styles_path=styles_path,
            utils_path=utils_path,
            grid=grid,
            no_cache=no_cache,
        )
        display_path = grid_path if (grid and os.path.exists(grid_path)) else tmp_path
        display_image_file(display_path)
        return

    doc_base_name = os.path.splitext(os.path.basename(target_path))[0]
    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(target_path, content)
    blocks = extract_code_blocks(content, is_html=doc_info.is_html)
    if not blocks:
        print(f"No drawlib code blocks found in '{target_path}' (detected type: {doc_info.doc_type}).")
        return

    if not target:
        print(f"Available drawlib code blocks in '{target_path}':")
        print(f"{'Index':<7} {'Line':<7} {'File Target':<28} {'Header Options'}")
        print("-" * 65)
        for b in blocks:
            target_rel_path = b.file_name if ("/" in b.file_name) else f"{doc_base_name}_images/{b.file_name}"
            opts = b.info_str if b.info_str else "-"
            print(f"{b.index:<7} L{b.line_number:<6} {target_rel_path:<28} {opts}")
        return

    selected_block = resolve_selected_block(blocks, target)
    if not selected_block:
        print(f"Error: Could not find block matching '{target}' in '{target_path}'.", file=sys.stderr)
        sys.exit(1)

    target_rel_path = (
        selected_block.file_name
        if ("/" in selected_block.file_name)
        else f"{doc_base_name}_images/{selected_block.file_name}"
    )
    print(
        f"Executing block #{selected_block.index} (L{selected_block.line_number} -> {target_rel_path})"
        + (" with grid overlay..." if grid else "...")
    )

    abs_doc = os.path.abspath(target_path)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name

    base, ext = os.path.splitext(tmp_path)
    grid_path = f"{base}_grid{ext}"
    render_code_with_context(
        code=selected_block.code,
        dest_abs=tmp_path,
        source_filename=abs_doc,
        file_dir=os.path.dirname(abs_doc),
        styles_path=styles_path,
        utils_path=utils_path,
        grid=grid,
        no_cache=no_cache,
    )
    display_path = grid_path if (grid and os.path.exists(grid_path)) else tmp_path
    display_image_file(display_path)


_render_code_with_context = render_code_with_context
_display_image_file = display_image_file
