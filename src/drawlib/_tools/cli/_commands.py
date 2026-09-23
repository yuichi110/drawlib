# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer commands for cache, template, css, serve, show, and export."""

from __future__ import annotations

import sys
import traceback
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from drawlib._core.l1_core import dutil_settings
from drawlib.tools.cache import clear_cache, download_cache, list_cache
from drawlib.tools.css import export_css, list_css
from drawlib.tools.export import export_block
from drawlib.tools.serve import serve_docs
from drawlib.tools.show import show_block
from drawlib.tools.template import export_template, list_templates, validate_template

console = Console()

cache_app = typer.Typer(
    name="cache",
    help="Manage cached font and icon assets.",
    no_args_is_help=True,
)

template_app = typer.Typer(
    name="template",
    help="List, export, or validate Jinja2 HTML templates.",
    no_args_is_help=True,
)

css_app = typer.Typer(
    name="css",
    help="List or export built-in CSS style presets.",
    no_args_is_help=True,
)


def _handle_cmd_error(prefix: str, exc: Exception) -> None:
    """Print formatted error message and exit with status code 1."""
    print(f"{prefix}: {exc}", file=sys.stderr)
    if dutil_settings.get_logging_mode() in {"verbose", "developer"}:
        traceback.print_exc()
    raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# drawlib cache {clear, list, download}
# ---------------------------------------------------------------------------
@cache_app.command("clear")
def cmd_cache_clear() -> None:
    """Delete all locally cached font and icon files."""
    try:
        clear_cache()
        print("Successfully cleared font and icon cache.")
    except Exception as e:
        _handle_cmd_error("Cache Error", e)


@cache_app.command("purge", hidden=True)
def cmd_cache_purge() -> None:
    """Alias for `drawlib cache clear`."""
    cmd_cache_clear()


@cache_app.command("list")
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
        _handle_cmd_error("Cache Error", e)


@cache_app.command("download")
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
        _handle_cmd_error("Cache Error", e)


# ---------------------------------------------------------------------------
# drawlib template {list, export, validate}
# ---------------------------------------------------------------------------
@template_app.command("list")
def cmd_template_list() -> None:
    """List available built-in Jinja2 HTML templates."""
    items = list_templates()
    table = Table(title="Built-in HTML Templates", header_style="bold cyan")
    table.add_column("Preset Name", style="bold yellow")
    table.add_column("Template File")
    table.add_column("Description")
    for item in items:
        table.add_row(item["name"], item["file"], item["description"])
    console.print(table)


@template_app.command("export")
def cmd_template_export(
    name_or_output: Annotated[
        Optional[str],
        typer.Argument(
            help="Built-in template preset ('sidebar', 'simple') or output file path (default: 'sidebar')."
        ),
    ] = None,
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Destination file path (default: template.html.j2)."),
    ] = None,
    name: Annotated[
        Optional[str],
        typer.Option("-n", "--name", help="Built-in template preset name ('sidebar' or 'simple')."),
    ] = None,
) -> None:
    """Export a built-in HTML template ('sidebar' or 'simple') to a local file."""
    try:
        preset_names = {t["name"] for t in list_templates()} | {"standalone"}
        if name is not None:
            preset = name
            dest = output or name_or_output or "template.html.j2"
        elif name_or_output is None:
            preset = "sidebar"
            dest = output or "template.html.j2"
        elif name_or_output in preset_names:
            preset = name_or_output
            dest = output or "template.html.j2"
        else:
            preset = "sidebar"
            dest = output or name_or_output

        out_file = export_template(name=preset, output=dest)
        print(f"Successfully exported template '{preset}' to: {out_file}")
    except Exception as e:
        _handle_cmd_error("Template Error", e)


@template_app.command("validate")
def cmd_template_validate(
    template_file: Annotated[
        str,
        typer.Argument(help="Path to Jinja2 HTML template file to validate."),
    ],
) -> None:
    """Validate a Jinja2 template file for syntax and required placeholders."""
    try:
        is_valid, msgs = validate_template(template_file)
        for msg in msgs:
            print(msg)
        if not is_valid:
            raise typer.Exit(code=1)
    except typer.Exit:
        raise
    except Exception as e:
        _handle_cmd_error("Template Error", e)


# ---------------------------------------------------------------------------
# drawlib css {list, export}
# ---------------------------------------------------------------------------
@css_app.command("list")
def cmd_css_list() -> None:
    """List available built-in CSS style presets."""
    items = list_css()
    table = Table(title="Built-in CSS Presets", header_style="bold cyan")
    table.add_column("Preset Name", style="bold yellow")
    table.add_column("CSS File")
    table.add_column("Description")
    for item in items:
        table.add_row(item["name"], item["file"], item["description"])
    console.print(table)


@css_app.command("export")
def cmd_css_export(
    name_or_output: Annotated[
        Optional[str],
        typer.Argument(
            help="Built-in CSS preset ('default', 'github', 'minimal', 'monochrome') or output file path."
        ),
    ] = None,
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Destination CSS file path (default: style.css)."),
    ] = None,
    name: Annotated[
        Optional[str],
        typer.Option("-n", "--name", help="Built-in CSS preset name ('default', 'github', 'minimal', 'monochrome')."),
    ] = None,
) -> None:
    """Export a built-in CSS preset to a local file for customization."""
    try:
        preset_names = {c["name"] for c in list_css()}
        if name is not None:
            preset = name
            dest = output or name_or_output or "style.css"
        elif name_or_output is None:
            preset = "default"
            dest = output or "style.css"
        elif name_or_output in preset_names:
            preset = name_or_output
            dest = output or "style.css"
        else:
            preset = "default"
            dest = output or name_or_output

        out_file = export_css(name=preset, output=dest)
        print(f"Successfully exported CSS preset '{preset}' to: {out_file}")
    except Exception as e:
        _handle_cmd_error("CSS Error", e)


# ---------------------------------------------------------------------------
# Top-level commands: serve, show, export
# ---------------------------------------------------------------------------
def register_top_commands(app: typer.Typer) -> None:
    """Register top-level commands (`serve`, `show`, `export`) onto the main Typer app."""

    @app.command("serve")
    def cmd_serve(
        directory: Annotated[
            Optional[str],
            typer.Argument(help="Directory to serve (default: auto-detect docs_html, docs, or current directory)."),
        ] = None,
        port: Annotated[
            int,
            typer.Option("-p", "--port", help="Port to run the HTTP server on."),
        ] = 8000,
        no_browser: Annotated[
            bool,
            typer.Option("--no-browser", help="Do not open browser automatically."),
        ] = False,
        skip_check: Annotated[
            bool,
            typer.Option("--skip-check", help="Skip pre-scan for broken links and assets before starting server."),
        ] = False,
        check_only: Annotated[
            bool,
            typer.Option(
                "--check",
                "--check-only",
                help="Check for broken links/assets in target directory and exit without starting server.",
            ),
        ] = False,
    ) -> None:
        """Start a local HTTP server to preview built HTML documentation."""
        try:
            serve_docs(
                directory=directory,
                port=port,
                open_browser=not no_browser,
                skip_check=skip_check,
                check_only=check_only,
            )
        except Exception as e:
            _handle_cmd_error("Serve Error", e)

    @app.command("show")
    def cmd_show(
        file: Annotated[
            str,
            typer.Argument(help="Target Markdown (.md), HTML (.html), or Python script (.py) path."),
        ],
        target: Annotated[
            Optional[str],
            typer.Argument(help="1-based block index (e.g. 1) or target image filename (e.g. arch.png)."),
        ] = None,
        output: Annotated[
            Optional[str],
            typer.Option("-o", "--output", help="Save output image to file path without opening GUI viewer."),
        ] = None,
        grid: Annotated[
            bool,
            typer.Option("-g", "--grid", help="Show canvas with coordinate grid overlaid."),
        ] = False,
        config: Annotated[
            Optional[str],
            typer.Option("-c", "--config", help="Path to Python config/setup script (e.g. config.py)."),
        ] = None,
    ) -> None:
        """Execute and display a drawlib code block from a Markdown/HTML file or Python script."""
        try:
            show_block(
                file_path=file,
                target=target,
                config_path=config,
                grid=grid,
                output_path=output,
            )
        except Exception as e:
            _handle_cmd_error("Show Error", e)

    @app.command("export")
    def cmd_export(
        file: Annotated[
            str,
            typer.Argument(help="Target Markdown (.md), HTML (.html), or Python script (.py) path."),
        ],
        target: Annotated[
            Optional[str],
            typer.Argument(help="1-based block index (e.g. 1) or target image filename (e.g. arch.png)."),
        ] = None,
        output: Annotated[
            Optional[str],
            typer.Option("-o", "--output", help="Output image file or directory path."),
        ] = None,
        config: Annotated[
            Optional[str],
            typer.Option("-c", "--config", help="Path to Python config/setup script (e.g. config.py)."),
        ] = None,
        grid: Annotated[
            bool,
            typer.Option("-g", "--grid", help="Export canvas with coordinate grid overlaid."),
        ] = False,
    ) -> None:
        """Execute and export a drawlib code block or Python script to an image file."""
        try:
            export_block(
                file_path=file,
                target=target,
                output_path=output,
                config_path=config,
                grid=grid,
            )
        except Exception as e:
            _handle_cmd_error("Export Error", e)
