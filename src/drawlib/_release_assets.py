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
archive structures, and contained files for fonts, icons, and maps.

Architectural Note (Do Not Move):
    This module is intentionally placed at the top level of `src/drawlib/` as a
    human- and tool-visible manifest definition table. AI coding agents and
    developers must NOT relocate or hide this file inside `drawlib._core`
    (`l1_core`, `l3_external`, etc.).
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

from drawlib._core.l3_external._package import (
    AssetManifest,
    AssetManifestItem,
    BaseReleaseAssetPackages,
    ReleaseAssetPackage,
    create_deterministic_zip_bytes,
)

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
    MAP_CITIES = "map_cities"
    MAP_COUNTRIES = "map_countries"
    MAP_WORLD = "map_world"


class ReleaseAssetPackages(BaseReleaseAssetPackages):
    """Container holding all release asset package definitions with full IDE type completion.

    Each package is exposed as a typed field for IDE autocompletion, while also
    providing dict-like item access, iteration, and lookup utilities.
    """

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
    map_cities: ReleaseAssetPackage
    map_countries: ReleaseAssetPackage
    map_world: ReleaseAssetPackage


# ==============================================================================
# Single Source of Truth (SoT): Explicit Asset Package Definitions
# ==============================================================================

RELEASE_ASSET_PACKAGES: Final[ReleaseAssetPackages] = ReleaseAssetPackages(
    font_arabic_noto_kufi=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ARABIC_NOTO_KUFI,
        category="font",
        archive_name="font_arabic_noto_kufi.zip",
        archive_sha256="7054fa6de8a5a410e1f963eb04144ade5d1df07dc647e85ddcecec282bbc6654",
        source_rel_path="fonts/arabic_noto_kufi",
        target_rel_path="fonts/arabic_noto_kufi",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_arabic_noto_naskh=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ARABIC_NOTO_NASKH,
        category="font",
        archive_name="font_arabic_noto_naskh.zip",
        archive_sha256="bcb55fd6bcd31926616c8ace47051b4b9c02f97a01927df6b1348fdc241959c9",
        source_rel_path="fonts/arabic_noto_naskh",
        target_rel_path="fonts/arabic_noto_naskh",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf"),
    ),
    font_arabic_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ARABIC_NOTO_SANS,
        category="font",
        archive_name="font_arabic_noto_sans.zip",
        archive_sha256="c3f4992bbae13c47ab9ca03dac20902705ba7875825094de3f6d3767ec8ca123",
        source_rel_path="fonts/arabic_noto_sans",
        target_rel_path="fonts/arabic_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_brahmic_bengali_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_BENGALI_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_bengali_noto_sans.zip",
        archive_sha256="58c81a64a7cede39c08061551de38c56d44988f5c5771003a324612101edff08",
        source_rel_path="fonts/brahmic_bengali_noto_sans",
        target_rel_path="fonts/brahmic_bengali_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_brahmic_bengali_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_BENGALI_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_bengali_noto_serif.zip",
        archive_sha256="58353474a2de6ee4d4f264de43840ddd3b7e629cdde1147ba3faa78cb45b568e",
        source_rel_path="fonts/brahmic_bengali_noto_serif",
        target_rel_path="fonts/brahmic_bengali_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_brahmic_devanagari_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_DEVANAGARI_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_devanagari_noto_sans.zip",
        archive_sha256="5126b3a2d7f633ffb11c1ecb06ad5e228ba7daf882a9a098c5730f2cd677a3f4",
        source_rel_path="fonts/brahmic_devanagari_noto_sans",
        target_rel_path="fonts/brahmic_devanagari_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_brahmic_devanagari_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_DEVANAGARI_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_devanagari_noto_serif.zip",
        archive_sha256="3c1818912177c94530cd530a36bb7be1df6fd100b84901e2ebf2d90fe9159c34",
        source_rel_path="fonts/brahmic_devanagari_noto_serif",
        target_rel_path="fonts/brahmic_devanagari_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_brahmic_tamil_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TAMIL_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_tamil_noto_sans.zip",
        archive_sha256="a47e2cc36980e3e4c8554c11e4d2a0ff3d2a6e41e5532a242e87958e6bb59b25",
        source_rel_path="fonts/brahmic_tamil_noto_sans",
        target_rel_path="fonts/brahmic_tamil_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_brahmic_tamil_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TAMIL_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_tamil_noto_serif.zip",
        archive_sha256="009b4e3d1792cba3e2382c5ffdbf6f3881a22fb6a953c0cbb1113c157c80b016",
        source_rel_path="fonts/brahmic_tamil_noto_serif",
        target_rel_path="fonts/brahmic_tamil_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_brahmic_telugu_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TELUGU_NOTO_SANS,
        category="font",
        archive_name="font_brahmic_telugu_noto_sans.zip",
        archive_sha256="5ae660080cf0911cc553e68a282a8cfeee26bdcf1675bc77b4e8b687b7a60d8a",
        source_rel_path="fonts/brahmic_telugu_noto_sans",
        target_rel_path="fonts/brahmic_telugu_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_brahmic_telugu_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_BRAHMIC_TELUGU_NOTO_SERIF,
        category="font",
        archive_name="font_brahmic_telugu_noto_serif.zip",
        archive_sha256="d7cf58f56b1895e9a3b934deb1aab6ab21e5f246c79227d3cb4cc337f2fc479d",
        source_rel_path="fonts/brahmic_telugu_noto_serif",
        target_rel_path="fonts/brahmic_telugu_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_chinese_hongkong_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_HONGKONG_NOTO_SANS,
        category="font",
        archive_name="font_chinese_hongkong_noto_sans.zip",
        archive_sha256="150d302fb90af2ffe360a12ca1d8c845f53ab7dc107f827d7fc1af8606f6bb11",
        source_rel_path="fonts/chinese_hongkong_noto_sans",
        target_rel_path="fonts/chinese_hongkong_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_chinese_hongkong_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_HONGKONG_NOTO_SERIF,
        category="font",
        archive_name="font_chinese_hongkong_noto_serif.zip",
        archive_sha256="20807fe65bb4a4614358bafaa7bc8b9ecb6f6d802b1115c76f8045f0f946d839",
        source_rel_path="fonts/chinese_hongkong_noto_serif",
        target_rel_path="fonts/chinese_hongkong_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_chinese_simplified_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_SIMPLIFIED_NOTO_SANS,
        category="font",
        archive_name="font_chinese_simplified_noto_sans.zip",
        archive_sha256="510e1f30dab17b2909043f3442d65b19f87fa195360ba0db0daa22e4298ea2ad",
        source_rel_path="fonts/chinese_simplified_noto_sans",
        target_rel_path="fonts/chinese_simplified_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_chinese_simplified_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_SIMPLIFIED_NOTO_SERIF,
        category="font",
        archive_name="font_chinese_simplified_noto_serif.zip",
        archive_sha256="a458b8984c7c388af33d81bbfbd332bb75d6619d9ed2b03a2b2fb22486650836",
        source_rel_path="fonts/chinese_simplified_noto_serif",
        target_rel_path="fonts/chinese_simplified_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_chinese_traditional_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_TRADITIONAL_NOTO_SANS,
        category="font",
        archive_name="font_chinese_traditional_noto_sans.zip",
        archive_sha256="d3ba673eaf06553ac49e1c18365580b9ca4e10f2584e95e425bc728e7b32be31",
        source_rel_path="fonts/chinese_traditional_noto_sans",
        target_rel_path="fonts/chinese_traditional_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_chinese_traditional_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CHINESE_TRADITIONAL_NOTO_SERIF,
        category="font",
        archive_name="font_chinese_traditional_noto_serif.zip",
        archive_sha256="89ca783a854355015709479405e123f47d5dba3718ac14f3fd878c3a23fa4420",
        source_rel_path="fonts/chinese_traditional_noto_serif",
        target_rel_path="fonts/chinese_traditional_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_cjk_japanese_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CJK_JAPANESE_NOTO_SANS,
        category="font",
        archive_name="font_cjk_japanese_noto_sans.zip",
        archive_sha256="3aefb1bc51e0c8fc712e0e020d322363dea6a54ff064df5f578a7f54cfaa983a",
        source_rel_path="fonts/cjk_japanese_noto_sans",
        target_rel_path="fonts/cjk_japanese_noto_sans",
        files=("bold.otf", "readme.txt", "regular.otf", "thin.otf"),
    ),
    font_cjk_japanese_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_CJK_JAPANESE_NOTO_SERIF,
        category="font",
        archive_name="font_cjk_japanese_noto_serif.zip",
        archive_sha256="58c1245c6144347b009c891041410cf65d9f78c2303e578c6d21ba58683ae015",
        source_rel_path="fonts/cjk_japanese_noto_serif",
        target_rel_path="fonts/cjk_japanese_noto_serif",
        files=("bold.otf", "readme.txt", "regular.otf", "thin.otf"),
    ),
    font_japanese_mplus_1p=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_MPLUS_1P,
        category="font",
        archive_name="font_japanese_mplus_1p.zip",
        archive_sha256="b6a865e4bde2ab2113310c31493543c73400d3622f668c2c69a40a90cc2d701f",
        source_rel_path="fonts/japanese_mplus_1p",
        target_rel_path="fonts/japanese_mplus_1p",
        files=("OFL.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_japanese_mplus_rounded1c=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_MPLUS_ROUNDED1C,
        category="font",
        archive_name="font_japanese_mplus_rounded1c.zip",
        archive_sha256="a7081b47470808c4faa14d4d9f44df2cd96c91b05823bf411668741c65ab5157",
        source_rel_path="fonts/japanese_mplus_rounded1c",
        target_rel_path="fonts/japanese_mplus_rounded1c",
        files=("OFL.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_japanese_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_NOTO_SANS,
        category="font",
        archive_name="font_japanese_noto_sans.zip",
        archive_sha256="c399f3ca1311ab0cb4e1137aea5667a20c198c5d7ee584e47dfc08f5d9de020d",
        source_rel_path="fonts/japanese_noto_sans",
        target_rel_path="fonts/japanese_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_japanese_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_NOTO_SERIF,
        category="font",
        archive_name="font_japanese_noto_serif.zip",
        archive_sha256="88ff2c8d9984d15624d49908fd6c12ccbf8bdf1366c560993eeb276e1e07cc57",
        source_rel_path="fonts/japanese_noto_serif",
        target_rel_path="fonts/japanese_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_japanese_sawarabi_gothic=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_SAWARABI_GOTHIC,
        category="font",
        archive_name="font_japanese_sawarabi_gothic.zip",
        archive_sha256="630c70b32c0d572eb5c0b9ec25d7a9771025bc7ec06933c4691cd78748f13e7e",
        source_rel_path="fonts/japanese_sawarabi_gothic",
        target_rel_path="fonts/japanese_sawarabi_gothic",
        files=("OFL.txt", "regular.ttf"),
    ),
    font_japanese_sawarabi_mincho=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_JAPANESE_SAWARABI_MINCHO,
        category="font",
        archive_name="font_japanese_sawarabi_mincho.zip",
        archive_sha256="6b90555bbccbb30fc4fcd66b510a6d139811328c56c690fbd678fba30997ab2d",
        source_rel_path="fonts/japanese_sawarabi_mincho",
        target_rel_path="fonts/japanese_sawarabi_mincho",
        files=("OFL.txt", "regular.ttf"),
    ),
    font_korean_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_KOREAN_NOTO_SANS,
        category="font",
        archive_name="font_korean_noto_sans.zip",
        archive_sha256="fddcc8a3fa84993625cfed095933befb401a80a2c8277cba986975d4a3b4767b",
        source_rel_path="fonts/korean_noto_sans",
        target_rel_path="fonts/korean_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_korean_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_KOREAN_NOTO_SERIF,
        category="font",
        archive_name="font_korean_noto_serif.zip",
        archive_sha256="e716a401ad779407403b7e0544ce40d889aa0be2b410394f1ff312ae2c952e5a",
        source_rel_path="fonts/korean_noto_serif",
        target_rel_path="fonts/korean_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_mono_courier=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_MONO_COURIER,
        category="font",
        archive_name="font_mono_courier.zip",
        archive_sha256="8bd2046daeed8cd4f98609f146ef60392d31bacd8cd3635a93f95a0f0d3f89c0",
        source_rel_path="fonts/mono_courier",
        target_rel_path="fonts/mono_courier",
        files=("OFL.txt", "bold.ttf", "regular.ttf"),
    ),
    font_mono_source_code_pro=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_MONO_SOURCE_CODE_PRO,
        category="font",
        archive_name="font_mono_source_code_pro.zip",
        archive_sha256="6f541570f188941ca7be6e2a162c17dc587aa26160f5c7f2ad456ed0adf12479",
        source_rel_path="fonts/mono_source_code_pro",
        target_rel_path="fonts/mono_source_code_pro",
        files=("LICENSE.md", "README.md", "bold.otf", "regular.otf", "thin.otf", "url.txt"),
    ),
    font_mono_source_han_code_jp=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_MONO_SOURCE_HAN_CODE_JP,
        category="font",
        archive_name="font_mono_source_han_code_jp.zip",
        archive_sha256="64083b35f01d1267f3a92b02bc785bfe0429b06ee7e04b3635556f9ed9e717ac",
        source_rel_path="fonts/mono_source_han_code_jp",
        target_rel_path="fonts/mono_source_han_code_jp",
        files=("LICENSE.txt", "README-JP.md", "README.md", "bold.otf", "regular.otf", "relnotes.txt", "thin.otf"),
    ),
    font_roboto=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO,
        category="font",
        archive_name="font_roboto.zip",
        archive_sha256="180720137126cc545831aec3a68bbca3db1a19839abdfbe53aa2907a35eceece",
        source_rel_path="fonts/roboto",
        target_rel_path="fonts/roboto",
        files=("LICENSE.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_roboto_condensed=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_CONDENSED,
        category="font",
        archive_name="font_roboto_condensed.zip",
        archive_sha256="81aed5304323e483ac9d01347d9eeb88ba453084000719439c1ed9ce9e017f8a",
        source_rel_path="fonts/roboto_condensed",
        target_rel_path="fonts/roboto_condensed",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_roboto_mono=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_MONO,
        category="font",
        archive_name="font_roboto_mono.zip",
        archive_sha256="bfdd43fbee05dd2de7c5670de94d13662c5e23af55355d4025e9c51e7e77173d",
        source_rel_path="fonts/roboto_mono",
        target_rel_path="fonts/roboto_mono",
        files=("LICENSE.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_roboto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_SERIF,
        category="font",
        archive_name="font_roboto_serif.zip",
        archive_sha256="dfa6ba2305d4120d98dfda8a1b45626c96833df7e031ea33d1b1337d3d90b987",
        source_rel_path="fonts/roboto_serif",
        target_rel_path="fonts/roboto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_roboto_slab=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_ROBOTO_SLAB,
        category="font",
        archive_name="font_roboto_slab.zip",
        archive_sha256="a3847c39cb9ee09ecf31942ccdb4913cf25f269cc6a51ce0a1392585e601724a",
        source_rel_path="fonts/roboto_slab",
        target_rel_path="fonts/roboto_slab",
        files=("LICENSE.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_sans_lato=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_LATO,
        category="font",
        archive_name="font_sans_lato.zip",
        archive_sha256="74403a5fed356f5bc63aece602b4b8424ff4ad5016be0c986ddd9f8a948fe1b5",
        source_rel_path="fonts/sans_lato",
        target_rel_path="fonts/sans_lato",
        files=("OFL.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_sans_monstserrat=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_MONSTSERRAT,
        category="font",
        archive_name="font_sans_monstserrat.zip",
        archive_sha256="720dc591e59f8bfb309f6ffb6be8467f6159a54b36e1f7ad1177087cf9cbf79f",
        source_rel_path="fonts/sans_monstserrat",
        target_rel_path="fonts/sans_monstserrat",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_sans_open_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_OPEN_SANS,
        category="font",
        archive_name="font_sans_open_sans.zip",
        archive_sha256="84496a6d45d8d3cbaa6e529c07286c2e268507f661b2f356bf57187d6e779c34",
        source_rel_path="fonts/sans_open_sans",
        target_rel_path="fonts/sans_open_sans",
        files=("OFL.txt", "OpenSans-Bold.ttf", "OpenSans-Light.ttf", "OpenSans-Regular.ttf", "README.txt"),
    ),
    font_sans_oswald=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_OSWALD,
        category="font",
        archive_name="font_sans_oswald.zip",
        archive_sha256="8cb10bce7a8d6e7a85f4dc1a99499e68563b04571edcbf741fb5e6b41a4041f4",
        source_rel_path="fonts/sans_oswald",
        target_rel_path="fonts/sans_oswald",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_sans_poppins=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_POPPINS,
        category="font",
        archive_name="font_sans_poppins.zip",
        archive_sha256="646cedeb1b05e79a4e17214df6d47dc1fdbe20582f0f1f1dcdb0a20982dea6f1",
        source_rel_path="fonts/sans_poppins",
        target_rel_path="fonts/sans_poppins",
        files=("OFL.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_sans_raleways=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SANS_RALEWAYS,
        category="font",
        archive_name="font_sans_raleways.zip",
        archive_sha256="00afb0a377c1bfeb26e00bc35879a8ba3da60554e5e0192b21eacee907a05747",
        source_rel_path="fonts/sans_raleways",
        target_rel_path="fonts/sans_raleways",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_serif_merriweather=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SERIF_MERRIWEATHER,
        category="font",
        archive_name="font_serif_merriweather.zip",
        archive_sha256="de7a01c553ef760325685a36cf7fae41682eb10fa71fa1888eb8782ff2b317e2",
        source_rel_path="fonts/serif_merriweather",
        target_rel_path="fonts/serif_merriweather",
        files=("OFL.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_serif_platypi=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SERIF_PLATYPI,
        category="font",
        archive_name="font_serif_platypi.zip",
        archive_sha256="b810c1e17d78b74713b075216199e13c4ea1d3f68b68502692688d8d2a029fed",
        source_rel_path="fonts/serif_platypi",
        target_rel_path="fonts/serif_platypi",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_serif_playfairdisplay=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_SERIF_PLAYFAIRDISPLAY,
        category="font",
        archive_name="font_serif_playfairdisplay.zip",
        archive_sha256="2fafbaba06f415651e41d75e2c712ae1b42b67a4506c582468c844c82b18e1a1",
        source_rel_path="fonts/serif_playfairdisplay",
        target_rel_path="fonts/serif_playfairdisplay",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf"),
    ),
    font_thai_noto_sans=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_THAI_NOTO_SANS,
        category="font",
        archive_name="font_thai_noto_sans.zip",
        archive_sha256="09ca09667b5afddd8841f3cf248a2020b58ddb72c1b5f54389b2722c9f4db0e7",
        source_rel_path="fonts/thai_noto_sans",
        target_rel_path="fonts/thai_noto_sans",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    font_thai_noto_serif=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.FONT_THAI_NOTO_SERIF,
        category="font",
        archive_name="font_thai_noto_serif.zip",
        archive_sha256="128d066b82395f3ee007421f1d0365a6fe131236150a76a466846f6368bb5260",
        source_rel_path="fonts/thai_noto_serif",
        target_rel_path="fonts/thai_noto_serif",
        files=("OFL.txt", "README.txt", "bold.ttf", "regular.ttf", "thin.ttf"),
    ),
    icon_phosphor=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.ICON_PHOSPHOR,
        category="icon",
        archive_name="icon_phosphor.zip",
        archive_sha256="6f9d7687235decedd0f0bc72ca67d05ca28b9baaf0c520bd9cc2743d2c0b7715",
        source_rel_path="fonticons/phosphor",
        target_rel_path="fonticons/phosphor",
        files=(
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
        ),
    ),
    icon_gcp=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.ICON_GCP,
        category="icon",
        archive_name="icon_gcp.zip",
        archive_sha256="238e87174c03c592ba57a275404a89f224e666623bff2692e7a67ce1bf3ac9a8",
        source_rel_path="icons/gcp",
        target_rel_path="icons/gcp",
        files=(
            "access_context_manager_default.png",
            "administration_default.png",
            "advanced_agent_modeling_default.png",
            "advanced_solutions_lab_default.png",
            "agent_assist_default.png",
            "ai_hub_default.png",
            "ai_hypercomputer_default.png",
            "ai_hypercomputer_modern.png",
            "ai_platform_default.png",
            "ai_platform_unified_default.png",
            "alloydb_default.png",
            "alloydb_modern.png",
            "analytics_hub_default.png",
            "anthos_config_management_default.png",
            "anthos_default.png",
            "anthos_modern.png",
            "anthos_service_mesh_default.png",
            "api_analytics_default.png",
            "api_default.png",
            "api_monetization_default.png",
            "apigee_api_platform_default.png",
            "apigee_default.png",
            "apigee_modern.png",
            "apigee_sense_default.png",
            "app_engine_default.png",
            "artifact_registry_default.png",
            "asset_inventory_default.png",
            "assured_workloads_default.png",
            "automl_default.png",
            "automl_natural_language_default.png",
            "automl_tables_default.png",
            "automl_translation_default.png",
            "automl_video_intelligence_default.png",
            "automl_vision_default.png",
            "bare_metal_solutions_default.png",
            "batch_default.png",
            "beyondcorp_default.png",
            "bigquery_default.png",
            "bigquery_modern.png",
            "bigtable_default.png",
            "billing_default.png",
            "binary_authorization_default.png",
            "catalog_default.png",
            "category_agents_default.png",
            "category_agents_modern.png",
            "category_ai_machine_learning_default.png",
            "category_ai_machine_learning_modern.png",
            "category_business_intelligence_default.png",
            "category_business_intelligence_modern.png",
            "category_collaboration_default.png",
            "category_collaboration_modern.png",
            "category_compute_default.png",
            "category_compute_modern.png",
            "category_containers_default.png",
            "category_containers_modern.png",
            "category_data_analytics_default.png",
            "category_data_analytics_modern.png",
            "category_databases_default.png",
            "category_databases_modern.png",
            "category_developer_tools_default.png",
            "category_developer_tools_modern.png",
            "category_devops_default.png",
            "category_devops_modern.png",
            "category_hybrid_multicloud_default.png",
            "category_hybrid_multicloud_modern.png",
            "category_integration_services_default.png",
            "category_integration_services_modern.png",
            "category_management_tools_default.png",
            "category_management_tools_modern.png",
            "category_maps_geospatial_default.png",
            "category_maps_geospatial_modern.png",
            "category_marketplace_default.png",
            "category_marketplace_modern.png",
            "category_media_services_default.png",
            "category_media_services_modern.png",
            "category_migration_default.png",
            "category_migration_modern.png",
            "category_mixed_reality_default.png",
            "category_mixed_reality_modern.png",
            "category_networking_default.png",
            "category_networking_modern.png",
            "category_observability_default.png",
            "category_observability_modern.png",
            "category_operations_default.png",
            "category_operations_modern.png",
            "category_security_identity_default.png",
            "category_security_identity_modern.png",
            "category_serverless_computing_default.png",
            "category_serverless_computing_modern.png",
            "category_storage_default.png",
            "category_storage_modern.png",
            "category_web3_default.png",
            "category_web3_modern.png",
            "category_web_mobile_default.png",
            "category_web_mobile_modern.png",
            "certificate_authority_service_default.png",
            "certificate_manager_default.png",
            "cloud_api_gateway_default.png",
            "cloud_apis_default.png",
            "cloud_armor_default.png",
            "cloud_asset_inventory_default.png",
            "cloud_audit_logs_default.png",
            "cloud_build_default.png",
            "cloud_cdn_default.png",
            "cloud_code_default.png",
            "cloud_composer_default.png",
            "cloud_data_fusion_default.png",
            "cloud_deploy_default.png",
            "cloud_deployment_manager_default.png",
            "cloud_dns_default.png",
            "cloud_domains_default.png",
            "cloud_ekm_default.png",
            "cloud_endpoints_default.png",
            "cloud_external_ip_addresses_default.png",
            "cloud_firewall_rules_default.png",
            "cloud_for_marketing_default.png",
            "cloud_functions_default.png",
            "cloud_generic_default.png",
            "cloud_gpu_default.png",
            "cloud_healthcare_api_default.png",
            "cloud_healthcare_marketplace_default.png",
            "cloud_hsm_default.png",
            "cloud_ids_default.png",
            "cloud_inference_api_default.png",
            "cloud_interconnect_default.png",
            "cloud_jobs_api_default.png",
            "cloud_load_balancing_default.png",
            "cloud_logging_default.png",
            "cloud_media_edge_default.png",
            "cloud_monitoring_default.png",
            "cloud_nat_default.png",
            "cloud_natural_language_api_default.png",
            "cloud_network_default.png",
            "cloud_ops_default.png",
            "cloud_optimization_ai_default.png",
            "cloud_optimization_ai_fleet_routing_api_default.png",
            "cloud_router_default.png",
            "cloud_routes_default.png",
            "cloud_run_default.png",
            "cloud_run_for_anthos_default.png",
            "cloud_run_modern.png",
            "cloud_scheduler_default.png",
            "cloud_security_scanner_default.png",
            "cloud_shell_default.png",
            "cloud_spanner_default.png",
            "cloud_spanner_modern.png",
            "cloud_sql_default.png",
            "cloud_sql_modern.png",
            "cloud_storage_default.png",
            "cloud_storage_modern.png",
            "cloud_tasks_default.png",
            "cloud_test_lab_default.png",
            "cloud_tpu_default.png",
            "cloud_translation_api_default.png",
            "cloud_vision_api_default.png",
            "cloud_vpn_default.png",
            "compute_engine_default.png",
            "compute_engine_modern.png",
            "configuration_management_default.png",
            "connectivity_test_default.png",
            "connectors_default.png",
            "contact_center_ai_default.png",
            "container_optimized_os_default.png",
            "container_registry_default.png",
            "data_catalog_default.png",
            "data_labeling_default.png",
            "data_layers_default.png",
            "data_loss_prevention_api_default.png",
            "data_qna_default.png",
            "data_studio_default.png",
            "data_transfer_default.png",
            "database_migration_service_default.png",
            "dataflow_default.png",
            "datalab_default.png",
            "dataplex_default.png",
            "datapol_default.png",
            "dataprep_default.png",
            "dataproc_default.png",
            "dataproc_metastore_default.png",
            "datashare_default.png",
            "datastore_default.png",
            "datastream_default.png",
            "debugger_default.png",
            "developer_portal_default.png",
            "dialogflow_cx_default.png",
            "dialogflow_default.png",
            "dialogflow_insights_default.png",
            "distributed_cloud_default.png",
            "distributed_cloud_modern.png",
            "document_ai_default.png",
            "early_access_center_default.png",
            "error_reporting_default.png",
            "eventarc_default.png",
            "filestore_default.png",
            "financial_services_marketplace_default.png",
            "firestore_default.png",
            "fleet_engine_default.png",
            "free_trial_default.png",
            "game_servers_default.png",
            "gce_systems_management_default.png",
            "genomics_default.png",
            "gke_on_prem_default.png",
            "google_cloud_marketplace_default.png",
            "google_kubernetes_engine_default.png",
            "google_kubernetes_engine_modern.png",
            "google_maps_platform_default.png",
            "healthcare_nlp_api_default.png",
            "home_default.png",
            "hyperdisk_default.png",
            "hyperdisk_modern.png",
            "identity_and_access_management_default.png",
            "identity_aware_proxy_default.png",
            "identity_platform_default.png",
            "iot_core_default.png",
            "iot_edge_default.png",
            "key_access_justifications_default.png",
            "key_management_service_default.png",
            "kuberun_default.png",
            "launcher_default.png",
            "local_ssd_default.png",
            "looker_default.png",
            "looker_modern.png",
            "managed_service_for_microsoft_active_directory_default.png",
            "mandiant_default.png",
            "mandiant_modern.png",
            "manifest.json",
            "media_translation_api_default.png",
            "memorystore_default.png",
            "migrate_for_anthos_default.png",
            "migrate_for_compute_engine_default.png",
            "my_cloud_default.png",
            "network_connectivity_center_default.png",
            "network_intelligence_center_default.png",
            "network_security_default.png",
            "network_tiers_default.png",
            "network_topology_default.png",
            "onboarding_default.png",
            "os_configuration_management_default.png",
            "os_inventory_management_default.png",
            "os_patch_management_default.png",
            "partner_interconnect_default.png",
            "partner_portal_default.png",
            "performance_dashboard_default.png",
            "permissions_default.png",
            "persistent_disk_default.png",
            "phishing_protection_default.png",
            "policy_analyzer_default.png",
            "premium_network_tier_default.png",
            "private_connectivity_default.png",
            "private_service_connect_default.png",
            "producer_portal_default.png",
            "profiler_default.png",
            "project_default.png",
            "pubsub_default.png",
            "quantum_engine_default.png",
            "quotas_default.png",
            "real_world_insights_default.png",
            "recommendations_ai_default.png",
            "release_notes_default.png",
            "retail_api_default.png",
            "risk_manager_default.png",
            "runtime_config_default.png",
            "secret_manager_default.png",
            "security_command_center_default.png",
            "security_command_center_modern.png",
            "security_default.png",
            "security_health_advisor_default.png",
            "security_key_enforcement_default.png",
            "security_operations_default.png",
            "security_operations_modern.png",
            "service_discovery_default.png",
            "speech_to_text_default.png",
            "stackdriver_default.png",
            "standard_network_tier_default.png",
            "stream_suite_default.png",
            "support_default.png",
            "tensorflow_enterprise_default.png",
            "text_to_speech_default.png",
            "threat_intelligence_default.png",
            "threat_intelligence_modern.png",
            "tools_for_powershell_default.png",
            "trace_default.png",
            "traffic_director_default.png",
            "transfer_appliance_default.png",
            "transfer_default.png",
            "user_preferences_default.png",
            "vertex_ai_default.png",
            "vertex_ai_modern.png",
            "video_intelligence_api_default.png",
            "virtual_private_cloud_default.png",
            "visual_inspection_default.png",
            "vmware_engine_default.png",
            "web_risk_default.png",
            "web_security_scanner_default.png",
            "workflows_default.png",
            "workload_identity_pool_default.png",
        ),
    ),
    map_cities=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.MAP_CITIES,
        category="map",
        archive_name="map_cities.zip",
        archive_sha256="387fd518706cc1db5040732bd7f0b66d08cdf11c3da297ea4fbc2a1f82c4bafe",
        source_rel_path="maps/cities",
        target_rel_path="maps/cities",
        files=(
            "australia_sydney.geojson",
            "china_hong_kong.geojson",
            "china_shanghai.geojson",
            "france_paris.geojson",
            "germany_berlin.geojson",
            "italy_rome.geojson",
            "japan_kyoto.geojson",
            "japan_osaka.geojson",
            "japan_tokyo.geojson",
            "singapore_singapore.geojson",
            "south_korea_seoul.geojson",
            "taiwan_taipei.geojson",
            "united_kingdom_london.geojson",
            "united_states_los_angeles.geojson",
            "united_states_new_york.geojson",
            "united_states_san_francisco.geojson",
        ),
    ),
    map_countries=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.MAP_COUNTRIES,
        category="map",
        archive_name="map_countries.zip",
        archive_sha256="e8a0a0fd8bbee0ee25b5441042f821044ba81b008257fce620a579387222f1ec",
        source_rel_path="maps/countries",
        target_rel_path="maps/countries",
        files=(
            "afghanistan.geojson",
            "aland.geojson",
            "albania.geojson",
            "algeria.geojson",
            "andorra.geojson",
            "angola.geojson",
            "antigua_and_barbuda.geojson",
            "argentina.geojson",
            "armenia.geojson",
            "aruba.geojson",
            "australia.geojson",
            "austria.geojson",
            "azerbaijan.geojson",
            "bahrain.geojson",
            "bangladesh.geojson",
            "barbados.geojson",
            "belarus.geojson",
            "belgium.geojson",
            "belize.geojson",
            "benin.geojson",
            "bhutan.geojson",
            "bolivia.geojson",
            "bosnia_and_herzegovina.geojson",
            "botswana.geojson",
            "brazil.geojson",
            "brunei.geojson",
            "bulgaria.geojson",
            "burkina_faso.geojson",
            "burundi.geojson",
            "cambodia.geojson",
            "cameroon.geojson",
            "canada.geojson",
            "cape_verde.geojson",
            "central_african_republic.geojson",
            "chad.geojson",
            "chile.geojson",
            "china.geojson",
            "colombia.geojson",
            "comoros.geojson",
            "congo.geojson",
            "costa_rica.geojson",
            "croatia.geojson",
            "cuba.geojson",
            "curacao.geojson",
            "cyprus.geojson",
            "czech_republic.geojson",
            "denmark.geojson",
            "djibouti.geojson",
            "dominica.geojson",
            "dominican_republic.geojson",
            "dr_congo.geojson",
            "east_timor.geojson",
            "ecuador.geojson",
            "egypt.geojson",
            "el_salvador.geojson",
            "equatorial_guinea.geojson",
            "eritrea.geojson",
            "estonia.geojson",
            "eswatini.geojson",
            "ethiopia.geojson",
            "fiji.geojson",
            "finland.geojson",
            "france.geojson",
            "french_polynesia.geojson",
            "gabon.geojson",
            "georgia.geojson",
            "germany.geojson",
            "ghana.geojson",
            "greece.geojson",
            "greenland.geojson",
            "grenada.geojson",
            "guam.geojson",
            "guatemala.geojson",
            "guernsey.geojson",
            "guinea.geojson",
            "guinea_bissau.geojson",
            "guyana.geojson",
            "haiti.geojson",
            "honduras.geojson",
            "hong_kong.geojson",
            "hungary.geojson",
            "iceland.geojson",
            "india.geojson",
            "indonesia.geojson",
            "iran.geojson",
            "iraq.geojson",
            "ireland.geojson",
            "isle_of_man.geojson",
            "israel.geojson",
            "italy.geojson",
            "ivory_coast.geojson",
            "jamaica.geojson",
            "japan.geojson",
            "jersey.geojson",
            "jordan.geojson",
            "kazakhstan.geojson",
            "kenya.geojson",
            "kiribati.geojson",
            "kosovo.geojson",
            "kuwait.geojson",
            "kyrgyzstan.geojson",
            "laos.geojson",
            "latvia.geojson",
            "lebanon.geojson",
            "lesotho.geojson",
            "liberia.geojson",
            "libya.geojson",
            "liechtenstein.geojson",
            "lithuania.geojson",
            "luxembourg.geojson",
            "macau.geojson",
            "madagascar.geojson",
            "malawi.geojson",
            "malaysia.geojson",
            "maldives.geojson",
            "mali.geojson",
            "malta.geojson",
            "marshall_islands.geojson",
            "mauritania.geojson",
            "mauritius.geojson",
            "mexico.geojson",
            "micronesia.geojson",
            "moldova.geojson",
            "monaco.geojson",
            "mongolia.geojson",
            "montenegro.geojson",
            "morocco.geojson",
            "mozambique.geojson",
            "myanmar.geojson",
            "namibia.geojson",
            "nauru.geojson",
            "nepal.geojson",
            "netherlands.geojson",
            "new_caledonia.geojson",
            "new_zealand.geojson",
            "nicaragua.geojson",
            "niger.geojson",
            "nigeria.geojson",
            "north_korea.geojson",
            "north_macedonia.geojson",
            "norway.geojson",
            "oman.geojson",
            "pakistan.geojson",
            "palau.geojson",
            "palestine.geojson",
            "panama.geojson",
            "papua_new_guinea.geojson",
            "paraguay.geojson",
            "peru.geojson",
            "philippines.geojson",
            "poland.geojson",
            "portugal.geojson",
            "puerto_rico.geojson",
            "qatar.geojson",
            "romania.geojson",
            "russia.geojson",
            "rwanda.geojson",
            "saint_kitts_and_nevis.geojson",
            "saint_lucia.geojson",
            "saint_vincent.geojson",
            "samoa.geojson",
            "san_marino.geojson",
            "sao_tome_and_principe.geojson",
            "saudi_arabia.geojson",
            "senegal.geojson",
            "serbia.geojson",
            "seychelles.geojson",
            "sierra_leone.geojson",
            "singapore.geojson",
            "sint_maarten.geojson",
            "slovakia.geojson",
            "slovenia.geojson",
            "solomon_islands.geojson",
            "somalia.geojson",
            "somaliland.geojson",
            "south_africa.geojson",
            "south_korea.geojson",
            "south_sudan.geojson",
            "spain.geojson",
            "sri_lanka.geojson",
            "sudan.geojson",
            "suriname.geojson",
            "sweden.geojson",
            "switzerland.geojson",
            "syria.geojson",
            "taiwan.geojson",
            "tajikistan.geojson",
            "tanzania.geojson",
            "thailand.geojson",
            "the_bahamas.geojson",
            "the_gambia.geojson",
            "togo.geojson",
            "tonga.geojson",
            "trinidad_and_tobago.geojson",
            "tunisia.geojson",
            "turkey.geojson",
            "turkish_republic_of_northern_cyprus.geojson",
            "turkmenistan.geojson",
            "tuvalu.geojson",
            "uganda.geojson",
            "ukraine.geojson",
            "united_arab_emirates.geojson",
            "united_kingdom.geojson",
            "united_states.geojson",
            "united_states_virgin_islands.geojson",
            "uruguay.geojson",
            "uzbekistan.geojson",
            "vanuatu.geojson",
            "vatican_city.geojson",
            "venezuela.geojson",
            "vietnam.geojson",
            "western_sahara.geojson",
            "yemen.geojson",
            "zambia.geojson",
            "zimbabwe.geojson",
        ),
    ),
    map_world=ReleaseAssetPackage(
        name=ReleaseAssetPackageName.MAP_WORLD,
        category="map",
        archive_name="map_world.zip",
        archive_sha256="19a1045e4dc7eda62f8da7595dd8b8d861a9ad217ee3762b1b0919c1babab244",
        source_rel_path="maps/world",
        target_rel_path="maps/world",
        files=("world.geojson",),
    ),
)


def get_all_release_asset_packages() -> list[ReleaseAssetPackage]:
    """Retrieve all defined release asset packages.

    Returns:
        list[ReleaseAssetPackage]: Combined list of font, icon, and map packages.
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


def get_map_asset_packages() -> list[ReleaseAssetPackage]:
    """Retrieve all map asset packages.

    Returns:
        list[ReleaseAssetPackage]: List of map package definitions.
    """
    return [pkg for pkg in RELEASE_ASSET_PACKAGES.values() if pkg.category == "map"]


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


def find_package_for_map_path(map_file_path: str) -> ReleaseAssetPackage | None:
    """Identify which asset package contains a given map resource path.

    Args:
        map_file_path: Relative map path (e.g. 'maps/world/world.geojson', 'countries/japan.geojson').

    Returns:
        ReleaseAssetPackage | None: The containing package if matched, otherwise None.
    """
    normalized = map_file_path.strip("/").removeprefix("maps/")
    family = normalized.split("/")[0] if "/" in normalized else normalized
    target_name = f"map_{family}"
    return RELEASE_ASSET_PACKAGES.get(target_name)


def find_package_for_resource_path(resource_path: str) -> ReleaseAssetPackage | None:
    """Identify which asset package contains a given resource path (font, icon, or map).

    Args:
        resource_path: Relative resource path
            (e.g. 'fonts/roboto/regular.ttf', 'icons/gcp/gce.png', 'maps/countries/japan.geojson').

    Returns:
        ReleaseAssetPackage | None: The containing package if matched, otherwise None.
    """
    norm = resource_path.strip("/")
    if norm.startswith("fonticons/") or norm.startswith("phosphor/"):
        return find_package_for_icon_path(norm)
    if norm.startswith("icons/") or norm.startswith("gcp/"):
        return find_package_for_icon_path(norm)
    if norm.startswith(("maps/", "world/", "countries/", "cities/")):
        return find_package_for_map_path(norm)
    return find_package_for_font_path(norm)


def ensure_asset_available(resource_path: str, tag: str = DEFAULT_RELEASE_TAG) -> None:
    """Ensure that the asset file for a given resource path is downloaded and available.

    Args:
        resource_path: Relative path to font, icon, or map file.
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
    """Download and extract all defined release asset packages (fonts, icons, and maps).

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


__all__ = [
    "DEFAULT_RELEASE_TAG",
    "AssetManifest",
    "AssetManifestItem",
    "BaseReleaseAssetPackages",
    "ReleaseAssetPackage",
    "ReleaseAssetPackageName",
    "ReleaseAssetPackages",
    "RELEASE_ASSET_PACKAGES",
    "create_deterministic_zip_bytes",
    "download_all_release_assets",
    "ensure_asset_available",
    "find_package_for_font_path",
    "find_package_for_icon_path",
    "find_package_for_map_path",
    "find_package_for_resource_path",
    "get_all_release_asset_packages",
    "get_font_asset_packages",
    "get_icon_asset_packages",
    "get_map_asset_packages",
    "get_release_asset_manifest",
]
