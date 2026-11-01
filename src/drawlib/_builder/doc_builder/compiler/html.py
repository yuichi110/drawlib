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
from typing import Any

from drawlib._builder._common import BuildImageCache, FileBuildProgress, load_project_manifest, resolve_styles_and_utils
from drawlib._builder.doc_builder.compiler.base import (
    copy_directory_assets,
    extract_html_body,
    extract_title,
    require_directory,
    resolve_doc_locale_and_root,
    resolve_template_and_css,
    validate_markdown_images,
    validate_markdown_links,
)
from drawlib._builder.doc_builder.detector import detect_document_type
from drawlib._builder.doc_builder.exporter_html import render_html_document
from drawlib._builder.doc_builder.i18n import (
    I18nConfig,
    build_language_switcher_context,
    rebase_html_relative_urls,
    resolve_locale_navbar_path,
    validate_i18n_project,
    validate_i18n_site,
)
from drawlib._builder.doc_builder.navbar import (
    NavbarSection,
    parse_navbar_markdown,
    resolve_navbar_for_page,
)
from drawlib._builder.doc_builder.parser_md import parse_markdown_to_html
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.doc_builder.progress import check_document_output_duplicates
from drawlib._slide._assets import bundle_svg_fonts
from drawlib._templates import get_html_readme, localize_css_for_language
from drawlib._templates.langs import get_language_config


def resolve_favicon_href(input_abs: str, out_dir_abs: str, dest_abs: str) -> str | None:
    """Resolve relative href to favicon for a given output HTML file."""
    for sub in ("_assets", "assets", ""):
        for fav_name in ("favicon.png", "favicon.ico", "favicon.svg"):
            src_fav = os.path.join(input_abs, sub, fav_name) if sub else os.path.join(input_abs, fav_name)
            dst_fav = os.path.join(out_dir_abs, sub, fav_name) if sub else os.path.join(out_dir_abs, fav_name)
            if os.path.isfile(src_fav) or os.path.isfile(dst_fav):
                return os.path.relpath(dst_fav, os.path.dirname(dest_abs)).replace(os.sep, "/")
    return None


def resolve_logo_hrefs(input_abs: str, out_dir_abs: str, dest_abs: str) -> tuple[str | None, str | None]:
    """Resolve relative hrefs to logo.png and logo_dark.png for a given output HTML file if present in source."""
    for sub in ("_assets", "assets", ""):
        for logo_name in ("logo.png", "logo.svg"):
            src_logo = os.path.join(input_abs, sub, logo_name) if sub else os.path.join(input_abs, logo_name)
            dst_logo = os.path.join(out_dir_abs, sub, logo_name) if sub else os.path.join(out_dir_abs, logo_name)
            if os.path.isfile(src_logo):
                logo_href = os.path.relpath(dst_logo, os.path.dirname(dest_abs)).replace(os.sep, "/")

                logo_dark_href: str | None = None
                for dark_name in ("logo_dark.png", "logo_dark.svg"):
                    src_dark = os.path.join(input_abs, sub, dark_name) if sub else os.path.join(input_abs, dark_name)
                    dst_dark = (
                        os.path.join(out_dir_abs, sub, dark_name) if sub else os.path.join(out_dir_abs, dark_name)
                    )
                    if os.path.isfile(src_dark):
                        logo_dark_href = os.path.relpath(dst_dark, os.path.dirname(dest_abs)).replace(os.sep, "/")
                        break
                if not logo_dark_href:
                    logo_dark_href = logo_href
                return logo_href, logo_dark_href
    return None, None


def build_html(
    input_dir: str,
    output_dir: str | None = None,
    *,
    image_format: str = "png",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    css_mode: str = "external",
) -> str:
    """Compile a Markdown/HTML documentation directory into a static HTML site or single-page document.

    When ``drawlib.toml`` contains ``[i18n]``, builds a multi-locale ``site`` or ``doc`` with
    shared diagram deduplication, per-locale stylesheets, language switcher navigation, and a
    root default-language ``index.html``.
    For single-language projects, ``drawlib.toml`` ``[project].type`` takes priority over file
    heuristics (``navbar.md`` presence for ``site`` vs merged ``index.html`` with Table of
    Contents for ``doc``).

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

    manifest = load_project_manifest(input_abs)
    if manifest is not None:
        if manifest.project.type == "slide":
            raise ValueError(
                f'Input directory "{input_abs}" is a "slide" presentation project (drawlib.toml). '
                'Please use "drawlib build slide" instead of "drawlib build html".'
            )
        if manifest.project.type == "images":
            raise ValueError(
                f'Input directory "{input_abs}" is an "images" script project (drawlib.toml). '
                'Please use "drawlib build image" instead of "drawlib build html".'
            )
        if manifest.i18n is not None:
            if manifest.project.type == "doc":
                return _build_i18n_doc_html(
                    input_abs=input_abs,
                    out_dir_abs=out_dir_abs,
                    i18n_cfg=manifest.i18n,
                    image_format=image_format,
                    styles_path=styles_path,
                    utils_path=utils_path,
                    no_cache=no_cache,
                    css_mode=css_mode,
                )
            return _build_i18n_html(
                input_abs=input_abs,
                out_dir_abs=out_dir_abs,
                i18n_cfg=manifest.i18n,
                image_format=image_format,
                styles_path=styles_path,
                utils_path=utils_path,
                no_cache=no_cache,
                css_mode=css_mode,
            )

    if manifest is not None:
        doc_lang = manifest.effective_lang
        project_root_abs = input_abs
        manifest_type: str | None = manifest.project.type
        manifest_title = manifest.project.title or None
    else:
        doc_lang, parent_manifest, project_root_abs = resolve_doc_locale_and_root(input_abs)
        manifest_type = parent_manifest.project.type if parent_manifest is not None else None
        manifest_title = (parent_manifest.project.title or None) if parent_manifest is not None else None

    template_file, css_file = resolve_template_and_css(input_abs)
    styles_abs, utils_abs = resolve_styles_and_utils(input_abs, styles_path, utils_path)

    navbar_candidates = [
        os.path.join(input_abs, "navbar.md"),
        os.path.join(input_abs, "navbar.markdown"),
    ]
    active_navbar_path: str | None = None
    for p in navbar_candidates:
        if os.path.isfile(p):
            active_navbar_path = p
            break

    is_site = (manifest_type == "site") if manifest_type is not None else (active_navbar_path is not None)

    navbar_sections: list[NavbarSection] | None = None
    site_title: str | None = None
    if is_site:
        if active_navbar_path is None:
            raise ValueError(f'Site project "{input_abs}" requires "navbar.md" at the root.')
        index_candidates = [
            os.path.join(input_abs, "index.md"),
            os.path.join(input_abs, "index.markdown"),
            os.path.join(input_abs, "index.html"),
            os.path.join(input_abs, "index.htm"),
        ]
        if not any(os.path.isfile(p) for p in index_candidates):
            raise ValueError(f'Directory build requires "index.md" or "index.html" at the root: "{input_abs}".')
        navbar_sections, site_title = parse_navbar_markdown(active_navbar_path, input_abs)
        if site_title is None and manifest_title:
            site_title = manifest_title

    style_css_path: str | None = None
    if css_mode != "embed":
        style_css_path = os.path.join(out_dir_abs, "style.css")
        if os.path.abspath(style_css_path) != os.path.abspath(css_file):
            os.makedirs(os.path.dirname(style_css_path), exist_ok=True)
            with open(css_file, "r", encoding="utf-8") as cf:
                raw_css = cf.read()
            with open(style_css_path, "w", encoding="utf-8") as out_cf:
                out_cf.write(localize_css_for_language(raw_css, lang=doc_lang))

    cache = BuildImageCache(enabled=not no_cache)
    html_tasks: list[tuple[str, str, bool]] = []

    for root, dirnames, files in os.walk(input_abs):
        if out_dir_abs != input_abs:
            dirnames[:] = sorted(
                d
                for d in dirnames
                if not d.startswith(".")
                and not d.startswith("_")
                and not (
                    os.path.abspath(os.path.join(root, d)) == out_dir_abs
                    or os.path.abspath(os.path.join(root, d)).startswith(out_dir_abs + os.sep)
                )
            )
        else:
            dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and not d.startswith("_"))
        for fname in sorted(files):
            if fname.startswith(".") or fname.startswith("_"):
                continue
            if fname.lower() in {
                "readme.md",
                "readme.markdown",
                "output_readme.md",
                "output_html_readme.md",
                "template.html",
                "template.html.j2",
                "drawlib.toml",
            }:
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

    processor: DrawlibBlockProcessor | None = None
    name_width = max((len(n) for n in display_names), default=0)
    image_width = len(str(max(max_blocks, 0)))
    root_index_dest_abs = os.path.join(out_dir_abs, "index.html")
    lang_cfg = get_language_config(doc_lang)

    if is_site and active_navbar_path and navbar_sections is not None:
        for idx, ((src_abs, dest_abs, is_md), disp_name) in enumerate(zip(html_tasks, display_names), start=1):
            rel_css_href = (
                os.path.relpath(style_css_path, os.path.dirname(dest_abs)).replace(os.sep, "/")
                if style_css_path
                else None
            )
            rel_index_url = os.path.relpath(root_index_dest_abs, os.path.dirname(dest_abs)).replace(os.sep, "/")
            rel_favicon_href = resolve_favicon_href(project_root_abs, out_dir_abs, dest_abs)
            rel_logo_href, rel_logo_dark_href = resolve_logo_hrefs(project_root_abs, out_dir_abs, dest_abs)
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
                project_root=project_root_abs,
                favicon_href=rel_favicon_href,
                logo_href=rel_logo_href,
                logo_dark_href=rel_logo_dark_href,
                html_lang=lang_cfg.code,
                html_dir=lang_cfg.direction,
                font_link_html=lang_cfg.font_link_html,
                css_lang=doc_lang,
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
            lang=doc_lang,
            project_root=project_root_abs,
        )

    excluded: set[str] = {template_file, css_file}
    if active_navbar_path:
        excluded.add(active_navbar_path)
    copy_directory_assets(
        project_root_abs if project_root_abs != input_abs else input_abs,
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


def _find_locale_index_src(lang_dir_abs: str) -> str:
    """Return absolute path to index.md or index.html inside a locale directory."""
    for cand_name in ("index.md", "index.markdown", "index.html", "index.htm"):
        cand = os.path.join(lang_dir_abs, cand_name)
        if os.path.isfile(cand):
            return cand
    raise ValueError(f'Multi-locale site requires "index.md" or "index.html" inside "{lang_dir_abs}".')


def _prepare_i18n_locales_metadata(
    input_abs: str,
    out_dir_abs: str,
    ordered_langs: list[str],
    css_file: str,
    css_mode: str,
) -> tuple[dict[str, tuple[list[NavbarSection], str | None]], dict[str, str | None]]:
    """Parse per-locale navbars and generate localized <lang>/style.css stylesheets."""
    locale_navbars: dict[str, tuple[list[NavbarSection], str | None]] = {}
    locale_css_paths: dict[str, str | None] = {}
    raw_css = ""
    if css_mode != "embed":
        with open(css_file, "r", encoding="utf-8") as cf:
            raw_css = cf.read()

    for lang in ordered_langs:
        lang_dir = os.path.join(input_abs, lang)
        _find_locale_index_src(lang_dir)
        nav_path = resolve_locale_navbar_path(lang_dir)
        if nav_path is None:
            raise ValueError(f'Multi-locale site requires "navbar.md" inside "{lang_dir}".')
        locale_navbars[lang] = parse_navbar_markdown(nav_path, lang_dir)

        if css_mode != "embed":
            lang_css_out = os.path.join(out_dir_abs, lang, "style.css")
            os.makedirs(os.path.dirname(lang_css_out), exist_ok=True)
            with open(lang_css_out, "w", encoding="utf-8") as out_cf:
                out_cf.write(localize_css_for_language(raw_css, lang=lang))
            locale_css_paths[lang] = lang_css_out
        else:
            locale_css_paths[lang] = None

    return locale_navbars, locale_css_paths


def _build_i18n_html_tasks(
    input_abs: str,
    out_dir_abs: str,
    ordered_langs: list[str],
    locale_files: dict[str, list[str]],
    image_format: str,
) -> tuple[list[tuple[str, str, str, str, bool]], list[str], int]:
    """Build ordered (lang, rel_path, src_abs, dest_abs, is_md) tasks and run duplicate checks per locale."""
    all_tasks: list[tuple[str, str, str, str, bool]] = []
    display_names: list[str] = []
    max_blocks = 0

    for lang in ordered_langs:
        lang_tasks: list[tuple[str, str, bool]] = []
        lang_disp: list[str] = []
        lang_shared_dirs: list[str | None] = []
        for rel_path in locale_files[lang]:
            src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
            is_md = rel_path.lower().endswith((".md", ".markdown"))
            rel_stem, _ = os.path.splitext(rel_path)
            rel_html = f"{rel_stem}.html" if is_md else rel_path
            dest_abs = os.path.join(out_dir_abs, lang, *rel_html.split("/"))
            shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))

            all_tasks.append((lang, rel_path, src_abs, dest_abs, is_md))
            disp = f"/{lang}/{rel_path}"
            display_names.append(disp)
            lang_tasks.append((src_abs, dest_abs, is_md))
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


def _build_i18n_html(
    *,
    input_abs: str,
    out_dir_abs: str,
    i18n_cfg: I18nConfig,
    image_format: str,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    css_mode: str,
) -> str:
    """Compile a multi-locale (i18n) site directory into HTML."""
    if out_dir_abs == input_abs:
        raise ValueError(
            f'Refusing to build multi-locale HTML in-place inside source directory "{input_abs}". '
            "Please specify a separate output directory."
        )

    template_file, css_file = resolve_template_and_css(input_abs)
    locale_files = validate_i18n_site(input_abs, i18n_cfg, default_format=image_format)

    default_lang = i18n_cfg.default_lang
    ordered_langs = [default_lang] + [lc for lc in i18n_cfg.langs if lc != default_lang]
    locale_navbars, locale_css_paths = _prepare_i18n_locales_metadata(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        ordered_langs=ordered_langs,
        css_file=css_file,
        css_mode=css_mode,
    )
    all_tasks, display_names, max_blocks = _build_i18n_html_tasks(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        ordered_langs=ordered_langs,
        locale_files=locale_files,
        image_format=image_format,
    )

    root_disp = "/index.html"
    total_files = len(all_tasks) + 1
    name_width = max((len(n) for n in [*display_names, root_disp]), default=0)
    image_width = len(str(max(max_blocks, 0)))
    cache = BuildImageCache(enabled=not no_cache)
    processors_by_cfg: dict[tuple[str | None, str | None], DrawlibBlockProcessor | None] = {}
    locale_styles_utils: dict[str, tuple[str | None, str | None]] = {
        lc: resolve_styles_and_utils(os.path.join(input_abs, lc), styles_path, utils_path) for lc in ordered_langs
    }

    for idx, ((lang, rel_path, src_abs, dest_abs, is_md), disp_name) in enumerate(
        zip(all_tasks, display_names),
        start=1,
    ):
        loc_styles, loc_utils = locale_styles_utils[lang]
        cfg_key = (loc_styles, loc_utils)
        processors_by_cfg[cfg_key] = _compile_i18n_locale_page(
            idx=idx,
            total_files=total_files,
            disp_name=disp_name,
            name_width=name_width,
            image_width=image_width,
            lang=lang,
            rel_path=rel_path,
            src_abs=src_abs,
            dest_abs=dest_abs,
            is_md=is_md,
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            i18n_cfg=i18n_cfg,
            locale_navbar=locale_navbars[lang],
            locale_css_path=locale_css_paths[lang],
            css_file=css_file,
            template_file=template_file,
            image_format=image_format,
            styles_abs=loc_styles,
            utils_abs=loc_utils,
            processor=processors_by_cfg.get(cfg_key),
            no_cache=no_cache,
            cache=cache,
        )

    def_styles, def_utils = locale_styles_utils[default_lang]
    def_key = (def_styles, def_utils)
    _compile_i18n_root_index_page(
        idx=total_files,
        total_files=total_files,
        disp_name=root_disp,
        name_width=name_width,
        image_width=image_width,
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        i18n_cfg=i18n_cfg,
        default_navbar=locale_navbars[default_lang],
        default_css_path=locale_css_paths[default_lang],
        css_file=css_file,
        template_file=template_file,
        image_format=image_format,
        styles_abs=def_styles,
        utils_abs=def_utils,
        processor=processors_by_cfg.get(def_key),
        no_cache=no_cache,
        cache=cache,
    )

    copy_directory_assets(input_abs, out_dir_abs, excluded_files={template_file, css_file})
    for css_out in locale_css_paths.values():
        if css_out is not None:
            bundle_svg_fonts(out_dir_abs, css_file_path=css_out)

    readme_out = os.path.join(out_dir_abs, "README.md")
    if not os.path.exists(readme_out):
        os.makedirs(out_dir_abs, exist_ok=True)
        with open(readme_out, "w", encoding="utf-8") as f:
            f.write(get_html_readme())

    return out_dir_abs


def _build_i18n_doc_html(
    *,
    input_abs: str,
    out_dir_abs: str,
    i18n_cfg: I18nConfig,
    image_format: str,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    css_mode: str,
) -> str:
    """Compile a multi-locale (i18n) linear ``doc`` directory into merged HTML documents per locale."""
    if out_dir_abs == input_abs:
        raise ValueError(
            f'Refusing to build multi-locale HTML in-place inside source directory "{input_abs}". '
            "Please specify a separate output directory."
        )

    template_file, css_file = resolve_template_and_css(input_abs)
    locale_files = validate_i18n_project(
        input_abs,
        i18n_cfg,
        project_type="doc",
        default_format=image_format,
    )

    default_lang = i18n_cfg.default_lang
    ordered_langs = [default_lang] + [lc for lc in i18n_cfg.langs if lc != default_lang]

    locale_css_paths: dict[str, str | None] = {}
    raw_css = ""
    if css_mode != "embed":
        with open(css_file, "r", encoding="utf-8") as cf:
            raw_css = cf.read()

    for lang in ordered_langs:
        lang_out_dir = os.path.join(out_dir_abs, lang)
        if os.path.isdir(lang_out_dir) and not os.path.exists(os.path.join(lang_out_dir, ".git")):
            for entry in os.listdir(lang_out_dir):
                if entry.lower().endswith((".html", ".htm")) and entry.lower() != "index.html":
                    stale_html = os.path.join(lang_out_dir, entry)
                    if os.path.isfile(stale_html):
                        os.remove(stale_html)

        if css_mode != "embed":
            lang_css_out = os.path.join(lang_out_dir, "style.css")
            os.makedirs(os.path.dirname(lang_css_out), exist_ok=True)
            with open(lang_css_out, "w", encoding="utf-8") as out_cf:
                out_cf.write(localize_css_for_language(raw_css, lang=lang))
            locale_css_paths[lang] = lang_css_out
        else:
            locale_css_paths[lang] = None

    all_disp_names: list[str] = []
    max_blocks = 0
    for lang in ordered_langs:
        lang_tasks: list[tuple[str, str, bool]] = []
        lang_disp: list[str] = []
        lang_shared_dirs: list[str | None] = []
        for rel_path in locale_files[lang]:
            src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
            is_md = rel_path.lower().endswith((".md", ".markdown"))
            rel_stem, _ = os.path.splitext(rel_path)
            dest_abs = os.path.join(out_dir_abs, lang, f"{os.path.basename(rel_stem)}.html")
            shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
            disp = f"/{lang}/{rel_path}"
            all_disp_names.append(disp)
            lang_tasks.append((src_abs, dest_abs, is_md))
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

    root_disp = "/index.html"
    total_files = len(all_disp_names) + 1
    name_width = max((len(n) for n in [*all_disp_names, root_disp]), default=0)
    image_width = len(str(max(max_blocks, 0)))
    cache = BuildImageCache(enabled=not no_cache)
    processors_by_cfg: dict[tuple[str | None, str | None], DrawlibBlockProcessor | None] = {}

    global_step = 0
    default_combined_body = ""
    default_doc_title = "Drawlib Document"

    for lang in ordered_langs:
        lang_out_dir = os.path.join(out_dir_abs, lang)
        lang_index_dest = os.path.join(lang_out_dir, "index.html")
        loc_styles, loc_utils = resolve_styles_and_utils(os.path.join(input_abs, lang), styles_path, utils_path)
        cfg_key = (loc_styles, loc_utils)
        processor = processors_by_cfg.get(cfg_key)

        chapter_anchors: dict[str, str] = {}
        for c_idx, rel_path in enumerate(locale_files[lang], start=1):
            src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
            stem = os.path.splitext(os.path.basename(src_abs))[0]
            slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", stem).strip("-").lower() or f"doc-{c_idx}"
            anchor_id = f"chapter-{c_idx}-{slug}"
            chapter_anchors[src_abs] = anchor_id
            chapter_anchors[os.path.basename(src_abs)] = anchor_id
            chapter_anchors[f"{stem}.md"] = anchor_id
            chapter_anchors[f"{stem}.html"] = anchor_id

        chapters_html: list[str] = []
        toc_entries: list[tuple[str, str]] = []
        inferred_title: str | None = None

        for rel_path in locale_files[lang]:
            global_step += 1
            src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
            rel_stem, _ = os.path.splitext(rel_path)
            dest_abs = os.path.join(lang_out_dir, f"{os.path.basename(rel_stem)}.html")
            shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
            progress = FileBuildProgress(
                global_step,
                total_files,
                file_name=f"/{lang}/{rel_path}",
                name_width=name_width,
                image_width=image_width,
            )
            chapter_body, chapter_title, processor = _compile_chapter_body(
                src_abs=src_abs,
                dest_abs=dest_abs,
                image_format=image_format,
                styles_path=loc_styles,
                utils_path=loc_utils,
                processor=processor,
                progress=progress,
                no_cache=no_cache,
                cache=cache,
                project_root=input_abs,
                shared_images_dir=shared_dir,
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
            chapters_html.append(
                f'<section id="{anchor_id}" class="doc-chapter pdf-chapter">\n{chapter_body}\n</section>'
            )

        processors_by_cfg[cfg_key] = processor
        lang_cfg = get_language_config(lang)
        body_parts: list[str] = []
        index_entries = toc_entries[1:]
        if len(index_entries) > 0:
            toc_items = "\n".join(f'    <li><a href="#{anc}">{t_title}</a></li>' for anc, t_title in index_entries)
            toc_html = (
                f'<nav class="doc-toc pdf-toc">\n'
                f"  <h2>{lang_cfg.toc_title}</h2>\n"
                f"  <ul>\n{toc_items}\n  </ul>\n"
                f"</nav>"
            )
            body_parts.append(chapters_html[0])
            body_parts.append(toc_html)
            body_parts.extend(chapters_html[1:])
        else:
            body_parts.extend(chapters_html)

        combined_body = "\n\n".join(body_parts)
        resolved_title = inferred_title or "Drawlib Document"
        if lang == default_lang:
            default_combined_body = combined_body
            default_doc_title = resolved_title

        languages_ctx, alt_links = build_language_switcher_context(
            config=i18n_cfg,
            out_dir_abs=out_dir_abs,
            rel_html_path="index.html",
            current_dest_abs=lang_index_dest,
            active_lang=lang,
        )
        rel_favicon_href = resolve_favicon_href(input_abs, out_dir_abs, lang_index_dest)
        rel_logo_href, rel_logo_dark_href = resolve_logo_hrefs(input_abs, out_dir_abs, lang_index_dest)
        full_html = render_html_document(
            body_html=combined_body,
            title=resolved_title,
            custom_css_path=css_file,
            css_href=("style.css" if locale_css_paths[lang] else None),
            nav_items=[],
            nav_sections=None,
            template_path=template_file,
            index_url="index.html",
            site_title=None,
            favicon_href=rel_favicon_href,
            logo_href=rel_logo_href,
            logo_dark_href=rel_logo_dark_href,
            html_lang=lang_cfg.code,
            html_dir=lang_cfg.direction,
            font_link_html=lang_cfg.font_link_html,
            languages=languages_ctx,
            alternate_links=alt_links,
            css_lang=lang,
        )
        os.makedirs(lang_out_dir, exist_ok=True)
        with open(lang_index_dest, "w", encoding="utf-8") as f:
            f.write(full_html)

    root_progress = FileBuildProgress(
        total_files,
        total_files,
        file_name=root_disp,
        name_width=name_width,
        image_width=image_width,
    )
    root_progress.update(0, 0, done=False)
    root_body = rebase_html_relative_urls(
        html=default_combined_body,
        from_dir=os.path.join(out_dir_abs, default_lang),
        to_dir=out_dir_abs,
        skip_prefixes=(),
    )
    root_dest_abs = os.path.join(out_dir_abs, "index.html")
    default_css_path = locale_css_paths[default_lang]
    root_css_href = os.path.relpath(default_css_path, out_dir_abs).replace(os.sep, "/") if default_css_path else None
    root_languages, root_alt_links = build_language_switcher_context(
        config=i18n_cfg,
        out_dir_abs=out_dir_abs,
        rel_html_path="index.html",
        current_dest_abs=root_dest_abs,
        active_lang=default_lang,
    )
    def_lang_cfg = get_language_config(default_lang)
    root_favicon_href = resolve_favicon_href(input_abs, out_dir_abs, root_dest_abs)
    root_logo_href, root_logo_dark_href = resolve_logo_hrefs(input_abs, out_dir_abs, root_dest_abs)
    root_html = render_html_document(
        body_html=root_body,
        title=default_doc_title,
        custom_css_path=css_file,
        css_href=root_css_href,
        nav_items=[],
        nav_sections=None,
        template_path=template_file,
        index_url="index.html",
        site_title=None,
        favicon_href=root_favicon_href,
        logo_href=root_logo_href,
        logo_dark_href=root_logo_dark_href,
        html_lang=def_lang_cfg.code,
        html_dir=def_lang_cfg.direction,
        font_link_html=def_lang_cfg.font_link_html,
        languages=root_languages,
        alternate_links=root_alt_links,
        css_lang=default_lang,
    )
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(root_dest_abs, "w", encoding="utf-8") as f:
        f.write(root_html)
    root_progress.update(0, 0, done=True)

    copy_directory_assets(input_abs, out_dir_abs, excluded_files={template_file, css_file})
    for css_out in locale_css_paths.values():
        if css_out is not None:
            bundle_svg_fonts(out_dir_abs, css_file_path=css_out)

    readme_out = os.path.join(out_dir_abs, "README.md")
    if not os.path.exists(readme_out):
        os.makedirs(out_dir_abs, exist_ok=True)
        with open(readme_out, "w", encoding="utf-8") as f:
            f.write(get_html_readme())

    return out_dir_abs


def _compile_i18n_locale_page(
    *,
    idx: int,
    total_files: int,
    disp_name: str,
    name_width: int,
    image_width: int,
    lang: str,
    rel_path: str,
    src_abs: str,
    dest_abs: str,
    is_md: bool,
    input_abs: str,
    out_dir_abs: str,
    i18n_cfg: I18nConfig,
    locale_navbar: tuple[list[NavbarSection], str | None],
    locale_css_path: str | None,
    css_file: str,
    template_file: str,
    image_format: str,
    styles_abs: str | None,
    utils_abs: str | None,
    processor: DrawlibBlockProcessor | None,
    no_cache: bool,
    cache: BuildImageCache,
) -> DrawlibBlockProcessor | None:
    """Compile a single <out_dir_abs>/<lang>/<rel_html> page."""
    rel_stem, _ = os.path.splitext(rel_path)
    rel_html = f"{rel_stem}.html" if is_md else rel_path
    shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
    lang_src_root = os.path.join(input_abs, lang)
    lang_out_root = os.path.join(out_dir_abs, lang)
    lang_index_dest = os.path.join(lang_out_root, "index.html")

    rel_css_href = (
        os.path.relpath(locale_css_path, os.path.dirname(dest_abs)).replace(os.sep, "/")
        if locale_css_path
        else None
    )
    rel_index_url = os.path.relpath(lang_index_dest, os.path.dirname(dest_abs)).replace(os.sep, "/")
    rel_favicon_href = resolve_favicon_href(input_abs, out_dir_abs, dest_abs)
    rel_logo_href, rel_logo_dark_href = resolve_logo_hrefs(input_abs, out_dir_abs, dest_abs)
    nav_sections_raw, site_title = locale_navbar
    cur_sections, cur_items = resolve_navbar_for_page(
        sections=nav_sections_raw,
        root_dir_abs=lang_src_root,
        out_dir_abs=lang_out_root,
        current_src_abs=src_abs,
        current_dest_abs=dest_abs,
    )
    languages_ctx, alt_links = build_language_switcher_context(
        config=i18n_cfg,
        out_dir_abs=out_dir_abs,
        rel_html_path=rel_html,
        current_dest_abs=dest_abs,
        active_lang=lang,
    )
    lang_cfg = get_language_config(lang)

    return _compile_single_html_file(
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
        favicon_href=rel_favicon_href,
        logo_href=rel_logo_href,
        logo_dark_href=rel_logo_dark_href,
        shared_images_dir=shared_dir,
        html_lang=lang_cfg.code,
        html_dir=lang_cfg.direction,
        font_link_html=lang_cfg.font_link_html,
        languages=languages_ctx,
        alternate_links=alt_links,
        css_lang=lang,
    )


def _compile_i18n_root_index_page(
    *,
    idx: int,
    total_files: int,
    disp_name: str,
    name_width: int,
    image_width: int,
    input_abs: str,
    out_dir_abs: str,
    i18n_cfg: I18nConfig,
    default_navbar: tuple[list[NavbarSection], str | None],
    default_css_path: str | None,
    css_file: str,
    template_file: str,
    image_format: str,
    styles_abs: str | None,
    utils_abs: str | None,
    processor: DrawlibBlockProcessor | None,
    no_cache: bool,
    cache: BuildImageCache,
) -> DrawlibBlockProcessor | None:
    """Compile root <out_dir_abs>/index.html from <default_lang>/index.* with rebased relative links."""
    default_lang = i18n_cfg.default_lang
    def_src_root = os.path.join(input_abs, default_lang)
    def_out_root = os.path.join(out_dir_abs, default_lang)
    src_abs = _find_locale_index_src(def_src_root)
    dest_abs = os.path.join(out_dir_abs, "index.html")
    shared_dir = os.path.join(out_dir_abs, "images", "index")

    rel_css_href = (
        os.path.relpath(default_css_path, out_dir_abs).replace(os.sep, "/")
        if default_css_path
        else None
    )
    rel_favicon_href = resolve_favicon_href(input_abs, out_dir_abs, dest_abs)
    rel_logo_href, rel_logo_dark_href = resolve_logo_hrefs(input_abs, out_dir_abs, dest_abs)
    nav_sections_raw, site_title = default_navbar
    cur_sections, cur_items = resolve_navbar_for_page(
        sections=nav_sections_raw,
        root_dir_abs=def_src_root,
        out_dir_abs=def_out_root,
        current_src_abs=src_abs,
        current_dest_abs=dest_abs,
    )
    languages_ctx, alt_links = build_language_switcher_context(
        config=i18n_cfg,
        out_dir_abs=out_dir_abs,
        rel_html_path="index.html",
        current_dest_abs=dest_abs,
        active_lang=default_lang,
    )
    lang_cfg = get_language_config(default_lang)

    return _compile_single_html_file(
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
        index_url="index.html",
        site_title=site_title,
        project_root=input_abs,
        favicon_href=rel_favicon_href,
        logo_href=rel_logo_href,
        logo_dark_href=rel_logo_dark_href,
        shared_images_dir=shared_dir,
        rebase_from_dir=def_out_root,
        html_lang=lang_cfg.code,
        html_dir=lang_cfg.direction,
        font_link_html=lang_cfg.font_link_html,
        languages=languages_ctx,
        alternate_links=alt_links,
        css_lang=default_lang,
    )


def _compile_merged_doc_html(
    *,
    html_tasks: list[tuple[str, str, bool]],
    display_names: list[str],
    input_abs: str,
    out_dir_abs: str,
    image_format: str,
    styles_path: str | None,
    utils_path: str | None,
    css_path: str | None,
    css_href: str | None,
    template_path: str | None,
    name_width: int,
    image_width: int,
    no_cache: bool,
    cache: BuildImageCache,
    lang: str = "en",
    project_root: str | None = None,
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
    inferred_title: str | None = None
    processor: DrawlibBlockProcessor | None = None
    total_files = len(html_tasks)
    eff_root = project_root or input_abs

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
            project_root=eff_root,
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

    lang_cfg = get_language_config(lang)
    body_parts: list[str] = []
    index_entries = toc_entries[1:]
    if len(index_entries) > 0:
        toc_items = "\n".join(f'    <li><a href="#{anc}">{t_title}</a></li>' for anc, t_title in index_entries)
        toc_html = (
            f'<nav class="doc-toc pdf-toc">\n'
            f"  <h2>{lang_cfg.toc_title}</h2>\n"
            f"  <ul>\n{toc_items}\n  </ul>\n"
            f"</nav>"
        )
        body_parts.append(chapters_html[0])
        body_parts.append(toc_html)
        body_parts.extend(chapters_html[1:])
    else:
        body_parts.extend(chapters_html)

    combined_body = "\n\n".join(body_parts)
    index_dest_abs = os.path.join(out_dir_abs, "index.html")
    rel_favicon_href = resolve_favicon_href(eff_root, out_dir_abs, index_dest_abs)
    rel_logo_href, rel_logo_dark_href = resolve_logo_hrefs(eff_root, out_dir_abs, index_dest_abs)
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
        favicon_href=rel_favicon_href,
        logo_href=rel_logo_href,
        logo_dark_href=rel_logo_dark_href,
        html_lang=lang_cfg.code,
        html_dir=lang_cfg.direction,
        font_link_html=lang_cfg.font_link_html,
        css_lang=lang,
    )

    os.makedirs(out_dir_abs, exist_ok=True)
    with open(index_dest_abs, "w", encoding="utf-8") as f:
        f.write(full_html)


def _compile_chapter_body(
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
) -> tuple[str, str, DrawlibBlockProcessor | None]:
    """Compile a single source file into an HTML body fragment and title."""
    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(src_abs, content)
    total_steps = doc_info.block_count
    if progress is not None:
        progress.update(0, total_steps, done=False)

    if doc_info.is_markdown:
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
                use_markdown_syntax=False,
                source_filename=src_abs,
                progress_callback=(progress.update if progress else None),
                shared_images_dir=shared_images_dir,
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
                shared_images_dir=shared_images_dir,
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
    styles_path: str | None = None,
    utils_path: str | None = None,
    css_path: str | None = None,
    css_href: str | None = None,
    template_path: str | None = None,
    processor: DrawlibBlockProcessor | None = None,
    progress: FileBuildProgress | None = None,
    no_cache: bool = False,
    cache: BuildImageCache | None = None,
    nav_sections: list[dict[str, Any]] | None = None,
    nav_items: list[dict[str, Any]] | None = None,
    index_url: str | None = None,
    site_title: str | None = None,
    project_root: str | None = None,
    favicon_href: str | None = None,
    logo_href: str | None = None,
    logo_dark_href: str | None = None,
    shared_images_dir: str | None = None,
    rebase_from_dir: str | None = None,
    html_lang: str | None = None,
    html_dir: str | None = None,
    font_link_html: str | None = None,
    languages: list[dict[str, Any]] | None = None,
    alternate_links: list[dict[str, str]] | None = None,
    css_lang: str = "en",
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
        shared_images_dir=shared_images_dir,
    )
    if rebase_from_dir is not None:
        body_html = rebase_html_relative_urls(
            html=body_html,
            from_dir=rebase_from_dir,
            to_dir=os.path.dirname(dest_abs),
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
        favicon_href=favicon_href,
        logo_href=logo_href,
        logo_dark_href=logo_dark_href,
        html_lang=html_lang,
        html_dir=html_dir,
        font_link_html=font_link_html,
        languages=languages,
        alternate_links=alternate_links,
        css_lang=css_lang,
    )

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    with open(dest_abs, "w", encoding="utf-8") as f:
        f.write(full_html)

    return processor
