# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/assets.py and tools/scripts/release_assets_tool.py."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from drawlib._release_assets import (
    RELEASE_ASSET_PACKAGES,
    AssetManifest,
    AssetManifestItem,
    ReleaseAssetPackageName,
)
from tools.dcli.assets import _resolve_tag, app
from tools.scripts.release_assets_tool import (
    GitHubReleaseClient,
    build_package_zip,
    resolve_github_token,
)

runner = CliRunner()


def test_resolve_tag() -> None:
    """Test release tag resolution."""
    assert _resolve_tag("v1.0") == "v1.0"
    default_tag = _resolve_tag(None)
    assert default_tag.startswith("v")
    assert "." in default_tag


def test_resolve_github_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test token resolution precedence."""
    assert resolve_github_token("explicit_token") == "explicit_token"

    monkeypatch.setenv("GITHUB_TOKEN", "env_github_token")
    assert resolve_github_token(None) == "env_github_token"

    monkeypatch.delenv("GITHUB_TOKEN")
    monkeypatch.setenv("GH_TOKEN", "env_gh_token")
    assert resolve_github_token(None) == "env_gh_token"


def test_build_package_zip() -> None:
    """Test building deterministic zip binary."""
    root = Path(__file__).resolve().parent.parent
    assets_dir = root / "release_assets" / "v0.3"
    if not assets_dir.exists():
        pytest.skip("release_assets/v0.3 not found.")

    pkg = RELEASE_ASSET_PACKAGES.font_roboto
    zip_bytes = build_package_zip(pkg, assets_dir)
    assert len(zip_bytes) > 0
    calculated_sha = hashlib.sha256(zip_bytes).hexdigest()
    assert calculated_sha == pkg.archive_sha256


def test_cli_assets_list() -> None:
    """Test 'assets list' CLI command."""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "font_roboto" in result.output
    assert "icon_phosphor" in result.output


def test_cli_assets_build_single(tmp_path: Path) -> None:
    """Test 'assets build font_roboto' command."""
    result = runner.invoke(app, ["build", "font_roboto", "--output-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "Built font_roboto.zip" in result.output
    tag = _resolve_tag(None)
    zip_path = tmp_path / tag / "font_roboto.zip"
    assert zip_path.is_file()
    assert hashlib.sha256(zip_path.read_bytes()).hexdigest() == RELEASE_ASSET_PACKAGES.font_roboto.archive_sha256


def test_cli_assets_upload_dry_run() -> None:
    """Test 'assets upload' in dry-run mode."""
    result = runner.invoke(app, ["upload", "font_roboto", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY-RUN" in result.output
    assert "font_roboto.zip" in result.output


def test_cli_assets_remove_dry_run() -> None:
    """Test 'assets remove' in dry-run mode."""
    result = runner.invoke(app, ["remove", "font_roboto", "--dry-run"])
    assert result.exit_code == 0
    assert "DRY-RUN" in result.output


def test_github_release_client_unit() -> None:
    """Unit test GitHubReleaseClient methods with mocked urllib."""
    client = GitHubReleaseClient(owner="owner", repo="repo", token="fake_token")  # noqa: S106

    # Mock get_release_by_tag
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"id": 101, "tag_name": "v0.3", "assets": []}).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        rel = client.get_release_by_tag("v0.3")
        assert rel is not None
        assert rel["id"] == 101

    # Mock upload_asset
    upload_resp = MagicMock()
    upload_resp.read.return_value = json.dumps({"id": 202, "name": "test.zip", "size": 100}).encode("utf-8")
    upload_resp.__enter__.return_value = upload_resp

    with patch("urllib.request.urlopen", return_value=upload_resp):
        asset = client.upload_asset(101, "test.zip", b"dummy")
        assert asset["id"] == 202


def test_cli_assets_remote_mocked() -> None:
    """Test 'assets remote' command with mocked GitHub response."""
    manifest = AssetManifest(
        version="v0.3",
        assets={
            "font_roboto.zip": AssetManifestItem(
                archive_name="font_roboto.zip",
                sha256=RELEASE_ASSET_PACKAGES.font_roboto.archive_sha256,
                size=12345,
            )
        },
    )

    fake_release = {
        "id": 101,
        "tag_name": "v0.3",
        "assets": [
            {"id": 1, "name": "font_roboto.zip", "size": 12345},
            {"id": 2, "name": "asset_manifest.json", "browser_download_url": "https://example.com/manifest.json"},
        ],
    }

    with (
        patch.object(GitHubReleaseClient, "get_release_by_tag", return_value=fake_release),
        patch.object(GitHubReleaseClient, "get_remote_manifest", return_value=manifest),
    ):
        result = runner.invoke(app, ["remote"])
        assert result.exit_code == 0
        assert "font_roboto" in result.output
        assert "Synchronized" in result.output


def test_cli_assets_sync_check() -> None:
    """Test 'assets sync --check' passes on current release assets."""
    result = runner.invoke(app, ["sync", "--check"])
    assert result.exit_code == 0
    assert "is up-to-date and in sync" in result.output
