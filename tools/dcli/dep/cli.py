# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Project dependency inspection and release tracking toolset."""

from __future__ import annotations

import json
from typing import Optional

import typer

from tools.dcli.common import console, err_console
from tools.dcli.dep.inspector import get_dependencies, get_releases

app = typer.Typer(
    name="dep",
    help="Inspect project dependencies and PyPI release history.",
    no_args_is_help=True,
)


@app.callback()
def callback() -> None:
    """Dependency toolset callback."""


@app.command("list")
def list_dependencies() -> None:
    """List all project dependencies defined in pyproject.toml."""
    dependencies = get_dependencies()
    for dep in dependencies:
        console.print(dep.name)


@app.command("releases")
def list_releases(
    package: str = typer.Argument(..., help="Package name to inspect on PyPI."),
    year_from: Optional[int] = typer.Option(None, "--from", help="Filter releases starting from this year."),
    year_to: Optional[int] = typer.Option(None, "--to", help="Filter releases up to this year."),
    output_format: str = typer.Option("text", "--format", help="Output format: 'text' or 'json'."),
) -> None:
    """List released versions for a specific package from PyPI.

    Args:
        package: Name of the PyPI package.
        year_from: Filter releases starting from this year.
        year_to: Filter releases up to this year.
        output_format: Output format ('text' or 'json').
    """
    try:
        releases = get_releases(package, year_from=year_from, year_to=year_to)
    except Exception as e:
        err_console.print(f"[bold red]{e}[/bold red]")
        raise typer.Exit(code=1) from e

    if output_format == "json":
        data = [{"version": r.version, "timestamps": r.timestamps.isoformat()} for r in releases]
        console.print(json.dumps(data, indent=2))
    else:
        for r in releases:
            console.print(r.version)


if __name__ == "__main__":
    app()
