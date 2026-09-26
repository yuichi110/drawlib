# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Multi-document HTML merger for drawlib build pdf."""

from __future__ import annotations

import base64
import mimetypes
import os
import re
import sys
from typing import List, Optional

from drawlib._tools.doc_builder.build_cache import BuildImageCache
from drawlib._tools.doc_builder.detector import detect_document_type
from drawlib._tools.doc_builder.exporter_html import render_pdf_document
from drawlib._tools.doc_builder.parser_md import parse_markdown_to_html
from drawlib._tools.doc_builder.processor import DrawlibBlockProcessor
from drawlib._tools.doc_builder.progress import (
    FileBuildProgress,
    check_document_output_duplicates,
    format_duplicate_output_error,
)


def _extract_title(content: str, filename: str, is_md: bool) -> str:
    """Extract document title from H1 heading or <title>/<h1> tag."""
    if is_md:
        for line in content.splitlines():
            s = line.strip()
            if s.startswith("# "):
                return s[2:].strip()
    else:
        title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.DOTALL | re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL | re.IGNORECASE)
        if h1_match:
            return re.sub(r"<[^>]+>", "", h1_match.group(1)).strip()

    base = os.path.splitext(filename)[0]
    return base.replace("_", " ").replace("-", " ").title()


def _extract_html_body(html_text: str) -> str:
    """Extract inner content of <body>...</body> if present, otherwise return html_text."""
    match = re.search(r"<body\b[^>]*>(.*?)</body>", html_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return html_text.strip()


def _inline_local_images(html_body: str, src_dir: str) -> str:
    """Convert relative <img src="..."> file references into Data URLs so merged chapters resolve assets."""
    pattern = re.compile(r'(<img\b[^>]*?\bsrc=["\'])([^"\']+)(["\'][^>]*>)', re.IGNORECASE)

    def repl(match: re.Match[str]) -> str:
        prefix, img_src, suffix = match.group(1), match.group(2).strip(), match.group(3)
        if img_src.startswith(("data:", "http://", "https://", "file://", "//")):
            return match.group(0)
        clean_ref = img_src.split("#")[0].split("?")[0]
        abs_img = os.path.abspath(os.path.join(src_dir, clean_ref))
        if not os.path.isfile(abs_img):
            return match.group(0)
        mime, _ = mimetypes.guess_type(abs_img)
        mime = mime or "image/png"
        try:
            with open(abs_img, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"{prefix}data:{mime};base64,{b64}{suffix}"
        except Exception:
            return match.group(0)

    return pattern.sub(repl, html_body)


def expand_input_files(inputs: List[str]) -> List[str]:
    """Expand a list of file and directory paths into an ordered list of Markdown/HTML file paths.

    Args:
        inputs (List[str]): Input file or directory paths.

    Returns:
        List[str]: Ordered list of absolute paths to .md and .html files.

    Raises:
        ValueError: If any input path does not exist or no valid documents are found.
    """
    collected: List[str] = []
    for item in inputs:
        abs_path = os.path.abspath(item)
        if not os.path.exists(abs_path):
            raise ValueError(f'Input path "{abs_path}" does not exist.')
        if os.path.isfile(abs_path):
            ext = os.path.splitext(abs_path)[1].lower()
            if ext not in {".md", ".markdown", ".html", ".htm"}:
                raise ValueError(f'Unsupported input file "{abs_path}". Expected .md or .html.')
            collected.append(abs_path)
        elif os.path.isdir(abs_path):
            dir_files: List[str] = []
            for root, _, files in os.walk(abs_path):
                for fname in sorted(files):
                    if fname.startswith("."):
                        continue
                    if fname.lower() in {
                        "readme.md",
                        "readme.markdown",
                        "template.html",
                        "template.html.j2",
                        "navbar.md",
                        "navbar.markdown",
                    }:
                        continue
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in {".md", ".markdown", ".html", ".htm"}:
                        dir_files.append(os.path.join(root, fname))

            dir_files.sort()
            collected.extend(dir_files)

    if not collected:
        raise ValueError("No Markdown (.md) or HTML (.html) files found in the specified inputs.")

    return collected


def build_merged_html(
    inputs: List[str],
    title: Optional[str] = None,
    page_break: bool = True,
    generate_index: bool = False,
    config_path: Optional[str] = None,
    css_path: Optional[str] = None,
    template_path: Optional[str] = None,
    no_cache: bool = False,
    *,
    toc: Optional[bool] = None,
) -> tuple[str, List[str]]:
    """Compile and merge one or more Markdown/HTML inputs into a single standalone HTML document.

    Args:
        inputs (List[str]): Ordered list of input file or directory paths.
        title (Optional[str]): Document title override. Defaults to first chapter's H1 title.
        page_break (bool): Whether to insert CSS page breaks between merged documents. Defaults to True.
        generate_index (bool): Whether to generate an index (Table of Contents) and insert it
            between the 1st and 2nd documents. Defaults to False.
        config_path (Optional[str]): Optional Python config script path.
        css_path (Optional[str]): Optional CSS preset name or file path.
        template_path (Optional[str]): Optional Jinja2 HTML template path.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.
        toc (Optional[bool]): Backward-compatible alias for generate_index.

    Returns:
        tuple[str, List[str]]: (merged_full_html_string, ordered_source_files).
    """
    if not inputs:
        raise ValueError("At least one input file or directory must be specified.")

    first_input = os.path.abspath(inputs[0])
    search_dir = first_input if os.path.isdir(first_input) else os.path.dirname(first_input)

    if template_path is None:
        t_cand = os.path.join(search_dir, "template.html")
        if not os.path.isfile(t_cand):
            raise ValueError(
                f'Missing required "template.html" in "{search_dir}". '
                'Please run "drawlib init" to initialize your project, or provide "template.html".'
            )
        template_path = t_cand

    if css_path is None:
        c_cand = os.path.join(search_dir, "style.css")
        if not os.path.isfile(c_cand):
            raise ValueError(
                f'Missing required "style.css" in "{search_dir}". '
                'Please run "drawlib init" to initialize your project, or provide "style.css".'
            )
        css_path = c_cand

    if config_path is None:
        for inp in inputs:
            inp_abs = os.path.abspath(inp)
            cand = (
                os.path.join(inp_abs, "config.py")
                if os.path.isdir(inp_abs)
                else os.path.join(os.path.dirname(inp_abs), "config.py")
            )
            if os.path.isfile(cand):
                config_path = cand
                break

    file_list = expand_input_files(inputs)
    cache = BuildImageCache(enabled=not no_cache)
    processor: Optional[DrawlibBlockProcessor] = None

    chapter_anchors: dict[str, str] = {}
    for idx, src_abs in enumerate(file_list, start=1):
        stem = os.path.splitext(os.path.basename(src_abs))[0]
        slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", stem).strip("-").lower() or f"doc-{idx}"
        anchor_id = f"chapter-{idx}-{slug}"
        chapter_anchors[src_abs] = anchor_id
        chapter_anchors[os.path.basename(src_abs)] = anchor_id
        chapter_anchors[f"{stem}.md"] = anchor_id
        chapter_anchors[f"{stem}.html"] = anchor_id

    chapters_html: List[str] = []
    toc_entries: List[tuple[str, str]] = []
    inferred_title: Optional[str] = title
    total_files = len(file_list)
    if len(inputs) == 1 and os.path.isdir(os.path.abspath(inputs[0])):
        base_root = os.path.abspath(inputs[0])
    elif len(file_list) > 1:
        common = os.path.commonpath(file_list)
        base_root = common if os.path.isdir(common) else os.path.dirname(common)
    else:
        base_root = os.path.dirname(file_list[0]) if file_list else ""
    display_names = ["/" + os.path.relpath(s_abs, base_root).replace(os.sep, "/") for s_abs in file_list]
    seen_sources: dict[str, str] = {}
    for s_abs, disp_name in zip(file_list, display_names):
        if s_abs in seen_sources:
            raise ValueError(format_duplicate_output_error(s_abs, seen_sources[s_abs], disp_name))
        seen_sources[s_abs] = disp_name
    max_blocks = check_document_output_duplicates(
        tasks=[(s_abs, "", s_abs.lower().endswith((".md", ".markdown"))) for s_abs in file_list],
        display_names=display_names,
        image_format="png",
        embed_images=False,
    )
    name_width = max((len(n) for n in display_names), default=0)
    image_width = len(str(max(max_blocks, 0)))

    for idx, (src_abs, disp_name) in enumerate(zip(file_list, display_names), start=1):
        with open(src_abs, "r", encoding="utf-8") as f:
            content = f.read()

        doc_info = detect_document_type(src_abs, content)
        total_steps = doc_info.block_count
        progress = FileBuildProgress(
            idx,
            total_files,
            file_name=disp_name,
            name_width=name_width,
            image_width=image_width,
        )
        progress.update(0, total_steps, done=False)

        src_dir = os.path.dirname(src_abs)
        doc_base_name = os.path.splitext(os.path.basename(src_abs))[0]
        chapter_title = _extract_title(content, os.path.basename(src_abs), doc_info.is_markdown)
        if inferred_title is None:
            inferred_title = chapter_title

        anchor_id = chapter_anchors[src_abs]
        toc_entries.append((anchor_id, chapter_title))

        if doc_info.has_drawlib and processor is None:
            processor = DrawlibBlockProcessor(config_path=config_path, no_cache=no_cache, cache=cache)

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
                processed_md = processor.process_markdown(
                    content,
                    doc_base_name=doc_base_name,
                    image_format="png",
                    embed_images=True,
                    source_filename=src_abs,
                    progress_callback=progress.as_callback(),
                )
                chapter_body = parse_markdown_to_html(processed_md)
            elif doc_info.doc_type == "markdown":
                chapter_body = parse_markdown_to_html(content)
            elif doc_info.doc_type == "html_drawlib":
                if processor is None:
                    processor = DrawlibBlockProcessor(config_path=config_path, no_cache=no_cache, cache=cache)
                processed_html = processor.process_html(
                    content,
                    doc_base_name=doc_base_name,
                    image_format="png",
                    embed_images=True,
                    source_filename=src_abs,
                    progress_callback=progress.as_callback(),
                )
                chapter_body = _extract_html_body(processed_html) if doc_info.is_full_html else processed_html
            else:
                chapter_body = _extract_html_body(content) if doc_info.is_full_html else content
        finally:
            os.chdir(orig_cwd)
            if sys_path_added and src_dir in sys.path:
                sys.path.remove(src_dir)

        chapter_body = _inline_local_images(chapter_body, src_dir)

        # Rewrite internal cross-file links to merged chapter anchors
        def _rewrite_link(match: re.Match[str]) -> str:
            href_target = match.group(1)
            base_target = os.path.basename(href_target.split("#")[0])
            if base_target in chapter_anchors:
                return f'href="#{chapter_anchors[base_target]}"'
            return match.group(0)

        chapter_body = re.sub(
            r'href=["\'](?!https?://|//|#)([^"\']+\.(?:md|html))(#[^"\']*)?["\']',
            _rewrite_link,
            chapter_body,
            flags=re.IGNORECASE,
        )

        break_style = ' style="page-break-before: always; break-before: page;"' if (page_break and idx > 1) else ""
        chapters_html.append(f'<section id="{anchor_id}" class="pdf-chapter"{break_style}>\n{chapter_body}\n</section>')
        progress.update(total_steps, total_steps, done=True)

    body_parts: List[str] = []
    index_entries = toc_entries[1:]
    if generate_index and len(index_entries) > 0:
        toc_items = "\n".join(f'    <li><a href="#{anc}">{t_title}</a></li>' for anc, t_title in index_entries)
        toc_break = (
            ' style="page-break-before: always; break-before: page; page-break-after: always; break-after: page;"'
            if page_break
            else ""
        )
        toc_html = (
            f'<nav class="pdf-toc"{toc_break}>\n  <h2>Table of Contents</h2>\n  <ul>\n{toc_items}\n  </ul>\n</nav>'
        )
        body_parts.append(chapters_html[0])
        body_parts.append(toc_html)
        body_parts.extend(chapters_html[1:])
    else:
        body_parts.extend(chapters_html)
    combined_body = "\n\n".join(body_parts)

    full_html = render_pdf_document(
        body_html=combined_body,
        title=inferred_title or "Drawlib Document",
        custom_css_path=css_path,
        template_path=template_path or "default",
    )

    return full_html, file_list
