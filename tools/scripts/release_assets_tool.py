# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GitHub Releases REST API asset management tool for drawlib.

Provides low-level and high-level interfaces for building, uploading, verifying,
and deleting release asset packages using the official GitHub REST API.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from drawlib._release_assets import (
    DEFAULT_RELEASE_TAG,
    AssetManifest,
    ReleaseAssetPackage,
    create_deterministic_zip_bytes,
)

MANIFEST_FILE_NAME = "asset_manifest.json"


def resolve_github_token(explicit_token: str | None = None) -> str | None:
    """Resolve GitHub Personal Access Token from arguments, environment, or .env file.

    Args:
        explicit_token: Explicitly provided token string.

    Returns:
        str | None: The resolved token or None if not found.
    """
    if explicit_token:
        return explicit_token

    if "GITHUB_TOKEN" in os.environ:
        return os.environ["GITHUB_TOKEN"]
    if "GH_TOKEN" in os.environ:
        return os.environ["GH_TOKEN"]

    # Check .env file in workspace root
    env_file = Path(".env")
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("\"'")
            if key in {"GITHUB_TOKEN", "GH_TOKEN"}:
                return val

    # Fallback to system git credential helper (macOS Keychain, Linux, Windows)
    return _resolve_token_from_git()


def _resolve_token_from_git() -> str | None:
    """Retrieve GitHub token from system git credential helper."""
    import subprocess  # noqa: PLC0415

    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n",
            text=True,
            capture_output=True,
            check=True,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1]
    except Exception:
        return None
    return None


class GitHubReleaseClient:
    """REST API client for managing GitHub Releases and binary assets."""

    def __init__(self, owner: str = "yuichi110", repo: str = "drawlib", token: str | None = None) -> None:
        """Initialize client with repository credentials.

        Args:
            owner: Repository owner on GitHub. Defaults to 'yuichi110'.
            repo: Repository name on GitHub. Defaults to 'drawlib'.
            token: GitHub personal access token with repo scope.
        """
        self.owner = owner
        self.repo = repo
        self.token = token
        self.api_base = f"https://api.github.com/repos/{owner}/{repo}"
        self.uploads_base = f"https://uploads.github.com/repos/{owner}/{repo}"

    def _headers(
        self,
        content_type: str = "application/vnd.github+json",
        accept: str = "application/vnd.github+json",
    ) -> dict[str, str]:
        """Construct standard HTTP headers for GitHub API requests.

        Args:
            content_type: Content-Type header string.
            accept: Accept header string.

        Returns:
            dict[str, str]: Prepared HTTP headers.
        """
        headers = {
            "Accept": accept,
            "User-Agent": "drawlib-dcli",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def get_release_by_tag(self, tag: str) -> dict[str, Any] | None:
        """Fetch release metadata by its git tag name.

        Args:
            tag: Git tag string, e.g. 'v0.3'.

        Returns:
            dict[str, Any] | None: Release JSON dictionary if found, otherwise None.

        Raises:
            urllib.error.HTTPError: On non-404 HTTP errors.
        """
        url = f"{self.api_base}/releases/tags/{tag}"
        req = urllib.request.Request(url, headers=self._headers(), method="GET")
        try:
            with urllib.request.urlopen(req) as resp:
                data: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
                return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise

    def create_release(
        self,
        tag: str,
        name: str | None = None,
        body: str | None = None,
        draft: bool = False,
        prerelease: bool = False,
    ) -> dict[str, Any]:
        """Create a new release for the given tag.

        Args:
            tag: Git tag name, e.g. 'v0.3'.
            name: Release title, defaults to tag.
            body: Release description body.
            draft: Whether to create as a draft release.
            prerelease: Whether to create as a pre-release.

        Returns:
            dict[str, Any]: Newly created release dictionary.
        """
        url = f"{self.api_base}/releases"
        payload = {
            "tag_name": tag,
            "name": name or tag,
            "body": body or f"Drawlib release assets for {tag}",
            "draft": draft,
            "prerelease": prerelease,
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers=self._headers("application/json"),
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            res: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
            return res

    def get_or_create_release(self, tag: str = DEFAULT_RELEASE_TAG) -> dict[str, Any]:
        """Retrieve existing release by tag, or create it if not found.

        Args:
            tag: Git tag name. Defaults to DEFAULT_RELEASE_TAG.

        Returns:
            dict[str, Any]: Release dictionary.
        """
        rel = self.get_release_by_tag(tag)
        if rel is not None:
            return rel
        return self.create_release(tag=tag)

    def delete_asset(self, asset_id: int) -> None:
        """Delete an existing release asset by its ID.

        Args:
            asset_id: GitHub numeric asset identifier.
        """
        url = f"{self.api_base}/releases/assets/{asset_id}"
        req = urllib.request.Request(url, headers=self._headers(), method="DELETE")
        with urllib.request.urlopen(req):
            pass

    def upload_asset(
        self,
        release_id: int,
        filename: str,
        data: bytes,
        content_type: str = "application/zip",
    ) -> dict[str, Any]:
        """Upload a binary asset file to a release.

        Args:
            release_id: Target release numeric ID.
            filename: Asset file name, e.g. 'font_roboto.zip'.
            data: Binary payload of the asset.
            content_type: MIME content type string.

        Returns:
            dict[str, Any]: Uploaded asset metadata dictionary.
        """
        query = urllib.parse.urlencode({"name": filename})
        url = f"{self.uploads_base}/releases/{release_id}/assets?{query}"
        headers = self._headers(content_type=content_type)
        headers["Content-Length"] = str(len(data))
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as resp:
            res: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
            return res

    def get_remote_manifest(self, release: dict[str, Any]) -> AssetManifest | None:
        """Download and parse remote asset_manifest.json if attached to the release.

        Args:
            release: Release dictionary containing assets list.

        Returns:
            AssetManifest | None: Parsed manifest or None if not uploaded.
        """
        assets = release.get("assets", [])
        manifest_asset = next((a for a in assets if a.get("name") == MANIFEST_FILE_NAME), None)
        if not manifest_asset:
            return None

        asset_id = manifest_asset.get("id")
        if asset_id is not None:
            url = f"{self.api_base}/releases/assets/{asset_id}"
            headers = self._headers(accept="application/octet-stream")
        else:
            download_url = manifest_asset.get("browser_download_url")
            if not download_url:
                return None
            url = download_url
            headers = {"User-Agent": "drawlib-dcli"}

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return AssetManifest.model_validate(data)
        except Exception:
            return None

    def upload_manifest(self, release: dict[str, Any], manifest: AssetManifest) -> dict[str, Any]:
        """Upload or update asset_manifest.json on the target release.

        Args:
            release: Release dictionary.
            manifest: AssetManifest model to serialize and upload.

        Returns:
            dict[str, Any]: Uploaded asset dictionary.
        """
        release_id = release["id"]
        # Delete old manifest asset if present
        for asset in release.get("assets", []):
            if asset.get("name") == MANIFEST_FILE_NAME:
                self.delete_asset(asset["id"])
                break

        data_bytes = manifest.model_dump_json(indent=2).encode("utf-8")
        return self.upload_asset(
            release_id=release_id,
            filename=MANIFEST_FILE_NAME,
            data=data_bytes,
            content_type="application/json",
        )


def build_package_zip(pkg: ReleaseAssetPackage, assets_root: Path) -> bytes:
    """Build byte-reproducible ZIP archive for a release asset package.

    Args:
        pkg: Release asset package definition.
        assets_root: Root directory of release assets, e.g. release_assets/v0.3.

    Returns:
        bytes: Binary ZIP data.
    """
    src_dir = assets_root / pkg.source_rel_path
    return create_deterministic_zip_bytes(src_dir, pkg.files)
