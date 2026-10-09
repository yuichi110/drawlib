# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Test execution and test coverage toolset."""

from __future__ import annotations

from typing import Optional

import typer

from tools.dcli.common import console, run_command

app = typer.Typer(
    name="test",
    help="Run unit, integration, and coverage tests using pytest.",
    no_args_is_help=True,
)


def _run_pytest(
    target: str,
    cov: bool = False,
    cov_report: bool = False,
    parallel: bool = False,
    extra_args: Optional[list[str]] = None,
) -> None:
    """Helper to construct and execute pytest commands.

    Args:
        target: Target test file or directory path.
        cov: Whether to collect coverage for drawlib.
        cov_report: Whether to print coverage report in terminal.
        parallel: Whether to run tests in parallel using pytest-xdist.
        extra_args: Additional arguments forwarded to pytest.
    """
    cmd = ["uv", "run", "pytest", "-s"]
    if parallel:
        cmd.extend(["-n", "auto", "--dist", "loadfile"])
    if cov:
        cmd.append("--cov=drawlib")
        if cov_report:
            cmd.append("--cov-report=term-missing")
    cmd.append(target)
    if extra_args:
        cmd.extend(extra_args)

    run_command(cmd, desc=f"Running pytest on {target}...")


@app.command("all")
def test_all(
    cov: bool = typer.Option(True, "--cov/--no-cov", help="Enable/disable coverage tracking."),
    cov_report: bool = typer.Option(False, "--cov-report", help="Show line-by-line coverage report."),
    parallel: bool = typer.Option(True, "--parallel/--no-parallel", help="Run tests in parallel via pytest-xdist."),
) -> None:
    """Run the complete test suite across all tests (drawlib + dcli).

    Args:
        cov: Whether to run coverage.
        cov_report: Whether to output terminal coverage report.
        parallel: Whether to run tests in parallel.
    """
    _run_pytest("tests/", cov=cov, cov_report=cov_report, parallel=parallel)
    console.print("[bold green]✓ All tests passed successfully![/bold green]")


@app.command("drawlib")
def test_drawlib(
    cov: bool = typer.Option(True, "--cov/--no-cov", help="Enable/disable coverage tracking."),
    cov_report: bool = typer.Option(False, "--cov-report", help="Show line-by-line coverage report."),
    parallel: bool = typer.Option(True, "--parallel/--no-parallel", help="Run tests in parallel via pytest-xdist."),
) -> None:
    """Run all unit and integration tests for drawlib package.

    Args:
        cov: Whether to run coverage.
        cov_report: Whether to output terminal coverage report.
        parallel: Whether to run tests in parallel.
    """
    _run_pytest("tests/drawlib/", cov=cov, cov_report=cov_report, parallel=parallel)
    console.print("[bold green]✓ All drawlib tests passed successfully![/bold green]")


@app.command("dcli")
def test_dcli(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run tests for dcli developer CLI tools.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/dcli/", cov=cov)
    console.print("[bold green]✓ All dcli tests passed successfully![/bold green]")


MODULE_SHORTCUTS: dict[str, str] = {
    "drawlib": "tests/drawlib/",
    "dcli": "tests/dcli/",
    "core": "tests/drawlib/_core/",
    "types": "tests/drawlib/_core/l2_types/",
    "styles": "tests/drawlib/_core/l3_styles/",
    "fonts": "tests/drawlib/_core/l3_fonts/",
    "images": "tests/drawlib/_core/l3_images/",
    "preset-styles": "tests/drawlib/preset_styles/",
    "canvas": "tests/drawlib/_core/l4_canvas/",
    "icons": "tests/drawlib/icons/",
    "smartarts": "tests/drawlib/smartarts/",
    "charts": "tests/drawlib/charts/",
    "diagrams": "tests/drawlib/diagrams/",
    "geo": "tests/drawlib/geo/",
    "graph": "tests/drawlib/graph/",
    "slide": "tests/drawlib/slide/",
    "anim": "tests/drawlib/anim/",
    "cli": "tests/drawlib/cli/",
    "doc-builder": "tests/drawlib/doc_builder/",
}


@app.command("target")
def test_target(
    target: str = typer.Argument(
        ...,
        help="Module shortcut keyword (e.g. 'canvas', 'smartarts', 'core') or test file/directory path.",
    ),
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
    cov_report: bool = typer.Option(False, "--cov-report", help="Show line-by-line coverage report."),
    parallel: bool = typer.Option(False, "--parallel/--no-parallel", help="Run tests in parallel via pytest-xdist."),
) -> None:
    """Run pytest targeting a specific module shortcut or file/directory path.

    Available shortcuts:
        core, types, styles, fonts, images, preset-styles, canvas, icons,
        smartarts, charts, diagrams, graph, slide, anim, cli, doc-builder

    Args:
        target: Shorthand module name or path.
        cov: Whether to run coverage.
        cov_report: Whether to output terminal coverage report.
        parallel: Whether to run tests in parallel.
    """
    resolved_target = MODULE_SHORTCUTS.get(target, target)
    _run_pytest(resolved_target, cov=cov, cov_report=cov_report, parallel=parallel)
    console.print(f"[bold green]✓ Target tests for '{target}' passed successfully![/bold green]")


if __name__ == "__main__":
    app()
