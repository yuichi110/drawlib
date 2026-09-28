# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""CLI subcommands and matrix visualizer for preset style catalogs."""

from __future__ import annotations

import math
import os
import sys
import tempfile
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from drawlib._core.fonts import Font
from drawlib._core.l2_types import Color, Dimage
from drawlib._core.l3_styles import Style
from drawlib._preset_styles import (
    BaseStyles,
    default_styles,
    google_styles,
    monochrome_styles,
)
from drawlib.canvas import clear, get_dimage, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text

console = Console()
_HELP_CTX = {"help_option_names": ["-h", "--help"]}

styles_app = typer.Typer(
    name="styles",
    help="Inspect and visualize preset style catalogs.",
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)

_PRESET_MAP: dict[str, tuple[BaseStyles, str]] = {
    "default": (default_styles, "DefaultStyles (Drawlib Standard Styles)"),
    "def": (default_styles, "DefaultStyles (Drawlib Standard Styles)"),
    "monochrome": (monochrome_styles, "MonochromeStyles (Grayscale / B&W Styles)"),
    "mono": (monochrome_styles, "MonochromeStyles (Grayscale / B&W Styles)"),
    "google": (google_styles, "GoogleStyles (Google Sheets Palette Styles)"),
}

_COL_HEADERS = ["standard", "flat", "solid", "dashed", "bold", "light"]
_VARIANTS = ["flat", "solid", "dashed", "bold", "light"]
_THEME_KEYS = ["primary", "flat", "solid", "dashed", "bold", "light"]
_SYSTEM_FIELDS = {"primary", "flat", "solid", "dashed", "bold", "light", "background_color", "sourcecode_font"}


def _extract_base_colors(styles: BaseStyles, filter_color: str | None = None) -> list[str]:
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
    for field_name in type(styles).model_fields:
        if field_name in _SYSTEM_FIELDS:
            continue
        base = field_name
        for v in _VARIANTS:
            if field_name.endswith(f"_{v}"):
                base = field_name[: -len(f"_{v}")]
                break
        if base not in base_colors:
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
    base_colors = _extract_base_colors(styles, filter_color)
    return max(1, math.ceil(len(base_colors) / page_size))


def _render_legend(styles: BaseStyles, legend_cx: float, legend_y: float) -> None:
    """Render the single reference legend card showing Shape, Text Style, and Line style.

    Args:
        styles (BaseStyles): Active BaseStyles instance.
        legend_cx (float): Center X coordinate of legend card.
        legend_y (float): Center Y coordinate of legend card.
    """
    legend_w = 88.0
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
        (legend_cx - 36.0, legend_y),
        "Legend:",
        style=Style(text_size=8.5, text_font=Font.SANSSERIF_BOLD, text_color=Color(80, 80, 80)),
    )

    st_sample = styles.primary
    fill_c = Color(st_sample.shape_fill_color or (255, 255, 255))
    lum = (fill_c.r * 299 + fill_c.g * 587 + fill_c.b * 114) / 1000
    legend_text_color = Color(0, 0, 0) if lum > 140 else Color(255, 255, 255)

    rectangle(
        (legend_cx - 20.0, legend_y),
        width=14.0,
        height=4.6,
        r=0.6,
        style=st_sample,
        text="Shape",
        textstyle=Style(text_size=7.2, text_font=Font.SANSSERIF_BOLD, text_color=legend_text_color),
    )
    text(
        (legend_cx + 2.0, legend_y),
        "Text Style",
        style=Style(
            text_size=8.5,
            text_font=Font.SANSSERIF_BOLD,
            text_color=Color(st_sample.text_color or (40, 40, 40)),
        ),
    )
    line(
        (legend_cx + 18.0, legend_y),
        (legend_cx + 36.0, legend_y),
        arrowhead="->",
        style=st_sample,
    )


def _draw_swatch(
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
    if not key or not hasattr(styles, key):
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
            textstyle=Style(
                text_size=8,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=Color(210, 210, 210),
            ),
        )
        return

    st: Style = getattr(styles, key)

    if "solid" in key or "dashed" in key:
        line_c = Color(st.line_color or (50, 50, 50))
        l_lum = (line_c.r * 299 + line_c.g * 587 + line_c.b * 114) / 1000
        text_c = line_c if l_lum < 160 else Color(40, 40, 40)
    else:
        fill_color = Color(st.shape_fill_color or (255, 255, 255))
        f_lum = (fill_color.r * 299 + fill_color.g * 587 + fill_color.b * 114) / 1000
        text_c = Color(0, 0, 0) if f_lum > 140 else Color(255, 255, 255)

    font_size = 6.4 if len(key) >= 16 else 7.2
    t_style = Style(text_color=text_c, text_size=font_size, text_font=Font.SANSSERIF_BOLD)
    rectangle(
        (cx, cy),
        width=tile_w - 1.2,
        height=tile_h - 1.0,
        r=0.6,
        style=st,
        text=key,
        textstyle=t_style,
    )


def render_styles_matrix(
    styles: BaseStyles,
    name: str,
    *,
    page: int = 1,
    page_size: int = 25,
    filter_color: str | None = None,
    grid: bool = False,
) -> Dimage:
    """Render an orthogonal visual matrix for a BaseStyles catalog page.

    Displays a single reference legend at the top (Shape swatch, Text Style, Arrow line),
    followed by an orthogonal grid where columns represent variants (standard, flat, solid,
    dashed, bold, light) and rows represent base colors for the specified page.

    Args:
        styles (BaseStyles): BaseStyles instance containing style attributes.
        name (str): Display name for the catalog header.
        page (int): 1-indexed page number to render. Defaults to 1.
        page_size (int): Number of colors per page. Defaults to 25.
        filter_color (str | None): Optional substring to filter base colors. Defaults to None.
        grid (bool): Whether to overlay coordinate grid. Defaults to False.

    Returns:
        Dimage: Rendered in-memory image.

    Raises:
        ValueError: If page is less than 1 or exceeds total pages.
    """
    base_colors = _extract_base_colors(styles, filter_color)
    total_pages = max(1, math.ceil(len(base_colors) / page_size))
    if page < 1 or page > total_pages:
        raise ValueError(f"Invalid page {page}. Available pages: 1 to {total_pages}.")

    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, len(base_colors))
    page_colors = base_colors[start_idx:end_idx]

    rows: list[tuple[str, list[str | None]]] = []
    if page == 1 and (filter_color is None or "primary" in filter_color.lower() or "theme" in filter_color.lower()):
        rows.append(("primary (theme)", list(_THEME_KEYS)))

    for b in page_colors:
        row_keys: list[str | None] = [
            b if hasattr(styles, b) else None,
            f"{b}_flat" if hasattr(styles, f"{b}_flat") else None,
            f"{b}_solid" if hasattr(styles, f"{b}_solid") else None,
            f"{b}_dashed" if hasattr(styles, f"{b}_dashed") else None,
            f"{b}_bold" if hasattr(styles, f"{b}_bold") else None,
            f"{b}_light" if hasattr(styles, f"{b}_light") else None,
        ]
        rows.append((b, row_keys))

    cols = len(_COL_HEADERS)
    n_rows = len(rows)

    tile_w = 22.0
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
    _render_legend(styles, canvas_w / 2, legend_y)

    col_start_y = legend_y - 6.5
    for c_idx, h in enumerate(_COL_HEADERS):
        cx = margin_x + c_idx * tile_w + tile_w / 2
        text(
            (cx, col_start_y),
            h,
            style=Style(text_size=9.5, text_font=Font.SANSSERIF_BOLD, text_color=Color(50, 50, 50)),
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
            _draw_swatch(styles, key, cx, cy, tile_w, tile_h)

    return get_dimage()


def _display_dimage(dimage: Dimage) -> None:
    """Display Dimage using PIL Image.show() unless disabled by environment."""
    if os.environ.get("DRAWLIB_SHOW_NO_DISPLAY") != "1":
        dimage.get_pil_image().show()


def _export_all_pages(
    styles: BaseStyles,
    short_name: str,
    total_pages: int,
    output: str | None,
    key: str,
    *,
    filter_color: str | None,
    grid: bool,
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
    """
    saved_paths: list[str] = []
    for p in range(1, total_pages + 1):
        dimage = render_styles_matrix(styles, short_name, page=p, filter_color=filter_color, grid=grid)
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


def _handle_single_page_output(
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

        has_display = bool(os.environ.get("DISPLAY")) or sys.platform in {"darwin", "win32"}
        if has_display:
            try:
                _display_dimage(dimage)
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


@styles_app.command("list")
def cmd_styles_list() -> None:
    """List all available built-in style preset catalogs."""
    table = Table(title="Drawlib Preset Styles", header_style="bold cyan")
    table.add_column("Preset Alias", style="bold")
    table.add_column("Class Name")
    table.add_column("Styles Count", justify="right")
    table.add_column("Description")

    visited: set[str] = set()
    for alias, (instance, desc) in _PRESET_MAP.items():
        cls_name = instance.__class__.__name__
        if cls_name in visited:
            continue
        visited.add(cls_name)
        count = len(instance.styles())
        table.add_row(alias, cls_name, str(count), desc)

    console.print(table)


@styles_app.command("show")
def cmd_styles_show(
    preset: Annotated[
        str,
        typer.Argument(help="Preset name: 'default', 'monochrome', or 'google'."),
    ],
    page: Annotated[
        int,
        typer.Argument(help="Page number (1-indexed, 25 colors per page). Defaults to 1."),
    ] = 1,
    all_pages: Annotated[
        bool,
        typer.Option("--all", "-a", help="Export all pages at once (e.g. styles_google_1.png, ...)."),
    ] = False,
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Save chart to image file instead of opening GUI."),
    ] = None,
    color: Annotated[
        Optional[str],
        typer.Option("-c", "--color", help="Filter by base color or hue name (e.g. 'blue', 'red')."),
    ] = None,
    grid: Annotated[
        bool,
        typer.Option("-g", "--grid", help="Show coordinate grid overlay."),
    ] = False,
) -> None:
    """Display or export a visual style matrix for a preset style catalog."""
    key = preset.strip().lower()
    if key not in _PRESET_MAP:
        avail = ", ".join(f"'{k}'" for k in sorted(set(_PRESET_MAP.keys())))
        console.print(f"[bold red]Error:[/bold red] Unknown style preset '{preset}'. Available presets: {avail}")
        raise typer.Exit(code=1)

    instance, display_name = _PRESET_MAP[key]
    short_name = display_name.split()[0]

    try:
        total_pages = get_styles_page_count(instance, filter_color=color)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    if all_pages:
        _export_all_pages(instance, short_name, total_pages, output, key, filter_color=color, grid=grid)
        return

    if not (1 <= page <= total_pages):
        console.print(
            f"[bold red]Error:[/bold red] Invalid page {page} for preset '{preset}'. "
            f"Available pages: 1 to {total_pages}."
        )
        raise typer.Exit(code=1)

    dimage = render_styles_matrix(instance, short_name, page=page, filter_color=color, grid=grid)
    _handle_single_page_output(dimage, output, key, short_name, page, total_pages)
