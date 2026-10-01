# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer commands for cache, css, serve, and show."""

from __future__ import annotations

import os
import sys
import traceback
from typing import Annotated, Literal, Optional

import typer
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from drawlib._builder.cache_manager import clear_cache, clear_image_cache, download_cache, list_cache
from drawlib._builder.doc_builder import show_code_block as show_block
from drawlib._builder.rules_builder import _normalize_topic
from drawlib._cli._help import HELP_EPILOG
from drawlib._cli._rules import cmd_rules_show
from drawlib._core.utils import dutil_settings
from drawlib._css_templates import (
    BUILTIN_HTML_CSS_PRESETS,
    BUILTIN_PDF_CSS_PRESETS,
    export_css,
    get_css,
    list_css,
)
from drawlib._http_server import serve_docs

console = Console()

_HELP_CTX = {"help_option_names": ["-h", "--help"]}

cache_app = typer.Typer(
    name="cache",
    help="Manage cached font and icon assets.",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)

css_app = typer.Typer(
    name="css",
    help="Manage built-in CSS style presets for HTML and PDF.",
    epilog=HELP_EPILOG,
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
        _handle_cmd_error("Cache Error", e)


@cache_app.command("purge", hidden=True, epilog=HELP_EPILOG)
def cmd_cache_purge() -> None:
    """Alias for `drawlib cache clear`."""
    cmd_cache_clear()


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
        _handle_cmd_error("Cache Error", e)


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
        _handle_cmd_error("Cache Error", e)


# ---------------------------------------------------------------------------
# drawlib css {list, show}
# ---------------------------------------------------------------------------
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


@css_app.command("list", epilog=HELP_EPILOG)
def cmd_css_list(
    target: Annotated[
        Optional[str],
        typer.Argument(
            help="Target document format ('html', 'pdf', or omitted for both).",
        ),
    ] = None,
) -> None:
    """List available built-in CSS presets for HTML and PDF."""
    if target is not None:
        normalized = target.strip().lower()
        if normalized not in {"html", "pdf", "all"}:
            console.print(f"[bold red]Error:[/bold red] Invalid target '{target}'. Must be 'html' or 'pdf'.")
            raise typer.Exit(code=1)
        if normalized in {"html", "pdf"}:
            _run_css_list("pdf" if normalized == "pdf" else "html")
            return

    all_preset_names = sorted(set(BUILTIN_HTML_CSS_PRESETS.keys()) | set(BUILTIN_PDF_CSS_PRESETS.keys()))
    table = Table(title="Built-in CSS Presets (HTML & PDF)", header_style="bold cyan")
    table.add_column("Preset Name", style="bold yellow")
    table.add_column("HTML", justify="center")
    table.add_column("PDF", justify="center")
    table.add_column("Description")

    for name in all_preset_names:
        in_html = name in BUILTIN_HTML_CSS_PRESETS
        in_pdf = name in BUILTIN_PDF_CSS_PRESETS
        html_str = "[green]Yes[/green]" if in_html else "[dim]No[/dim]"
        pdf_str = "[green]Yes[/green]" if in_pdf else "[dim]No[/dim]"
        desc = (
            BUILTIN_HTML_CSS_PRESETS.get(name, {}).get("description")
            or BUILTIN_PDF_CSS_PRESETS.get(name, {}).get("description", "")
        )
        table.add_row(name, html_str, pdf_str, desc)

    console.print(table)


def _resolve_css_target_and_preset(
    target_or_preset: str,
    preset: Optional[str],
) -> tuple[Literal["html", "pdf"], str]:
    """Resolve and validate target and preset name from positional CLI arguments."""
    arg1_lower = target_or_preset.strip().lower()
    if preset is None:
        if arg1_lower in {"html", "pdf"}:
            console.print(f"[bold red]Error:[/bold red] Missing preset name for target '{arg1_lower}'.")
            console.print(f"Usage: drawlib css show {arg1_lower} <PRESET> [-o OUTPUT]")
            raise typer.Exit(code=1)
        return "html", target_or_preset.strip()

    if arg1_lower not in {"html", "pdf"}:
        console.print(f"[bold red]Error:[/bold red] Invalid target '{target_or_preset}'. Must be 'html' or 'pdf'.")
        raise typer.Exit(code=1)
    return ("pdf" if arg1_lower == "pdf" else "html"), preset.strip()


def _run_css_export(
    target: Literal["html", "pdf"],
    preset: str,
    output: Optional[str],
    force: bool,
    lang: str = "en",
) -> None:
    """Export a built-in CSS preset to destination file."""
    try:
        out_abs = export_css(name=preset, output_path=output, target=target, force=force, lang=lang)
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


def _print_css_content(content: str) -> None:
    """Print CSS stylesheet content to stdout with syntax highlighting if terminal."""
    if sys.stdout.isatty():
        syntax = Syntax(content, "css", theme="monokai", line_numbers=False)
        console.print(syntax)
    else:
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()


@css_app.command("show", epilog=HELP_EPILOG)
def cmd_css_show(
    target_or_preset: Annotated[
        str,
        typer.Argument(
            metavar="[TARGET] PRESET",
            help="Target format ('html' or 'pdf') and/or preset name (e.g. 'html google' or 'google').",
        ),
    ],
    preset: Annotated[
        Optional[str],
        typer.Argument(
            help="Built-in CSS preset name (when target is specified as first argument).",
        ),
    ] = None,
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
    lang: Annotated[
        str,
        typer.Option(
            "-l",
            "--lang",
            help="Language code or alias for typography font stack (e.g. 'en', 'ja', 'zh-cn', 'th').",
        ),
    ] = "en",
) -> None:
    """Display or export a built-in CSS stylesheet preset for HTML or PDF."""
    target, preset_name = _resolve_css_target_and_preset(target_or_preset, preset)

    if output is not None:
        _run_css_export(target, preset_name, output, force, lang=lang)
        return

    try:
        content = get_css(name=preset_name, target=target, lang=lang)
        _print_css_content(content)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to load CSS preset: {e}")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# Top-level commands: serve, show
# ---------------------------------------------------------------------------
def register_top_commands(app: typer.Typer) -> None:
    """Register top-level commands (`serve`, `show`) onto the main Typer app."""

    @app.command("serve", epilog=HELP_EPILOG)
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

    @app.command("show", epilog=HELP_EPILOG)
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
            typer.Option(
                "-o",
                "--output",
                help="Save output image to file path without opening GUI viewer (headless export).",
            ),
        ] = None,
        grid: Annotated[
            bool,
            typer.Option("-g", "--grid", help="Show canvas with coordinate grid overlaid."),
        ] = False,
        styles: Annotated[
            Optional[str],
            typer.Option("-s", "--styles", help="Path to Python styles script (e.g. styles.py)."),
        ] = None,
        utils: Annotated[
            Optional[str],
            typer.Option("-u", "--utils", help="Path to Python utils script (e.g. utils.py)."),
        ] = None,
        no_cache: Annotated[
            bool,
            typer.Option("--no-cache", help="Disable reading and writing the SQLite build image cache."),
        ] = False,
    ) -> None:
        """Execute and display or export a drawlib code block from a Markdown/HTML file or Python script."""
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
                styles_path=styles,
                utils_path=utils,
                grid=grid,
                output_path=output,
                no_cache=no_cache,
            )
        except Exception as e:
            _handle_cmd_error("Show Error", e)
