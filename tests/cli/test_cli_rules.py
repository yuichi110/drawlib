# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests for drawlib rules CLI command."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


def run_drawlib_cli(args: list[str], cwd: str) -> subprocess.CompletedProcess[str]:
    """Helper to execute drawlib CLI command via subprocess with current PYTHONPATH."""
    env = os.environ.copy()
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
    env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")

    cmd = [sys.executable, "-m", "drawlib"] + args
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=False)


def test_cli_rules_default(tmp_path: Path) -> None:
    """Test `drawlib rules` without arguments outputs overview."""
    res = run_drawlib_cli(["rules"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "# Drawlib Agent Drawing Guidelines" in res.stdout
    assert "from drawlib.canvas import" in res.stdout


def test_cli_rules_show_default(tmp_path: Path) -> None:
    """Test `drawlib rules show` without topic outputs overview."""
    res = run_drawlib_cli(["rules", "show"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "# Drawlib Agent Drawing Guidelines" in res.stdout


def test_cli_rules_list(tmp_path: Path) -> None:
    """Test `drawlib rules list` lists all topics."""
    res = run_drawlib_cli(["rules", "list"], cwd=str(tmp_path))
    assert res.returncode == 0
    for topic in [
        "overview",
        "cli",
        "docs_build",
        "shapes",
        "lines",
        "text",
        "icons",
        "preset_styles",
        "smartarts",
        "charts",
        "diagrams",
    ]:
        assert topic in res.stdout


@pytest.mark.parametrize(
    "topic,expected_heading",
    [
        ("overview", "# Drawlib Agent Drawing Guidelines"),
        ("cli", "# Drawlib CLI Guidelines"),
        ("docs_build", "# Drawlib Documentation Build Guidelines"),
        ("shapes", "# Drawlib Shapes Guidelines"),
        ("lines", "# Drawlib Lines Guidelines"),
        ("text", "# Drawlib Text Guidelines"),
        ("icons", "# Drawlib Icons Guidelines"),
        ("preset_styles", "# Drawlib Preset Styles Guidelines"),
        ("smartarts", "# Drawlib SmartArts Guidelines"),
        ("charts", "# Drawlib Charts Guidelines"),
        ("diagrams", "# Drawlib Diagrams Guidelines"),
    ],
)
def test_cli_rules_show_topics(tmp_path: Path, topic: str, expected_heading: str) -> None:
    """Test `drawlib rules show <topic>` for each supported topic."""
    res = run_drawlib_cli(["rules", "show", topic], cwd=str(tmp_path))
    assert res.returncode == 0
    assert expected_heading in res.stdout


def test_cli_rules_show_themes_alias(tmp_path: Path) -> None:
    """Test `drawlib rules show themes` redirects to preset_styles with a friendly note."""
    res = run_drawlib_cli(["rules", "show", "themes"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "# Drawlib Preset Styles Guidelines" in res.stdout
    assert "preset_styles" in res.stderr.lower()


def test_cli_rules_show_docs_alias(tmp_path: Path) -> None:
    """Test `drawlib rules show docs` redirects to docs_build."""
    res = run_drawlib_cli(["rules", "show", "docs"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "# Drawlib Documentation Build Guidelines" in res.stdout


def test_cli_rules_show_unknown_topic(tmp_path: Path) -> None:
    """Test `drawlib rules show unknown` exits with code 1 and prints available topics."""
    res = run_drawlib_cli(["rules", "show", "unknown_topic"], cwd=str(tmp_path))
    assert res.returncode == 1
    assert "Error: Unknown rule topic 'unknown_topic'" in res.stderr
    assert "Available topics:" in res.stderr
