# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/code_check."""

from __future__ import annotations

from unittest.mock import patch

from typer.testing import CliRunner

from tools.dcli.code_check import app
from tools.dcli.code_check.docstring import check_file
from tools.dcli.code_check.lines import count_lines_in_file

runner = CliRunner()


def test_count_lines_in_file(tmp_path) -> None:
    """Test counting lines in a file."""
    test_file = tmp_path / "test.py"
    test_file.write_text("line 1\nline 2\nline 3\n", encoding="utf-8")
    assert count_lines_in_file(test_file) == 3


def test_check_cli_docstring() -> None:
    """Test dcli check docstring command."""
    result = runner.invoke(app, ["docstring"])
    assert result.exit_code == 0
    assert "Docstring checks passed" in result.output


def test_docstring_check_file_handles_non_docstring_first_expr(tmp_path) -> None:
    """Verify check_file handles @validate_call functions starting with a non-string expression (Python 3.14+)."""
    target = tmp_path / "sample.py"
    target.write_text(
        "@validate_call\ndef no_doc_call() -> None:\n    helper()\n\n"
        '@validate_call\ndef bad_doc(x: int) -> None:\n    """Args: x (TypeFloat): value."""\n    pass\n',
        encoding="utf-8",
    )
    violations = check_file(str(target))
    assert len(violations) == 1
    assert violations[0][1] == "TypeFloat"


def test_check_cli_lint_uses_no_fix_by_default() -> None:
    """Test dcli code-check lint passes --no-fix when --fix is not specified."""
    with patch("tools.dcli.code_check.cli.run_command") as mock_run:
        result = runner.invoke(app, ["lint"])
        assert result.exit_code == 0
        cmds = [call.args[0] for call in mock_run.call_args_list]
        assert cmds == [
            ["uv", "run", "ruff", "check", "--no-fix", "src"],
            ["uv", "run", "ruff", "check", "--no-fix", "tests"],
            ["uv", "run", "ruff", "check", "--no-fix", "tools"],
        ]


def test_check_cli_lint_uses_fix_when_requested() -> None:
    """Test dcli code-check lint passes --fix when --fix is specified."""
    with patch("tools.dcli.code_check.cli.run_command") as mock_run:
        result = runner.invoke(app, ["lint", "--fix"])
        assert result.exit_code == 0
        cmds = [call.args[0] for call in mock_run.call_args_list]
        assert cmds == [
            ["uv", "run", "ruff", "check", "--fix", "src"],
            ["uv", "run", "ruff", "check", "--fix", "tests"],
            ["uv", "run", "ruff", "check", "--fix", "tools"],
        ]
