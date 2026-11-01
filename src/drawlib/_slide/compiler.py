# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Slide presentation compiler for Drawlib HTML presentation decks."""

from __future__ import annotations

import html
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Literal

from drawlib._builder._common import (
    BuildImageCache,
    find_project_manifest,
    load_project_manifest,
    load_styles_and_utils,
    resolve_styles_and_utils,
)
from drawlib._builder.doc_builder.detector import preserve_outer_fences, restore_outer_fences
from drawlib._builder.doc_builder.i18n import (
    build_language_switcher_context,
    rebase_html_relative_urls,
    validate_i18n_project,
)
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.doc_builder.processor.options import parse_block_info
from drawlib._slide._assets import deploy_slide_assets, format_asset_markup
from drawlib._slide._blocks import (
    PATTERN_CONTAINER_BOX,
    extract_slide_notes,
    process_container_blocks,
)
from drawlib._slide.base import reset_slide_context, set_slide_context
from drawlib._templates.langs import get_language_config

if TYPE_CHECKING:
    from drawlib._builder._common.manifest import I18nConfig, ProjectManifest
    from drawlib._builder.doc_builder.processor.options import DrawlibBlockOptions

_PATTERN_DRAWLIB: Final[re.Pattern[str]] = re.compile(
    r"(?<=\n)[ \t]*```drawlib([^\n]*)\n(.*?)\n[ \t]*```",
    re.DOTALL,
)
_PATTERN_H1: Final[re.Pattern[str]] = re.compile(r"^[ \t]*#(?!#)[ \t]+(.+?)[ \t#]*$")
_PATTERN_FENCE_LINE: Final[re.Pattern[str]] = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
_KNOWN_DIAGRAM_EXTS: Final[tuple[str, ...]] = (".svg", ".png", ".apng", ".webp", ".jpg", ".jpeg")


@dataclass(frozen=True)
class _SlideRenderOptions:
    """Internal rendering options shared across slides in a build invocation."""

    output_abs: str
    default_format: str
    dpi: int | None
    force_image_format: bool
    static_anim_frame: Literal["first", "last"] | None


def _resolve_drawlib_filename(
    options: DrawlibBlockOptions,
    idx: int,
    counter: int,
    default_format: str,
    *,
    has_anim: bool,
    force_image_format: bool,
) -> str:
    """Resolve output filename for a single drawlib block."""
    if force_image_format:
        eff_fmt = default_format or "png"
    else:
        eff_fmt = options.format or default_format or "svg"
        if has_anim and eff_fmt == "svg":
            eff_fmt = "png"

    if not options.file:
        return f"drawlib_{idx}_{counter}.{eff_fmt}"

    dl_file = options.file
    if force_image_format:
        stem, ext = os.path.splitext(dl_file)
        if ext.lower() in _KNOWN_DIAGRAM_EXTS:
            return f"{stem}.{eff_fmt}"
        return f"{dl_file}.{eff_fmt}"

    if not dl_file.lower().endswith(_KNOWN_DIAGRAM_EXTS):
        return f"{dl_file}.{eff_fmt}"
    return dl_file


def _flatten_slide_animation_in_place(
    target_path: str,
    anim_frame: Literal["first", "last"],
) -> None:
    """Convert multi-frame animated images in-place into a single static PNG frame."""
    from drawlib._builder._common.office import ensure_static_office_image  # noqa: PLC0415

    parent_dir = os.path.dirname(target_path) or "."
    static_path, _, _ = ensure_static_office_image(
        target_path,
        parent_dir,
        anim_frame=anim_frame,
    )
    if os.path.abspath(static_path) != os.path.abspath(target_path):
        os.replace(static_path, target_path)


def require_slide_manifest(input_abs: str) -> ProjectManifest:
    """Load and validate a required ``type = "slide"`` ``drawlib.toml`` manifest."""
    manifest = load_project_manifest(input_abs)
    if manifest is None:
        found = find_project_manifest(input_abs)
        if found is not None and os.path.abspath(found[0]) != input_abs:
            proj_root, _ = found
            raise ValueError(
                f'No "drawlib.toml" manifest found in "{input_abs}". '
                f'Found project manifest in parent directory "{proj_root}" — '
                f'pass the project root directory "{proj_root}" instead of a locale subdirectory.'
            )
        raise ValueError(
            f'Missing required "drawlib.toml" project manifest in "{input_abs}". '
            'Initialize a slide project with "drawlib init slide" or add a drawlib.toml manifest.'
        )

    if manifest.project.type != "slide":
        raise ValueError(
            f'Input directory "{input_abs}" is a "{manifest.project.type}" project (drawlib.toml), '
            'not a "slide" presentation project.'
        )
    if manifest.i18n is None:
        raise ValueError(f'Slide project "{input_abs}" requires an [i18n] section in drawlib.toml.')
    return manifest


def _resolve_output_dir(input_abs: str, output_dir: str | None) -> str:
    """Resolve target output directory path.

    Defaults to ``<parent>/<base>_html`` where ``<base>`` strips trailing ``_src``
    from ``input_abs`` basename (or ``<input_abs>_html`` if not ending in ``_src``).

    Args:
        input_abs: Absolute path to presentation source directory.
        output_dir: Optional explicit output directory.

    Returns:
        str: Resolved absolute output directory path.

    Raises:
        ValueError: If resolved output directory equals ``input_abs``.
    """
    if output_dir:
        output_abs = os.path.abspath(output_dir)
    else:
        cleaned = input_abs.rstrip(os.sep)
        base_name = os.path.basename(cleaned)
        parent_dir = os.path.dirname(cleaned)
        if base_name.endswith("_src") and len(base_name) > 4:
            output_abs = os.path.join(parent_dir, f"{base_name[:-4]}_html")
        else:
            output_abs = f"{cleaned}_html"

    if os.path.abspath(output_abs) == os.path.abspath(input_abs):
        raise ValueError(f"Output directory cannot be the same as input directory: '{input_abs}'")
    os.makedirs(output_abs, exist_ok=True)
    return output_abs


def _clean_output_dir(output_abs: str, input_abs: str) -> None:
    """Remove previous generated assets from output directory before building.

    Args:
        output_abs: Absolute path to target output directory.
        input_abs: Absolute path to source directory.
    """
    if not os.path.exists(output_abs) or os.path.abspath(output_abs) == os.path.abspath(input_abs):
        return
    if os.path.exists(os.path.join(output_abs, ".git")):
        return

    for item in os.listdir(output_abs):
        if item.startswith("."):
            continue
        item_path = os.path.join(output_abs, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)


def _extract_first_h1(markdown_text: str) -> str | None:
    """Extract the first Markdown ``# H1`` heading outside fenced code blocks."""
    masked, _ = preserve_outer_fences(markdown_text)
    in_fence = False
    fence_marker = ""
    for line in masked.splitlines():
        if not in_fence:
            m_open = _PATTERN_FENCE_LINE.match(line)
            if m_open:
                in_fence = True
                fence_marker = m_open.group(1)
                continue
            m_h1 = _PATTERN_H1.match(line)
            if m_h1:
                heading = m_h1.group(1).strip()
                if heading:
                    return heading
        else:
            close_pat = rf"^[ \t]{{0,3}}{re.escape(fence_marker[0])}{{{len(fence_marker)},}}[ \t\r]*$"
            if re.match(close_pat, line):
                in_fence = False
                fence_marker = ""
    return None


def _rebase_slide_html_urls(
    html_fragment: str,
    rel_slide_path: str,
    output_abs: str,
    lang: str,
) -> str:
    """Rebase relative HTML ``href``/``src`` attributes in a slide body to ``<output_abs>/<lang>/``."""
    if not html_fragment:
        return html_fragment

    slide_rel_dir = os.path.dirname(rel_slide_path)
    virtual_from_dir = os.path.normpath(os.path.join(output_abs, lang, *slide_rel_dir.split("/")))
    lang_out_dir = os.path.join(output_abs, lang)

    rebased = rebase_html_relative_urls(
        html=html_fragment,
        from_dir=virtual_from_dir,
        to_dir=lang_out_dir,
        skip_prefixes=("../images/", "images/", "_assets/", "assets/"),
    )

    protected_blocks: list[str] = []

    def _protect(m: re.Match[str]) -> str:
        idx_mask = len(protected_blocks)
        protected_blocks.append(m.group(0))
        return f"__DRAWLIB_SLIDE_CODE_MASK_{idx_mask}__"

    masked = re.sub(r"(?is)<pre\b[^>]*>.*?</pre>|<code\b[^>]*>.*?</code>", _protect, rebased)
    rewritten = re.sub(
        r'(\b(?:href|src)=["\'])(_assets/|assets/)',
        r"\1../\2",
        masked,
        flags=re.IGNORECASE,
    )
    for idx_mask, original in enumerate(protected_blocks):
        rewritten = rewritten.replace(f"__DRAWLIB_SLIDE_CODE_MASK_{idx_mask}__", original)
    return rewritten


def _process_drawlib_blocks(
    text: str,
    processor: DrawlibBlockProcessor,
    file_path: str,
    md_stem: str,
    idx: int,
    render_opts: _SlideRenderOptions,
    rendered_targets: set[str],
) -> str:
    """Execute and replace ````drawlib```` blocks, deduplicating shared targets across locales."""
    counter = 0
    masked_text, preserved = preserve_outer_fences(text)

    def replacer(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        info_str = match.group(1).strip()
        code = match.group(2).strip()
        options = parse_block_info(info_str)

        has_anim = (
            options.anim_trigger is not None
            or options.anim_loop is not None
            or bool(options.anim_pause)
            or "Animation(" in code
        )
        dl_file = _resolve_drawlib_filename(
            options,
            idx,
            counter,
            render_opts.default_format,
            has_anim=has_anim,
            force_image_format=render_opts.force_image_format,
        )

        if "/" in dl_file or "\\" in dl_file:
            rel_asset_path = dl_file.replace("\\", "/")
        else:
            rel_asset_path = f"images/{md_stem}/{dl_file}"

        target_path = os.path.normpath(os.path.join(render_opts.output_abs, rel_asset_path))
        target_abs = os.path.abspath(target_path)

        if target_abs not in rendered_targets or not os.path.isfile(target_abs):
            os.makedirs(os.path.dirname(target_abs), exist_ok=True)
            processor.render_block_to_file(
                code,
                target_abs,
                source_filename=file_path,
                no_cache=options.no_cache,
                dpi=render_opts.dpi,
            )
            if render_opts.static_anim_frame is not None:
                _flatten_slide_animation_in_place(target_abs, render_opts.static_anim_frame)
            if os.path.isfile(target_abs):
                rendered_targets.add(target_abs)

        markup_opts = None if render_opts.static_anim_frame is not None else options
        return format_asset_markup(
            rel_asset_path,
            "Illustration",
            output_abs=render_opts.output_abs,
            options=markup_opts,
            asset_url_prefix="../",
        )

    replaced = _PATTERN_DRAWLIB.sub(replacer, masked_text)
    return restore_outer_fences(replaced, preserved)


def _assemble_slide_section(
    rendered_body: str,
    idx: int,
    notes_html: str = "",
) -> str:
    """Assemble final slide <section> markup on the 1920x1080 stage."""
    active_cls = " active" if idx == 1 else ""
    notes_block = (
        f'      <aside class="slide-notes" hidden>\n{notes_html}\n      </aside>\n'
        if notes_html
        else '      <aside class="slide-notes" hidden></aside>\n'
    )
    return (
        f'    <section class="slide{active_cls}" data-slide-index="{idx}">\n'
        f'      <div class="slide-body">\n{rendered_body.strip()}\n      </div>\n'
        f"{notes_block}"
        f"    </section>"
    )


def _clear_project_utils_module(input_abs: str) -> None:
    """Evict cached top-level ``utils`` module if it was imported from ``input_abs``."""
    mod = sys.modules.get("utils")
    if mod is None:
        return
    mod_file = getattr(mod, "__file__", None)
    if mod_file and os.path.abspath(mod_file).startswith(input_abs + os.sep):
        sys.modules.pop("utils", None)


def _compile_locale_slides(
    *,
    input_abs: str,
    lang: str,
    rel_files: list[str],
    styles_path: str | None,
    utils_path: str | None,
    no_cache: bool,
    cache: BuildImageCache,
    render_opts: _SlideRenderOptions,
    rendered_targets: set[str],
) -> tuple[str, str, str | None]:
    """Compile all Markdown slides for a single locale and return ``(slides_markup, thumbs_markup, first_h1)``."""
    total_slides = len(rel_files)
    lang_src_dir = os.path.join(input_abs, lang)
    loc_styles, loc_utils = resolve_styles_and_utils(lang_src_dir, styles_path, utils_path)
    _clear_project_utils_module(input_abs)
    load_styles_and_utils(styles_path=loc_styles, utils_path=loc_utils)
    processor = DrawlibBlockProcessor(
        styles_path=loc_styles,
        utils_path=loc_utils,
        no_cache=no_cache,
        cache=cache,
        project_root=input_abs,
        require_file=False,
        extra_config_hash=f"total_slides:{total_slides}",
    )

    slides_html_list: list[str] = []
    thumbs_html_list: list[str] = []
    first_h1_title: str | None = None

    for idx, rel_path in enumerate(rel_files, start=1):
        file_path = os.path.join(lang_src_dir, *rel_path.split("/"))
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        md_stem = os.path.splitext(rel_path)[0] or Path(file_path).stem
        ctx_token = set_slide_context(index=idx, total=total_slides)
        try:
            content_without_notes, notes_html = extract_slide_notes(raw_content)
            if first_h1_title is None:
                first_h1_title = _extract_first_h1(content_without_notes)

            text_to_search = (
                "\n" + content_without_notes if not content_without_notes.startswith("\n") else content_without_notes
            )
            if not PATTERN_CONTAINER_BOX.search(text_to_search):
                text_to_search = f"::: block xy=(80, 140) width=1760 height=840\n{text_to_search.strip()}\n:::"

            t_drawlib = _process_drawlib_blocks(
                text=text_to_search,
                processor=processor,
                file_path=file_path,
                md_stem=md_stem,
                idx=idx,
                render_opts=render_opts,
                rendered_targets=rendered_targets,
            )
            t_containers = process_container_blocks(t_drawlib)
            rendered_body = _rebase_slide_html_urls(
                t_containers.strip(),
                rel_slide_path=rel_path,
                output_abs=render_opts.output_abs,
                lang=lang,
            )
            rebased_notes = _rebase_slide_html_urls(
                notes_html,
                rel_slide_path=rel_path,
                output_abs=render_opts.output_abs,
                lang=lang,
            )
            slides_html_list.append(
                _assemble_slide_section(
                    rendered_body=rendered_body,
                    idx=idx,
                    notes_html=rebased_notes,
                )
            )
        finally:
            reset_slide_context(ctx_token)

        curr_thumb = " current" if idx == 1 else ""
        thumbs_html_list.append(
            f'    <div class="overview-thumb{curr_thumb}" data-slide-target="{idx}">\n'
            f'      <div class="thumb-title">Slide {idx}</div>\n'
            f'      <div class="thumb-number">{idx} / {total_slides}</div>\n'
            f"    </div>"
        )

    return "\n\n".join(slides_html_list), "\n".join(thumbs_html_list), first_h1_title


def _resolve_favicon_markup(input_abs: str, output_abs: str, lang_out_dir: str) -> str:
    """Resolve optional ``<link rel="icon" ...>`` markup relative to ``lang_out_dir``."""
    mime_by_ext = {
        ".png": "image/png",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
    }
    for sub in ("_assets", "assets", ""):
        for fav_name in ("favicon.png", "favicon.ico", "favicon.svg"):
            dst_fav = os.path.join(output_abs, sub, fav_name) if sub else os.path.join(output_abs, fav_name)
            src_fav = os.path.join(input_abs, sub, fav_name) if sub else os.path.join(input_abs, fav_name)
            if os.path.isfile(dst_fav) or os.path.isfile(src_fav):
                target_fav = dst_fav if os.path.isfile(dst_fav) else os.path.join(output_abs, "_assets", fav_name)
                rel_fav = os.path.relpath(target_fav, lang_out_dir).replace(os.sep, "/")
                ext = os.path.splitext(fav_name)[1].lower()
                mime = mime_by_ext.get(ext, "image/png")
                return f'  <link rel="icon" type="{mime}" href="{html.escape(rel_fav, quote=True)}">\n'
    return ""


def _build_lang_switcher_html(languages_ctx: list[dict[str, Any]]) -> str:
    """Build ``<details class="slide-lang-dropdown">`` markup when multiple locales exist."""
    if len(languages_ctx) <= 1:
        return ""

    active_label = ""
    for item in languages_ctx:
        if item.get("active"):
            active_label = str(item.get("label", ""))
            break
    if not active_label:
        active_label = str(languages_ctx[0].get("label", ""))

    esc_active_label = html.escape(active_label)
    option_lines: list[str] = []
    for item in languages_ctx:
        is_active = bool(item.get("active"))
        cls = "slide-lang-option active" if is_active else "slide-lang-option"
        esc_url = html.escape(str(item.get("url", "")), quote=True)
        esc_code = html.escape(str(item.get("code", "")), quote=True)
        esc_html_lang = html.escape(str(item.get("html_lang", "")), quote=True)
        esc_label = html.escape(str(item.get("label", "")))
        aria_curr = ' aria-current="page"' if is_active else ""
        check_svg = (
            '\n        <svg class="slide-lang-check" viewBox="0 0 24 24" aria-hidden="true">'
            '<polyline points="20 6 9 17 4 12"></polyline></svg>'
            if is_active
            else ""
        )
        option_lines.append(
            f'      <a href="{esc_url}" class="{cls}" data-lang-switch="{esc_code}" '
            f'lang="{esc_html_lang}" hreflang="{esc_html_lang}" role="menuitem"{aria_curr}>\n'
            f"        <span>{esc_label}</span>{check_svg}\n"
            f"      </a>"
        )

    options_markup = "\n".join(option_lines)
    return (
        '  <details class="slide-lang-dropdown">\n'
        '    <summary class="slide-lang-btn" title="Switch Language (L)" aria-label="Select language">\n'
        '      <svg class="slide-lang-globe" viewBox="0 0 24 24" aria-hidden="true">'
        '<circle cx="12" cy="12" r="10"></circle>'
        '<line x1="2" y1="12" x2="22" y2="12"></line>'
        '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 '
        '15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>\n'
        f'      <span class="slide-lang-label">{esc_active_label}</span>\n'
        "    </summary>\n"
        '    <div class="slide-lang-menu" role="menu">\n'
        f"{options_markup}\n"
        "    </div>\n"
        "  </details>\n"
    )


def _render_locale_index_html(
    *,
    input_abs: str,
    output_abs: str,
    i18n_cfg: I18nConfig,
    lang: str,
    deck_title: str,
    slides_markup: str,
    thumbs_markup: str,
) -> str:
    """Write ``<output_abs>/<lang>/index.html`` and return its absolute path."""
    lang_out_dir = os.path.join(output_abs, lang)
    os.makedirs(lang_out_dir, exist_ok=True)
    lang_index_abs = os.path.join(lang_out_dir, "index.html")

    lang_cfg = get_language_config(lang)
    languages_ctx, alt_links = build_language_switcher_context(
        config=i18n_cfg,
        out_dir_abs=output_abs,
        rel_html_path="index.html",
        current_dest_abs=lang_index_abs,
        active_lang=lang,
    )

    alt_links_markup = "".join(
        f'  <link rel="alternate" hreflang="{html.escape(link["hreflang"], quote=True)}" '
        f'href="{html.escape(link["url"], quote=True)}">\n'
        for link in alt_links
    )
    favicon_markup = _resolve_favicon_markup(input_abs, output_abs, lang_out_dir)
    extra_font_markup = f"  {lang_cfg.font_link_html.strip()}\n" if lang_cfg.font_link_html.strip() else ""
    switcher_markup = _build_lang_switcher_html(languages_ctx)

    esc_html_lang = html.escape(lang_cfg.code, quote=True)
    esc_html_dir = html.escape(lang_cfg.direction, quote=True)
    esc_title = html.escape(deck_title)

    html_content = (
        "<!DOCTYPE html>\n"
        f'<html lang="{esc_html_lang}" dir="{esc_html_dir}">\n'
        "<head>\n"
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"  <title>{esc_title}</title>\n"
        f"{favicon_markup}"
        f"{alt_links_markup}"
        '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        "family=Google+Sans:wght@400;500;700&"
        "family=Inter:wght@400;500;600;700&"
        'family=JetBrains+Mono:wght@400;600&display=swap">\n'
        f"{extra_font_markup}"
        '  <link rel="stylesheet" href="style.css">\n'
        "</head>\n"
        "<body>\n\n"
        '<div class="presentation-viewport">\n'
        '  <div class="presentation-stage">\n'
        f"{slides_markup}\n"
        "  </div>\n"
        "</div>\n\n"
        "<!-- On-Screen Controls -->\n"
        '<div class="slide-controls">\n'
        '  <button id="btn-prev" title="Previous Slide (Left Arrow)">◀</button>\n'
        '  <button id="btn-next" title="Next Slide (Right Arrow)">▶</button>\n'
        '  <button id="btn-overview" title="Slide Overview (O / Esc)">☵</button>\n'
        '  <button id="btn-presenter" title="Presenter View (P / S)">🗒</button>\n'
        '  <button id="btn-fullscreen" title="Fullscreen (F)">⛶</button>\n'
        f"{switcher_markup}"
        "</div>\n\n"
        "<!-- Overview Modal Grid -->\n"
        '<div class="overview-modal">\n'
        '  <div class="overview-grid">\n'
        f"{thumbs_markup}\n"
        "  </div>\n"
        "</div>\n\n"
        '<script src="../slide.js"></script>\n'
        "</body>\n"
        "</html>\n"
    )

    with open(lang_index_abs, "w", encoding="utf-8") as f:
        f.write(html_content)
    return lang_index_abs


def build_slide(
    input_dir: str,
    output_dir: str | None = None,
    *,
    title: str | None = None,
    theme: str | None = None,
    image_format: str = "svg",
    dpi: int | None = None,
    force_image_format: bool = False,
    static_anim_frame: Literal["first", "last"] | None = None,
    styles_path: str | None = None,
    utils_path: str | None = None,
    no_cache: bool = False,
) -> str:
    """Compile an ``i18n``-native presentation project into a multi-locale HTML slide deck.

    Args:
        input_dir: Project root directory containing ``drawlib.toml`` and ``<lang>/`` slides.
        output_dir: Target directory for compiled slide deck (defaults to ``<base>_html``).
        title: Optional presentation HTML title override.
        theme: CSS theme preset name ('google', 'default', 'google-dark', etc.).
        image_format: Default image format for embedded diagrams ('svg', 'webp', or 'png').
        dpi: Optional rasterization DPI override when generating raster diagrams.
        force_image_format: If True, rewrite explicit block filenames (e.g. .svg) to image_format.
        static_anim_frame: If set ('first' or 'last'), flatten multi-frame animations into static PNGs.
        styles_path: Optional path to custom styles.py script.
        utils_path: Optional path to custom utils.py script.
        no_cache: If True, disable reading/writing build cache.

    Returns:
        str: Absolute path to ``<output_abs>/<default_lang>/index.html``.

    Raises:
        ValueError: If ``input_dir`` is invalid, lacks ``drawlib.toml``, or fails i18n parity checks.
    """
    input_abs = os.path.abspath(input_dir)
    if not os.path.isdir(input_abs):
        raise ValueError(f"Input directory does not exist: '{input_dir}'")

    manifest = require_slide_manifest(input_abs)
    assert manifest.i18n is not None  # noqa: S101
    i18n_cfg = manifest.i18n

    output_abs = _resolve_output_dir(input_abs, output_dir)
    locale_files = validate_i18n_project(
        input_abs,
        i18n_cfg,
        project_type="slide",
        default_format=image_format,
    )
    _clean_output_dir(output_abs, input_abs)
    os.makedirs(output_abs, exist_ok=True)

    deck_theme = theme or (manifest.project.style if manifest.project.style else None) or "google"
    manifest_title = manifest.project.title.strip() if manifest.project.title and manifest.project.title.strip() else ""
    default_lang = i18n_cfg.default_lang
    ordered_langs = [default_lang, *[lc for lc in i18n_cfg.langs if lc != default_lang]]

    render_opts = _SlideRenderOptions(
        output_abs=output_abs,
        default_format=image_format,
        dpi=dpi,
        force_image_format=force_image_format,
        static_anim_frame=static_anim_frame,
    )
    rendered_targets: set[str] = set()
    cache = BuildImageCache(enabled=not no_cache)
    compiled_locales: dict[str, tuple[str, str, str]] = {}

    orig_cwd = os.getcwd()
    try:
        os.chdir(input_abs)
        for lang in ordered_langs:
            slides_markup, thumbs_markup, first_h1 = _compile_locale_slides(
                input_abs=input_abs,
                lang=lang,
                rel_files=locale_files[lang],
                styles_path=styles_path,
                utils_path=utils_path,
                no_cache=no_cache,
                cache=cache,
                render_opts=render_opts,
                rendered_targets=rendered_targets,
            )
            locale_title = title or manifest_title or first_h1 or "Presentation"
            compiled_locales[lang] = (slides_markup, thumbs_markup, locale_title)
    finally:
        os.chdir(orig_cwd)

    deploy_slide_assets(
        input_abs=input_abs,
        output_abs=output_abs,
        deck_theme=deck_theme,
        langs=i18n_cfg.langs,
    )

    locale_index_paths: dict[str, str] = {}
    for lang in i18n_cfg.langs:
        slides_markup, thumbs_markup, locale_title = compiled_locales[lang]
        locale_index_paths[lang] = _render_locale_index_html(
            input_abs=input_abs,
            output_abs=output_abs,
            i18n_cfg=i18n_cfg,
            lang=lang,
            deck_title=locale_title,
            slides_markup=slides_markup,
            thumbs_markup=thumbs_markup,
        )

    from drawlib._builder.doc_builder.compiler.base import write_root_redirect_html  # noqa: PLC0415

    default_title = compiled_locales[default_lang][2]
    write_root_redirect_html(output_abs, default_lang, title=default_title)
    return locale_index_paths[default_lang]
