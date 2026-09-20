# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Document compiler package for drawlib."""

import os
import re
import shutil
import sys
from typing import Optional

from drawlib._tools.doc_builder.exporter_html import get_default_css, render_html_document
from drawlib._tools.doc_builder.exporter_md import write_rendered_markdown
from drawlib._tools.doc_builder.exporter_pdf import export_html_to_pdf
from drawlib._tools.doc_builder.parser_md import parse_markdown_to_html
from drawlib._tools.doc_builder.processor import DrawlibBlockProcessor, extract_code_blocks, show_code_block
from drawlib._tools.doc_builder.template import export_default_template, validate_template


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


def _get_single_file_nav_items(doc_dir: str, active_filename: str) -> list[dict[str, object]]:
    """Build navigation items list for Markdown files in a single flat directory."""
    items: list[dict[str, object]] = []
    if not os.path.isdir(doc_dir):
        return items

    filenames = sorted(os.listdir(doc_dir))
    if "index.md" in filenames:
        filenames.remove("index.md")
        filenames.insert(0, "index.md")

    for fname in filenames:
        if fname.endswith(".md") or fname.endswith(".markdown"):
            file_path = os.path.join(doc_dir, fname)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                title = _extract_title(content, fname)
            except Exception:
                title = os.path.splitext(fname)[0].replace("_", " ").title()

            html_name = os.path.splitext(fname)[0] + ".html"
            items.append({
                "title": title,
                "url": html_name,
                "active": (fname == active_filename),
            })
    return items


def _compile_single_file(
    src_abs: str,
    dest_abs: str,
    output_format: Optional[str] = None,
    image_format: str = "png",
    config_path: Optional[str] = None,
    css_path: Optional[str] = None,
    css_href: Optional[str] = None,
    nav_list: Optional[list[dict[str, str]]] = None,
    template_path: Optional[str] = None,
) -> None:
    """Internal helper to compile a single source file to target output path."""
    fmt = output_format.lower() if output_format else None
    if not fmt:
        if dest_abs.endswith(".pdf"):
            fmt = "pdf"
        elif dest_abs.endswith(".md") or dest_abs.endswith(".markdown"):
            fmt = "markdown"
        else:
            fmt = "html"

    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    processor = DrawlibBlockProcessor(config_path=config_path)
    is_md = src_abs.endswith(".md") or src_abs.endswith(".markdown")
    if is_md:
        _validate_markdown_images(src_abs, content)
    doc_base_name = os.path.splitext(os.path.basename(dest_abs))[0]
    output_dir = os.path.dirname(dest_abs)

    if fmt == "markdown":
        rendered_md = (
            processor.process_markdown(
                content,
                doc_base_name=doc_base_name,
                output_dir=output_dir,
                image_format=image_format,
                use_markdown_syntax=True,
                source_filename=src_abs,
            )
            if is_md
            else content
        )
        write_rendered_markdown(rendered_md, dest_abs)
    elif fmt in {"html", "pdf"}:
        embed_images = fmt == "pdf"
        if is_md:
            processed_text = processor.process_markdown(
                content,
                doc_base_name=doc_base_name,
                output_dir=output_dir if not embed_images else None,
                image_format=image_format,
                embed_images=embed_images,
                source_filename=src_abs,
            )
            body_html = parse_markdown_to_html(processed_text)
        else:
            body_html = processor.process_html(
                content,
                doc_base_name=doc_base_name,
                output_dir=output_dir if not embed_images else None,
                image_format=image_format,
                embed_images=embed_images,
                source_filename=src_abs,
            )

        doc_title = _extract_title(content, os.path.basename(src_abs)) if is_md else os.path.basename(src_abs)

        if is_md and nav_list:
            doc_nav_items: list[dict[str, object]] = []
            dest_dir = os.path.dirname(dest_abs)
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
        )

        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        if fmt == "html":
            with open(dest_abs, "w", encoding="utf-8") as f:
                f.write(full_html)
        else:
            export_html_to_pdf(full_html, dest_abs)


def _build_directory(
    input_abs: str,
    output_path: Optional[str],
    output_format: Optional[str],
    image_format: str,
    css_mode: str,
    config_path: Optional[str],
    css_path: Optional[str],
    template_path: Optional[str] = None,
) -> str:
    """Internal helper to recursively process and compile a directory of documents."""
    out_dir_abs = os.path.abspath(output_path) if output_path else input_abs
    nav_list = _build_directory_nav_list(input_abs, out_dir_abs)

    if output_format == "pdf":
        actual_css_mode = "embed"
    else:
        actual_css_mode = "external" if css_mode == "auto" else css_mode

    style_css_path: Optional[str] = None
    if actual_css_mode == "external":
        style_css_path = os.path.join(out_dir_abs, "style.css")
        os.makedirs(os.path.dirname(style_css_path), exist_ok=True)
        with open(style_css_path, "w", encoding="utf-8") as f:
            f.write(get_default_css(custom_css_path=css_path))

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
                if output_format == "pdf":
                    ext = ".pdf"
                elif output_format == "markdown":
                    ext = ".md" if out_dir_abs != input_abs else ".rendered.md"
                else:
                    ext = ".html"

                dest_abs = os.path.join(out_dir_abs, rel_base + ext)

                if src_abs == dest_abs:
                    raise ValueError(
                        f'Refusing to overwrite input source file "{src_abs}". '
                        "Please specify a different output directory using -o / --output."
                    )

                rel_css_href = os.path.relpath(style_css_path, os.path.dirname(dest_abs)) if style_css_path else None

                _compile_single_file(
                    src_abs=src_abs,
                    dest_abs=dest_abs,
                    output_format=output_format,
                    image_format=image_format,
                    config_path=config_path,
                    css_path=css_path,
                    css_href=rel_css_href,
                    nav_list=nav_list,
                    template_path=template_path,
                )

            elif fname.endswith(".html"):
                dest_abs = os.path.join(out_dir_abs, rel_path)
                if src_abs == dest_abs:
                    continue

                rel_css_href = os.path.relpath(style_css_path, os.path.dirname(dest_abs)) if style_css_path else None

                _compile_single_file(
                    src_abs=src_abs,
                    dest_abs=dest_abs,
                    output_format=output_format,
                    image_format=image_format,
                    config_path=config_path,
                    css_path=css_path,
                    css_href=rel_css_href,
                    nav_list=None,
                    template_path=template_path,
                )

            else:
                if output_format == "pdf":
                    continue
                dest_abs = os.path.join(out_dir_abs, rel_path)
                if src_abs == dest_abs:
                    continue

                os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
                shutil.copy2(src_abs, dest_abs)

    return out_dir_abs


def build_document(
    input_path: str,
    output_path: Optional[str] = None,
    output_format: Optional[str] = None,
    image_format: str = "png",
    css_mode: str = "auto",
    config_path: Optional[str] = None,
    css_path: Optional[str] = None,
    template_path: Optional[str] = None,
) -> str:
    """Compile input Markdown/HTML file or directory with drawlib code blocks into HTML, PDF, or Markdown.

    Args:
        input_path (str): Path to input file (.md, .html) or directory.
        output_path (Optional[str]): Path to output file or directory.
        output_format (Optional[str]): Output format: 'html', 'pdf', or 'markdown'.
        image_format (str): Image format for code blocks: 'png', 'svg', or 'inline_svg'. Default is 'png'.
        css_mode (str): CSS styling mode: 'auto', 'embed', or 'external'. Default is 'auto'.
        config_path (Optional[str]): Path to Python config script.
        css_path (Optional[str]): Path to custom CSS file for HTML styling.
        template_path (Optional[str]): Optional path to custom Jinja2 HTML template.

    Returns:
        str: Absolute path of generated output file or directory.

    Raises:
        ValueError: If input path does not exist, or output path overwrites input source file.
    """
    input_abs = os.path.abspath(input_path)
    if not os.path.exists(input_abs):
        raise ValueError(f'Input path "{input_abs}" does not exist.')

    # Recursive directory compilation
    if os.path.isdir(input_abs):
        return _build_directory(
            input_abs=input_abs,
            output_path=output_path,
            output_format=output_format,
            image_format=image_format,
            css_mode=css_mode,
            config_path=config_path,
            css_path=css_path,
            template_path=template_path,
        )

    # Single file compilation
    fmt = output_format.lower() if output_format else None
    if not fmt:
        if output_path and output_path.endswith(".pdf"):
            fmt = "pdf"
        elif output_path and output_path.endswith(".md"):
            fmt = "markdown"
        else:
            fmt = "html"

    if output_path:
        if os.path.isdir(output_path) or output_path.endswith(os.sep) or output_path.endswith("/"):
            out_dir = os.path.abspath(output_path)
            base_name = os.path.splitext(os.path.basename(input_abs))[0]
            ext = ".pdf" if fmt == "pdf" else (".rendered.md" if fmt == "markdown" else ".html")
            dest_abs = os.path.join(out_dir, base_name + ext)
        else:
            dest_abs = os.path.abspath(output_path)
    else:
        base_name = os.path.splitext(input_abs)[0]
        ext = ".pdf" if fmt == "pdf" else (".rendered.md" if fmt == "markdown" else ".html")
        dest_abs = f"{base_name}{ext}"

    if input_abs == dest_abs:
        raise ValueError(
            f'Refusing to overwrite input source file "{input_abs}". '
            "Please specify a different output path using -o / --output."
        )

    actual_css_mode = "embed" if css_mode == "auto" else css_mode
    style_css_path: Optional[str] = None
    if actual_css_mode == "external":
        dest_dir = os.path.dirname(dest_abs)
        style_css_path = os.path.join(dest_dir, "style.css")
        os.makedirs(dest_dir, exist_ok=True)
        with open(style_css_path, "w", encoding="utf-8") as f:
            f.write(get_default_css(custom_css_path=css_path))

    rel_css_href = os.path.relpath(style_css_path, os.path.dirname(dest_abs)) if style_css_path else None

    _compile_single_file(
        src_abs=input_abs,
        dest_abs=dest_abs,
        output_format=fmt,
        image_format=image_format,
        config_path=config_path,
        css_path=css_path,
        css_href=rel_css_href,
        nav_list=None,
        template_path=template_path,
    )
    return dest_abs


def build_documents(
    targets: list[tuple[str, str] | str],
    output_dir: Optional[str] = None,
    output_format: Optional[str] = None,
    image_format: str = "png",
    css_mode: str = "auto",
    config_path: Optional[str] = None,
    css_path: Optional[str] = None,
    template_path: Optional[str] = None,
) -> list[str]:
    """Compile multiple target Markdown/HTML documents with unified navigation.

    Args:
        targets (list[tuple[str, str] | str]): List of target files or (input_path, output_path) tuples.
        output_dir (Optional[str]): Default directory for outputs if targets are single input paths.
        output_format (Optional[str]): Output format: 'html', 'pdf', or 'markdown'.
        image_format (str): Image format for code blocks: 'png', 'svg', or 'inline_svg'. Default is 'png'.
        css_mode (str): CSS styling mode: 'auto', 'embed', or 'external'. Default is 'auto'.
        config_path (Optional[str]): Path to Python config script.
        css_path (Optional[str]): Path to custom CSS file for HTML styling.
        template_path (Optional[str]): Optional path to custom Jinja2 HTML template.

    Returns:
        list[str]: List of absolute paths of generated output files.
    """
    normalized_targets: list[tuple[str, str]] = []

    for item in targets:
        if isinstance(item, tuple):
            src_abs = os.path.abspath(item[0])
            dest_abs = os.path.abspath(item[1])
        else:
            src_abs = os.path.abspath(item)
            fname = os.path.basename(src_abs)
            base_name, _ = os.path.splitext(fname)
            ext = ".pdf" if output_format == "pdf" else (".rendered.md" if output_format == "markdown" else ".html")
            if output_dir:
                dest_abs = os.path.abspath(os.path.join(output_dir, base_name + ext))
            else:
                dest_abs = os.path.abspath(os.path.join(os.path.dirname(src_abs), base_name + ext))
        normalized_targets.append((src_abs, dest_abs))

    global_nav_items: list[dict[str, str]] = []
    for src_abs, dest_abs in normalized_targets:
        if src_abs.endswith(".md") or src_abs.endswith(".markdown"):
            try:
                with open(src_abs, "r", encoding="utf-8") as f:
                    content = f.read()
                title = _extract_title(content, os.path.basename(src_abs))
            except Exception:
                title = os.path.splitext(os.path.basename(src_abs))[0].title()

            global_nav_items.append({
                "title": title,
                "src_abs": src_abs,
                "dest_abs": dest_abs,
            })

    actual_css_mode = "external" if (css_mode == "external" or (css_mode == "auto" and output_dir)) else "embed"
    style_css_path: Optional[str] = None
    if actual_css_mode == "external" and output_dir:
        out_dir_abs = os.path.abspath(output_dir)
        style_css_path = os.path.join(out_dir_abs, "style.css")
        os.makedirs(out_dir_abs, exist_ok=True)
        with open(style_css_path, "w", encoding="utf-8") as f:
            f.write(get_default_css(custom_css_path=css_path))

    compiled_paths: list[str] = []

    for src_abs, dest_abs in normalized_targets:
        if not os.path.exists(src_abs):
            raise ValueError(f'Input file "{src_abs}" does not exist.')
        if src_abs == dest_abs:
            raise ValueError(f'Refusing to overwrite input source file "{src_abs}".')

        rel_css_href = os.path.relpath(style_css_path, os.path.dirname(dest_abs)) if style_css_path else None

        _compile_single_file(
            src_abs=src_abs,
            dest_abs=dest_abs,
            output_format=output_format,
            image_format=image_format,
            config_path=config_path,
            css_path=css_path,
            css_href=rel_css_href,
            nav_list=global_nav_items if (src_abs.endswith(".md") or src_abs.endswith(".markdown")) else None,
            template_path=template_path,
        )
        compiled_paths.append(dest_abs)

    return compiled_paths


build = build_document


__all__ = [
    "build",
    "build_document",
    "build_documents",
    "export_default_template",
    "extract_code_blocks",
    "show_code_block",
    "validate_template",
    "DrawlibBlockProcessor",
    "parse_markdown_to_html",
    "render_html_document",
]
