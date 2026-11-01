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

from drawlib._builder._common import BuildImageCache, load_project_manifest, resolve_styles_and_utils
from drawlib._builder.doc_builder.compiler.base import (
    require_directory,
    resolve_doc_locale_and_root,
    resolve_multi_locale_dest,
    resolve_template_and_css,
)
from drawlib._builder.doc_builder.exporter_pdf import export_html_to_pdf
from drawlib._builder.doc_builder.i18n import validate_i18n_project
from drawlib._builder.doc_builder.merger import build_merged_html


def _is_slide_project_dir(input_abs: str) -> bool:
    """Return True if input_abs is a slide presentation source directory."""
    if not os.path.isdir(input_abs):
        return False
    manifest = load_project_manifest(input_abs)
    if manifest is not None:
        return manifest.project.type == "slide"
    if os.path.isfile(os.path.join(input_abs, "slide.css")):
        return True
    style_css = os.path.join(input_abs, "style.css")
    if os.path.isfile(style_css):
        try:
            with open(style_css, "r", encoding="utf-8") as f:
                css_text = f.read()
            if (
                "--slide-width" in css_text
                or ".presentation-stage" in css_text
                or "1920px 1080px" in css_text
                or "16in 9in" in css_text
            ):
                return True
        except OSError:
            pass
    build_html_sh = os.path.join(input_abs, "build_html.sh")
    if os.path.isfile(build_html_sh):
        try:
            with open(build_html_sh, "r", encoding="utf-8") as f:
                if "build slide" in f.read():
                    return True
        except OSError:
            pass
    return False


def _build_i18n_doc_pdfs(
    *,
    input_dir_abs: str,
    output_file: str | None,
    base_name: str,
    title: str | None,
    page_break: bool,
    generate_index: bool,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    timestamp: bool,
) -> str:
    """Compile all locales of a multi-language ``doc`` project into ``<base>_<lang>.pdf`` files."""
    manifest = load_project_manifest(input_dir_abs)
    if manifest is None or manifest.i18n is None:
        raise ValueError(f'Expected multi-locale drawlib.toml in "{input_dir_abs}".')

    validate_i18n_project(input_dir_abs, manifest.i18n, project_type="doc")
    template_file, css_file = resolve_template_and_css(input_dir_abs)
    cache = BuildImageCache(enabled=not no_cache)
    default_parent = os.path.dirname(input_dir_abs)
    generated_paths: dict[str, str] = {}

    for lang in manifest.i18n.langs:
        lang_dir_abs = os.path.join(input_dir_abs, lang)
        loc_styles, loc_utils = resolve_styles_and_utils(lang_dir_abs, styles_path, utils_path)
        merged_html, _ = build_merged_html(
            inputs=[lang_dir_abs],
            title=title,
            page_break=page_break,
            generate_index=generate_index,
            styles_path=loc_styles,
            utils_path=loc_utils,
            css_path=css_file,
            template_path=template_file,
            no_cache=no_cache,
            lang=lang,
            project_root=input_dir_abs,
            cache=cache,
        )
        dest_abs = resolve_multi_locale_dest(default_parent, base_name, output_file, lang, ".pdf")
        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        export_html_to_pdf(merged_html, dest_abs, timestamp=timestamp)
        generated_paths[lang] = dest_abs

    return generated_paths[manifest.i18n.default_lang]


def build_pdf(
    input_path: str | None = None,
    output_file: str | None = None,
    *,
    input_dir: str | None = None,
    title: str | None = None,
    page_break: bool = True,
    generate_index: bool = False,
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    timestamp: bool = False,
) -> str:
    """Merge Markdown chapters, single Markdown file, or slide deck into a print-ready vector PDF.

    For multi-language ``doc`` projects (``[i18n]`` in ``drawlib.toml``), compiles one
    ``<base>_<lang>.pdf`` per configured locale and returns the ``default_lang`` PDF path.

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
        str: Absolute path of generated PDF file (or default-locale PDF for multi-locale doc projects).

    Raises:
        ValueError: If input_path does not exist or has an unsupported format.
    """
    resolved_input = input_path if input_path is not None else input_dir
    if not resolved_input:
        raise ValueError("No input directory or file specified for build_pdf.")
    if not os.path.exists(resolved_input):
        raise ValueError(f'Input path "{resolved_input}" does not exist.')

    input_abs = os.path.abspath(resolved_input)
    direct_manifest = load_project_manifest(input_abs) if os.path.isdir(input_abs) else None
    if direct_manifest is not None:
        if direct_manifest.project.type == "site":
            raise ValueError(
                f'Input directory "{input_abs}" is a multi-page "site" project (drawlib.toml). '
                'Please use "drawlib build html" instead of "drawlib build pdf".'
            )
        if direct_manifest.project.type == "images":
            raise ValueError(
                f'Input directory "{input_abs}" is an "images" script project (drawlib.toml). '
                'Please use "drawlib build image" instead of "drawlib build pdf".'
            )

    # 1. Slide presentation project directory
    if _is_slide_project_dir(input_abs):
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
        eff_slide_title = title or (
            direct_manifest.project.title if direct_manifest and direct_manifest.project.title else None
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            index_html = build_slide(
                input_dir=input_abs,
                output_dir=tmp_dir,
                title=eff_slide_title,
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
        doc_lang, _, proj_root = resolve_doc_locale_and_root(input_abs)
        styles_abs, utils_abs = resolve_styles_and_utils(search_dir, styles_path, utils_path)
        template_file: str | None = None
        css_file: str | None = None
        for cand_dir in (search_dir, proj_root):
            if template_file is None and os.path.isfile(os.path.join(cand_dir, "template.html")):
                template_file = os.path.join(cand_dir, "template.html")
            if css_file is None and os.path.isfile(os.path.join(cand_dir, "style.css")):
                css_file = os.path.join(cand_dir, "style.css")

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
            lang=doc_lang,
            project_root=proj_root,
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
    dir_name = os.path.basename(input_dir_abs.rstrip(os.sep))
    base_name = dir_name[:-4] if dir_name.endswith("_src") else dir_name
    if not base_name:
        base_name = "document"

    if direct_manifest is not None and direct_manifest.i18n is not None:
        return _build_i18n_doc_pdfs(
            input_dir_abs=input_dir_abs,
            output_file=output_file,
            base_name=base_name,
            title=title,
            page_break=page_break,
            generate_index=generate_index,
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
            timestamp=timestamp,
        )

    doc_lang, _, proj_root = resolve_doc_locale_and_root(input_dir_abs)
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
        lang=doc_lang,
        project_root=proj_root,
    )

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
