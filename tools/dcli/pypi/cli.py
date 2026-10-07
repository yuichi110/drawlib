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

import json
import os
import shutil
from pathlib import Path
from typing import Optional

import typer

from tools.dcli.common import PROJECT_ROOT, console, err_console, run_command
from tools.dcli.pypi.client import (
    LIB_NAME,
    check_new_version_ok,
    get_latest_version,
    get_new_version,
)
from tools.dcli.pypi.client import (
    list_versions as client_list_versions,
)
from tools.dcli.pypi.dep import get_dependencies, get_releases
from tools.dcli.pypi.pyproject import update_pyproject_toml

_get_new_version = get_new_version

app = typer.Typer(
    name="pypi",
    help="Version verification, dependency tracking, metadata sync, and publishing to PyPI / TestPyPI.",
    no_args_is_help=True,
)


@app.command("deps")
def list_dependencies() -> None:
    """List all project dependencies defined in pyproject.toml."""
    dependencies = get_dependencies()
    for dep in dependencies:
        console.print(dep.name)


@app.command("dep-releases")
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


@app.command("list-versions")
def list_versions(
    test_pypi: bool = typer.Option(False, "--test-pypi", help="Query TestPyPI instead of production PyPI."),
) -> None:
    """List all released versions of drawlib from PyPI.

    Args:
        test_pypi: Whether to inspect TestPyPI.
    """
    console.print("[bold cyan]Querying PyPI versions...[/bold cyan]")
    try:
        versions = client_list_versions(LIB_NAME, test_pypi=test_pypi)
    except Exception as e:
        err_console.print(f"[bold red]Failed to fetch versions: {e}[/bold red]")
        raise typer.Exit(code=1) from e

    for v in versions:
        console.print(f"  [yellow]{v}[/yellow]")


@app.command("latest")
def get_latest(
    test_pypi: bool = typer.Option(False, "--test-pypi", help="Query TestPyPI instead of production PyPI."),
) -> None:
    """Get the latest released version of drawlib from PyPI.

    Args:
        test_pypi: Whether to inspect TestPyPI.
    """
    console.print("[bold cyan]Querying latest PyPI version...[/bold cyan]")
    try:
        latest = get_latest_version(LIB_NAME, test_pypi=test_pypi)
    except Exception as e:
        err_console.print(f"[bold red]Failed to fetch latest version: {e}[/bold red]")
        raise typer.Exit(code=1) from e

    console.print(f"Latest version: [bold green]{latest}[/bold green]")


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
    console.print("[bold cyan]Validating new version...[/bold cyan]")
    latest_version = get_latest_version(LIB_NAME, test_pypi)
    new_version = get_new_version()
    try:
        check_new_version_ok(latest_version, new_version, allow_jump=allow_jump)
        console.print("[bold green]✓ Check success. Version is valid for release.[/bold green]")
    except Exception as e:
        err_console.print(f"[bold red]Check failed: {e}[/bold red]")
        raise typer.Exit(code=1) from e


@app.command("update-pyproject")
def update_pyproject() -> None:
    """Synchronize pyproject.toml metadata and version from src/drawlib/__init__.py."""
    console.print("[bold cyan]Updating pyproject.toml metadata...[/bold cyan]")
    update_pyproject_toml()
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

    dist_dir = PROJECT_ROOT / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    run_command(["uv", "run", "drawlib", "cache", "clear", "--all"], desc="Purging cached assets...")
    run_command(["uv", "build"], desc="Building wheel and sdist distributions...")

    publish_cmd = ["uv", "publish"]
    if test_pypi:
        publish_cmd.extend(["--publish-url", "https://test.pypi.org/legacy/"])
    publish_cmd.extend(["--token", resolved_token])

    run_command(publish_cmd, desc=f"Uploading distribution to {target_name}...")
    console.print(f"[bold green]★ Successfully published to {target_name}![/bold green]")


if __name__ == "__main__":
    app()
