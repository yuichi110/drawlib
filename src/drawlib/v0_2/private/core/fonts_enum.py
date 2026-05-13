# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Font enum definitions."""

from drawlib.v0_2.private.types import FontBase


class Font(FontBase):
    """Basic fonts."""

    # sansserif
    SANSSERIF_LIGHT = "Font.SANSSERIF_LIGHT"
    SANSSERIF_REGULAR = "Font.SANSSERIF_REGULAR"
    SANSSERIF_BOLD = "Font.SANSSERIF_BOLD"

    # serif
    SERIF_LIGHT = "Font.SERIF_LIGHT"
    SERIF_REGULAR = "Font.SERIF_REGULAR"
    SERIF_BOLD = "Font.SERIF_BOLD"


class FontSansSerif(FontBase):
    """SansSerif fonts."""

    # lato
    LATO_LIGHT = "FontSansSerif.LATO_LIGHT"
    LATO_REGULAR = "FontSansSerif.LATO_REGULAR"
    LATO_BOLD = "FontSansSerif.LATO_BOLD"

    # montserrat
    MONTSERRAT_LIGHT = "FontSansSerif.MONTSERRAT_LIGHT"
    MONTSERRAT_REGULAR = "FontSansSerif.MONTSERRAT_REGULAR"
    MONTSERRAT_BOLD = "FontSansSerif.MONTSERRAT_BOLD"

    # oswald
    OSWALD_LIGHT = "FontSansSerif.OSWALD_LIGHT"
    OSWALD_REGULAR = "FontSansSerif.OSWALD_REGULAR"
    OSWALD_BOLD = "FontSansSerif.OSWALD_BOLD"

    # poppins
    POPPINS_LIGHT = "FontSansSerif.POPPINS_LIGHT"
    POPPINS_REGULAR = "FontSansSerif.POPPINS_REGULAR"
    POPPINS_BOLD = "FontSansSerif.POPPINS_BOLD"

    # raleways
    RALEWAYS_LIGHT = "FontSansSerif.RALEWAYS_LIGHT"
    RALEWAYS_REGULAR = "FontSansSerif.RALEWAYS_REGULAR"
    RALEWAYS_BOLD = "FontSansSerif.RALEWAYS_BOLD"


class FontSerif(FontBase):
    """Serif fonts."""

    # courier
    COURIER_REGULAR = "FontSerif.COURIER_REGULAR"
    COURIER_BOLD = "FontSerif.COURIER_BOLD"

    # merriweather
    MERRIWEATHER_LIGHT = "FontSerif.MERRIWEATHER_LIGHT"
    MERRIWEATHER_REGULAR = "FontSerif.MERRIWEATHER_REGULAR"
    MERRIWEATHER_BOLD = "FontSerif.MERRIWEATHER_BOLD"

    # platypi
    PLATYPI_LIGHT = "FontSerif.PLATYPI_LIGHT"
    PLATYPI_REGULAR = "FontSerif.PLATYPI_REGULAR"
    PLATYPI_BOLD = "FontSerif.PLATYPI_BOLD"

    # playfairdisplay
    PLAYFAIRDISPLAY_REGULAR = "FontSerif.PLAYFAIRDISPLAY_REGULAR"
    PLAYFAIRDISPLAY_BOLD = "FontSerif.PLAYFAIRDISPLAY_BOLD"


class FontMonoSpace(FontBase):
    """Mono space fonts."""

    # robotomono
    ROBOTO_MONO_LIGHT = "FontMonoSpace.ROBOTO_MONO_LIGHT"
    ROBOTO_MONO_REGULAR = "FontMonoSpace.ROBOTO_MONO_REGULAR"
    ROBOTO_MONO_BOLD = "FontMonoSpace.ROBOTO_MONO_BOLD"

    # courier
    COURIER_REGULAR = "FontMonoSpace.COURIER_REGULAR"
    COURIER_BOLD = "FontMonoSpace.COURIER_BOLD"

    # source code pro
    SOURCECODEPRO_LIGHT = "FontMonoSpace.SOURCECODEPRO_LIGHT"
    SOURCECODEPRO_REGULAR = "FontMonoSpace.SOURCECODEPRO_REGULAR"
    SOURCECODEPRO_BOLD = "FontMonoSpace.SOURCECODEPRO_BOLD"

    # source han code jp
    SOURCEHANCODEJP_LIGHT = "FontMonoSpace.SOURCEHANCODEJP_LIGHT"
    SOURCEHANCODEJP_REGULAR = "FontMonoSpace.SOURCEHANCODEJP_REGULAR"
    SOURCEHANCODEJP_BOLD = "FontMonoSpace.SOURCEHANCODEJP_BOLD"


class FontRoboto(FontBase):
    """Roboto fonts."""

    # roboto
    ROBOTO_LIGHT = "FontRoboto.ROBOTO_LIGHT"
    ROBOTO_REGULAR = "FontRoboto.ROBOTO_REGULAR"
    ROBOTO_BOLD = "FontRoboto.ROBOTO_BOLD"

    # robotoserif
    SERIF_LIGHT = "FontRoboto.SERIF_LIGHT"
    SERIF_REGULAR = "FontRoboto.SERIF_REGULAR"
    SERIF_BOLD = "FontRoboto.SERIF_BOLD"

    # robotomono
    MONO_LIGHT = "FontRoboto.MONO_LIGHT"
    MONO_REGULAR = "FontRoboto.MONO_REGULAR"
    MONO_BOLD = "FontRoboto.MONO_BOLD"

    # condensed
    CONDENSED_LIGHT = "FontRoboto.CONDENSED_LIGHT"
    CONDENSED_REGULAR = "FontRoboto.CONDENSED_REGULAR"
    CONDENSED_BOLD = "FontRoboto.CONDENSED_BOLD"

    # slab
    SLAB_LIGHT = "FontRoboto.SLAB_LIGHT"
    SLAB_REGULAR = "FontRoboto.SLAB_REGULAR"
    SLAB_BOLD = "FontRoboto.SLAB_BOLD"


class FontSourceCode(FontBase):
    """Source code fonts."""

    ROBOTO_MONO = "FontSourceCode.ROBOTO_MONO"
    COURIER = "FontSourceCode.COURIER"
    SOURCECODEPRO = "FontSourceCode.SOURCECODEPRO"
    SOURCEHANCODEJP = "FontSourceCode.SOURCEHANCODEJP"


class FontArabic(FontBase):
    """Arabic fonts."""

    # sans
    SANSSERIF_LIGHT = "FontArabic.SANSSERIF_LIGHT"
    SANSSERIF_REGULAR = "FontArabic.SANSSERIF_REGULAR"
    SANSSERIF_BOLD = "FontArabic.SANSSERIF_BOLD"

    # kufi
    KUFI_LIGHT = "FontArabic.KUFI_LIGHT"
    KUFI_REGULAR = "FontArabic.KUFI_REGULAR"
    KUFI_BOLD = "FontArabic.KUFI_BOLD"

    # naskh
    NASKH_REGULAR = "FontArabic.NASKH_REGULAR"
    NASKH_BOLD = "FontArabic.NASKH_BOLD"


class FontBrahmic(FontBase):
    """Brahmic fonts."""

    # bengali
    BENGALI_SANSSERIF_LIGHT = "FontBrahmic.BENGALI_SANSSERIF_LIGHT"
    BENGALI_SANSSERIF_REGULAR = "FontBrahmic.BENGALI_SANSSERIF_REGULAR"
    BENGALI_SANSSERIF_BOLD = "FontBrahmic.BENGALI_SANSSERIF_BOLD"
    BENGALI_SERIF_LIGHT = "FontBrahmic.BENGALI_SERIF_LIGHT"
    BENGALI_SERIF_REGULAR = "FontBrahmic.BENGALI_SERIF_REGULAR"
    BENGALI_SERIF_BOLD = "FontBrahmic.BENGALI_SERIF_BOLD"

    # devanagari
    DEVANAGARI_SANSSERIF_LIGHT = "FontBrahmic.DEVANAGARI_SANSSERIF_LIGHT"
    DEVANAGARI_SANSSERIF_REGULAR = "FontBrahmic.DEVANAGARI_SANSSERIF_REGULAR"
    DEVANAGARI_SANSSERIF_BOLD = "FontBrahmic.DEVANAGARI_SANSSERIF_BOLD"
    DEVANAGARI_SERIF_LIGHT = "FontBrahmic.DEVANAGARI_SERIF_LIGHT"
    DEVANAGARI_SERIF_REGULAR = "FontBrahmic.DEVANAGARI_SERIF_REGULAR"
    DEVANAGARI_SERIF_BOLD = "FontBrahmic.DEVANAGARI_SERIF_BOLD"

    # tamil
    TAMIL_SANSSERIF_LIGHT = "FontBrahmic.TAMIL_SANSSERIF_LIGHT"
    TAMIL_SANSSERIF_REGULAR = "FontBrahmic.TAMIL_SANSSERIF_REGULAR"
    TAMIL_SANSSERIF_BOLD = "FontBrahmic.TAMIL_SANSSERIF_BOLD"
    TAMIL_SERIF_LIGHT = "FontBrahmic.TAMIL_SERIF_LIGHT"
    TAMIL_SERIF_REGULAR = "FontBrahmic.TAMIL_SERIF_REGULAR"
    TAMIL_SERIF_BOLD = "FontBrahmic.TAMIL_SERIF_BOLD"

    # telugu
    TELUGU_SANSSERIF_LIGHT = "FontBrahmic.TELUGU_SANSSERIF_LIGHT"
    TELUGU_SANSSERIF_REGULAR = "FontBrahmic.TELUGU_SANSSERIF_REGULAR"
    TELUGU_SANSSERIF_BOLD = "FontBrahmic.TELUGU_SANSSERIF_BOLD"
    TELUGU_SERIF_LIGHT = "FontBrahmic.TELUGU_SERIF_LIGHT"
    TELUGU_SERIF_REGULAR = "FontBrahmic.TELUGU_SERIF_REGULAR"
    TELUGU_SERIF_BOLD = "FontBrahmic.TELUGU_SERIF_BOLD"


class FontChinese(FontBase):
    """Chinese fonts."""

    # simplified
    SIMPLIFIED_SANSSERIF_LIGHT = "FontChinese.SIMPLIFIED_SANSSERIF_LIGHT"
    SIMPLIFIED_SANSSERIF_REGULAR = "FontChinese.SIMPLIFIED_SANSSERIF_REGULAR"
    SIMPLIFIED_SANSSERIF_BOLD = "FontChinese.SIMPLIFIED_SANSSERIF_BOLD"
    SIMPLIFIED_SERIF_LIGHT = "FontChinese.SIMPLIFIED_SERIF_LIGHT"
    SIMPLIFIED_SERIF_REGULAR = "FontChinese.SIMPLIFIED_SERIF_REGULAR"
    SIMPLIFIED_SERIF_BOLD = "FontChinese.SIMPLIFIED_SERIF_BOLD"

    # traditional
    TRADITIONAL_SANSSERIF_LIGHT = "FontChinese.TRADITIONAL_SANSSERIF_LIGHT"
    TRADITIONAL_SANSSERIF_REGULAR = "FontChinese.TRADITIONAL_SANSSERIF_REGULAR"
    TRADITIONAL_SANSSERIF_BOLD = "FontChinese.TRADITIONAL_SANSSERIF_BOLD"
    TRADITIONAL_SERIF_LIGHT = "FontChinese.TRADITIONAL_SERIF_LIGHT"
    TRADITIONAL_SERIF_REGULAR = "FontChinese.TRADITIONAL_SERIF_REGULAR"
    TRADITIONAL_SERIF_BOLD = "FontChinese.TRADITIONAL_SERIF_BOLD"

    # hong kong
    HONGKONG_SANSSERIF_LIGHT = "FontChinese.HONGKONG_SANSSERIF_LIGHT"
    HONGKONG_SANSSERIF_REGULAR = "FontChinese.HONGKONG_SANSSERIF_REGULAR"
    HONGKONG_SANSSERIF_BOLD = "FontChinese.HONGKONG_SANSSERIF_BOLD"
    HONGKONG_SERIF_LIGHT = "FontChinese.HONGKONG_SERIF_LIGHT"
    HONGKONG_SERIF_REGULAR = "FontChinese.HONGKONG_SERIF_REGULAR"
    HONGKONG_SERIF_BOLD = "FontChinese.HONGKONG_SERIF_BOLD"


class FontJapanese(FontBase):
    """Japanese fonts."""

    # sansserif
    SANSSERIF_LIGHT = "FontJapanese.SANSSERIF_LIGHT"
    SANSSERIF_REGULAR = "FontJapanese.SANSSERIF_REGULAR"
    SANSSERIF_BOLD = "FontJapanese.SANSSERIF_BOLD"

    # serif
    SERIF_LIGHT = "FontJapanese.SERIF_LIGHT"
    SERIF_REGULAR = "FontJapanese.SERIF_REGULAR"
    SERIF_BOLD = "FontJapanese.SERIF_BOLD"

    # mplus1p
    MPLUS1P_LIGHT = "FontJapanese.MPLUS1P_LIGHT"
    MPLUS1P_REGULAR = "FontJapanese.MPLUS1P_REGULAR"
    MPLUS1P_BOLD = "FontJapanese.MPLUS1P_BOLD"

    # mplus rounded 1c
    MPLUSROUNDED1C_LIGHT = "FontJapanese.MPLUSROUNDED1C_LIGHT"
    MPLUSROUNDED1C_REGULAR = "FontJapanese.MPLUSROUNDED1C_REGULAR"
    MPLUSROUNDED1C_BOLD = "FontJapanese.MPLUSROUNDED1C_BOLD"

    # sawarabi
    SAWARABI_GOTHIC = "FontJapanese.SAWARABI_GOTHIC"
    SAWARABI_MINCHO = "FontJapanese.SAWARABI_MINCHO"


class FontKorean(FontBase):
    """Korean fonts."""

    # sansserif
    SANSSERIF_LIGHT = "FontKorean.SANSSERIF_LIGHT"
    SANSSERIF_REGULAR = "FontKorean.SANSSERIF_REGULAR"
    SANSSERIF_BOLD = "FontKorean.SANSSERIF_BOLD"

    # serif
    SERIF_LIGHT = "FontKorean.SERIF_LIGHT"
    SERIF_REGULAR = "FontKorean.SERIF_REGULAR"
    SERIF_BOLD = "FontKorean.SERIF_BOLD"


class FontThai(FontBase):
    """Thai fonts."""

    # sansserif
    SANSSERIF_LIGHT = "FontThai.SANSSERIF_LIGHT"
    SANSSERIF_REGULAR = "FontThai.SANSSERIF_REGULAR"
    SANSSERIF_BOLD = "FontThai.SANSSERIF_BOLD"

    # serif
    SERIF_LIGHT = "FontThai.SERIF_LIGHT"
    SERIF_REGULAR = "FontThai.SERIF_REGULAR"
    SERIF_BOLD = "FontThai.SERIF_BOLD"
