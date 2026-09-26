# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code quality and static analysis toolset (Ruff, Ty, docstrings)."""

from __future__ import annotations

import typer

from tools.dcli.common import console, run_command

app = typer.Typer(
    name="check",
    help="Perform linting, static type checking, docstring validation, and line counts.",
    no_args_is_help=True,
)


@app.command("lint")
def lint(
    fix: bool = typer.Option(False, "--fix", "-f", help="Automatically fix fixable lint issues."),
) -> None:
    """Run Ruff linter and formatter across project targets.

    Args:
        fix: If True, automatically fix fixable lint issues.
    """
    targets = ["src", "tests", "tools"]
    for target in targets:
        cmd = ["uv", "run", "ruff", "check", "--preview"]
        if fix:
            cmd.append("--fix")
        cmd.append(target)
        run_command(cmd, desc=f"Running Ruff on {target}...")
    console.print("[bold green]✓ All lint checks passed![/bold green]")


@app.command("type")
def type_check() -> None:
    """Run Ty static type checker across project targets."""
    targets = ["src/drawlib", "tests", "tools"]
    for target in targets:
        run_command(
            ["uv", "run", "ty", "check", target],
            env={"PYTHONPATH": "tools/scripts"},
            desc=f"Running Ty type checker on {target}...",
        )
    console.print("[bold green]✓ All type checks passed![/bold green]")


@app.command("docstring")
def docstring() -> None:
    """Validate that forbidden type aliases do not appear in @validate_call function docstrings."""
    run_command(
        ["uv", "run", "python", "tools/scripts/check_docstring.py"],
        desc="Checking @validate_call function docstring type annotations...",
    )
    console.print("[bold green]✓ Docstring checks passed![/bold green]")


@app.command("lines")
def count_lines() -> None:
    """Count source code lines in the project."""
    run_command(["uv", "run", "python", "tools/scripts/count_lines.py"], desc="Counting lines of code...")


@app.command("all")
def check_all(
    fix: bool = typer.Option(False, "--fix", "-f", help="Automatically fix fixable lint issues."),
) -> None:
    """Run all primary checks (lint, type, docstrings).

    Args:
        fix: If True, automatically fix fixable lint issues.
    """
    console.print("[bold cyan]Running all code quality checks...[/bold cyan]")
    lint(fix=fix)
    type_check()
    docstring()
    console.print("\n[bold green]★ All quality checks passed successfully![/bold green]\n")


if __name__ == "__main__":
    app()
