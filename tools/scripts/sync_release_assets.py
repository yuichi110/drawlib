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
        "import hashlib",
        "import io",
        "import urllib.request",
        "import zipfile",
        "from enum import StrEnum",
        "from pathlib import Path",
        "from typing import Final, Literal",
        "",
        "from pydantic import BaseModel, ConfigDict, Field",
        "",
        "import drawlib._assets",
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
            "class ReleaseAssetPackage(BaseModel):",
            '    """Data model representing a downloadable release asset package.',
            "",
            "    Attributes:",
            "        name: Unique package identifier, e.g. 'font_roboto'.",
            "        category: Category of the asset package ('font' or 'icon').",
            "        archive_name: ZIP archive file name, e.g. 'font_roboto.zip'.",
            "        archive_sha256: SHA-256 hex digest of the ZIP archive file.",
            "        source_rel_path: Relative path within release_assets/<ver>/, e.g. 'fonts/roboto'.",
            "        target_rel_path: Relative path where the asset is extracted locally.",
            "        files: List of file names contained within this asset package.",
            '    """',
            "",
            "    model_config = ConfigDict(frozen=True)",
            "",
            '    name: ReleaseAssetPackageName = Field(description="Unique package identifier, e.g. \'font_roboto\'.")',
            '    category: Literal["font", "icon"] = Field(',
            '        description="Category of the asset package (\'font\' or \'icon\').",',
            "    )",
            '    archive_name: str = Field(description="ZIP archive file name, e.g. \'font_roboto.zip\'.")',
            '    archive_sha256: str = Field(description="SHA-256 hex digest of the ZIP archive file.")',
            "    source_rel_path: str = Field(",
            '        description="Relative path within release_assets/<ver>/, e.g. \'fonts/roboto\'.",',
            "    )",
            "    target_rel_path: str = Field(",
            '        description="Relative path where the asset is extracted locally, e.g. \'fonts/roboto\'.",',
            "    )",
            "    files: list[str] = Field(",
            '        description="List of file names contained within this asset package.",',
            "    )",
            "",
            "    @property",
            "    def sha256(self) -> str:",
            '        """Alias for archive_sha256."""',
            "        return self.archive_sha256",
            "",
            "    def get_download_url(",
            "        self,",
            '        repo_owner: str = "yuichi110",',
            '        repo_name: str = "drawlib",',
            f'        tag: str = "{tag}",',
            "    ) -> str:",
            '        """Construct the GitHub Releases download URL for this package.',
            "",
            "        Args:",
            "            repo_owner: Repository owner on GitHub. Defaults to 'yuichi110'.",
            "            repo_name: Repository name on GitHub. Defaults to 'drawlib'.",
            f"            tag: Release tag name, e.g. '{tag}'.",
            "",
            "        Returns:",
            "            str: Absolute download URL from GitHub Releases.",
            '        """',
            '        return f"https://github.com/{repo_owner}/{repo_name}/releases/download/{tag}/{self.archive_name}"',
            "",
            "    def get_local_dir(self) -> Path:",
            '        """Get the absolute local destination directory for this package in drawlib._assets.',
            "",
            "        Returns:",
            "            Path: Local directory path, e.g. '.../drawlib/_assets/fonts/roboto'.",
            '        """',
            "        base_dir = Path(drawlib._assets.__file__).parent",
            "        return base_dir / self.target_rel_path",
            "",
            "    def is_downloaded(self) -> bool:",
            '        """Check if all files in this package are already downloaded and present locally.',
            "",
            "        Returns:",
            "            bool: True if all files exist, False otherwise.",
            '        """',
            "        local_dir = self.get_local_dir()",
            "        if not local_dir.is_dir():",
            "            return False",
            "        return all((local_dir / fname).is_file() for fname in self.files)",
            "",
            "    def download_and_extract(",
            "        self,",
            "        tag: str = DEFAULT_RELEASE_TAG,",
            "        force: bool = False,",
            "    ) -> None:",
            '        """Download package archive from GitHub Releases, verify SHA-256, and extract files.',
            "",
            "        Args:",
            "            tag: GitHub release tag name. Defaults to DEFAULT_RELEASE_TAG.",
            "            force: If True, re-download and re-extract even if files already exist.",
            "",
            "        Raises:",
            "            RuntimeError: If download fails, SHA-256 does not match, or extraction fails.",
            '        """',
            "        if not force and self.is_downloaded():",
            "            return",
            "",
            "        url = self.get_download_url(tag=tag)",
            '        req = urllib.request.Request(url, headers={"User-Agent": "drawlib"})  # noqa: S310',
            "        try:",
            "            with urllib.request.urlopen(req) as resp:  # noqa: S310",
            "                data: bytes = resp.read()",
            "        except Exception as e:",
            '            msg = f"Failed to download asset package \'{self.name}\' from \'{url}\': {e}"',
            "            raise RuntimeError(msg) from e",
            "",
            "        actual_sha256 = hashlib.sha256(data).hexdigest()",
            "        if actual_sha256.lower() != self.archive_sha256.lower():",
            "            msg = (",
            '                f"Checksum mismatch for \'{self.archive_name}\': "',
            '                f"expected {self.archive_sha256}, got {actual_sha256}"',
            "            )",
            "            raise RuntimeError(msg)",
            "",
            "        local_dir = self.get_local_dir()",
            "        local_dir.mkdir(parents=True, exist_ok=True)",
            "        try:",
            "            with zipfile.ZipFile(io.BytesIO(data)) as zf:",
            "                zf.extractall(local_dir)",
            "        except Exception as e:",
            '            msg = f"Failed to extract asset package \'{self.archive_name}\' to \'{local_dir}\': {e}"',
            "            raise RuntimeError(msg) from e",
            "",
            "",
            "class AssetManifestItem(BaseModel):",
            '    """Metadata item for a single release asset in the manifest.',
            "",
            "    Attributes:",
            "        archive_name: Archive file name, e.g. 'font_roboto.zip'.",
            "        sha256: Cryptographic SHA-256 hex digest of the archive file.",
            "        size: File size in bytes.",
            '    """',
            "",
            "    model_config = ConfigDict(frozen=True)",
            "",
            '    archive_name: str = Field(description="Archive file name.")',
            '    sha256: str = Field(description="SHA-256 hex digest of the archive file.")',
            '    size: int = Field(description="File size in bytes.")',
            "",
            "",
            "class AssetManifest(BaseModel):",
            '    """Release asset manifest mapping archive names to their metadata.',
            "",
            "    Attributes:",
            "        version: Drawlib release version tag, e.g. 'v0.3'.",
            "        assets: Dictionary mapping archive_name to its AssetManifestItem.",
            '    """',
            "",
            f'    version: str = Field(default="{tag}", description="Drawlib release version tag, e.g. \'{tag}\'.")',
            "    assets: dict[str, AssetManifestItem] = Field(",
            "        default_factory=dict,",
            '        description="Dictionary mapping archive_name to its AssetManifestItem.",',
            "    )",
            "",
            "",
            "class ReleaseAssetPackages(BaseModel):",
            '    """Container holding all release asset package definitions with full IDE type completion.',
            "",
            "    Each package is exposed as a typed field for IDE autocompletion, while also",
            "    providing dict-like item access, iteration, and lookup utilities.",
            '    """',
            "",
            "    model_config = ConfigDict(frozen=True)",
            "",
        ]
    )

    for pkg in packages:
        lines.append(f'    {pkg["var_name"]}: ReleaseAssetPackage')

    lines.extend(
        [
            "",
            "    def __getitem__(self, key: str | ReleaseAssetPackageName) -> ReleaseAssetPackage:",
            '        """Access package by its identifier string or enum.',
            "",
            "        Args:",
            "            key: Package identifier string or ReleaseAssetPackageName enum.",
            "",
            "        Returns:",
            "            ReleaseAssetPackage: The requested asset package.",
            "",
            "        Raises:",
            "            KeyError: If key does not correspond to a known asset package.",
            '        """',
            "        key_str = key.value if isinstance(key, ReleaseAssetPackageName) else str(key)",
            "        if key_str in self.__class__.model_fields:",
            "            val = getattr(self, key_str)",
            "            if isinstance(val, ReleaseAssetPackage):",
            "                return val",
            '        raise KeyError(f"Asset package \'{key_str}\' not found.")',
            "",
            "    def __contains__(self, key: object) -> bool:",
            '        """Check if a package identifier or enum exists.',
            "",
            "        Args:",
            "            key: Package identifier or enum.",
            "",
            "        Returns:",
            "            bool: True if package exists, False otherwise.",
            '        """',
            "        if isinstance(key, ReleaseAssetPackageName):",
            "            return key.value in self.__class__.model_fields",
            "        if isinstance(key, str):",
            "            return key in self.__class__.model_fields",
            "        return False",
            "",
            "    def __len__(self) -> int:",
            '        """Return the number of registered asset packages.',
            "",
            "        Returns:",
            "            int: Number of asset packages.",
            '        """',
            "        return len(self.__class__.model_fields)",
            "",
            "    def keys(self) -> list[str]:",
            '        """Return a list of all package identifier strings.',
            "",
            "        Returns:",
            "            list[str]: Package identifiers.",
            '        """',
            "        return list(self.__class__.model_fields.keys())",
            "",
            "    def values(self) -> list[ReleaseAssetPackage]:",
            '        """Return a list of all ReleaseAssetPackage instances.',
            "",
            "        Returns:",
            "            list[ReleaseAssetPackage]: All asset packages.",
            '        """',
            "        return [getattr(self, name) for name in self.__class__.model_fields]",
            "",
            "    def items(self) -> list[tuple[str, ReleaseAssetPackage]]:",
            '        """Return identifier and package pairs.',
            "",
            "        Returns:",
            "            list[tuple[str, ReleaseAssetPackage]]: List of (name, package) tuples.",
            '        """',
            "        return [(name, getattr(self, name)) for name in self.__class__.model_fields]",
            "",
            "    def get(",
            "        self,",
            "        key: str | ReleaseAssetPackageName,",
            "        default: ReleaseAssetPackage | None = None,",
            "    ) -> ReleaseAssetPackage | None:",
            '        """Safely retrieve an asset package by identifier or enum.',
            "",
            "        Args:",
            "            key: Package identifier string or enum.",
            "            default: Fallback value if package is not found. Defaults to None.",
            "",
            "        Returns:",
            "            ReleaseAssetPackage | None: The matching package if found, otherwise default.",
            '        """',
            "        try:",
            "            return self[key]",
            "        except KeyError:",
            "            return default",
            "",
            "    def all(self) -> list[ReleaseAssetPackage]:",
            '        """Return all asset packages as a list.',
            "",
            "        Returns:",
            "            list[ReleaseAssetPackage]: All package definitions.",
            '        """',
            "        return self.values()",
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
            "def create_deterministic_zip_bytes(source_dir: Path, files: list[str]) -> bytes:",
            '    """Build a deterministic, byte-reproducible ZIP archive from specified files.',
            "",
            "    Normalizes file ordering, modification timestamps, and permissions so that",
            "    identical content yields bit-identical archives and SHA-256 digests.",
            "",
            "    Args:",
            "        source_dir: Directory containing the asset files.",
            "        files: List of file names to include in the archive.",
            "",
            "    Returns:",
            "        bytes: Binary content of the generated ZIP archive.",
            '    """',
            "    buf = io.BytesIO()",
            '    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:',
            "        for fname in sorted(files):",
            "            fpath = source_dir / fname",
            "            data = fpath.read_bytes()",
            "            zinfo = zipfile.ZipInfo(filename=fname, date_time=(2026, 1, 1, 0, 0, 0))",
            "            zinfo.external_attr = 0o644 << 16",
            "            zf.writestr(zinfo, data)",
            "    return buf.getvalue()",
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
