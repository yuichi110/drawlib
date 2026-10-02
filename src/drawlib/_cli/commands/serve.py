# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer command for `drawlib serve` local documentation server."""

from __future__ import annotations

import sys
import traceback
from typing import Annotated, Optional

import typer

from drawlib._cli._help import HELP_EPILOG
from drawlib._core.l1_core import dutil_settings
from drawlib._http_server import serve_docs


def _handle_serve_error(prefix: str, exc: Exception) -> None:
    """Print formatted error message and exit with status code 1."""
    print(f"{prefix}: {exc}", file=sys.stderr)
    if dutil_settings.get_logging_mode() in {"verbose", "developer"}:
        traceback.print_exc()
    raise typer.Exit(code=1)


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
    check: Annotated[
        bool,
        typer.Option(
            "--check",
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
            check_only=check,
        )
    except Exception as e:
        _handle_serve_error("Serve Error", e)
