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
from typing import Annotated, Literal, Optional

import typer
from rich.console import Console

from drawlib._builder.doc_builder import build_html, build_markdown, build_pdf
from drawlib._builder.image_builder import build_image
from drawlib._cli._help import HELP_EPILOG
from drawlib._core.l1_core import dutil_settings

build_app = typer.Typer(
    name="build",
    help="Compile Python scripts or Markdown/HTML documents into images, Markdown, HTML, or PDF.",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

console = Console()


def _handle_build_error(prefix: str, exc: Exception) -> None:
    """Print formatted error message and exit with status code 1."""
    print(f"{prefix}: {exc}", file=sys.stderr)
    if dutil_settings.get_logging_mode() in {"verbose", "developer"}:
        traceback.print_exc()
    raise typer.Exit(code=1)


@build_app.command("image", epilog=HELP_EPILOG)
def cmd_build_image(
    input_path: Annotated[
        str,
        typer.Argument(metavar="INPUT", help="Target Python file (.py) or directory containing Python drawing code."),
    ],
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", "--output-dir", help="Output image file path or output directory path."),
    ] = None,
    format: Annotated[
        Optional[Literal["png", "webp", "jpg", "pdf"]],
        typer.Option("-f", "--format", help="Output image format override (png, webp, jpg, pdf)."),
    ] = None,
    styles: Annotated[
        Optional[str],
        typer.Option("-s", "--styles", help="Path to Python styles script (e.g. styles.py)."),
    ] = None,
    utils: Annotated[
        Optional[str],
        typer.Option("-u", "--utils", help="Path to Python utils script (e.g. utils.py)."),
    ] = None,
    grid: Annotated[
        bool,
        typer.Option("-g", "--grid", help="Save companion *_grid.<ext> images with coordinate grid overlaid."),
    ] = False,
    disable_auto_clear: Annotated[
        bool,
        typer.Option(
            "--disable-auto-clear",
            help="Disable clearing canvas per executing drawing code files.",
        ),
    ] = False,
    enable_auto_initialize: Annotated[
        bool,
        typer.Option(
            "--enable-auto-initialize",
            help="Enable initializing canvas per executing drawing code files.",
        ),
    ] = False,
    no_cache: Annotated[
        bool,
        typer.Option("--no-cache", help="Disable reading and writing the SQLite build image cache."),
    ] = False,
) -> None:
    """Execute a Python drawing script (.py) or directory containing scripts to generate images."""
    try:
        executed = build_image(
            input_path=input_path,
            output_path=output,
            format=format,
            styles_path=styles,
            utils_path=utils,
            grid=grid,
            disable_auto_clear=disable_auto_clear,
            enable_auto_initialize=enable_auto_initialize,
            no_cache=no_cache,
        )
        print(f"Successfully executed image build for {len(executed)} target(s).")
    except Exception as e:
        _handle_build_error("Build Image Error", e)


@build_app.command("markdown", epilog=HELP_EPILOG)
def cmd_build_markdown(
    input_dir: Annotated[
        str,
        typer.Argument(metavar="DIR", help="Directory containing Markdown (.md) source files."),
    ],
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Output Markdown directory path."),
    ] = None,
    format: Annotated[
        Literal["png", "webp"],
        typer.Option("-f", "--format", help="Image output format for drawlib blocks: png or webp."),
    ] = "png",
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
    """Compile a directory containing Markdown files with drawlib code blocks into rendered Markdown."""
    try:
        out_file = build_markdown(
            input_dir=input_dir,
            output_dir=output,
            image_format=format,
            styles_path=styles,
            utils_path=utils,
            no_cache=no_cache,
        )
        print(f"Successfully compiled Markdown document(s): {out_file}")
    except Exception as e:
        _handle_build_error("Build Markdown Error", e)


@build_app.command("html", epilog=HELP_EPILOG)
def cmd_build_html(
    input_dir: Annotated[
        str,
        typer.Argument(metavar="DIR", help="Directory containing documentation source files."),
    ],
    output: Annotated[
        Optional[str],
        typer.Option("-o", "--output", help="Output HTML directory path."),
    ] = None,
    format: Annotated[
        Literal["png", "webp"],
        typer.Option("-f", "--format", help="Image output format for drawlib blocks: png or webp."),
    ] = "png",
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
    """Compile a Markdown/HTML documentation directory into a static HTML site."""
    try:
        out_file = build_html(
            input_dir=input_dir,
            output_dir=output,
            image_format=format,
            styles_path=styles,
            utils_path=utils,
            no_cache=no_cache,
        )
        print(f"Successfully compiled HTML document(s): {out_file}")
    except Exception as e:
        _handle_build_error("Build HTML Error", e)


@build_app.command("pdf", epilog=HELP_EPILOG)
def cmd_build_pdf(
    input_dir: Annotated[
        str,
        typer.Argument(
            metavar="DIR",
            help="Directory containing Markdown chapters to export to PDF.",
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
    generate_index: Annotated[
        bool,
        typer.Option(
            "--generate-index/--no-generate-index",
            "--toc/--no-toc",
            help="Generate an index (Table of Contents) and insert it between the 1st and 2nd documents.",
        ),
    ] = False,
    title: Annotated[
        Optional[str],
        typer.Option("--title", help="Document title override for the merged PDF."),
    ] = None,
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
    timestamp: Annotated[
        bool,
        typer.Option(
            "--timestamp",
            help="Include current build timestamp in PDF metadata instead of normalizing it.",
        ),
    ] = False,
) -> None:
    """Merge Markdown chapters in a directory into a single HTML and export to PDF."""
    try:
        out_file = build_pdf(
            input_dir=input_dir,
            output_file=output,
            page_break=page_break,
            generate_index=generate_index,
            title=title,
            styles_path=styles,
            utils_path=utils,
            no_cache=no_cache,
            timestamp=timestamp,
        )
        print(f"Successfully compiled PDF document: {out_file}")
    except Exception as e:
        _handle_build_error("Build PDF Error", e)
