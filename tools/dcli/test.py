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
    """Run _core unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/_core/", cov=cov)


@app.command("types")
def test_types(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l2_types unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/_core/l2_types/", cov=cov)


@app.command("styles")
def test_styles(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l3_styles unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/_core/l3_styles/", cov=cov)


@app.command("fonts")
def test_fonts(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l3_fonts unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/_core/l3_fonts/", cov=cov)


@app.command("images")
def test_images(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l3_images unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/_core/l3_images/", cov=cov)


@app.command("preset-styles")
def test_preset_styles(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run preset_styles unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/preset_styles/", cov=cov)


@app.command("canvas")
def test_canvas(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run l4_canvas unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/_core/l4_canvas/", cov=cov)


@app.command("icons")
def test_icons(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run icons unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/icons/", cov=cov)


@app.command("smartarts")
def test_smartarts(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run smartarts unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/smartarts/", cov=cov)


@app.command("charts")
def test_charts(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run charts unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/charts/", cov=cov)


@app.command("diagrams")
def test_diagrams(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run diagrams unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/diagrams/", cov=cov)


@app.command("graph")
def test_graph(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run graph layout unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/graph/", cov=cov)


@app.command("slide")
def test_slide(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run slide presentation unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/slide/", cov=cov)


@app.command("anim")
def test_anim(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run animation unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/anim/", cov=cov)


@app.command("cli")
def test_cli(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run CLI unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/cli/", cov=cov)


@app.command("doc-builder")
def test_doc_builder(
    cov: bool = typer.Option(False, "--cov/--no-cov", help="Enable/disable coverage tracking."),
) -> None:
    """Run doc_builder unit tests.

    Args:
        cov: Whether to collect coverage.
    """
    _run_pytest("tests/drawlib/doc_builder/", cov=cov)


if __name__ == "__main__":
    app()
