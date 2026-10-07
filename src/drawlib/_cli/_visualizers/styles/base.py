# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base styles matrix visualizer components and shared drawing routines."""

from __future__ import annotations

import io
import math
import os
import sys
import tempfile

import typer
from PIL import Image
from rich.console import Console

from drawlib import LIB_VERSION
from drawlib._builder._common.cache import CliImageCache, hash_text
from drawlib._cli._visualizers._common import display_dimage
from drawlib._core.l3_colors import Color, ColorUtil
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_images import Dimage
from drawlib._core.l3_styles import Style
from drawlib._preset_styles import BaseStyles
from drawlib.canvas import clear, get_dimage, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text

console = Console()

COL_HEADERS: list[str] = [
    "Bordered",
    "Bold",
    "Thin",
    "Flat",
    "Outline",
    "OutlineBold",
    "OutlineThin",
    "Dashed",
    "DashedBold",
    "DashedThin",
]

VARIANTS: list[str] = [
    "Bordered",
    "Bold",
    "Thin",
    "Flat",
    "Outline",
    "Solid",
    "OutlineBold",
    "SolidBold",
    "OutlineThin",
    "SolidThin",
    "Dashed",
    "DashedBold",
    "DashedThin",
    "Dotted",
    "DottedBold",
    "DottedThin",
]

SEMANTIC_ROLES: list[str] = [
    "Primary",
    "Secondary",
    "Accent",
    "Muted",
    "Danger",
    "Success",
    "Warning",
    "Light",
    "Dark",
    "Neutral",
]

SYSTEM_FIELDS: set[str] = {
    "width",
    "height",
    "dpi",
    "colors",
    "background_color",
    "sourcecode_font",
    "Canvas",
    "CanvasFlat",
    *SEMANTIC_ROLES,
    *(f"{role}{v}" for role in SEMANTIC_ROLES for v in VARIANTS),
}


def get_row_keys(styles: BaseStyles, base: str) -> list[str | None]:
    """Retrieve 10 style keys for a given base name across the 10 orthogonal columns.

    Args:
        styles (BaseStyles): Active BaseStyles instance.
        base (str): Base color or semantic role name.

    Returns:
        list[str | None]: 10 style attribute names or None if unsupported.
    """

    def _has_key(k: str) -> bool:
        try:
            return isinstance(getattr(styles, k, None), Style)
        except AttributeError:
            return False

    return [
        base if _has_key(base) else (f"{base}Bordered" if _has_key(f"{base}Bordered") else None),
        f"{base}Bold" if _has_key(f"{base}Bold") else None,
        f"{base}Thin" if _has_key(f"{base}Thin") else None,
        f"{base}Flat" if _has_key(f"{base}Flat") else None,
        f"{base}Outline" if _has_key(f"{base}Outline") else (f"{base}Solid" if _has_key(f"{base}Solid") else None),
        f"{base}OutlineBold"
        if _has_key(f"{base}OutlineBold")
        else (f"{base}SolidBold" if _has_key(f"{base}SolidBold") else None),
        f"{base}OutlineThin"
        if _has_key(f"{base}OutlineThin")
        else (f"{base}SolidThin" if _has_key(f"{base}SolidThin") else None),
        f"{base}Dashed" if _has_key(f"{base}Dashed") else None,
        f"{base}DashedBold" if _has_key(f"{base}DashedBold") else None,
        f"{base}DashedThin" if _has_key(f"{base}DashedThin") else None,
    ]


def format_supports_badge(supports: frozenset[str]) -> str:
    """Format a compact badge showing supported drawing targets.

    Args:
        supports (frozenset[str]): Supported target features.

    Returns:
        str: Compact badge text (e.g. '[S L T I]').
    """
    tags: list[str] = []
    if "shape" in supports:
        tags.append("S")
    if "line" in supports:
        tags.append("L")
    if "text" in supports:
        tags.append("T")
    if "icon" in supports:
        tags.append("I")
    if "image" in supports:
        tags.append("M")
    return f"[{' '.join(tags)}]"


def extract_base_colors(styles: BaseStyles, filter_color: str | None = None) -> list[str]:
    """Discover and optionally filter base color names from preset style model fields.

    Args:
        styles (BaseStyles): BaseStyles instance.
        filter_color (str | None): Optional search substring to filter colors.

    Returns:
        list[str]: Discovered base color names.

    Raises:
        ValueError: If filter_color is specified but matches no colors.
    """
    base_colors: list[str] = []
    sorted_variants = sorted(VARIANTS, key=len, reverse=True)
    model_cls = styles if isinstance(styles, type) else type(styles)
    for field_name in model_cls.model_fields:
        if field_name in SYSTEM_FIELDS or field_name.endswith("Neutral") or field_name.endswith("NeutralFlat"):
            continue
        base = field_name
        for v in sorted_variants:
            if field_name.endswith(v):
                base = field_name[: -len(v)]
                break
        if base and base not in base_colors:
            base_colors.append(base)

    if filter_color is not None:
        target = filter_color.strip().lower()
        matched = [b for b in base_colors if target in b.lower()]
        if not matched:
            raise ValueError(f"No base colors match filter '{filter_color}'. Available: {', '.join(base_colors[:15])}")
        return matched

    return base_colors


def get_styles_page_count(
    styles: BaseStyles,
    *,
    page_size: int = 25,
    filter_color: str | None = None,
) -> int:
    """Calculate the total number of pages required to display a styles catalog.

    Args:
        styles (BaseStyles): BaseStyles instance.
        page_size (int): Number of colors per page. Defaults to 25.
        filter_color (str | None): Optional color filter. Defaults to None.

    Returns:
        int: Total number of pages (at least 1).
    """
    base_colors = extract_base_colors(styles, filter_color)
    return max(1, math.ceil(len(base_colors) / page_size))


def render_legend(styles: BaseStyles, legend_cx: float, legend_y: float) -> None:
    """Render the single reference legend card showing Shape, Text Style, Line style, and badges.

    Args:
        styles (BaseStyles): Active BaseStyles instance.
        legend_cx (float): Center X coordinate of legend card.
        legend_y (float): Center Y coordinate of legend card.
    """
    legend_w = 130.0
    legend_h = 7.0
    rectangle(
        (legend_cx, legend_y),
        width=legend_w,
        height=legend_h,
        r=1.2,
        style=Style(
            shape_fill_color=Color(250, 250, 250),
            shape_line_color=Color(215, 215, 215),
            shape_line_width=1,
        ),
    )
    text(
        (legend_cx - 55.0, legend_y),
        "Legend:",
        style=Style(text_size=8.5, text_font=Font.SANSSERIF_BOLD, text_color=Color(80, 80, 80)),
    )

    st_sample = styles.Primary
    fill_c = Color(st_sample.shape_fill_color or (255, 255, 255))
    legend_text_color = ColorUtil.get_contrast_text_color(
        fill_c,
        dark_color=Color(0, 0, 0),
        light_color=Color(255, 255, 255),
    )

    txt_c = Color(st_sample.text_color or (40, 40, 40))
    txt_lum = ColorUtil.get_luminance(txt_c)
    legend_txt_sample_color = Color(40, 40, 40) if txt_lum > 0.78 else txt_c

    line_c = Color(st_sample.line_color or (40, 40, 40))
    line_lum = ColorUtil.get_luminance(line_c)
    legend_arrow_style = Style(line_color=Color(40, 40, 40), line_width=1.5) if line_lum > 0.78 else st_sample

    rectangle(
        (legend_cx - 40.0, legend_y),
        width=13.0,
        height=4.6,
        r=0.6,
        style=st_sample,
        text="Shape",
        text_style=Style(text_size=7.2, text_font=Font.SANSSERIF_BOLD, text_color=legend_text_color),
    )
    text(
        (legend_cx - 21.0, legend_y),
        "Text Style",
        style=Style(
            text_size=8.5,
            text_font=Font.SANSSERIF_BOLD,
            text_color=legend_txt_sample_color,
        ),
    )
    line(
        (legend_cx - 8.0, legend_y),
        (legend_cx + 8.0, legend_y),
        arrow_head="->",
        style=legend_arrow_style,
    )
    text(
        (legend_cx + 36.0, legend_y),
        "Badges: [S]hape  [L]ine  [T]ext  [I]con",
        style=Style(
            text_size=7.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=Color(90, 90, 90),
        ),
    )


def draw_swatch(
    styles: BaseStyles,
    key: str | None,
    cx: float,
    cy: float,
    tile_w: float,
    tile_h: float,
) -> None:
    """Draw a single style swatch rectangle or empty placeholder box.

    Args:
        styles (BaseStyles): BaseStyles instance.
        key (str | None): Style attribute name or None if slot is empty.
        cx (float): Center X coordinate.
        cy (float): Center Y coordinate.
        tile_w (float): Swatch width.
        tile_h (float): Swatch height.
    """
    try:
        st: Style | None = getattr(styles, key, None) if key else None
    except AttributeError:
        st = None

    if key is None or st is None or not isinstance(st, Style):
        rectangle(
            (cx, cy),
            width=tile_w - 1.2,
            height=tile_h - 1.0,
            r=0.6,
            style=Style(
                shape_fill_color=Color(252, 252, 252),
                shape_line_color=Color(235, 235, 235),
                shape_line_width=1,
                shape_line_style="dashed",
            ),
            text="-",
            text_style=Style(
                text_size=8,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=Color(210, 210, 210),
            ),
        )
        return

    if "outline" in key.lower() or "dashed" in key.lower() or "solid" in key.lower():
        line_c = Color(st.line_color or (50, 50, 50))
        l_lum = (line_c.r * 299 + line_c.g * 587 + line_c.b * 114) / 1000
        text_c = line_c if l_lum < 160 else Color(40, 40, 40)
    else:
        fill_color = Color(st.shape_fill_color or (255, 255, 255))
        f_lum = (fill_color.r * 299 + fill_color.g * 587 + fill_color.b * 114) / 1000
        text_c = Color(0, 0, 0) if f_lum > 140 else Color(255, 255, 255)

    rectangle(
        (cx, cy),
        width=tile_w - 1.2,
        height=tile_h - 1.0,
        r=0.6,
        style=st,
    )

    badge = format_supports_badge(st.supports)
    badge_c = text_c.patch(alpha=0.75) if hasattr(text_c, "patch") else text_c
    font_size = 4.2 if len(key) >= 22 else (4.8 if len(key) >= 17 else (5.6 if len(key) >= 13 else 6.4))
    text((cx, cy + 1.1), key, style=Style(text_color=text_c, text_size=font_size, text_font=Font.SANSSERIF_BOLD))
    text((cx, cy - 1.8), badge, style=Style(text_color=badge_c, text_size=4.8, text_font=Font.SANSSERIF_REGULAR))


def get_semantic_rows(styles: BaseStyles, filter_color: str | None) -> list[tuple[str, list[str | None]]]:
    """Extract semantic role rows available in this preset style.

    Args:
        styles (BaseStyles): Preset styles instance.
        filter_color (str | None): Optional filter string.

    Returns:
        list[tuple[str, list[str | None]]]: List of (row_label, row_keys) tuples.
    """
    rows: list[tuple[str, list[str | None]]] = []
    for role in SEMANTIC_ROLES:
        try:
            has_role = isinstance(getattr(styles, role, None), Style)
        except AttributeError:
            has_role = False
        if not has_role:
            continue
        label = f"{role} (theme)" if role == "Primary" else role
        if filter_color is None or any(s in filter_color.lower() for s in (role.lower(), "theme", "semantic")):
            rows.append((label, get_row_keys(styles, role)))
    return rows


def render_styles_matrix(
    styles: BaseStyles,
    name: str,
    *,
    page: int = 1,
    page_size: int = 25,
    filter_color: str | None = None,
    grid: bool = False,
    no_cache: bool = False,
) -> Dimage:
    """Render an orthogonal visual matrix for a BaseStyles catalog page.

    Args:
        styles (BaseStyles): BaseStyles instance.
        name (str): Display name for catalog header.
        page (int): 1-indexed page number. Defaults to 1.
        page_size (int): Number of colors per page. Defaults to 25.
        filter_color (str | None): Optional substring to filter base colors.
        grid (bool): Whether to overlay coordinate grid. Defaults to False.
        no_cache (bool): If True, bypass cache. Defaults to False.

    Returns:
        Dimage: Rendered in-memory image.
    """
    preset_slug = name.strip().lower().split()[0]
    cache = CliImageCache(enabled=not no_cache)
    cache_key = hash_text(f"styles_matrix:{preset_slug}:{page}:{page_size}:{filter_color}:{grid}:{LIB_VERSION}")

    if cache.enabled:
        cached_blob = cache.get(cache_key)
        if cached_blob is not None:
            pil_img = Image.open(io.BytesIO(cached_blob))
            return Dimage(pil_img)

    base_colors = extract_base_colors(styles, filter_color)
    total_pages = max(1, math.ceil(len(base_colors) / page_size))
    if page < 1 or page > total_pages:
        raise ValueError(f"Invalid page {page}. Available pages: 1 to {total_pages}.")

    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, len(base_colors))
    page_colors = base_colors[start_idx:end_idx]

    rows: list[tuple[str, list[str | None]]] = []
    if page == 1:
        rows.extend(get_semantic_rows(styles, filter_color))

    for b in page_colors:
        rows.append((b, get_row_keys(styles, b)))

    cols = len(COL_HEADERS)
    n_rows = len(rows)

    tile_w = 20.0
    tile_h = 7.5
    margin_x = 24.0
    margin_y = 6.0
    header_h = 16.0
    col_header_h = 5.0

    canvas_w = int(math.ceil(margin_x + cols * tile_w + 6.0))
    canvas_h = int(math.ceil(margin_y * 2 + n_rows * tile_h + header_h + col_header_h))

    clear()
    setup(width=canvas_w, height=canvas_h, grid=grid)

    title_y = canvas_h - margin_y - 4.0
    page_suffix = f" (Page {page}/{total_pages})" if total_pages > 1 else ""
    text(
        (canvas_w / 2, title_y),
        f"{name} Style Catalog{page_suffix}",
        style=Style(text_size=17, text_font=Font.SANSSERIF_BOLD, text_color=Color(30, 30, 30)),
    )

    legend_y = title_y - 7.5
    render_legend(styles, canvas_w / 2, legend_y)

    col_start_y = legend_y - 6.5
    for c_idx, h in enumerate(COL_HEADERS):
        cx = margin_x + c_idx * tile_w + tile_w / 2
        text(
            (cx, col_start_y),
            h,
            style=Style(text_size=7.5, text_font=Font.SANSSERIF_BOLD, text_color=Color(50, 50, 50)),
        )

    matrix_start_y = col_start_y - 2.5
    for r_idx, (row_label, style_keys) in enumerate(rows):
        cy = matrix_start_y - (r_idx * tile_h + tile_h / 2)
        text(
            (margin_x - 2.5, cy),
            row_label,
            style=Style(
                text_size=8.0,
                text_font=Font.SANSSERIF_BOLD,
                text_halign="right",
                text_color=Color(60, 60, 60),
            ),
        )

        for c_idx, key in enumerate(style_keys):
            cx = margin_x + c_idx * tile_w + tile_w / 2
            draw_swatch(styles, key, cx, cy, tile_w, tile_h)

    dimage = get_dimage()
    if cache.enabled:
        bio = io.BytesIO()
        dimage.get_pil_image().save(bio, format="PNG")
        cache.put(
            cache_key=cache_key,
            category="styles",
            preset_name=preset_slug,
            page=page,
            has_grid=grid,
            png_blob=bio.getvalue(),
        )

    return dimage


def export_all_pages(
    styles: BaseStyles,
    short_name: str,
    total_pages: int,
    output: str | None,
    key: str,
    *,
    filter_color: str | None,
    grid: bool,
    no_cache: bool = False,
) -> None:
    """Export all pages of a style catalog sequentially to separate image files.

    Args:
        styles (BaseStyles): BaseStyles instance.
        short_name (str): Catalog short name.
        total_pages (int): Total number of pages.
        output (str | None): Base output filename or None for default.
        key (str): Catalog preset key.
        filter_color (str | None): Color filter if applied.
        grid (bool): Whether to show coordinate grid overlay.
        no_cache (bool): If True, bypass cache. Defaults to False.
    """
    saved_paths: list[str] = []
    for p in range(1, total_pages + 1):
        dimage = render_styles_matrix(
            styles, short_name, page=p, filter_color=filter_color, grid=grid, no_cache=no_cache
        )
        if output:
            base, ext = os.path.splitext(output)
            if not ext:
                ext = ".png"
            clean_base = base[:-2] if base.endswith("_1") else base
            target_path = os.path.abspath(f"{clean_base}_{p}{ext}")
        else:
            target_path = os.path.abspath(f"styles_{key}_{p}.png")

        dimage.save(target_path)
        saved_paths.append(target_path)

    console.print(f"[bold green]Success:[/bold green] Exported all {total_pages} pages:")
    for path in saved_paths:
        console.print(f"  - [bold cyan]'{path}'[/bold cyan]")


def handle_single_page_output(
    dimage: Dimage,
    output: str | None,
    key: str,
    short_name: str,
    page: int,
    total_pages: int,
) -> None:
    """Save or display single page of styles catalog.

    Args:
        dimage (Dimage): Rendered page image.
        output (str | None): User-provided output path.
        key (str): Catalog preset key.
        short_name (str): Catalog short name.
        page (int): Current page number.
        total_pages (int): Total page count.
    """
    page_info = f" (Page {page}/{total_pages})" if total_pages > 1 else ""

    if output:
        dest_abs = os.path.abspath(output)
        try:
            dimage.save(dest_abs)
            msg = (
                f"[bold green]Success:[/bold green] Exported styles chart{page_info} "
                f"to [bold cyan]'{dest_abs}'[/bold cyan]."
            )
            console.print(msg)
            if total_pages > 1:
                next_p = page + 1 if page < total_pages else 1
                console.print(
                    f"[dim]Tip: {short_name} has {total_pages} pages. "
                    f"To export another page: 'drawlib styles show {key} {next_p} -o styles_{key}_{next_p}.png', "
                    f"or use '--all' to export all pages.[/dim]"
                )
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] Failed to save image to '{dest_abs}': {e}")
            raise typer.Exit(code=1)
    else:
        prefix_tag = f"drawlib_styles_{key}_p{page}_" if total_pages > 1 else f"drawlib_styles_{key}_"
        with tempfile.NamedTemporaryFile(suffix=".png", prefix=prefix_tag, delete=False) as tmp:
            tmp_path = tmp.name
        dimage.save(tmp_path)

        has_display = (
            bool(os.environ.get("DISPLAY")) or sys.platform in {"darwin", "win32"}
        ) and os.environ.get("DRAWLIB_SHOW_NO_DISPLAY") != "1"
        if has_display:
            try:
                display_dimage(dimage)
                console.print(f"Rendered successfully to temp file: [bold cyan]'{tmp_path}'[/bold cyan]")
            except Exception:
                has_display = False

        if not has_display:
            suggested_out = f"styles_{key}_{page}.png" if total_pages > 1 else f"styles_{key}.png"
            console.print(
                f"[bold yellow]Notice:[/bold yellow] No GUI display ($DISPLAY) detected in this remote environment.\n"
                f"Rendered styles chart{page_info} to: [bold cyan]'{tmp_path}'[/bold cyan]\n"
                f"[dim]Tip: Open this in VS Code, or use '-o {suggested_out}' to save to your workspace.[/dim]"
            )
            if total_pages > 1:
                next_p = page + 1 if page < total_pages else 1
                console.print(
                    f"[dim]Info: {short_name} has {total_pages} pages in total (25 colors per page).\n"
                    f"      To view another page: uv run drawlib styles show {key} {next_p}\n"
                    f"      To export all pages:  uv run drawlib styles show {key} --all -o styles_{key}.png[/dim]"
                )
