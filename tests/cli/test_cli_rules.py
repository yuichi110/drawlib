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

import pytest

from tests.cli.common import run_drawlib_cli


def test_cli_rules_default() -> None:
    """Test `drawlib rules` without arguments outputs overview."""
    res = run_drawlib_cli(["rules"])
    assert res.returncode == 0
    assert "# Drawlib Agent Drawing Guidelines" in res.stdout
    assert "from drawlib.canvas import" in res.stdout


def test_cli_rules_show_default() -> None:
    """Test `drawlib rules show` without topic outputs overview."""
    res = run_drawlib_cli(["rules", "show"])
    assert res.returncode == 0
    assert "# Drawlib Agent Drawing Guidelines" in res.stdout


def test_cli_rules_list() -> None:
    """Test `drawlib rules list` lists all topics."""
    res = run_drawlib_cli(["rules", "list"])
    assert res.returncode == 0
    for topic in [
        "overview",
        "overview_min",
        "canvas",
        "config",
        "cli",
        "docs_build",
        "shapes",
        "lines",
        "text",
        "colors",
        "fonts",
        "images",
        "math",
        "types",
        "icons",
        "preset_styles",
        "smartarts",
        "charts",
        "diagrams",
        "tools",
    ]:
        assert topic in res.stdout


@pytest.mark.parametrize(
    "topic,expected_heading",
    [
        ("overview", "# Drawlib Agent Drawing Guidelines"),
        ("overview_min", "# Drawlib Agent Drawing Guidelines (Minimal)"),
        ("canvas", "# Drawlib Canvas Guidelines"),
        ("config", "# Drawlib Configuration Architecture Guidelines"),
        ("cli", "# Drawlib CLI Guidelines"),
        ("docs_build", "# Drawlib Documentation Build Guidelines"),
        ("shapes", "# Drawlib Shapes Guidelines"),
        ("lines", "# Drawlib Lines Guidelines"),
        ("text", "# Drawlib Text Guidelines"),
        ("colors", "# Drawlib Colors Guidelines"),
        ("fonts", "# Drawlib Fonts Guidelines"),
        ("images", "# Drawlib Images Guidelines"),
        ("math", "# Drawlib Math Guidelines"),
        ("types", "# Drawlib Types & Style Models Guidelines"),
        ("tools", "# Drawlib Tools Guidelines"),
        ("icons", "# Drawlib Icons Guidelines"),
        ("preset_styles", "# Drawlib Preset Styles Guidelines"),
        ("smartarts", "# Drawlib SmartArts Guidelines"),
        ("charts", "# Drawlib Charts Guidelines"),
        ("diagrams", "# Drawlib Diagrams Guidelines"),
    ],
)
def test_cli_rules_show_topics(topic: str, expected_heading: str) -> None:
    """Test `drawlib rules show <topic>` for each supported topic."""
    res = run_drawlib_cli(["rules", "show", topic])
    assert res.returncode == 0
    assert expected_heading in res.stdout


def test_cli_rules_show_themes_alias() -> None:
    """Test `drawlib rules show themes` redirects to preset_styles with a friendly note."""
    res = run_drawlib_cli(["rules", "show", "themes"])
    assert res.returncode == 0
    assert "# Drawlib Preset Styles Guidelines" in res.stdout
    assert "preset_styles" in res.stderr.lower()


def test_cli_rules_show_docs_alias() -> None:
    """Test `drawlib rules show docs` redirects to docs_build."""
    res = run_drawlib_cli(["rules", "show", "docs"])
    assert res.returncode == 0
    assert "# Drawlib Documentation Build Guidelines" in res.stdout


def test_cli_rules_show_unknown_topic() -> None:
    """Test `drawlib rules show unknown` exits with code 1 and prints available topics."""
    res = run_drawlib_cli(["rules", "show", "unknown_topic"])
    assert res.returncode == 1
    assert "Error: Unknown rule topic 'unknown_topic'" in res.stderr
    assert "Available topics:" in res.stderr


def test_cli_rules_show_raw() -> None:
    """Test `drawlib rules show --raw` returns raw markdown without the instruction banner."""
    res = run_drawlib_cli(["rules", "show", "overview", "--raw"])
    assert res.returncode == 0
    assert "# Drawlib Agent Drawing Guidelines" in res.stdout
    assert "Instructions for AI Agents & Developers" not in res.stdout


def test_cli_rules_show_rebuild_and_clean() -> None:
    """Test `drawlib rules show --rebuild` caches output and `drawlib rules clean` removes it."""
    # Build on demand
    res_show = run_drawlib_cli(["rules", "show", "overview", "--rebuild"])
    assert res_show.returncode == 0
    assert "# Drawlib Agent Drawing Guidelines" in res_show.stdout
    assert "Instructions for AI Agents & Developers" in res_show.stdout

    # Clean cache
    res_clean = run_drawlib_cli(["rules", "clean"])
    assert res_clean.returncode == 0
    assert "Successfully cleaned" in res_clean.stdout


def test_cli_rules_build_specific_topic() -> None:
    """Test `drawlib rules build <topic>` pre-builds illustrations."""
    res_build = run_drawlib_cli(["rules", "build", "overview", "--force"])
    assert res_build.returncode == 0
    assert "Successfully compiled rule topic 'overview'" in res_build.stdout

    # Clean cache after test
    res_clean = run_drawlib_cli(["rules", "clean"])
    assert res_clean.returncode == 0


def test_cli_show_rules_fallback() -> None:
    """Test `drawlib show <topic>` seamlessly redirects to `drawlib rules show <topic>`."""
    res_canvas = run_drawlib_cli(["show", "canvas"])
    assert res_canvas.returncode == 0
    assert "# Drawlib Canvas Guidelines" in res_canvas.stdout

    res_tools = run_drawlib_cli(["show", "tools"])
    assert res_tools.returncode == 0
    assert "# Drawlib Tools Guidelines" in res_tools.stdout
