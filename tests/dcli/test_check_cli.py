# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/check."""

from __future__ import annotations

from typer.testing import CliRunner

from tools.dcli.check import app
from tools.dcli.check.lines import count_lines_in_file

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
