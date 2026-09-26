# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Common test runner utilities for drawlib CLI tests."""

from __future__ import annotations

import os
from typing import Sequence

from typer.testing import CliRunner

from drawlib._tools.cli._app import app


class CliResult:
    """Wrapper around CliRunner Result providing backward-compatible attributes."""

    def __init__(self, exit_code: int, stdout: str, stderr: str = "") -> None:
        self.returncode: int = exit_code
        self.exit_code: int = exit_code
        self.stdout: str = stdout
        self.stderr: str = stderr

    def __repr__(self) -> str:
        """Return developer-friendly string representation of CliResult."""
        return f"CliResult(returncode={self.returncode}, stdout={self.stdout!r}, stderr={self.stderr!r})"


def run_drawlib_cli(args: Sequence[str], cwd: str | None = None) -> CliResult:
    """Execute drawlib CLI in-memory using Typer CliRunner.

    Args:
        args: Command line arguments for drawlib.
        cwd: Optional working directory for command execution.

    Returns:
        CliResult: Result with returncode, stdout, and stderr attributes.
    """
    runner = CliRunner()
    original_cwd = os.getcwd()
    old_display = os.environ.get("DRAWLIB_SHOW_NO_DISPLAY")
    os.environ["DRAWLIB_SHOW_NO_DISPLAY"] = "1"
    try:
        if cwd is not None:
            os.chdir(cwd)
        result = runner.invoke(app, list(args), catch_exceptions=True)
        return CliResult(
            exit_code=result.exit_code,
            stdout=result.stdout,
            stderr=result.stderr if hasattr(result, "stderr") and result.stderr else "",
        )
    finally:
        if cwd is not None:
            os.chdir(original_cwd)
        if old_display is None:
            os.environ.pop("DRAWLIB_SHOW_NO_DISPLAY", None)
        else:
            os.environ["DRAWLIB_SHOW_NO_DISPLAY"] = old_display
