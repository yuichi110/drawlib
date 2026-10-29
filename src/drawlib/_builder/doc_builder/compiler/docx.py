# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""MS Word (.docx) document compiler for drawlib."""

from __future__ import annotations

import os

from drawlib._builder._common import resolve_styles_and_utils
from drawlib._builder.doc_builder.compiler.base import require_directory
from drawlib._builder.doc_builder.compiler.pdf import _is_slide_project_dir


def _resolve_docx_dest(default_base_dir: str, default_stem: str, output_file: str | None) -> str:
    """Resolve output .docx file path from explicit option or default directory/stem."""
    if output_file:
        if os.path.isdir(output_file) or output_file.endswith(os.sep) or output_file.endswith("/"):
            return os.path.abspath(os.path.join(output_file, f"{default_stem}.docx"))
        return os.path.abspath(output_file)
    return os.path.join(default_base_dir, f"{default_stem}.docx")


def build_docx(
    input_path: str | None = None,
    output_file: str | None = None,
    *,
    input_dir: str | None = None,
    title: str | None = None,
    page_break: bool = True,
    generate_index: bool = False,
    dpi: int = 200,
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str:
    """Compile Markdown chapters or a single Markdown file into a native MS Word (.docx) document.

    Args:
        input_path (Optional[str]): Directory containing Markdown (.md) chapters or single Markdown file.
        output_file (Optional[str]): Destination .docx file path. Defaults to '<name>.docx'.
        input_dir (Optional[str]): Alias for input_path.
        title (Optional[str]): Document title override.
        page_break (bool): Insert page breaks between merged chapters. Defaults to True.
        generate_index (bool): Generate a Table of Contents between 1st and 2nd documents.
        dpi (int): Rasterization DPI for embedded drawlib diagrams. Defaults to 200.
        styles_path (Optional[str]): Path to custom styles.py script.
        utils_path (Optional[str]): Path to custom utils.py script.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.
        timestamp (bool): If True, include current build timestamp in document metadata.

    Returns:
        str: Absolute path of generated .docx file.

    Raises:
        ValueError: If input_path does not exist, is a slide presentation directory, or has an unsupported format.
    """
    resolved_input = input_path if input_path is not None else input_dir
    if not resolved_input:
        raise ValueError("No input directory or file specified for build_docx.")
    if not os.path.exists(resolved_input):
        raise ValueError(f'Input path "{resolved_input}" does not exist.')
    if dpi <= 0:
        raise ValueError(f"dpi must be a positive integer, got {dpi}.")

    input_abs = os.path.abspath(resolved_input)

    if _is_slide_project_dir(input_abs):
        raise ValueError(
            f'Input directory "{input_abs}" is a slide presentation project. '
            f'Please use "drawlib build pptx {resolved_input}" to export MS PowerPoint (.pptx) slides.'
        )

    from drawlib._builder.doc_builder.exporter_docx import export_chapters_to_docx

    if os.path.isfile(input_abs):
        ext = os.path.splitext(input_abs)[1].lower()
        if ext not in {".md", ".markdown"}:
            raise ValueError(f'Unsupported input file "{input_abs}". Expected .md file for Word (.docx) export.')

        search_dir = os.path.dirname(input_abs)
        styles_abs, utils_abs = resolve_styles_and_utils(search_dir, styles_path, utils_path)
        c_cand = os.path.join(search_dir, "style.css")
        css_file = c_cand if os.path.isfile(c_cand) else None

        stem = os.path.splitext(os.path.basename(input_abs))[0]
        dest_abs = _resolve_docx_dest(search_dir, stem, output_file)
        export_chapters_to_docx(
            inputs=[input_abs],
            output_path=dest_abs,
            title=title,
            page_break=page_break,
            generate_index=generate_index,
            dpi=dpi,
            styles_path=styles_abs,
            utils_path=utils_abs,
            css_path=css_file,
            no_cache=no_cache,
            timestamp=timestamp,
        )
        return dest_abs

    input_dir_abs = require_directory(resolved_input, "build_docx")
    styles_abs, utils_abs = resolve_styles_and_utils(input_dir_abs, styles_path, utils_path)
    c_cand = os.path.join(input_dir_abs, "style.css")
    css_file = c_cand if os.path.isfile(c_cand) else None

    dir_name = os.path.basename(input_dir_abs.rstrip(os.sep))
    base_name = dir_name[:-4] if dir_name.endswith("_src") else dir_name
    if not base_name:
        base_name = "document"

    dest_abs = _resolve_docx_dest(os.path.dirname(input_dir_abs), base_name, output_file)
    export_chapters_to_docx(
        inputs=[input_dir_abs],
        output_path=dest_abs,
        title=title,
        page_break=page_break,
        generate_index=generate_index,
        dpi=dpi,
        styles_path=styles_abs,
        utils_path=utils_abs,
        css_path=css_file,
        no_cache=no_cache,
        timestamp=timestamp,
    )
    return dest_abs
