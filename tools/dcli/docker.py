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

import shutil
import subprocess
from typing import Optional

import typer

from tools.dcli.common import console, err_console, run_command

app = typer.Typer(
    name="docker",
    help="Build production drawlib images and run clean-room container tests.",
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


def _ensure_docker_ready() -> None:
    """Verify both Docker CLI and daemon are ready.

    Raises:
        typer.Exit: If CLI is missing or daemon is not running.
    """
    _check_docker_cli()
    if not _is_daemon_running():
        err_console.print("[bold red]Error: Docker daemon is not running.[/bold red]")
        raise typer.Exit(code=1)


def _resolve_prod_image_tag(
    custom_tag: Optional[str],
    with_pdf: bool,
    with_assets: bool,
) -> str:
    """Resolve full image name and tag for production build."""
    if custom_tag:
        return custom_tag if ":" in custom_tag else f"drawlib:{custom_tag}"
    if with_pdf and with_assets:
        return "drawlib:full"
    if with_pdf:
        return "drawlib:pdf"
    if with_assets:
        return "drawlib:assets"
    return "drawlib:slim"


@app.command("status")
def status() -> None:
    """Check Docker CLI and daemon status."""
    _check_docker_cli()
    if _is_daemon_running():
        console.print("[bold green]Docker daemon is running.[/bold green]")
    else:
        console.print("[bold yellow]Docker daemon is NOT running or not responding.[/bold yellow]")


@app.command("build")
def build(
    pdf: bool = typer.Option(False, "--pdf", help="Include PDF conversion engine (Playwright + Chromium)."),
    assets: bool = typer.Option(False, "--assets", help="Pre-download all font and icon packages for offline usage."),
    full: bool = typer.Option(False, "--full", help="Build full offline-ready image (--pdf + --assets)."),
    python: str = typer.Option("3.12", "--python", help="Python base version (e.g. 3.11, 3.12, 3.13)."),
    pypi: Optional[str] = typer.Option(
        None,
        "--pypi",
        help="Install specified drawlib version from PyPI instead of local source.",
    ),
    tag: Optional[str] = typer.Option(
        None,
        "--tag",
        "-t",
        help="Custom image tag (defaults to 'slim', 'pdf', 'assets', or 'full').",
    ),
) -> None:
    """Build production drawlib Docker image (slim, pdf, assets, or full)."""
    _ensure_docker_ready()

    with_pdf = pdf or full
    with_assets = assets or full
    image_ref = _resolve_prod_image_tag(tag, with_pdf=with_pdf, with_assets=with_assets)
    install_source = "pypi" if pypi else "local"

    cmd = [
        "docker",
        "build",
        "-f",
        "tools/docker/Dockerfile.prod",
        "--build-arg",
        f"PYTHON_VERSION={python}",
        "--build-arg",
        f"INSTALL_SOURCE={install_source}",
        "--build-arg",
        f"DRAWLIB_VERSION={pypi or ''}",
        "--build-arg",
        f"WITH_PDF={'true' if with_pdf else 'false'}",
        "--build-arg",
        f"WITH_ASSETS={'true' if with_assets else 'false'}",
        "-t",
        image_ref,
        ".",
    ]
    run_command(cmd, desc=f"Building production image {image_ref}...")
    console.print(f"[bold green]✓ Image {image_ref} built successfully![/bold green]")


@app.command("test")
def test(
    pypi: Optional[str] = typer.Option(
        None,
        "--pypi",
        help="Test specified drawlib version installed from official PyPI.",
    ),
    test_pypi: Optional[str] = typer.Option(
        None,
        "--test-pypi",
        help="Test specified drawlib version installed from TestPyPI.",
    ),
    python: str = typer.Option("3.12", "--python", help="Python base version (e.g. 3.11, 3.12, 3.13)."),
) -> None:
    """Build clean-room test image (local or PyPI) and run pytest inside container."""
    if pypi and test_pypi:
        err_console.print("[bold red]Error: Cannot specify both --pypi and --test-pypi.[/bold red]")
        raise typer.Exit(code=1)

    _ensure_docker_ready()

    if pypi or test_pypi:
        version = pypi or test_pypi or ""
        repo_label = "test-pypi" if test_pypi else "pypi"
        pypi_url = "https://test.pypi.org/simple/" if test_pypi else "https://pypi.org/simple/"
        image_ref = f"test-drawlib:p{python}_{repo_label}_d{version}"
        build_cmd = [
            "docker",
            "build",
            "-f",
            "tools/docker/Dockerfile.test_pypi",
            "--build-arg",
            f"PYTHON_VERSION={python}",
            "--build-arg",
            f"PYPI_URL={pypi_url}",
            "--build-arg",
            f"DRAWLIB_VERSION={version}",
            "-t",
            image_ref,
            ".",
        ]
    else:
        image_ref = f"test-drawlib:p{python}_local"
        build_cmd = [
            "docker",
            "build",
            "-f",
            "tools/docker/Dockerfile.test_local",
            "--build-arg",
            f"PYTHON_VERSION={python}",
            "-t",
            image_ref,
            ".",
        ]

    run_command(build_cmd, desc=f"Building test image {image_ref}...")
    run_command(
        ["docker", "run", "--rm", image_ref],
        desc=f"Running pytest inside container {image_ref}...",
    )
    console.print(f"[bold green]✓ Container tests passed in {image_ref}![/bold green]")


@app.command("list")
def list_images() -> None:
    """List all drawlib and test-drawlib Docker images."""
    _check_docker_cli()
    run_command(
        [
            "docker",
            "images",
            "--filter",
            "reference=drawlib",
            "--filter",
            "reference=test-drawlib",
        ],
        desc="Listing drawlib Docker images...",
    )


@app.command("prune")
def prune_images() -> None:
    """Remove all drawlib and test-drawlib Docker images."""
    _check_docker_cli()
    proc = subprocess.run(
        [
            "docker",
            "images",
            "--filter",
            "reference=drawlib",
            "--filter",
            "reference=test-drawlib",
            "-q",
        ],  # noqa: S603, S607
        capture_output=True,
        text=True,
        check=False,
    )
    # Deduplicate image IDs while preserving order
    image_ids = list(dict.fromkeys(line.strip() for line in proc.stdout.splitlines() if line.strip()))
    if not image_ids:
        console.print("[yellow]No drawlib or test-drawlib images found.[/yellow]")
        return

    run_command(["docker", "rmi", "-f", *image_ids], desc="Removing drawlib Docker images...")
    console.print("[bold green]✓ All drawlib Docker images removed.[/bold green]")


if __name__ == "__main__":
    app()
