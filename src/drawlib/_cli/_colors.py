# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""CLI subcommands and chart renderer for preset color catalogs."""

from __future__ import annotations

import colorsys
import math
import os
import sys
import tempfile
from typing import Annotated, Literal, Optional

import typer
from rich.console import Console
from rich.table import Table

from drawlib._core.fonts import Font
from drawlib._core.l2_types import Color, Dimage
from drawlib._core.l3_styles import BaseColors, Style
from drawlib._preset_colors import (
    DefaultColors,
    GoogleColors,
    MonochromeColors,
    colors_16,
    colors_140,
)
from drawlib.canvas import clear, get_dimage, setup
from drawlib.shapes import rectangle
from drawlib.text import text

console = Console()
_HELP_CTX = {"help_option_names": ["-h", "--help"]}

colors_app = typer.Typer(
    name="colors",
    help="Inspect and visualize preset color catalogs.",
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)

SortMode = Literal["hsv", "name", "raw"]

_PRESET_MAP: dict[str, tuple[BaseColors | type[BaseColors], str]] = {
    "140": (colors_140, "Colors140 (CSS 140 Web Colors)"),
    "colors140": (colors_140, "Colors140 (CSS 140 Web Colors)"),
    "16": (colors_16, "Colors16 (Basic 16 Web Colors)"),
    "colors16": (colors_16, "Colors16 (Basic 16 Web Colors)"),
    "colors": (colors_16, "Colors16 (Basic 16 Web Colors)"),
    "default": (DefaultColors, "DefaultColors (Drawlib Default Palette)"),
    "google": (GoogleColors, "GoogleColors (Official Google Palette)"),
    "monochrome": (MonochromeColors, "MonochromeColors (Grayscale Palette)"),
    "mono": (MonochromeColors, "MonochromeColors (Grayscale Palette)"),
}


def _sort_colors(items: list[tuple[str, Color]], mode: SortMode) -> list[tuple[str, Color]]:
    """Sort color items by HSV, name, or raw definition order.

    Args:
        items (list[tuple[str, Color]]): List of (name, Color) pairs.
        mode (SortMode): Sorting mode ('hsv', 'name', or 'raw').

    Returns:
        list[tuple[str, Color]]: Sorted list of (name, Color) pairs.
    """
    if mode == "raw":
        return items
    if mode == "name":
        return sorted(items, key=lambda x: x[0].lower())

    def _hsv_key(item: tuple[str, Color]) -> tuple[int, float, float, float]:
        _, col = item
        if col.alpha == 0.0:
            return (0, 0.0, 0.0, 0.0)

        r, g, b = col.r / 255.0, col.g / 255.0, col.b / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # Grayscale / Low saturation (< 0.08)
        if s < 0.08:
            return (1, 0.0, -round(v, 3), 0.0)

        # Chromatic colors sorted by Hue, then Value, then Saturation
        return (2, round(h, 2), round(v, 2), round(s, 2))

    return sorted(items, key=_hsv_key)


_SEMANTIC_KEYS: tuple[str, ...] = ("Primary", "Secondary", "Accent", "Muted", "Danger", "Success")


def _draw_color_tile(
    cx: float,
    cy: float,
    tile_w: float,
    tile_h: float,
    col_name: str,
    col: Color,
) -> None:
    """Draw a single color swatch tile with color name and hex code.

    Args:
        cx (float): Center X coordinate.
        cy (float): Center Y coordinate.
        tile_w (float): Tile width.
        tile_h (float): Tile height.
        col_name (str): Color name label.
        col (Color): Color instance.
    """
    if col.alpha == 0.0:
        rectangle(
            (cx, cy),
            width=tile_w - 1.2,
            height=tile_h - 1.2,
            r=0.8,
            style=Style(
                shape_fill_color=Color(255, 255, 255),
                shape_line_color=Color(180, 180, 180),
                shape_line_width=1,
                shape_line_style="dashed",
            ),
        )
        text_color = Color(80, 80, 80)
        hex_str = "Alpha 0.0"
    else:
        rectangle(
            (cx, cy),
            width=tile_w - 1.2,
            height=tile_h - 1.2,
            r=0.8,
            style=Style(
                shape_fill_color=col,
                shape_line_color=Color(200, 200, 200, 0.6),
                shape_line_width=1,
            ),
        )
        lum = (col.r * 299 + col.g * 587 + col.b * 114) / 1000
        text_color = Color(0, 0, 0) if lum > 140 else Color(255, 255, 255)
        hex_str = col.hex

    if len(col_name) >= 16:
        font_size = 6.5
    elif len(col_name) >= 13:
        font_size = 7.5
    elif len(col_name) >= 10:
        font_size = 8.5
    else:
        font_size = 9.0

    label = f"{col_name}\n{hex_str}"
    text(
        (cx, cy),
        label,
        style=Style(
            text_color=text_color,
            text_size=font_size,
            text_font=Font.SANSSERIF_BOLD,
        ),
    )


def render_color_chart(
    colors: BaseColors | type[BaseColors],
    name: str,
    *,
    sort_mode: SortMode = "hsv",
    grid: bool = False,
) -> Dimage:
    """Render a dynamic visual color chart for any BaseColors instance.

    Args:
        colors (BaseColors): BaseColors instance containing color attributes.
        name (str): Display name of the color palette.
        sort_mode (SortMode): Sorting strategy ('hsv', 'name', or 'raw'). Defaults to 'hsv'.
        grid (bool): Whether to overlay coordinate grid. Defaults to False.

    Returns:
        Dimage: Rendered in-memory image.
    """
    semantic_items = [(k, getattr(colors, k)) for k in _SEMANTIC_KEYS if getattr(colors, k, None) is not None]
    has_semantics = len(semantic_items) > 0

    raw_items = [(k, v) for k, v in colors if k not in _SEMANTIC_KEYS]
    items = _sort_colors(raw_items, sort_mode)
    n = len(items)

    # 1. Determine optimal grid columns
    if n <= 8:
        cols = 4
    elif n <= 24:
        cols = 4
    elif n <= 60:
        cols = 6
    else:
        cols = 10
    if has_semantics:
        cols = max(cols, len(semantic_items))
    rows = math.ceil(n / cols)

    tile_w = 17.0
    tile_h = 10.5
    margin_x = 6.0
    margin_y = 6.0
    header_h = 10.0
    semantic_h = 17.0 if has_semantics else 0.0

    canvas_w = int(math.ceil(margin_x * 2 + cols * tile_w))
    canvas_h = int(math.ceil(margin_y * 2 + rows * tile_h + header_h + semantic_h))

    # 2. Canvas setup
    clear()
    setup(width=canvas_w, height=canvas_h, grid=grid)

    # 3. Title Header
    title_text = f"{name} ({n} colors)"
    text(
        (canvas_w / 2, canvas_h - margin_y - header_h / 2),
        title_text,
        style=Style(
            text_size=16,
            text_font=Font.SANSSERIF_BOLD,
            text_color=Color(40, 40, 40),
        ),
    )

    # 4. Semantic Theme Row
    if has_semantics:
        sem_title_y = canvas_h - margin_y - header_h - 2.5
        sem_names = ", ".join(k for k, _ in semantic_items)
        text(
            (canvas_w / 2, sem_title_y),
            f"Semantic Theme Colors ({sem_names})",
            style=Style(
                text_size=9.5,
                text_font=Font.SANSSERIF_BOLD,
                text_color=Color(70, 70, 70),
            ),
        )
        sem_total_w = len(semantic_items) * tile_w
        sem_start_x = (canvas_w - sem_total_w) / 2
        sem_cy = sem_title_y - (tile_h / 2 + 2.0)
        for s_idx, (s_name, s_col) in enumerate(semantic_items):
            s_cx = sem_start_x + s_idx * tile_w + tile_w / 2
            _draw_color_tile(s_cx, sem_cy, tile_w, tile_h, s_name, s_col)

    # 5. Main Palette Swatches Grid
    start_y = canvas_h - margin_y - header_h - semantic_h
    for idx, (col_name, col) in enumerate(items):
        r_idx = idx // cols
        c_idx = idx % cols

        cx = margin_x + c_idx * tile_w + tile_w / 2
        cy = start_y - (r_idx * tile_h + tile_h / 2)
        _draw_color_tile(cx, cy, tile_w, tile_h, col_name, col)

    return get_dimage()


def _display_dimage(dimage: Dimage) -> None:
    """Display Dimage using PIL Image.show() unless disabled by environment."""
    if os.environ.get("DRAWLIB_SHOW_NO_DISPLAY") != "1":
        dimage.get_pil_image().show()


@colors_app.command("list")
def cmd_colors_list() -> None:
    """List all available built-in color presets."""
    table = Table(title="Drawlib Preset Colors", header_style="bold cyan")
    table.add_column("Preset Alias", style="bold")
    table.add_column("Class Name")
    table.add_column("Colors Count", justify="right")
    table.add_column("Description")

    visited = set()
    for alias, (instance, desc) in _PRESET_MAP.items():
        cls_name = instance.__name__ if isinstance(instance, type) else instance.__class__.__name__
        if cls_name in visited:
            continue
        visited.add(cls_name)
        count = len(list(instance))
        table.add_row(alias, cls_name, str(count), desc)

    console.print(table)


@colors_app.command("show")
def cmd_colors_show(
    preset: Annotated[
        str,
        typer.Argument(help="Preset name: '140', 'google', 'default', 'monochrome', '16'."),
    ],
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Save chart to image file instead of opening GUI."),
    ] = None,
    sort: Annotated[
        SortMode,
        typer.Option("--sort", "-s", help="Color sort order: 'hsv', 'name', or 'raw'."),
    ] = "hsv",
    grid: Annotated[
        bool,
        typer.Option("-g", "--grid", help="Show coordinate grid overlay."),
    ] = False,
) -> None:
    """Display or export a visual color chart for a preset color catalog."""
    key = preset.strip().lower()
    if key not in _PRESET_MAP:
        avail = ", ".join(f"'{k}'" for k in sorted(set(_PRESET_MAP.keys())))
        console.print(f"[bold red]Error:[/bold red] Unknown color preset '{preset}'. Available presets: {avail}")
        raise typer.Exit(code=1)

    instance, display_name = _PRESET_MAP[key]
    dimage = render_color_chart(instance, display_name, sort_mode=sort, grid=grid)

    if output:
        dest_abs = os.path.abspath(output)
        try:
            dimage.save(dest_abs)
            msg = f"[bold green]Success:[/bold green] Exported color chart to [bold cyan]'{dest_abs}'[/bold cyan]."
            console.print(msg)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] Failed to save image to '{dest_abs}': {e}")
            raise typer.Exit(code=1)
    else:
        with tempfile.NamedTemporaryFile(suffix=".png", prefix=f"drawlib_colors_{key}_", delete=False) as tmp:
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
            console.print(
                f"[bold yellow]Notice:[/bold yellow] No GUI display ($DISPLAY) detected in this remote environment.\n"
                f"Rendered color chart to: [bold cyan]'{tmp_path}'[/bold cyan]\n"
                f"[dim]Tip: Open this in VS Code, or use '-o colors_{key}.png' to save to your workspace.[/dim]"
            )
