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

from tests.drawlib.cli.common import run_drawlib_cli


def test_cli_rules_default() -> None:
    """Test `drawlib rules` without arguments outputs help message."""
    res = run_drawlib_cli(["rules"])
    assert res.returncode != 0
    assert "Usage:" in res.stdout or "Usage:" in res.stderr
    assert "rules [OPTIONS] COMMAND" in (res.stdout + res.stderr)
    assert "show" in (res.stdout + res.stderr)
    assert "list" in (res.stdout + res.stderr)


def test_cli_rules_show_missing_topic() -> None:
    """Test `drawlib rules show` without topic fails with missing argument error."""
    res = run_drawlib_cli(["rules", "show"])
    assert res.returncode != 0
    assert "Missing argument" in (res.stdout + res.stderr)
    assert "topic" in (res.stdout + res.stderr).lower()


def test_cli_rules_list() -> None:
    """Test `drawlib rules list` lists all general guidelines and library modules."""
    res = run_drawlib_cli(["rules", "list"])
    assert res.returncode == 0
    assert "General Guidelines:" in res.stdout
    assert "Library Modules (drawlib.*):" in res.stdout
    for topic in [
        "agent-instruction",
        "overview",
        "style-guide",
        "anim-guide",
        "project",
        "cli",
        "api",
        "lib-canvas",
        "lib-anim",
        "lib-shapes",
        "lib-lines",
        "lib-text",
        "lib-preset-colors",
        "lib-styles",
        "lib-preset-styles",
        "lib-fonts",
        "lib-images",
        "lib-icons",
        "lib-math",
        "lib-types",
        "lib-smartarts",
        "lib-charts",
        "lib-diagrams",
        "lib-graph",
        "lib-tools",
        "lib-slide",
    ]:
        assert topic in res.stdout


@pytest.mark.parametrize(
    "topic,expected_heading",
    [
        ("agent-instruction", "# Drawlib AI Agent Instructions"),
        ("overview", "# Drawlib Agent Drawing Guidelines"),
        ("style-guide", "# Drawlib Diagram Style Guide & Aesthetic Philosophy"),
        ("anim-guide", "# Drawlib Animation Design & Best Practices Guide"),
        ("project", "# Drawlib Project Architecture & Scaffolding Guidelines"),
        ("cli", "# Drawlib CLI Guidelines"),
        ("api", "# Drawlib API Reference & Cheat Sheet"),
        ("lib-canvas", "# Drawlib Canvas Guidelines"),
        ("lib-anim", "# Drawlib Animation Guidelines"),
        ("lib-shapes", "# Drawlib Shapes Guidelines"),
        ("lib-lines", "# Drawlib Lines Guidelines"),
        ("lib-text", "# Drawlib Text Guidelines"),
        ("lib-preset-colors", "# Drawlib Preset Colors Guidelines"),
        ("lib-styles", "# Drawlib Styles & Utilities Architecture Guidelines"),
        ("lib-preset-styles", "# Drawlib Preset Styles Guidelines"),
        ("lib-fonts", "# Drawlib Fonts Guidelines"),
        ("lib-images", "# Drawlib Images Guidelines"),
        ("lib-icons", "# Drawlib Icons Guidelines"),
        ("lib-math", "# Drawlib Math Guidelines"),
        ("lib-types", "# Drawlib Types & Style Models Guidelines"),
        ("lib-smartarts", "# Drawlib SmartArts Guidelines"),
        ("lib-charts", "# Drawlib Charts Guidelines"),
        ("lib-diagrams", "# Drawlib Diagrams Guidelines"),
        ("lib-graph", "# Drawlib Graph Guidelines"),
        ("lib-tools", "# Drawlib Tools Guidelines"),
        ("lib-slide", "# Drawlib Slide Presentation & Stage Guidelines"),
    ],
)
def test_cli_rules_show_topics(topic: str, expected_heading: str) -> None:
    """Test `drawlib rules show <topic>` for each supported topic."""
    res = run_drawlib_cli(["rules", "show", topic])
    assert res.returncode == 0
    assert expected_heading in res.stdout


def test_cli_rules_show_underscore_normalization() -> None:
    """Test `drawlib rules show` transparently accepts underscore-style topic names."""
    res = run_drawlib_cli(["rules", "show", "lib_shapes"])
    assert res.returncode == 0
    assert "# Drawlib Shapes Guidelines" in res.stdout

    res_agent = run_drawlib_cli(["rules", "show", "agent_instruction"])
    assert res_agent.returncode == 0
    assert "# Drawlib AI Agent Instructions" in res_agent.stdout

    res_style = run_drawlib_cli(["rules", "show", "style_guide"])
    assert res_style.returncode == 0
    assert "# Drawlib Diagram Style Guide & Aesthetic Philosophy" in res_style.stdout

    res_anim = run_drawlib_cli(["rules", "show", "anim_guide"])
    assert res_anim.returncode == 0
    assert "# Drawlib Animation Design & Best Practices Guide" in res_anim.stdout


@pytest.mark.parametrize(
    "deprecated_topic",
    [
        "shapes",
        "lines",
        "canvas",
        "themes",
        "theme",
        "docs",
        "doc",
        "preset_styles",
        "overview-min",
        "overview_min",
        "docs-build",
        "docs_build",
    ],
)
def test_cli_rules_show_deprecated_topics_rejected(deprecated_topic: str) -> None:
    """Test that legacy or un-prefixed topics are strictly rejected with code 1."""
    res = run_drawlib_cli(["rules", "show", deprecated_topic])
    assert res.returncode == 1
    assert f"Error: Unknown rule topic '{deprecated_topic}'" in res.stderr
    assert "Available topics:" in res.stderr


def test_cli_rules_show_unknown_topic() -> None:
    """Test `drawlib rules show unknown` exits with code 1 and prints available topics."""
    res = run_drawlib_cli(["rules", "show", "unknown_topic"])
    assert res.returncode == 1
    assert "Error: Unknown rule topic 'unknown_topic'" in res.stderr
    assert "Available topics:" in res.stderr


def test_cli_rules_show_raw() -> None:
    """Test `drawlib rules show --raw` returns raw markdown without building illustrations."""
    res = run_drawlib_cli(["rules", "show", "overview", "--raw"])
    assert res.returncode == 0
    assert "# Drawlib Agent Drawing Guidelines" in res.stdout
    assert "PYTHON_RUNTIME/site-packages/drawlib/_cached_assets/rules/overview_images" not in res.stdout


def test_cli_rules_show_rebuild_and_clear() -> None:
    """Test `drawlib rules show --rebuild` caches output and `drawlib rules clear` removes it."""
    # Build on demand
    res_show = run_drawlib_cli(["rules", "show", "overview", "--rebuild"])
    assert res_show.returncode == 0
    assert "# Drawlib Agent Drawing Guidelines" in res_show.stdout
    assert "PYTHON_RUNTIME/site-packages/drawlib/_cached_assets/rules/overview_images" in res_show.stdout

    # Clear cache
    res_clear = run_drawlib_cli(["rules", "clear"])
    assert res_clear.returncode == 0
    assert "Successfully cleared" in res_clear.stdout

    # Verify deprecated 'clean' is rejected
    res_clean = run_drawlib_cli(["rules", "clean"])
    assert res_clean.returncode != 0


def test_cli_rules_build_specific_topic() -> None:
    """Test `drawlib rules build <topic>` pre-builds illustrations."""
    res_build = run_drawlib_cli(["rules", "build", "lib-shapes", "--force"])
    assert res_build.returncode == 0
    assert "Successfully compiled rule topic 'lib-shapes'" in res_build.stdout

    # Clear cache after test
    res_clear = run_drawlib_cli(["rules", "clear"])
    assert res_clear.returncode == 0


def test_cli_show_rules_fallback() -> None:
    """Test `drawlib show <topic>` seamlessly redirects to `drawlib rules show <topic>`."""
    res_canvas = run_drawlib_cli(["show", "lib-canvas"])
    assert res_canvas.returncode == 0
    assert "# Drawlib Canvas Guidelines" in res_canvas.stdout

    res_tools = run_drawlib_cli(["show", "lib-tools"])
    assert res_tools.returncode == 0
    assert "# Drawlib Tools Guidelines" in res_tools.stdout


@pytest.mark.parametrize(
    "cmd_args",
    [
        ["--help"],
        ["init", "--help"],
        ["serve", "--help"],
        ["show", "--help"],
        ["build", "--help"],
        ["build", "image", "--help"],
        ["build", "markdown", "--help"],
        ["build", "html", "--help"],
        ["build", "pdf", "--help"],
        ["cache", "--help"],
        ["cache", "clear", "--help"],
        ["cache", "list", "--help"],
        ["cache", "download", "--help"],
        ["colors", "--help"],
        ["colors", "list", "--help"],
        ["colors", "show", "--help"],
        ["css", "--help"],
        ["css", "list", "--help"],
        ["css", "show", "--help"],
        ["rules", "--help"],
        ["rules", "show", "--help"],
        ["rules", "build", "--help"],
        ["rules", "clear", "--help"],
        ["rules", "list", "--help"],
        ["styles", "--help"],
        ["styles", "list", "--help"],
        ["styles", "show", "--help"],
    ],
)
def test_cli_help_shows_ai_instructions(cmd_args: list[str]) -> None:
    """Test that all CLI commands display the AI Instructions epilog in their help text."""
    res = run_drawlib_cli(cmd_args)
    assert res.returncode == 0
    assert "AI Instructions:" in res.stdout
    assert "drawlib rules show agent-instruction" in res.stdout
    assert "drawlib rules show cli" in res.stdout
    assert "drawlib rules show overview" in res.stdout
    assert "drawlib rules list" in res.stdout
