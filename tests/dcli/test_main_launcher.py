# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/__main__.py (Master Launcher)."""

from __future__ import annotations

from typer.testing import CliRunner

from tools.dcli.__main__ import app, discover_toolsets

runner = CliRunner()


def test_discover_toolsets() -> None:
    """Test discovering available CLI toolsets."""
    toolsets = discover_toolsets()
    expected = {"assets", "check", "codegen", "docker", "docs", "pypi", "test"}
    assert expected == set(toolsets)
    assert "__init__" not in toolsets
    assert "common" not in toolsets
    assert "completion" not in toolsets


def test_launcher_help_table() -> None:
    """Test dcli master launcher displays available toolsets table."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Drawlib Development CLI (dcli)" in result.output
    assert "Available Toolsets" in result.output
    assert "check" in result.output
    assert "test" in result.output
    assert "docs" in result.output


def test_launcher_invalid_toolset() -> None:
    """Test dcli master launcher handles invalid toolset gracefully."""
    result = runner.invoke(app, ["--invalid-toolset", "invalid_xyz"])
    assert result.exit_code == 1
    assert "Error: Invalid Toolset" in result.output
    assert "invalid_xyz" in result.output
