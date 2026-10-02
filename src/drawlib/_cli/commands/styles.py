# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""CLI subcommands for inspecting and visualizing preset style catalogs."""

from __future__ import annotations

from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from drawlib._cli._help import HELP_EPILOG
from drawlib._cli._visualizers.styles import (
    export_all_pages,
    get_styles_page_count,
    handle_single_page_output,
    render_styles_matrix,
)
from drawlib._preset_styles import (
    BaseStyles,
    DefaultStyles,
    DefaultStyles1,
    DefaultStyles2,
    DefaultStyles3,
    DefaultStyles4,
    DefaultStyles5,
    DefaultStyles6,
    GoogleStyles,
    MonochromeStyles,
)

console = Console()
_HELP_CTX = {"help_option_names": ["-h", "--help"]}

styles_app = typer.Typer(
    name="styles",
    help="Inspect and visualize preset style catalogs.",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)


def _get_preset(cls: type[BaseStyles]) -> BaseStyles:
    inst = cls.get_default_instance()
    if inst is None:
        raise RuntimeError(f"Default instance for {cls.__name__} not registered.")
    return inst


_PRESET_MAP: dict[str, tuple[BaseStyles, str]] = {
    "default": (_get_preset(DefaultStyles), "DefaultStyles (Drawlib Standard Styles - Tone 4)"),
    "def": (_get_preset(DefaultStyles), "DefaultStyles (Drawlib Standard Styles - Tone 4)"),
    "default1": (_get_preset(DefaultStyles1), "DefaultStyles1 (Drawlib Tone 1 Ultra Light)"),
    "default2": (_get_preset(DefaultStyles2), "DefaultStyles2 (Drawlib Tone 2 Light)"),
    "default3": (_get_preset(DefaultStyles3), "DefaultStyles3 (Drawlib Tone 3 Medium Soft)"),
    "default4": (_get_preset(DefaultStyles4), "DefaultStyles4 (Drawlib Tone 4 Standard Base)"),
    "default5": (_get_preset(DefaultStyles5), "DefaultStyles5 (Drawlib Tone 5 Deep)"),
    "default6": (_get_preset(DefaultStyles6), "DefaultStyles6 (Drawlib Tone 6 Darkest Shade)"),
    "monochrome": (_get_preset(MonochromeStyles), "MonochromeStyles (Grayscale / B&W Styles)"),
    "mono": (_get_preset(MonochromeStyles), "MonochromeStyles (Grayscale / B&W Styles)"),
    "google": (_get_preset(GoogleStyles), "GoogleStyles (Google Sheets Palette Styles)"),
}


@styles_app.command("list", epilog=HELP_EPILOG)
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


@styles_app.command("show", epilog=HELP_EPILOG)
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
    no_cache: Annotated[
        bool,
        typer.Option("--no-cache", help="Disable reading and writing the styles image cache."),
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
        export_all_pages(
            instance,
            short_name,
            total_pages,
            output,
            key,
            filter_color=color,
            grid=grid,
            no_cache=no_cache,
        )
        return

    if not (1 <= page <= total_pages):
        console.print(
            f"[bold red]Error:[/bold red] Invalid page {page} for preset '{preset}'. "
            f"Available pages: 1 to {total_pages}."
        )
        raise typer.Exit(code=1)

    dimage = render_styles_matrix(
        instance, short_name, page=page, filter_color=color, grid=grid, no_cache=no_cache
    )
    handle_single_page_output(dimage, output, key, short_name, page, total_pages)
