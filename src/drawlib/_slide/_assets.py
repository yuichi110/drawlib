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

from drawlib._templates import get_css, get_slide_js


def format_asset_markup(
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


def copy_static_assets(input_abs: str, output_abs: str) -> None:
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
