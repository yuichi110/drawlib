# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""CLI subcommands for inspecting and visualizing preset color catalogs."""

from __future__ import annotations

import os
import sys
import tempfile
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from drawlib._cli._help import HELP_EPILOG
from drawlib._cli._visualizers._common import display_dimage
from drawlib._cli._visualizers.colors import SortMode, render_color_chart
from drawlib._core.l3_colors import BaseColors
from drawlib._preset_colors import (
    CssColors,
    DefaultColors,
    DefaultColors1,
    DefaultColors2,
    DefaultColors3,
    DefaultColors4,
    DefaultColors5,
    DefaultColors6,
    GoogleColors,
    MonochromeColors,
)

console = Console()
_HELP_CTX = {"help_option_names": ["-h", "--help"]}

colors_app = typer.Typer(
    name="colors",
    help="Inspect and visualize preset color catalogs.",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)

_PRESET_MAP: dict[str, tuple[BaseColors | type[BaseColors], str]] = {
    "default": (DefaultColors, "DefaultColors (Drawlib Default Palette)"),
    "def": (DefaultColors, "DefaultColors (Drawlib Default Palette)"),
    "default1": (DefaultColors1, "DefaultColors1 (Drawlib Tone 1 Ultra Light)"),
    "default2": (DefaultColors2, "DefaultColors2 (Drawlib Tone 2 Light)"),
    "default3": (DefaultColors3, "DefaultColors3 (Drawlib Tone 3 Medium Soft)"),
    "default4": (DefaultColors4, "DefaultColors4 (Drawlib Tone 4 Standard Base)"),
    "default5": (DefaultColors5, "DefaultColors5 (Drawlib Tone 5 Deep)"),
    "default6": (DefaultColors6, "DefaultColors6 (Drawlib Tone 6 Darkest Shade)"),
    "google": (GoogleColors, "GoogleColors (Official Google Palette)"),
    "monochrome": (MonochromeColors, "MonochromeColors (Grayscale Palette)"),
    "mono": (MonochromeColors, "MonochromeColors (Grayscale Palette)"),
    "css": (CssColors, "CssColors (W3C CSS Named Colors)"),
}


@colors_app.command("list", epilog=HELP_EPILOG)
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


@colors_app.command("show", epilog=HELP_EPILOG)
def cmd_colors_show(
    preset: Annotated[
        str,
        typer.Argument(help="Preset name: 'default', 'google', 'monochrome', or 'css'."),
    ],
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Save chart to image file instead of opening GUI."),
    ] = None,
    sort: Annotated[
        SortMode,
        typer.Option("--sort", help="Color sort order: 'hsv', 'name', or 'raw'."),
    ] = "hsv",
    grid: Annotated[
        bool,
        typer.Option("-g", "--grid", help="Show coordinate grid overlay."),
    ] = False,
    no_cache: Annotated[
        bool,
        typer.Option("--no-cache", help="Disable reading and writing the colors image cache."),
    ] = False,
) -> None:
    """Display or export a visual color chart for a preset color catalog."""
    key = preset.strip().lower()
    if key not in _PRESET_MAP:
        avail = ", ".join(f"'{k}'" for k in sorted(set(_PRESET_MAP.keys())))
        console.print(f"[bold red]Error:[/bold red] Unknown color preset '{preset}'. Available presets: {avail}")
        raise typer.Exit(code=1)

    instance, display_name = _PRESET_MAP[key]
    dimage = render_color_chart(instance, display_name, sort_mode=sort, grid=grid, no_cache=no_cache)

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
            console.print(
                f"[bold yellow]Notice:[/bold yellow] No GUI display ($DISPLAY) detected in this remote environment.\n"
                f"Rendered color chart to: [bold cyan]'{tmp_path}'[/bold cyan]\n"
                f"[dim]Tip: Open this in VS Code, or use '-o colors_{key}.png' to save to your workspace.[/dim]"
            )
