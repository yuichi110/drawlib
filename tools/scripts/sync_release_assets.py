# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Synchronize release assets from release_assets/ directory into src/drawlib/_release_assets.py.

Scans all packages in release_assets/<tag>/ (fonts, fonticons, icons), builds
deterministic in-memory ZIP archives to compute exact SHA-256 digests, and generates
the unified Single Source of Truth (SoT) file at src/drawlib/_release_assets.py.
"""

from __future__ import annotations

import hashlib
import io
import subprocess
import zipfile
from pathlib import Path


def create_deterministic_zip_bytes(source_dir: Path, files: list[str]) -> bytes:
    """Build a deterministic, byte-reproducible ZIP archive from specified files."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for fname in sorted(files):
            fpath = source_dir / fname
            data = fpath.read_bytes()
            zinfo = zipfile.ZipInfo(filename=fname, date_time=(2026, 1, 1, 0, 0, 0))
            zinfo.external_attr = 0o644 << 16
            zf.writestr(zinfo, data)
    return buf.getvalue()


def scan_asset_packages(assets_root: Path) -> list[dict[str, object]]:
    """Scan release_assets directory and collect metadata for all packages."""
    categories = [
        ("fonts", "font", "fonts"),
        ("fonticons", "icon", "fonticons"),
        ("icons", "icon", "icons"),
    ]
    packages: list[dict[str, object]] = []

    for subdir, cat, rel_prefix in categories:
        cat_dir = assets_root / subdir
        if not cat_dir.is_dir():
            continue

        for p in sorted(cat_dir.iterdir()):
            if not p.is_dir() or p.name.startswith("."):
                continue

            files = sorted([f.name for f in p.iterdir() if f.is_file() and not f.name.startswith(".")])
            zip_bytes = create_deterministic_zip_bytes(p, files)
            sha256_digest = hashlib.sha256(zip_bytes).hexdigest()

            var_name = f"{cat}_{p.name}"
            enum_name = var_name.upper()
            archive_name = f"{var_name}.zip"
            source_rel_path = f"{rel_prefix}/{p.name}"
            target_rel_path = f"{rel_prefix}/{p.name}"

            packages.append(
                {
                    "var_name": var_name,
                    "enum_name": enum_name,
                    "category": cat,
                    "archive_name": archive_name,
                    "archive_sha256": sha256_digest,
                    "source_rel_path": source_rel_path,
                    "target_rel_path": target_rel_path,
                    "files": files,
                    "size_bytes": len(zip_bytes),
                }
            )

    return packages


def generate_release_assets_code(packages: list[dict[str, object]], tag: str = "v0.3") -> str:
    """Generate Python source code for src/drawlib/_release_assets.py."""
    lines: list[str] = [
        "# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)",
        "#",
        "# This software is licensed under the Apache License, Version 2.0.",
        "# For more information, please visit: https://github.com/yuichi110/drawlib",
        "#",
        "# This software is provided \"as is\", without warranty of any kind,",
        "# express or implied, including but not limited to the warranties of",
        "# merchantability, fitness for a particular purpose and noninfringement.",
        "",
        '"""Release assets packaging and download specifications for drawlib.',
        "",
        "Acts as the Single Source of Truth (SoT) defining all downloadable asset packages,",
        "archive structures, and contained files for fonts and icons.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from enum import StrEnum",
        "from typing import Final",
        "",
        "from drawlib._core.l3_external._package import (",
        "    AssetManifest,",
        "    AssetManifestItem,",
        "    BaseReleaseAssetPackages,",
        "    ReleaseAssetPackage,",
        "    create_deterministic_zip_bytes,",
        ")",
        "",
        f'DEFAULT_RELEASE_TAG: Final[str] = "{tag}"',
        "",
        "",
        "class ReleaseAssetPackageName(StrEnum):",
        '    """Enumeration of all available release asset package names."""',
        "",
    ]

    for pkg in packages:
        lines.append(f'    {pkg["enum_name"]} = "{pkg["var_name"]}"')

    lines.extend(
        [
            "",
            "",
            "class ReleaseAssetPackages(BaseReleaseAssetPackages):",
            '    """Container holding all release asset package definitions with full IDE type completion.',
            "",
            "    Each package is exposed as a typed field for IDE autocompletion, while also",
            "    providing dict-like item access, iteration, and lookup utilities.",
            '    """',
            "",
        ]
    )

    for pkg in packages:
        lines.append(f'    {pkg["var_name"]}: ReleaseAssetPackage')

    lines.extend(
        [
            "",
            "",
            "# ==============================================================================",
            "# Single Source of Truth (SoT): Explicit Asset Package Definitions",
            "# ==============================================================================",
            "",
            "RELEASE_ASSET_PACKAGES: Final[ReleaseAssetPackages] = ReleaseAssetPackages(",
        ]
    )

    for pkg in packages:
        lines.append(f'    {pkg["var_name"]}=ReleaseAssetPackage(')
        lines.append(f'        name=ReleaseAssetPackageName.{pkg["enum_name"]},')
        lines.append(f'        category="{pkg["category"]}",')
        lines.append(f'        archive_name="{pkg["archive_name"]}",')
        lines.append(f'        archive_sha256="{pkg["archive_sha256"]}",')
        lines.append(f'        source_rel_path="{pkg["source_rel_path"]}",')
        lines.append(f'        target_rel_path="{pkg["target_rel_path"]}",')
        lines.append(f'        files={pkg["files"]!r},')
        lines.append("    ),")

    lines.extend(
        [
            ")",
            "",
            "",
            "def get_all_release_asset_packages() -> list[ReleaseAssetPackage]:",
            '    """Retrieve all defined release asset packages.',
            "",
            "    Returns:",
            "        list[ReleaseAssetPackage]: Combined list of font and icon packages.",
            '    """',
            "    return RELEASE_ASSET_PACKAGES.all()",
            "",
            "",
            "def get_font_asset_packages() -> list[ReleaseAssetPackage]:",
            '    """Retrieve all font asset packages.',
            "",
            "    Returns:",
            "        list[ReleaseAssetPackage]: List of font package definitions.",
            '    """',
            '    return [pkg for pkg in RELEASE_ASSET_PACKAGES.values() if pkg.category == "font"]',
            "",
            "",
            "def get_icon_asset_packages() -> list[ReleaseAssetPackage]:",
            '    """Retrieve all icon asset packages.',
            "",
            "    Returns:",
            "        list[ReleaseAssetPackage]: List of icon package definitions.",
            '    """',
            '    return [pkg for pkg in RELEASE_ASSET_PACKAGES.values() if pkg.category == "icon"]',
            "",
            "",
            "def find_package_by_name(package_name: str | ReleaseAssetPackageName) -> ReleaseAssetPackage | None:",
            '    """Find an asset package by its unique package identifier, enum, or archive name.',
            "",
            "    Args:",
            "        package_name: The package identifier or enum (e.g. 'font_roboto', 'font_roboto.zip').",
            "",
            "    Returns:",
            "        ReleaseAssetPackage | None: The matching package if found, otherwise None.",
            '    """',
            "    name_str = (",
            "        package_name.value if isinstance(package_name, ReleaseAssetPackageName) else str(package_name)",
            "    )",
            "    if name_str in RELEASE_ASSET_PACKAGES:",
            "        return RELEASE_ASSET_PACKAGES[name_str]",
            "    for pkg in RELEASE_ASSET_PACKAGES.values():",
            "        if pkg.archive_name == name_str:",
            "            return pkg",
            "    return None",
            "",
            "",
            "def find_package_for_font_path(font_file_path: str) -> ReleaseAssetPackage | None:",
            '    """Identify which asset package contains a given font resource path.',
            "",
            "    Args:",
            "        font_file_path: Relative font path (e.g. 'roboto/regular.ttf' or 'fonts/roboto/regular.ttf').",
            "",
            "    Returns:",
            "        ReleaseAssetPackage | None: The containing package if matched, otherwise None.",
            '    """',
            '    normalized = font_file_path.strip("/").removeprefix("fonts/")',
            '    family = normalized.split("/")[0] if "/" in normalized else normalized',
            '    target_name = f"font_{family}"',
            "    return RELEASE_ASSET_PACKAGES.get(target_name)",
            "",
            "",
            "def find_package_for_icon_path(icon_file_path: str) -> ReleaseAssetPackage | None:",
            '    """Identify which asset package contains a given icon resource path.',
            "",
            "    Args:",
            "        icon_file_path: Relative icon path",
            "            (e.g. 'phosphor/thin.ttf', 'fonticons/phosphor/thin.ttf', 'icons/gcp/gce.png').",
            "",
            "    Returns:",
            "        ReleaseAssetPackage | None: The containing package if matched, otherwise None.",
            '    """',
            '    normalized = icon_file_path.strip("/").removeprefix("fonticons/").removeprefix("icons/")',
            '    family = normalized.split("/")[0] if "/" in normalized else normalized',
            '    target_name = f"icon_{family}"',
            "    return RELEASE_ASSET_PACKAGES.get(target_name)",
            "",
            "",
            "def find_package_for_resource_path(resource_path: str) -> ReleaseAssetPackage | None:",
            '    """Identify which asset package contains a given resource path (font or icon).',
            "",
            "    Args:",
            "        resource_path: Relative resource path",
            "            (e.g. 'fonts/roboto/regular.ttf', 'fonticons/phosphor/thin.ttf', 'icons/gcp/gce.png').",
            "",
            "    Returns:",
            "        ReleaseAssetPackage | None: The containing package if matched, otherwise None.",
            '    """',
            '    norm = resource_path.strip("/")',
            '    if norm.startswith("fonticons/") or norm.startswith("phosphor/"):',
            "        return find_package_for_icon_path(norm)",
            '    if norm.startswith("icons/") or norm.startswith("gcp/"):',
            "        return find_package_for_icon_path(norm)",
            "    return find_package_for_font_path(norm)",
            "",
            "",
            "def ensure_asset_available(resource_path: str, tag: str = DEFAULT_RELEASE_TAG) -> None:",
            '    """Ensure that the asset file for a given resource path is downloaded and available.',
            "",
            "    Args:",
            "        resource_path: Relative path to font or icon file.",
            "        tag: Release tag to download from if missing. Defaults to DEFAULT_RELEASE_TAG.",
            "",
            "    Raises:",
            "        ValueError: If no release asset package matches the resource path.",
            "        RuntimeError: If downloading or extracting the package fails.",
            '    """',
            "    pkg = find_package_for_resource_path(resource_path)",
            "    if pkg is None:",
            '        raise ValueError(f"No release asset package found for resource path \'{resource_path}\'.")',
            "",
            "    if not pkg.is_downloaded():",
            "        pkg.download_and_extract(tag=tag)",
            "",
            "",
            "def download_all_release_assets(tag: str = DEFAULT_RELEASE_TAG, force: bool = False) -> None:",
            '    """Download and extract all defined release asset packages (fonts and icons).',
            "",
            "    Args:",
            "        tag: Release tag to download from. Defaults to DEFAULT_RELEASE_TAG.",
            "        force: If True, force re-download even if already present.",
            '    """',
            "    for pkg in RELEASE_ASSET_PACKAGES.values():",
            "        pkg.download_and_extract(tag=tag, force=force)",
            "",
            "",
            "def get_release_asset_manifest(tag: str = DEFAULT_RELEASE_TAG) -> AssetManifest:",
            '    """Generate complete release manifest from defined packages.',
            "",
            "    Args:",
            "        tag: Release version tag. Defaults to DEFAULT_RELEASE_TAG.",
            "",
            "    Returns:",
            "        AssetManifest: Populated release manifest.",
            '    """',
            "    assets = {",
            "        pkg.archive_name: AssetManifestItem(",
            "            archive_name=pkg.archive_name,",
            "            sha256=pkg.archive_sha256,",
            "            size=0,",
            "        )",
            "        for pkg in RELEASE_ASSET_PACKAGES.values()",
            "    }",
            "    return AssetManifest(version=tag, assets=assets)",
            "",
            "",
            "__all__ = [",
            '    "DEFAULT_RELEASE_TAG",',
            '    "AssetManifest",',
            '    "AssetManifestItem",',
            '    "BaseReleaseAssetPackages",',
            '    "ReleaseAssetPackage",',
            '    "ReleaseAssetPackageName",',
            '    "ReleaseAssetPackages",',
            '    "RELEASE_ASSET_PACKAGES",',
            '    "create_deterministic_zip_bytes",',
            '    "download_all_release_assets",',
            '    "ensure_asset_available",',
            '    "find_package_for_font_path",',
            '    "find_package_for_icon_path",',
            '    "find_package_for_resource_path",',
            '    "get_all_release_asset_packages",',
            '    "get_release_asset_manifest",',
            "]",
            "",
        ]
    )

    return "\n".join(lines)


def sync_release_assets(
    assets_root: Path = Path("release_assets/v0.3"),
    target_py: Path = Path("src/drawlib/_release_assets.py"),
    tag: str = "v0.3",
    check: bool = False,
) -> bool:
    """Scan assets, generate code, and update or check src/drawlib/_release_assets.py.

    Returns:
        bool: True if in sync (or updated successfully), False if check failed.
    """
    packages = scan_asset_packages(assets_root)
    generated_code = generate_release_assets_code(packages, tag=tag)

    proc = subprocess.run(
        ["uv", "run", "ruff", "format", "-"],
        input=generated_code,
        text=True,
        capture_output=True,
        check=True,
    )
    formatted_code = proc.stdout

    if check:
        current_code = target_py.read_text(encoding="utf-8") if target_py.is_file() else ""
        return current_code == formatted_code

    target_py.write_text(formatted_code, encoding="utf-8")
    return True


if __name__ == "__main__":
    import sys

    tag = sys.argv[1] if len(sys.argv) > 1 else "v0.3"
    assets_dir = Path(f"release_assets/{tag}")
    target_file = Path("src/drawlib/_release_assets.py")

    print(f"Scanning release assets in {assets_dir}...")
    packages = scan_asset_packages(assets_dir)
    print(f"Found {len(packages)} packages.")
    sync_release_assets(assets_dir, target_file, tag=tag)
    print(f"Successfully generated and formatted {target_file}!")
