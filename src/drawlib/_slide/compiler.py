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
import shlex
import shutil
from pathlib import Path
from typing import Any, Optional

from drawlib._builder._common import resolve_styles_and_utils
from drawlib._builder.doc_builder.parser_md import parse_markdown_to_html
from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._builder.doc_builder.processor.options import DrawlibBlockOptions, parse_block_info
from drawlib._slide.base import BoundingBox, reset_slide_context, set_slide_context
from drawlib._templates import get_css, get_slide_js

_PATTERN_DRAWLIB = re.compile(
    r"(?<=\n)[ \t]*```drawlib([^\n]*)\n(.*?)\n[ \t]*```",
    re.DOTALL,
)
_PATTERN_CONTAINER_BOX = re.compile(
    r"(?:\n|^)[ \t]*:::+[ \t]*(?:block|box)(?:\s+([^\n]*))?\n(.*?)\n[ \t]*:::+",
    re.DOTALL,
)


def _parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML-style frontmatter delimited by leading '---'.

    Args:
        content: Raw markdown text.

    Returns:
        tuple[dict[str, Any], str]: (parsed frontmatter dict, remaining markdown body).
    """
    frontmatter: dict[str, Any] = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            for line in fm_text.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or ":" not in line:
                    continue
                key, val = line.split(":", 1)
                k = key.strip().lower()
                v = val.strip().strip('"').strip("'")
                if v.lower() in {"true", "yes"}:
                    frontmatter[k] = True
                elif v.lower() in {"false", "no"}:
                    frontmatter[k] = False
                else:
                    frontmatter[k] = v

    return frontmatter, body


def _extract_slide_title(markdown_text: str, default: str) -> str:
    """Extract first heading title from markdown body or return default.

    Args:
        markdown_text: Raw or processed markdown text.
        default: Fallback title.

    Returns:
        str: Discovered heading title or default.
    """
    for line in markdown_text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return re.sub(r"^#+\s*", "", line).strip()
    return default


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


def _format_asset_markup(
    file_name: str,
    alt_text: str,
    output_abs: str = "",
) -> str:
    """Format HTML markup for a rendered slide asset to fill its parent block container.

    Args:
        file_name: Image filename or relative path on disk.
        alt_text: Alt text attribute.
        output_abs: Absolute path to output directory for inlining SVGs.

    Returns:
        str: Generated HTML snippet.
    """
    if file_name.lower().endswith(".svg") and output_abs:
        svg_disk = os.path.normpath(os.path.join(output_abs, file_name))
        if os.path.exists(svg_disk):
            with open(svg_disk, encoding="utf-8") as f:
                svg_content = f.read()
            svg_clean = re.sub(r"<\?xml[^>]*\?>", "", svg_content)
            svg_clean = re.sub(r"<!DOCTYPE[^>]*>", "", svg_clean).strip()
            svg_clean = re.sub(
                r"<svg\s+",
                '<svg class="slide-vector-graphic" style="width: 100%; height: 100%; object-fit: contain;" ',
                svg_clean,
                count=1,
            )
            return (
                f'\n<figure class="drawlib-image">\n'
                f"  {svg_clean}\n"
                f"</figure>\n"
            )
    return (
        f'\n<figure class="drawlib-image">\n'
        f'  <img src="{file_name}" alt="{alt_text}" class="slide-raster-graphic" '
        f'style="width: 100%; height: 100%; object-fit: contain;" />\n'
        f"</figure>\n"
    )


def _parse_box_coordinates(
    header_opts: str,
) -> tuple[Optional[float], Optional[float], Optional[float], Optional[float], str]:
    """Extract (x, y) and (w, h) bounding box coordinates from container options.

    Args:
        header_opts: Raw header options string from ::: box.

    Returns:
        tuple[Optional[float], Optional[float], Optional[float], Optional[float], str]:
            (x, y, w, h, remaining_options_string).
    """
    x: Optional[float] = None
    y: Optional[float] = None
    w: Optional[float] = None
    h: Optional[float] = None

    tuple_pattern = r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)"
    tuple_matches = list(re.finditer(tuple_pattern, header_opts))
    if len(tuple_matches) >= 1:
        x = float(tuple_matches[0].group(1))
        y = float(tuple_matches[0].group(2))
    if len(tuple_matches) >= 2:
        w = float(tuple_matches[1].group(1))
        h = float(tuple_matches[1].group(2))

    cleaned_opts = re.sub(tuple_pattern, " ", header_opts).strip()
    return x, y, w, h, cleaned_opts


def _build_box_styles(
    x: Optional[float],
    y: Optional[float],
    w: Optional[float],
    h: Optional[float],
    font_size: Optional[str],
    align: Optional[str],
    z_index: Optional[int],
    custom_styles: list[str],
) -> list[str]:
    """Construct inline CSS style declarations for a positioned text box.

    Args:
        x: Left coordinate in pixels.
        y: Top coordinate in pixels.
        w: Width in pixels.
        h: Height in pixels.
        font_size: Optional font size override.
        align: Optional text alignment.
        z_index: Optional z-index layer.
        custom_styles: Additional inline CSS rules.

    Returns:
        list[str]: CSS style statements.
    """
    styles: list[str] = []
    actual_x = x if x is not None else 80.0
    actual_y = y if y is not None else 140.0
    actual_w = w if w is not None else 1760.0
    actual_h = h if h is not None else 840.0
    styles.append("position: absolute;")
    styles.append(f"left: {actual_x}px; top: {actual_y}px;")
    styles.append(f"width: {actual_w}px; height: {actual_h}px;")
    if font_size:
        fs = font_size if any(font_size.endswith(u) for u in ("px", "rem", "em", "%", "pt")) else f"{font_size}px"
        styles.append(f"font-size: {fs};")
    if align:
        styles.append(f"text-align: {align};")
    if z_index is not None:
        styles.append(f"z-index: {z_index};")
    for cs in custom_styles:
        clean = cs.strip().rstrip(";")
        if clean:
            styles.append(f"{clean};")
    return styles


def _handle_keyed_box_token(
    k: str,
    v: str,
    extra_class: list[str],
    custom_styles: list[str],
) -> tuple[Optional[str], Optional[int], Optional[str]]:
    """Handle a key:value token for box options."""
    k_lower = k.lower()
    if k_lower in {"font", "font-size", "fontsize", "fs"}:
        return v, None, None
    elif k_lower in {"z", "z_index", "z-index"}:
        try:
            return None, int(v), None
        except ValueError:
            return None, None, None
    elif k_lower in {"align", "text-align"}:
        return None, None, v.lower()
    elif k_lower in {"class", "css_class"}:
        extra_class.extend(v.split())
    elif k_lower in {"style", "css"}:
        custom_styles.append(v)
    return None, None, None


def _handle_pos_box_token(arg: str) -> tuple[Optional[str], bool, Optional[str]]:
    """Handle standalone keyword argument without key prefix."""
    kw_lower = arg.lower()
    if kw_lower == "compact":
        return None, True, None
    elif kw_lower in {"center", "left", "right"}:
        return None, False, kw_lower
    elif re.match(r"^\d+(px|rem|em|%)$", kw_lower):
        return arg, False, None
    return None, False, None


def _parse_box_tokens(
    cleaned_opts: str,
) -> tuple[Optional[str], bool, Optional[str], Optional[int], list[str], list[str]]:
    """Parse key:value tokens for a ::: box container.

    Args:
        cleaned_opts: Options string stripped of coordinate tuples.

    Returns:
        tuple: (font_size, compact, align, z_index, extra_classes, custom_styles).
    """
    font_size: Optional[str] = None
    compact: bool = False
    align: Optional[str] = None
    z_index: Optional[int] = None
    extra_class: list[str] = []
    custom_styles: list[str] = []

    try:
        tokens = shlex.split(cleaned_opts, posix=True)
    except ValueError:
        tokens = cleaned_opts.split()

    for token in tokens:
        if ":" in token or "=" in token:
            sep = ":" if ":" in token else "="
            k, v = token.split(sep, 1)
            v_clean = v.strip().strip('"').strip("'")
            fs, z, al = _handle_keyed_box_token(k.strip(), v_clean, extra_class, custom_styles)
            if fs:
                font_size = fs
            if z is not None:
                z_index = z
            if al:
                align = al
        else:
            v_clean = token.strip().strip('"').strip("'")
            fs, cp, al = _handle_pos_box_token(v_clean)
            if fs:
                font_size = fs
            if cp:
                compact = True
            if al:
                align = al

    return font_size, compact, align, z_index, extra_class, custom_styles


def _process_container_blocks(text: str) -> str:
    """Parse and convert ::: box ... ::: container syntax to positioned text box <div> elements.

    Args:
        text: Markdown text with potential ::: box blocks.

    Returns:
        str: Transformed text with HTML container markup.
    """

    def replacer(match: re.Match[str]) -> str:
        header_opts = (match.group(1) or "").strip()
        content = match.group(2).strip()

        x, y, w, h, cleaned_opts = _parse_box_coordinates(header_opts)
        font_size, compact, align, z_index, extra_class, custom_styles = _parse_box_tokens(cleaned_opts)
        styles = _build_box_styles(x, y, w, h, font_size, align, z_index, custom_styles)

        classes = ["slide-block", "slide-text-box"]
        if compact:
            classes.append("compact")
        classes.extend(extra_class)

        rendered_inner = parse_markdown_to_html(content)
        style_attr = f' style="{" ".join(styles)}"' if styles else ""
        class_attr = f' class="{" ".join(classes)}"'

        return f"\n<div{class_attr}{style_attr}>\n{rendered_inner}\n</div>\n"

    return _PATTERN_CONTAINER_BOX.sub(replacer, text)


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

        eff_fmt = options.format or default_format or "svg"
        if options.file:
            dl_file = options.file
            if not dl_file.endswith((".svg", ".png", ".webp")):
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
        return _format_asset_markup(rel_asset_path, "Illustration", output_abs=output_abs)

    return _PATTERN_DRAWLIB.sub(replacer, text)


def _assemble_slide_section(
    rendered_body: str,
    idx: int,
) -> str:
    """Assemble final slide <section> markup on the 1920x1080 stage.

    Args:
        rendered_body: HTML body snippet containing positioned slide-block elements.
        idx: Slide index.

    Returns:
        str: Slide <section> HTML markup.
    """
    active_cls = " active" if idx == 1 else ""
    return (
        f'    <section class="slide{active_cls}" data-slide-index="{idx}">\n'
        f'      <div class="slide-body">\n{rendered_body.strip()}\n      </div>\n'
        f"    </section>"
    )


def _copy_static_assets(input_abs: str, output_abs: str) -> None:
    """Copy static image and font assets from input directory to output directory.

    Args:
        input_abs: Source directory.
        output_abs: Target directory.
    """
    for asset_file in os.listdir(input_abs):
        asset_lower = asset_file.lower()
        if (
            asset_lower.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ttf", ".woff", ".woff2"))
            and not asset_lower.startswith(".")
        ):
            src_p = os.path.join(input_abs, asset_file)
            dst_p = os.path.join(output_abs, asset_file)
            if not os.path.exists(dst_p):
                shutil.copy2(src_p, dst_p)


def _deploy_slide_assets(input_abs: str, output_abs: str, deck_theme: str) -> None:
    """Deploy slide.css, slide.js, and static assets to the output directory.

    Args:
        input_abs: Input directory containing potential slide.css overrides and assets.
        output_abs: Output directory.
        deck_theme: Chosen CSS theme name.
    """
    local_css_path = os.path.join(input_abs, "slide.css")
    if os.path.isfile(local_css_path):
        with open(local_css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
    else:
        css_content = get_css(name=deck_theme, target="slide")

    with open(os.path.join(output_abs, "slide.css"), "w", encoding="utf-8") as f:
        f.write(css_content)

    with open(os.path.join(output_abs, "slide.js"), "w", encoding="utf-8") as f:
        f.write(get_slide_js())

    for asset_dir_name in ("_assets", "assets"):
        local_assets_dir = os.path.join(input_abs, asset_dir_name)
        out_assets_dir = os.path.join(output_abs, asset_dir_name)
        if os.path.isdir(local_assets_dir) and os.path.abspath(local_assets_dir) != os.path.abspath(out_assets_dir):
            if os.path.exists(out_assets_dir):
                shutil.rmtree(out_assets_dir)
            shutil.copytree(local_assets_dir, out_assets_dir)


def build_slide(
    input_dir: str,
    output_dir: Optional[str] = None,
    *,
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

    deck_title = "Drawlib Presentation"
    deck_theme = theme or "google"

    slides_html_list: list[str] = []
    thumbs_html_list: list[str] = []

    for idx, filename in enumerate(candidate_files, start=1):
        file_path = os.path.join(input_abs, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        frontmatter, body_text = _parse_frontmatter(raw_content)
        if "theme" in frontmatter and not theme:
            deck_theme = str(frontmatter["theme"])

        slide_title = str(frontmatter.get("title", "")) or _extract_slide_title(body_text, f"Slide {idx}")
        if idx == 1 and deck_title == "Drawlib Presentation":
            deck_title = slide_title

        ctx_token = set_slide_context(index=idx, total=total_slides)
        try:
            # If no ::: block or ::: box is in body_text, auto-wrap in default stage block
            text_to_search = "\n" + body_text if not body_text.startswith("\n") else body_text
            if not _PATTERN_CONTAINER_BOX.search(text_to_search):
                text_to_search = f"::: block (80, 140) (1760, 840)\n{text_to_search.strip()}\n:::"

            t_drawlib = _process_drawlib_blocks(
                text_to_search,
                output_abs,
                processor,
                file_path,
                idx,
                image_format,
            )
            t_containers = _process_container_blocks(t_drawlib)
            rendered_body = t_containers.strip()

            slide_section = _assemble_slide_section(
                rendered_body=rendered_body,
                idx=idx,
            )
            slides_html_list.append(slide_section)
        finally:
            reset_slide_context(ctx_token)

        curr_thumb = " current" if idx == 1 else ""
        thumbs_html_list.append(
            f'    <div class="overview-thumb{curr_thumb}" data-slide-target="{idx}">\n'
            f'      <div class="thumb-title">{idx}. {slide_title}</div>\n'
            f'      <div class="thumb-number">{idx} / {total_slides}</div>\n'
            f"    </div>"
        )

    _copy_static_assets(input_abs, output_abs)
    _deploy_slide_assets(input_abs, output_abs, deck_theme)

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
        '  <link rel="stylesheet" href="slide.css">\n'
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
