# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Font definition module."""

import dataclasses
import os
from enum import Enum
from typing import Tuple
from urllib.parse import urljoin

import drawlib.assets.v0_1.fonts
from drawlib.v0_1.private.util import get_script_relative_path


def get_fontfile_tuple(path: str, md5_hash: str) -> Tuple[str, str, str]:
    """Convert provided path to local absolute path and download URL with MD5 info.

    This function takes a relative path to a font file and its MD5 hash, then constructs
    the absolute local path to the font file, the download URL, and returns them along
    with the MD5 hash.

    Args:
        path (str): The relative path to the font file.
        md5_hash (str): The MD5 hash of the font file.

    Returns:
        Tuple[str, str, str]: A tuple containing:
            - font_path (str): The local absolute path to the font file.
            - url (str): The download URL for the font file.
            - md5_hash (str): The MD5 hash of the font file.
    """
    paths = [p for p in path.split("/") if p]

    # Construct the local font path
    dir_path = os.path.dirname(drawlib.assets.v0_1.fonts.__file__)
    font_path = os.path.join(dir_path, *paths)

    # Construct the URL
    url = urljoin(
        "https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/v0_1/fonts/",
        "/".join(paths),
    )

    return (font_path, url, md5_hash)


@dataclasses.dataclass
class FontFile:
    """A class representing a font file"""

    file: str  # type: ignore

    @property
    def file(self) -> str:
        """Get the font file path.

        Returns:
            str: The path to the font file.
        """
        return self._file

    @file.setter
    def file(self, value: str) -> None:
        """Set the font file path.

        Validates that the provided path exists and is a valid file path. If not,
        raises an appropriate exception.

        Args:
            value (str): The path to the font file.

        Raises:
            ValueError: If the provided value is a property.
            FileNotFoundError: If the file does not exist at the specified path.
        """
        if isinstance(value, property):
            raise ValueError("font file not specified at class FontFile.")

        path = get_script_relative_path(value)
        if not os.path.exists(path):
            raise FileNotFoundError(f'font file "{path}" does not exist.')
        self._file = path


# Default
# - Font: English + CJK
#
# Alphabet
# - FontSansSerif
# - FontSans
# - FontMonoSpace
# - FontRoboto
#
# SourceCode
# - FontSourcecode
#
# LocalLanguages
# - FontArabic
# - FontBrahmic
# - FontChinese
# - (not yet) FontCyrillic
# - (not yet) FontGreek
# - FontJapanese
# - FontKorean
# - FontThai


class FontBase(Enum):
    """Base class of all font classes."""


class Font(FontBase):
    """Basic fonts."""

    # sansserif
    SANSSERIF_LIGHT = get_fontfile_tuple(
        "cjk_japanese_noto_sans/light.otf",
        "88ce9ab7e76fed605c822b52605ac2fd",
    )
    SANSSERIF_REGULAR = get_fontfile_tuple(
        "cjk_japanese_noto_sans/regular.otf",
        "6d57a40c6695bd46457315e2a9dc757a",
    )
    SANSSERIF_BOLD = get_fontfile_tuple(
        "cjk_japanese_noto_sans/bold.otf",
        "64d01f4e75814352cc9dea68074f4067",
    )

    # serif
    SERIF_LIGHT = get_fontfile_tuple(
        "cjk_japanese_noto_serif/light.otf",
        "0def63d37c63f0945d1046dae5ab4d83",
    )
    SERIF_REGULAR = get_fontfile_tuple(
        "cjk_japanese_noto_serif/regular.otf",
        "069123ca4dcbdee5cef81ef2f1d2ba8d",
    )
    SERIF_BOLD = get_fontfile_tuple(
        "cjk_japanese_noto_serif/bold.otf",
        "ea7175c0325777d126622340f9c94a66",
    )


class FontSansSerif(FontBase):
    """SansSerif fonts."""

    # lato
    LATO_LIGHT = get_fontfile_tuple(
        "sans_lato/light.ttf",
        "2bcc211c05fc425a57b2767a4cdcf174",
    )
    LATO_REGULAR = get_fontfile_tuple(
        "sans_lato/regular.ttf",
        "122dd68d69fe9587e062d20d9ff5de2a",
    )
    LATO_BOLD = get_fontfile_tuple(
        "sans_lato/bold.ttf",
        "24b516c266d7341c954cb2918f1c8f38",
    )

    # montserrat
    MONTSERRAT_LIGHT = get_fontfile_tuple(
        "sans_monstserrat/light.ttf",
        "94fbe93542f684134cad1d775947ca92",
    )
    MONTSERRAT_REGULAR = get_fontfile_tuple(
        "sans_monstserrat/regular.ttf",
        "5e077c15f6e1d334dd4e9be62b28ac75",
    )
    MONTSERRAT_BOLD = get_fontfile_tuple(
        "sans_monstserrat/bold.ttf",
        "ed86af2ed5bbaf879e9f2ec2e2eac929",
    )

    # oswald
    OSWALD_LIGHT = get_fontfile_tuple(
        "sans_oswald/light.ttf",
        "fb3af9a7ffb259726bb3cb30b74ab7dc",
    )
    OSWALD_REGULAR = get_fontfile_tuple(
        "sans_oswald/regular.ttf",
        "b299a657c45aa257f1458b327f491bfb",
    )
    OSWALD_BOLD = get_fontfile_tuple(
        "sans_oswald/bold.ttf",
        "c95751378db3c5c8bfd993b164e13422",
    )

    # poppins
    POPPINS_LIGHT = get_fontfile_tuple(
        "sans_poppins/light.ttf",
        "fcc40ae9a542d001971e53eaed948410",
    )
    POPPINS_REGULAR = get_fontfile_tuple(
        "sans_poppins/regular.ttf",
        "093ee89be9ede30383f39a899c485a82",
    )
    POPPINS_BOLD = get_fontfile_tuple(
        "sans_poppins/bold.ttf",
        "08c20a487911694291bd8c5de41315ad",
    )

    # raleways
    RALEWAYS_LIGHT = get_fontfile_tuple(
        "sans_raleways/light.ttf",
        "a36750fa9f5530b0c2760267df04ae37",
    )
    RALEWAYS_REGULAR = get_fontfile_tuple(
        "sans_raleways/regular.ttf",
        "d95649da7dfb965a289ac29105ce8771",
    )
    RALEWAYS_BOLD = get_fontfile_tuple(
        "sans_raleways/bold.ttf",
        "21c82294041b1504a5cbe4f566c8acd6",
    )


class FontSerif(FontBase):
    """Serif fonts."""

    # courier
    COURIER_REGULAR = get_fontfile_tuple(
        "mono_courier/regular.ttf",
        "fba4686ed1d1b4ef05ab14db78805dbe",
    )
    COURIER_BOLD = get_fontfile_tuple(
        "mono_courier/bold.ttf",
        "4acfa45d29d240044e0075a8e58f0862",
    )

    # merriweather
    MERRIWEATHER_LIGHT = get_fontfile_tuple(
        "serif_merriweather/light.ttf",
        "eccb6c6a243a3d44219648b6cdbc58ce",
    )
    MERRIWEATHER_REGULAR = get_fontfile_tuple(
        "serif_merriweather/regular.ttf",
        "e2f219e63a575a41e10f991e9c95819a",
    )
    MERRIWEATHER_BOLD = get_fontfile_tuple(
        "serif_merriweather/bold.ttf",
        "79ea53fed59f391498dfc6f2fbea97c2",
    )

    # platypi
    PLATYPI_LIGHT = get_fontfile_tuple(
        "serif_platypi/light.ttf",
        "113ff25ffa6c98594583200398ab5c71",
    )
    PLATYPI_REGULAR = get_fontfile_tuple(
        "serif_platypi/regular.ttf",
        "a7f199dd97ff6567df8978b579213e3d",
    )
    PLATYPI_BOLD = get_fontfile_tuple(
        "serif_platypi/bold.ttf",
        "344e0525c3f473c8959c66e1df44e2e1",
    )

    # playfairdisplay
    PLAYFAIRDISPLAY_REGULAR = get_fontfile_tuple(
        "serif_playfairdisplay/regular.ttf",
        "1a28efdbd2876d90e554a67faabad24b",
    )
    PLAYFAIRDISPLAY_BOLD = get_fontfile_tuple(
        "serif_playfairdisplay/bold.ttf",
        "9b38798112efb7cf6eca1de031cec4ca",
    )


class FontMonoSpace(FontBase):
    """Mono space fonts."""

    # robotomono
    ROBOTO_MONO_LIGHT = get_fontfile_tuple(
        "roboto_mono/light.ttf",
        "c9166464b1db95fc3cdf9b50fc7f98e2",
    )
    ROBOTO_MONO_REGULAR = get_fontfile_tuple(
        "roboto_mono/regular.ttf",
        "5b04fdfec4c8c36e8ca574e40b7148bb",
    )
    ROBOTO_MONO_BOLD = get_fontfile_tuple(
        "roboto_mono/bold.ttf",
        "90190d91283189e340b2a44fe560f2cd",
    )

    # courier
    COURIER_REGULAR = get_fontfile_tuple(
        "mono_courier/regular.ttf",
        "fba4686ed1d1b4ef05ab14db78805dbe",
    )
    COURIER_BOLD = get_fontfile_tuple(
        "mono_courier/bold.ttf",
        "4acfa45d29d240044e0075a8e58f0862",
    )

    # source code pro
    SOURCECODEPRO_LIGHT = get_fontfile_tuple(
        "mono_source_code_pro/light.otf",
        "93d429d024b482990231386a4eb49dd7",
    )
    SOURCECODEPRO_REGULAR = get_fontfile_tuple(
        "mono_source_code_pro/regular.otf",
        "f471e697282189889a1514d0ebcf5491",
    )
    SOURCECODEPRO_BOLD = get_fontfile_tuple(
        "mono_source_code_pro/bold.otf",
        "ec83816e7ec8fa6d3c3a60bdb8cf89de",
    )

    # source han code jp
    SOURCEHANCODEJP_LIGHT = get_fontfile_tuple(
        "mono_source_han_code_jp/light.otf",
        "ef1eb2fa9ff7c02e8a3336a70826ad47",
    )
    SOURCEHANCODEJP_REGULAR = get_fontfile_tuple(
        "mono_source_han_code_jp/regular.otf",
        "abcdbd5449ad6a30d540221a12f4a0b5",
    )
    SOURCEHANCODEJP_BOLD = get_fontfile_tuple(
        "mono_source_han_code_jp/bold.otf",
        "dff5826247909bb8e04b8bf3be893386",
    )


class FontRoboto(FontBase):
    """Roboto fonts."""

    # roboto
    ROBOTO_LIGHT = get_fontfile_tuple(
        "roboto/light.ttf",
        "881e150ab929e26d1f812c4342c15a7c",
    )
    ROBOTO_REGULAR = get_fontfile_tuple(
        "roboto/regular.ttf",
        "8a36205bd9b83e03af0591a004bc97f4",
    )
    ROBOTO_BOLD = get_fontfile_tuple(
        "roboto/bold.ttf",
        "b8e42971dec8d49207a8c8e2b919a6ac",
    )

    # robotoserif
    SERIF_LIGHT = get_fontfile_tuple(
        "roboto_serif/light.ttf",
        "4781a153250a8caf652b4f5b129c30ed",
    )
    SERIF_REGULAR = get_fontfile_tuple(
        "roboto_serif/regular.ttf",
        "2fde5a4a0cef2c19b4b6a30763322847",
    )
    SERIF_BOLD = get_fontfile_tuple(
        "roboto_serif/bold.ttf",
        "8ec6ab43edac2144cfd2494d522de733",
    )

    # robotomono
    MONO_LIGHT = get_fontfile_tuple(
        "roboto_mono/light.ttf",
        "c9166464b1db95fc3cdf9b50fc7f98e2",
    )
    MONO_REGULAR = get_fontfile_tuple(
        "roboto_mono/regular.ttf",
        "5b04fdfec4c8c36e8ca574e40b7148bb",
    )
    MONO_BOLD = get_fontfile_tuple(
        "roboto_mono/bold.ttf",
        "90190d91283189e340b2a44fe560f2cd",
    )

    # condensed
    CONDENSED_LIGHT = get_fontfile_tuple(
        "roboto_condensed/light.ttf",
        "68680c984f72eef7b2e2cf269382f2a6",
    )
    CONDENSED_REGULAR = get_fontfile_tuple(
        "roboto_condensed/regular.ttf",
        "f1123f4b3d926ac4f72cc8091a4b5d19",
    )
    CONDENSED_BOLD = get_fontfile_tuple(
        "roboto_condensed/bold.ttf",
        "0233b881b26ce6cc3884c6944940d11b",
    )

    # slab
    SLAB_LIGHT = get_fontfile_tuple(
        "roboto_slab/light.ttf",
        "4c63608980b784c679bbadeb18d9acf4",
    )
    SLAB_REGULAR = get_fontfile_tuple(
        "roboto_slab/regular.ttf",
        "2100b4a02ebb94c0aa18cabd642ee507",
    )
    SLAB_BOLD = get_fontfile_tuple(
        "roboto_slab/bold.ttf",
        "2c44adc1ebd36820fd75012412e6f550",
    )


###################
# Source Code ###
###################


class FontSourceCode(FontBase):
    """Source code fonts."""

    ROBOTO_MONO = get_fontfile_tuple(
        "roboto_mono/regular.ttf",
        "5b04fdfec4c8c36e8ca574e40b7148bb",
    )
    COURIER = get_fontfile_tuple(
        "mono_courier/regular.ttf",
        "fba4686ed1d1b4ef05ab14db78805dbe",
    )
    SOURCECODEPRO = get_fontfile_tuple(
        "mono_source_code_pro/regular.otf",
        "f471e697282189889a1514d0ebcf5491",
    )
    SOURCEHANCODEJP = get_fontfile_tuple(
        "mono_source_han_code_jp/regular.otf",
        "abcdbd5449ad6a30d540221a12f4a0b5",
    )


#######################
# Local Languages ###
#######################


class FontArabic(FontBase):
    """Arabic fonts."""

    # sans
    SANSSERIF_LIGHT = get_fontfile_tuple(
        "arabic_noto_sans/light.ttf",
        "ffcfcc231a05032bca6e0819aa60eacb",
    )
    SANSSERIF_REGULAR = get_fontfile_tuple(
        "arabic_noto_sans/regular.ttf",
        "75527903c6a793772b02807c5343f4c8",
    )
    SANSSERIF_BOLD = get_fontfile_tuple(
        "arabic_noto_sans/bold.ttf",
        "cda675687ed1576b7bda072838c0ed5f",
    )

    # kufi
    KUFI_LIGHT = get_fontfile_tuple(
        "arabic_noto_kufi/light.ttf",
        "23517c64b528b3c744bfb3be94e58836",
    )
    KUFI_REGULAR = get_fontfile_tuple(
        "arabic_noto_kufi/regular.ttf",
        "600b529eb4849a54dde020e3ea389de2",
    )
    KUFI_BOLD = get_fontfile_tuple(
        "arabic_noto_kufi/bold.ttf",
        "34886bd59d48cf9113e1e9386bee615e",
    )

    # naskh
    NASKH_REGULAR = get_fontfile_tuple(
        "arabic_noto_naskh/regular.ttf",
        "08f2d6bfe92d3e78721a0e1746397344",
    )
    NASKH_BOLD = get_fontfile_tuple(
        "arabic_noto_naskh/bold.ttf",
        "3e8ac1d70691caf5ddfd36fee8acce3d",
    )


class FontBrahmic(FontBase):
    """Brahmic fonts."""

    # bengali
    BENGALI_SANSSERIF_LIGHT = get_fontfile_tuple(
        "brahmic_bengali_noto_sans/light.ttf",
        "7e54641bfed39afb0b9b957168eb7869",
    )
    BENGALI_SANSSERIF_REGULAR = get_fontfile_tuple(
        "brahmic_bengali_noto_sans/regular.ttf",
        "997ec45c6f75da576966ce470cebdd8f",
    )
    BENGALI_SANSSERIF_BOLD = get_fontfile_tuple(
        "brahmic_bengali_noto_sans/bold.ttf",
        "b4463ed2663bd59adff9ef090dabaa14",
    )
    BENGALI_SERIF_LIGHT = get_fontfile_tuple(
        "brahmic_bengali_noto_serif/light.ttf",
        "1890d63acffba90859e2bfb2bea18035",
    )
    BENGALI_SERIF_REGULAR = get_fontfile_tuple(
        "brahmic_bengali_noto_serif/regular.ttf",
        "7de2929b2584456afd8251c356de1285",
    )
    BENGALI_SERIF_BOLD = get_fontfile_tuple(
        "brahmic_bengali_noto_serif/bold.ttf",
        "eccf90709f61853a4aa1d184f8e54216",
    )

    # devanagari
    DEVANAGARI_SANSSERIF_LIGHT = get_fontfile_tuple(
        "brahmic_devanagari_noto_sans/light.ttf",
        "be21506bd5d277aa33b7d6d2563477af",
    )
    DEVANAGARI_SANSSERIF_REGULAR = get_fontfile_tuple(
        "brahmic_devanagari_noto_sans/regular.ttf",
        "46dbe14f577b56ade221acf89631fd7b",
    )
    DEVANAGARI_SANSSERIF_BOLD = get_fontfile_tuple(
        "brahmic_devanagari_noto_sans/bold.ttf",
        "bb252b622a58dc3bf433dbf5754e6f7e",
    )
    DEVANAGARI_SERIF_LIGHT = get_fontfile_tuple(
        "brahmic_devanagari_noto_serif/light.ttf",
        "bae0ad5209cfee6a43bbd3163b98056c",
    )
    DEVANAGARI_SERIF_REGULAR = get_fontfile_tuple(
        "brahmic_devanagari_noto_serif/regular.ttf",
        "6c24c42e9eafb1cdda367671361f52a2",
    )
    DEVANAGARI_SERIF_BOLD = get_fontfile_tuple(
        "brahmic_devanagari_noto_serif/bold.ttf",
        "bedfefb38fe53bc1fa18c5a651c1d7b3",
    )

    # tamil
    TAMIL_SANSSERIF_LIGHT = get_fontfile_tuple(
        "brahmic_tamil_noto_sans/light.ttf",
        "b6ced5e5b7a0d6f2e763db77705cb7cc",
    )
    TAMIL_SANSSERIF_REGULAR = get_fontfile_tuple(
        "brahmic_tamil_noto_sans/regular.ttf",
        "cfd0079baedcd7cd5d2ad98c1489d023",
    )
    TAMIL_SANSSERIF_BOLD = get_fontfile_tuple(
        "brahmic_tamil_noto_sans/bold.ttf",
        "df89701fdee0d1de9f7f6c7fbbae8874",
    )
    TAMIL_SERIF_LIGHT = get_fontfile_tuple(
        "brahmic_tamil_noto_serif/light.ttf",
        "0e5ddcae43424e9a547917ec1e997695",
    )
    TAMIL_SERIF_REGULAR = get_fontfile_tuple(
        "brahmic_tamil_noto_serif/regular.ttf",
        "0916bea8b08896c86b50c6766f506416",
    )
    TAMIL_SERIF_BOLD = get_fontfile_tuple(
        "brahmic_tamil_noto_serif/bold.ttf",
        "32be9efedcdf21ad3cbb960b43f8e575",
    )

    # telugu
    TELUGU_SANSSERIF_LIGHT = get_fontfile_tuple(
        "brahmic_telugu_noto_sans/light.ttf",
        "644489807d1b7ff280724920e6d46208",
    )
    TELUGU_SANSSERIF_REGULAR = get_fontfile_tuple(
        "brahmic_telugu_noto_sans/regular.ttf",
        "79fd1e624e819497bc22b35830906ecb",
    )
    TELUGU_SANSSERIF_BOLD = get_fontfile_tuple(
        "brahmic_telugu_noto_sans/bold.ttf",
        "48dd5f30af67f36e23c885e341094d83",
    )
    TELUGU_SERIF_LIGHT = get_fontfile_tuple(
        "brahmic_telugu_noto_serif/light.ttf",
        "9e72f2730d10bd62e437360f30dc3e63",
    )
    TELUGU_SERIF_REGULAR = get_fontfile_tuple(
        "brahmic_telugu_noto_serif/regular.ttf",
        "0d5da9d39e03e0dbdfb91002710f4be0",
    )
    TELUGU_SERIF_BOLD = get_fontfile_tuple(
        "brahmic_telugu_noto_serif/bold.ttf",
        "b12935df488a2a17167e180ea3569360",
    )


class FontChinese(FontBase):
    """Chinese fonts."""

    # simplified
    SIMPLIFIED_SANSSERIF_LIGHT = get_fontfile_tuple(
        "chinese_simplified_noto_sans/light.ttf",
        "d52d4d74290978e137446b7b62b1c5d2",
    )
    SIMPLIFIED_SANSSERIF_REGULAR = get_fontfile_tuple(
        "chinese_simplified_noto_sans/regular.ttf",
        "19498325f22381f551df06ce1b4cad4f",
    )
    SIMPLIFIED_SANSSERIF_BOLD = get_fontfile_tuple(
        "chinese_simplified_noto_sans/bold.ttf",
        "f8f91dd976cfe63e46490e63345e8c2e",
    )
    SIMPLIFIED_SERIF_LIGHT = get_fontfile_tuple(
        "chinese_simplified_noto_serif/light.ttf",
        "33c62feebda55f521b6210671c9f3df8",
    )
    SIMPLIFIED_SERIF_REGULAR = get_fontfile_tuple(
        "chinese_simplified_noto_serif/regular.ttf",
        "3d973955a90c1a69029f56fd52b7c7a2",
    )
    SIMPLIFIED_SERIF_BOLD = get_fontfile_tuple(
        "chinese_simplified_noto_serif/bold.ttf",
        "848c527475e6444da5bc77f540f3d701",
    )

    # traditional
    TRADITIONAL_SANSSERIF_LIGHT = get_fontfile_tuple(
        "chinese_traditional_noto_sans/light.ttf",
        "b00ec05f9416dcf69687be79e2c645d7",
    )
    TRADITIONAL_SANSSERIF_REGULAR = get_fontfile_tuple(
        "chinese_traditional_noto_sans/regular.ttf",
        "ad18e8fc265252917dd3698e268977d7",
    )
    TRADITIONAL_SANSSERIF_BOLD = get_fontfile_tuple(
        "chinese_traditional_noto_sans/bold.ttf",
        "a4ee55b412c13458ec428c1f6821e283",
    )
    TRADITIONAL_SERIF_LIGHT = get_fontfile_tuple(
        "chinese_traditional_noto_serif/light.ttf",
        "d1b13a4bdcde44b480cee69815a375cd",
    )
    TRADITIONAL_SERIF_REGULAR = get_fontfile_tuple(
        "chinese_traditional_noto_serif/regular.ttf",
        "4fbc0356bda7984a81788c9614d27867",
    )
    TRADITIONAL_SERIF_BOLD = get_fontfile_tuple(
        "chinese_traditional_noto_serif/bold.ttf",
        "5144d59a55c50e9f23aea89041af0d23",
    )

    # hong kong
    HONGKONG_SANSSERIF_LIGHT = get_fontfile_tuple(
        "chinese_hongkong_noto_sans/light.ttf",
        "c014c66923388c93ec4b0158687f1604",
    )
    HONGKONG_SANSSERIF_REGULAR = get_fontfile_tuple(
        "chinese_hongkong_noto_sans/regular.ttf",
        "7882ea6ae9cc19826e98cc46769f15fe",
    )
    HONGKONG_SANSSERIF_BOLD = get_fontfile_tuple(
        "chinese_hongkong_noto_sans/bold.ttf",
        "f5fbe3e2e9478bfc00e255934fc1a842",
    )
    HONGKONG_SERIF_LIGHT = get_fontfile_tuple(
        "chinese_hongkong_noto_serif/light.ttf",
        "c61d4737ea4a774853955b86b38fc871",
    )
    HONGKONG_SERIF_REGULAR = get_fontfile_tuple(
        "chinese_hongkong_noto_serif/regular.ttf",
        "d8e6524288c8c19327d3562ca431b471",
    )
    HONGKONG_SERIF_BOLD = get_fontfile_tuple(
        "chinese_hongkong_noto_serif/bold.ttf",
        "08302783208cf67b70d2b53bbc3150b8",
    )


class FontJapanese(FontBase):
    """Japanese fonts."""

    # sansserif
    SANSSERIF_LIGHT = get_fontfile_tuple(
        "japanese_noto_sans/light.ttf",
        "7d1e0e68062ba3ae1cc12009620f645d",
    )
    SANSSERIF_REGULAR = get_fontfile_tuple(
        "japanese_noto_sans/regular.ttf",
        "022f32abf24d5534496095e04aa739b3",
    )
    SANSSERIF_BOLD = get_fontfile_tuple(
        "japanese_noto_sans/bold.ttf",
        "4aec04fd98881db5fbc79075428727ef",
    )

    # serif
    SERIF_LIGHT = get_fontfile_tuple(
        "japanese_noto_serif/light.ttf",
        "0f3e1a61caa6528059bf62dae1902235",
    )
    SERIF_REGULAR = get_fontfile_tuple(
        "japanese_noto_serif/regular.ttf",
        "a0cc86e68bdf1711e30bffb6d0bb0b49",
    )
    SERIF_BOLD = get_fontfile_tuple(
        "japanese_noto_serif/bold.ttf",
        "9ec5752a714a1f0871b4ad04f0d6f283",
    )

    # mplus1p
    MPLUS1P_LIGHT = get_fontfile_tuple(
        "japanese_mplus_1p/light.ttf",
        "01fea1cae2979588652514d83e9c0423",
    )
    MPLUS1P_REGULAR = get_fontfile_tuple(
        "japanese_mplus_1p/regular.ttf",
        "bfab3ff358a7fa14c5703ad49063cb16",
    )
    MPLUS1P_BOLD = get_fontfile_tuple(
        "japanese_mplus_1p/bold.ttf",
        "aa140061f44d0dda19ab2573a0ad93d3",
    )

    # mplus rounded 1c
    MPLUSROUNDED1C_LIGHT = get_fontfile_tuple(
        "japanese_mplus_rounded1c/light.ttf",
        "9c62a03e973fc7c73bfb935296a2b693",
    )
    MPLUSROUNDED1C_REGULAR = get_fontfile_tuple(
        "japanese_mplus_rounded1c/regular.ttf",
        "686088cf66e883b2d4c2e8c9cde6d32f",
    )
    MPLUSROUNDED1C_BOLD = get_fontfile_tuple(
        "japanese_mplus_rounded1c/bold.ttf",
        "d4599c8dc8ba3353fd83af468838f1f8",
    )

    # sawarabi
    SAWARABI_GOTHIC = get_fontfile_tuple(
        "japanese_sawarabi_gothic/regular.ttf",
        "28d35b15cdc5fc9937335bfed22e1838",
    )
    SAWARABI_MINCHO = get_fontfile_tuple(
        "japanese_sawarabi_mincho/regular.ttf",
        "568e086e3451178636c5f10761df2c45",
    )


class FontKorean(FontBase):
    """Korean fonts."""

    # sansserif
    SANSSERIF_LIGHT = get_fontfile_tuple(
        "korean_noto_sans/light.ttf",
        "e61301e66b058697c6031c39edb7c0d2",
    )
    SANSSERIF_REGULAR = get_fontfile_tuple(
        "korean_noto_sans/regular.ttf",
        "e910afbd441c5247227fb4a731d65799",
    )
    SANSSERIF_BOLD = get_fontfile_tuple(
        "korean_noto_sans/bold.ttf",
        "671db5f821991c90d7f8499bcf9fed7e",
    )

    # serif
    SERIF_LIGHT = get_fontfile_tuple(
        "korean_noto_serif/light.ttf",
        "9922efae87ff1960a63efdc3466edd90",
    )
    SERIF_REGULAR = get_fontfile_tuple(
        "korean_noto_serif/regular.ttf",
        "80c68ab78fd0e67500929a9cdc53da0c",
    )
    SERIF_BOLD = get_fontfile_tuple(
        "korean_noto_serif/bold.ttf",
        "8c4085a8e0d34353e2f0d9285abef61e",
    )


class FontThai(FontBase):
    """Thai fonts."""

    # sansserif
    SANSSERIF_LIGHT = get_fontfile_tuple(
        "thai_noto_sans/light.ttf",
        "fa192df61c8ef9a6a204c6323fdae9dc",
    )
    SANSSERIF_REGULAR = get_fontfile_tuple(
        "thai_noto_sans/regular.ttf",
        "a84996ee5e940db8c7c2e1375728ca68",
    )
    SANSSERIF_BOLD = get_fontfile_tuple(
        "thai_noto_sans/bold.ttf",
        "1296256d14a6c704f87967dc06583a64",
    )

    # serif
    SERIF_LIGHT = get_fontfile_tuple(
        "thai_noto_serif/light.ttf",
        "70c158b4144d83cba0f7266952ddad2f",
    )
    SERIF_REGULAR = get_fontfile_tuple(
        "thai_noto_serif/regular.ttf",
        "fe28175fbf4e79f1562d30f60933cab7",
    )
    SERIF_BOLD = get_fontfile_tuple(
        "thai_noto_serif/bold.ttf",
        "dc10158f174b8141c810880b98ba5a5a",
    )
