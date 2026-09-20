# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Docker container and test image management toolset."""

from __future__ import annotations

import platform
import shutil
import subprocess
from typing import Optional

import typer

from tools.dcli.common import console, err_console, run_command

app = typer.Typer(
    name="docker",
    help="Manage local Docker daemon and test container images.",
    no_args_is_help=True,
)


def _check_docker_cli() -> None:
    """Check if docker CLI is available in PATH.

    Raises:
        typer.Exit: If docker command is not found.
    """
    if not shutil.which("docker"):
        err_console.print("[bold red]Error: 'docker' CLI not found in PATH.[/bold red]")
        raise typer.Exit(code=1)


def _is_daemon_running() -> bool:
    """Check if the Docker daemon is responding."""
    res = subprocess.run(
        ["docker", "info", "--format", "{{.ServerVersion}}"],  # noqa: S603, S607
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return res.returncode == 0


@app.command("daemon-status")
def daemon_status() -> None:
    """Check Docker daemon status."""
    _check_docker_cli()
    if _is_daemon_running():
        console.print("[bold green]Docker daemon is running.[/bold green]")
    else:
        console.print("[bold yellow]Docker daemon is NOT running or not responding.[/bold yellow]")


@app.command("daemon-start")
def daemon_start() -> None:
    """Start Docker Desktop application (macOS only).

    Raises:
        typer.Exit: If executed on a non-macOS system.
    """
    if platform.system() != "Darwin":
        err_console.print("[bold red]Error: daemon-start is only supported on macOS.[/bold red]")
        raise typer.Exit(code=1)

    if _is_daemon_running():
        console.print("[bold green]Docker daemon is already running.[/bold green]")
        return

    run_command(["open", "-a", "Docker"], desc="Starting Docker Desktop...")
    console.print("[cyan]Please wait while Docker Desktop starts up...[/cyan]")


@app.command("daemon-stop")
def daemon_stop() -> None:
    """Stop all running Docker containers and quit Docker Desktop (macOS only).

    Raises:
        typer.Exit: If executed on a non-macOS system.
    """
    if platform.system() != "Darwin":
        err_console.print("[bold red]Error: daemon-stop is only supported on macOS.[/bold red]")
        raise typer.Exit(code=1)

    console.print("[cyan]Stopping running containers...[/cyan]")
    ps_proc = subprocess.run(
        ["docker", "ps", "-q"],  # noqa: S603, S607
        capture_output=True,
        text=True,
        check=False,
    )
    running_ids = [line.strip() for line in ps_proc.stdout.splitlines() if line.strip()]
    if running_ids:
        subprocess.run(["docker", "stop", *running_ids], check=False)  # noqa: S603, S607

    console.print("[cyan]Terminating Docker Desktop processes...[/cyan]")
    subprocess.run(["pkill", "-SIGTERM", "-a", "Docker"], check=False)  # noqa: S603, S607
    subprocess.run(["pkill", "-SIGTERM", "-f", "com.docker.backend"], check=False)  # noqa: S603, S607
    console.print("[bold green]✓ Docker shutdown initiated.[/bold green]")


@app.command("build-image")
def build_image(
    version: str = typer.Option(..., "--version", "-v", help="Drawlib version to test."),
    python: str = typer.Option("3.12", "--python", help="Python base version (e.g. 3.11, 3.12)."),
    repo: str = typer.Option("pypi", "--repo", help="PyPI repository ('pypi' or 'test-pypi')."),
) -> None:
    """Build test Docker image using Dockerfile.pypi_test.

    Args:
        version: Drawlib version to test.
        python: Python version.
        repo: Repository to install drawlib from.

    Raises:
        typer.Exit: If daemon is not running.
    """
    _check_docker_cli()
    if not _is_daemon_running():
        err_console.print("[bold red]Error: Docker daemon is not running.[/bold red]")
        raise typer.Exit(code=1)

    pypi_url = "https://test.pypi.org/simple/" if repo == "test-pypi" else "https://pypi.org/simple/"
    tag = f"p{python}_{repo}_d{version}"

    cmd = [
        "docker",
        "build",
        "-f",
        "Dockerfile.pypi_test",
        "--build-arg",
        f"PYTHON_VERSION={python}",
        "--build-arg",
        f"PYPI_URL={pypi_url}",
        "--build-arg",
        f"DRAWLIB_VERSION={version}",
        "-t",
        f"test-drawlib:{tag}",
        ".",
    ]
    run_command(cmd, desc=f"Building test image test-drawlib:{tag}...")
    console.print(f"[bold green]✓ Image test-drawlib:{tag} built successfully![/bold green]")


@app.command("list-images")
def list_images() -> None:
    """List all test-drawlib Docker images."""
    _check_docker_cli()
    run_command(["docker", "images", "test-drawlib"], desc="Listing test-drawlib images...")


@app.command("prune-images")
def prune_images() -> None:
    """Remove all test-drawlib Docker images."""
    _check_docker_cli()
    proc = subprocess.run(
        ["docker", "images", "test-drawlib", "-q"],  # noqa: S603, S607
        capture_output=True,
        text=True,
        check=False,
    )
    image_ids = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if not image_ids:
        console.print("[yellow]No test-drawlib images found.[/yellow]")
        return

    run_command(["docker", "rmi", *image_ids], desc="Removing test-drawlib images...")
    console.print("[bold green]✓ All test-drawlib images removed.[/bold green]")


if __name__ == "__main__":
    app()
