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

from drawlib._tools.doc_builder.detector import detect_document_type
from drawlib._tools.doc_builder.exporter_html import render_html_document
from drawlib._tools.doc_builder.parser_md import parse_markdown_to_html
from drawlib._tools.doc_builder.processor import DrawlibBlockProcessor


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
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in {".md", ".markdown", ".html", ".htm"}:
                        dir_files.append(os.path.join(root, fname))

            def _sort_key(p: str) -> tuple[int, str]:
                base = os.path.basename(p).lower()
                if base in {"index.md", "index.markdown", "index.html", "index.htm"}:
                    return (0, p)
                return (1, p)

            dir_files.sort(key=_sort_key)
            collected.extend(dir_files)

    if not collected:
        raise ValueError("No Markdown (.md) or HTML (.html) files found in the specified inputs.")

    return collected


def build_merged_html(
    inputs: List[str],
    title: Optional[str] = None,
    page_break: bool = True,
    toc: bool = False,
    config_path: Optional[str] = None,
    css_path: Optional[str] = None,
    template_path: Optional[str] = None,
) -> tuple[str, List[str]]:
    """Compile and merge one or more Markdown/HTML inputs into a single standalone HTML document.

    Args:
        inputs (List[str]): Ordered list of input file or directory paths.
        title (Optional[str]): Document title override. Defaults to first chapter's H1 title.
        page_break (bool): Whether to insert CSS page breaks between merged documents. Defaults to True.
        toc (bool): Whether to generate a Table of Contents at the start of the merged document. Defaults to False.
        config_path (Optional[str]): Optional Python config script path.
        css_path (Optional[str]): Optional CSS preset name or file path.
        template_path (Optional[str]): Optional Jinja2 HTML template path.

    Returns:
        tuple[str, List[str]]: (merged_full_html_string, ordered_source_files).
    """
    file_list = expand_input_files(inputs)
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

    for idx, src_abs in enumerate(file_list, start=1):
        with open(src_abs, "r", encoding="utf-8") as f:
            content = f.read()

        doc_info = detect_document_type(src_abs, content)
        src_dir = os.path.dirname(src_abs)
        doc_base_name = os.path.splitext(os.path.basename(src_abs))[0]
        chapter_title = _extract_title(content, os.path.basename(src_abs), doc_info.is_markdown)
        if inferred_title is None:
            inferred_title = chapter_title

        anchor_id = chapter_anchors[src_abs]
        toc_entries.append((anchor_id, chapter_title))

        if doc_info.has_drawlib and processor is None:
            processor = DrawlibBlockProcessor(config_path=config_path)

        orig_cwd = os.getcwd()
        sys_path_added = False
        try:
            os.chdir(src_dir)
            if src_dir not in sys.path:
                sys.path.insert(0, src_dir)
                sys_path_added = True

            if doc_info.doc_type == "markdown_drawlib":
                if processor is None:
                    processor = DrawlibBlockProcessor(config_path=config_path)
                processed_md = processor.process_markdown(
                    content,
                    doc_base_name=doc_base_name,
                    image_format="png",
                    embed_images=True,
                    source_filename=src_abs,
                )
                chapter_body = parse_markdown_to_html(processed_md)
            elif doc_info.doc_type == "markdown":
                chapter_body = parse_markdown_to_html(content)
            elif doc_info.doc_type == "html_drawlib":
                if processor is None:
                    processor = DrawlibBlockProcessor(config_path=config_path)
                processed_html = processor.process_html(
                    content,
                    doc_base_name=doc_base_name,
                    image_format="png",
                    embed_images=True,
                    source_filename=src_abs,
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

    body_parts: List[str] = []
    if toc and len(toc_entries) > 0:
        toc_items = "\n".join(
            f'    <li><a href="#{anc}">{t_title}</a></li>' for anc, t_title in toc_entries
        )
        toc_break = ' style="page-break-after: always; break-after: page;"' if page_break else ""
        body_parts.append(
            f'<nav class="pdf-toc"{toc_break}>\n  <h2>Table of Contents</h2>\n  <ul>\n{toc_items}\n  </ul>\n</nav>'
        )

    body_parts.extend(chapters_html)
    combined_body = "\n\n".join(body_parts)

    full_html = render_html_document(
        body_html=combined_body,
        title=inferred_title or "Drawlib Document",
        custom_css_path=css_path,
        css_href=None,
        nav_items=[],
        template_path=template_path or "simple",
    )

    return full_html, file_list
