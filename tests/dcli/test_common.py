# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/common.py."""

from __future__ import annotations

import pytest
import typer

from tools.dcli.common import PROJECT_ROOT, run_command


def test_project_root_is_valid() -> None:
    """Test that PROJECT_ROOT contains pyproject.toml and src/."""
    assert (PROJECT_ROOT / "pyproject.toml").is_file()
    assert (PROJECT_ROOT / "src").is_dir()
    assert (PROJECT_ROOT / "tools").is_dir()


def test_run_command_success() -> None:
    """Test run_command executes simple successful command."""
    run_command(["python3", "-c", "print('hello')"], desc="Test print")


def test_run_command_not_found() -> None:
    """Test run_command handles missing executable."""
    with pytest.raises(typer.Exit) as exc_info:
        run_command(["nonexistent_binary_xyz_123"])
    assert exc_info.value.exit_code == 1


def test_run_command_failure() -> None:
    """Test run_command handles nonzero exit code."""
    with pytest.raises(typer.Exit) as exc_info:
        run_command(["python3", "-c", "import sys; sys.exit(42)"])
    assert exc_info.value.exit_code == 42
