# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Integration tests for the ./dcli bash script executable."""

# ruff: noqa: S404, S603

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

from tools.dcli.common import PROJECT_ROOT

DCLI_PATH = PROJECT_ROOT / "dcli"
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


def _run_dcli(*args: str, extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """Run ./dcli with color disabled and strip any ANSI escape codes."""
    env = os.environ.copy()
    env["NO_COLOR"] = "1"
    env["TERM"] = "dumb"
    env.pop("FORCE_COLOR", None)
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        [str(DCLI_PATH), *args],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        env=env,
        check=False,
    )
    proc.stdout = _ANSI_ESCAPE_RE.sub("", proc.stdout)
    proc.stderr = _ANSI_ESCAPE_RE.sub("", proc.stderr)
    return proc


def test_dcli_script_no_args() -> None:
    """Test ./dcli execution with no arguments displays available toolsets."""
    proc = _run_dcli()
    assert proc.returncode == 0
    assert "Drawlib Development CLI (dcli)" in proc.stdout
    assert "Available Toolsets" in proc.stdout
    assert "code-check" in proc.stdout
    assert "release-assets" in proc.stdout
    assert "test" in proc.stdout


def test_dcli_script_help() -> None:
    """Test ./dcli --help execution."""
    proc = _run_dcli("--help")
    assert proc.returncode == 0
    assert "Usage: python -m tools.dcli" in proc.stdout


def test_dcli_script_invalid_toolset() -> None:
    """Test ./dcli with an invalid toolset name returns exit code 1."""
    proc = _run_dcli("unknown_toolset_xyz")
    assert proc.returncode == 1
    assert "Error: Invalid Toolset" in proc.stdout
    assert "unknown_toolset_xyz" in proc.stdout


def test_dcli_script_subcommand_dispatch() -> None:
    """Test ./dcli code-check --help dispatches properly to the code_check toolset."""
    proc = _run_dcli("code-check", "--help")
    assert proc.returncode == 0
    assert "lint" in proc.stdout
    assert "type" in proc.stdout
    assert "docstring" in proc.stdout


def test_dcli_script_autocomplete_toolsets() -> None:
    """Test ./dcli autocompletion hook for toolset names."""
    env = os.environ.copy()
    env["_DCLI_COMPLETE"] = "complete"
    env["COMP_WORDS"] = "./dcli "
    env["COMP_CWORD"] = "1"

    proc = subprocess.run(
        [str(DCLI_PATH)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        env=env,
        check=False,
    )
    assert proc.returncode == 0
    candidates = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    assert "code-check" in candidates
    assert "release-assets" in candidates
    assert "test" in candidates
    assert "docs" in candidates


def test_dcli_script_autocomplete_subcommands() -> None:
    """Test ./dcli autocompletion hook for toolset subcommands."""
    env = os.environ.copy()
    env["_DCLI_COMPLETE"] = "complete"
    env["COMP_WORDS"] = "./dcli code-check "
    env["COMP_CWORD"] = "2"

    proc = subprocess.run(
        [str(DCLI_PATH)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        env=env,
        check=False,
    )
    assert proc.returncode == 0
    candidates = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    assert "lint" in candidates
    assert "type" in candidates
