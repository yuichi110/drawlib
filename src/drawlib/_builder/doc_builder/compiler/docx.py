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

from drawlib._builder._common import (
    BuildImageCache,
    ProjectManifest,
    find_project_manifest,
    load_project_manifest,
    resolve_styles_and_utils,
)
from drawlib._builder.doc_builder.compiler.base import (
    require_directory,
    resolve_doc_locale_and_root,
    resolve_multi_locale_dest,
)
from drawlib._builder.doc_builder.i18n import validate_i18n_project


def _resolve_docx_dest(default_base_dir: str, default_stem: str, output_file: str | None) -> str:
    """Resolve output .docx file path from explicit option or default directory/stem."""
    if output_file:
        if os.path.isdir(output_file) or output_file.endswith((os.sep, "/")):
            return os.path.abspath(os.path.join(output_file, f"{default_stem}.docx"))
        return os.path.abspath(output_file)
    return os.path.join(default_base_dir, f"{default_stem}.docx")


def _build_i18n_doc_docx(
    *,
    input_dir_abs: str,
    manifest: ProjectManifest,
    output_file: str | None,
    base_name: str,
    title: str | None,
    page_break: bool,
    generate_index: bool,
    dpi: int,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    timestamp: bool,
) -> str:
    """Compile all locales of a ``doc`` project into ``<base>_<lang>.docx`` files."""
    from drawlib._builder.doc_builder.exporter_docx import export_chapters_to_docx  # noqa: PLC0415

    if manifest.i18n is None:
        raise ValueError(f'Expected "[i18n]" configuration in "{input_dir_abs}/drawlib.toml".')

    validate_i18n_project(input_dir_abs, manifest.i18n, project_type="doc")
    c_cand = os.path.join(input_dir_abs, "style.css")
    css_file = c_cand if os.path.isfile(c_cand) else None
    cache = BuildImageCache(enabled=not no_cache)
    default_parent = os.path.dirname(input_dir_abs)
    generated_paths: dict[str, str] = {}

    for lang in manifest.i18n.langs:
        lang_dir_abs = os.path.join(input_dir_abs, lang)
        loc_styles, loc_utils = resolve_styles_and_utils(lang_dir_abs, styles_path, utils_path)
        dest_abs = resolve_multi_locale_dest(default_parent, base_name, output_file, lang, ".docx")
        export_chapters_to_docx(
            inputs=[lang_dir_abs],
            output_path=dest_abs,
            title=title,
            page_break=page_break,
            generate_index=generate_index,
            dpi=dpi,
            styles_path=loc_styles,
            utils_path=loc_utils,
            css_path=css_file,
            no_cache=no_cache,
            timestamp=timestamp,
            lang=lang,
            project_root=input_dir_abs,
            cache=cache,
        )
        generated_paths[lang] = dest_abs

    return generated_paths[manifest.i18n.default_lang]


def _compile_single_file_docx(
    *,
    input_abs: str,
    output_file: str | None,
    title: str | None,
    page_break: bool,
    generate_index: bool,
    dpi: int,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    timestamp: bool,
) -> str:
    """Compile a standalone Markdown file into a native MS Word (.docx) document."""
    from drawlib._builder.doc_builder.exporter_docx import export_chapters_to_docx  # noqa: PLC0415

    ext = os.path.splitext(input_abs)[1].lower()
    if ext not in {".md", ".markdown"}:
        raise ValueError(f'Unsupported input file "{input_abs}". Expected .md file for Word (.docx) export.')

    search_dir = os.path.dirname(input_abs)
    doc_lang, _, proj_root = resolve_doc_locale_and_root(input_abs)
    styles_abs, utils_abs = resolve_styles_and_utils(search_dir, styles_path, utils_path)
    css_file: str | None = None
    for cand_dir in (search_dir, proj_root):
        c_cand = os.path.join(cand_dir, "style.css")
        if os.path.isfile(c_cand):
            css_file = c_cand
            break

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
        lang=doc_lang,
        project_root=proj_root,
    )
    return dest_abs


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
    """Compile a ``doc`` project directory or standalone Markdown file into MS Word (.docx).

    For ``doc`` project directories (``[i18n]`` in ``drawlib.toml``), compiles one
    ``<base>_<lang>.docx`` per configured locale and returns the ``default_lang`` DOCX path.

    Args:
        input_path (Optional[str]): ``doc`` project directory or standalone ``.md`` file.
        output_file (Optional[str]): Destination .docx file path (or base path/directory for project builds).
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
        str: Absolute path of generated .docx file (or default-locale .docx for ``doc`` projects).

    Raises:
        ValueError: If input_path does not exist, lacks ``drawlib.toml`` for directories, or has an unsupported type.
    """
    resolved_input = input_path if input_path is not None else input_dir
    if not resolved_input:
        raise ValueError("No input directory or file specified for build_docx.")
    if not os.path.exists(resolved_input):
        raise ValueError(f'Input path "{resolved_input}" does not exist.')
    if dpi <= 0:
        raise ValueError(f"dpi must be a positive integer, got {dpi}.")

    input_abs = os.path.abspath(resolved_input)
    if os.path.isfile(input_abs):
        return _compile_single_file_docx(
            input_abs=input_abs,
            output_file=output_file,
            title=title,
            page_break=page_break,
            generate_index=generate_index,
            dpi=dpi,
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
            timestamp=timestamp,
        )

    input_dir_abs = require_directory(resolved_input, "build_docx")
    manifest = load_project_manifest(input_dir_abs)
    if manifest is None:
        found = find_project_manifest(input_dir_abs, max_up=3)
        if found is not None:
            proj_root, _ = found
            raise ValueError(
                f'Input directory "{input_dir_abs}" is a subdirectory inside project "{proj_root}". '
                f'Please pass the project root directory "{proj_root}" containing "drawlib.toml".'
            )
        raise ValueError(
            f'Missing required "drawlib.toml" in "{input_dir_abs}". '
            'Word (.docx) directory builds require a Drawlib "doc" project manifest '
            '(run "drawlib init project doc").'
        )

    if manifest.project.type == "slide":
        raise ValueError(
            f'Input directory "{input_dir_abs}" is a "slide" presentation project (drawlib.toml). '
            f'Please use "drawlib build pptx {resolved_input}" to export MS PowerPoint (.pptx) slides.'
        )
    if manifest.project.type == "site":
        raise ValueError(
            f'Input directory "{input_dir_abs}" is a multi-page "site" project (drawlib.toml). '
            'Please use "drawlib build html" instead of "drawlib build docx".'
        )
    if manifest.project.type == "images":
        raise ValueError(
            f'Input directory "{input_dir_abs}" is an "images" script project (drawlib.toml). '
            'Please use "drawlib build image" instead of "drawlib build docx".'
        )

    dir_name = os.path.basename(input_dir_abs.rstrip(os.sep))
    base_name = dir_name[:-4] if dir_name.endswith("_src") else dir_name
    if not base_name:
        base_name = "document"

    return _build_i18n_doc_docx(
        input_dir_abs=input_dir_abs,
        manifest=manifest,
        output_file=output_file,
        base_name=base_name,
        title=title,
        page_break=page_break,
        generate_index=generate_index,
        dpi=dpi,
        styles_path=styles_path,
        utils_path=utils_path,
        no_cache=no_cache,
        timestamp=timestamp,
    )
