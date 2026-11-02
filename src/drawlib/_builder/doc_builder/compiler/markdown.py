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
from typing import Literal

from drawlib._builder._common import (
    BuildImageCache,
    FileBuildProgress,
    find_project_manifest,
    load_project_manifest,
    resolve_styles_and_utils,
)
from drawlib._builder.doc_builder.compiler.base import (
    copy_directory_assets,
    require_directory,
    validate_markdown_images,
    validate_markdown_links,
)
from drawlib._builder.doc_builder.detector import detect_document_type
from drawlib._builder.doc_builder.exporter_md import write_rendered_markdown
from drawlib._builder.doc_builder.i18n import (
    I18nConfig,
    rebase_markdown_relative_urls,
    validate_i18n_project,
)
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.doc_builder.progress import check_document_output_duplicates


def _resolve_default_markdown_out_dir(input_abs: str, output_dir: str | None) -> str:
    """Resolve output Markdown directory path, defaulting to ``<parent>/<base>_markdown``."""
    if output_dir:
        return os.path.abspath(output_dir)
    dir_name = os.path.basename(input_abs.rstrip(os.sep))
    base_name = dir_name[:-4] if dir_name.endswith("_src") and len(dir_name) > 4 else (dir_name or "docs")
    return os.path.join(os.path.dirname(input_abs), f"{base_name}_markdown")


def build_markdown(
    input_dir: str,
    output_dir: str | None = None,
    *,
    image_format: str = "png",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
) -> str:
    """Compile an i18n-native ``site`` or ``doc`` directory into rendered Markdown.

    Args:
        input_dir (str): Project root directory containing ``drawlib.toml`` and ``<lang>/`` folders.
        output_dir (Optional[str]): Target output directory. Defaults to ``<base>_markdown``.
        image_format (str): Image output format ('png' or 'webp'). Defaults to 'png'.
        styles_path (Optional[str]): Path to custom styles.py script.
        utils_path (Optional[str]): Path to custom utils.py script.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.

    Returns:
        str: Absolute path of generated Markdown output directory.

    Raises:
        ValueError: If input_dir is not a valid ``doc`` or ``site`` project root directory or output overwrites source.
    """
    input_abs = require_directory(input_dir, "build_markdown")
    out_dir_abs = _resolve_default_markdown_out_dir(input_abs, output_dir)

    if out_dir_abs == input_abs:
        raise ValueError(
            f'Refusing to overwrite input source directory "{input_abs}". Please specify a different output directory.'
        )

    manifest = load_project_manifest(input_abs)
    if manifest is None:
        found = find_project_manifest(input_abs, max_up=3)
        if found is not None:
            proj_root, _ = found
            raise ValueError(
                f'Input directory "{input_abs}" is a subdirectory inside project "{proj_root}". '
                f'Please pass the project root directory "{proj_root}" containing "drawlib.toml".'
            )
        raise ValueError(
            f'Missing required "drawlib.toml" in "{input_abs}". '
            "Markdown directory builds require a Drawlib project manifest "
            '(run "drawlib init project site" or "drawlib init project doc").'
        )

    if manifest.project.type == "slide":
        raise ValueError(
            f'Input directory "{input_abs}" is a "slide" presentation project (drawlib.toml). '
            'Please use "drawlib build slide" instead of "drawlib build markdown".'
        )
    if manifest.project.type == "images":
        raise ValueError(
            f'Input directory "{input_abs}" is an "images" script project (drawlib.toml). '
            'Please use "drawlib build image" instead of "drawlib build markdown".'
        )
    if manifest.i18n is None:
        raise ValueError(f'Invalid "{input_abs}/drawlib.toml": "[i18n]" configuration is required.')

    proj_type: Literal["site", "doc"] = "doc" if manifest.project.type == "doc" else "site"
    return _build_i18n_markdown(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        i18n_cfg=manifest.i18n,
        project_type=proj_type,
        image_format=image_format,
        styles_path=styles_path,
        utils_path=utils_path,
        no_cache=no_cache,
    )


def _find_locale_index_md(lang_dir_abs: str) -> str | None:
    """Return absolute path to index.md / index.markdown inside a locale directory if present."""
    for cand_name in ("index.md", "index.markdown"):
        cand = os.path.join(lang_dir_abs, cand_name)
        if os.path.isfile(cand):
            return cand
    return None


def _build_i18n_markdown_tasks(
    input_abs: str,
    out_dir_abs: str,
    ordered_langs: list[str],
    locale_files: dict[str, list[str]],
    image_format: str,
) -> tuple[list[tuple[str, str, str, str]], list[str], int]:
    """Build ordered (lang, src_abs, dest_abs, shared_dir) tasks across locales and validate duplicates."""
    all_tasks: list[tuple[str, str, str, str]] = []
    display_names: list[str] = []
    max_blocks = 0

    for lang in ordered_langs:
        lang_tasks: list[tuple[str, str, bool]] = []
        lang_disp: list[str] = []
        lang_shared_dirs: list[str | None] = []
        for rel_path in locale_files[lang]:
            if not rel_path.lower().endswith((".md", ".markdown")):
                continue
            src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
            dest_abs = os.path.join(out_dir_abs, lang, *rel_path.split("/"))
            rel_stem, _ = os.path.splitext(rel_path)
            shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
            disp = f"/{lang}/{rel_path}"

            all_tasks.append((lang, src_abs, dest_abs, shared_dir))
            display_names.append(disp)
            lang_tasks.append((src_abs, dest_abs, True))
            lang_disp.append(disp)
            lang_shared_dirs.append(shared_dir)

        loc_max = check_document_output_duplicates(
            tasks=lang_tasks,
            display_names=lang_disp,
            image_format=image_format,
            embed_images=False,
            shared_images_dirs=lang_shared_dirs,
        )
        max_blocks = max(max_blocks, loc_max)

    return all_tasks, display_names, max_blocks


def _build_i18n_markdown(
    *,
    input_abs: str,
    out_dir_abs: str,
    i18n_cfg: I18nConfig,
    project_type: Literal["site", "doc"],
    image_format: str,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
) -> str:
    """Compile a multi-locale (i18n) site or doc directory into rendered Markdown."""
    locale_files = validate_i18n_project(
        input_abs,
        i18n_cfg,
        project_type=project_type,
        default_format=image_format,
    )

    default_lang = i18n_cfg.default_lang
    ordered_langs = [default_lang] + [lc for lc in i18n_cfg.langs if lc != default_lang]
    locale_styles_utils: dict[str, tuple[str | None, str | None]] = {
        lang: resolve_styles_and_utils(os.path.join(input_abs, lang), styles_path, utils_path) for lang in ordered_langs
    }

    all_tasks, display_names, max_blocks = _build_i18n_markdown_tasks(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        ordered_langs=ordered_langs,
        locale_files=locale_files,
        image_format=image_format,
    )

    def_index_src = _find_locale_index_md(os.path.join(input_abs, default_lang)) if project_type == "site" else None
    extra_names = [*display_names, "/index.md"] if def_index_src else display_names
    total_files = len(extra_names)
    name_width = max((len(n) for n in extra_names), default=0)
    image_width = len(str(max(max_blocks, 0)))

    cache = BuildImageCache(enabled=not no_cache)
    processors_by_cfg: dict[tuple[str | None, str | None], DrawlibBlockProcessor | None] = {}

    for idx, ((lang, src_abs, dest_abs, shared_dir), disp_name) in enumerate(zip(all_tasks, display_names), start=1):
        loc_styles, loc_utils = locale_styles_utils[lang]
        cfg_key = (loc_styles, loc_utils)
        proc = _compile_single_markdown_file(
            src_abs=src_abs,
            dest_abs=dest_abs,
            image_format=image_format,
            styles_path=loc_styles,
            utils_path=loc_utils,
            processor=processors_by_cfg.get(cfg_key),
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
            shared_images_dir=shared_dir,
        )
        processors_by_cfg[cfg_key] = proc

    if def_index_src is not None:
        def_styles, def_utils = locale_styles_utils[default_lang]
        def_cfg_key = (def_styles, def_utils)
        _compile_single_markdown_file(
            src_abs=def_index_src,
            dest_abs=os.path.join(out_dir_abs, "index.md"),
            image_format=image_format,
            styles_path=def_styles,
            utils_path=def_utils,
            processor=processors_by_cfg.get(def_cfg_key),
            progress=FileBuildProgress(
                total_files,
                total_files,
                file_name="/index.md",
                name_width=name_width,
                image_width=image_width,
            ),
            no_cache=no_cache,
            cache=cache,
            project_root=input_abs,
            shared_images_dir=os.path.join(out_dir_abs, "images", "index"),
            rebase_from_dir=os.path.join(out_dir_abs, default_lang),
        )

    copy_directory_assets(input_abs, out_dir_abs)
    return out_dir_abs


def _compile_single_markdown_file(
    src_abs: str,
    dest_abs: str,
    image_format: str,
    styles_path: str | None = None,
    utils_path: str | None = None,
    processor: DrawlibBlockProcessor | None = None,
    progress: FileBuildProgress | None = None,
    no_cache: bool = False,
    cache: BuildImageCache | None = None,
    project_root: str | None = None,
    shared_images_dir: str | None = None,
    rebase_from_dir: str | None = None,
) -> DrawlibBlockProcessor | None:
    """Compile a single Markdown file with drawlib blocks into rendered Markdown."""
    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(src_abs, content)
    total_steps = doc_info.block_count
    if progress is not None:
        progress.update(0, total_steps, done=False)

    validate_markdown_links(src_abs, content)
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
                shared_images_dir=shared_images_dir,
            )
            rendered_content = processed_text
        else:
            rendered_content = content

        if rebase_from_dir is not None:
            rendered_content = rebase_markdown_relative_urls(
                markdown_text=rendered_content,
                from_dir=rebase_from_dir,
                to_dir=output_dir,
            )

        write_rendered_markdown(rendered_content, dest_abs)
    finally:
        os.chdir(orig_cwd)
        if sys_path_added and src_dir in sys.path:
            sys.path.remove(src_dir)

    if progress is not None:
        progress.update(total_steps, total_steps, done=True)

    return processor
