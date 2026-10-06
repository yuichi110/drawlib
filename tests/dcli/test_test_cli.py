# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/test.py."""

from __future__ import annotations

from unittest.mock import patch

from typer.testing import CliRunner

from tools.dcli.test import _run_pytest, app

runner = CliRunner()


def test_run_pytest_args() -> None:
    """Test pytest argument list construction."""
    with patch("tools.dcli.test.run_command") as mock_run:
        _run_pytest("tests/drawlib/", cov=True, cov_report=True, parallel=True, extra_args=["-k", "test_foo"])
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert cmd[0:3] == ["uv", "run", "pytest"]
        assert "-n" in cmd
        assert "--cov=drawlib" in cmd
        assert "--cov-report=term-missing" in cmd
        assert "tests/drawlib/" in cmd
        assert "-k" in cmd
        assert "test_foo" in cmd


def test_test_all_command() -> None:
    """Test dcli test all command."""
    with patch("tools.dcli.test._run_pytest") as mock_run:
        result = runner.invoke(app, ["all", "--no-cov", "--no-parallel"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with("tests/", cov=False, cov_report=False, parallel=False)


def test_test_dcli_command() -> None:
    """Test dcli test dcli command."""
    with patch("tools.dcli.test._run_pytest") as mock_run:
        result = runner.invoke(app, ["dcli"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with("tests/dcli/", cov=False)


def test_test_core_command() -> None:
    """Test dcli test core command."""
    with patch("tools.dcli.test._run_pytest") as mock_run:
        result = runner.invoke(app, ["core"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with("tests/drawlib/_core/", cov=False)


def test_test_target_command() -> None:
    """Test dcli test target command."""
    with patch("tools.dcli.test._run_pytest") as mock_run:
        result = runner.invoke(app, ["target", "tests/my_test.py"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with("tests/my_test.py", cov=False)
