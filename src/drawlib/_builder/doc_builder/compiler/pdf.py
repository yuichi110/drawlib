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
    input_dir: str,
    output_file: Optional[str] = None,
    *,
    title: Optional[str] = None,
    page_break: bool = True,
    generate_index: bool = False,
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str:
    """Merge Markdown chapters in a directory into a single HTML and export to PDF.

    Args:
        input_dir (str): Directory containing Markdown (.md) chapter documents.
        output_file (Optional[str]): Destination PDF file path. Defaults to '<input_dir_name>.pdf'.
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
        ValueError: If input_dir is not a directory or required assets are missing.
    """
    input_abs = require_directory(input_dir, "build_pdf")
    template_file, css_file = resolve_template_and_css(input_abs)
    styles_abs, utils_abs = resolve_styles_and_utils(input_abs, styles_path, utils_path)

    merged_html, file_list = build_merged_html(
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

    if output_file:
        if os.path.isdir(output_file) or output_file.endswith(os.sep) or output_file.endswith("/"):
            dir_name = os.path.basename(input_abs.rstrip(os.sep)) or "document"
            dest_abs = os.path.abspath(os.path.join(output_file, f"{dir_name}.pdf"))
        else:
            dest_abs = os.path.abspath(output_file)
    else:
        dir_name = os.path.basename(input_abs.rstrip(os.sep)) or "document"
        dest_abs = os.path.join(os.path.dirname(input_abs), f"{dir_name}.pdf")

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    export_html_to_pdf(merged_html, dest_abs, timestamp=timestamp)
    return dest_abs
