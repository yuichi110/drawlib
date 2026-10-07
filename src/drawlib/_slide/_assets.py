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

import os
import re
import shutil
from typing import TYPE_CHECKING, Optional

from drawlib._templates import get_css, get_slide_js

if TYPE_CHECKING:
    from drawlib._builder.doc_builder.processor.options import DrawlibBlockOptions


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
        output_abs: Absolute path to output directory for inlining SVGs.
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
        return (
            f'\n<figure class="drawlib-image drawlib-anim-container" '
            f'data-anim-trigger="{trigger}" data-anim-loop="{loop}"{pause_attr}>\n'
            f'  <canvas class="drawlib-anim-canvas" data-src="{file_name}" '
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
