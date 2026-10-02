# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer sub-application for `drawlib cache` commands."""

from __future__ import annotations

import sys
import traceback
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from drawlib._builder.cache_manager import clear_cache, clear_image_cache, download_cache, list_cache
from drawlib._cli._help import HELP_EPILOG
from drawlib._core.l1_core import dutil_settings

console = Console()

_HELP_CTX = {"help_option_names": ["-h", "--help"]}

cache_app = typer.Typer(
    name="cache",
    help="Manage cached font and icon assets.",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)


def _handle_cache_error(prefix: str, exc: Exception) -> None:
    """Print formatted error message and exit with status code 1."""
    print(f"{prefix}: {exc}", file=sys.stderr)
    if dutil_settings.get_logging_mode() in {"verbose", "developer"}:
        traceback.print_exc()
    raise typer.Exit(code=1)


@cache_app.command("clear", epilog=HELP_EPILOG)
def cmd_cache_clear(
    all_assets: Annotated[
        bool,
        typer.Option("--all", "-a", help="Clear all caches including fonts, icons, and SQLite image cache."),
    ] = False,
    images: Annotated[
        bool,
        typer.Option("--images", "-i", help="Clear SQLite image cache (.drawlib/cache.db)."),
    ] = False,
) -> None:
    """Delete locally cached font, icon, and image files."""
    try:
        if images:
            clear_image_cache()
            print("Successfully cleared image cache.")
        elif all_assets:
            clear_cache()
            clear_image_cache()
            print("Successfully cleared all caches (fonts, icons, and image cache).")
        else:
            clear_cache()
            clear_image_cache(cli_only=True)
            print("Successfully cleared font, icon, and CLI image caches.")
    except Exception as e:
        _handle_cache_error("Cache Error", e)


@cache_app.command("list", epilog=HELP_EPILOG)
def cmd_cache_list() -> None:
    """List all downloadable font and icon packages and local cache status."""
    try:
        items = list_cache()
        table = Table(title="Drawlib Font & Icon Cache", header_style="bold cyan")
        table.add_column("Package", style="bold")
        table.add_column("Category")
        table.add_column("Cached", justify="center")
        table.add_column("Files", justify="right")
        table.add_column("Size (KB)", justify="right")

        total_bytes = 0
        cached_count = 0
        for item in items:
            is_cached = bool(item["cached"])
            if is_cached:
                cached_count += 1
            size_b = int(item["size_bytes"])
            total_bytes += size_b
            status_str = "[green]Yes[/green]" if is_cached else "[dim]No[/dim]"
            size_kb = f"{size_b / 1024:.1f}" if size_b > 0 else "-"
            table.add_row(
                str(item["name"]),
                str(item["category"]),
                status_str,
                str(item["file_count"]),
                size_kb,
            )

        console.print(table)
        console.print(
            f"[dim]Cached packages: {cached_count}/{len(items)} "
            f"(Total local size: {total_bytes / (1024 * 1024):.2f} MB)[/dim]"
        )
    except Exception as e:
        _handle_cache_error("Cache Error", e)


@cache_app.command("download", epilog=HELP_EPILOG)
def cmd_cache_download(
    all_assets: Annotated[
        bool,
        typer.Option("--all", help="Download all font and icon packages (default)."),
    ] = True,
    fonts: Annotated[
        bool,
        typer.Option("--fonts", help="Download font packages only."),
    ] = False,
    icons: Annotated[
        bool,
        typer.Option("--icons", help="Download icon packages only."),
    ] = False,
) -> None:
    """Pre-download font and/or icon packages from GitHub Releases."""
    try:
        download_cache(all_assets=all_assets, fonts=fonts, icons=icons)
        print("Successfully downloaded requested cache assets.")
    except Exception as e:
        _handle_cache_error("Cache Error", e)
