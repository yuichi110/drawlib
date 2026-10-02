# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Markdown documentation compiler for drawlib."""

from __future__ import annotations

import os
import sys
from typing import Optional

from drawlib._builder._common import BuildImageCache, FileBuildProgress, resolve_styles_and_utils
from drawlib._builder.doc_builder.compiler.base import (
    copy_directory_assets,
    require_directory,
    validate_markdown_images,
)
from drawlib._builder.doc_builder.detector import detect_document_type
from drawlib._builder.doc_builder.exporter_md import write_rendered_markdown
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.doc_builder.progress import check_document_output_duplicates


def build_markdown(
    input_dir: str,
    output_dir: Optional[str] = None,
    *,
    image_format: str = "png",
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    no_cache: bool = False,
) -> str:
    """Compile a directory of Markdown files with drawlib code blocks into rendered Markdown.

    Args:
        input_dir (str): Directory containing Markdown (.md) source files.
        output_dir (Optional[str]): Target output directory. Defaults to input_dir.
        image_format (str): Image output format ('png' or 'webp'). Defaults to 'png'.
        styles_path (Optional[str]): Path to custom styles.py script.
        utils_path (Optional[str]): Path to custom utils.py script.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.

    Returns:
        str: Absolute path of generated Markdown output directory.

    Raises:
        ValueError: If input_dir is not a directory or output is invalid.
    """
    input_abs = require_directory(input_dir, "build_markdown")
    out_dir_abs = os.path.abspath(output_dir) if output_dir else input_abs

    if out_dir_abs == input_abs:
        raise ValueError(
            f'Refusing to overwrite input source directory "{input_abs}". '
            "Please specify a different output directory."
        )

    styles_abs, utils_abs = resolve_styles_and_utils(input_abs, styles_path, utils_path)
    cache = BuildImageCache(enabled=not no_cache)

    md_tasks: list[tuple[str, str]] = []
    for root, dirnames, files in os.walk(input_abs):
        if out_dir_abs != input_abs:
            dirnames[:] = [
                d
                for d in dirnames
                if not (
                    os.path.abspath(os.path.join(root, d)) == out_dir_abs
                    or os.path.abspath(os.path.join(root, d)).startswith(out_dir_abs + os.sep)
                )
            ]
        for fname in sorted(files):
            if fname.startswith("."):
                continue
            if fname.lower() in {"readme.md", "readme.markdown"}:
                continue
            if fname.endswith((".md", ".markdown")):
                src_abs = os.path.join(root, fname)
                rel_path = os.path.relpath(src_abs, input_abs)
                dest_abs = os.path.join(out_dir_abs, rel_path)
                md_tasks.append((src_abs, dest_abs))

    total_files = len(md_tasks)
    display_names = ["/" + os.path.relpath(s_abs, input_abs).replace(os.sep, "/") for s_abs, _ in md_tasks]
    max_blocks = check_document_output_duplicates(
        tasks=[(s_abs, d_abs, True) for s_abs, d_abs in md_tasks],
        display_names=display_names,
        image_format=image_format,
        embed_images=False,
    )
    name_width = max((len(n) for n in display_names), default=0)
    image_width = len(str(max(max_blocks, 0)))

    processor: Optional[DrawlibBlockProcessor] = None
    for idx, ((src_abs, dest_abs), disp_name) in enumerate(zip(md_tasks, display_names), start=1):
        processor = _compile_single_markdown_file(
            src_abs=src_abs,
            dest_abs=dest_abs,
            image_format=image_format,
            styles_path=styles_abs,
            utils_path=utils_abs,
            processor=processor,
            progress=FileBuildProgress(
                idx,
                total_files,
                file_name=disp_name,
                name_width=name_width,
                image_width=image_width,
            ),
            no_cache=no_cache,
            cache=cache,
            project_root=input_abs,
        )

    copy_directory_assets(input_abs, out_dir_abs)
    return out_dir_abs


def _compile_single_markdown_file(
    src_abs: str,
    dest_abs: str,
    image_format: str,
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    processor: Optional[DrawlibBlockProcessor] = None,
    progress: Optional[FileBuildProgress] = None,
    no_cache: bool = False,
    cache: Optional[BuildImageCache] = None,
    project_root: Optional[str] = None,
) -> DrawlibBlockProcessor | None:
    """Compile a single Markdown file with drawlib blocks into rendered Markdown."""
    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(src_abs, content)
    total_steps = doc_info.block_count
    if progress is not None:
        progress.update(0, total_steps, done=False)

    validate_markdown_images(src_abs, content)

    if doc_info.has_drawlib and processor is None:
        processor = DrawlibBlockProcessor(
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
            cache=cache,
            project_root=project_root,
        )

    src_dir = os.path.dirname(src_abs)
    output_dir = os.path.dirname(dest_abs)
    doc_base_name = os.path.splitext(os.path.basename(dest_abs))[0]

    orig_cwd = os.getcwd()
    sys_path_added = False
    try:
        os.chdir(src_dir)
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
            sys_path_added = True

        if doc_info.doc_type == "markdown_drawlib":
            if processor is None:
                processor = DrawlibBlockProcessor(
                    styles_path=styles_path,
                    utils_path=utils_path,
                    no_cache=no_cache,
                    cache=cache,
                    project_root=project_root,
                )
            processed_text = processor.process_markdown(
                content,
                doc_base_name=doc_base_name,
                output_dir=output_dir,
                image_format=image_format,
                use_markdown_syntax=True,
                source_filename=src_abs,
                progress_callback=(progress.update if progress else None),
            )
            rendered_content = processed_text
        else:
            rendered_content = content

        write_rendered_markdown(rendered_content, dest_abs)
    finally:
        os.chdir(orig_cwd)
        if sys_path_added and src_dir in sys.path:
            sys.path.remove(src_dir)

    if progress is not None:
        progress.update(total_steps, total_steps, done=True)

    return processor
