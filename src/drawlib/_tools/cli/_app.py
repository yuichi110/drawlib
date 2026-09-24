# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Main Typer application for drawlib CLI."""

from __future__ import annotations

from typing import Annotated

import typer

import drawlib
from drawlib._core.l1_core import dutil_settings, logger
from drawlib._tools.cli._build import build_app
from drawlib._tools.cli._commands import cache_app, css_app, register_top_commands, template_app
from drawlib._tools.cli._rules import rules_app

app = typer.Typer(
    name="drawlib",
    help="Python drawing library. Illustration as Code.",
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

app.add_typer(build_app, name="build")
app.add_typer(cache_app, name="cache")
app.add_typer(template_app, name="template")
app.add_typer(css_app, name="css")
app.add_typer(rules_app, name="rules")
register_top_commands(app)


def _version_callback(value: bool) -> None:
    """Display drawlib version and exit."""
    if value:
        logger.critical(f"software={drawlib.LIB_VERSION}")
        logger.critical(f"api={drawlib.LIB_VERSION}")
        raise typer.Exit(code=0)


@app.callback()
def main_callback(
    version: Annotated[
        bool,
        typer.Option(
            "-v",
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Show drawlib version and exit.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option("--quiet", help="Enable quiet logging (show only error messages)."),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Enable verbose logging."),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", help="Enable verbose logging (equivalent to --verbose)."),
    ] = False,
    developer: Annotated[
        bool,
        typer.Option("--developer", help="Enable verbose logging and disable user-facing error suppression."),
    ] = False,
) -> None:
    """Configure global logging options for drawlib CLI."""
    _ = version
    if quiet and (verbose or debug or developer):
        raise typer.BadParameter("Option --quiet cannot be combined with --verbose, --debug, or --developer.")

    if quiet:
        dutil_settings.set_logging_mode("quiet")
    elif developer:
        dutil_settings.set_logging_mode("developer")
    elif verbose or debug:
        dutil_settings.set_logging_mode("verbose")
    else:
        dutil_settings.set_logging_mode("normal")


def call_command() -> None:
    """Execute the drawlib Typer CLI application."""
    app()
