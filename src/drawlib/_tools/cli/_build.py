# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer sub-application for `drawlib build {image, markdown, html, pdf}` commands."""

from __future__ import annotations

import sys
import traceback
from typing import Annotated, List, Literal, Optional

import typer
from rich.console import Console

from drawlib._core.l1_core import dutil_settings
from drawlib.tools.build.html import build_html
from drawlib.tools.build.image import build_image
from drawlib.tools.build.markdown import build_markdown
from drawlib.tools.build.pdf import build_pdf

build_app = typer.Typer(
    name="build",
    help="Compile Python scripts or Markdown/HTML documents into images, Markdown, HTML, or PDF.",
    no_args_is_help=True,
)

console = Console()


def _handle_build_error(prefix: str, exc: Exception) -> None:
    """Print formatted error message and exit with status code 1."""
    print(f"{prefix}: {exc}", file=sys.stderr)
    if dutil_settings.get_logging_mode() in {"verbose", "developer"}:
        traceback.print_exc()
    raise typer.Exit(code=1)


@build_app.command("image")
def cmd_build_image(
    inputs: Annotated[
        List[str],
        typer.Argument(help="Target Python file(s) (.py) or directory containing Python drawing code."),
    ],
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", "--output-dir", help="Output image file path or output directory path."),
    ] = None,
    format: Annotated[
        Optional[Literal["png", "webp", "jpg", "pdf"]],
        typer.Option("-f", "--format", help="Output image format override (png, webp, jpg, pdf)."),
    ] = None,
    config: Annotated[
        Optional[str],
        typer.Option("-c", "--config", help="Path to Python config/setup script (e.g. config.py)."),
    ] = None,
    grid: Annotated[
        bool,
        typer.Option("-g", "--grid", help="Save companion *_grid.<ext> images with coordinate grid overlaid."),
    ] = False,
    disable_auto_clear: Annotated[
        bool,
        typer.Option(
            "--disable-auto-clear",
            "--disable_auto_clear",
            help="Disable clearing canvas per executing drawing code files.",
        ),
    ] = False,
    enable_auto_initialize: Annotated[
        bool,
        typer.Option(
            "--enable-auto-initialize",
            "--enable_auto_initialize",
            help="Enable initializing canvas per executing drawing code files.",
        ),
    ] = False,
) -> None:
    """Execute one or more Python drawing scripts (.py) or package directories to generate images."""
    try:
        executed = build_image(
            inputs=inputs,
            output=output,
            format=format,
            config=config,
            grid=grid,
            disable_auto_clear=disable_auto_clear,
            enable_auto_initialize=enable_auto_initialize,
        )
        print(f"Successfully executed image build for {len(executed)} target(s).")
    except Exception as e:
        _handle_build_error("Build Image Error", e)


@build_app.command("markdown")
def cmd_build_markdown(
    input_path: Annotated[
        str,
        typer.Argument(metavar="INPUT", help="Input Markdown (.md) file path or directory path."),
    ],
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Output Markdown file or directory path."),
    ] = None,
    image_format: Annotated[
        Literal["png", "webp"],
        typer.Option("--image-format", help="Image output format for drawlib blocks: png or webp."),
    ] = "png",
    config: Annotated[
        Optional[str],
        typer.Option("-c", "--config", help="Path to Python config/setup script (e.g. config.py)."),
    ] = None,
) -> None:
    """Compile Markdown file or directory containing drawlib code blocks into rendered Markdown."""
    try:
        out_file = build_markdown(
            input_path=input_path,
            output=output,
            image_format=image_format,
            config=config,
        )
        print(f"Successfully compiled Markdown document(s): {out_file}")
    except Exception as e:
        _handle_build_error("Build Markdown Error", e)


@build_app.command("html")
def cmd_build_html(
    input_path: Annotated[
        str,
        typer.Argument(metavar="INPUT", help="Input Markdown (.md), HTML (.html), or directory path."),
    ],
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Output HTML file or directory path."),
    ] = None,
    image_format: Annotated[
        Literal["png", "webp"],
        typer.Option("--image-format", help="Image output format for drawlib blocks: png or webp."),
    ] = "png",
    css: Annotated[
        Optional[str],
        typer.Option("--css", help="CSS preset (default, github, minimal, monochrome) or custom .css file path."),
    ] = None,
    template: Annotated[
        Optional[str],
        typer.Option("-t", "--template", help="Template preset (sidebar, simple) or custom .html.j2 file path."),
    ] = None,
    config: Annotated[
        Optional[str],
        typer.Option("-c", "--config", help="Path to Python config/setup script (e.g. config.py)."),
    ] = None,
) -> None:
    """Compile Markdown/HTML file or directory into a static HTML page or multi-page website."""
    try:
        out_file = build_html(
            input_path=input_path,
            output=output,
            image_format=image_format,
            css=css,
            template=template,
            config=config,
        )
        print(f"Successfully compiled HTML document(s): {out_file}")
    except Exception as e:
        _handle_build_error("Build HTML Error", e)


@build_app.command("pdf")
def cmd_build_pdf(
    inputs: Annotated[
        List[str],
        typer.Argument(
            metavar="INPUTS...",
            help="One or more input Markdown (.md), HTML (.html) files, or directories to merge into PDF.",
        ),
    ],
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Output PDF file path."),
    ] = None,
    page_break: Annotated[
        bool,
        typer.Option("--page-break/--no-page-break", help="Insert CSS page breaks between merged chapters."),
    ] = True,
    toc: Annotated[
        bool,
        typer.Option("--toc/--no-toc", help="Generate a Table of Contents at the beginning of the PDF."),
    ] = False,
    title: Annotated[
        Optional[str],
        typer.Option("--title", help="Document title override for the merged PDF."),
    ] = None,
    css: Annotated[
        Optional[str],
        typer.Option("--css", help="CSS preset (default, github, minimal, monochrome) or custom .css file path."),
    ] = None,
    template: Annotated[
        Optional[str],
        typer.Option("-t", "--template", help="Template preset (simple, sidebar) or custom .html.j2 file path."),
    ] = None,
    config: Annotated[
        Optional[str],
        typer.Option("-c", "--config", help="Path to Python config/setup script (e.g. config.py)."),
    ] = None,
) -> None:
    """Merge one or more Markdown/HTML files or directories into a single HTML and export to PDF."""
    try:
        out_file = build_pdf(
            inputs=inputs,
            output=output,
            page_break=page_break,
            toc=toc,
            title=title,
            css=css,
            template=template,
            config=config,
        )
        print(f"Successfully compiled PDF document: {out_file}")
    except Exception as e:
        _handle_build_error("Build PDF Error", e)
