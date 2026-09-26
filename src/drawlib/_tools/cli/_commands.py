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

import os
import sys
import traceback
from typing import Annotated, Literal, Optional

import typer
from rich.console import Console
from rich.table import Table

from drawlib._core.l1_core import dutil_settings
from drawlib._tools.cli._rules import cmd_rules_show
from drawlib._tools.rules_builder import _normalize_topic
from drawlib.tools.cache import clear_cache, download_cache, list_cache
from drawlib.tools.css import export_css, list_css
from drawlib.tools.export import export_block
from drawlib.tools.serve import serve_docs
from drawlib.tools.show import show_block

console = Console()

_HELP_CTX = {"help_option_names": ["-h", "--help"]}

cache_app = typer.Typer(
    name="cache",
    help="Manage cached font and icon assets.",
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)

css_app = typer.Typer(
    name="css",
    help="Manage built-in CSS style presets for HTML and PDF.",
    no_args_is_help=True,
    context_settings=_HELP_CTX,
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
# drawlib css {html, pdf}
# ---------------------------------------------------------------------------
css_html_app = typer.Typer(
    name="html",
    help="List or export built-in HTML CSS presets (html_css).",
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)
css_pdf_app = typer.Typer(
    name="pdf",
    help="List or export built-in PDF CSS presets (pdf_css).",
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)
css_app.add_typer(css_html_app, name="html")
css_app.add_typer(css_pdf_app, name="pdf")


def _run_css_list(target: Literal["html", "pdf"]) -> None:
    items = list_css(target=target)
    title = f"Built-in {target.upper()} CSS Presets ({target}_css)"
    table = Table(title=title, header_style="bold cyan")
    table.add_column("Preset Name", style="bold yellow")
    table.add_column("CSS File")
    table.add_column("Description")
    for item in items:
        table.add_row(item["name"], item["file"], item["description"])
    console.print(table)


@css_html_app.command("list")
def cmd_css_html_list() -> None:
    """List available built-in HTML CSS presets (default, google, google-dark, google-auto, etc.)."""
    _run_css_list("html")


@css_pdf_app.command("list")
def cmd_css_pdf_list() -> None:
    """List available built-in PDF CSS presets (default, google, default-dark, google-dark, etc.)."""
    _run_css_list("pdf")


def _run_css_export(
    target: Literal["html", "pdf"],
    preset: str,
    output: Optional[str],
    force: bool,
) -> None:
    try:
        out_abs = export_css(name=preset, output_path=output, target=target, force=force)
        console.print(
            f"[bold green]Success:[/bold green] Exported {target.upper()} CSS preset "
            f"[bold yellow]'{preset}'[/bold yellow] to [bold cyan]'{out_abs}'[/bold cyan]."
        )
    except (FileExistsError, ValueError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to export CSS preset: {e}")
        raise typer.Exit(code=1)


@css_html_app.command("export")
def cmd_css_html_export(
    preset: Annotated[
        str,
        typer.Argument(
            help="Built-in HTML CSS preset name (e.g., 'google', 'default-dark', 'github').",
        ),
    ],
    output: Annotated[
        Optional[str],
        typer.Option(
            "-o",
            "--output",
            help="Destination CSS file path (default: docs_src/style.css if present, else style.css).",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help="Overwrite destination file if it already exists.",
        ),
    ] = False,
) -> None:
    """Export a built-in HTML CSS preset to a local stylesheet file."""
    _run_css_export("html", preset, output, force)


@css_pdf_app.command("export")
def cmd_css_pdf_export(
    preset: Annotated[
        str,
        typer.Argument(
            help="Built-in PDF CSS preset name (e.g., 'google', 'default-dark', 'github').",
        ),
    ],
    output: Annotated[
        Optional[str],
        typer.Option(
            "-o",
            "--output",
            help="Destination CSS file path (default: docs_src/style.css if present, else style.css).",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help="Overwrite destination file if it already exists.",
        ),
    ] = False,
) -> None:
    """Export a built-in PDF CSS preset to a local stylesheet file."""
    _run_css_export("pdf", preset, output, force)


@css_app.command("export")
def cmd_css_export(
    preset: Annotated[
        str,
        typer.Argument(
            help="Built-in CSS preset name (e.g., 'google', 'default-dark', 'github').",
        ),
    ],
    output: Annotated[
        Optional[str],
        typer.Option(
            "-o",
            "--output",
            help="Destination CSS file path (default: docs_src/style.css if present, else style.css).",
        ),
    ] = None,
    target: Annotated[
        str,
        typer.Option(
            "-t",
            "--target",
            help="Target document format ('html' or 'pdf'). Defaults to 'html'.",
        ),
    ] = "html",
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help="Overwrite destination file if it already exists.",
        ),
    ] = False,
) -> None:
    """Export a built-in CSS preset for HTML or PDF."""
    normalized_target = target.strip().lower()
    if normalized_target == "pdf":
        _run_css_export("pdf", preset, output, force)
    elif normalized_target == "html":
        _run_css_export("html", preset, output, force)
    else:
        console.print(f"[bold red]Error:[/bold red] Invalid target '{target}'. Must be 'html' or 'pdf'.")
        raise typer.Exit(code=1)


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
        # If file is not a regular file on disk, check if it matches a rules topic name
        if not os.path.isfile(file):
            try:
                canonical = _normalize_topic(file)
                cmd_rules_show(topic=canonical)
                return
            except ValueError:
                pass

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
