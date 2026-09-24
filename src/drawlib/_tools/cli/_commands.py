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
from typing import Annotated, Literal, Optional

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

_HELP_CTX = {"help_option_names": ["-h", "--help"]}

cache_app = typer.Typer(
    name="cache",
    help="Manage cached font and icon assets.",
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)

template_app = typer.Typer(
    name="template",
    help="Manage built-in Jinja2 templates for HTML and PDF.",
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
# drawlib template {html, pdf, list, export, validate}
# ---------------------------------------------------------------------------
template_html_app = typer.Typer(
    name="html",
    help="List, export, or validate built-in HTML templates (html_templates).",
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)
template_pdf_app = typer.Typer(
    name="pdf",
    help="List, export, or validate built-in PDF templates (pdf_templates).",
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)
template_app.add_typer(template_html_app, name="html")
template_app.add_typer(template_pdf_app, name="pdf")


def _run_template_list(target: Literal["html", "pdf"]) -> None:
    items = list_templates(target=target)
    title = f"Built-in {target.upper()} Templates ({target}_templates)"
    table = Table(title=title, header_style="bold cyan")
    table.add_column("Preset Name", style="bold yellow")
    table.add_column("Template File")
    table.add_column("Description")
    for item in items:
        table.add_row(item["name"], item["file"], item["description"])
    console.print(table)


def _run_template_export(
    target: Literal["html", "pdf"],
    name_or_output: Optional[str],
    output: Optional[str],
    name: Optional[str],
) -> None:
    try:
        default_preset = "default" if target == "pdf" else "sidebar"
        default_dest = "pdf_template.html.j2" if target == "pdf" else "template.html.j2"
        preset_names = {t["name"] for t in list_templates(target=target)} | {"standalone", "simple"}
        if name is not None:
            preset = name
            dest = output or name_or_output or default_dest
        elif name_or_output is None:
            preset = default_preset
            dest = output or default_dest
        elif name_or_output in preset_names:
            preset = name_or_output
            dest = output or default_dest
        else:
            preset = default_preset
            dest = output or name_or_output

        out_file = export_template(name=preset, output=dest, target=target)
        print(f"Successfully exported {target.upper()} template '{preset}' to: {out_file}")
    except Exception as e:
        _handle_cmd_error("Template Error", e)


def _run_template_validate(target: Literal["html", "pdf"], template_file: str) -> None:
    try:
        is_valid, msgs = validate_template(template_file, target=target)
        for msg in msgs:
            print(msg)
        if not is_valid:
            raise typer.Exit(code=1)
    except typer.Exit:
        raise
    except Exception as e:
        _handle_cmd_error("Template Error", e)


@template_html_app.command("list")
def cmd_template_html_list() -> None:
    """List available built-in HTML templates (sidebar, simple)."""
    _run_template_list("html")


@template_html_app.command("export")
def cmd_template_html_export(
    name_or_output: Annotated[
        Optional[str],
        typer.Argument(help="HTML template preset ('sidebar', 'simple') or output file path."),
    ] = None,
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Destination file path (default: template.html.j2)."),
    ] = None,
    name: Annotated[
        Optional[str],
        typer.Option("-n", "--name", help="HTML template preset name ('sidebar' or 'simple')."),
    ] = None,
) -> None:
    """Export a built-in HTML template ('sidebar' or 'simple') to a local file."""
    _run_template_export("html", name_or_output, output, name)


@template_html_app.command("validate")
def cmd_template_html_validate(
    template_file: Annotated[str, typer.Argument(help="Path to Jinja2 HTML template file to validate.")],
) -> None:
    """Validate a custom Jinja2 HTML template file."""
    _run_template_validate("html", template_file)


@template_pdf_app.command("list")
def cmd_template_pdf_list() -> None:
    """List available built-in PDF templates (default, book)."""
    _run_template_list("pdf")


@template_pdf_app.command("export")
def cmd_template_pdf_export(
    name_or_output: Annotated[
        Optional[str],
        typer.Argument(help="PDF template preset ('default', 'book') or output file path."),
    ] = None,
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Destination file path (default: pdf_template.html.j2)."),
    ] = None,
    name: Annotated[
        Optional[str],
        typer.Option("-n", "--name", help="PDF template preset name ('default' or 'book')."),
    ] = None,
) -> None:
    """Export a built-in PDF template ('default' or 'book') to a local file."""
    _run_template_export("pdf", name_or_output, output, name)


@template_pdf_app.command("validate")
def cmd_template_pdf_validate(
    template_file: Annotated[str, typer.Argument(help="Path to Jinja2 PDF template file to validate.")],
) -> None:
    """Validate a custom Jinja2 PDF template file."""
    _run_template_validate("pdf", template_file)


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


def _run_css_export(
    target: Literal["html", "pdf"],
    name_or_output: Optional[str],
    output: Optional[str],
    name: Optional[str],
) -> None:
    try:
        default_dest = "pdf_style.css" if target == "pdf" else "style.css"
        preset_names = {c["name"] for c in list_css(target=target)}
        if name is not None:
            preset = name
            dest = output or name_or_output or default_dest
        elif name_or_output is None:
            preset = "default"
            dest = output or default_dest
        elif name_or_output in preset_names:
            preset = name_or_output
            dest = output or default_dest
        else:
            preset = "default"
            dest = output or name_or_output

        out_file = export_css(name=preset, output=dest, target=target)
        print(f"Successfully exported {target.upper()} CSS preset '{preset}' to: {out_file}")
    except Exception as e:
        _handle_cmd_error("CSS Error", e)


@css_html_app.command("list")
def cmd_css_html_list() -> None:
    """List available built-in HTML CSS presets (default, google, google-dark, google-auto, etc.)."""
    _run_css_list("html")


@css_html_app.command("export")
def cmd_css_html_export(
    name_or_output: Annotated[
        Optional[str],
        typer.Argument(
            help="HTML CSS preset ('default', 'google', 'google-dark', 'google-auto', 'github', ...) or output path."
        ),
    ] = None,
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Destination CSS file path (default: style.css)."),
    ] = None,
    name: Annotated[
        Optional[str],
        typer.Option("-n", "--name", help="HTML CSS preset name."),
    ] = None,
) -> None:
    """Export a built-in HTML CSS preset to a local file."""
    _run_css_export("html", name_or_output, output, name)


@css_pdf_app.command("list")
def cmd_css_pdf_list() -> None:
    """List available built-in PDF CSS presets (default, google, github, minimal, monochrome)."""
    _run_css_list("pdf")


@css_pdf_app.command("export")
def cmd_css_pdf_export(
    name_or_output: Annotated[
        Optional[str],
        typer.Argument(help="PDF CSS preset ('default', 'google', 'github', 'minimal', 'monochrome') or output path."),
    ] = None,
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Destination CSS file path (default: pdf_style.css)."),
    ] = None,
    name: Annotated[
        Optional[str],
        typer.Option("-n", "--name", help="PDF CSS preset name."),
    ] = None,
) -> None:
    """Export a built-in PDF CSS preset to a local file."""
    _run_css_export("pdf", name_or_output, output, name)


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
