# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Document compiler package for drawlib."""

from __future__ import annotations

import os
import re
import shutil
import sys
from typing import List, Optional, Sequence, Union

from drawlib._tools.doc_builder.build_cache import BuildImageCache
from drawlib._tools.doc_builder.detector import DocType, DocumentInputInfo, detect_document_type
from drawlib._tools.doc_builder.exporter_html import get_default_css, render_html_document
from drawlib._tools.doc_builder.exporter_md import write_rendered_markdown
from drawlib._tools.doc_builder.exporter_pdf import export_html_to_pdf
from drawlib._tools.doc_builder.merger import build_merged_html
from drawlib._tools.doc_builder.parser_md import parse_markdown_to_html
from drawlib._tools.doc_builder.processor import (
    DrawlibBlockProcessor,
    export_code_block,
    extract_code_blocks,
    show_code_block,
)
from drawlib._tools.doc_builder.progress import (
    FileBuildProgress,
    check_document_output_duplicates,
)
from drawlib._tools.doc_builder.template import (
    export_css,
    export_default_template,
    export_html_css,
    export_html_template,
    export_pdf_css,
    export_pdf_template,
    export_template,
    list_css,
    list_html_css,
    list_html_templates,
    list_pdf_css,
    list_pdf_templates,
    list_templates,
    validate_template,
)


def _validate_markdown_images(src_abs: str, content: str) -> None:
    """Check for missing local static images referenced via ![alt](path) in markdown."""
    src_dir = os.path.dirname(src_abs)
    pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    for match in pattern.finditer(content):
        img_ref = match.group(2).strip()
        if not img_ref or img_ref.startswith(("http://", "https://", "data:", "#")):
            continue
        clean_ref = img_ref.split("#")[0].split("?")[0]
        resolved_path = os.path.abspath(os.path.join(src_dir, clean_ref))
        if not os.path.exists(resolved_path):
            sys.stderr.write(f"WARNING: Image '{img_ref}' referenced in '{src_abs}' does not exist.\n")


def _extract_title(md_content: str, filename: str) -> str:
    """Extract title from first H1 header in Markdown content or fallback to filename."""
    for line in md_content.splitlines():
        line_str = line.strip()
        if line_str.startswith("# "):
            return line_str[2:].strip()
    base = os.path.splitext(filename)[0]
    return base.replace("_", " ").replace("-", " ").title()


def _build_directory_nav_list(input_abs: str, out_dir_abs: str) -> list[dict[str, str]]:
    """Collect all Markdown files in input_abs recursively and construct navigation targets."""
    nav_list: list[dict[str, str]] = []
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
            if fname.endswith(".md") or fname.endswith(".markdown"):
                src_abs = os.path.join(root, fname)
                rel_path = os.path.relpath(src_abs, input_abs)
                rel_base, _ = os.path.splitext(rel_path)
                dest_abs_html = os.path.join(out_dir_abs, rel_base + ".html")

                try:
                    with open(src_abs, "r", encoding="utf-8") as f:
                        content = f.read()
                    title = _extract_title(content, fname)
                except Exception:
                    title = os.path.splitext(fname)[0].replace("_", " ").title()

                nav_list.append({
                    "title": title,
                    "src_abs": src_abs,
                    "dest_abs": dest_abs_html,
                })

    def _sort_key(item: dict[str, str]) -> tuple[int, str]:
        src_abs = item["src_abs"]
        base = os.path.basename(src_abs).lower()
        if base in {"index.md", "index.markdown"}:
            return (0, src_abs)
        return (1, src_abs)

    nav_list.sort(key=_sort_key)
    return nav_list


def _compile_single_markdown_file(
    src_abs: str,
    dest_abs: str,
    image_format: str,
    config_path: Optional[str],
    processor: Optional[DrawlibBlockProcessor] = None,
    progress: Optional[FileBuildProgress] = None,
    no_cache: bool = False,
    cache: Optional[BuildImageCache] = None,
) -> DrawlibBlockProcessor | None:
    """Compile a single Markdown file into rendered Markdown."""
    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    _validate_markdown_images(src_abs, content)
    doc_info: DocumentInputInfo = detect_document_type(src_abs, content)
    total_steps = doc_info.block_count
    if progress is not None:
        progress.update(0, total_steps, done=False)

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    if doc_info.doc_type == "markdown":
        write_rendered_markdown(content, dest_abs)
        if progress is not None:
            progress.update(total_steps, total_steps, done=True)
        return processor

    if processor is None:
        processor = DrawlibBlockProcessor(config_path=config_path, no_cache=no_cache, cache=cache)

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

        rendered_md = processor.process_markdown(
            content,
            doc_base_name=doc_base_name,
            output_dir=output_dir,
            image_format=image_format,
            use_markdown_syntax=True,
            source_filename=src_abs,
            progress_callback=progress.as_callback() if progress is not None else None,
        )
        write_rendered_markdown(rendered_md, dest_abs)
    finally:
        os.chdir(orig_cwd)
        if sys_path_added and src_dir in sys.path:
            sys.path.remove(src_dir)

    if progress is not None:
        progress.update(total_steps, total_steps, done=True)

    return processor


def build_markdown(
    input_path: str,
    output: Optional[str] = None,
    image_format: str = "png",
    config: Optional[str] = None,
    no_cache: bool = False,
    *,
    output_path: Optional[str] = None,
    config_path: Optional[str] = None,
) -> str:
    """Compile a Markdown file or directory containing drawlib code blocks into standard rendered Markdown.

    Args:
        input_path (str): Input Markdown (.md) file or directory path.
        output (Optional[str]): Destination file or directory path.
        image_format (str): Image output format ('png' or 'webp'). Defaults to 'png'.
        config (Optional[str]): Optional Python configuration script path.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.
        output_path (Optional[str]): Alias for output.
        config_path (Optional[str]): Alias for config.

    Returns:
        str: Absolute path of generated Markdown file or directory.

    Raises:
        ValueError: If input path does not exist, is not Markdown, or overwrites source.
    """
    output = output or output_path
    config = config or config_path
    input_abs = os.path.abspath(input_path)
    if not os.path.exists(input_abs):
        raise ValueError(f'Input path "{input_abs}" does not exist.')

    cache = BuildImageCache(enabled=not no_cache)

    if os.path.isdir(input_abs):
        out_dir_abs = os.path.abspath(output) if output else input_abs
        processor: Optional[DrawlibBlockProcessor] = None
        md_tasks: list[tuple[str, str]] = []
        asset_tasks: list[tuple[str, str]] = []

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
                src_abs = os.path.join(root, fname)
                rel_path = os.path.relpath(src_abs, input_abs)
                if fname.endswith(".md") or fname.endswith(".markdown"):
                    rel_base, _ = os.path.splitext(rel_path)
                    ext = ".md" if out_dir_abs != input_abs else ".rendered.md"
                    dest_abs = os.path.join(out_dir_abs, rel_base + ext)
                    if src_abs == dest_abs:
                        raise ValueError(
                            f'Refusing to overwrite input source file "{src_abs}". '
                            "Please specify a different output directory using -o / --output."
                        )
                    md_tasks.append((src_abs, dest_abs))
                elif not fname.endswith((".html", ".htm")):
                    dest_abs = os.path.join(out_dir_abs, rel_path)
                    if src_abs != dest_abs:
                        asset_tasks.append((src_abs, dest_abs))

        for src_abs, dest_abs in asset_tasks:
            os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
            shutil.copy2(src_abs, dest_abs)

        total_files = len(md_tasks)
        display_names = [
            "/" + os.path.relpath(s_abs, input_abs).replace(os.sep, "/") for s_abs, _ in md_tasks
        ]
        max_blocks = check_document_output_duplicates(
            tasks=[(s_abs, d_abs, True) for s_abs, d_abs in md_tasks],
            display_names=display_names,
            image_format=image_format,
            embed_images=False,
        )
        name_width = max((len(n) for n in display_names), default=0)
        image_width = len(str(max(max_blocks, 0)))
        for idx, ((src_abs, dest_abs), disp_name) in enumerate(zip(md_tasks, display_names), start=1):
            processor = _compile_single_markdown_file(
                src_abs=src_abs,
                dest_abs=dest_abs,
                image_format=image_format,
                config_path=config,
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
            )

        return out_dir_abs

    ext = os.path.splitext(input_abs)[1].lower()
    if ext not in {".md", ".markdown"}:
        raise ValueError(f'Input file "{input_abs}" is not a Markdown file (.md).')

    if output:
        if os.path.isdir(output) or output.endswith(os.sep) or output.endswith("/"):
            out_dir = os.path.abspath(output)
            base_name = os.path.splitext(os.path.basename(input_abs))[0]
            dest_abs = os.path.join(out_dir, f"{base_name}.md")
        else:
            dest_abs = os.path.abspath(output)
    else:
        base_name = os.path.splitext(input_abs)[0]
        dest_abs = f"{base_name}.rendered.md"

    if input_abs == dest_abs:
        raise ValueError(
            f'Refusing to overwrite input source file "{input_abs}". '
            "Please specify a different output path using -o / --output."
        )

    single_name = f"/{os.path.basename(input_abs)}"
    max_blocks = check_document_output_duplicates(
        tasks=[(input_abs, dest_abs, True)],
        display_names=[single_name],
        image_format=image_format,
        embed_images=False,
    )
    _compile_single_markdown_file(
        src_abs=input_abs,
        dest_abs=dest_abs,
        image_format=image_format,
        config_path=config,
        progress=FileBuildProgress(
            1,
            1,
            file_name=single_name,
            name_width=len(single_name),
            image_width=len(str(max(max_blocks, 0))),
        ),
        no_cache=no_cache,
        cache=cache,
    )
    return dest_abs


def _compile_single_html_file(
    src_abs: str,
    dest_abs: str,
    image_format: str,
    config_path: Optional[str],
    css_path: Optional[str],
    css_href: Optional[str],
    nav_list: Optional[list[dict[str, str]]],
    template_path: Optional[str],
    processor: Optional[DrawlibBlockProcessor] = None,
    progress: Optional[FileBuildProgress] = None,
    no_cache: bool = False,
    cache: Optional[BuildImageCache] = None,
) -> DrawlibBlockProcessor | None:
    """Compile a single Markdown or HTML file into HTML."""
    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(src_abs, content)
    total_steps = doc_info.block_count
    if progress is not None:
        progress.update(0, total_steps, done=False)

    if doc_info.is_markdown:
        _validate_markdown_images(src_abs, content)

    if doc_info.has_drawlib and processor is None:
        processor = DrawlibBlockProcessor(config_path=config_path, no_cache=no_cache, cache=cache)

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
                processor = DrawlibBlockProcessor(config_path=config_path, no_cache=no_cache, cache=cache)
            processed_text = processor.process_markdown(
                content,
                doc_base_name=doc_base_name,
                output_dir=output_dir,
                image_format=image_format,
                embed_images=False,
                source_filename=src_abs,
                progress_callback=progress.as_callback() if progress is not None else None,
            )
            body_html = parse_markdown_to_html(processed_text)
        elif doc_info.doc_type == "markdown":
            body_html = parse_markdown_to_html(content)
        elif doc_info.doc_type == "html_drawlib":
            if processor is None:
                processor = DrawlibBlockProcessor(config_path=config_path, no_cache=no_cache, cache=cache)
            processed_html = processor.process_html(
                content,
                doc_base_name=doc_base_name,
                output_dir=output_dir,
                image_format=image_format,
                embed_images=False,
                source_filename=src_abs,
                progress_callback=progress.as_callback() if progress is not None else None,
            )
            if doc_info.is_full_html and template_path is None:
                os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
                with open(dest_abs, "w", encoding="utf-8") as f:
                    f.write(processed_html)
                if progress is not None:
                    progress.update(total_steps, total_steps, done=True)
                return processor
            body_html = processed_html
        else:
            if doc_info.is_full_html and template_path is None:
                os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
                with open(dest_abs, "w", encoding="utf-8") as f:
                    f.write(content)
                if progress is not None:
                    progress.update(total_steps, total_steps, done=True)
                return processor
            body_html = content

        doc_title = (
            _extract_title(content, os.path.basename(src_abs))
            if doc_info.is_markdown
            else os.path.basename(src_abs)
        )

        index_rel_url = "index.html"
        if doc_info.is_markdown and nav_list:
            doc_nav_items: list[dict[str, object]] = []
            dest_dir = os.path.dirname(dest_abs)

            root_index_nav = None
            for nav in nav_list:
                if os.path.basename(nav["dest_abs"]) == "index.html":
                    if root_index_nav is None or len(nav["dest_abs"]) < len(root_index_nav["dest_abs"]):
                        root_index_nav = nav
            if root_index_nav is not None:
                index_rel_url = os.path.relpath(root_index_nav["dest_abs"], dest_dir)
            elif nav_list:
                index_rel_url = os.path.relpath(nav_list[0]["dest_abs"], dest_dir)

            for nav in nav_list:
                rel_url = os.path.relpath(nav["dest_abs"], dest_dir)
                doc_nav_items.append({
                    "title": nav["title"],
                    "url": rel_url,
                    "active": (nav["src_abs"] == src_abs),
                })
        else:
            doc_nav_items = []

        full_html = render_html_document(
            body_html=body_html,
            title=doc_title,
            custom_css_path=css_path,
            css_href=css_href,
            nav_items=doc_nav_items,
            template_path=template_path,
            index_url=index_rel_url,
        )

        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        with open(dest_abs, "w", encoding="utf-8") as f:
            f.write(full_html)
    finally:
        os.chdir(orig_cwd)
        if sys_path_added and src_dir in sys.path:
            sys.path.remove(src_dir)

    if progress is not None:
        progress.update(total_steps, total_steps, done=True)

    return processor


def build_html(
    input_path: str,
    output: Optional[str] = None,
    image_format: str = "png",
    css: Optional[str] = None,
    template: Optional[str] = None,
    config: Optional[str] = None,
    no_cache: bool = False,
    *,
    css_mode: str = "external",
    output_path: Optional[str] = None,
    css_path: Optional[str] = None,
    template_path: Optional[str] = None,
    config_path: Optional[str] = None,
) -> str:
    """Compile a Markdown/HTML file or directory into HTML with an external style.css stylesheet.

    Args:
        input_path (str): Input Markdown (.md), HTML (.html), or directory path.
        output (Optional[str]): Destination file or directory path.
        image_format (str): Image output format ('png' or 'webp'). Defaults to 'png'.
        css (Optional[str]): CSS preset name ('default', 'github', 'minimal', 'monochrome') or .css file path.
        template (Optional[str]): Template preset ('sidebar', 'simple') or .html.j2 file path.
        config (Optional[str]): Optional Python configuration script path.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.
        css_mode (str): CSS mode ('external' by default, or 'embed' if overridden internally).
        output_path (Optional[str]): Alias for output.
        css_path (Optional[str]): Alias for css.
        template_path (Optional[str]): Alias for template.
        config_path (Optional[str]): Alias for config.

    Returns:
        str: Absolute path of generated HTML file or directory.

    Raises:
        ValueError: If input path does not exist or output overwrites source file.
    """
    output = output or output_path
    css = css or css_path
    template = template or template_path
    config = config or config_path
    input_abs = os.path.abspath(input_path)
    if not os.path.exists(input_abs):
        raise ValueError(f'Input path "{input_abs}" does not exist.')

    cache = BuildImageCache(enabled=not no_cache)

    if os.path.isdir(input_abs):
        out_dir_abs = os.path.abspath(output) if output else input_abs
        nav_list = _build_directory_nav_list(input_abs, out_dir_abs)

        style_css_path: Optional[str] = None
        if css_mode != "embed":
            style_css_path = os.path.join(out_dir_abs, "style.css")
            os.makedirs(os.path.dirname(style_css_path), exist_ok=True)
            with open(style_css_path, "w", encoding="utf-8") as f:
                f.write(get_default_css(custom_css_path=css))

        processor: Optional[DrawlibBlockProcessor] = None
        html_tasks: list[tuple[str, str, bool]] = []
        asset_tasks: list[tuple[str, str]] = []

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
                src_abs = os.path.join(root, fname)
                rel_path = os.path.relpath(src_abs, input_abs)

                if fname.endswith(".md") or fname.endswith(".markdown"):
                    rel_base, _ = os.path.splitext(rel_path)
                    dest_abs = os.path.join(out_dir_abs, rel_base + ".html")
                    html_tasks.append((src_abs, dest_abs, True))
                elif fname.endswith((".html", ".htm")):
                    dest_abs = os.path.join(out_dir_abs, rel_path)
                    if src_abs == dest_abs:
                        continue
                    html_tasks.append((src_abs, dest_abs, False))
                else:
                    dest_abs = os.path.join(out_dir_abs, rel_path)
                    if src_abs != dest_abs:
                        asset_tasks.append((src_abs, dest_abs))

        total_files = len(html_tasks)
        display_names = [
            "/" + os.path.relpath(s_abs, input_abs).replace(os.sep, "/") for s_abs, _, _ in html_tasks
        ]
        max_blocks = check_document_output_duplicates(
            tasks=html_tasks,
            display_names=display_names,
            image_format=image_format,
            embed_images=False,
        )

        for src_abs, dest_abs in asset_tasks:
            os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
            shutil.copy2(src_abs, dest_abs)

        name_width = max((len(n) for n in display_names), default=0)
        image_width = len(str(max(max_blocks, 0)))
        for idx, ((src_abs, dest_abs, is_md), disp_name) in enumerate(zip(html_tasks, display_names), start=1):
            rel_css_href = (
                os.path.relpath(style_css_path, os.path.dirname(dest_abs)) if style_css_path else None
            )
            processor = _compile_single_html_file(
                src_abs=src_abs,
                dest_abs=dest_abs,
                image_format=image_format,
                config_path=config,
                css_path=css,
                css_href=rel_css_href,
                nav_list=nav_list if is_md else None,
                template_path=template,
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
            )

        return out_dir_abs

    if output:
        if os.path.isdir(output) or output.endswith(os.sep) or output.endswith("/"):
            out_dir = os.path.abspath(output)
            base_name = os.path.splitext(os.path.basename(input_abs))[0]
            dest_abs = os.path.join(out_dir, f"{base_name}.html")
        else:
            dest_abs = os.path.abspath(output)
    else:
        base_name = os.path.splitext(input_abs)[0]
        ext = os.path.splitext(input_abs)[1].lower()
        dest_abs = f"{base_name}.rendered.html" if ext in {".html", ".htm"} else f"{base_name}.html"

    if input_abs == dest_abs:
        raise ValueError(
            f'Refusing to overwrite input source file "{input_abs}". '
            "Please specify a different output path using -o / --output."
        )

    single_name = f"/{os.path.basename(input_abs)}"
    is_md_single = os.path.splitext(input_abs)[1].lower() in {".md", ".markdown"}
    max_blocks = check_document_output_duplicates(
        tasks=[(input_abs, dest_abs, is_md_single)],
        display_names=[single_name],
        image_format=image_format,
        embed_images=False,
    )

    rel_css_href: Optional[str] = None
    if css_mode != "embed":
        style_css_path = os.path.join(os.path.dirname(dest_abs), "style.css")
        os.makedirs(os.path.dirname(style_css_path), exist_ok=True)
        with open(style_css_path, "w", encoding="utf-8") as f:
            f.write(get_default_css(custom_css_path=css))
        rel_css_href = "style.css"

    _compile_single_html_file(
        src_abs=input_abs,
        dest_abs=dest_abs,
        image_format=image_format,
        config_path=config,
        css_path=css,
        css_href=rel_css_href,
        nav_list=None,
        template_path=template,
        progress=FileBuildProgress(
            1,
            1,
            file_name=single_name,
            name_width=len(single_name),
            image_width=len(str(max(max_blocks, 0))),
        ),
        no_cache=no_cache,
        cache=cache,
    )
    return dest_abs


def build_pdf(
    inputs: Union[str, Sequence[str]],
    output: Optional[str] = None,
    page_break: bool = True,
    generate_index: bool = False,
    title: Optional[str] = None,
    css: Optional[str] = None,
    template: Optional[str] = None,
    config: Optional[str] = None,
    no_cache: bool = False,
    *,
    toc: Optional[bool] = None,
    output_path: Optional[str] = None,
    css_path: Optional[str] = None,
    template_path: Optional[str] = None,
    config_path: Optional[str] = None,
) -> str:
    """Merge one or more Markdown/HTML files or directories into a single HTML and export to PDF.

    Args:
        inputs (Union[str, Sequence[str]]): One or more input file or directory paths.
        output (Optional[str]): Destination PDF file path. Defaults to '<first_input_stem>.pdf'.
        page_break (bool): Insert CSS page breaks between merged chapters. Defaults to True.
        generate_index (bool): Generate an index (Table of Contents) between the 1st and 2nd
            documents of the PDF. Defaults to False.
        title (Optional[str]): Document title override.
        css (Optional[str]): CSS preset name or file path.
        template (Optional[str]): Jinja2 HTML template preset or file path.
        config (Optional[str]): Optional Python configuration script path.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.
        toc (Optional[bool]): Backward-compatible alias for generate_index.
        output_path (Optional[str]): Alias for output.
        css_path (Optional[str]): Alias for css.
        template_path (Optional[str]): Alias for template.
        config_path (Optional[str]): Alias for config.

    Returns:
        str: Absolute path of generated PDF file.
    """
    if toc is not None:
        generate_index = toc
    output = output or output_path
    css = css or css_path
    template = template or template_path
    config = config or config_path
    input_list: List[str] = [inputs] if isinstance(inputs, str) else list(inputs)
    if not input_list:
        raise ValueError("At least one input file or directory must be specified for build_pdf.")

    merged_html, file_list = build_merged_html(
        inputs=input_list,
        title=title,
        page_break=page_break,
        generate_index=generate_index,
        config_path=config,
        css_path=css,
        template_path=template,
        no_cache=no_cache,
    )

    if output:
        if os.path.isdir(output) or output.endswith(os.sep) or output.endswith("/"):
            first_stem = os.path.splitext(os.path.basename(file_list[0]))[0]
            dest_abs = os.path.abspath(os.path.join(output, f"{first_stem}.pdf"))
        else:
            dest_abs = os.path.abspath(output)
    else:
        first_input = os.path.abspath(input_list[0])
        if os.path.isdir(first_input):
            dir_name = os.path.basename(first_input.rstrip(os.sep)) or "document"
            dest_abs = os.path.join(os.path.dirname(first_input), f"{dir_name}.pdf")
        else:
            base_name = os.path.splitext(first_input)[0]
            dest_abs = f"{base_name}.pdf"

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    export_html_to_pdf(merged_html, dest_abs)
    return dest_abs


def build_document(
    input_path: str,
    output_path: Optional[str] = None,
    output_format: Optional[str] = None,
    image_format: str = "png",
    css_mode: str = "external",
    config_path: Optional[str] = None,
    css_path: Optional[str] = None,
    template_path: Optional[str] = None,
) -> str:
    """Compile input Markdown/HTML file or directory into HTML, PDF, or Markdown (backward-compatible wrapper)."""
    fmt = output_format.lower() if output_format else None
    if not fmt:
        if output_path and output_path.endswith(".pdf"):
            fmt = "pdf"
        elif output_path and output_path.endswith(".md"):
            fmt = "markdown"
        else:
            fmt = "html"

    if fmt == "markdown":
        return build_markdown(
            input_path=input_path,
            output=output_path,
            image_format=image_format,
            config=config_path,
        )
    if fmt == "pdf":
        return build_pdf(
            inputs=[input_path],
            output=output_path,
            css=css_path,
            template=template_path,
            config=config_path,
        )
    return build_html(
        input_path=input_path,
        output=output_path,
        image_format=image_format,
        css=css_path,
        template=template_path,
        config=config_path,
        css_mode=css_mode,
    )


def build(
    input_path: str,
    output_path: Optional[str] = None,
    output_format: Optional[str] = None,
    image_format: str = "png",
    css_mode: str = "external",
    config_path: Optional[str] = None,
    css_path: Optional[str] = None,
    template_path: Optional[str] = None,
) -> str:
    """Alias for build_document."""
    return build_document(
        input_path=input_path,
        output_path=output_path,
        output_format=output_format,
        image_format=image_format,
        css_mode=css_mode,
        config_path=config_path,
        css_path=css_path,
        template_path=template_path,
    )


def build_documents(
    input_dir: Optional[str] = None,
    output_dir: Optional[str] = None,
    output_format: str = "html",
    image_format: str = "png",
    css_mode: str = "external",
    config_path: Optional[str] = None,
    css_path: Optional[str] = None,
    template_path: Optional[str] = None,
    *,
    targets: Optional[Sequence[tuple[str, str]]] = None,
) -> List[str]:
    """Compile all documents in a directory or a list of (src, dest) target pairs."""
    if targets is not None:
        nav_list: list[dict[str, str]] = []
        for src_p, dest_p in targets:
            src_abs = os.path.abspath(src_p)
            dest_abs = os.path.abspath(dest_p)
            with open(src_abs, "r", encoding="utf-8") as f:
                content = f.read()
            nav_list.append({
                "title": _extract_title(content, os.path.basename(src_abs)),
                "src_abs": src_abs,
                "dest_abs": dest_abs,
            })

        result_paths: List[str] = []
        processor: Optional[DrawlibBlockProcessor] = None
        for src_p, dest_p in targets:
            src_abs = os.path.abspath(src_p)
            dest_abs = os.path.abspath(dest_p)
            style_css_path = os.path.join(os.path.dirname(dest_abs), "style.css")
            os.makedirs(os.path.dirname(style_css_path), exist_ok=True)
            with open(style_css_path, "w", encoding="utf-8") as f:
                f.write(get_default_css(custom_css_path=css_path))
            processor = _compile_single_html_file(
                src_abs=src_abs,
                dest_abs=dest_abs,
                image_format=image_format,
                config_path=config_path,
                css_path=css_path,
                css_href="style.css",
                nav_list=nav_list,
                template_path=template_path,
                processor=processor,
            )
            result_paths.append(dest_abs)
        return result_paths

    if not input_dir:
        raise ValueError("Either input_dir or targets must be provided to build_documents.")

    out = build_document(
        input_path=input_dir,
        output_path=output_dir,
        output_format=output_format,
        image_format=image_format,
        css_mode=css_mode,
        config_path=config_path,
        css_path=css_path,
        template_path=template_path,
    )
    return [out]


__all__ = [
    "DocType",
    "DocumentInputInfo",
    "DrawlibBlockProcessor",
    "build",
    "build_document",
    "build_documents",
    "build_html",
    "build_markdown",
    "build_merged_html",
    "build_pdf",
    "detect_document_type",
    "export_code_block",
    "export_css",
    "export_default_template",
    "export_html_css",
    "export_html_template",
    "export_pdf_css",
    "export_pdf_template",
    "export_template",
    "extract_code_blocks",
    "list_css",
    "list_html_css",
    "list_html_templates",
    "list_pdf_css",
    "list_pdf_templates",
    "list_templates",
    "show_code_block",
    "validate_template",
]
