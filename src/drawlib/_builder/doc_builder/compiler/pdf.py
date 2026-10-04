# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""PDF document compiler for drawlib."""

from __future__ import annotations

import os
from typing import Optional

from drawlib._builder._common import resolve_styles_and_utils
from drawlib._builder.doc_builder.compiler.base import (
    require_directory,
    resolve_template_and_css,
)
from drawlib._builder.doc_builder.exporter_pdf import export_html_to_pdf
from drawlib._builder.doc_builder.merger import build_merged_html


def build_pdf(
    input_path: Optional[str] = None,
    output_file: Optional[str] = None,
    *,
    input_dir: Optional[str] = None,
    title: Optional[str] = None,
    page_break: bool = True,
    generate_index: bool = False,
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str:
    """Merge Markdown chapters, single Markdown file, or slide deck into a print-ready vector PDF.

    Args:
        input_path (Optional[str]): Directory containing Markdown (.md) documents, single Markdown file,
            or slide presentation directory.
        output_file (Optional[str]): Destination PDF file path. Defaults to '<name>.pdf'.
        input_dir (Optional[str]): Alias for input_path.
        title (Optional[str]): Document title override.
        page_break (bool): Insert CSS page breaks between merged chapters. Defaults to True.
        generate_index (bool): Generate a Table of Contents between 1st and 2nd documents.
        styles_path (Optional[str]): Path to custom styles.py script.
        utils_path (Optional[str]): Path to custom utils.py script.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.
        timestamp (bool): If True, include current build timestamp in PDF metadata.

    Returns:
        str: Absolute path of generated PDF file.

    Raises:
        ValueError: If input_path does not exist or has an unsupported format.
    """
    resolved_input = input_path if input_path is not None else input_dir
    if not resolved_input:
        raise ValueError("No input directory or file specified for build_pdf.")
    if not os.path.exists(resolved_input):
        raise ValueError(f'Input path "{resolved_input}" does not exist.')

    input_abs = os.path.abspath(resolved_input)

    # 1. Slide presentation project directory
    if os.path.isdir(input_abs) and os.path.isfile(os.path.join(input_abs, "slide.css")):
        import tempfile

        from drawlib._builder.doc_builder.exporter_pdf import export_html_file_to_pdf
        from drawlib._slide import build_slide

        dir_name = os.path.basename(input_abs.rstrip(os.sep))
        base_name = dir_name[:-4] if dir_name.endswith("_src") else dir_name
        if not base_name:
            base_name = "slide"

        if output_file:
            if os.path.isdir(output_file) or output_file.endswith(os.sep) or output_file.endswith("/"):
                dest_abs = os.path.abspath(os.path.join(output_file, f"{base_name}.pdf"))
            else:
                dest_abs = os.path.abspath(output_file)
        else:
            dest_abs = os.path.join(os.path.dirname(input_abs), f"{base_name}.pdf")

        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_html = build_slide(
                input_dir=input_abs,
                output_dir=tmp_dir,
                styles_path=styles_path,
                utils_path=utils_path,
                no_cache=no_cache,
            )
            export_html_file_to_pdf(index_html, dest_abs, timestamp=timestamp, prefer_css_page_size=True)
        return dest_abs

    # 2. Single Markdown / HTML file
    if os.path.isfile(input_abs):
        ext = os.path.splitext(input_abs)[1].lower()
        if ext not in {".md", ".markdown", ".html", ".htm"}:
            raise ValueError(f'Unsupported input file "{input_abs}". Expected .md or .html.')

        search_dir = os.path.dirname(input_abs)
        styles_abs, utils_abs = resolve_styles_and_utils(search_dir, styles_path, utils_path)
        t_cand = os.path.join(search_dir, "template.html")
        template_file = t_cand if os.path.isfile(t_cand) else None
        c_cand = os.path.join(search_dir, "style.css")
        css_file = c_cand if os.path.isfile(c_cand) else None

        merged_html, _ = build_merged_html(
            inputs=[input_abs],
            title=title,
            page_break=page_break,
            generate_index=generate_index,
            styles_path=styles_abs,
            utils_path=utils_abs,
            css_path=css_file,
            template_path=template_file,
            no_cache=no_cache,
        )

        stem = os.path.splitext(os.path.basename(input_abs))[0]
        if output_file:
            if os.path.isdir(output_file) or output_file.endswith(os.sep) or output_file.endswith("/"):
                dest_abs = os.path.abspath(os.path.join(output_file, f"{stem}.pdf"))
            else:
                dest_abs = os.path.abspath(output_file)
        else:
            dest_abs = os.path.join(search_dir, f"{stem}.pdf")

        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        export_html_to_pdf(merged_html, dest_abs, timestamp=timestamp)
        return dest_abs

    # 3. Document chapters directory
    input_dir_abs = require_directory(resolved_input, "build_pdf")
    template_file, css_file = resolve_template_and_css(input_dir_abs)
    styles_abs, utils_abs = resolve_styles_and_utils(input_dir_abs, styles_path, utils_path)

    merged_html, _ = build_merged_html(
        inputs=[input_dir_abs],
        title=title,
        page_break=page_break,
        generate_index=generate_index,
        styles_path=styles_abs,
        utils_path=utils_abs,
        css_path=css_file,
        template_path=template_file,
        no_cache=no_cache,
    )

    dir_name = os.path.basename(input_dir_abs.rstrip(os.sep))
    base_name = dir_name[:-4] if dir_name.endswith("_src") else dir_name
    if not base_name:
        base_name = "document"

    if output_file:
        if os.path.isdir(output_file) or output_file.endswith(os.sep) or output_file.endswith("/"):
            dest_abs = os.path.abspath(os.path.join(output_file, f"{base_name}.pdf"))
        else:
            dest_abs = os.path.abspath(output_file)
    else:
        dest_abs = os.path.join(os.path.dirname(input_dir_abs), f"{base_name}.pdf")

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    export_html_to_pdf(merged_html, dest_abs, timestamp=timestamp)
    return dest_abs
