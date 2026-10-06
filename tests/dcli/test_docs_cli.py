# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/docs."""

from __future__ import annotations

from unittest.mock import patch

from typer.testing import CliRunner

from tools.dcli.docs import app
from tools.dcli.docs.builder import ALL_TARGETS, TARGET_MAP

runner = CliRunner()


def test_docs_cli_help() -> None:
    """Test dcli docs --help."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "build" in result.output
    assert "serve" in result.output


def test_target_definitions() -> None:
    """Test that all targets are properly mapped."""
    assert "site" in TARGET_MAP
    assert "docs" in TARGET_MAP
    assert "quickstart" in TARGET_MAP
    assert "dogfooding" in TARGET_MAP
    assert "dogfooding-en" in TARGET_MAP
    assert "slide" in TARGET_MAP
    assert "readme" in TARGET_MAP


def test_docs_build_unknown_target() -> None:
    """Test building an unknown target reports error."""
    result = runner.invoke(app, ["build", "nonexistent_target"])
    assert result.exit_code == 1
    assert "Unknown target" in result.output


def test_docs_build_invocation() -> None:
    """Test build command invokes build_docs correctly."""
    with patch("tools.dcli.docs.cli.build_docs") as mock_build:
        result = runner.invoke(app, ["build", "quickstart", "--no-clean"])
        assert result.exit_code == 0
        mock_build.assert_called_once_with(target_name="quickstart", build_all=False, clean=False)


def test_docs_build_all_invocation() -> None:
    """Test build --all invokes build_docs correctly."""
    with patch("tools.dcli.docs.cli.build_docs") as mock_build:
        result = runner.invoke(app, ["build", "--all"])
        assert result.exit_code == 0
        mock_build.assert_called_once_with(target_name=None, build_all=True, clean=True)


def test_docs_serve_nonexistent_directory(tmp_path) -> None:
    """Test serve reports error if target directory does not exist."""
    result = runner.invoke(app, ["serve", "nonexistent_dir"])
    assert result.exit_code == 1
    assert "does not exist" in result.output
