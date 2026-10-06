# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/dep."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import patch

from typer.testing import CliRunner

from tools.dcli.dep import app
from tools.dcli.dep.inspector import DependencyInfo, ReleaseInfo, get_dependencies

runner = CliRunner()


def test_get_dependencies() -> None:
    """Test retrieving dependencies from pyproject.toml."""
    deps = get_dependencies()
    assert len(deps) > 0
    dep_names = [d.name for d in deps]
    assert "matplotlib" in dep_names
    assert "pydantic" in dep_names


def test_dep_cli_list() -> None:
    """Test dcli dep list command."""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "matplotlib" in result.output
    assert "pydantic" in result.output


def test_dep_cli_releases() -> None:
    """Test dcli dep releases command."""
    mock_releases = [
        ReleaseInfo(version="0.3.0", timestamps=datetime(2026, 1, 1, tzinfo=timezone.utc)),
        ReleaseInfo(version="0.2.0", timestamps=datetime(2025, 1, 1, tzinfo=timezone.utc)),
    ]
    with patch("tools.dcli.dep.cli.get_releases", return_value=mock_releases):
        result = runner.invoke(app, ["releases", "drawlib"])
        assert result.exit_code == 0
        assert "0.3.0" in result.output
        assert "0.2.0" in result.output


def test_dep_cli_releases_json() -> None:
    """Test dcli dep releases --format json command."""
    mock_releases = [
        ReleaseInfo(version="0.3.0", timestamps=datetime(2026, 1, 1, tzinfo=timezone.utc)),
    ]
    with patch("tools.dcli.dep.cli.get_releases", return_value=mock_releases):
        result = runner.invoke(app, ["releases", "drawlib", "--format", "json"])
        assert result.exit_code == 0
        assert '"version": "0.3.0"' in result.output
