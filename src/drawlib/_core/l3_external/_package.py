# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Release asset package data models and download/extraction execution logic."""

from __future__ import annotations

import hashlib
import io
import urllib.request
import zipfile
from collections.abc import Iterator
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from drawlib._core.l1_core._const import ASSETS_DIR_PATH


class ReleaseAssetPackage(BaseModel):
    """Data model representing a downloadable release asset package.

    Attributes:
        name: Unique package identifier, e.g. 'font_roboto'.
        category: Category of the asset package ('font' or 'icon').
        archive_name: ZIP archive file name, e.g. 'font_roboto.zip'.
        archive_sha256: SHA-256 hex digest of the ZIP archive file.
        source_rel_path: Relative path within release_assets/<ver>/, e.g. 'fonts/roboto'.
        target_rel_path: Relative path where the asset is extracted locally.
        files: List of file names contained within this asset package.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(description="Unique package identifier, e.g. 'font_roboto'.")
    category: Literal["font", "icon", "map"] = Field(
        description="Category of the asset package ('font', 'icon', or 'map').",
    )
    archive_name: str = Field(description="ZIP archive file name, e.g. 'font_roboto.zip'.")
    archive_sha256: str = Field(description="SHA-256 hex digest of the ZIP archive file.")
    source_rel_path: str = Field(
        description="Relative path within release_assets/<ver>/, e.g. 'fonts/roboto'.",
    )
    target_rel_path: str = Field(
        description="Relative path where the asset is extracted locally, e.g. 'fonts/roboto'.",
    )
    files: list[str] = Field(
        description="List of file names contained within this asset package.",
    )

    @property
    def sha256(self) -> str:
        """Alias for archive_sha256."""
        return self.archive_sha256

    def get_download_url(
        self,
        repo_owner: str = "yuichi110",
        repo_name: str = "drawlib",
        tag: str = "v0.3",
    ) -> str:
        """Construct the GitHub Releases download URL for this package.

        Args:
            repo_owner: Repository owner on GitHub. Defaults to 'yuichi110'.
            repo_name: Repository name on GitHub. Defaults to 'drawlib'.
            tag: Release tag name, e.g. 'v0.3'.

        Returns:
            str: Absolute download URL from GitHub Releases.
        """
        return f"https://github.com/{repo_owner}/{repo_name}/releases/download/{tag}/{self.archive_name}"

    def get_local_dir(self) -> Path:
        """Get the absolute local destination directory for this package in drawlib._cached_assets.

        Returns:
            Path: Local directory path, e.g. '.../drawlib/_cached_assets/fonts/roboto'.
        """
        base_dir = Path(ASSETS_DIR_PATH)
        return base_dir / self.target_rel_path

    def is_downloaded(self) -> bool:
        """Check if all files in this package are already downloaded and present locally.

        Returns:
            bool: True if all files exist, False otherwise.
        """
        local_dir = self.get_local_dir()
        if not local_dir.is_dir():
            return False
        return all((local_dir / fname).is_file() for fname in self.files)

    def download_and_extract(
        self,
        tag: str = "v0.3",
        force: bool = False,
    ) -> None:
        """Download package archive from GitHub Releases, verify SHA-256, and extract files.

        Args:
            tag: GitHub release tag name. Defaults to 'v0.3'.
            force: If True, re-download and re-extract even if files already exist.

        Raises:
            RuntimeError: If download fails, SHA-256 does not match, or extraction fails.
        """
        if not force and self.is_downloaded():
            return

        url = self.get_download_url(tag=tag)
        req = urllib.request.Request(url, headers={"User-Agent": "drawlib"})  # noqa: S310
        try:
            with urllib.request.urlopen(req) as resp:  # noqa: S310
                data: bytes = resp.read()
        except Exception as e:
            msg = f"Failed to download asset package '{self.name}' from '{url}': {e}"
            raise RuntimeError(msg) from e

        actual_sha256 = hashlib.sha256(data).hexdigest()
        if actual_sha256.lower() != self.archive_sha256.lower():
            msg = f"Checksum mismatch for '{self.archive_name}': expected {self.archive_sha256}, got {actual_sha256}"
            raise RuntimeError(msg)

        local_dir = self.get_local_dir()
        local_dir.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                zf.extractall(local_dir)
        except Exception as e:
            msg = f"Failed to extract asset package '{self.archive_name}' to '{local_dir}': {e}"
            raise RuntimeError(msg) from e


class AssetManifestItem(BaseModel):
    """Metadata item for a single release asset in the manifest.

    Attributes:
        archive_name: Archive file name, e.g. 'font_roboto.zip'.
        sha256: Cryptographic SHA-256 hex digest of the archive file.
        size: File size in bytes.
    """

    model_config = ConfigDict(frozen=True)

    archive_name: str = Field(description="Archive file name.")
    sha256: str = Field(description="SHA-256 hex digest of the archive file.")
    size: int = Field(description="File size in bytes.")


class AssetManifest(BaseModel):
    """Release asset manifest mapping archive names to their metadata.

    Attributes:
        version: Drawlib release version tag, e.g. 'v0.3'.
        assets: Dictionary mapping archive_name to its AssetManifestItem.
    """

    version: str = Field(default="v0.3", description="Drawlib release version tag, e.g. 'v0.3'.")
    assets: dict[str, AssetManifestItem] = Field(
        default_factory=dict,
        description="Dictionary mapping archive_name to its AssetManifestItem.",
    )


def create_deterministic_zip_bytes(source_dir: Path, files: list[str]) -> bytes:
    """Build a deterministic, byte-reproducible ZIP archive from specified files.

    Normalizes file ordering, modification timestamps, and permissions so that
    identical content yields bit-identical archives and SHA-256 digests.

    Args:
        source_dir: Directory containing the asset files.
        files: List of file names to include in the archive.

    Returns:
        bytes: Binary content of the generated ZIP archive.
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for fname in sorted(files):
            fpath = source_dir / fname
            data = fpath.read_bytes()
            zinfo = zipfile.ZipInfo(filename=fname, date_time=(2026, 1, 1, 0, 0, 0))
            zinfo.create_system = 3
            zinfo.external_attr = 0o644 << 16
            zf.writestr(zinfo, data)
    return buf.getvalue()


class BaseReleaseAssetPackages(BaseModel):
    """Base container holding release asset package definitions with dictionary-like access."""

    model_config = ConfigDict(frozen=True)

    def __getitem__(self, key: str | object) -> ReleaseAssetPackage:
        """Access package by its identifier string or enum.

        Args:
            key: Package identifier string or enum.

        Returns:
            ReleaseAssetPackage: The requested asset package.

        Raises:
            KeyError: If key does not correspond to a known asset package.
        """
        val_name = getattr(key, "value", None)
        key_str = val_name if isinstance(val_name, str) else str(key)
        if key_str in self.__class__.model_fields:
            val = getattr(self, key_str)
            if isinstance(val, ReleaseAssetPackage):
                return val
        raise KeyError(f"Asset package '{key_str}' not found.")

    def __contains__(self, key: object) -> bool:
        """Check if a package identifier or enum exists.

        Args:
            key: Package identifier or enum.

        Returns:
            bool: True if package exists, False otherwise.
        """
        val_name = getattr(key, "value", None)
        key_str = val_name if isinstance(val_name, str) else str(key)
        return key_str in self.__class__.model_fields

    def __len__(self) -> int:
        """Return the number of registered asset packages.

        Returns:
            int: Number of asset packages.
        """
        return len(self.__class__.model_fields)

    def keys(self) -> list[str]:
        """Return a list of all package identifier strings.

        Returns:
            list[str]: Package identifiers.
        """
        return list(self.__class__.model_fields.keys())

    def values(self) -> list[ReleaseAssetPackage]:
        """Return a list of all ReleaseAssetPackage instances.

        Returns:
            list[ReleaseAssetPackage]: All asset packages.
        """
        return [getattr(self, name) for name in self.__class__.model_fields]

    def items(self) -> list[tuple[str, ReleaseAssetPackage]]:
        """Return identifier and package pairs.

        Returns:
            list[tuple[str, ReleaseAssetPackage]]: List of (name, package) tuples.
        """
        return [(name, getattr(self, name)) for name in self.__class__.model_fields]

    def get(
        self,
        key: str | object,
        default: ReleaseAssetPackage | None = None,
    ) -> ReleaseAssetPackage | None:
        """Safely retrieve an asset package by identifier or enum.

        Args:
            key: Package identifier string or enum.
            default: Fallback value if package is not found. Defaults to None.

        Returns:
            ReleaseAssetPackage | None: The matching package if found, otherwise default.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def all(self) -> list[ReleaseAssetPackage]:
        """Return all asset packages as a list."""
        return self.values()


__all__ = [
    "AssetManifest",
    "AssetManifestItem",
    "BaseReleaseAssetPackages",
    "ReleaseAssetPackage",
    "create_deterministic_zip_bytes",
]
