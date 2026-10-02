# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer sub-application for `drawlib css` commands."""

from __future__ import annotations

import sys
from typing import Annotated, Literal, Optional

import typer
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from drawlib._cli._help import HELP_EPILOG
from drawlib._css_templates import (
    BUILTIN_HTML_CSS_PRESETS,
    BUILTIN_PDF_CSS_PRESETS,
    export_css,
    get_css,
    list_css,
)

console = Console()
_HELP_CTX = {"help_option_names": ["-h", "--help"]}

css_app = typer.Typer(
    name="css",
    help="Manage built-in CSS style presets for HTML and PDF.",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)


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
