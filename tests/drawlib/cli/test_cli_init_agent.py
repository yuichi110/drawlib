# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and CLI integration tests for `drawlib init agent` and `drawlib.tools` agent helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from drawlib.tools import (
    detect_agent_targets,
    get_agent_instruction,
    init_agent_instruction,
    list_agent_targets,
)
from tests.drawlib.cli.common import run_drawlib_cli


def test_cli_init_agent_list_and_no_args(tmp_path: Path) -> None:
    """Verify `drawlib init agent list`, `--list`, and zero-arg help output."""
    res_pos = run_drawlib_cli(["init", "agent", "list"], cwd=str(tmp_path))
    assert res_pos.returncode == 0
    for expected in ("antigravity", "claude", "cursor", "copilot", "windsurf", "cline", "roo", "codex", "gemini"):
        assert expected in res_pos.stdout

    res_flag = run_drawlib_cli(["init", "agent", "--list"], cwd=str(tmp_path))
    assert res_flag.returncode == 0
    assert res_flag.stdout == res_pos.stdout

    res_empty = run_drawlib_cli(["init", "agent"], cwd=str(tmp_path))
    assert res_empty.returncode == 0
    assert "Usage:" in res_empty.stdout
    assert "drawlib init agent list" in res_empty.stdout


def test_agent_instruction_size_under_windsurf_limit() -> None:
    """Ensure every rendered agent instruction stays well below Windsurf's 12,000-character limit."""
    targets = [item["name"] for item in list_agent_targets()]
    assert len(targets) == 9

    for name in targets:
        for mode in ("auto", "always"):
            rendered = get_agent_instruction(name, mode=mode)
            assert "# Drawlib AI Agent Instructions" in rendered
            assert len(rendered) < 10_600, f"{name} ({mode}) exceeded compact character budget: {len(rendered)}"


def test_repo_antigravity_rule_is_synced() -> None:
    """Verify repository `.agents/rules/drawlib.md` matches `get_agent_instruction('antigravity', 'always')`."""
    repo_rule = Path(__file__).resolve().parents[3] / ".agents" / "rules" / "drawlib.md"
    expected = get_agent_instruction("antigravity", mode="always")
    assert repo_rule.read_text(encoding="utf-8") == expected


def test_antigravity_smart_directory_selection_and_modes(tmp_path: Path) -> None:
    """Verify `.agents/` default, `.agent/` legacy fallback, and `auto` vs `always` YAML frontmatter."""
    # 1. Fresh repo -> .agents/rules/drawlib.md with default mode=auto (model_decision)
    res_auto = run_drawlib_cli(["init", "agent", "antigravity"], cwd=str(tmp_path))
    assert res_auto.returncode == 0
    plural_rule = tmp_path / ".agents" / "rules" / "drawlib.md"
    assert plural_rule.is_file()
    content_auto = plural_rule.read_text(encoding="utf-8")
    assert content_auto.startswith("---\ntrigger: model_decision\ndescription: ")

    # Overwrite with --mode always --force
    res_always = run_drawlib_cli(["init", "agent", "antigravity", "-m", "always", "-f"], cwd=str(tmp_path))
    assert res_always.returncode == 0
    content_always = plural_rule.read_text(encoding="utf-8")
    assert content_always.startswith("---\ntrigger: always_on\n---\n\n# Drawlib AI Agent Instructions")

    # 2. Repo with existing singular `.agent/` directory (and no `.agents/`) -> .agent/rules/drawlib.md
    legacy_repo = tmp_path / "legacy_ws"
    (legacy_repo / ".agent").mkdir(parents=True)
    res_legacy = run_drawlib_cli(["init", "agent", "antigravity"], cwd=str(legacy_repo))
    assert res_legacy.returncode == 0
    assert (legacy_repo / ".agent" / "rules" / "drawlib.md").is_file()
    assert not (legacy_repo / ".agents").exists()


def test_frontmatter_formats_for_cursor_copilot_windsurf_and_plain_targets(tmp_path: Path) -> None:
    """Verify tool-specific frontmatter schemas across Cursor, Copilot, Windsurf, Claude, Cline, and Roo."""
    res = run_drawlib_cli(
        ["init", "agent", "claude", "cursor", "copilot", "windsurf", "cline", "roo"],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0

    claude_md = (tmp_path / ".claude" / "rules" / "drawlib.md").read_text(encoding="utf-8")
    assert claude_md.startswith("# Drawlib AI Agent Instructions")

    cursor_auto = (tmp_path / ".cursor" / "rules" / "drawlib.mdc").read_text(encoding="utf-8")
    assert "alwaysApply: false" in cursor_auto
    assert 'description: "' in cursor_auto

    copilot_auto = (tmp_path / ".github" / "instructions" / "drawlib.instructions.md").read_text(encoding="utf-8")
    assert 'applyTo: "**/*_src/**, **/*.md, **/*.py, **/drawlib.toml"' in copilot_auto

    windsurf_auto = (tmp_path / ".windsurf" / "rules" / "drawlib.md").read_text(encoding="utf-8")
    assert windsurf_auto.startswith("---\ntrigger: model_decision\ndescription: ")

    assert (tmp_path / ".clinerules" / "drawlib.md").read_text(encoding="utf-8").startswith("# Drawlib")
    assert (tmp_path / ".roo" / "rules" / "drawlib.md").read_text(encoding="utf-8").startswith("# Drawlib")

    # Check --mode always variants for Cursor and Copilot
    run_drawlib_cli(["init", "agent", "cursor,copilot", "--mode", "always", "--force"], cwd=str(tmp_path))
    cursor_always = (tmp_path / ".cursor" / "rules" / "drawlib.mdc").read_text(encoding="utf-8")
    assert "alwaysApply: true" in cursor_always
    copilot_always = (tmp_path / ".github" / "instructions" / "drawlib.instructions.md").read_text(encoding="utf-8")
    assert 'applyTo: "**"' in copilot_always


def test_shared_file_marker_merge_and_force_update(tmp_path: Path) -> None:
    """Verify non-destructive append and idempotent marker-block replacement on AGENTS.md and GEMINI.md."""
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# Team Repository Rules\n\nAlways run pytest before committing.\n", encoding="utf-8")

    # Appends without requiring --force when markers are not yet present
    res_append = run_drawlib_cli(["init", "agent", "codex"], cwd=str(tmp_path))
    assert res_append.returncode == 0
    merged = agents_md.read_text(encoding="utf-8")
    assert merged.startswith("# Team Repository Rules\n\nAlways run pytest before committing.\n\n")
    assert "<!-- drawlib-agent-instruction:start -->" in merged
    assert "<!-- drawlib-agent-instruction:end -->" in merged

    # Append custom footer after Drawlib block to verify in-place replacement preserves both ends
    agents_md.write_text(merged + "\n## Footer Section\nKeep this intact.\n", encoding="utf-8")

    # Second run without --force is rejected
    res_dup = run_drawlib_cli(["init", "agent", "agents-md"], cwd=str(tmp_path))
    assert res_dup.returncode == 1
    assert "already exist" in res_dup.stderr

    # Corrupt content inside markers, then --force restores clean Drawlib block while preserving header & footer
    tampered = agents_md.read_text(encoding="utf-8").replace(
        "# Drawlib AI Agent Instructions",
        "# OUTDATED DRAWLIB BLOCK",
    )
    agents_md.write_text(tampered, encoding="utf-8")

    res_force = run_drawlib_cli(["init", "agent", "codex", "--force"], cwd=str(tmp_path))
    assert res_force.returncode == 0
    restored = agents_md.read_text(encoding="utf-8")
    assert "# OUTDATED DRAWLIB BLOCK" not in restored
    assert "# Drawlib AI Agent Instructions" in restored
    assert restored.startswith("# Team Repository Rules\n\nAlways run pytest before committing.\n\n")
    assert restored.endswith("\n## Footer Section\nKeep this intact.\n")


def test_init_agent_all_and_atomic_conflict_guard(tmp_path: Path) -> None:
    """Verify `all` creates modular rule files only and multi-agent conflict fails atomically."""
    # Pre-create conflicting .cursor/rules/drawlib.mdc -> multi-agent init must not write .claude/rules/drawlib.md
    cursor_file = tmp_path / ".cursor" / "rules" / "drawlib.mdc"
    cursor_file.parent.mkdir(parents=True)
    cursor_file.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError):
        init_agent_instruction(["claude", "cursor"], destination=tmp_path, force=False)
    assert not (tmp_path / ".claude" / "rules" / "drawlib.md").exists()

    # Clean workspace: `drawlib init agents all` (plural alias) creates all 7 modular files, not AGENTS.md/GEMINI.md
    clean_ws = tmp_path / "clean"
    clean_ws.mkdir()
    res_all = run_drawlib_cli(["init", "agents", "all"], cwd=str(clean_ws))
    assert res_all.returncode == 0
    assert (clean_ws / ".agents" / "rules" / "drawlib.md").is_file()
    assert (clean_ws / ".claude" / "rules" / "drawlib.md").is_file()
    assert (clean_ws / ".cursor" / "rules" / "drawlib.mdc").is_file()
    assert (clean_ws / ".github" / "instructions" / "drawlib.instructions.md").is_file()
    assert (clean_ws / ".windsurf" / "rules" / "drawlib.md").is_file()
    assert (clean_ws / ".clinerules" / "drawlib.md").is_file()
    assert (clean_ws / ".roo" / "rules" / "drawlib.md").is_file()
    assert not (clean_ws / "AGENTS.md").exists()
    assert not (clean_ws / "GEMINI.md").exists()


def test_detect_agent_targets_and_cli_detect(tmp_path: Path) -> None:
    """Verify `--detect` finds configured agents while ignoring unrelated `.github/workflows`."""
    # Empty repo + unrelated .github/workflows -> nothing detected
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    assert detect_agent_targets(tmp_path) == []

    res_none = run_drawlib_cli(["init", "agent", "--detect"], cwd=str(tmp_path))
    assert res_none.returncode == 1
    assert "No existing AI agent configuration" in res_none.stderr

    # Add .claude/, .github/copilot-instructions.md, and GEMINI.md
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".github" / "copilot-instructions.md").write_text("# Copilot\n", encoding="utf-8")
    (tmp_path / "GEMINI.md").write_text("# Local Gemini Context\n", encoding="utf-8")

    detected = detect_agent_targets(tmp_path)
    assert detected == ["claude", "copilot", "gemini"]

    res_ok = run_drawlib_cli(["init", "agent", "--detect"], cwd=str(tmp_path))
    assert res_ok.returncode == 0
    assert (tmp_path / ".claude" / "rules" / "drawlib.md").is_file()
    assert (tmp_path / ".github" / "instructions" / "drawlib.instructions.md").is_file()
    assert "<!-- drawlib-agent-instruction:start -->" in (tmp_path / "GEMINI.md").read_text(encoding="utf-8")


def test_global_scope_and_error_cases(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify `--global` writes to user home paths and rejects unsupported/conflicting options."""
    fake_home = tmp_path / "fake_home"
    fake_home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    res_global = run_drawlib_cli(
        ["init", "agent", "antigravity", "claude", "windsurf", "codex", "gemini", "--global"],
        cwd=str(tmp_path),
    )
    assert res_global.returncode == 0
    assert (fake_home / ".gemini" / "config" / "rules" / "drawlib.md").is_file()
    assert (fake_home / ".claude" / "rules" / "drawlib.md").is_file()
    windsurf_global = (fake_home / ".codeium" / "windsurf" / "memories" / "global_rules.md").read_text(encoding="utf-8")
    assert windsurf_global.startswith("<!-- drawlib-agent-instruction:start -->")
    assert (fake_home / ".codex" / "AGENTS.md").is_file()
    assert (fake_home / ".gemini" / "GEMINI.md").is_file()

    # Cursor and Copilot do not have file-based global rules
    res_cursor_global = run_drawlib_cli(["init", "agent", "cursor", "--global"], cwd=str(tmp_path))
    assert res_cursor_global.returncode == 1
    assert "not supported for 'cursor'" in res_cursor_global.stderr

    # --detect + --global conflict
    res_conflict = run_drawlib_cli(["init", "agent", "--detect", "--global"], cwd=str(tmp_path))
    assert res_conflict.returncode == 1

    # Custom -o output works for 1 agent, fails for multiple agents
    custom_out = tmp_path / "custom" / "my_rule.md"
    res_out = run_drawlib_cli(["init", "agent", "antigravity", "-o", str(custom_out)], cwd=str(tmp_path))
    assert res_out.returncode == 0
    assert custom_out.is_file()

    res_multi_out = run_drawlib_cli(["init", "agent", "claude", "cursor", "-o", str(custom_out)], cwd=str(tmp_path))
    assert res_multi_out.returncode == 1

    # Legacy .clinerules regular file blocking .clinerules/drawlib.md directory creation
    (tmp_path / ".clinerules").write_text("legacy file", encoding="utf-8")
    res_cline_err = run_drawlib_cli(["init", "agent", "cline"], cwd=str(tmp_path))
    assert res_cline_err.returncode == 1
    assert "already exists as a file" in res_cline_err.stderr
