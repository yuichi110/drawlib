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

import os
import re
import shutil
from pathlib import Path
from typing import Final, Optional

from drawlib._builder._common import resolve_styles_and_utils
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.doc_builder.processor.options import parse_block_info
from drawlib._slide._assets import copy_static_assets, deploy_slide_assets, format_asset_markup
from drawlib._slide._blocks import (
    PATTERN_CONTAINER_BOX,
    extract_slide_notes,
    process_container_blocks,
)
from drawlib._slide.base import reset_slide_context, set_slide_context

_PATTERN_DRAWLIB: Final[re.Pattern[str]] = re.compile(
    r"(?<=\n)[ \t]*```drawlib([^\n]*)\n(.*?)\n[ \t]*```",
    re.DOTALL,
)


def _resolve_output_dir(input_abs: str, output_dir: Optional[str]) -> str:
    """Resolve target output directory path.

    Args:
        input_abs: Absolute path to presentation source directory.
        output_dir: Optional explicit output directory.

    Returns:
        str: Resolved absolute output directory path.
    """
    if output_dir:
        output_abs = os.path.abspath(output_dir)
    elif input_abs.endswith("_src"):
        output_abs = input_abs[:-4]
    else:
        output_abs = os.path.join(input_abs, "slide")
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


def _collect_slide_files(input_abs: str) -> list[str]:
    """Discover and alphabetically sort candidate markdown slide files.

    Args:
        input_abs: Absolute path to source directory.

    Returns:
        list[str]: Sorted list of filenames.
    """
    files = [
        f
        for f in os.listdir(input_abs)
        if (f.endswith(".md") or f.endswith(".markdown"))
        and not f.startswith(".")
        and f.lower() not in {"navbar.md", "readme.md"}
    ]
    files.sort()
    return files


def _process_drawlib_blocks(
    text: str,
    output_abs: str,
    processor: DrawlibBlockProcessor,
    file_path: str,
    idx: int,
    default_format: str,
) -> str:
    """Execute and replace ```drawlib blocks.

    Args:
        text: Markdown text with code blocks.
        output_abs: Target output directory.
        processor: Initialized block processor.
        file_path: Absolute path to slide source file.
        idx: Slide index.
        default_format: Default image format.

    Returns:
        str: Transformed markdown text.
    """
    counter = 0
    md_stem = Path(file_path).stem if file_path else f"slide_{idx}"

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
        eff_fmt = options.format or default_format or "svg"
        if has_anim and eff_fmt == "svg":
            eff_fmt = "png"
        if options.file:
            dl_file = options.file
            if not dl_file.endswith((".svg", ".png", ".apng", ".webp")):
                dl_file = f"{dl_file}.{eff_fmt}"
        else:
            dl_file = f"drawlib_{idx}_{counter}.{eff_fmt}"

        if "/" in dl_file or "\\" in dl_file:
            rel_asset_path = dl_file.replace("\\", "/")
        else:
            rel_asset_path = f"images/{md_stem}/{dl_file}"

        target_path = os.path.normpath(os.path.join(output_abs, rel_asset_path))
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        processor.render_block_to_file(
            code,
            target_path,
            source_filename=file_path,
            no_cache=options.no_cache,
        )
        return format_asset_markup(rel_asset_path, "Illustration", output_abs=output_abs, options=options)

    return _PATTERN_DRAWLIB.sub(replacer, text)


def _assemble_slide_section(
    rendered_body: str,
    idx: int,
    notes_html: str = "",
) -> str:
    """Assemble final slide <section> markup on the 1920x1080 stage.

    Args:
        rendered_body: HTML body snippet containing positioned slide-block elements.
        idx: Slide index.
        notes_html: Optional HTML snippet of speaker notes for Presenter View.

    Returns:
        str: Slide <section> HTML markup.
    """
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


def build_slide(
    input_dir: str,
    output_dir: Optional[str] = None,
    *,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    image_format: str = "svg",
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    no_cache: bool = False,
) -> str:
    """Compile a presentation source directory into a static HTML slide deck.

    Args:
        input_dir: Directory containing Markdown (.md) slide files and presentation assets.
        output_dir: Target directory for compiled slide deck (defaults to 'slide/' or 'slides_html/').
        title: Optional presentation HTML title (defaults to 'Drawlib Presentation').
        theme: CSS theme preset name ('google', 'default', 'google-dark', etc.).
        image_format: Default image format for embedded diagrams ('svg', 'webp', or 'png').
        styles_path: Optional path to custom styles.py script.
        utils_path: Optional path to custom utils.py script.
        no_cache: If True, disable reading/writing build cache.

    Returns:
        str: Absolute path to the generated index.html file.

    Raises:
        ValueError: If input_dir is invalid or no slide files are found.
    """
    input_abs = os.path.abspath(input_dir)
    if not os.path.isdir(input_abs):
        raise ValueError(f"Input directory does not exist: '{input_dir}'")

    output_abs = _resolve_output_dir(input_abs, output_dir)
    _clean_output_dir(output_abs, input_abs)
    candidate_files = _collect_slide_files(input_abs)
    if not candidate_files:
        raise ValueError(f"No Markdown slide files (.md) found in '{input_dir}'")

    total_slides = len(candidate_files)
    styles_abs, utils_abs = resolve_styles_and_utils(input_abs, styles_path, utils_path)
    processor = DrawlibBlockProcessor(
        styles_path=styles_abs,
        utils_path=utils_abs,
        no_cache=no_cache,
        project_root=input_abs,
        require_file=False,
        extra_config_hash=f"total_slides:{total_slides}",
    )

    deck_title = title or "Drawlib Presentation"
    deck_theme = theme or "google"

    slides_html_list: list[str] = []
    thumbs_html_list: list[str] = []

    for idx, filename in enumerate(candidate_files, start=1):
        file_path = os.path.join(input_abs, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        ctx_token = set_slide_context(index=idx, total=total_slides)
        try:
            content_without_notes, notes_html = extract_slide_notes(raw_content)
            # If no ::: block or ::: box is in content_without_notes, auto-wrap in default stage block
            text_to_search = (
                "\n" + content_without_notes
                if not content_without_notes.startswith("\n")
                else content_without_notes
            )
            if not PATTERN_CONTAINER_BOX.search(text_to_search):
                text_to_search = f"::: block (80, 140) (1760, 840)\n{text_to_search.strip()}\n:::"

            t_drawlib = _process_drawlib_blocks(
                text_to_search,
                output_abs,
                processor,
                file_path,
                idx,
                image_format,
            )
            t_containers = process_container_blocks(t_drawlib)
            rendered_body = t_containers.strip()

            slide_section = _assemble_slide_section(
                rendered_body=rendered_body,
                idx=idx,
                notes_html=notes_html,
            )
            slides_html_list.append(slide_section)
        finally:
            reset_slide_context(ctx_token)

        curr_thumb = " current" if idx == 1 else ""
        thumbs_html_list.append(
            f'    <div class="overview-thumb{curr_thumb}" data-slide-target="{idx}">\n'
            f'      <div class="thumb-title">Slide {idx}</div>\n'
            f'      <div class="thumb-number">{idx} / {total_slides}</div>\n'
            f"    </div>"
        )

    copy_static_assets(input_abs, output_abs)
    deploy_slide_assets(input_abs, output_abs, deck_theme)

    slides_markup = "\n\n".join(slides_html_list)
    thumbs_markup = "\n".join(thumbs_html_list)

    html_content = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"  <title>{deck_title}</title>\n"
        '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        "family=Google+Sans:wght@400;500;700&"
        "family=Inter:wght@400;500;600;700&"
        'family=JetBrains+Mono:wght@400;600&display=swap">\n'
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
        "</div>\n\n"
        "<!-- Overview Modal Grid -->\n"
        '<div class="overview-modal">\n'
        '  <div class="overview-grid">\n'
        f"{thumbs_markup}\n"
        "  </div>\n"
        "</div>\n\n"
        '<script src="slide.js"></script>\n'
        "</body>\n"
        "</html>\n"
    )

    index_html_path = os.path.join(output_abs, "index.html")
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return index_html_path
