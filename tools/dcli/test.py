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
    """Run the complete test suite across all tests.

    Args:
        cov: Whether to run coverage.
        cov_report: Whether to output terminal coverage report.
        parallel: Whether to run tests in parallel.
    """
    _run_pytest("tests/", cov=cov, cov_report=cov_report, parallel=parallel)
    console.print("[bold green]✓ All tests passed successfully![/bold green]")


@app.command("target")
def test_target(
    path: str = typer.Argument(..., help="Path to specific test directory or file."),
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run pytest targeting a specific test path or file.

    Args:
        path: Path to file or directory.
        cov: Whether to run coverage.
    """
    _run_pytest(path, cov=cov)


@app.command("core")
def test_core(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l1_core unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/l1_core/", cov=cov)


@app.command("models")
def test_models(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l2_models unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/l2_models/", cov=cov)


@app.command("types")
def test_types(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l2_types unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/l2_types/", cov=cov)


@app.command("styles")
def test_styles(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l3_styles unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/l3_styles/", cov=cov)


@app.command("fonts")
def test_fonts(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l3_fonts unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/l3_fonts/", cov=cov)


@app.command("preset-styles")
def test_preset_styles(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run preset_styles unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/preset_styles/", cov=cov)


@app.command("canvas")
def test_canvas(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l4_canvas unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/l4_canvas/", cov=cov)


@app.command("icons")
def test_icons(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l6_icons unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/l6_icons/", cov=cov)


@app.command("cli")
def test_cli(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run CLI unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/cli/", cov=cov)


@app.command("doc-builder")
def test_doc_builder(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run doc_builder unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/doc_builder/", cov=cov)


@app.command("smartarts")
def test_smartarts(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l7_smartarts unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/l7_smartarts/", cov=cov)


if __name__ == "__main__":
    app()
