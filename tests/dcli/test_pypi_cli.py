# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/pypi."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from tools.dcli.pypi import app
from tools.dcli.pypi.client import (
    _get_new_version,
    _parse_version,
    check_new_version_ok,
    get_latest_version,
    list_versions,
)
from tools.dcli.pypi.dep import ReleaseInfo, get_dependencies

runner = CliRunner()


def test_parse_version() -> None:
    """Test version string parsing and sorting."""
    assert _parse_version("0.2.1") > _parse_version("0.2.1.rc1")
    assert _parse_version("0.2.1.rc2") > _parse_version("0.2.1.rc1")
    assert _parse_version("0.3.0") > _parse_version("0.2.9")


def test_check_new_version_ok() -> None:
    """Test version validity checking logic."""
    # Standard valid increments
    check_new_version_ok(latest_version="0.2.0", new_version="0.2.1")
    check_new_version_ok(latest_version="0.2.0", new_version="0.3.0.dev1")
    check_new_version_ok(latest_version="0.2.0", new_version="1.0.0.dev1")

    # Prerelease increments
    check_new_version_ok(latest_version="0.2.0.dev1", new_version="0.2.0.dev2")
    check_new_version_ok(latest_version="0.2.0.dev2", new_version="0.2.0.rc1")
    check_new_version_ok(latest_version="0.2.0.rc1", new_version="0.2.0")

    # Invalid: older version
    with pytest.raises(ValueError, match="must be greater than latest version"):
        check_new_version_ok(latest_version="0.2.5", new_version="0.2.4")

    # Invalid: version jump without allow_jump
    with pytest.raises(ValueError):
        check_new_version_ok(latest_version="0.2.0", new_version="0.4.0.dev1", allow_jump=False)

    # Valid: version jump with allow_jump
    check_new_version_ok(latest_version="0.2.0", new_version="0.4.0.dev1", allow_jump=True)


def test_get_new_version() -> None:
    """Test retrieving local version from __init__.py."""
    version = _get_new_version()
    assert isinstance(version, str)
    assert len(version.split(".")) >= 3


def test_pypi_cli_latest() -> None:
    """Test dcli pypi latest CLI command."""
    with patch("tools.dcli.pypi.cli.get_latest_version", return_value="0.3.0"):
        result = runner.invoke(app, ["latest"])
        assert result.exit_code == 0
        assert "0.3.0" in result.output


def test_pypi_cli_list_versions() -> None:
    """Test dcli pypi list-versions CLI command."""
    with patch("tools.dcli.pypi.cli.client_list_versions", return_value=["0.3.0", "0.2.0"]):
        result = runner.invoke(app, ["list-versions"])
        assert result.exit_code == 0
        assert "0.3.0" in result.output
        assert "0.2.0" in result.output


def test_pypi_cli_check_version_success() -> None:
    """Test dcli pypi check-version success."""
    with (
        patch("tools.dcli.pypi.cli.get_latest_version", return_value="0.2.0"),
        patch("tools.dcli.pypi.cli.get_new_version", return_value="0.2.1"),
        patch("tools.dcli.pypi.cli.check_new_version_ok") as mock_check,
    ):
        result = runner.invoke(app, ["check-version"])
        assert result.exit_code == 0
        assert "Check success" in result.output
        mock_check.assert_called_once_with("0.2.0", "0.2.1", allow_jump=False)


def test_pypi_cli_check_version_failure() -> None:
    """Test dcli pypi check-version failure."""
    with (
        patch("tools.dcli.pypi.cli.get_latest_version", return_value="0.2.1"),
        patch("tools.dcli.pypi.cli.get_new_version", return_value="0.2.0"),
        patch("tools.dcli.pypi.cli.check_new_version_ok", side_effect=ValueError("Invalid version")),
    ):
        result = runner.invoke(app, ["check-version"])
        assert result.exit_code == 1
        assert "Check failed" in result.output


def test_get_dependencies() -> None:
    """Test retrieving dependencies from pyproject.toml."""
    deps = get_dependencies()
    assert len(deps) > 0
    dep_names = [d.name for d in deps]
    assert "matplotlib" in dep_names
    assert "pydantic" in dep_names


def test_pypi_cli_deps() -> None:
    """Test dcli pypi deps command."""
    result = runner.invoke(app, ["deps"])
    assert result.exit_code == 0
    assert "matplotlib" in result.output
    assert "pydantic" in result.output


def test_pypi_cli_dep_releases() -> None:
    """Test dcli pypi dep-releases command."""
    mock_releases = [
        ReleaseInfo(version="0.3.0", timestamps=datetime(2026, 1, 1, tzinfo=timezone.utc)),
        ReleaseInfo(version="0.2.0", timestamps=datetime(2025, 1, 1, tzinfo=timezone.utc)),
    ]
    with patch("tools.dcli.pypi.cli.get_releases", return_value=mock_releases):
        result = runner.invoke(app, ["dep-releases", "drawlib"])
        assert result.exit_code == 0
        assert "0.3.0" in result.output
        assert "0.2.0" in result.output


def test_pypi_cli_dep_releases_json() -> None:
    """Test dcli pypi dep-releases --format json command."""
    mock_releases = [
        ReleaseInfo(version="0.3.0", timestamps=datetime(2026, 1, 1, tzinfo=timezone.utc)),
    ]
    with patch("tools.dcli.pypi.cli.get_releases", return_value=mock_releases):
        result = runner.invoke(app, ["dep-releases", "drawlib", "--format", "json"])
        assert result.exit_code == 0
        assert '"version": "0.3.0"' in result.output


def test_pypi_cli_publish_purges_cache() -> None:
    """Test dcli pypi publish clears cached assets via drawlib cache clear --all before building."""
    with (
        patch("tools.dcli.pypi.cli.update_pyproject"),
        patch("tools.dcli.pypi.cli.check_version"),
        patch("tools.dcli.pypi.cli.run_command") as mock_run,
    ):
        result = runner.invoke(app, ["publish", "--test-pypi", "--token", "dummy-token"])
        assert result.exit_code == 0
        cmds = [call.args[0] for call in mock_run.call_args_list]
        assert ["uv", "run", "drawlib", "cache", "clear", "--all"] in cmds
        assert ["uv", "build"] in cmds
