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
import sys
from typing import Any, Literal

from drawlib._builder._common import (
    BlockRenderJob,
    BuildImageCache,
    CatalogConfig,
    FileBuildProgress,
    LlmsLink,
    LlmsSection,
    ProjectManifest,
    SitemapEntry,
    build_page_seo_metadata,
    collect_standard_document_block_jobs,
    ensure_seo_og_image_copied,
    extract_markdown_description,
    find_project_manifest,
    load_project_manifest,
    prerender_document_blocks,
    render_seo_head_tags,
    resolve_build_workers,
    resolve_localized_description,
    resolve_public_page_url,
    resolve_styles_and_utils,
    upgrade_alternate_links,
    write_llms_txt,
    write_robots_txt,
    write_sitemap_xml,
)
from drawlib._builder.doc_builder.catalog_nav import (
    CompiledCatalogPage,
    build_catalog_page_navigation_context,
    inject_catalog_heading_ids_and_badges,
    order_catalog_locale_files,
    resolve_catalog_chrome_context,
)
from drawlib._builder.doc_builder.compiler.base import (
    copy_directory_assets,
    extract_html_body,
    extract_title,
    require_directory,
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


def _resolve_default_html_out_dir(input_abs: str, output_dir: str | None) -> str:
    """Resolve output HTML directory path, defaulting to ``<parent>/<base>_html``."""
    if output_dir:
        return os.path.abspath(output_dir)
    dir_name = os.path.basename(input_abs.rstrip(os.sep))
    base_name = dir_name[:-4] if dir_name.endswith("_src") and len(dir_name) > 4 else (dir_name or "docs")
    return os.path.join(os.path.dirname(input_abs), f"{base_name}_html")


def build_html(
    input_dir: str,
    output_dir: str | None = None,
    *,
    image_format: str = "png",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    css_mode: str = "external",
    workers: int | Literal["auto"] = "auto",
) -> str:
    """Compile an i18n-native ``site``, ``doc``, or ``catalog`` project directory into static HTML.

    Builds all configured locales in ``drawlib.toml`` ``[i18n]`` with shared diagram
    deduplication, per-locale stylesheets, language switcher navigation (when 2+ locales
    are configured), and a root default-language ``index.html``.

    Args:
        input_dir (str): Project root directory containing ``drawlib.toml`` and ``<lang>/`` folders.
        output_dir (Optional[str]): Target output directory. Defaults to ``<base>_html``.
        image_format (str): Image output format ('png' or 'webp'). Defaults to 'png'.
        styles_path (Optional[str]): Path to custom styles.py script.
        utils_path (Optional[str]): Path to custom utils.py script.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.
        css_mode (str): CSS linking mode ('external' by default, or 'embed').
        workers (int | Literal["auto"]): Number of parallel rendering worker processes ('auto' or int >= 1).

    Returns:
        str: Absolute path of generated HTML output directory.

    Raises:
        ValueError: If input_dir is not a valid ``doc``, ``site``, or ``catalog`` project root directory.
    """
    eff_workers = resolve_build_workers(workers)
    input_abs = require_directory(input_dir, "build_html")
    out_dir_abs = _resolve_default_html_out_dir(input_abs, output_dir)

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
            "HTML directory builds require a Drawlib project manifest "
            '(run "drawlib init project site", "drawlib init project doc", or "drawlib init project catalog").'
        )

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
    if manifest.i18n is None:
        raise ValueError(f'Invalid "{input_abs}/drawlib.toml": "[i18n]" configuration is required.')

    if manifest.project.type == "doc":
        return _build_i18n_doc_html(
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            manifest=manifest,
            i18n_cfg=manifest.i18n,
            image_format=image_format,
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
            css_mode=css_mode,
            workers=eff_workers,
        )
    if manifest.project.type == "catalog":
        return _build_i18n_catalog_html(
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            manifest=manifest,
            i18n_cfg=manifest.i18n,
            image_format=image_format,
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
            css_mode=css_mode,
            workers=eff_workers,
        )
    return _build_i18n_site_html(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        manifest=manifest,
        i18n_cfg=manifest.i18n,
        image_format=image_format,
        styles_path=styles_path,
        utils_path=utils_path,
        no_cache=no_cache,
        css_mode=css_mode,
        workers=eff_workers,
    )


def _find_locale_index_src(lang_dir_abs: str) -> str:
    """Return absolute path to index.md or index.html inside a locale directory."""
    for cand_name in ("index.md", "index.markdown", "index.html", "index.htm"):
        cand = os.path.join(lang_dir_abs, cand_name)
        if os.path.isfile(cand):
            return cand
    raise ValueError(f'Site project requires "index.md" or "index.html" inside "{lang_dir_abs}".')


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
            raise ValueError(f'Site project requires "navbar.md" inside "{lang_dir}".')
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


def _build_i18n_site_html(
    *,
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    image_format: str,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    css_mode: str,
    workers: int = 1,
) -> str:
    """Compile an i18n-native ``site`` directory into HTML."""
    if out_dir_abs == input_abs:
        raise ValueError(
            f'Refusing to build HTML in-place inside source directory "{input_abs}". '
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

    if workers > 1:
        site_jobs: list[BlockRenderJob] = []
        for lang, rel_path, src_abs, dest_abs, is_md in all_tasks:
            loc_styles, loc_utils = locale_styles_utils[lang]
            rel_stem, _ = os.path.splitext(rel_path)
            shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
            site_jobs.extend(
                collect_standard_document_block_jobs(
                    src_abs=src_abs,
                    dest_abs=dest_abs,
                    is_md=is_md,
                    image_format=image_format,
                    embed_images=False,
                    styles_path=loc_styles,
                    utils_path=loc_utils,
                    project_root=input_abs,
                    shared_images_dir=shared_dir,
                    require_file=True,
                    no_cache_global=no_cache,
                )
            )
        prerender_document_blocks(site_jobs, cache=cache, workers=workers)

    rel_htmls_by_lang: dict[str, list[str]] = {lc: [] for lc in ordered_langs}
    page_meta_by_src: dict[str, tuple[str, str, str]] = {}
    default_src_files: list[str] = []
    landing_desc_by_lang: dict[str, str] = {}

    for idx, ((lang, rel_path, src_abs, dest_abs, is_md), disp_name) in enumerate(
        zip(all_tasks, display_names),
        start=1,
    ):
        loc_styles, loc_utils = locale_styles_utils[lang]
        cfg_key = (loc_styles, loc_utils)
        next_proc, doc_title, doc_desc, rel_html = _compile_i18n_locale_page(
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
            manifest=manifest,
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
        processors_by_cfg[cfg_key] = next_proc
        rel_htmls_by_lang[lang].append(rel_html)
        if rel_html == "index.html":
            landing_desc_by_lang[lang] = doc_desc
        if lang == default_lang:
            abs_src_key = os.path.abspath(src_abs)
            default_src_files.append(abs_src_key)
            page_meta_by_src[abs_src_key] = (doc_title, doc_desc, f"{lang}/{rel_html}")

    def_styles, def_utils = locale_styles_utils[default_lang]
    def_key = (def_styles, def_utils)
    _, root_title, root_desc = _compile_i18n_root_index_page(
        idx=total_files,
        total_files=total_files,
        disp_name=root_disp,
        name_width=name_width,
        image_width=image_width,
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        manifest=manifest,
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

    _emit_site_seo_files(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        manifest=manifest,
        i18n_cfg=i18n_cfg,
        ordered_langs=ordered_langs,
        rel_htmls_by_lang=rel_htmls_by_lang,
        default_navbar=locale_navbars[default_lang],
        page_meta_by_src=page_meta_by_src,
        default_src_files=default_src_files,
        landing_desc_by_lang=landing_desc_by_lang,
        root_title=root_title,
        root_desc=root_desc,
    )

    readme_out = os.path.join(out_dir_abs, "README.md")
    if not os.path.exists(readme_out):
        os.makedirs(out_dir_abs, exist_ok=True)
        with open(readme_out, "w", encoding="utf-8") as f:
            f.write(get_html_readme())

    return out_dir_abs


def _prepare_i18n_doc_locales(
    *,
    input_abs: str,
    out_dir_abs: str,
    ordered_langs: list[str],
    locale_files: dict[str, list[str]],
    css_file: str,
    css_mode: str,
    image_format: str,
) -> tuple[dict[str, str | None], list[str], int]:
    """Prepare localized ``style.css`` files, clean stale HTMLs, and check duplicate block outputs for ``doc``."""
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

    return locale_css_paths, all_disp_names, max_blocks


def _compile_doc_locale_combined(
    *,
    lang: str,
    rel_files: list[str],
    input_abs: str,
    out_dir_abs: str,
    start_step: int,
    total_files: int,
    name_width: int,
    image_width: int,
    image_format: str,
    loc_styles: str | None,
    loc_utils: str | None,
    processor: DrawlibBlockProcessor | None,
    no_cache: bool,
    cache: BuildImageCache,
) -> tuple[str, str, str, list[tuple[str, str, str]], int, DrawlibBlockProcessor | None]:
    """Compile all chapters for one ``doc`` locale and return combined body, title, desc, chapters, step, proc."""
    lang_out_dir = os.path.join(out_dir_abs, lang)
    chapter_anchors: dict[str, str] = {}
    for c_idx, rel_path in enumerate(rel_files, start=1):
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
    chapters_meta: list[tuple[str, str, str]] = []
    inferred_title: str | None = None
    first_desc = ""
    global_step = start_step

    for rel_path in rel_files:
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
        chapter_body, chapter_title, chapter_desc, processor = _compile_chapter_body(
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
        if not first_desc and chapter_desc:
            first_desc = chapter_desc

        anchor_id = chapter_anchors[src_abs]
        toc_entries.append((anchor_id, chapter_title))
        chapters_meta.append((anchor_id, chapter_title, chapter_desc))

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
            f'<nav class="doc-toc pdf-toc">\n  <h2>{lang_cfg.toc_title}</h2>\n  <ul>\n{toc_items}\n  </ul>\n</nav>'
        )
        body_parts.append(chapters_html[0])
        body_parts.append(toc_html)
        body_parts.extend(chapters_html[1:])
    else:
        body_parts.extend(chapters_html)

    combined_body = "\n\n".join(body_parts)
    resolved_title = inferred_title or "Drawlib Document"
    return combined_body, resolved_title, first_desc, chapters_meta, global_step, processor


def _build_i18n_doc_html(
    *,
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    image_format: str,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    css_mode: str,
    workers: int = 1,
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
    locale_css_paths, all_disp_names, max_blocks = _prepare_i18n_doc_locales(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        ordered_langs=ordered_langs,
        locale_files=locale_files,
        css_file=css_file,
        css_mode=css_mode,
        image_format=image_format,
    )

    root_disp = "/index.html"
    total_files = len(all_disp_names) + 1
    name_width = max((len(n) for n in [*all_disp_names, root_disp]), default=0)
    image_width = len(str(max(max_blocks, 0)))
    cache = BuildImageCache(enabled=not no_cache)
    processors_by_cfg: dict[tuple[str | None, str | None], DrawlibBlockProcessor | None] = {}
    locale_styles_utils: dict[str, tuple[str | None, str | None]] = {
        lc: resolve_styles_and_utils(os.path.join(input_abs, lc), styles_path, utils_path) for lc in ordered_langs
    }

    if workers > 1:
        doc_jobs: list[BlockRenderJob] = []
        for lang in ordered_langs:
            loc_styles, loc_utils = locale_styles_utils[lang]
            lang_out_dir = os.path.join(out_dir_abs, lang)
            for rel_path in locale_files[lang]:
                src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
                is_md = rel_path.lower().endswith((".md", ".markdown"))
                rel_stem, _ = os.path.splitext(rel_path)
                dest_abs = os.path.join(lang_out_dir, f"{os.path.basename(rel_stem)}.html")
                shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
                doc_jobs.extend(
                    collect_standard_document_block_jobs(
                        src_abs=src_abs,
                        dest_abs=dest_abs,
                        is_md=is_md,
                        image_format=image_format,
                        embed_images=False,
                        styles_path=loc_styles,
                        utils_path=loc_utils,
                        project_root=input_abs,
                        shared_images_dir=shared_dir,
                        require_file=True,
                        no_cache_global=no_cache,
                    )
                )
        prerender_document_blocks(doc_jobs, cache=cache, workers=workers)

    global_step = 0
    default_combined_body = ""
    default_doc_title = "Drawlib Document"
    default_doc_desc = ""
    default_chapters_meta: list[tuple[str, str, str]] = []
    landing_desc_by_lang: dict[str, str] = {}
    doc_site_title = manifest.project.title.strip() or None

    for lang in ordered_langs:
        lang_out_dir = os.path.join(out_dir_abs, lang)
        lang_index_dest = os.path.join(lang_out_dir, "index.html")
        loc_styles, loc_utils = locale_styles_utils[lang]
        cfg_key = (loc_styles, loc_utils)

        combined_body, resolved_title, first_desc, chapters_meta, global_step, next_proc = _compile_doc_locale_combined(
            lang=lang,
            rel_files=locale_files[lang],
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            start_step=global_step,
            total_files=total_files,
            name_width=name_width,
            image_width=image_width,
            image_format=image_format,
            loc_styles=loc_styles,
            loc_utils=loc_utils,
            processor=processors_by_cfg.get(cfg_key),
            no_cache=no_cache,
            cache=cache,
        )
        processors_by_cfg[cfg_key] = next_proc
        landing_desc_by_lang[lang] = first_desc
        if lang == default_lang:
            default_combined_body = combined_body
            default_doc_title = resolved_title
            default_doc_desc = first_desc
            default_chapters_meta = chapters_meta

        lang_cfg = get_language_config(lang)
        languages_ctx, alt_links = build_language_switcher_context(
            config=i18n_cfg,
            out_dir_abs=out_dir_abs,
            rel_html_path="index.html",
            current_dest_abs=lang_index_dest,
            active_lang=lang,
        )
        seo_meta_html, eff_alt_links = _resolve_page_seo_and_alternates(
            manifest=manifest,
            out_dir_abs=out_dir_abs,
            dest_abs=lang_index_dest,
            lang=lang,
            page_title=resolved_title,
            site_title=doc_site_title,
            page_description=first_desc,
            prefer_manifest_description=True,
            alternate_links=alt_links,
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
            alternate_links=eff_alt_links,
            css_lang=lang,
            seo_meta_html=seo_meta_html,
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
    root_seo_html, eff_root_alt_links = _resolve_page_seo_and_alternates(
        manifest=manifest,
        out_dir_abs=out_dir_abs,
        dest_abs=root_dest_abs,
        lang=default_lang,
        page_title=default_doc_title,
        site_title=doc_site_title,
        page_description=default_doc_desc,
        prefer_manifest_description=True,
        alternate_links=root_alt_links,
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
        alternate_links=eff_root_alt_links,
        css_lang=default_lang,
        seo_meta_html=root_seo_html,
    )
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(root_dest_abs, "w", encoding="utf-8") as f:
        f.write(root_html)
    root_progress.update(0, 0, done=True)

    copy_directory_assets(input_abs, out_dir_abs, excluded_files={template_file, css_file})
    for css_out in locale_css_paths.values():
        if css_out is not None:
            bundle_svg_fonts(out_dir_abs, css_file_path=css_out)

    _emit_doc_seo_files(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        manifest=manifest,
        i18n_cfg=i18n_cfg,
        ordered_langs=ordered_langs,
        default_title=default_doc_title,
        default_chapters=default_chapters_meta,
        landing_desc_by_lang=landing_desc_by_lang,
    )

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
    manifest: ProjectManifest | None,
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
) -> tuple[DrawlibBlockProcessor | None, str, str, str]:
    """Compile a single <out_dir_abs>/<lang>/<rel_html> page and return (processor, title, desc, rel_html)."""
    rel_stem, _ = os.path.splitext(rel_path)
    rel_html = f"{rel_stem}.html" if is_md else rel_path
    shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
    lang_src_root = os.path.join(input_abs, lang)
    lang_out_root = os.path.join(out_dir_abs, lang)
    lang_index_dest = os.path.join(lang_out_root, "index.html")

    rel_css_href = (
        os.path.relpath(locale_css_path, os.path.dirname(dest_abs)).replace(os.sep, "/") if locale_css_path else None
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
    is_landing_index = rel_html == "index.html"

    next_proc, doc_title, doc_desc = _compile_single_html_file(
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
        manifest=manifest,
        out_dir_abs=out_dir_abs,
        prefer_manifest_description=is_landing_index,
    )
    return next_proc, doc_title, doc_desc, rel_html


def _compile_i18n_root_index_page(
    *,
    idx: int,
    total_files: int,
    disp_name: str,
    name_width: int,
    image_width: int,
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest | None,
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
) -> tuple[DrawlibBlockProcessor | None, str, str]:
    """Compile root <out_dir_abs>/index.html from <default_lang>/index.* with rebased relative links."""
    default_lang = i18n_cfg.default_lang
    def_src_root = os.path.join(input_abs, default_lang)
    def_out_root = os.path.join(out_dir_abs, default_lang)
    src_abs = _find_locale_index_src(def_src_root)
    dest_abs = os.path.join(out_dir_abs, "index.html")
    shared_dir = os.path.join(out_dir_abs, "images", "index")

    rel_css_href = os.path.relpath(default_css_path, out_dir_abs).replace(os.sep, "/") if default_css_path else None
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
        manifest=manifest,
        out_dir_abs=out_dir_abs,
        prefer_manifest_description=True,
    )


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
) -> tuple[str, str, str, DrawlibBlockProcessor | None]:
    """Compile a single source file into an HTML body fragment, title, and plain-text summary."""
    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    doc_info = detect_document_type(src_abs, content)
    total_steps = doc_info.block_count
    if progress is not None:
        progress.update(0, total_steps, done=False)

    if doc_info.is_markdown:
        validate_markdown_links(src_abs, content)
        validate_markdown_images(src_abs, content)
        doc_desc = extract_markdown_description(content)
    else:
        doc_desc = ""

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

    return body_html, doc_title, doc_desc, processor


def _resolve_page_seo_and_alternates(
    *,
    manifest: ProjectManifest | None,
    out_dir_abs: str | None,
    dest_abs: str,
    lang: str,
    page_title: str,
    site_title: str | None,
    page_description: str,
    prefer_manifest_description: bool,
    alternate_links: list[dict[str, str]] | None,
) -> tuple[str | None, list[dict[str, str]] | None]:
    """Build rendered SEO ``<head>`` tags and upgrade ``alternate_links`` when ``[seo]`` is active."""
    if manifest is None or manifest.seo is None or out_dir_abs is None:
        return None, alternate_links

    upgraded = (
        upgrade_alternate_links(alternate_links, manifest.seo.site_url, out_dir_abs, dest_abs)
        if alternate_links and manifest.seo.site_url
        else alternate_links
    )
    seo_meta = build_page_seo_metadata(
        manifest=manifest,
        out_dir_abs=out_dir_abs,
        dest_abs=dest_abs,
        lang=lang,
        page_title=page_title,
        site_title=site_title,
        page_description=page_description,
        prefer_manifest_description=prefer_manifest_description,
    )
    seo_html = render_seo_head_tags(seo_meta) if seo_meta is not None else None
    return seo_html, upgraded


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
    manifest: ProjectManifest | None = None,
    out_dir_abs: str | None = None,
    prefer_manifest_description: bool = False,
) -> tuple[DrawlibBlockProcessor | None, str, str]:
    """Compile a single Markdown or HTML file into HTML and return ``(processor, title, description)``."""
    body_html, doc_title, doc_desc, processor = _compile_chapter_body(
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

    seo_meta_html, eff_alt_links = _resolve_page_seo_and_alternates(
        manifest=manifest,
        out_dir_abs=out_dir_abs,
        dest_abs=dest_abs,
        lang=css_lang,
        page_title=doc_title,
        site_title=site_title,
        page_description=doc_desc,
        prefer_manifest_description=prefer_manifest_description,
        alternate_links=alternate_links,
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
        alternate_links=eff_alt_links,
        css_lang=css_lang,
        seo_meta_html=seo_meta_html,
    )

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    with open(dest_abs, "w", encoding="utf-8") as f:
        f.write(full_html)

    return processor, doc_title, doc_desc


def _build_i18n_sitemap_entries(
    site_url: str,
    i18n_cfg: I18nConfig,
    ordered_langs: list[str],
    rel_htmls_by_lang: dict[str, list[str]],
) -> list[SitemapEntry]:
    """Construct ``SitemapEntry`` items for root ``index.html`` and all localized pages."""
    multi_locale = len(i18n_cfg.langs) >= 2
    default_lang = i18n_cfg.default_lang

    def _alternates_for(rel_html: str) -> tuple[tuple[str, str], ...]:
        if not multi_locale:
            return ()
        alts = [
            (get_language_config(lc).code, resolve_public_page_url(site_url, f"{lc}/{rel_html}"))
            for lc in i18n_cfg.langs
        ]
        x_def_rel = "index.html" if rel_html == "index.html" else f"{default_lang}/{rel_html}"
        alts.append(("x-default", resolve_public_page_url(site_url, x_def_rel)))
        return tuple(alts)

    entries: list[SitemapEntry] = [
        SitemapEntry(
            loc=resolve_public_page_url(site_url, "index.html"),
            alternates=_alternates_for("index.html"),
        )
    ]
    for lang in ordered_langs:
        rel_list = rel_htmls_by_lang.get(lang, [])
        ordered_rels = (["index.html"] if "index.html" in rel_list else []) + [
            r for r in rel_list if r != "index.html"
        ]
        for rel_html in ordered_rels:
            entries.append(
                SitemapEntry(
                    loc=resolve_public_page_url(site_url, f"{lang}/{rel_html}"),
                    alternates=_alternates_for(rel_html),
                )
            )
    return entries


def _format_llms_url(site_url: str, rel_out_path: str) -> str:
    """Format a public or root-relative link URL for ``llms.txt``."""
    if site_url:
        return resolve_public_page_url(site_url, rel_out_path)
    norm = rel_out_path.replace("\\", "/").lstrip("/")
    if not norm or norm == "index.html":
        return "/"
    if norm.endswith("/index.html"):
        return f"/{norm[:-len('index.html')]}"
    return f"/{norm}"


def _build_locales_llms_section(
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    site_url: str,
    landing_desc_by_lang: dict[str, str],
) -> LlmsSection | None:
    """Build optional ``Locales`` section for ``llms.txt`` when 2+ languages are configured."""
    if len(i18n_cfg.langs) < 2:
        return None
    links: list[LlmsLink] = []
    for lc in i18n_cfg.langs:
        lang_cfg = get_language_config(lc)
        label = i18n_cfg.labels.get(lc) or lang_cfg.display_name
        desc = resolve_localized_description(
            manifest=manifest,
            lang=lc,
            page_description=landing_desc_by_lang.get(lc, ""),
            prefer_manifest=True,
        )
        links.append(
            LlmsLink(
                title=f"{label} ({lang_cfg.code})",
                url=_format_llms_url(site_url, f"{lc}/index.html"),
                description=desc,
            )
        )
    return LlmsSection(title="Locales", links=links)


def _build_site_llms_sections(
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    site_url: str,
    nav_sections: list[NavbarSection],
    page_meta_by_src: dict[str, tuple[str, str, str]],
    default_src_files: list[str],
    landing_desc_by_lang: dict[str, str],
) -> list[LlmsSection]:
    """Organize ``site`` pages into ``LlmsSection`` blocks following ``navbar.md`` hierarchy."""
    sections: list[LlmsSection] = []
    seen_srcs: set[str] = set()

    for nav_sec in nav_sections:
        sec_links: list[LlmsLink] = []
        for item in nav_sec.items:
            if item.is_external or not item.target_file_abs:
                continue
            src_key = os.path.abspath(item.target_file_abs)
            meta = page_meta_by_src.get(src_key)
            if meta is None or src_key in seen_srcs:
                continue
            seen_srcs.add(src_key)
            doc_title, doc_desc, rel_out_html = meta
            sec_links.append(
                LlmsLink(
                    title=(item.title or doc_title),
                    url=_format_llms_url(site_url, rel_out_html),
                    description=doc_desc,
                )
            )
        if sec_links:
            sections.append(LlmsSection(title=(nav_sec.title or "Overview"), links=sec_links))

    extra_links: list[LlmsLink] = []
    for src_abs in default_src_files:
        src_key = os.path.abspath(src_abs)
        if src_key in seen_srcs or src_key not in page_meta_by_src:
            continue
        doc_title, doc_desc, rel_out_html = page_meta_by_src[src_key]
        extra_links.append(
            LlmsLink(
                title=doc_title,
                url=_format_llms_url(site_url, rel_out_html),
                description=doc_desc,
            )
        )
    if extra_links:
        sections.append(LlmsSection(title="Pages", links=extra_links))

    locales_sec = _build_locales_llms_section(manifest, i18n_cfg, site_url, landing_desc_by_lang)
    if locales_sec is not None:
        sections.append(locales_sec)
    return sections


def _emit_site_seo_files(
    *,
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    ordered_langs: list[str],
    rel_htmls_by_lang: dict[str, list[str]],
    default_navbar: tuple[list[NavbarSection], str | None],
    page_meta_by_src: dict[str, tuple[str, str, str]],
    default_src_files: list[str],
    landing_desc_by_lang: dict[str, str],
    root_title: str,
    root_desc: str,
) -> None:
    """Emit ``og_image`` copy, ``sitemap.xml``, ``robots.txt``, and ``llms.txt`` for a ``site`` build."""
    seo = manifest.seo
    if seo is None:
        return

    ensure_seo_og_image_copied(input_abs, out_dir_abs, seo)
    if seo.sitemap and seo.site_url:
        entries = _build_i18n_sitemap_entries(seo.site_url, i18n_cfg, ordered_langs, rel_htmls_by_lang)
        write_sitemap_xml(out_dir_abs, entries)
    if seo.robots:
        write_robots_txt(out_dir_abs, seo.site_url, include_sitemap=(seo.sitemap and bool(seo.site_url)))
    if seo.llms_txt:
        nav_sections, nav_site_title = default_navbar
        llms_title = manifest.project.title.strip() or nav_site_title or root_title
        llms_summary = resolve_localized_description(
            manifest=manifest,
            lang=i18n_cfg.default_lang,
            page_description=root_desc,
            prefer_manifest=True,
            max_length=240,
        )
        sections = _build_site_llms_sections(
            manifest=manifest,
            i18n_cfg=i18n_cfg,
            site_url=seo.site_url,
            nav_sections=nav_sections,
            page_meta_by_src=page_meta_by_src,
            default_src_files=default_src_files,
            landing_desc_by_lang=landing_desc_by_lang,
        )
        write_llms_txt(out_dir_abs, title=llms_title, summary=llms_summary, sections=sections)


def _emit_doc_seo_files(
    *,
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    ordered_langs: list[str],
    default_title: str,
    default_chapters: list[tuple[str, str, str]],
    landing_desc_by_lang: dict[str, str],
) -> None:
    """Emit ``og_image`` copy, ``sitemap.xml``, ``robots.txt``, and ``llms.txt`` for a ``doc`` build."""
    seo = manifest.seo
    if seo is None:
        return

    ensure_seo_og_image_copied(input_abs, out_dir_abs, seo)
    rel_htmls_by_lang = {lc: ["index.html"] for lc in ordered_langs}
    if seo.sitemap and seo.site_url:
        entries = _build_i18n_sitemap_entries(seo.site_url, i18n_cfg, ordered_langs, rel_htmls_by_lang)
        write_sitemap_xml(out_dir_abs, entries)
    if seo.robots:
        write_robots_txt(out_dir_abs, seo.site_url, include_sitemap=(seo.sitemap and bool(seo.site_url)))
    if seo.llms_txt:
        default_lang = i18n_cfg.default_lang
        base_doc_url = _format_llms_url(seo.site_url, f"{default_lang}/index.html")
        chapter_links = [
            LlmsLink(title=ch_title, url=f"{base_doc_url}#{anchor_id}", description=ch_desc)
            for anchor_id, ch_title, ch_desc in default_chapters
        ]
        sections: list[LlmsSection] = []
        if chapter_links:
            sections.append(LlmsSection(title="Chapters", links=chapter_links))
        locales_sec = _build_locales_llms_section(manifest, i18n_cfg, seo.site_url, landing_desc_by_lang)
        if locales_sec is not None:
            sections.append(locales_sec)

        first_desc = default_chapters[0][2] if default_chapters else ""
        llms_title = manifest.project.title.strip() or default_title
        llms_summary = resolve_localized_description(
            manifest=manifest,
            lang=default_lang,
            page_description=first_desc,
            prefer_manifest=True,
            max_length=240,
        )
        write_llms_txt(out_dir_abs, title=llms_title, summary=llms_summary, sections=sections)


def _prepare_i18n_catalog_locales(
    *,
    input_abs: str,
    out_dir_abs: str,
    ordered_langs: list[str],
    locale_files: dict[str, list[str]],
    css_file: str,
    css_mode: str,
    image_format: str,
) -> tuple[
    dict[str, list[tuple[str, str | None]]],
    dict[str, str | None],
    dict[str, str | None],
    list[str],
    int,
]:
    """Order per-locale catalog files, emit localized ``style.css``, and run duplicate diagram checks."""
    ordered_by_lang: dict[str, list[tuple[str, str | None]]] = {}
    nav_titles_by_lang: dict[str, str | None] = {}
    locale_css_paths: dict[str, str | None] = {}
    raw_css = ""
    if css_mode != "embed":
        with open(css_file, "r", encoding="utf-8") as cf:
            raw_css = cf.read()

    display_names: list[str] = []
    max_blocks = 0

    for lang in ordered_langs:
        lang_dir = os.path.join(input_abs, lang)
        ordered_entries, nav_site_title = order_catalog_locale_files(lang_dir, locale_files[lang])
        ordered_by_lang[lang] = ordered_entries
        nav_titles_by_lang[lang] = nav_site_title

        if css_mode != "embed":
            lang_css_out = os.path.join(out_dir_abs, lang, "style.css")
            os.makedirs(os.path.dirname(lang_css_out), exist_ok=True)
            with open(lang_css_out, "w", encoding="utf-8") as out_cf:
                out_cf.write(localize_css_for_language(raw_css, lang=lang))
            locale_css_paths[lang] = lang_css_out
        else:
            locale_css_paths[lang] = None

        lang_tasks: list[tuple[str, str, bool]] = []
        lang_disp: list[str] = []
        lang_shared_dirs: list[str | None] = []
        for rel_path, _ in ordered_entries:
            src_abs = os.path.join(lang_dir, *rel_path.split("/"))
            is_md = rel_path.lower().endswith((".md", ".markdown"))
            rel_stem, _ = os.path.splitext(rel_path)
            rel_html = f"{rel_stem}.html" if is_md else rel_path
            dest_abs = os.path.join(out_dir_abs, lang, *rel_html.split("/"))
            shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
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

    return ordered_by_lang, nav_titles_by_lang, locale_css_paths, display_names, max_blocks


def _compile_catalog_locale_pages(
    *,
    lang: str,
    ordered_entries: list[tuple[str, str | None]],
    input_abs: str,
    out_dir_abs: str,
    start_step: int,
    total_files: int,
    name_width: int,
    image_width: int,
    image_format: str,
    loc_styles: str | None,
    loc_utils: str | None,
    processor: DrawlibBlockProcessor | None,
    no_cache: bool,
    cache: BuildImageCache,
) -> tuple[list[CompiledCatalogPage], int, DrawlibBlockProcessor | None]:
    """Compile all Markdown/HTML pages in one ``catalog`` locale and upgrade ``H1``–``H4`` headings."""
    compiled: list[CompiledCatalogPage] = []
    step = start_step
    lang_dir = os.path.join(input_abs, lang)

    for rel_path, section_title in ordered_entries:
        step += 1
        src_abs = os.path.join(lang_dir, *rel_path.split("/"))
        is_md = rel_path.lower().endswith((".md", ".markdown"))
        rel_stem, _ = os.path.splitext(rel_path)
        rel_html = f"{rel_stem}.html" if is_md else rel_path
        dest_abs = os.path.join(out_dir_abs, lang, *rel_html.split("/"))
        shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))

        raw_md: str | None = None
        if is_md:
            with open(src_abs, "r", encoding="utf-8") as mf:
                raw_md = mf.read()

        progress = FileBuildProgress(
            step,
            total_files,
            file_name=f"/{lang}/{rel_path}",
            name_width=name_width,
            image_width=image_width,
        )
        body_html, _, doc_desc, processor = _compile_chapter_body(
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
        fallback_stem = os.path.basename(rel_stem)
        h1_title, upgraded_body, subitems = inject_catalog_heading_ids_and_badges(
            body_html=body_html,
            md_text=raw_md,
            fallback_stem=fallback_stem,
        )
        compiled.append(
            CompiledCatalogPage(
                rel_path=rel_path,
                rel_html=rel_html,
                src_abs=src_abs,
                dest_abs=dest_abs,
                section_title=section_title,
                h1_title=h1_title,
                description=doc_desc,
                body_html=upgraded_body,
                subitems=subitems,
            )
        )

    return compiled, step, processor


def _render_single_catalog_page_html(
    *,
    page: CompiledCatalogPage,
    pages: list[CompiledCatalogPage],
    active_index: int,
    dest_abs: str,
    rel_html_for_i18n: str,
    lang: str,
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    catalog_cfg: CatalogConfig,
    site_title: str,
    locale_css_path: str | None,
    css_file: str,
    template_file: str,
    index_url: str,
    rebase_body_from_dir: str | None = None,
    prefer_manifest_description: bool = False,
) -> None:
    """Render and write a single catalog HTML document (page, locale landing, or root index)."""
    body_html = page.body_html
    dest_dir = os.path.dirname(dest_abs)
    if rebase_body_from_dir is not None and os.path.abspath(rebase_body_from_dir) != os.path.abspath(dest_dir):
        body_html = rebase_html_relative_urls(
            html=body_html,
            from_dir=rebase_body_from_dir,
            to_dir=dest_dir,
            skip_prefixes=(),
        )

    catalog_nav_sections, catalog_pager = build_catalog_page_navigation_context(
        pages=pages,
        active_index=active_index,
        current_dest_abs=dest_abs,
        sidebar_expanded=catalog_cfg.sidebar_expanded,
    )
    chrome_ctx = resolve_catalog_chrome_context(
        catalog_cfg=catalog_cfg,
        lang=lang,
        default_lang=i18n_cfg.default_lang,
        lang_out_dir=os.path.join(out_dir_abs, lang),
        current_dest_abs=dest_abs,
    )
    extra_ctx: dict[str, Any] = {
        **chrome_ctx,
        "catalog_nav_sections": catalog_nav_sections,
        "catalog_pager": catalog_pager,
        "current_page_title": page.h1_title,
    }

    rel_css_href = os.path.relpath(locale_css_path, dest_dir).replace(os.sep, "/") if locale_css_path else None
    favicon_href = resolve_favicon_href(input_abs, out_dir_abs, dest_abs)
    logo_href, logo_dark_href = resolve_logo_hrefs(input_abs, out_dir_abs, dest_abs)
    languages_ctx, alt_links = build_language_switcher_context(
        config=i18n_cfg,
        out_dir_abs=out_dir_abs,
        rel_html_path=rel_html_for_i18n,
        current_dest_abs=dest_abs,
        active_lang=lang,
    )
    seo_meta_html, eff_alt_links = _resolve_page_seo_and_alternates(
        manifest=manifest,
        out_dir_abs=out_dir_abs,
        dest_abs=dest_abs,
        lang=lang,
        page_title=page.h1_title,
        site_title=site_title,
        page_description=page.description,
        prefer_manifest_description=prefer_manifest_description,
        alternate_links=alt_links,
    )
    lang_cfg = get_language_config(lang)
    full_html = render_html_document(
        body_html=body_html,
        title=page.h1_title,
        custom_css_path=css_file,
        css_href=rel_css_href,
        nav_items=[],
        nav_sections=None,
        template_path=template_file,
        index_url=index_url,
        site_title=site_title,
        favicon_href=favicon_href,
        logo_href=logo_href,
        logo_dark_href=logo_dark_href,
        html_lang=lang_cfg.code,
        html_dir=lang_cfg.direction,
        font_link_html=lang_cfg.font_link_html,
        languages=languages_ctx,
        alternate_links=eff_alt_links,
        css_lang=lang,
        seo_meta_html=seo_meta_html,
        css_target="catalog",
        extra_context=extra_ctx,
    )
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_abs, "w", encoding="utf-8") as out_f:
        out_f.write(full_html)


def _build_catalog_llms_sections(
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    site_url: str,
    default_pages: list[CompiledCatalogPage],
    landing_desc_by_lang: dict[str, str],
) -> list[LlmsSection]:
    """Organize default-locale ``catalog`` categories and ``H2`` items into ``LlmsSection`` blocks."""
    default_lang = i18n_cfg.default_lang
    grouped: list[tuple[str, list[LlmsLink]]] = []

    for page in default_pages:
        sec_title = page.section_title or "Catalog"
        desc = page.description
        if not desc and page.subitems:
            preview_syms = ", ".join(sub.sidebar_label for sub in page.subitems[:6])
            desc = f"Items: {preview_syms}"
        link = LlmsLink(
            title=page.h1_title,
            url=_format_llms_url(site_url, f"{default_lang}/{page.rel_html}"),
            description=desc,
        )
        if not grouped or grouped[-1][0] != sec_title:
            grouped.append((sec_title, [link]))
        else:
            grouped[-1][1].append(link)

    sections = [LlmsSection(title=sec_name, links=links) for sec_name, links in grouped if links]
    locales_sec = _build_locales_llms_section(manifest, i18n_cfg, site_url, landing_desc_by_lang)
    if locales_sec is not None:
        sections.append(locales_sec)
    return sections


def _emit_catalog_seo_files(
    *,
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    ordered_langs: list[str],
    rel_htmls_by_lang: dict[str, list[str]],
    default_pages: list[CompiledCatalogPage],
    default_site_title: str,
    landing_desc_by_lang: dict[str, str],
) -> None:
    """Emit ``og_image`` copy, ``sitemap.xml``, ``robots.txt``, and ``llms.txt`` for a ``catalog`` build."""
    seo = manifest.seo
    if seo is None:
        return

    ensure_seo_og_image_copied(input_abs, out_dir_abs, seo)
    if seo.sitemap and seo.site_url:
        entries = _build_i18n_sitemap_entries(seo.site_url, i18n_cfg, ordered_langs, rel_htmls_by_lang)
        write_sitemap_xml(out_dir_abs, entries)
    if seo.robots:
        write_robots_txt(out_dir_abs, seo.site_url, include_sitemap=(seo.sitemap and bool(seo.site_url)))
    if seo.llms_txt:
        first_desc = default_pages[0].description if default_pages else ""
        llms_title = manifest.project.title.strip() or default_site_title
        llms_summary = resolve_localized_description(
            manifest=manifest,
            lang=i18n_cfg.default_lang,
            page_description=first_desc,
            prefer_manifest=True,
            max_length=240,
        )
        sections = _build_catalog_llms_sections(
            manifest=manifest,
            i18n_cfg=i18n_cfg,
            site_url=seo.site_url,
            default_pages=default_pages,
            landing_desc_by_lang=landing_desc_by_lang,
        )
        write_llms_txt(out_dir_abs, title=llms_title, summary=llms_summary, sections=sections)


def _render_catalog_locale_outputs(
    *,
    lang: str,
    pages: list[CompiledCatalogPage],
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    catalog_cfg: CatalogConfig,
    site_title: str,
    locale_css_path: str | None,
    css_file: str,
    template_file: str,
) -> list[str]:
    """Render all page HTMLs for one ``catalog`` locale plus a ``<lang>/index.html`` landing alias if needed."""
    lang_index_dest = os.path.join(out_dir_abs, lang, "index.html")
    rel_htmls: list[str] = []
    has_explicit_index = any(p.rel_html == "index.html" for p in pages)

    for idx, page in enumerate(pages):
        rel_index_url = os.path.relpath(lang_index_dest, os.path.dirname(page.dest_abs)).replace(os.sep, "/")
        _render_single_catalog_page_html(
            page=page,
            pages=pages,
            active_index=idx,
            dest_abs=page.dest_abs,
            rel_html_for_i18n=page.rel_html,
            lang=lang,
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            manifest=manifest,
            i18n_cfg=i18n_cfg,
            catalog_cfg=catalog_cfg,
            site_title=site_title,
            locale_css_path=locale_css_path,
            css_file=css_file,
            template_file=template_file,
            index_url=rel_index_url,
            prefer_manifest_description=(idx == 0 and page.rel_html == "index.html"),
        )
        rel_htmls.append(page.rel_html)

    if not has_explicit_index and pages:
        first_page = pages[0]
        _render_single_catalog_page_html(
            page=first_page,
            pages=pages,
            active_index=0,
            dest_abs=lang_index_dest,
            rel_html_for_i18n="index.html",
            lang=lang,
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            manifest=manifest,
            i18n_cfg=i18n_cfg,
            catalog_cfg=catalog_cfg,
            site_title=site_title,
            locale_css_path=locale_css_path,
            css_file=css_file,
            template_file=template_file,
            index_url="index.html",
            rebase_body_from_dir=os.path.dirname(first_page.dest_abs),
            prefer_manifest_description=True,
        )
        rel_htmls.insert(0, "index.html")

    return rel_htmls


def _build_i18n_catalog_html(
    *,
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    image_format: str,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    css_mode: str,
    workers: int = 1,
) -> str:
    """Compile an i18n-native ``catalog`` directory into multi-page HTML."""
    if out_dir_abs == input_abs:
        raise ValueError(
            f'Refusing to build HTML in-place inside source directory "{input_abs}". '
            "Please specify a separate output directory."
        )

    template_file, css_file = resolve_template_and_css(input_abs)
    locale_files = validate_i18n_project(input_abs, i18n_cfg, project_type="catalog", default_format=image_format)
    catalog_cfg = manifest.catalog if manifest.catalog is not None else CatalogConfig()

    default_lang = i18n_cfg.default_lang
    ordered_langs = [default_lang] + [lc for lc in i18n_cfg.langs if lc != default_lang]
    ordered_by_lang, nav_titles_by_lang, locale_css_paths, display_names, max_blocks = _prepare_i18n_catalog_locales(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        ordered_langs=ordered_langs,
        locale_files=locale_files,
        css_file=css_file,
        css_mode=css_mode,
        image_format=image_format,
    )

    root_disp = "/index.html"
    total_files = len(display_names) + 1
    name_width = max((len(n) for n in [*display_names, root_disp]), default=0)
    image_width = len(str(max(max_blocks, 0)))
    cache = BuildImageCache(enabled=not no_cache)
    processors_by_cfg: dict[tuple[str | None, str | None], DrawlibBlockProcessor | None] = {}
    locale_styles_utils: dict[str, tuple[str | None, str | None]] = {
        lc: resolve_styles_and_utils(os.path.join(input_abs, lc), styles_path, utils_path) for lc in ordered_langs
    }

    if workers > 1:
        cat_jobs: list[BlockRenderJob] = []
        for lang in ordered_langs:
            loc_styles, loc_utils = locale_styles_utils[lang]
            lang_dir = os.path.join(input_abs, lang)
            for rel_path, _ in ordered_by_lang[lang]:
                src_abs = os.path.join(lang_dir, *rel_path.split("/"))
                is_md = rel_path.lower().endswith((".md", ".markdown"))
                rel_stem, _ = os.path.splitext(rel_path)
                rel_html = f"{rel_stem}.html" if is_md else rel_path
                dest_abs = os.path.join(out_dir_abs, lang, *rel_html.split("/"))
                shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
                cat_jobs.extend(
                    collect_standard_document_block_jobs(
                        src_abs=src_abs,
                        dest_abs=dest_abs,
                        is_md=is_md,
                        image_format=image_format,
                        embed_images=False,
                        styles_path=loc_styles,
                        utils_path=loc_utils,
                        project_root=input_abs,
                        shared_images_dir=shared_dir,
                        require_file=True,
                        no_cache_global=no_cache,
                    )
                )
        prerender_document_blocks(cat_jobs, cache=cache, workers=workers)

    pages_by_lang: dict[str, list[CompiledCatalogPage]] = {}
    rel_htmls_by_lang: dict[str, list[str]] = {}
    landing_desc_by_lang: dict[str, str] = {}
    step_idx = 0

    for lang in ordered_langs:
        loc_styles, loc_utils = locale_styles_utils[lang]
        cfg_key = (loc_styles, loc_utils)
        pages, step_idx, next_proc = _compile_catalog_locale_pages(
            lang=lang,
            ordered_entries=ordered_by_lang[lang],
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            start_step=step_idx,
            total_files=total_files,
            name_width=name_width,
            image_width=image_width,
            image_format=image_format,
            loc_styles=loc_styles,
            loc_utils=loc_utils,
            processor=processors_by_cfg.get(cfg_key),
            no_cache=no_cache,
            cache=cache,
        )
        processors_by_cfg[cfg_key] = next_proc
        pages_by_lang[lang] = pages
        landing_desc_by_lang[lang] = pages[0].description if pages else ""
        loc_site_title = manifest.project.title.strip() or nav_titles_by_lang[lang] or "Catalog"
        rel_htmls_by_lang[lang] = _render_catalog_locale_outputs(
            lang=lang,
            pages=pages,
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            manifest=manifest,
            i18n_cfg=i18n_cfg,
            catalog_cfg=catalog_cfg,
            site_title=loc_site_title,
            locale_css_path=locale_css_paths[lang],
            css_file=css_file,
            template_file=template_file,
        )

    default_pages = pages_by_lang[default_lang]
    default_site_title = manifest.project.title.strip() or nav_titles_by_lang[default_lang] or "Catalog"
    root_progress = FileBuildProgress(
        total_files,
        total_files,
        file_name=root_disp,
        name_width=name_width,
        image_width=image_width,
    )
    root_progress.update(0, 0, done=False)
    if default_pages:
        first_def_page = default_pages[0]
        _render_single_catalog_page_html(
            page=first_def_page,
            pages=default_pages,
            active_index=0,
            dest_abs=os.path.join(out_dir_abs, "index.html"),
            rel_html_for_i18n="index.html",
            lang=default_lang,
            input_abs=input_abs,
            out_dir_abs=out_dir_abs,
            manifest=manifest,
            i18n_cfg=i18n_cfg,
            catalog_cfg=catalog_cfg,
            site_title=default_site_title,
            locale_css_path=locale_css_paths[default_lang],
            css_file=css_file,
            template_file=template_file,
            index_url="index.html",
            rebase_body_from_dir=os.path.dirname(first_def_page.dest_abs),
            prefer_manifest_description=True,
        )
    root_progress.update(0, 0, done=True)

    copy_directory_assets(input_abs, out_dir_abs, excluded_files={template_file, css_file})
    for css_out in locale_css_paths.values():
        if css_out is not None:
            bundle_svg_fonts(out_dir_abs, css_file_path=css_out)

    _emit_catalog_seo_files(
        input_abs=input_abs,
        out_dir_abs=out_dir_abs,
        manifest=manifest,
        i18n_cfg=i18n_cfg,
        ordered_langs=ordered_langs,
        rel_htmls_by_lang=rel_htmls_by_lang,
        default_pages=default_pages,
        default_site_title=default_site_title,
        landing_desc_by_lang=landing_desc_by_lang,
    )

    readme_out = os.path.join(out_dir_abs, "README.md")
    if not os.path.exists(readme_out):
        os.makedirs(out_dir_abs, exist_ok=True)
        with open(readme_out, "w", encoding="utf-8") as f:
            f.write(get_html_readme())

    return out_dir_abs



