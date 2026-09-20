# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""PyPI publishing and version management toolset."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Optional

import typer

from tools.dcli.common import console, err_console, run_command

app = typer.Typer(
    name="pypi",
    help="Version verification, metadata synchronization, and publishing to PyPI / TestPyPI.",
    no_args_is_help=True,
)


@app.command("list-versions")
def list_versions(
    test_pypi: bool = typer.Option(False, "--test-pypi", help="Query TestPyPI instead of production PyPI."),
) -> None:
    """List all released versions of drawlib from PyPI.

    Args:
        test_pypi: Whether to inspect TestPyPI.
    """
    cmd = ["uv", "run", "python", "tools/scripts/pypi_tools.py", "--list_versions"]
    if test_pypi:
        cmd.append("--test_pypi")
    run_command(cmd, desc="Querying PyPI versions...")


@app.command("latest")
def get_latest(
    test_pypi: bool = typer.Option(False, "--test-pypi", help="Query TestPyPI instead of production PyPI."),
) -> None:
    """Get the latest released version of drawlib from PyPI.

    Args:
        test_pypi: Whether to inspect TestPyPI.
    """
    cmd = ["uv", "run", "python", "tools/scripts/pypi_tools.py", "--get_latest_version"]
    if test_pypi:
        cmd.append("--test_pypi")
    run_command(cmd, desc="Querying latest PyPI version...")


@app.command("check-version")
def check_version(
    test_pypi: bool = typer.Option(False, "--test-pypi", help="Check against TestPyPI instead of production PyPI."),
    allow_jump: bool = typer.Option(False, "--allow-jump", help="Allow major/minor version jumps."),
) -> None:
    """Check if local version in src/drawlib/__init__.py is valid for release.

    Args:
        test_pypi: Whether to validate against TestPyPI.
        allow_jump: Whether to permit non-consecutive version jumps.
    """
    cmd = ["uv", "run", "python", "tools/scripts/pypi_tools.py", "--check_new_version_ok"]
    if test_pypi:
        cmd.append("--test_pypi")
    if allow_jump:
        cmd.append("--allow_jump")
    run_command(cmd, desc="Validating new version...")


@app.command("update-pyproject")
def update_pyproject() -> None:
    """Synchronize pyproject.toml metadata and version from src/drawlib/__init__.py."""
    run_command(
        ["uv", "run", "python", "tools/scripts/update_pyprojecttoml.py"],
        desc="Updating pyproject.toml metadata...",
    )
    console.print("[bold green]✓ pyproject.toml updated successfully![/bold green]")


@app.command("publish")
def publish(
    test_pypi: bool = typer.Option(False, "--test-pypi", help="Publish to TestPyPI instead of production PyPI."),
    allow_jump: bool = typer.Option(False, "--allow-jump", help="Allow major/minor version jumps."),
    token: Optional[str] = typer.Option(None, "--token", help="PyPI API token (or via environment variable)."),
) -> None:
    """Build and publish package to PyPI or TestPyPI.

    Args:
        test_pypi: Whether to publish to TestPyPI.
        allow_jump: Whether to allow version jumps.
        token: PyPI token (overrides env var).

    Raises:
        typer.Exit: If required publishing token is missing.
    """
    env_token_name = "TEST_PYPI_TOKEN" if test_pypi else "PYPI_TOKEN"
    resolved_token = token or os.environ.get(env_token_name)
    if not resolved_token:
        err_console.print(
            f"[bold red]Error: Token not found. Set ${env_token_name} or pass --token <TOKEN>[/bold red]"
        )
        raise typer.Exit(code=1)

    target_name = "TestPyPI" if test_pypi else "PyPI"
    console.print(f"[bold cyan]Preparing to publish drawlib to {target_name}...[/bold cyan]")

    update_pyproject()
    check_version(test_pypi=test_pypi, allow_jump=allow_jump)

    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    run_command(["uv", "run", "python", "-m", "drawlib", "--purge_font_cache"], desc="Purging font cache...")
    run_command(["uv", "build"], desc="Building wheel and sdist distributions...")

    publish_cmd = ["uv", "publish"]
    if test_pypi:
        publish_cmd.extend(["--publish-url", "https://test.pypi.org/legacy/"])
    publish_cmd.extend(["--token", resolved_token])

    run_command(publish_cmd, desc=f"Uploading distribution to {target_name}...")
    console.print(f"[bold green]★ Successfully published to {target_name}![/bold green]")


if __name__ == "__main__":
    app()
