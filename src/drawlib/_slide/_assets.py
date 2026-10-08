# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Asset deployment and markup formatting for slide presentations."""

from __future__ import annotations

import base64
import contextlib
import json
import os
import re
import shutil
from typing import TYPE_CHECKING, Optional

from drawlib._core.l1_core import FONT_DIR_PATH, FONT_ICON_DIR_PATH
from drawlib._core.l3_external import download_if_not_exist
from drawlib._templates import get_css, get_slide_js

if TYPE_CHECKING:
    from drawlib._builder.doc_builder.processor.options import DrawlibBlockOptions

_PATTERN_SVG_FONTS_COMMENT = re.compile(r"<!--\s*drawlib-svg-fonts:\s*(\[.*?\])\s*-->")


def _resolve_font_src_spec(src_spec: str) -> str:
    """Resolve portable font source spec to an absolute local file path, downloading if needed."""
    if src_spec.startswith("builtin:fonts/"):
        rel_sub = src_spec.removeprefix("builtin:fonts/")
        abs_src = os.path.join(FONT_DIR_PATH, *rel_sub.split("/"))
        if not os.path.isfile(abs_src):
            with contextlib.suppress(Exception):
                download_if_not_exist(file_path=abs_src)
        return abs_src
    if src_spec.startswith("builtin:fonticons/"):
        rel_sub = src_spec.removeprefix("builtin:fonticons/")
        abs_src = os.path.join(FONT_ICON_DIR_PATH, *rel_sub.split("/"))
        if not os.path.isfile(abs_src):
            with contextlib.suppress(Exception):
                download_if_not_exist(file_path=abs_src)
        return abs_src
    return src_spec


def _extract_svg_font_records_from_file(svg_path: str) -> list[dict[str, str]]:
    """Extract drawlib-svg-fonts metadata records from a single SVG file."""
    records: list[dict[str, str]] = []
    with contextlib.suppress(OSError):
        with open(svg_path, "r", encoding="utf-8") as f:
            content = f.read()
        for match in _PATTERN_SVG_FONTS_COMMENT.finditer(content):
            with contextlib.suppress(json.JSONDecodeError, TypeError):
                items = json.loads(match.group(1))
                if not isinstance(items, list):
                    continue
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    fam = str(item.get("family", "")).strip()
                    rel_p = str(item.get("rel_path", "")).strip()
                    src_p = str(item.get("src", "")).strip()
                    fmt = str(item.get("format", "truetype")).strip()
                    if fam and rel_p and src_p:
                        records.append({"family": fam, "rel_path": rel_p, "src": src_p, "format": fmt})
    return records


def _collect_svg_font_records(output_abs: str) -> list[dict[str, str]]:
    """Walk output_abs and collect deduplicated SVG font records."""
    seen_families: set[str] = set()
    bundled_records: list[dict[str, str]] = []
    for root, dirnames, files in os.walk(output_abs):
        dirnames[:] = [d for d in sorted(dirnames) if not d.startswith(".")]
        for fname in sorted(files):
            if not fname.lower().endswith(".svg") or fname.startswith("."):
                continue
            for rec in _extract_svg_font_records_from_file(os.path.join(root, fname)):
                if rec["family"] not in seen_families:
                    seen_families.add(rec["family"])
                    bundled_records.append(rec)
    return bundled_records


def _write_svg_font_faces_css(
    output_abs: str,
    css_file_path: str,
    active_records: list[dict[str, str]],
) -> None:
    """Write idempotent @font-face declarations to css_file_path."""
    css_dir = os.path.dirname(os.path.abspath(css_file_path))
    marker = "/* Auto-bundled Drawlib SVG Fonts */"
    css_blocks: list[str] = [f"\n{marker}"]
    for rec in active_records:
        dst_abs = os.path.normpath(os.path.join(output_abs, rec["rel_path"]))
        rel_url = os.path.relpath(dst_abs, css_dir).replace(os.sep, "/")
        css_blocks.append(
            f"@font-face {{\n"
            f"  font-family: '{rec['family']}';\n"
            f"  src: url('{rel_url}') format('{rec['format']}');\n"
            f"  font-weight: normal;\n"
            f"  font-style: normal;\n"
            f"  font-display: block;\n"
            f"}}"
        )
    with open(css_file_path, "r", encoding="utf-8") as cf:
        existing_css = cf.read()
    if marker in existing_css:
        existing_css = existing_css.split(marker, 1)[0].rstrip() + "\n"
    with open(css_file_path, "w", encoding="utf-8") as cf:
        cf.write(existing_css + "\n".join(css_blocks) + "\n")


def bundle_svg_fonts(
    output_abs: str,
    css_file_path: Optional[str] = None,
) -> list[dict[str, str]]:
    """Scan generated SVG files in output_abs, copy used fonts to _assets/fonts/, and inject @font-face CSS.

    Args:
        output_abs: Absolute path to the build output directory.
        css_file_path: Optional path to style.css where @font-face declarations should be appended.

    Returns:
        list[dict[str, str]]: List of bundled font metadata records.
    """
    if not os.path.isdir(output_abs):
        return []

    bundled_records = _collect_svg_font_records(output_abs)
    if not bundled_records:
        return []

    active_records: list[dict[str, str]] = []
    for rec in bundled_records:
        abs_src = _resolve_font_src_spec(rec["src"])
        if not os.path.isfile(abs_src):
            continue
        dst_path = os.path.normpath(os.path.join(output_abs, rec["rel_path"]))
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        if os.path.abspath(abs_src) != os.path.abspath(dst_path):
            shutil.copy2(abs_src, dst_path)
        active_records.append(rec)

    if active_records and css_file_path and os.path.isfile(css_file_path):
        _write_svg_font_faces_css(output_abs, css_file_path, active_records)

    return active_records


def format_asset_markup(
    file_name: str,
    alt_text: str,
    output_abs: str = "",
    options: Optional[DrawlibBlockOptions] = None,
) -> str:
    """Format HTML markup for a rendered slide asset to fill its parent block container.

    Args:
        file_name: Image filename or relative path on disk.
        alt_text: Alt text attribute.
        output_abs: Absolute path to output directory for inlining SVGs and Base64 animation data.
        options: Parsed drawlib block options for animation playback controls.

    Returns:
        str: Generated HTML snippet.
    """
    if file_name.lower().endswith(".svg") and output_abs:
        svg_disk = os.path.normpath(os.path.join(output_abs, file_name))
        if os.path.exists(svg_disk):
            with open(svg_disk, encoding="utf-8") as f:
                svg_content = f.read()
            svg_clean = re.sub(r"<\?xml[^>]*\?>", "", svg_content)
            svg_clean = re.sub(r"<!DOCTYPE[^>]*>", "", svg_clean)
            svg_clean = _PATTERN_SVG_FONTS_COMMENT.sub("", svg_clean).strip()
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

    has_anim_opts = options is not None and (
        options.anim_trigger is not None
        or options.anim_loop is not None
        or bool(options.anim_pause)
    )
    if has_anim_opts and options is not None and file_name.lower().endswith((".png", ".apng", ".webp")):
        trigger = options.anim_trigger or "auto"
        loop = options.anim_loop or ("once" if options.anim_pause else "infinite")
        pause_attr = (
            f' data-anim-pause="{",".join(str(p) for p in options.anim_pause)}"'
            if options.anim_pause
            else ""
        )
        base64_attr = ""
        if output_abs:
            anim_disk = os.path.normpath(os.path.join(output_abs, file_name))
            if os.path.isfile(anim_disk):
                with contextlib.suppress(OSError):
                    with open(anim_disk, "rb") as af:
                        b64_data = base64.b64encode(af.read()).decode("ascii")
                    base64_attr = f' data-base64="{b64_data}"'
        return (
            f'\n<figure class="drawlib-image drawlib-anim-container" '
            f'data-anim-trigger="{trigger}" data-anim-loop="{loop}"{pause_attr}>\n'
            f'  <canvas class="drawlib-anim-canvas" data-src="{file_name}"{base64_attr} '
            f'role="img" aria-label="{alt_text}"></canvas>\n'
            f'  <div class="anim-play-badge" title="Click to play / continue animation">\n'
            f'    <svg class="play-icon" viewBox="0 0 24 24">'
            f'<polygon points="6 4 20 12 6 20" fill="currentColor"></polygon></svg>\n'
            f'    <svg class="replay-icon" viewBox="0 0 24 24">'
            f'<path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4'
            f'c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z" fill="currentColor"></path></svg>\n'
            f"  </div>\n"
            f"</figure>\n"
        )

    return (
        f'\n<figure class="drawlib-image">\n'
        f'  <img src="{file_name}" alt="{alt_text}" class="slide-raster-graphic" '
        f'style="width: 100%; height: 100%; object-fit: contain;" />\n'
        f"</figure>\n"
    )


def copy_static_assets(input_abs: str, output_abs: str) -> None:
    """Copy static image and font assets from input directory to output directory.

    Args:
        input_abs: Source directory.
        output_abs: Target directory.
    """
    for asset_file in os.listdir(input_abs):
        asset_lower = asset_file.lower()
        if (
            asset_lower.endswith((".png", ".apng", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ttf", ".woff", ".woff2"))
            and not asset_lower.startswith(".")
        ):
            src_p = os.path.join(input_abs, asset_file)
            dst_p = os.path.join(output_abs, asset_file)
            if not os.path.exists(dst_p):
                shutil.copy2(src_p, dst_p)


def deploy_slide_assets(input_abs: str, output_abs: str, deck_theme: str) -> None:
    """Deploy style.css, slide.js, static assets, and auto-bundled SVG fonts to the output directory.

    Args:
        input_abs: Input directory containing potential style.css overrides and assets.
        output_abs: Output directory.
        deck_theme: Chosen CSS theme name.
    """
    local_style_css = os.path.join(input_abs, "style.css")
    local_slide_css = os.path.join(input_abs, "slide.css")
    if os.path.isfile(local_style_css):
        with open(local_style_css, "r", encoding="utf-8") as f:
            css_content = f.read()
    elif os.path.isfile(local_slide_css):
        with open(local_slide_css, "r", encoding="utf-8") as f:
            css_content = f.read()
    else:
        css_content = get_css(name=deck_theme, target="slide")

    style_css_out = os.path.join(output_abs, "style.css")
    with open(style_css_out, "w", encoding="utf-8") as f:
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

    bundle_svg_fonts(output_abs, css_file_path=style_css_out)
