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

from typing import Optional

import typer

from tools.dcli.common import console, run_command

app = typer.Typer(
    name="dep",
    help="Inspect project dependencies and PyPI release history.",
    no_args_is_help=True,
)


@app.command("list")
def list_dependencies() -> None:
    """List all project dependencies defined in pyproject.toml."""
    run_command(
        ["uv", "run", "python", "tools/scripts/dependency_tool.py", "list"],
        desc="Listing dependencies from pyproject.toml...",
    )


@app.command("releases")
def list_releases(
    package: str = typer.Argument(..., help="Package name to inspect on PyPI."),
    year_from: Optional[int] = typer.Option(None, "--from", help="Filter releases starting from this year."),
    output_format: str = typer.Option("text", "--format", help="Output format: 'text' or 'json'."),
) -> None:
    """List released versions for a specific package from PyPI.

    Args:
        package: Name of the PyPI package.
        year_from: Filter releases starting from this year.
        output_format: Output format ('text' or 'json').
    """
    cmd = ["uv", "run", "python", "tools/scripts/dependency_tool.py", "releases", package]
    if year_from is not None:
        cmd.extend(["--from", str(year_from)])
    if output_format != "text":
        cmd.extend(["--format", output_format])

    run_command(cmd, desc=f"Querying releases for '{package}'...")


if __name__ == "__main__":
    app()
