# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Jupyter / Google Colab (.ipynb + HTML preview + Dry-Run) compiler for drawlib."""

from __future__ import annotations

import importlib.resources
import os
import tempfile
from typing import Any, Literal

from drawlib._builder._common import (
    BlockRenderJob,
    BuildImageCache,
    FileBuildProgress,
    I18nConfig,
    JupyterConfig,
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
from drawlib._builder.doc_builder.compiler.base import (
    copy_directory_assets,
    extract_title,
    resolve_doc_locale_and_root,
    validate_markdown_images,
    validate_markdown_links,
)
from drawlib._builder.doc_builder.compiler.html import (
    resolve_favicon_href,
    resolve_logo_hrefs,
)
from drawlib._builder.doc_builder.exporter_html import render_html_document
from drawlib._builder.doc_builder.exporter_jupyter import (
    NotebookExecutionResult,
    NotebookSegment,
    build_ipynb_dict,
    execute_notebook_cells,
    parse_notebook_segments,
    render_notebook_body_html,
    write_ipynb_file,
)
from drawlib._builder.doc_builder.i18n import (
    build_language_switcher_context,
    rebase_html_relative_urls,
    validate_i18n_project,
)
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.doc_builder.progress import check_document_output_duplicates
from drawlib._templates import get_css, get_html_readme, localize_css_for_language
from drawlib._templates.langs import get_language_config


def _resolve_default_jupyter_out_dir(input_abs: str, output_dir: str | None) -> str:
    """Resolve output Jupyter directory path, defaulting to ``<parent>/<base>_jupyter``."""
    if output_dir:
        return os.path.abspath(output_dir)
    dir_name = os.path.basename(input_abs.rstrip(os.sep))
    base_name = dir_name[:-4] if dir_name.endswith("_src") and len(dir_name) > 4 else (dir_name or "jupyter")
    return os.path.join(os.path.dirname(input_abs), f"{base_name}_jupyter")


def _resolve_jupyter_template_and_css(
    input_abs: str,
    style_name: str = "default",
) -> tuple[str, str, tempfile.TemporaryDirectory[str] | None]:
    """Resolve ``(template_path, css_content, temp_dir_holder)`` for a Jupyter project."""
    cand_tmpl = os.path.join(input_abs, "template.html")
    cand_css = os.path.join(input_abs, "style.css")

    raw_css = ""
    if os.path.isfile(cand_css):
        with open(cand_css, "r", encoding="utf-8") as f:
            raw_css = f.read()
    else:
        try:
            raw_css = get_css(name=style_name, target="jupyter", lang="en")
        except ValueError:
            raw_css = get_css(name="default", target="html", lang="en")

    if os.path.isfile(cand_tmpl):
        return cand_tmpl, raw_css, None

    tmp_holder = tempfile.TemporaryDirectory(prefix="drawlib_jupyter_tmpl_")
    res = importlib.resources.files("drawlib._templates")
    try:
        tmpl_text = res.joinpath("project", "jupyter", "template.html.template").read_text(encoding="utf-8")
    except FileNotFoundError:
        tmpl_text = res.joinpath("project", "site", "template.html.template").read_text(encoding="utf-8")
    fallback_tmpl = os.path.join(tmp_holder.name, "template.html")
    with open(fallback_tmpl, "w", encoding="utf-8") as f:
        f.write(tmpl_text)
    return fallback_tmpl, raw_css, tmp_holder


def _render_markdown_mode_drawlib_segments(
    segments: list[NotebookSegment],
    *,
    processor: DrawlibBlockProcessor,
    source_abs: str,
    progress: FileBuildProgress | None = None,
) -> None:
    """Render all ``cell_mode == 'markdown'`` Drawlib diagram segments to their target image files."""
    file_dir = os.path.dirname(source_abs)
    exec_dir = file_dir
    if (
        processor.project_root
        and not os.path.exists(os.path.join(file_dir, "_assets"))
        and os.path.exists(os.path.join(processor.project_root, "_assets"))
    ):
        exec_dir = processor.project_root

    md_segs = [seg for seg in segments if seg.kind == "drawlib" and seg.cell_mode == "markdown" and seg.target_img_path]
    total_steps = len(md_segs)

    orig_cwd = os.getcwd()
    try:
        if os.path.isdir(exec_dir):
            os.chdir(exec_dir)
        for step_idx, seg in enumerate(md_segs, start=1):
            if seg.target_img_path is None:
                continue
            block_no_cache = bool(seg.drawlib_options and seg.drawlib_options.no_cache)
            processor.render_block_to_file(
                code=seg.source,
                target_file_path=seg.target_img_path,
                source_filename=source_abs,
                no_cache=block_no_cache,
            )
            if progress is not None:
                progress.update(step_idx, total_steps, done=False)
    finally:
        os.chdir(orig_cwd)


def _build_single_jupyter_file(
    src_abs: str,
    output_path: str | None,
    *,
    image_format: str,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    execute: bool | None,
    dry_run: bool,
) -> str:
    """Compile or dry-run a single ``.md`` notebook file."""
    ext = os.path.splitext(src_abs)[1].lower()
    if ext not in {".md", ".markdown"}:
        raise ValueError(f'Single-file Jupyter build requires a Markdown (.md) file, got "{src_abs}".')

    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    validate_markdown_links(src_abs, content)
    validate_markdown_images(src_abs, content)

    lang, manifest, proj_root = resolve_doc_locale_and_root(src_abs)
    loc_styles, loc_utils = resolve_styles_and_utils(os.path.dirname(src_abs), styles_path, utils_path)
    jupyter_cfg = manifest.jupyter if (manifest is not None and manifest.jupyter is not None) else JupyterConfig()
    eff_execute = True if dry_run else (execute if execute is not None else jupyter_cfg.execute)
    doc_base_name = os.path.splitext(os.path.basename(src_abs))[0]

    with tempfile.TemporaryDirectory(prefix="drawlib_jupyter_single_") as tmp_dir:
        if dry_run:
            target_out_dir = tmp_dir
            ipynb_dest = os.path.join(tmp_dir, f"{doc_base_name}.ipynb")
        elif output_path:
            out_abs = os.path.abspath(output_path)
            if out_abs.lower().endswith(".ipynb"):
                ipynb_dest = out_abs
                target_out_dir = os.path.dirname(out_abs)
            else:
                target_out_dir = out_abs
                ipynb_dest = os.path.join(out_abs, f"{doc_base_name}.ipynb")
        else:
            target_out_dir = os.path.dirname(src_abs)
            ipynb_dest = os.path.join(target_out_dir, f"{doc_base_name}.ipynb")

        segments = parse_notebook_segments(
            content,
            doc_base_name=doc_base_name,
            output_dir=target_out_dir,
            default_format=image_format,
            default_drawlib_cell_mode=jupyter_cfg.drawlib_cell_mode,
            require_file=True,
        )

        processor = DrawlibBlockProcessor(
            styles_path=loc_styles,
            utils_path=loc_utils,
            no_cache=no_cache,
            project_root=proj_root,
        )
        _render_markdown_mode_drawlib_segments(
            segments,
            processor=processor,
            source_abs=src_abs,
        )

        exec_result: NotebookExecutionResult | None = None
        if eff_execute:
            exec_result = execute_notebook_cells(
                segments,
                source_path=src_abs,
                styles_path=loc_styles,
                utils_path=loc_utils,
                project_root=proj_root,
                doc_base_name=doc_base_name,
                output_dir=target_out_dir,
            )

        if dry_run:
            cell_cnt = exec_result.executed_cell_count if exec_result is not None else 0
            print(f"[Dry-Run] Verified '{src_abs}' ({cell_cnt} code cell(s) executed).")
            return src_abs

        rel_nb = f"{lang}/{doc_base_name}.ipynb" if (manifest and manifest.is_i18n) else f"{doc_base_name}.ipynb"
        colab_url = jupyter_cfg.build_colab_url(rel_nb)
        site_url = manifest.seo.site_url if (manifest and manifest.seo) else ""
        ipynb_dict = build_ipynb_dict(
            segments,
            image_mode=jupyter_cfg.image_mode,
            colab_url=colab_url,
            setup_packages=jupyter_cfg.setup_packages,
            site_url=site_url,
            lang=lang if (manifest and manifest.is_i18n) else None,
            notebook_name=os.path.basename(ipynb_dest),
        )
        write_ipynb_file(ipynb_dict, ipynb_dest)
        return ipynb_dest


def build_jupyter(
    input_path: str,
    output_dir: str | None = None,
    *,
    image_format: str = "png",
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
    execute: bool | None = None,
    dry_run: bool = False,
    css_mode: str = "external",
    workers: int | Literal["auto"] = "auto",
) -> str:
    """Compile a ``jupyter`` project directory or single ``.md`` file into ``.ipynb`` and HTML preview.

    Args:
        input_path: Project root directory containing ``drawlib.toml`` or a single ``.md`` file.
        output_dir: Target output directory (or ``.ipynb`` file path in single-file mode).
        image_format: Default diagram image format ('png', 'webp', or 'svg'). Defaults to 'png'.
        styles_path: Optional path to custom ``styles.py``.
        utils_path: Optional path to custom ``utils.py``.
        no_cache: If True, disable reading/writing the SQLite build image cache.
        execute: Whether to sequentially dry-run code cells in-process (defaults to ``[jupyter].execute``).
        dry_run: If True, execute and verify all cells/diagrams in a temporary directory without writing output.
        css_mode: CSS linking mode for HTML preview ('external' or 'embed').
        workers: Number of parallel rendering worker processes ('auto' or int >= 1).

    Returns:
        str: Absolute path of generated output directory (or file path in single-file mode).
    """
    abs_in = os.path.abspath(input_path)
    if not os.path.exists(abs_in):
        raise ValueError(f'Input path "{abs_in}" does not exist.')

    if os.path.isfile(abs_in):
        return _build_single_jupyter_file(
            abs_in,
            output_dir,
            image_format=image_format,
            styles_path=styles_path,
            utils_path=utils_path,
            no_cache=no_cache,
            execute=execute,
            dry_run=dry_run,
        )

    eff_workers = resolve_build_workers(workers)
    manifest = load_project_manifest(abs_in)
    if manifest is None:
        found = find_project_manifest(abs_in, max_up=3)
        if found is not None:
            proj_root, _ = found
            raise ValueError(
                f'Input directory "{abs_in}" is a subdirectory inside project "{proj_root}". '
                f'Please pass the project root directory "{proj_root}" containing "drawlib.toml".'
            )
        raise ValueError(
            f'Missing required "drawlib.toml" in "{abs_in}". '
            'Run "drawlib init project jupyter" to initialize a Jupyter/Colab project.'
        )

    if manifest.project.type != "jupyter":
        raise ValueError(
            f'Input directory "{abs_in}" has project type "{manifest.project.type}" in drawlib.toml; '
            'expected type = "jupyter".'
        )
    if manifest.i18n is None:
        raise ValueError(f'Invalid "{abs_in}/drawlib.toml": "[i18n]" configuration is required.')

    i18n_cfg: I18nConfig = manifest.i18n
    jupyter_cfg: JupyterConfig = manifest.jupyter or JupyterConfig()
    eff_execute = True if dry_run else (execute if execute is not None else jupyter_cfg.execute)

    locale_files = validate_i18n_project(
        abs_in,
        i18n_cfg,
        project_type="jupyter",
        default_format=image_format,
    )
    default_lang = i18n_cfg.default_lang
    ordered_langs = [default_lang] + [lc for lc in i18n_cfg.langs if lc != default_lang]

    if dry_run:
        with tempfile.TemporaryDirectory(prefix="drawlib_jupyter_dryrun_") as tmp_out:
            _compile_jupyter_locales(
                input_abs=abs_in,
                out_dir_abs=tmp_out,
                manifest=manifest,
                i18n_cfg=i18n_cfg,
                jupyter_cfg=jupyter_cfg,
                ordered_langs=ordered_langs,
                locale_files=locale_files,
                image_format=image_format,
                styles_path=styles_path,
                utils_path=utils_path,
                no_cache=no_cache,
                execute=eff_execute,
                dry_run=True,
                css_mode=css_mode,
                workers=eff_workers,
            )
        return abs_in

    out_dir_abs = _resolve_default_jupyter_out_dir(abs_in, output_dir)
    if out_dir_abs == abs_in:
        raise ValueError(
            f'Refusing to build Jupyter project in-place inside source directory "{abs_in}". '
            "Please specify a separate output directory."
        )

    _compile_jupyter_locales(
        input_abs=abs_in,
        out_dir_abs=out_dir_abs,
        manifest=manifest,
        i18n_cfg=i18n_cfg,
        jupyter_cfg=jupyter_cfg,
        ordered_langs=ordered_langs,
        locale_files=locale_files,
        image_format=image_format,
        styles_path=styles_path,
        utils_path=utils_path,
        no_cache=no_cache,
        execute=eff_execute,
        dry_run=False,
        css_mode=css_mode,
        workers=eff_workers,
    )
    return out_dir_abs


def _compile_jupyter_locales(
    *,
    input_abs: str,
    out_dir_abs: str,
    manifest: ProjectManifest,
    i18n_cfg: I18nConfig,
    jupyter_cfg: JupyterConfig,
    ordered_langs: list[str],
    locale_files: dict[str, list[str]],
    image_format: str,
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    execute: bool,
    dry_run: bool,
    css_mode: str,
    workers: int,
) -> None:
    """Compile all locales for a ``jupyter`` project."""
    tmpl_file, raw_css, tmp_holder = _resolve_jupyter_template_and_css(input_abs, manifest.project.style)
    try:
        all_disp_names: list[str] = []
        max_blocks = 0
        locale_css_paths: dict[str, str | None] = {}

        for lang in ordered_langs:
            lang_out_dir = os.path.join(out_dir_abs, lang)
            if not dry_run and css_mode != "embed":
                lang_css_out = os.path.join(lang_out_dir, "style.css")
                os.makedirs(os.path.dirname(lang_css_out), exist_ok=True)
                with open(lang_css_out, "w", encoding="utf-8") as cf:
                    cf.write(localize_css_for_language(raw_css, lang=lang))
                locale_css_paths[lang] = lang_css_out
            else:
                locale_css_paths[lang] = None

            lang_tasks: list[tuple[str, str, bool]] = []
            lang_disp: list[str] = []
            lang_shared_dirs: list[str | None] = []
            for rel_path in locale_files[lang]:
                src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
                rel_stem, _ = os.path.splitext(rel_path)
                dest_abs = os.path.join(lang_out_dir, f"{rel_stem}.html")
                shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
                disp = f"/{lang}/{rel_path}"
                all_disp_names.append(disp)
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

        total_files = len(all_disp_names) + (0 if dry_run else 1)
        name_width = max((len(n) for n in [*all_disp_names, "/index.html"]), default=0)
        image_width = len(str(max(max_blocks, 0)))
        cache = BuildImageCache(enabled=not no_cache)
        locale_styles_utils: dict[str, tuple[str | None, str | None]] = {
            lc: resolve_styles_and_utils(os.path.join(input_abs, lc), styles_path, utils_path) for lc in ordered_langs
        }

        if workers > 1 and jupyter_cfg.drawlib_cell_mode == "markdown":
            jobs: list[BlockRenderJob] = []
            for lang in ordered_langs:
                loc_styles, loc_utils = locale_styles_utils[lang]
                lang_out_dir = os.path.join(out_dir_abs, lang)
                for rel_path in locale_files[lang]:
                    src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
                    rel_stem, _ = os.path.splitext(rel_path)
                    dest_abs = os.path.join(lang_out_dir, f"{rel_stem}.html")
                    shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
                    jobs.extend(
                        collect_standard_document_block_jobs(
                            src_abs=src_abs,
                            dest_abs=dest_abs,
                            is_md=True,
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
            prerender_document_blocks(jobs, cache=cache, workers=workers)

        if not dry_run:
            for lang in ordered_langs:
                copy_directory_assets(os.path.join(input_abs, lang), os.path.join(out_dir_abs, lang))
            for sub in ("_assets", "assets"):
                cand_assets = os.path.join(input_abs, sub)
                if os.path.isdir(cand_assets):
                    copy_directory_assets(cand_assets, os.path.join(out_dir_abs, sub))

        global_step = 0
        default_lang = i18n_cfg.default_lang
        default_first_html = ""
        default_first_lang_dir = os.path.join(out_dir_abs, default_lang)
        site_title = manifest.project.title.strip() or "Drawlib Notebooks"
        site_url = manifest.seo.site_url if manifest.seo else ""
        rel_htmls_by_lang: dict[str, list[str]] = {lc: [] for lc in ordered_langs}
        llms_sections: list[LlmsSection] = []

        for lang in ordered_langs:
            lang_out_dir = os.path.join(out_dir_abs, lang)
            loc_styles, loc_utils = locale_styles_utils[lang]
            lang_cfg = get_language_config(lang)
            processor = DrawlibBlockProcessor(
                styles_path=loc_styles,
                utils_path=loc_utils,
                no_cache=no_cache,
                cache=cache,
                project_root=input_abs,
            )

            # Pre-extract titles for sidebar navigation across all notebooks in this locale
            nb_entries: list[tuple[str, str, str]] = []
            for rel_path in locale_files[lang]:
                src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
                with open(src_abs, "r", encoding="utf-8") as f:
                    md_raw = f.read()
                rel_stem, _ = os.path.splitext(rel_path)
                rel_html = f"{rel_stem}.html"
                nb_title = extract_title(md_raw, os.path.basename(src_abs))
                nb_entries.append((rel_path, rel_html, nb_title))

            llms_links: list[LlmsLink] = []
            first_rendered_html = ""
            has_explicit_index = False

            for rel_path, rel_html, nb_title in nb_entries:
                global_step += 1
                src_abs = os.path.join(input_abs, lang, *rel_path.split("/"))
                rel_stem, _ = os.path.splitext(rel_path)
                if rel_stem == "index":
                    has_explicit_index = True
                dest_html_abs = os.path.join(lang_out_dir, *rel_html.split("/"))
                dest_ipynb_abs = os.path.join(lang_out_dir, *(f"{rel_stem}.ipynb").split("/"))
                shared_dir = os.path.join(out_dir_abs, "images", *rel_stem.split("/"))
                doc_base_name = os.path.basename(rel_stem)

                with open(src_abs, "r", encoding="utf-8") as f:
                    content = f.read()

                validate_markdown_links(src_abs, content)
                validate_markdown_images(src_abs, content)

                segments = parse_notebook_segments(
                    content,
                    doc_base_name=doc_base_name,
                    output_dir=os.path.dirname(dest_html_abs),
                    shared_images_dir=shared_dir,
                    default_format=image_format,
                    default_drawlib_cell_mode=jupyter_cfg.drawlib_cell_mode,
                    require_file=True,
                )

                md_drawlib_count = sum(
                    1 for s in segments if s.kind == "drawlib" and s.cell_mode == "markdown"
                )
                progress = FileBuildProgress(
                    global_step,
                    total_files,
                    file_name=f"/{lang}/{rel_path}",
                    name_width=name_width,
                    image_width=image_width,
                )
                progress.update(0, md_drawlib_count, done=False)

                _render_markdown_mode_drawlib_segments(
                    segments,
                    processor=processor,
                    source_abs=src_abs,
                    progress=progress,
                )

                exec_result: NotebookExecutionResult | None = None
                if execute:
                    exec_result = execute_notebook_cells(
                        segments,
                        source_path=src_abs,
                        styles_path=loc_styles,
                        utils_path=loc_utils,
                        project_root=input_abs,
                        doc_base_name=doc_base_name,
                        output_dir=os.path.dirname(dest_html_abs),
                        shared_images_dir=shared_dir,
                    )

                progress.update(md_drawlib_count, md_drawlib_count, done=True)
                if dry_run:
                    continue

                rel_nb_in_out = f"{lang}/{rel_stem}.ipynb"
                colab_url = jupyter_cfg.build_colab_url(rel_nb_in_out)
                ipynb_dict = build_ipynb_dict(
                    segments,
                    image_mode=jupyter_cfg.image_mode,
                    colab_url=colab_url,
                    setup_packages=jupyter_cfg.setup_packages,
                    site_url=site_url,
                    lang=lang,
                    notebook_name=os.path.basename(dest_ipynb_abs),
                )
                write_ipynb_file(ipynb_dict, dest_ipynb_abs)

                ipynb_href = os.path.basename(dest_ipynb_abs)
                body_html = render_notebook_body_html(
                    segments,
                    execution_result=exec_result,
                    ipynb_href=ipynb_href,
                    colab_url=colab_url,
                    setup_packages=jupyter_cfg.setup_packages,
                )

                cur_dir = os.path.dirname(dest_html_abs)
                nav_items: list[dict[str, Any]] = []
                for _, item_rel_html, item_title in nb_entries:
                    item_target = os.path.join(lang_out_dir, *item_rel_html.split("/"))
                    item_href = os.path.relpath(item_target, cur_dir).replace(os.sep, "/")
                    nav_items.append(
                        {
                            "title": item_title,
                            "url": item_href,
                            "active": (item_rel_html == rel_html),
                            "is_external": False,
                        }
                    )

                css_path = locale_css_paths[lang]
                css_href = os.path.relpath(css_path, cur_dir).replace(os.sep, "/") if css_path else None
                index_target = os.path.join(lang_out_dir, "index.html")
                index_url = os.path.relpath(index_target, cur_dir).replace(os.sep, "/")
                favicon_href = resolve_favicon_href(input_abs, out_dir_abs, dest_html_abs)
                logo_href, logo_dark_href = resolve_logo_hrefs(input_abs, out_dir_abs, dest_html_abs)
                languages, alternate_links = build_language_switcher_context(
                    config=i18n_cfg,
                    out_dir_abs=out_dir_abs,
                    rel_html_path=rel_html,
                    current_dest_abs=dest_html_abs,
                    active_lang=lang,
                )

                page_desc = extract_markdown_description(content) or resolve_localized_description(manifest, lang)
                seo_meta_html: str | None = None
                if manifest.seo is not None:
                    if alternate_links and manifest.seo.site_url:
                        alternate_links = upgrade_alternate_links(
                            alternate_links,
                            manifest.seo.site_url,
                            out_dir_abs,
                            dest_html_abs,
                        )
                    page_seo = build_page_seo_metadata(
                        manifest=manifest,
                        out_dir_abs=out_dir_abs,
                        dest_abs=dest_html_abs,
                        lang=lang,
                        page_title=nb_title,
                        site_title=site_title,
                        page_description=page_desc,
                        prefer_manifest_description=False,
                    )
                    seo_meta_html = render_seo_head_tags(page_seo) if page_seo is not None else None
                    pub_url = (
                        resolve_public_page_url(manifest.seo.site_url, f"{lang}/{rel_html}")
                        if manifest.seo.site_url
                        else f"/{lang}/{rel_html}"
                    )
                    llms_links.append(
                        LlmsLink(
                            title=nb_title,
                            url=pub_url,
                            description=page_desc,
                        )
                    )

                rel_htmls_by_lang[lang].append(rel_html)
                rendered_html = render_html_document(
                    body_html=body_html,
                    title=nb_title,
                    custom_css_path=None,
                    css_href=css_href,
                    nav_items=nav_items,
                    nav_sections=None,
                    template_path=tmpl_file,
                    index_url=index_url,
                    site_title=site_title,
                    favicon_href=favicon_href,
                    logo_href=logo_href,
                    logo_dark_href=logo_dark_href,
                    html_lang=lang_cfg.code,
                    html_dir=lang_cfg.direction,
                    font_link_html=lang_cfg.font_link_html,
                    languages=languages,
                    alternate_links=alternate_links,
                    css_lang=lang,
                    seo_meta_html=seo_meta_html,
                    css_target="jupyter",
                )
                os.makedirs(os.path.dirname(dest_html_abs), exist_ok=True)
                with open(dest_html_abs, "w", encoding="utf-8") as out_f:
                    out_f.write(rendered_html)

                if not first_rendered_html:
                    first_rendered_html = rendered_html

            if not dry_run and not has_explicit_index and first_rendered_html:
                lang_index_abs = os.path.join(lang_out_dir, "index.html")
                with open(lang_index_abs, "w", encoding="utf-8") as idx_f:
                    idx_f.write(first_rendered_html)
                if "index.html" not in rel_htmls_by_lang[lang]:
                    rel_htmls_by_lang[lang].insert(0, "index.html")

            if lang == default_lang:
                default_first_html = first_rendered_html
            if llms_links:
                llms_sections.append(LlmsSection(title=f"Notebooks ({lang})", links=llms_links))

        if dry_run:
            return

        # Write root /index.html rebased from <default_lang>/index.html
        global_step += 1
        root_progress = FileBuildProgress(
            global_step,
            total_files,
            file_name="/index.html",
            name_width=name_width,
            image_width=image_width,
        )
        root_progress.update(0, 0, done=False)
        root_index_abs = os.path.join(out_dir_abs, "index.html")
        rebased_root_html = rebase_html_relative_urls(
            default_first_html,
            from_dir=default_first_lang_dir,
            to_dir=out_dir_abs,
            skip_prefixes=(),
        )
        os.makedirs(out_dir_abs, exist_ok=True)
        with open(root_index_abs, "w", encoding="utf-8") as rf:
            rf.write(rebased_root_html)
        root_progress.update(0, 0, done=True)

        readme_out = os.path.join(out_dir_abs, "README.md")
        with open(readme_out, "w", encoding="utf-8") as rmf:
            rmf.write(get_html_readme())

        if manifest.seo is not None:
            ensure_seo_og_image_copied(input_abs, out_dir_abs, manifest.seo)
            has_sitemap = False
            if manifest.seo.sitemap and manifest.seo.site_url:
                sitemap_entries: list[SitemapEntry] = []
                for lc in ordered_langs:
                    for rel_h in rel_htmls_by_lang.get(lc, []):
                        sitemap_entries.append(
                            SitemapEntry(
                                loc=resolve_public_page_url(manifest.seo.site_url, f"{lc}/{rel_h}"),
                                alternates=(),
                            )
                        )
                if sitemap_entries:
                    write_sitemap_xml(out_dir_abs, sitemap_entries)
                    has_sitemap = True
            if manifest.seo.robots:
                write_robots_txt(out_dir_abs, manifest.seo.site_url, include_sitemap=has_sitemap)
            if manifest.seo.llms_txt and llms_sections:
                write_llms_txt(
                    out_dir_abs,
                    title=site_title,
                    summary=resolve_localized_description(manifest, default_lang),
                    sections=llms_sections,
                )
    finally:
        if tmp_holder is not None:
            tmp_holder.cleanup()
