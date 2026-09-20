# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib Development CLI (dcli) Master Launcher.

Acts as the entry point when dcli is executed without specifying a toolset.
Discovers available toolset modules in tools/dcli and renders a formatted summary.
"""

from __future__ import annotations

import contextlib
import importlib
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(help="Drawlib Development CLI Launcher")

EXCLUDED_MODULES = frozenset({"__init__.py", "__main__.py", "common.py", "completion.py"})


def discover_toolsets() -> list[str]:
    """Scan tools/dcli directory for executable toolset modules.

    Returns:
        list[str]: Sorted list of toolset module names.
    """
    dcli_dir = Path(__file__).resolve().parent
    toolsets = []
    for f in dcli_dir.glob("*.py"):
        if f.name not in EXCLUDED_MODULES and not f.name.startswith("_"):
            toolsets.append(f.stem)
    return sorted(toolsets)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,  # noqa: ARG001
    invalid_toolset: Optional[str] = typer.Option(
        None,
        "--invalid-toolset",
        hidden=True,
        help="Internal option to display formatted error for invalid toolset names.",
    ),
) -> None:
    """Drawlib CLI Master Launcher.

    Args:
        ctx: Typer context object.
        invalid_toolset: Optional invalid toolset name provided via internal delegation.

    Raises:
        typer.Exit: Exits with code 1 if invalid_toolset is set.
    """
    console = Console()

    if invalid_toolset:
        console.print()
        console.print(
            Panel(
                f"[red]Toolset [bold]{invalid_toolset}[/bold] is not a valid toolset under 'tools/dcli/'.[/red]\n\n"
                f"Run [bold]./dcli[/bold] without arguments to view all active toolsets.",
                title="Error: Invalid Toolset",
                border_style="red",
                expand=False,
            )
        )
        console.print()
        raise typer.Exit(code=1)

    available_toolsets = discover_toolsets()

    console.print()
    console.print("[bold cyan]Drawlib Development CLI (dcli)[/bold cyan]")
    console.print("[dim]Usage: ./dcli <toolset> [command] [options][/dim]")
    console.print()

    table = Table(title="Available Toolsets", title_style="bold green", show_header=True, header_style="bold blue")
    table.add_column("Toolset", style="bold yellow", width=16)
    table.add_column("Description", style="white")

    for toolset in available_toolsets:
        desc = "No description available."
        with contextlib.suppress(Exception):
            mod = importlib.import_module(f"tools.dcli.{toolset}")
            if mod.__doc__:
                lines = [line.strip() for line in mod.__doc__.splitlines() if line.strip()]
                if lines:
                    desc = lines[0]
        table.add_row(toolset, desc)

    console.print(table)
    console.print()
    console.print("[dim]Example: ./dcli check all[/dim]")
    console.print("[dim]         ./dcli test cli[/dim]")
    console.print("[dim]         ./dcli docs build[/dim]")
    console.print()


if __name__ == "__main__":
    app()
