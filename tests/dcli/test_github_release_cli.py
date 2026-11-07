# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/github_release."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from tools.dcli.github_release import (
    app,
    extract_release_note,
    format_github_release_body,
    normalize_version_and_tag,
    parse_release_notes,
)
from tools.dcli.release_assets import GitHubReleaseClient

runner = CliRunner()

SAMPLE_NOTES = """# Release Notes & Migration Guide

## Version 0.3.2

*Release Date: 2026/10/30*

Version 0.3.2 introduces Office export.

---

### Highlights

- Added `.docx` and `.pptx`.

---

## Version 0.3.1

*Release Date: 2026/10/23*

Version 0.3.1 introduces heatmaps.

---

## Version 0.3.0

*Release Date: 2026/10/21*

Initial 0.3 architecture.

---

## Version 0.2.x Archive

- **v0.2.3**: Legacy release.
"""


def test_normalize_version_and_tag() -> None:
    """Test normalizing version and tag strings and rejecting 2-segment asset tags."""
    assert normalize_version_and_tag("0.3.6") == ("0.3.6", "v0.3.6")
    assert normalize_version_and_tag("v0.3.6") == ("0.3.6", "v0.3.6")
    assert normalize_version_and_tag("v0.4.0.rc1") == ("0.4.0.rc1", "v0.4.0.rc1")

    with pytest.raises(ValueError, match="Invalid release version"):
        normalize_version_and_tag("v0.3")


def test_parse_and_extract_release_notes(tmp_path: Path) -> None:
    """Test chronological parsing and trailing horizontal-rule cleanup."""
    notes_file = tmp_path / "release_notes.md"
    notes_file.write_text(SAMPLE_NOTES, encoding="utf-8")

    entries = parse_release_notes(notes_file)
    assert [e.version for e in entries] == ["0.3.0", "0.3.1", "0.3.2"]
    assert not entries[-1].body.endswith("---")
    assert "Added `.docx` and `.pptx`." in entries[-1].body

    entry_31 = extract_release_note("v0.3.1", notes_path=notes_file)
    assert entry_31.tag == "v0.3.1"
    formatted = format_github_release_body(entry_31)
    assert "https://pypi.org/project/drawlib/0.3.1/" in formatted


def test_cli_notes_preview(tmp_path: Path) -> None:
    """Test 'github-release notes' CLI command."""
    notes_file = tmp_path / "release_notes.md"
    notes_file.write_text(SAMPLE_NOTES, encoding="utf-8")

    result = runner.invoke(app, ["notes", "v0.3.2", "--notes-file", str(notes_file)])
    assert result.exit_code == 0
    assert "Added `.docx` and `.pptx`." in result.output


def test_cli_list_mocked(tmp_path: Path) -> None:
    """Test 'github-release list' CLI command with mocked GitHub API."""
    notes_file = tmp_path / "release_notes.md"
    notes_file.write_text(SAMPLE_NOTES, encoding="utf-8")

    fake_releases = [
        {"id": 10, "tag_name": "v0.3.2", "draft": False, "prerelease": False, "published_at": "2026-10-30T00:00:00Z"},
        {"id": 1, "tag_name": "v0.3", "draft": False, "prerelease": False, "published_at": "2026-09-20T00:00:00Z"},
    ]
    with patch.object(GitHubReleaseClient, "list_releases", return_value=fake_releases):
        result = runner.invoke(app, ["list", "--notes-file", str(notes_file), "--token", "dummy"])

    assert result.exit_code == 0
    assert "v0.3.2" in result.output
    assert "Latest" in result.output
    assert "Missing on GitHub" in result.output


def test_cli_create_idempotent_and_update(tmp_path: Path) -> None:
    """Test 'github-release create' creates missing, skips existing, and updates with --update."""
    notes_file = tmp_path / "release_notes.md"
    notes_file.write_text(SAMPLE_NOTES, encoding="utf-8")

    with (
        patch("tools.dcli.github_release.cli.resolve_commit_for_version", return_value=None),
        patch.object(GitHubReleaseClient, "get_release_by_tag", return_value=None),
        patch.object(GitHubReleaseClient, "create_release", return_value={"id": 99}) as mock_create,
    ):
        res_new = runner.invoke(app, ["create", "v0.3.2", "--notes-file", str(notes_file), "--token", "dummy"])
        assert res_new.exit_code == 0
        mock_create.assert_called_once()
        assert mock_create.call_args.kwargs["make_latest"] == "true"

    existing = {"id": 99, "tag_name": "v0.3.2"}
    with (
        patch("tools.dcli.github_release.cli.resolve_commit_for_version", return_value=None),
        patch.object(GitHubReleaseClient, "get_release_by_tag", return_value=existing),
        patch.object(GitHubReleaseClient, "create_release") as mock_create2,
        patch.object(GitHubReleaseClient, "update_release", return_value=existing) as mock_update,
    ):
        res_skip = runner.invoke(app, ["create", "v0.3.2", "--notes-file", str(notes_file), "--token", "dummy"])
        assert res_skip.exit_code == 0
        assert "Skipped v0.3.2" in res_skip.output
        mock_create2.assert_not_called()
        mock_update.assert_not_called()

        res_upd = runner.invoke(
            app, ["create", "v0.3.2", "--update", "--notes-file", str(notes_file), "--token", "dummy"]
        )
        assert res_upd.exit_code == 0
        mock_update.assert_called_once()


def test_cli_sync_backfill_order_and_latest_flag(tmp_path: Path) -> None:
    """Test 'github-release sync' creates releases chronologically and sets Latest only on highest version."""
    notes_file = tmp_path / "release_notes.md"
    notes_file.write_text(SAMPLE_NOTES, encoding="utf-8")

    with (
        patch("tools.dcli.github_release.cli.resolve_commit_for_version", side_effect=[None, "deadbeef1234", None]),
        patch.object(GitHubReleaseClient, "list_releases", return_value=[]),
        patch.object(GitHubReleaseClient, "create_release", return_value={"id": 1}) as mock_create,
    ):
        result = runner.invoke(app, ["sync", "--notes-file", str(notes_file), "--token", "dummy"])

    assert result.exit_code == 0
    calls = mock_create.call_args_list
    assert [c.kwargs["tag"] for c in calls] == ["v0.3.0", "v0.3.1", "v0.3.2"]
    assert [c.kwargs["make_latest"] for c in calls] == ["false", "false", "true"]
    assert calls[1].kwargs["target_commitish"] == "deadbeef1234"
