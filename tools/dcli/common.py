# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Common utilities and process runners for dcli."""

import os
import subprocess
from pathlib import Path
from typing import Mapping, Optional, Sequence

import typer
from rich.console import Console

console = Console()
err_console = Console(stderr=True)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

EXCLUDED_MODULES = frozenset({"__init__.py", "__main__.py", "common.py", "completion.py"})


def discover_toolsets() -> list[str]:
    """Scan tools/dcli directory for executable toolset modules or packages.

    Returns:
        list[str]: Sorted list of toolset module names.
    """
    dcli_dir = Path(__file__).resolve().parent
    toolsets: set[str] = set()
    for f in dcli_dir.glob("*.py"):
        if f.name not in EXCLUDED_MODULES and not f.name.startswith("_"):
            toolsets.add(f.stem)
    for d in dcli_dir.iterdir():
        if d.is_dir() and not d.name.startswith(("_", ".")) and (d / "__init__.py").exists():
            toolsets.add(d.name)
    return sorted(toolsets)


def run_command(
    args: Sequence[str],
    cwd: Optional[Path | str] = None,
    env: Optional[Mapping[str, str]] = None,
    desc: Optional[str] = None,
) -> None:
    """Execute a system process with rich logging and error tracking.

    Args:
        args: Command arguments to execute.
        cwd: Working directory (defaults to PROJECT_ROOT).
        env: Environment variables dictionary.
        desc: Optional description to display.

    Raises:
        typer.Exit: If the subprocess execution fails.
    """
    work_dir = Path(cwd) if cwd else PROJECT_ROOT
    if desc:
        console.print(f"[bold cyan]{desc}[/bold cyan]")
    console.print(f"[dim]Running:[/dim] [blue]{' '.join(args)}[/blue]")

    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    try:
        subprocess.run(args, cwd=work_dir, env=merged_env, check=True)
    except FileNotFoundError as e:
        err_console.print(f"[bold red]Error: Command '{args[0]}' not found in PATH.[/bold red]")
        raise typer.Exit(code=1) from e
    except subprocess.CalledProcessError as e:
        err_console.print(f"[bold red]Execution failed with exit code {e.returncode}.[/bold red]")
        raise typer.Exit(code=e.returncode) from e
