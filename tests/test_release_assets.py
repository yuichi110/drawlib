# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for drawlib._release_assets module."""

from __future__ import annotations

from pathlib import Path

import pytest

from drawlib._release_assets import (
    RELEASE_ASSET_PACKAGES,
    AssetManifest,
    AssetManifestItem,
    ReleaseAssetPackage,
    ReleaseAssetPackageName,
    ReleaseAssetPackages,
    find_package_by_name,
    find_package_for_font_path,
    get_all_release_asset_packages,
    get_font_asset_packages,
    get_icon_asset_packages,
)


def test_get_font_asset_packages() -> None:
    """Test retrieving font asset packages."""
    fonts = get_font_asset_packages()
    assert len(fonts) >= 45
    for pkg in fonts:
        assert isinstance(pkg, ReleaseAssetPackage)
        assert pkg.category == "font"
        assert pkg.name.startswith("font_")
        assert pkg.archive_name.endswith(".zip")
        assert pkg.source_rel_path.startswith("fonts/")
        assert pkg.target_rel_path.startswith("fonts/")


def test_get_icon_asset_packages() -> None:
    """Test retrieving icon asset packages."""
    icons = get_icon_asset_packages()
    assert len(icons) >= 1
    phosphor = next((pkg for pkg in icons if pkg.name == "icon_phosphor"), None)
    assert phosphor is not None
    assert phosphor.category == "icon"
    assert phosphor.archive_name == "icon_phosphor.zip"


def test_get_all_release_asset_packages() -> None:
    """Test total consolidated list of packages."""
    all_pkgs = get_all_release_asset_packages()
    names = [pkg.name for pkg in all_pkgs]
    assert len(names) == len(set(names)), "Duplicate package names detected."


def test_find_package_by_name() -> None:
    """Test finding packages by identifier and archive name."""
    pkg = find_package_by_name("font_roboto")
    assert pkg is not None
    assert pkg.name == "font_roboto"

    pkg_by_archive = find_package_by_name("font_roboto.zip")
    assert pkg_by_archive is not None
    assert pkg_by_archive.name == "font_roboto"

    assert find_package_by_name("non_existent_package") is None


def test_find_package_for_font_path() -> None:
    """Test resolving package from relative font file paths."""
    pkg = find_package_for_font_path("roboto/regular.ttf")
    assert pkg is not None
    assert pkg.name == "font_roboto"

    pkg_prefixed = find_package_for_font_path("fonts/cjk_japanese_noto_sans/bold.otf")
    assert pkg_prefixed is not None
    assert pkg_prefixed.name == "font_cjk_japanese_noto_sans"


def test_package_get_download_url() -> None:
    """Test download URL generation."""
    pkg = find_package_by_name("font_roboto")
    assert pkg is not None
    url = pkg.get_download_url(repo_owner="owner", repo_name="repo", tag="v1.0.0")
    assert url == "https://github.com/owner/repo/releases/download/v1.0.0/font_roboto.zip"


def test_asset_manifest_serialization() -> None:
    """Test serialization and deserialization of AssetManifest."""
    item = AssetManifestItem(
        archive_name="font_roboto.zip",
        sha256="abcdef1234567890",
        size=12345,
    )
    manifest = AssetManifest(
        version="v0.3",
        assets={"font_roboto.zip": item},
    )

    data = manifest.model_dump()
    assert data["version"] == "v0.3"
    assert data["assets"]["font_roboto.zip"]["size"] == 12345

    restored = AssetManifest.model_validate(data)
    assert restored.version == manifest.version
    assert restored.assets["font_roboto.zip"].sha256 == item.sha256


def test_release_asset_packages_container() -> None:
    """Test ReleaseAssetPackages container attributes, indexing, and methods."""
    assert isinstance(RELEASE_ASSET_PACKAGES, ReleaseAssetPackages)
    assert len(RELEASE_ASSET_PACKAGES) == 47

    # Direct attribute access with full IDE autocompletion
    roboto = RELEASE_ASSET_PACKAGES.font_roboto
    assert roboto.name == "font_roboto"
    assert roboto.category == "font"
    assert "regular.ttf" in roboto.files

    phosphor = RELEASE_ASSET_PACKAGES.icon_phosphor
    assert phosphor.name == "icon_phosphor"
    assert phosphor.category == "icon"

    # Dict-like item access via string key and enum key
    assert RELEASE_ASSET_PACKAGES["font_roboto"] == roboto
    assert RELEASE_ASSET_PACKAGES[ReleaseAssetPackageName.FONT_ROBOTO] == roboto
    assert RELEASE_ASSET_PACKAGES["icon_phosphor"] == phosphor

    with pytest.raises(KeyError):
        _ = RELEASE_ASSET_PACKAGES["unknown_package"]

    # Safe get method
    assert RELEASE_ASSET_PACKAGES.get("font_roboto") == roboto
    assert RELEASE_ASSET_PACKAGES.get(ReleaseAssetPackageName.FONT_ROBOTO) == roboto
    assert RELEASE_ASSET_PACKAGES.get("unknown_package") is None

    # Containment
    assert "font_roboto" in RELEASE_ASSET_PACKAGES
    assert ReleaseAssetPackageName.FONT_ROBOTO in RELEASE_ASSET_PACKAGES
    assert "unknown_package" not in RELEASE_ASSET_PACKAGES

    # Keys, values, items, all
    assert len(RELEASE_ASSET_PACKAGES.keys()) == 47
    assert len(RELEASE_ASSET_PACKAGES.values()) == 47
    assert len(RELEASE_ASSET_PACKAGES.items()) == 47
    assert len(RELEASE_ASSET_PACKAGES.all()) == 47


def test_release_asset_package_name_enum() -> None:
    """Test ReleaseAssetPackageName enum values and string conversion."""
    assert ReleaseAssetPackageName.FONT_ROBOTO == "font_roboto"
    assert ReleaseAssetPackageName.ICON_PHOSPHOR == "icon_phosphor"
    assert str(ReleaseAssetPackageName.FONT_ROBOTO) == "font_roboto"

    # Find package by enum
    pkg = find_package_by_name(ReleaseAssetPackageName.FONT_ROBOTO)
    assert pkg is not None
    assert pkg.name == ReleaseAssetPackageName.FONT_ROBOTO


def test_all_declared_files_exist_on_disk() -> None:
    """Verify that all files declared in RELEASE_ASSET_PACKAGES exist in release_assets/v0.3/."""
    root = Path(__file__).resolve().parent.parent
    assets_dir = root / "release_assets" / "v0.3"
    if not assets_dir.exists():
        pytest.skip("release_assets/v0.3 not present on this machine.")

    for pkg in get_all_release_asset_packages():
        pkg_dir = assets_dir / pkg.source_rel_path
        assert pkg_dir.is_dir(), f"Directory missing for {pkg.name}: {pkg_dir}"
        assert len(pkg.files) > 0, f"No files defined for {pkg.name}"
        for filename in pkg.files:
            file_path = pkg_dir / filename
            assert file_path.is_file(), f"File missing for {pkg.name}: {file_path}"
