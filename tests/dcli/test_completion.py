# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/completion.py."""

from __future__ import annotations

import pytest

from tools.dcli.completion import (
    complete,
    get_active_toolsets,
    get_completion_candidates,
    get_subcommand_candidates,
)


def test_get_active_toolsets() -> None:
    """Test retrieving active toolsets."""
    toolsets = get_active_toolsets()
    assert "code-check" in toolsets
    assert "release-assets" in toolsets
    assert "test" in toolsets
    assert "docs" in toolsets
    assert "pypi" in toolsets


def test_get_subcommand_candidates() -> None:
    """Test retrieving subcommands for a specific toolset."""
    check_cmds = get_subcommand_candidates("code-check")
    assert "lint" in check_cmds
    assert "type" in check_cmds
    assert "docstring" in check_cmds
    assert "lines" in check_cmds

    # Matching with prefix
    prefix_cmds = get_subcommand_candidates("code-check", prefix="li")
    assert "lint" in prefix_cmds
    assert "lines" in prefix_cmds
    assert "type" not in prefix_cmds


def test_get_completion_candidates_toolset() -> None:
    """Test completion candidates for toolset level."""
    # When user typed './dcli code-' and hits Tab
    candidates = get_completion_candidates(["./dcli", "code-"], cword=1)
    assert candidates == ["code-check"]

    # When user typed './dcli ' and hits Tab
    candidates_all = get_completion_candidates(["./dcli", ""], cword=1)
    assert "code-check" in candidates_all
    assert "test" in candidates_all


def test_get_completion_candidates_subcommands() -> None:
    """Test completion candidates for subcommand level."""
    # When user typed './dcli code-check ' and hits Tab
    candidates = get_completion_candidates(["./dcli", "code-check", ""], cword=2)
    assert "lint" in candidates
    assert "type" in candidates

    # When user typed './dcli code-check do' and hits Tab
    candidates_prefix = get_completion_candidates(["./dcli", "code-check", "do"], cword=2)
    assert "docstring" in candidates_prefix
    assert "lint" not in candidates_prefix


def test_complete_main_output(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the complete() CLI function output."""
    monkeypatch.setenv("COMP_WORDS", "./dcli code-check li")
    monkeypatch.setenv("COMP_CWORD", "2")

    complete()
    captured = capsys.readouterr()
    lines = [line.strip() for line in captured.out.splitlines() if line.strip()]
    assert "lint" in lines
    assert "lines" in lines
    assert "type" not in lines
