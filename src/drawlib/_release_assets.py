# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Release assets packaging and download specifications for drawlib.

Acts as the Single Source of Truth (SoT) defining all downloadable asset packages,
archive structures, and contained files for fonts and icons.
"""

from __future__ import annotations

import hashlib
import io
import urllib.request
import zipfile
from enum import StrEnum
from pathlib import Path
from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field

import drawlib._assets

DEFAULT_RELEASE_TAG: Final[str] = "v0.3"


class ReleaseAssetPackageName(StrEnum):
    """Enumeration of all available release asset package names."""

    FONT_ARABIC_NOTO_KUFI = "font_arabic_noto_kufi"
    FONT_ARABIC_NOTO_NASKH = "font_arabic_noto_naskh"
    FONT_ARABIC_NOTO_SANS = "font_arabic_noto_sans"
    FONT_BRAHMIC_BENGALI_NOTO_SANS = "font_brahmic_bengali_noto_sans"
    FONT_BRAHMIC_BENGALI_NOTO_SERIF = "font_brahmic_bengali_noto_serif"
    FONT_BRAHMIC_DEVANAGARI_NOTO_SANS = "font_brahmic_devanagari_noto_sans"
    FONT_BRAHMIC_DEVANAGARI_NOTO_SERIF = "font_brahmic_devanagari_noto_serif"
    FONT_BRAHMIC_TAMIL_NOTO_SANS = "font_brahmic_tamil_noto_sans"
    FONT_BRAHMIC_TAMIL_NOTO_SERIF = "font_brahmic_tamil_noto_serif"
    FONT_BRAHMIC_TELUGU_NOTO_SANS = "font_brahmic_telugu_noto_sans"
    FONT_BRAHMIC_TELUGU_NOTO_SERIF = "font_brahmic_telugu_noto_serif"
    FONT_CHINESE_HONGKONG_NOTO_SANS = "font_chinese_hongkong_noto_sans"
    FONT_CHINESE_HONGKONG_NOTO_SERIF = "font_chinese_hongkong_noto_serif"
    FONT_CHINESE_SIMPLIFIED_NOTO_SANS = "font_chinese_simplified_noto_sans"
    FONT_CHINESE_SIMPLIFIED_NOTO_SERIF = "font_chinese_simplified_noto_serif"
    FONT_CHINESE_TRADITIONAL_NOTO_SANS = "font_chinese_traditional_noto_sans"
    FONT_CHINESE_TRADITIONAL_NOTO_SERIF = "font_chinese_traditional_noto_serif"
    FONT_CJK_JAPANESE_NOTO_SANS = "font_cjk_japanese_noto_sans"
    FONT_CJK_JAPANESE_NOTO_SERIF = "font_cjk_japanese_noto_serif"
    FONT_JAPANESE_MPLUS_1P = "font_japanese_mplus_1p"
    FONT_JAPANESE_MPLUS_ROUNDED1C = "font_japanese_mplus_rounded1c"
    FONT_JAPANESE_NOTO_SANS = "font_japanese_noto_sans"
    FONT_JAPANESE_NOTO_SERIF = "font_japanese_noto_serif"
    FONT_JAPANESE_SAWARABI_GOTHIC = "font_japanese_sawarabi_gothic"
    FONT_JAPANESE_SAWARABI_MINCHO = "font_japanese_sawarabi_mincho"
    FONT_KOREAN_NOTO_SANS = "font_korean_noto_sans"
    FONT_KOREAN_NOTO_SERIF = "font_korean_noto_serif"
    FONT_MONO_COURIER = "font_mono_courier"
    FONT_MONO_SOURCE_CODE_PRO = "font_mono_source_code_pro"
    FONT_MONO_SOURCE_HAN_CODE_JP = "font_mono_source_han_code_jp"
    FONT_ROBOTO = "font_roboto"
    FONT_ROBOTO_CONDENSED = "font_roboto_condensed"
    FONT_ROBOTO_MONO = "font_roboto_mono"
    FONT_ROBOTO_SERIF = "font_roboto_serif"
    FONT_ROBOTO_SLAB = "font_roboto_slab"
    FONT_SANS_LATO = "font_sans_lato"
    FONT_SANS_MONSTSERRAT = "font_sans_monstserrat"
    FONT_SANS_OPEN_SANS = "font_sans_open_sans"
    FONT_SANS_OSWALD = "font_sans_oswald"
    FONT_SANS_POPPINS = "font_sans_poppins"
    FONT_SANS_RALEWAYS = "font_sans_raleways"
    FONT_SERIF_MERRIWEATHER = "font_serif_merriweather"
    FONT_SERIF_PLATYPI = "font_serif_platypi"
    FONT_SERIF_PLAYFAIRDISPLAY = "font_serif_playfairdisplay"
    FONT_THAI_NOTO_SANS = "font_thai_noto_sans"
    FONT_THAI_NOTO_SERIF = "font_thai_noto_serif"
    ICON_PHOSPHOR = "icon_phosphor"
    ICON_GCP = "icon_gcp"


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

    name: ReleaseAssetPackageName = Field(description="Unique package identifier, e.g. 'font_roboto'.")
    category: Literal["font", "icon"] = Field(
        description="Category of the asset package ('font' or 'icon').",
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
        """Get the absolute local destination directory for this package in drawlib._assets.

        Returns:
            Path: Local directory path, e.g. '.../drawlib/_assets/fonts/roboto'.
        """
        base_dir = Path(drawlib._assets.__file__).parent
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
        tag: str = DEFAULT_RELEASE_TAG,
        force: bool = False,
    ) -> None:
        """Download package archive from GitHub Releases, verify SHA-256, and extract files.

        Args:
            tag: GitHub release tag name. Defaults to DEFAULT_RELEASE_TAG.
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


class ReleaseAssetPackages(BaseModel):
    """Container holding all release asset package definitions with full IDE type completion.

    Each package is exposed as a typed field for IDE autocompletion, while also
    providing dict-like item access, iteration, and lookup utilities.
    """

    model_config = ConfigDict(frozen=True)

    font_arabic_noto_kufi: ReleaseAssetPackage
    font_arabic_noto_naskh: ReleaseAssetPackage
    font_arabic_noto_sans: ReleaseAssetPackage
    font_brahmic_bengali_noto_sans: ReleaseAssetPackage
    font_brahmic_bengali_noto_serif: ReleaseAssetPackage
    font_brahmic_devanagari_noto_sans: ReleaseAssetPackage
    font_brahmic_devanagari_noto_serif: ReleaseAssetPackage
    font_brahmic_tamil_noto_sans: ReleaseAssetPackage
    font_brahmic_tamil_noto_serif: ReleaseAssetPackage
    font_brahmic_telugu_noto_sans: ReleaseAssetPackage
    font_brahmic_telugu_noto_serif: ReleaseAssetPackage
    font_chinese_hongkong_noto_sans: ReleaseAssetPackage
    font_chinese_hongkong_noto_serif: ReleaseAssetPackage
    font_chinese_simplified_noto_sans: ReleaseAssetPackage
    font_chinese_simplified_noto_serif: ReleaseAssetPackage
    font_chinese_traditional_noto_sans: ReleaseAssetPackage
    font_chinese_traditional_noto_serif: ReleaseAssetPackage
    font_cjk_japanese_noto_sans: ReleaseAssetPackage
    font_cjk_japanese_noto_serif: ReleaseAssetPackage
    font_japanese_mplus_1p: ReleaseAssetPackage
    font_japanese_mplus_rounded1c: ReleaseAssetPackage
    font_japanese_noto_sans: ReleaseAssetPackage
    font_japanese_noto_serif: ReleaseAssetPackage
    font_japanese_sawarabi_gothic: ReleaseAssetPackage
    font_japanese_sawarabi_mincho: ReleaseAssetPackage
    font_korean_noto_sans: ReleaseAssetPackage
    font_korean_noto_serif: ReleaseAssetPackage
    font_mono_courier: ReleaseAssetPackage
    font_mono_source_code_pro: ReleaseAssetPackage
    font_mono_source_han_code_jp: ReleaseAssetPackage
    font_roboto: ReleaseAssetPackage
    font_roboto_condensed: ReleaseAssetPackage
    font_roboto_mono: ReleaseAssetPackage
    font_roboto_serif: ReleaseAssetPackage
    font_roboto_slab: ReleaseAssetPackage
    font_sans_lato: ReleaseAssetPackage
    font_sans_monstserrat: ReleaseAssetPackage
    font_sans_open_sans: ReleaseAssetPackage
    font_sans_oswald: ReleaseAssetPackage
    font_sans_poppins: ReleaseAssetPackage
    font_sans_raleways: ReleaseAssetPackage
    font_serif_merriweather: ReleaseAssetPackage
    font_serif_platypi: ReleaseAssetPackage
    font_serif_playfairdisplay: ReleaseAssetPackage
    font_thai_noto_sans: ReleaseAssetPackage
    font_thai_noto_serif: ReleaseAssetPackage
    icon_phosphor: ReleaseAssetPackage
    icon_gcp: ReleaseAssetPackage

    def __getitem__(self, key: str | ReleaseAssetPackageName) -> ReleaseAssetPackage:
        """Access package by its identifier string or enum.

        Args:
            key: Package identifier string or ReleaseAssetPackageName enum.

        Returns:
            ReleaseAssetPackage: The requested asset package.

        Raises:
            KeyError: If key does not correspond to a known asset package.
        """
        key_str = key.value if isinstance(key, ReleaseAssetPackageName) else str(key)
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
        if isinstance(key, ReleaseAssetPackageName):
            return key.value in self.__class__.model_fields
        if isinstance(key, str):
            return key in self.__class__.model_fields
        return False

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
        key: str | ReleaseAssetPackageName,
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
        """Return all asset packages as a list.

        Returns:
            list[ReleaseAssetPackage]: All package definitions.
        """
        return self.values()


# ==============================================================================
# Single Source of Truth (SoT): Explicit Asset Package Definitions
# ==============================================================================

RELEASE_ASSET_PACKAGES: Final[ReleaseAssetPackages] = ReleaseAssetPackages(
    font_arabic_noto_kufi=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ARABIC_NOTO_KUFI,
        category="font",
        archive_name="font_arabic_noto_kufi.zip",
        archive_sha256="b9def74cf139f0821a71e09d850127a05cd2efeae9212a9c3973d3573850819a",
        source_rel_path="fonts/arabic_noto_kufi",
        target_rel_path="fonts/arabic_noto_kufi",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_arabic_noto_naskh=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ARABIC_NOTO_NASKH,
        category="font",
        archive_name="font_arabic_noto_naskh.zip",
        archive_sha256="bcb55fd6bcd31926616c8ace47051b4b9c02f97a01927df6b1348fdc241959c9",
        source_rel_path="fonts/arabic_noto_naskh",
        target_rel_path="fonts/arabic_noto_naskh",
        files=["OFL.txt", "README.txt", "bold.ttf", "regular.ttf"],
    ),
    font_arabic_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ARABIC_NOTO_SANS,
        category="font",
        archive_name="font_arabic_noto_sans.zip",
        archive_sha256="349937b7962bde607eddf7892ee3e8b8bc5d94554979ff642ccf10bd12ac74e5",
        source_rel_path="fonts/arabic_noto_sans",
        target_rel_path="fonts/arabic_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_bengali_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_BENGALI_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_bengali_noto_sans.zip",
        archive_sha256="d72e6b70f49ceacc25d34b092de48ddf583d72aa2960e78ea8eff047107309e6",
        source_rel_path="fonts/brahmic_bengali_noto_sans",
        target_rel_path="fonts/brahmic_bengali_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_bengali_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_BENGALI_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_bengali_noto_serif.zip",
        archive_sha256="fb9bb9601d3402c5f6ae265cd7189c7ce8c374408a23ae4c6d417fceed9beb7c",
        source_rel_path="fonts/brahmic_bengali_noto_serif",
        target_rel_path="fonts/brahmic_bengali_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_devanagari_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_DEVANAGARI_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_devanagari_noto_sans.zip",
        archive_sha256="0ea7a85d70decd60db976f09d0f57ecb3a3f817ad650ed2007d2ff36f248cd64",
        source_rel_path="fonts/brahmic_devanagari_noto_sans",
        target_rel_path="fonts/brahmic_devanagari_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_devanagari_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_DEVANAGARI_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_devanagari_noto_serif.zip",
        archive_sha256="19097fbccd17f6e694f1c324730961925d3115a9557a72a525c6cb6005f3c62a",
        source_rel_path="fonts/brahmic_devanagari_noto_serif",
        target_rel_path="fonts/brahmic_devanagari_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_tamil_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TAMIL_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_tamil_noto_sans.zip",
        archive_sha256="22902fe03d741ae3d7d3b8372fa6a0c1240ce137360fb790882927a9c4351610",
        source_rel_path="fonts/brahmic_tamil_noto_sans",
        target_rel_path="fonts/brahmic_tamil_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_tamil_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TAMIL_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_tamil_noto_serif.zip",
        archive_sha256="2f980967778648b0795bd3dd6476eb07cbab45642da9f9dd7144865f56103a97",
        source_rel_path="fonts/brahmic_tamil_noto_serif",
        target_rel_path="fonts/brahmic_tamil_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_telugu_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TELUGU_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_telugu_noto_sans.zip",
        archive_sha256="2007b1b523475c8d204cba706551b0add15a22627f5d06804eca5af407f9e5dc",
        source_rel_path="fonts/brahmic_telugu_noto_sans",
        target_rel_path="fonts/brahmic_telugu_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_telugu_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TELUGU_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_telugu_noto_serif.zip",
        archive_sha256="465790f011cca980c72bc79494469b8faf6ab76150c5e28bcd69e801a0b51d6c",
        source_rel_path="fonts/brahmic_telugu_noto_serif",
        target_rel_path="fonts/brahmic_telugu_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_hongkong_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_HONGKONG_NOTO_SANS,
        category="font",
        archive_name="font_chinese_hongkong_noto_sans.zip",
        archive_sha256="a17ec42d3d201f9ac6c32fa8e1ac1aecaa87e26fa23f78e08f362353bdd23221",
        source_rel_path="fonts/chinese_hongkong_noto_sans",
        target_rel_path="fonts/chinese_hongkong_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_hongkong_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_HONGKONG_NOTO_SERIF,
        category="font",
        archive_name="font_chinese_hongkong_noto_serif.zip",
        archive_sha256="69668cb393b2a3528458bd35e61eec65d5ba61f8acb8a2d4f58b291aa88e9e9b",
        source_rel_path="fonts/chinese_hongkong_noto_serif",
        target_rel_path="fonts/chinese_hongkong_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_simplified_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_SIMPLIFIED_NOTO_SANS,
        category="font",
        archive_name="font_chinese_simplified_noto_sans.zip",
        archive_sha256="04003bff3e6be20df258190cf2d2a25e3feeef8d34e45ecdc52eaf8c744f2546",
        source_rel_path="fonts/chinese_simplified_noto_sans",
        target_rel_path="fonts/chinese_simplified_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_simplified_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_SIMPLIFIED_NOTO_SERIF,
        category="font",
        archive_name="font_chinese_simplified_noto_serif.zip",
        archive_sha256="caf448471e2ff79ab03cd1180b1bd7d3940be7a7a24ba2ea1b78c936b7250692",
        source_rel_path="fonts/chinese_simplified_noto_serif",
        target_rel_path="fonts/chinese_simplified_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_traditional_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_TRADITIONAL_NOTO_SANS,
        category="font",
        archive_name="font_chinese_traditional_noto_sans.zip",
        archive_sha256="70c319c6812d262d6ac91b161baec373aecdc185bd55a91dee7614150ff47802",
        source_rel_path="fonts/chinese_traditional_noto_sans",
        target_rel_path="fonts/chinese_traditional_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_traditional_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_TRADITIONAL_NOTO_SERIF,
        category="font",
        archive_name="font_chinese_traditional_noto_serif.zip",
        archive_sha256="8a776c41885b1648b6b69000b9989649c46319405c8d0b8b42620e8c34cfbc06",
        source_rel_path="fonts/chinese_traditional_noto_serif",
        target_rel_path="fonts/chinese_traditional_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_cjk_japanese_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CJK_JAPANESE_NOTO_SANS,
        category="font",
        archive_name="font_cjk_japanese_noto_sans.zip",
        archive_sha256="ff8c6b38c2cd47f430fd5db95aed64df6d32134edc08d0b4acd89f63a2fe0368",
        source_rel_path="fonts/cjk_japanese_noto_sans",
        target_rel_path="fonts/cjk_japanese_noto_sans",
        files=["bold.otf", "light.otf", "readme.txt", "regular.otf"],
    ),
    font_cjk_japanese_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CJK_JAPANESE_NOTO_SERIF,
        category="font",
        archive_name="font_cjk_japanese_noto_serif.zip",
        archive_sha256="8fa2df7dcebfd2cb2153afcae9a413891c69debbcc7ef6f60063b37dc9b96170",
        source_rel_path="fonts/cjk_japanese_noto_serif",
        target_rel_path="fonts/cjk_japanese_noto_serif",
        files=["bold.otf", "light.otf", "readme.txt", "regular.otf"],
    ),
    font_japanese_mplus_1p=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_MPLUS_1P,
        category="font",
        archive_name="font_japanese_mplus_1p.zip",
        archive_sha256="11bb62b652fe332fa8acd6353e6f9186d95d4273bdc4d708e7543ea4577be163",
        source_rel_path="fonts/japanese_mplus_1p",
        target_rel_path="fonts/japanese_mplus_1p",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_japanese_mplus_rounded1c=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_MPLUS_ROUNDED1C,
        category="font",
        archive_name="font_japanese_mplus_rounded1c.zip",
        archive_sha256="0feb1c4f6b7998d580fb24f33ab66a496c2e94c25be28996883dd3e1bbac3fda",
        source_rel_path="fonts/japanese_mplus_rounded1c",
        target_rel_path="fonts/japanese_mplus_rounded1c",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_japanese_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_NOTO_SANS,
        category="font",
        archive_name="font_japanese_noto_sans.zip",
        archive_sha256="3f7738b875e4f1260ed208aec56d551ac450a3e184413a45f54fb6a88e098a2f",
        source_rel_path="fonts/japanese_noto_sans",
        target_rel_path="fonts/japanese_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_japanese_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_NOTO_SERIF,
        category="font",
        archive_name="font_japanese_noto_serif.zip",
        archive_sha256="c6a3a7a6dd2cef871599a7b6b19d46466cc22450a7b842c6cda563c426533a83",
        source_rel_path="fonts/japanese_noto_serif",
        target_rel_path="fonts/japanese_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_japanese_sawarabi_gothic=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_SAWARABI_GOTHIC,
        category="font",
        archive_name="font_japanese_sawarabi_gothic.zip",
        archive_sha256="630c70b32c0d572eb5c0b9ec25d7a9771025bc7ec06933c4691cd78748f13e7e",
        source_rel_path="fonts/japanese_sawarabi_gothic",
        target_rel_path="fonts/japanese_sawarabi_gothic",
        files=["OFL.txt", "regular.ttf"],
    ),
    font_japanese_sawarabi_mincho=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_SAWARABI_MINCHO,
        category="font",
        archive_name="font_japanese_sawarabi_mincho.zip",
        archive_sha256="6b90555bbccbb30fc4fcd66b510a6d139811328c56c690fbd678fba30997ab2d",
        source_rel_path="fonts/japanese_sawarabi_mincho",
        target_rel_path="fonts/japanese_sawarabi_mincho",
        files=["OFL.txt", "regular.ttf"],
    ),
    font_korean_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_KOREAN_NOTO_SANS,
        category="font",
        archive_name="font_korean_noto_sans.zip",
        archive_sha256="0f964dd2843392befb85bb7e74303abc357e1645084abd78a7cdef82d6f9c226",
        source_rel_path="fonts/korean_noto_sans",
        target_rel_path="fonts/korean_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_korean_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_KOREAN_NOTO_SERIF,
        category="font",
        archive_name="font_korean_noto_serif.zip",
        archive_sha256="fa4a10937508c4c0ec0113ea88e22719ab084f690dcddf4107e6421980c4cb77",
        source_rel_path="fonts/korean_noto_serif",
        target_rel_path="fonts/korean_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_mono_courier=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_MONO_COURIER,
        category="font",
        archive_name="font_mono_courier.zip",
        archive_sha256="8bd2046daeed8cd4f98609f146ef60392d31bacd8cd3635a93f95a0f0d3f89c0",
        source_rel_path="fonts/mono_courier",
        target_rel_path="fonts/mono_courier",
        files=["OFL.txt", "bold.ttf", "regular.ttf"],
    ),
    font_mono_source_code_pro=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_MONO_SOURCE_CODE_PRO,
        category="font",
        archive_name="font_mono_source_code_pro.zip",
        archive_sha256="24229c659a1958790d216ac201541192066eb1149e8da07492747b9b48b2e9ce",
        source_rel_path="fonts/mono_source_code_pro",
        target_rel_path="fonts/mono_source_code_pro",
        files=["LICENSE.md", "README.md", "bold.otf", "light.otf", "regular.otf", "url.txt"],
    ),
    font_mono_source_han_code_jp=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_MONO_SOURCE_HAN_CODE_JP,
        category="font",
        archive_name="font_mono_source_han_code_jp.zip",
        archive_sha256="214eab8774510523f1428d0e84125a04c9533bf7012dc54415364de9961b80a2",
        source_rel_path="fonts/mono_source_han_code_jp",
        target_rel_path="fonts/mono_source_han_code_jp",
        files=["LICENSE.txt", "README-JP.md", "README.md", "bold.otf", "light.otf", "regular.otf", "relnotes.txt"],
    ),
    font_roboto=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO,
        category="font",
        archive_name="font_roboto.zip",
        archive_sha256="43b2adfe5105282507c13cd3187436b26af85a784160336fc5d48ea029d4aca6",
        source_rel_path="fonts/roboto",
        target_rel_path="fonts/roboto",
        files=["LICENSE.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_roboto_condensed=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_CONDENSED,
        category="font",
        archive_name="font_roboto_condensed.zip",
        archive_sha256="cd31a02acd032b82d8b6a933fecd6954e10d2282590e9ee86225097902efae81",
        source_rel_path="fonts/roboto_condensed",
        target_rel_path="fonts/roboto_condensed",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_roboto_mono=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_MONO,
        category="font",
        archive_name="font_roboto_mono.zip",
        archive_sha256="9574ee82125c8f062c0a9b15319e8455537babbf14387c6f1049675c8913f0bb",
        source_rel_path="fonts/roboto_mono",
        target_rel_path="fonts/roboto_mono",
        files=["LICENSE.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_roboto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_SERIF,
        category="font",
        archive_name="font_roboto_serif.zip",
        archive_sha256="eb144d96fb3bf028dbb25d603a139114dc36fd9bcc1c292490249c17ce9e808c",
        source_rel_path="fonts/roboto_serif",
        target_rel_path="fonts/roboto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_roboto_slab=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_SLAB,
        category="font",
        archive_name="font_roboto_slab.zip",
        archive_sha256="f373b04de9ee84b1dcd7398cf8b245e9bfd7bb615b9e902afd308e6fe8446e1c",
        source_rel_path="fonts/roboto_slab",
        target_rel_path="fonts/roboto_slab",
        files=["LICENSE.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_lato=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_LATO,
        category="font",
        archive_name="font_sans_lato.zip",
        archive_sha256="7309b68eee9b9c37cc606b38c8c0a1597cf7ad967a061cd2686749838f56a13f",
        source_rel_path="fonts/sans_lato",
        target_rel_path="fonts/sans_lato",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_monstserrat=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_MONSTSERRAT,
        category="font",
        archive_name="font_sans_monstserrat.zip",
        archive_sha256="e70eaf60e2553d574b68d4869e15f740fe2285a944ff232ac3707438d17319a8",
        source_rel_path="fonts/sans_monstserrat",
        target_rel_path="fonts/sans_monstserrat",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_open_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_OPEN_SANS,
        category="font",
        archive_name="font_sans_open_sans.zip",
        archive_sha256="84496a6d45d8d3cbaa6e529c07286c2e268507f661b2f356bf57187d6e779c34",
        source_rel_path="fonts/sans_open_sans",
        target_rel_path="fonts/sans_open_sans",
        files=["OFL.txt", "OpenSans-Bold.ttf", "OpenSans-Light.ttf", "OpenSans-Regular.ttf", "README.txt"],
    ),
    font_sans_oswald=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_OSWALD,
        category="font",
        archive_name="font_sans_oswald.zip",
        archive_sha256="2485a64a14ea4610557e5e7fd031442d03290a69aaab4572548b8096588e931f",
        source_rel_path="fonts/sans_oswald",
        target_rel_path="fonts/sans_oswald",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_poppins=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_POPPINS,
        category="font",
        archive_name="font_sans_poppins.zip",
        archive_sha256="e1e0f7ae5433c9cc645251bd64350d2bf9adbd41c4b898faf0742935ff2298d9",
        source_rel_path="fonts/sans_poppins",
        target_rel_path="fonts/sans_poppins",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_raleways=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_RALEWAYS,
        category="font",
        archive_name="font_sans_raleways.zip",
        archive_sha256="9185f50b2ef4fbaeb2d9d8cf4ec2528d53a4423f231353c9ee3d7c65075a465e",
        source_rel_path="fonts/sans_raleways",
        target_rel_path="fonts/sans_raleways",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_serif_merriweather=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SERIF_MERRIWEATHER,
        category="font",
        archive_name="font_serif_merriweather.zip",
        archive_sha256="1a67b556f2796d15f2a49efa335c955cb020e9a33b336ee09dc5f20c63156b02",
        source_rel_path="fonts/serif_merriweather",
        target_rel_path="fonts/serif_merriweather",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_serif_platypi=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SERIF_PLATYPI,
        category="font",
        archive_name="font_serif_platypi.zip",
        archive_sha256="4685831f67ce3f7437c4aba4474e987aaedeb28ada65f4173fc749ccbcdb0e1e",
        source_rel_path="fonts/serif_platypi",
        target_rel_path="fonts/serif_platypi",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_serif_playfairdisplay=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SERIF_PLAYFAIRDISPLAY,
        category="font",
        archive_name="font_serif_playfairdisplay.zip",
        archive_sha256="2fafbaba06f415651e41d75e2c712ae1b42b67a4506c582468c844c82b18e1a1",
        source_rel_path="fonts/serif_playfairdisplay",
        target_rel_path="fonts/serif_playfairdisplay",
        files=["OFL.txt", "README.txt", "bold.ttf", "regular.ttf"],
    ),
    font_thai_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_THAI_NOTO_SANS,
        category="font",
        archive_name="font_thai_noto_sans.zip",
        archive_sha256="92a7bd268a79af5a3577b9eee11c55675129df567a6c568615e7769de0fbfeda",
        source_rel_path="fonts/thai_noto_sans",
        target_rel_path="fonts/thai_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_thai_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_THAI_NOTO_SERIF,
        category="font",
        archive_name="font_thai_noto_serif.zip",
        archive_sha256="cc88579a84ecc0587c61bcd8974c98f45744bd51da993d38c684531e54af3206",
        source_rel_path="fonts/thai_noto_serif",
        target_rel_path="fonts/thai_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    icon_phosphor=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.ICON_PHOSPHOR,
        category="icon",
        archive_name="icon_phosphor.zip",
        archive_sha256="6f9d7687235decedd0f0bc72ca67d05ca28b9baaf0c520bd9cc2743d2c0b7715",
        source_rel_path="fonticons/phosphor",
        target_rel_path="fonticons/phosphor",
        files=[
            "LICENSE.txt",
            "bold.css",
            "bold.ttf",
            "fill.css",
            "fill.ttf",
            "light.css",
            "light.ttf",
            "regular.css",
            "regular.ttf",
            "thin.css",
            "thin.ttf",
            "version.txt",
        ],
    ),
    icon_gcp=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.ICON_GCP,
        category="icon",
        archive_name="icon_gcp.zip",
        archive_sha256="34e400995bfdc6cae891c01bab2cabfb4b368f0a12f7b09042b7570fbe0ae989",
        source_rel_path="icons/gcp",
        target_rel_path="icons/gcp",
        files=[
            "access_context_manager.png",
            "administration.png",
            "advanced_agent_modeling.png",
            "advanced_solutions_lab.png",
            "agent_assist.png",
            "ai_hub.png",
            "ai_hypercomputer.png",
            "ai_platform.png",
            "ai_platform_unified.png",
            "alloydb.png",
            "analytics_hub.png",
            "anthos.png",
            "anthos_config_management.png",
            "anthos_service_mesh.png",
            "api.png",
            "api_analytics.png",
            "api_monetization.png",
            "apigee.png",
            "apigee_api_platform.png",
            "apigee_sense.png",
            "app_engine.png",
            "artifact_registry.png",
            "asset_inventory.png",
            "assured_workloads.png",
            "automl.png",
            "automl_natural_language.png",
            "automl_tables.png",
            "automl_translation.png",
            "automl_video_intelligence.png",
            "automl_vision.png",
            "bare_metal_solutions.png",
            "batch.png",
            "beyondcorp.png",
            "bigquery.png",
            "bigtable.png",
            "billing.png",
            "binary_authorization.png",
            "catalog.png",
            "category_agents.png",
            "category_ai_machine_learning.png",
            "category_business_intelligence.png",
            "category_collaboration.png",
            "category_compute.png",
            "category_containers.png",
            "category_data_analytics.png",
            "category_databases.png",
            "category_developer_tools.png",
            "category_devops.png",
            "category_hybrid_multicloud.png",
            "category_integration_services.png",
            "category_management_tools.png",
            "category_maps_geospatial.png",
            "category_marketplace.png",
            "category_media_services.png",
            "category_migration.png",
            "category_mixed_reality.png",
            "category_networking.png",
            "category_observability.png",
            "category_operations.png",
            "category_security_identity.png",
            "category_serverless_computing.png",
            "category_storage.png",
            "category_web3.png",
            "category_web_mobile.png",
            "certificate_authority_service.png",
            "certificate_manager.png",
            "cloud_api_gateway.png",
            "cloud_apis.png",
            "cloud_armor.png",
            "cloud_asset_inventory.png",
            "cloud_audit_logs.png",
            "cloud_build.png",
            "cloud_cdn.png",
            "cloud_code.png",
            "cloud_composer.png",
            "cloud_data_fusion.png",
            "cloud_deploy.png",
            "cloud_deployment_manager.png",
            "cloud_dns.png",
            "cloud_domains.png",
            "cloud_ekm.png",
            "cloud_endpoints.png",
            "cloud_external_ip_addresses.png",
            "cloud_firewall_rules.png",
            "cloud_for_marketing.png",
            "cloud_functions.png",
            "cloud_generic.png",
            "cloud_gpu.png",
            "cloud_healthcare_api.png",
            "cloud_healthcare_marketplace.png",
            "cloud_hsm.png",
            "cloud_ids.png",
            "cloud_inference_api.png",
            "cloud_interconnect.png",
            "cloud_jobs_api.png",
            "cloud_load_balancing.png",
            "cloud_logging.png",
            "cloud_media_edge.png",
            "cloud_monitoring.png",
            "cloud_nat.png",
            "cloud_natural_language_api.png",
            "cloud_network.png",
            "cloud_ops.png",
            "cloud_optimization_ai.png",
            "cloud_optimization_ai_fleet_routing_api.png",
            "cloud_router.png",
            "cloud_routes.png",
            "cloud_run.png",
            "cloud_run_for_anthos.png",
            "cloud_scheduler.png",
            "cloud_security_scanner.png",
            "cloud_shell.png",
            "cloud_spanner.png",
            "cloud_sql.png",
            "cloud_storage.png",
            "cloud_tasks.png",
            "cloud_test_lab.png",
            "cloud_tpu.png",
            "cloud_translation_api.png",
            "cloud_vision_api.png",
            "cloud_vpn.png",
            "compute_engine.png",
            "configuration_management.png",
            "connectivity_test.png",
            "connectors.png",
            "contact_center_ai.png",
            "container_optimized_os.png",
            "container_registry.png",
            "data_catalog.png",
            "data_labeling.png",
            "data_layers.png",
            "data_loss_prevention_api.png",
            "data_qna.png",
            "data_studio.png",
            "data_transfer.png",
            "database_migration_service.png",
            "dataflow.png",
            "datalab.png",
            "dataplex.png",
            "datapol.png",
            "dataprep.png",
            "dataproc.png",
            "dataproc_metastore.png",
            "datashare.png",
            "datastore.png",
            "datastream.png",
            "debugger.png",
            "developer_portal.png",
            "dialogflow.png",
            "dialogflow_cx.png",
            "dialogflow_insights.png",
            "distributed_cloud.png",
            "document_ai.png",
            "early_access_center.png",
            "error_reporting.png",
            "eventarc.png",
            "filestore.png",
            "financial_services_marketplace.png",
            "firestore.png",
            "fleet_engine.png",
            "free_trial.png",
            "functions.png",
            "game_servers.png",
            "gce.png",
            "gce_systems_management.png",
            "gcs.png",
            "genomics.png",
            "gke.png",
            "gke_on_prem.png",
            "google_cloud_marketplace.png",
            "google_kubernetes_engine.png",
            "google_maps_platform.png",
            "healthcare_nlp_api.png",
            "home.png",
            "hyperdisk.png",
            "iam.png",
            "identity_and_access_management.png",
            "identity_aware_proxy.png",
            "identity_platform.png",
            "iot_core.png",
            "iot_edge.png",
            "key_access_justifications.png",
            "key_management_service.png",
            "kms.png",
            "kuberun.png",
            "launcher.png",
            "local_ssd.png",
            "looker.png",
            "managed_service_for_microsoft_active_directory.png",
            "mandiant.png",
            "manifest.json",
            "media_translation_api.png",
            "memorystore.png",
            "migrate_for_anthos.png",
            "migrate_for_compute_engine.png",
            "my_cloud.png",
            "network_connectivity_center.png",
            "network_intelligence_center.png",
            "network_security.png",
            "network_tiers.png",
            "network_topology.png",
            "onboarding.png",
            "os_configuration_management.png",
            "os_inventory_management.png",
            "os_patch_management.png",
            "partner_interconnect.png",
            "partner_portal.png",
            "performance_dashboard.png",
            "permissions.png",
            "persistent_disk.png",
            "phishing_protection.png",
            "policy_analyzer.png",
            "premium_network_tier.png",
            "private_connectivity.png",
            "private_service_connect.png",
            "producer_portal.png",
            "profiler.png",
            "project.png",
            "pubsub.png",
            "quantum_engine.png",
            "quotas.png",
            "real_world_insights.png",
            "recommendations_ai.png",
            "release_notes.png",
            "retail_api.png",
            "risk_manager.png",
            "runtime_config.png",
            "secret_manager.png",
            "security.png",
            "security_command_center.png",
            "security_health_advisor.png",
            "security_key_enforcement.png",
            "security_operations.png",
            "service_discovery.png",
            "speech_to_text.png",
            "stackdriver.png",
            "standard_network_tier.png",
            "stream_suite.png",
            "support.png",
            "tensorflow_enterprise.png",
            "text_to_speech.png",
            "threat_intelligence.png",
            "tools_for_powershell.png",
            "trace.png",
            "traffic_director.png",
            "transfer.png",
            "transfer_appliance.png",
            "user_preferences.png",
            "vertex_ai.png",
            "vertexai.png",
            "video_intelligence_api.png",
            "virtual_private_cloud.png",
            "visual_inspection.png",
            "vmware_engine.png",
            "vpc.png",
            "web_risk.png",
            "web_security_scanner.png",
            "workflows.png",
            "workload_identity_pool.png",
        ],
    ),
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
            zinfo.external_attr = 0o644 << 16
            zf.writestr(zinfo, data)
    return buf.getvalue()


def get_all_release_asset_packages() -> list[ReleaseAssetPackage]:
    """Retrieve all defined release asset packages.

    Returns:
        list[ReleaseAssetPackage]: Combined list of font and icon packages.
    """
    return RELEASE_ASSET_PACKAGES.all()


def get_font_asset_packages() -> list[ReleaseAssetPackage]:
    """Retrieve all font asset packages.

    Returns:
        list[ReleaseAssetPackage]: List of font package definitions.
    """
    return [pkg for pkg in RELEASE_ASSET_PACKAGES.values() if pkg.category == "font"]


def get_icon_asset_packages() -> list[ReleaseAssetPackage]:
    """Retrieve all icon asset packages.

    Returns:
        list[ReleaseAssetPackage]: List of icon package definitions.
    """
    return [pkg for pkg in RELEASE_ASSET_PACKAGES.values() if pkg.category == "icon"]


def find_package_by_name(package_name: str | ReleaseAssetPackageName) -> ReleaseAssetPackage | None:
    """Find an asset package by its unique package identifier, enum, or archive name.

    Args:
        package_name: The package identifier or enum (e.g. 'font_roboto', 'font_roboto.zip').

    Returns:
        ReleaseAssetPackage | None: The matching package if found, otherwise None.
    """
    name_str = package_name.value if isinstance(package_name, ReleaseAssetPackageName) else str(package_name)
    if name_str in RELEASE_ASSET_PACKAGES:
        return RELEASE_ASSET_PACKAGES[name_str]
    for pkg in RELEASE_ASSET_PACKAGES.values():
        if pkg.archive_name == name_str:
            return pkg
    return None


def find_package_for_font_path(font_file_path: str) -> ReleaseAssetPackage | None:
    """Identify which asset package contains a given font resource path.

    Args:
        font_file_path: Relative font path (e.g. 'roboto/regular.ttf' or 'fonts/roboto/regular.ttf').

    Returns:
        ReleaseAssetPackage | None: The containing package if matched, otherwise None.
    """
    normalized = font_file_path.strip("/").removeprefix("fonts/")
    family = normalized.split("/")[0] if "/" in normalized else normalized
    target_name = f"font_{family}"
    return RELEASE_ASSET_PACKAGES.get(target_name)


def find_package_for_icon_path(icon_file_path: str) -> ReleaseAssetPackage | None:
    """Identify which asset package contains a given icon resource path.

    Args:
        icon_file_path: Relative icon path
            (e.g. 'phosphor/thin.ttf', 'fonticons/phosphor/thin.ttf', 'icons/gcp/gce.png').

    Returns:
        ReleaseAssetPackage | None: The containing package if matched, otherwise None.
    """
    normalized = icon_file_path.strip("/").removeprefix("fonticons/").removeprefix("icons/")
    family = normalized.split("/")[0] if "/" in normalized else normalized
    target_name = f"icon_{family}"
    return RELEASE_ASSET_PACKAGES.get(target_name)


def find_package_for_resource_path(resource_path: str) -> ReleaseAssetPackage | None:
    """Identify which asset package contains a given resource path (font or icon).

    Args:
        resource_path: Relative resource path
            (e.g. 'fonts/roboto/regular.ttf', 'fonticons/phosphor/thin.ttf', 'icons/gcp/gce.png').

    Returns:
        ReleaseAssetPackage | None: The containing package if matched, otherwise None.
    """
    norm = resource_path.strip("/")
    if norm.startswith("fonticons/") or norm.startswith("phosphor/"):
        return find_package_for_icon_path(norm)
    if norm.startswith("icons/") or norm.startswith("gcp/"):
        return find_package_for_icon_path(norm)
    return find_package_for_font_path(norm)


def ensure_asset_available(resource_path: str, tag: str = DEFAULT_RELEASE_TAG) -> None:
    """Ensure that the asset file for a given resource path is downloaded and available.

    Args:
        resource_path: Relative path to font or icon file.
        tag: Release tag to download from if missing. Defaults to DEFAULT_RELEASE_TAG.

    Raises:
        ValueError: If no release asset package matches the resource path.
        RuntimeError: If downloading or extracting the package fails.
    """
    pkg = find_package_for_resource_path(resource_path)
    if pkg is None:
        raise ValueError(f"No release asset package found for resource path '{resource_path}'.")

    if not pkg.is_downloaded():
        pkg.download_and_extract(tag=tag)


def download_all_release_assets(tag: str = DEFAULT_RELEASE_TAG, force: bool = False) -> None:
    """Download and extract all defined release asset packages (fonts and icons).

    Args:
        tag: Release tag to download from. Defaults to DEFAULT_RELEASE_TAG.
        force: If True, force re-download even if already present.
    """
    for pkg in RELEASE_ASSET_PACKAGES.values():
        pkg.download_and_extract(tag=tag, force=force)


def get_release_asset_manifest(tag: str = DEFAULT_RELEASE_TAG) -> AssetManifest:
    """Generate complete release manifest from defined packages.

    Args:
        tag: Release version tag. Defaults to DEFAULT_RELEASE_TAG.

    Returns:
        AssetManifest: Populated release manifest.
    """
    assets = {
        pkg.archive_name: AssetManifestItem(
            archive_name=pkg.archive_name,
            sha256=pkg.archive_sha256,
            size=0,
        )
        for pkg in RELEASE_ASSET_PACKAGES.values()
    }
    return AssetManifest(version=tag, assets=assets)
