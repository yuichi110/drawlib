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

from enum import StrEnum
from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field


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


class ReleaseAssetPackage(BaseModel):
    """Data model representing a downloadable release asset package.

    Attributes:
        name: Unique package identifier, e.g. 'font_roboto'.
        category: Category of the asset package ('font' or 'icon').
        archive_name: ZIP archive file name, e.g. 'font_roboto.zip'.
        source_rel_path: Relative path within release_assets/<ver>/, e.g. 'fonts/roboto'.
        target_rel_path: Relative path where the asset is extracted locally.
        files: List of file names contained within this asset package.
    """

    model_config = ConfigDict(frozen=True)

    name: ReleaseAssetPackageName = Field(description="Unique package identifier, e.g. 'font_roboto'.")
    category: Literal["font", "icon"] = Field(description="Category of the asset package ('font' or 'icon').")
    archive_name: str = Field(description="ZIP archive file name, e.g. 'font_roboto.zip'.")
    source_rel_path: str = Field(
        description="Relative path within release_assets/<ver>/, e.g. 'fonts/roboto'.",
    )
    target_rel_path: str = Field(
        description="Relative path where the asset is extracted locally, e.g. 'fonts/roboto'.",
    )
    files: list[str] = Field(
        description="List of file names contained within this asset package.",
    )

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
        source_rel_path="fonts/arabic_noto_kufi",
        target_rel_path="fonts/arabic_noto_kufi",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_arabic_noto_naskh=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ARABIC_NOTO_NASKH,
        category="font",
        archive_name="font_arabic_noto_naskh.zip",
        source_rel_path="fonts/arabic_noto_naskh",
        target_rel_path="fonts/arabic_noto_naskh",
        files=["OFL.txt", "README.txt", "bold.ttf", "regular.ttf"],
    ),
    font_arabic_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ARABIC_NOTO_SANS,
        category="font",
        archive_name="font_arabic_noto_sans.zip",
        source_rel_path="fonts/arabic_noto_sans",
        target_rel_path="fonts/arabic_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_bengali_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_BENGALI_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_bengali_noto_sans.zip",
        source_rel_path="fonts/brahmic_bengali_noto_sans",
        target_rel_path="fonts/brahmic_bengali_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_bengali_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_BENGALI_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_bengali_noto_serif.zip",
        source_rel_path="fonts/brahmic_bengali_noto_serif",
        target_rel_path="fonts/brahmic_bengali_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_devanagari_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_DEVANAGARI_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_devanagari_noto_sans.zip",
        source_rel_path="fonts/brahmic_devanagari_noto_sans",
        target_rel_path="fonts/brahmic_devanagari_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_devanagari_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_DEVANAGARI_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_devanagari_noto_serif.zip",
        source_rel_path="fonts/brahmic_devanagari_noto_serif",
        target_rel_path="fonts/brahmic_devanagari_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_tamil_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TAMIL_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_tamil_noto_sans.zip",
        source_rel_path="fonts/brahmic_tamil_noto_sans",
        target_rel_path="fonts/brahmic_tamil_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_tamil_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TAMIL_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_tamil_noto_serif.zip",
        source_rel_path="fonts/brahmic_tamil_noto_serif",
        target_rel_path="fonts/brahmic_tamil_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_telugu_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TELUGU_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_telugu_noto_sans.zip",
        source_rel_path="fonts/brahmic_telugu_noto_sans",
        target_rel_path="fonts/brahmic_telugu_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_brahmic_telugu_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TELUGU_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_telugu_noto_serif.zip",
        source_rel_path="fonts/brahmic_telugu_noto_serif",
        target_rel_path="fonts/brahmic_telugu_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_hongkong_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_HONGKONG_NOTO_SANS,
        category="font",
        archive_name="font_chinese_hongkong_noto_sans.zip",
        source_rel_path="fonts/chinese_hongkong_noto_sans",
        target_rel_path="fonts/chinese_hongkong_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_hongkong_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_HONGKONG_NOTO_SERIF,
        category="font",
        archive_name="font_chinese_hongkong_noto_serif.zip",
        source_rel_path="fonts/chinese_hongkong_noto_serif",
        target_rel_path="fonts/chinese_hongkong_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_simplified_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_SIMPLIFIED_NOTO_SANS,
        category="font",
        archive_name="font_chinese_simplified_noto_sans.zip",
        source_rel_path="fonts/chinese_simplified_noto_sans",
        target_rel_path="fonts/chinese_simplified_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_simplified_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_SIMPLIFIED_NOTO_SERIF,
        category="font",
        archive_name="font_chinese_simplified_noto_serif.zip",
        source_rel_path="fonts/chinese_simplified_noto_serif",
        target_rel_path="fonts/chinese_simplified_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_traditional_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_TRADITIONAL_NOTO_SANS,
        category="font",
        archive_name="font_chinese_traditional_noto_sans.zip",
        source_rel_path="fonts/chinese_traditional_noto_sans",
        target_rel_path="fonts/chinese_traditional_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_chinese_traditional_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_TRADITIONAL_NOTO_SERIF,
        category="font",
        archive_name="font_chinese_traditional_noto_serif.zip",
        source_rel_path="fonts/chinese_traditional_noto_serif",
        target_rel_path="fonts/chinese_traditional_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_cjk_japanese_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CJK_JAPANESE_NOTO_SANS,
        category="font",
        archive_name="font_cjk_japanese_noto_sans.zip",
        source_rel_path="fonts/cjk_japanese_noto_sans",
        target_rel_path="fonts/cjk_japanese_noto_sans",
        files=["bold.otf", "light.otf", "readme.txt", "regular.otf"],
    ),
    font_cjk_japanese_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CJK_JAPANESE_NOTO_SERIF,
        category="font",
        archive_name="font_cjk_japanese_noto_serif.zip",
        source_rel_path="fonts/cjk_japanese_noto_serif",
        target_rel_path="fonts/cjk_japanese_noto_serif",
        files=["bold.otf", "light.otf", "readme.txt", "regular.otf"],
    ),
    font_japanese_mplus_1p=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_MPLUS_1P,
        category="font",
        archive_name="font_japanese_mplus_1p.zip",
        source_rel_path="fonts/japanese_mplus_1p",
        target_rel_path="fonts/japanese_mplus_1p",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_japanese_mplus_rounded1c=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_MPLUS_ROUNDED1C,
        category="font",
        archive_name="font_japanese_mplus_rounded1c.zip",
        source_rel_path="fonts/japanese_mplus_rounded1c",
        target_rel_path="fonts/japanese_mplus_rounded1c",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_japanese_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_NOTO_SANS,
        category="font",
        archive_name="font_japanese_noto_sans.zip",
        source_rel_path="fonts/japanese_noto_sans",
        target_rel_path="fonts/japanese_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_japanese_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_NOTO_SERIF,
        category="font",
        archive_name="font_japanese_noto_serif.zip",
        source_rel_path="fonts/japanese_noto_serif",
        target_rel_path="fonts/japanese_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_japanese_sawarabi_gothic=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_SAWARABI_GOTHIC,
        category="font",
        archive_name="font_japanese_sawarabi_gothic.zip",
        source_rel_path="fonts/japanese_sawarabi_gothic",
        target_rel_path="fonts/japanese_sawarabi_gothic",
        files=["OFL.txt", "regular.ttf"],
    ),
    font_japanese_sawarabi_mincho=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_SAWARABI_MINCHO,
        category="font",
        archive_name="font_japanese_sawarabi_mincho.zip",
        source_rel_path="fonts/japanese_sawarabi_mincho",
        target_rel_path="fonts/japanese_sawarabi_mincho",
        files=["OFL.txt", "regular.ttf"],
    ),
    font_korean_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_KOREAN_NOTO_SANS,
        category="font",
        archive_name="font_korean_noto_sans.zip",
        source_rel_path="fonts/korean_noto_sans",
        target_rel_path="fonts/korean_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_korean_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_KOREAN_NOTO_SERIF,
        category="font",
        archive_name="font_korean_noto_serif.zip",
        source_rel_path="fonts/korean_noto_serif",
        target_rel_path="fonts/korean_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_mono_courier=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_MONO_COURIER,
        category="font",
        archive_name="font_mono_courier.zip",
        source_rel_path="fonts/mono_courier",
        target_rel_path="fonts/mono_courier",
        files=["OFL.txt", "bold.ttf", "regular.ttf"],
    ),
    font_mono_source_code_pro=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_MONO_SOURCE_CODE_PRO,
        category="font",
        archive_name="font_mono_source_code_pro.zip",
        source_rel_path="fonts/mono_source_code_pro",
        target_rel_path="fonts/mono_source_code_pro",
        files=["LICENSE.md", "README.md", "bold.otf", "light.otf", "regular.otf", "url.txt"],
    ),
    font_mono_source_han_code_jp=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_MONO_SOURCE_HAN_CODE_JP,
        category="font",
        archive_name="font_mono_source_han_code_jp.zip",
        source_rel_path="fonts/mono_source_han_code_jp",
        target_rel_path="fonts/mono_source_han_code_jp",
        files=["LICENSE.txt", "README-JP.md", "README.md", "bold.otf", "light.otf", "regular.otf", "relnotes.txt"],
    ),
    font_roboto=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO,
        category="font",
        archive_name="font_roboto.zip",
        source_rel_path="fonts/roboto",
        target_rel_path="fonts/roboto",
        files=["LICENSE.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_roboto_condensed=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_CONDENSED,
        category="font",
        archive_name="font_roboto_condensed.zip",
        source_rel_path="fonts/roboto_condensed",
        target_rel_path="fonts/roboto_condensed",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_roboto_mono=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_MONO,
        category="font",
        archive_name="font_roboto_mono.zip",
        source_rel_path="fonts/roboto_mono",
        target_rel_path="fonts/roboto_mono",
        files=["LICENSE.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_roboto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_SERIF,
        category="font",
        archive_name="font_roboto_serif.zip",
        source_rel_path="fonts/roboto_serif",
        target_rel_path="fonts/roboto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_roboto_slab=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_SLAB,
        category="font",
        archive_name="font_roboto_slab.zip",
        source_rel_path="fonts/roboto_slab",
        target_rel_path="fonts/roboto_slab",
        files=["LICENSE.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_lato=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_LATO,
        category="font",
        archive_name="font_sans_lato.zip",
        source_rel_path="fonts/sans_lato",
        target_rel_path="fonts/sans_lato",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_monstserrat=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_MONSTSERRAT,
        category="font",
        archive_name="font_sans_monstserrat.zip",
        source_rel_path="fonts/sans_monstserrat",
        target_rel_path="fonts/sans_monstserrat",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_open_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_OPEN_SANS,
        category="font",
        archive_name="font_sans_open_sans.zip",
        source_rel_path="fonts/sans_open_sans",
        target_rel_path="fonts/sans_open_sans",
        files=["OFL.txt", "OpenSans-Bold.ttf", "OpenSans-Light.ttf", "OpenSans-Regular.ttf", "README.txt"],
    ),
    font_sans_oswald=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_OSWALD,
        category="font",
        archive_name="font_sans_oswald.zip",
        source_rel_path="fonts/sans_oswald",
        target_rel_path="fonts/sans_oswald",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_poppins=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_POPPINS,
        category="font",
        archive_name="font_sans_poppins.zip",
        source_rel_path="fonts/sans_poppins",
        target_rel_path="fonts/sans_poppins",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_sans_raleways=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_RALEWAYS,
        category="font",
        archive_name="font_sans_raleways.zip",
        source_rel_path="fonts/sans_raleways",
        target_rel_path="fonts/sans_raleways",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_serif_merriweather=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SERIF_MERRIWEATHER,
        category="font",
        archive_name="font_serif_merriweather.zip",
        source_rel_path="fonts/serif_merriweather",
        target_rel_path="fonts/serif_merriweather",
        files=["OFL.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_serif_platypi=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SERIF_PLATYPI,
        category="font",
        archive_name="font_serif_platypi.zip",
        source_rel_path="fonts/serif_platypi",
        target_rel_path="fonts/serif_platypi",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_serif_playfairdisplay=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SERIF_PLAYFAIRDISPLAY,
        category="font",
        archive_name="font_serif_playfairdisplay.zip",
        source_rel_path="fonts/serif_playfairdisplay",
        target_rel_path="fonts/serif_playfairdisplay",
        files=["OFL.txt", "README.txt", "bold.ttf", "regular.ttf"],
    ),
    font_thai_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_THAI_NOTO_SANS,
        category="font",
        archive_name="font_thai_noto_sans.zip",
        source_rel_path="fonts/thai_noto_sans",
        target_rel_path="fonts/thai_noto_sans",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    font_thai_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_THAI_NOTO_SERIF,
        category="font",
        archive_name="font_thai_noto_serif.zip",
        source_rel_path="fonts/thai_noto_serif",
        target_rel_path="fonts/thai_noto_serif",
        files=["OFL.txt", "README.txt", "bold.ttf", "light.ttf", "regular.ttf"],
    ),
    icon_phosphor=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.ICON_PHOSPHOR,
        category="icon",
        archive_name="icon_phosphor.zip",
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
)


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
