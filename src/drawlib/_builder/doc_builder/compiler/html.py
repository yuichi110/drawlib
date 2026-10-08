# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""HTML documentation compiler for drawlib."""

from __future__ import annotations

import os
import re
import shutil
import sys
from typing import Any, Optional

from drawlib._builder._common import BuildImageCache, FileBuildProgress, resolve_styles_and_utils
from drawlib._builder.doc_builder.compiler.base import (
    copy_directory_assets,
    extract_html_body,
    extract_title,
    require_directory,
    resolve_template_and_css,
    validate_markdown_images,
)
from drawlib._builder.doc_builder.detector import detect_document_type
from drawlib._builder.doc_builder.exporter_html import render_html_document
from drawlib._builder.doc_builder.navbar import (
    NavbarSection,
    parse_navbar_markdown,
    resolve_navbar_for_page,
)
from drawlib._builder.doc_builder.parser_md import parse_markdown_to_html
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.doc_builder.progress import check_document_output_duplicates
from drawlib._slide._assets import bundle_svg_fonts
from drawlib._templates import get_html_readme


def build_html(
    input_dir: str,
    output_dir: Optional[str] = None,
    *,
    image_format: str = "png",
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    no_cache: bool = False,
    css_mode: str = "external",
) -> str:
    """Compile a Markdown/HTML documentation directory into a static HTML site or single-page document.

    When ``navbar.md`` is present (`site` project), each Markdown/HTML file is compiled
    into a corresponding HTML file with a navigation sidebar. When ``navbar.md`` is absent
    (`doc` project), all chapters are merged in filename order into a single standalone
    ``index.html`` with a Table of Contents, matching PDF compilation behavior.

    Args:
        input_dir (str): Directory containing Markdown (.md), HTML, and site assets.
        output_dir (Optional[str]): Target output directory. Defaults to input_dir.
        image_format (str): Image output format ('png' or 'webp'). Defaults to 'png'.
        styles_path (Optional[str]): Path to custom styles.py script.
        utils_path (Optional[str]): Path to custom utils.py script.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.
        css_mode (str): CSS linking mode ('external' by default, or 'embed').

    Returns:
        str: Absolute path of generated HTML output directory.

    Raises:
        ValueError: If input_dir is not a directory, required assets are missing, or output is invalid.
    """
    input_abs = require_directory(input_dir, "build_html")
    out_dir_abs = os.path.abspath(output_dir) if output_dir else input_abs

    template_file, css_file = resolve_template_and_css(input_abs)
    styles_abs, utils_abs = resolve_styles_and_utils(input_abs, styles_path, utils_path)

    navbar_candidates = [
        os.path.join(input_abs, "navbar.md"),
        os.path.join(input_abs, "navbar.markdown"),
    ]
    active_navbar_path: Optional[str] = None
    for p in navbar_candidates:
        if os.path.isfile(p):
            active_navbar_path = p
            break

    navbar_sections: Optional[list[NavbarSection]] = None
    site_title: Optional[str] = None
    if active_navbar_path:
        index_candidates = [
            os.path.join(input_abs, "index.md"),
            os.path.join(input_abs, "index.markdown"),
            os.path.join(input_abs, "index.html"),
            os.path.join(input_abs, "index.htm"),
        ]
        if not any(os.path.isfile(p) for p in index_candidates):
            raise ValueError(
                f'Directory build requires "index.md" or "index.html" at the root: "{input_abs}".'
            )
        navbar_sections, site_title = parse_navbar_markdown(active_navbar_path, input_abs)

    style_css_path: Optional[str] = None
    if css_mode != "embed":
        style_css_path = os.path.join(out_dir_abs, "style.css")
        if os.path.abspath(style_css_path) != os.path.abspath(css_file):
            os.makedirs(os.path.dirname(style_css_path), exist_ok=True)
            shutil.copyfile(css_file, style_css_path)

    cache = BuildImageCache(enabled=not no_cache)
    html_tasks: list[tuple[str, str, bool]] = []

    for root, dirnames, files in os.walk(input_abs):
        if out_dir_abs != input_abs:
            dirnames[:] = sorted(
                d
                for d in dirnames
                if not (
                    os.path.abspath(os.path.join(root, d)) == out_dir_abs
                    or os.path.abspath(os.path.join(root, d)).startswith(out_dir_abs + os.sep)
                )
            )
        else:
            dirnames.sort()
        for fname in sorted(files):
            if fname.startswith("."):
                continue
            if fname.lower() in {"readme.md", "readme.markdown", "template.html", "template.html.j2"}:
                continue
            src_abs = os.path.join(root, fname)
            if active_navbar_path and os.path.abspath(src_abs) == os.path.abspath(active_navbar_path):
                continue
            rel_path = os.path.relpath(src_abs, input_abs)

            if fname.endswith((".md", ".markdown")):
                rel_base, _ = os.path.splitext(rel_path)
                dest_abs = os.path.join(out_dir_abs, rel_base + ".html")
                html_tasks.append((src_abs, dest_abs, True))
            elif fname.endswith((".html", ".htm")):
                dest_abs = os.path.join(out_dir_abs, rel_path)
                if src_abs != dest_abs:
                    html_tasks.append((src_abs, dest_abs, False))

    if not html_tasks:
        raise ValueError(f'No Markdown or HTML documentation files found in directory "{input_abs}".')

    total_files = len(html_tasks)
    display_names = ["/" + os.path.relpath(s_abs, input_abs).replace(os.sep, "/") for s_abs, _, _ in html_tasks]
    max_blocks = check_document_output_duplicates(
        tasks=html_tasks,
        display_names=display_names,
        image_format=image_format,
        embed_images=False,
    )

    processor: Optional[DrawlibBlockProcessor] = None
    name_width = max((len(n) for n in display_names), default=0)
    image_width = len(str(max(max_blocks, 0)))
    root_index_dest_abs = os.path.join(out_dir_abs, "index.html")

    if active_navbar_path and navbar_sections is not None:
        for idx, ((src_abs, dest_abs, is_md), disp_name) in enumerate(zip(html_tasks, display_names), start=1):
            rel_css_href = (
                os.path.relpath(style_css_path, os.path.dirname(dest_abs)).replace(os.sep, "/")
                if style_css_path
                else None
            )
            rel_index_url = os.path.relpath(root_index_dest_abs, os.path.dirname(dest_abs)).replace(os.sep, "/")
            if is_md:
                cur_sections, cur_items = resolve_navbar_for_page(
                    sections=navbar_sections,
                    root_dir_abs=input_abs,
                    out_dir_abs=out_dir_abs,
                    current_src_abs=src_abs,
                    current_dest_abs=dest_abs,
                )
            else:
                cur_sections, cur_items = None, None

            processor = _compile_single_html_file(
                src_abs=src_abs,
                dest_abs=dest_abs,
                image_format=image_format,
                styles_path=styles_abs,
                utils_path=utils_abs,
                css_path=css_file,
                css_href=rel_css_href,
                template_path=template_file,
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
                nav_sections=cur_sections,
                nav_items=cur_items,
                index_url=rel_index_url,
                site_title=site_title,
                project_root=input_abs,
            )
    else:
        _compile_merged_doc_html(
            html_tasks=html_tasks,
            display_names=display_names,
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            image_format=image_format,
            styles_path=styles_abs,
            utils_path=utils_abs,
            css_path=css_file,
            css_href=("style.css" if style_css_path else None),
            template_path=template_file,
            name_width=name_width,
            image_width=image_width,
            no_cache=no_cache,
            cache=cache,
        )

    excluded: set[str] = {template_file, css_file}
    if active_navbar_path:
        excluded.add(active_navbar_path)
    copy_directory_assets(
        input_abs,
        out_dir_abs,
        excluded_files=excluded,
    )
    bundle_svg_fonts(out_dir_abs, css_file_path=style_css_path)

    readme_out = os.path.join(out_dir_abs, "README.md")
    if out_dir_abs != input_abs or not os.path.exists(readme_out):
        os.makedirs(out_dir_abs, exist_ok=True)
        with open(readme_out, "w", encoding="utf-8") as f:
            f.write(get_html_readme())

    return out_dir_abs


def _compile_merged_doc_html(
    *,
    html_tasks: list[tuple[str, str, bool]],
    display_names: list[str],
    input_abs: str,
    out_dir_abs: str,
    image_format: str,
    styles_path: Optional[str],
    utils_path: Optional[str],
    css_path: Optional[str],
    css_href: Optional[str],
    template_path: Optional[str],
    name_width: int,
    image_width: int,
    no_cache: bool,
    cache: BuildImageCache,
) -> None:
    """Compile and merge all chapters in a linear doc project into a single index.html."""
    if (
        out_dir_abs != input_abs
        and os.path.isdir(out_dir_abs)
        and not os.path.exists(os.path.join(out_dir_abs, ".git"))
    ):
        for entry in os.listdir(out_dir_abs):
            if entry.lower().endswith((".html", ".htm")) and entry.lower() != "index.html":
                stale_html = os.path.join(out_dir_abs, entry)
                if os.path.isfile(stale_html):
                    os.remove(stale_html)

    chapter_anchors: dict[str, str] = {}
    for idx, (src_abs, _, _) in enumerate(html_tasks, start=1):
        stem = os.path.splitext(os.path.basename(src_abs))[0]
        slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", stem).strip("-").lower() or f"doc-{idx}"
        anchor_id = f"chapter-{idx}-{slug}"
        chapter_anchors[src_abs] = anchor_id
        chapter_anchors[os.path.basename(src_abs)] = anchor_id
        chapter_anchors[f"{stem}.md"] = anchor_id
        chapter_anchors[f"{stem}.html"] = anchor_id

    chapters_html: list[str] = []
    toc_entries: list[tuple[str, str]] = []
    inferred_title: Optional[str] = None
    processor: Optional[DrawlibBlockProcessor] = None
    total_files = len(html_tasks)

    for idx, ((src_abs, dest_abs, _), disp_name) in enumerate(zip(html_tasks, display_names), start=1):
        progress = FileBuildProgress(
            idx,
            total_files,
            file_name=disp_name,
            name_width=name_width,
            image_width=image_width,
        )
        chapter_body, chapter_title, processor = _compile_chapter_body(
            src_abs=src_abs,
            dest_abs=dest_abs,
            image_format=image_format,
            styles_path=styles_path,
            utils_path=utils_path,
            processor=processor,
            progress=progress,
            no_cache=no_cache,
            cache=cache,
            project_root=input_abs,
        )
        if inferred_title is None:
            inferred_title = chapter_title

        anchor_id = chapter_anchors[src_abs]
        toc_entries.append((anchor_id, chapter_title))

        def _rewrite_link(match: re.Match[str], _anchors: dict[str, str] = chapter_anchors) -> str:
            href_target = match.group(1)
            base_target = os.path.basename(href_target.split("#")[0])
            if base_target in _anchors:
                return f'href="#{_anchors[base_target]}"'
            return match.group(0)

        chapter_body = re.sub(
            r'href=["\'](?!https?://|//|#)([^"\']+\.(?:md|html))(#[^"\']*)?["\']',
            _rewrite_link,
            chapter_body,
            flags=re.IGNORECASE,
        )

        chapters_html.append(f'<section id="{anchor_id}" class="doc-chapter pdf-chapter">\n{chapter_body}\n</section>')

    body_parts: list[str] = []
    index_entries = toc_entries[1:]
    if len(index_entries) > 0:
        toc_items = "\n".join(f'    <li><a href="#{anc}">{t_title}</a></li>' for anc, t_title in index_entries)
        toc_html = (
            f'<nav class="doc-toc pdf-toc">\n  <h2>Table of Contents</h2>\n  <ul>\n{toc_items}\n  </ul>\n</nav>'
        )
        body_parts.append(chapters_html[0])
        body_parts.append(toc_html)
        body_parts.extend(chapters_html[1:])
    else:
        body_parts.extend(chapters_html)

    combined_body = "\n\n".join(body_parts)
    full_html = render_html_document(
        body_html=combined_body,
        title=inferred_title or "Drawlib Document",
        custom_css_path=css_path,
        css_href=css_href,
        nav_items=[],
        nav_sections=None,
        template_path=template_path,
        index_url="index.html",
        site_title=None,
    )

    index_dest_abs = os.path.join(out_dir_abs, "index.html")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(index_dest_abs, "w", encoding="utf-8") as f:
        f.write(full_html)


def _compile_chapter_body(
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
) -> tuple[str, str, DrawlibBlockProcessor | None]:
    """Compile a single source file into an HTML body fragment and title."""
    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(src_abs, content)
    total_steps = doc_info.block_count
    if progress is not None:
        progress.update(0, total_steps, done=False)

    if doc_info.is_markdown:
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
                use_markdown_syntax=False,
                source_filename=src_abs,
                progress_callback=(progress.update if progress else None),
            )
            body_html = parse_markdown_to_html(processed_text)
            doc_title = extract_title(content, os.path.basename(src_abs))
        elif doc_info.doc_type == "html_drawlib":
            if processor is None:
                processor = DrawlibBlockProcessor(
                    styles_path=styles_path,
                    utils_path=utils_path,
                    no_cache=no_cache,
                    cache=cache,
                    project_root=project_root,
                )
            processed_text = processor.process_html(
                content,
                doc_base_name=doc_base_name,
                output_dir=output_dir,
                image_format=image_format,
                source_filename=src_abs,
                progress_callback=(progress.update if progress else None),
            )
            body_html = extract_html_body(processed_text)
            doc_title = extract_title(content, os.path.basename(src_abs))
        elif doc_info.doc_type == "markdown":
            body_html = parse_markdown_to_html(content)
            doc_title = extract_title(content, os.path.basename(src_abs))
        else:
            body_html = extract_html_body(content)
            doc_title = extract_title(content, os.path.basename(src_abs))
    finally:
        os.chdir(orig_cwd)
        if sys_path_added and src_dir in sys.path:
            sys.path.remove(src_dir)

    if progress is not None:
        progress.update(total_steps, total_steps, done=True)

    return body_html, doc_title, processor


def _compile_single_html_file(
    src_abs: str,
    dest_abs: str,
    image_format: str,
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    css_path: Optional[str] = None,
    css_href: Optional[str] = None,
    template_path: Optional[str] = None,
    processor: Optional[DrawlibBlockProcessor] = None,
    progress: Optional[FileBuildProgress] = None,
    no_cache: bool = False,
    cache: Optional[BuildImageCache] = None,
    nav_sections: Optional[list[dict[str, Any]]] = None,
    nav_items: Optional[list[dict[str, Any]]] = None,
    index_url: Optional[str] = None,
    site_title: Optional[str] = None,
    project_root: Optional[str] = None,
) -> DrawlibBlockProcessor | None:
    """Compile a single Markdown or HTML file into HTML."""
    body_html, doc_title, processor = _compile_chapter_body(
        src_abs=src_abs,
        dest_abs=dest_abs,
        image_format=image_format,
        styles_path=styles_path,
        utils_path=utils_path,
        processor=processor,
        progress=progress,
        no_cache=no_cache,
        cache=cache,
        project_root=project_root,
    )

    full_html = render_html_document(
        body_html=body_html,
        title=doc_title,
        custom_css_path=css_path,
        css_href=css_href,
        nav_items=(nav_items or []),
        nav_sections=nav_sections,
        template_path=template_path,
        index_url=(index_url or "index.html"),
        site_title=site_title,
    )

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    with open(dest_abs, "w", encoding="utf-8") as f:
        f.write(full_html)

    return processor
