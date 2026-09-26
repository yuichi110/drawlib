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
from drawlib._core.utils import dutil_settings, logger
from drawlib._tools.cli._build import build_app
from drawlib._tools.cli._commands import cache_app, css_app, register_top_commands
from drawlib._tools.cli._init import cmd_init
from drawlib._tools.cli._rules import rules_app
from drawlib._tools.rules_builder import build_rule, is_rule_cached

app = typer.Typer(
    name="drawlib",
    help="Python drawing library. Illustration as Code.",
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

app.add_typer(build_app, name="build")
app.add_typer(cache_app, name="cache")
app.add_typer(css_app, name="css")
app.add_typer(rules_app, name="rules")
app.command(
    "init",
    help="Scaffold a starter drawlib project with sample illustrations and build script.",
)(cmd_init)
register_top_commands(app)


def _version_callback(value: bool) -> None:
    """Display drawlib version and exit."""
    if value:
        typer.echo(drawlib.LIB_VERSION)
        raise typer.Exit(code=0)


def _ensure_overview_rules_cached() -> None:
    """Ensure that the overview rule document and companion illustrations are built and cached.

    Because overview rules are often exported to project configuration files (e.g. .cursorrules,
    CLAUDE.md) during initial setup, AI agents may never explicitly invoke `drawlib rules show overview`.
    Pre-building the overview cache on any drawlib CLI invocation guarantees that relative illustration
    image assets exist when an agent references them via multimodal viewing tools.
    """
    try:
        if not is_rule_cached("overview"):
            build_rule("overview", quiet=True)
    except Exception as exc:
        logger.debug("Failed to ensure overview rules cache: %s", exc)


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
    """Configure global logging options for drawlib CLI and ensure overview rules are cached."""
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

    _ensure_overview_rules_cached()


def call_command() -> None:
    """Execute the drawlib Typer CLI application."""
    app()
