# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer command for `drawlib show` block execution and export."""

from __future__ import annotations

import os
import sys
import traceback
from typing import Annotated, Optional

import typer

from drawlib._builder.doc_builder import show_code_block
from drawlib._builder.rules_builder import _normalize_topic
from drawlib._cli.commands.rules import cmd_rules_show
from drawlib._core.l1_core import dutil_settings


def _handle_show_error(prefix: str, exc: Exception) -> None:
    """Print formatted error message and exit with status code 1."""
    print(f"{prefix}: {exc}", file=sys.stderr)
    if dutil_settings.get_logging_mode() in {"verbose", "developer"}:
        traceback.print_exc()
    raise typer.Exit(code=1)


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
        show_code_block(
            file_path=file,
            target=target,
            styles_path=styles,
            utils_path=utils,
            grid=grid,
            output_path=output,
            no_cache=no_cache,
        )
    except Exception as e:
        _handle_show_error("Show Error", e)
