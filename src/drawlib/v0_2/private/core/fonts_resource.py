# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Font resource definitions."""

from pydantic import BaseModel

from drawlib.v0_2.private.core.fonts_enum import (
    Font,
    FontArabic,
    FontBrahmic,
    FontChinese,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
    FontThai,
)
from drawlib.v0_2.private.types import FontBase


class FontResource(BaseModel):
    """Static font resource definition."""

    path: str
    md5: str


FONT_RESOURCES: dict[FontBase, FontResource] = {
    Font.SANSSERIF_LIGHT: FontResource(
        path="cjk_japanese_noto_sans/light.otf",
        md5="88ce9ab7e76fed605c822b52605ac2fd",
    ),
    Font.SANSSERIF_REGULAR: FontResource(
        path="cjk_japanese_noto_sans/regular.otf",
        md5="6d57a40c6695bd46457315e2a9dc757a",
    ),
    Font.SANSSERIF_BOLD: FontResource(
        path="cjk_japanese_noto_sans/bold.otf",
        md5="64d01f4e75814352cc9dea68074f4067",
    ),
    Font.SERIF_LIGHT: FontResource(
        path="cjk_japanese_noto_serif/light.otf",
        md5="0def63d37c63f0945d1046dae5ab4d83",
    ),
    Font.SERIF_REGULAR: FontResource(
        path="cjk_japanese_noto_serif/regular.otf",
        md5="069123ca4dcbdee5cef81ef2f1d2ba8d",
    ),
    Font.SERIF_BOLD: FontResource(
        path="cjk_japanese_noto_serif/bold.otf",
        md5="ea7175c0325777d126622340f9c94a66",
    ),
    FontSansSerif.LATO_LIGHT: FontResource(
        path="sans_lato/light.ttf",
        md5="2bcc211c05fc425a57b2767a4cdcf174",
    ),
    FontSansSerif.LATO_REGULAR: FontResource(
        path="sans_lato/regular.ttf",
        md5="122dd68d69fe9587e062d20d9ff5de2a",
    ),
    FontSansSerif.LATO_BOLD: FontResource(
        path="sans_lato/bold.ttf",
        md5="24b516c266d7341c954cb2918f1c8f38",
    ),
    FontSansSerif.MONTSERRAT_LIGHT: FontResource(
        path="sans_monstserrat/light.ttf",
        md5="94fbe93542f684134cad1d775947ca92",
    ),
    FontSansSerif.MONTSERRAT_REGULAR: FontResource(
        path="sans_monstserrat/regular.ttf",
        md5="5e077c15f6e1d334dd4e9be62b28ac75",
    ),
    FontSansSerif.MONTSERRAT_BOLD: FontResource(
        path="sans_monstserrat/bold.ttf",
        md5="ed86af2ed5bbaf879e9f2ec2e2eac929",
    ),
    FontSansSerif.OSWALD_LIGHT: FontResource(
        path="sans_oswald/light.ttf",
        md5="fb3af9a7ffb259726bb3cb30b74ab7dc",
    ),
    FontSansSerif.OSWALD_REGULAR: FontResource(
        path="sans_oswald/regular.ttf",
        md5="b299a657c45aa257f1458b327f491bfb",
    ),
    FontSansSerif.OSWALD_BOLD: FontResource(
        path="sans_oswald/bold.ttf",
        md5="c95751378db3c5c8bfd993b164e13422",
    ),
    FontSansSerif.POPPINS_LIGHT: FontResource(
        path="sans_poppins/light.ttf",
        md5="fcc40ae9a542d001971e53eaed948410",
    ),
    FontSansSerif.POPPINS_REGULAR: FontResource(
        path="sans_poppins/regular.ttf",
        md5="093ee89be9ede30383f39a899c485a82",
    ),
    FontSansSerif.POPPINS_BOLD: FontResource(
        path="sans_poppins/bold.ttf",
        md5="08c20a487911694291bd8c5de41315ad",
    ),
    FontSansSerif.RALEWAYS_LIGHT: FontResource(
        path="sans_raleways/light.ttf",
        md5="a36750fa9f5530b0c2760267df04ae37",
    ),
    FontSansSerif.RALEWAYS_REGULAR: FontResource(
        path="sans_raleways/regular.ttf",
        md5="d95649da7dfb965a289ac29105ce8771",
    ),
    FontSansSerif.RALEWAYS_BOLD: FontResource(
        path="sans_raleways/bold.ttf",
        md5="21c82294041b1504a5cbe4f566c8acd6",
    ),
    FontSerif.COURIER_REGULAR: FontResource(
        path="mono_courier/regular.ttf",
        md5="fba4686ed1d1b4ef05ab14db78805dbe",
    ),
    FontSerif.COURIER_BOLD: FontResource(
        path="mono_courier/bold.ttf",
        md5="4acfa45d29d240044e0075a8e58f0862",
    ),
    FontSerif.MERRIWEATHER_LIGHT: FontResource(
        path="serif_merriweather/light.ttf",
        md5="eccb6c6a243a3d44219648b6cdbc58ce",
    ),
    FontSerif.MERRIWEATHER_REGULAR: FontResource(
        path="serif_merriweather/regular.ttf",
        md5="e2f219e63a575a41e10f991e9c95819a",
    ),
    FontSerif.MERRIWEATHER_BOLD: FontResource(
        path="serif_merriweather/bold.ttf",
        md5="79ea53fed59f391498dfc6f2fbea97c2",
    ),
    FontSerif.PLATYPI_LIGHT: FontResource(
        path="serif_platypi/light.ttf",
        md5="113ff25ffa6c98594583200398ab5c71",
    ),
    FontSerif.PLATYPI_REGULAR: FontResource(
        path="serif_platypi/regular.ttf",
        md5="a7f199dd97ff6567df8978b579213e3d",
    ),
    FontSerif.PLATYPI_BOLD: FontResource(
        path="serif_platypi/bold.ttf",
        md5="344e0525c3f473c8959c66e1df44e2e1",
    ),
    FontSerif.PLAYFAIRDISPLAY_REGULAR: FontResource(
        path="serif_playfairdisplay/regular.ttf",
        md5="1a28efdbd2876d90e554a67faabad24b",
    ),
    FontSerif.PLAYFAIRDISPLAY_BOLD: FontResource(
        path="serif_playfairdisplay/bold.ttf",
        md5="9b38798112efb7cf6eca1de031cec4ca",
    ),
    FontMonoSpace.ROBOTO_MONO_LIGHT: FontResource(
        path="roboto_mono/light.ttf",
        md5="c9166464b1db95fc3cdf9b50fc7f98e2",
    ),
    FontMonoSpace.ROBOTO_MONO_REGULAR: FontResource(
        path="roboto_mono/regular.ttf",
        md5="5b04fdfec4c8c36e8ca574e40b7148bb",
    ),
    FontMonoSpace.ROBOTO_MONO_BOLD: FontResource(
        path="roboto_mono/bold.ttf",
        md5="90190d91283189e340b2a44fe560f2cd",
    ),
    FontMonoSpace.COURIER_REGULAR: FontResource(
        path="mono_courier/regular.ttf",
        md5="fba4686ed1d1b4ef05ab14db78805dbe",
    ),
    FontMonoSpace.COURIER_BOLD: FontResource(
        path="mono_courier/bold.ttf",
        md5="4acfa45d29d240044e0075a8e58f0862",
    ),
    FontMonoSpace.SOURCECODEPRO_LIGHT: FontResource(
        path="mono_source_code_pro/light.otf",
        md5="93d429d024b482990231386a4eb49dd7",
    ),
    FontMonoSpace.SOURCECODEPRO_REGULAR: FontResource(
        path="mono_source_code_pro/regular.otf",
        md5="f471e697282189889a1514d0ebcf5491",
    ),
    FontMonoSpace.SOURCECODEPRO_BOLD: FontResource(
        path="mono_source_code_pro/bold.otf",
        md5="ec83816e7ec8fa6d3c3a60bdb8cf89de",
    ),
    FontMonoSpace.SOURCEHANCODEJP_LIGHT: FontResource(
        path="mono_source_han_code_jp/light.otf",
        md5="ef1eb2fa9ff7c02e8a3336a70826ad47",
    ),
    FontMonoSpace.SOURCEHANCODEJP_REGULAR: FontResource(
        path="mono_source_han_code_jp/regular.otf",
        md5="abcdbd5449ad6a30d540221a12f4a0b5",
    ),
    FontMonoSpace.SOURCEHANCODEJP_BOLD: FontResource(
        path="mono_source_han_code_jp/bold.otf",
        md5="dff5826247909bb8e04b8bf3be893386",
    ),
    FontRoboto.ROBOTO_LIGHT: FontResource(
        path="roboto/light.ttf",
        md5="881e150ab929e26d1f812c4342c15a7c",
    ),
    FontRoboto.ROBOTO_REGULAR: FontResource(
        path="roboto/regular.ttf",
        md5="8a36205bd9b83e03af0591a004bc97f4",
    ),
    FontRoboto.ROBOTO_BOLD: FontResource(
        path="roboto/bold.ttf",
        md5="b8e42971dec8d49207a8c8e2b919a6ac",
    ),
    FontRoboto.SERIF_LIGHT: FontResource(
        path="roboto_serif/light.ttf",
        md5="4781a153250a8caf652b4f5b129c30ed",
    ),
    FontRoboto.SERIF_REGULAR: FontResource(
        path="roboto_serif/regular.ttf",
        md5="2fde5a4a0cef2c19b4b6a30763322847",
    ),
    FontRoboto.SERIF_BOLD: FontResource(
        path="roboto_serif/bold.ttf",
        md5="8ec6ab43edac2144cfd2494d522de733",
    ),
    FontRoboto.MONO_LIGHT: FontResource(
        path="roboto_mono/light.ttf",
        md5="c9166464b1db95fc3cdf9b50fc7f98e2",
    ),
    FontRoboto.MONO_REGULAR: FontResource(
        path="roboto_mono/regular.ttf",
        md5="5b04fdfec4c8c36e8ca574e40b7148bb",
    ),
    FontRoboto.MONO_BOLD: FontResource(
        path="roboto_mono/bold.ttf",
        md5="90190d91283189e340b2a44fe560f2cd",
    ),
    FontRoboto.CONDENSED_LIGHT: FontResource(
        path="roboto_condensed/light.ttf",
        md5="68680c984f72eef7b2e2cf269382f2a6",
    ),
    FontRoboto.CONDENSED_REGULAR: FontResource(
        path="roboto_condensed/regular.ttf",
        md5="f1123f4b3d926ac4f72cc8091a4b5d19",
    ),
    FontRoboto.CONDENSED_BOLD: FontResource(
        path="roboto_condensed/bold.ttf",
        md5="0233b881b26ce6cc3884c6944940d11b",
    ),
    FontRoboto.SLAB_LIGHT: FontResource(
        path="roboto_slab/light.ttf",
        md5="4c63608980b784c679bbadeb18d9acf4",
    ),
    FontRoboto.SLAB_REGULAR: FontResource(
        path="roboto_slab/regular.ttf",
        md5="2100b4a02ebb94c0aa18cabd642ee507",
    ),
    FontRoboto.SLAB_BOLD: FontResource(
        path="roboto_slab/bold.ttf",
        md5="2c44adc1ebd36820fd75012412e6f550",
    ),
    FontSourceCode.ROBOTO_MONO: FontResource(
        path="roboto_mono/regular.ttf",
        md5="5b04fdfec4c8c36e8ca574e40b7148bb",
    ),
    FontSourceCode.COURIER: FontResource(
        path="mono_courier/regular.ttf",
        md5="fba4686ed1d1b4ef05ab14db78805dbe",
    ),
    FontSourceCode.SOURCECODEPRO: FontResource(
        path="mono_source_code_pro/regular.otf",
        md5="f471e697282189889a1514d0ebcf5491",
    ),
    FontSourceCode.SOURCEHANCODEJP: FontResource(
        path="mono_source_han_code_jp/regular.otf",
        md5="abcdbd5449ad6a30d540221a12f4a0b5",
    ),
    FontArabic.SANSSERIF_LIGHT: FontResource(
        path="arabic_noto_sans/light.ttf",
        md5="ffcfcc231a05032bca6e0819aa60eacb",
    ),
    FontArabic.SANSSERIF_REGULAR: FontResource(
        path="arabic_noto_sans/regular.ttf",
        md5="75527903c6a793772b02807c5343f4c8",
    ),
    FontArabic.SANSSERIF_BOLD: FontResource(
        path="arabic_noto_sans/bold.ttf",
        md5="cda675687ed1576b7bda072838c0ed5f",
    ),
    FontArabic.KUFI_LIGHT: FontResource(
        path="arabic_noto_kufi/light.ttf",
        md5="23517c64b528b3c744bfb3be94e58836",
    ),
    FontArabic.KUFI_REGULAR: FontResource(
        path="arabic_noto_kufi/regular.ttf",
        md5="600b529eb4849a54dde020e3ea389de2",
    ),
    FontArabic.KUFI_BOLD: FontResource(
        path="arabic_noto_kufi/bold.ttf",
        md5="34886bd59d48cf9113e1e9386bee615e",
    ),
    FontArabic.NASKH_REGULAR: FontResource(
        path="arabic_noto_naskh/regular.ttf",
        md5="08f2d6bfe92d3e78721a0e1746397344",
    ),
    FontArabic.NASKH_BOLD: FontResource(
        path="arabic_noto_naskh/bold.ttf",
        md5="3e8ac1d70691caf5ddfd36fee8acce3d",
    ),
    FontBrahmic.BENGALI_SANSSERIF_LIGHT: FontResource(
        path="brahmic_bengali_noto_sans/light.ttf",
        md5="7e54641bfed39afb0b9b957168eb7869",
    ),
    FontBrahmic.BENGALI_SANSSERIF_REGULAR: FontResource(
        path="brahmic_bengali_noto_sans/regular.ttf",
        md5="997ec45c6f75da576966ce470cebdd8f",
    ),
    FontBrahmic.BENGALI_SANSSERIF_BOLD: FontResource(
        path="brahmic_bengali_noto_sans/bold.ttf",
        md5="b4463ed2663bd59adff9ef090dabaa14",
    ),
    FontBrahmic.BENGALI_SERIF_LIGHT: FontResource(
        path="brahmic_bengali_noto_serif/light.ttf",
        md5="1890d63acffba90859e2bfb2bea18035",
    ),
    FontBrahmic.BENGALI_SERIF_REGULAR: FontResource(
        path="brahmic_bengali_noto_serif/regular.ttf",
        md5="7de2929b2584456afd8251c356de1285",
    ),
    FontBrahmic.BENGALI_SERIF_BOLD: FontResource(
        path="brahmic_bengali_noto_serif/bold.ttf",
        md5="eccf90709f61853a4aa1d184f8e54216",
    ),
    FontBrahmic.DEVANAGARI_SANSSERIF_LIGHT: FontResource(
        path="brahmic_devanagari_noto_sans/light.ttf",
        md5="be21506bd5d277aa33b7d6d2563477af",
    ),
    FontBrahmic.DEVANAGARI_SANSSERIF_REGULAR: FontResource(
        path="brahmic_devanagari_noto_sans/regular.ttf",
        md5="46dbe14f577b56ade221acf89631fd7b",
    ),
    FontBrahmic.DEVANAGARI_SANSSERIF_BOLD: FontResource(
        path="brahmic_devanagari_noto_sans/bold.ttf",
        md5="bb252b622a58dc3bf433dbf5754e6f7e",
    ),
    FontBrahmic.DEVANAGARI_SERIF_LIGHT: FontResource(
        path="brahmic_devanagari_noto_serif/light.ttf",
        md5="bae0ad5209cfee6a43bbd3163b98056c",
    ),
    FontBrahmic.DEVANAGARI_SERIF_REGULAR: FontResource(
        path="brahmic_devanagari_noto_serif/regular.ttf",
        md5="6c24c42e9eafb1cdda367671361f52a2",
    ),
    FontBrahmic.DEVANAGARI_SERIF_BOLD: FontResource(
        path="brahmic_devanagari_noto_serif/bold.ttf",
        md5="bedfefb38fe53bc1fa18c5a651c1d7b3",
    ),
    FontBrahmic.TAMIL_SANSSERIF_LIGHT: FontResource(
        path="brahmic_tamil_noto_sans/light.ttf",
        md5="b6ced5e5b7a0d6f2e763db77705cb7cc",
    ),
    FontBrahmic.TAMIL_SANSSERIF_REGULAR: FontResource(
        path="brahmic_tamil_noto_sans/regular.ttf",
        md5="cfd0079baedcd7cd5d2ad98c1489d023",
    ),
    FontBrahmic.TAMIL_SANSSERIF_BOLD: FontResource(
        path="brahmic_tamil_noto_sans/bold.ttf",
        md5="df89701fdee0d1de9f7f6c7fbbae8874",
    ),
    FontBrahmic.TAMIL_SERIF_LIGHT: FontResource(
        path="brahmic_tamil_noto_serif/light.ttf",
        md5="0e5ddcae43424e9a547917ec1e997695",
    ),
    FontBrahmic.TAMIL_SERIF_REGULAR: FontResource(
        path="brahmic_tamil_noto_serif/regular.ttf",
        md5="0916bea8b08896c86b50c6766f506416",
    ),
    FontBrahmic.TAMIL_SERIF_BOLD: FontResource(
        path="brahmic_tamil_noto_serif/bold.ttf",
        md5="32be9efedcdf21ad3cbb960b43f8e575",
    ),
    FontBrahmic.TELUGU_SANSSERIF_LIGHT: FontResource(
        path="brahmic_telugu_noto_sans/light.ttf",
        md5="644489807d1b7ff280724920e6d46208",
    ),
    FontBrahmic.TELUGU_SANSSERIF_REGULAR: FontResource(
        path="brahmic_telugu_noto_sans/regular.ttf",
        md5="79fd1e624e819497bc22b35830906ecb",
    ),
    FontBrahmic.TELUGU_SANSSERIF_BOLD: FontResource(
        path="brahmic_telugu_noto_sans/bold.ttf",
        md5="48dd5f30af67f36e23c885e341094d83",
    ),
    FontBrahmic.TELUGU_SERIF_LIGHT: FontResource(
        path="brahmic_telugu_noto_serif/light.ttf",
        md5="9e72f2730d10bd62e437360f30dc3e63",
    ),
    FontBrahmic.TELUGU_SERIF_REGULAR: FontResource(
        path="brahmic_telugu_noto_serif/regular.ttf",
        md5="0d5da9d39e03e0dbdfb91002710f4be0",
    ),
    FontBrahmic.TELUGU_SERIF_BOLD: FontResource(
        path="brahmic_telugu_noto_serif/bold.ttf",
        md5="b12935df488a2a17167e180ea3569360",
    ),
    FontChinese.SIMPLIFIED_SANSSERIF_LIGHT: FontResource(
        path="chinese_simplified_noto_sans/light.ttf",
        md5="d52d4d74290978e137446b7b62b1c5d2",
    ),
    FontChinese.SIMPLIFIED_SANSSERIF_REGULAR: FontResource(
        path="chinese_simplified_noto_sans/regular.ttf",
        md5="19498325f22381f551df06ce1b4cad4f",
    ),
    FontChinese.SIMPLIFIED_SANSSERIF_BOLD: FontResource(
        path="chinese_simplified_noto_sans/bold.ttf",
        md5="f8f91dd976cfe63e46490e63345e8c2e",
    ),
    FontChinese.SIMPLIFIED_SERIF_LIGHT: FontResource(
        path="chinese_simplified_noto_serif/light.ttf",
        md5="33c62feebda55f521b6210671c9f3df8",
    ),
    FontChinese.SIMPLIFIED_SERIF_REGULAR: FontResource(
        path="chinese_simplified_noto_serif/regular.ttf",
        md5="3d973955a90c1a69029f56fd52b7c7a2",
    ),
    FontChinese.SIMPLIFIED_SERIF_BOLD: FontResource(
        path="chinese_simplified_noto_serif/bold.ttf",
        md5="848c527475e6444da5bc77f540f3d701",
    ),
    FontChinese.TRADITIONAL_SANSSERIF_LIGHT: FontResource(
        path="chinese_traditional_noto_sans/light.ttf",
        md5="b00ec05f9416dcf69687be79e2c645d7",
    ),
    FontChinese.TRADITIONAL_SANSSERIF_REGULAR: FontResource(
        path="chinese_traditional_noto_sans/regular.ttf",
        md5="ad18e8fc265252917dd3698e268977d7",
    ),
    FontChinese.TRADITIONAL_SANSSERIF_BOLD: FontResource(
        path="chinese_traditional_noto_sans/bold.ttf",
        md5="a4ee55b412c13458ec428c1f6821e283",
    ),
    FontChinese.TRADITIONAL_SERIF_LIGHT: FontResource(
        path="chinese_traditional_noto_serif/light.ttf",
        md5="d1b13a4bdcde44b480cee69815a375cd",
    ),
    FontChinese.TRADITIONAL_SERIF_REGULAR: FontResource(
        path="chinese_traditional_noto_serif/regular.ttf",
        md5="4fbc0356bda7984a81788c9614d27867",
    ),
    FontChinese.TRADITIONAL_SERIF_BOLD: FontResource(
        path="chinese_traditional_noto_serif/bold.ttf",
        md5="5144d59a55c50e9f23aea89041af0d23",
    ),
    FontChinese.HONGKONG_SANSSERIF_LIGHT: FontResource(
        path="chinese_hongkong_noto_sans/light.ttf",
        md5="c014c66923388c93ec4b0158687f1604",
    ),
    FontChinese.HONGKONG_SANSSERIF_REGULAR: FontResource(
        path="chinese_hongkong_noto_sans/regular.ttf",
        md5="7882ea6ae9cc19826e98cc46769f15fe",
    ),
    FontChinese.HONGKONG_SANSSERIF_BOLD: FontResource(
        path="chinese_hongkong_noto_sans/bold.ttf",
        md5="f5fbe3e2e9478bfc00e255934fc1a842",
    ),
    FontChinese.HONGKONG_SERIF_LIGHT: FontResource(
        path="chinese_hongkong_noto_serif/light.ttf",
        md5="c61d4737ea4a774853955b86b38fc871",
    ),
    FontChinese.HONGKONG_SERIF_REGULAR: FontResource(
        path="chinese_hongkong_noto_serif/regular.ttf",
        md5="d8e6524288c8c19327d3562ca431b471",
    ),
    FontChinese.HONGKONG_SERIF_BOLD: FontResource(
        path="chinese_hongkong_noto_serif/bold.ttf",
        md5="08302783208cf67b70d2b53bbc3150b8",
    ),
    FontJapanese.SANSSERIF_LIGHT: FontResource(
        path="japanese_noto_sans/light.ttf",
        md5="7d1e0e68062ba3ae1cc12009620f645d",
    ),
    FontJapanese.SANSSERIF_REGULAR: FontResource(
        path="japanese_noto_sans/regular.ttf",
        md5="022f32abf24d5534496095e04aa739b3",
    ),
    FontJapanese.SANSSERIF_BOLD: FontResource(
        path="japanese_noto_sans/bold.ttf",
        md5="4aec04fd98881db5fbc79075428727ef",
    ),
    FontJapanese.SERIF_LIGHT: FontResource(
        path="japanese_noto_serif/light.ttf",
        md5="0f3e1a61caa6528059bf62dae1902235",
    ),
    FontJapanese.SERIF_REGULAR: FontResource(
        path="japanese_noto_serif/regular.ttf",
        md5="a0cc86e68bdf1711e30bffb6d0bb0b49",
    ),
    FontJapanese.SERIF_BOLD: FontResource(
        path="japanese_noto_serif/bold.ttf",
        md5="9ec5752a714a1f0871b4ad04f0d6f283",
    ),
    FontJapanese.MPLUS1P_LIGHT: FontResource(
        path="japanese_mplus_1p/light.ttf",
        md5="01fea1cae2979588652514d83e9c0423",
    ),
    FontJapanese.MPLUS1P_REGULAR: FontResource(
        path="japanese_mplus_1p/regular.ttf",
        md5="bfab3ff358a7fa14c5703ad49063cb16",
    ),
    FontJapanese.MPLUS1P_BOLD: FontResource(
        path="japanese_mplus_1p/bold.ttf",
        md5="aa140061f44d0dda19ab2573a0ad93d3",
    ),
    FontJapanese.MPLUSROUNDED1C_LIGHT: FontResource(
        path="japanese_mplus_rounded1c/light.ttf",
        md5="9c62a03e973fc7c73bfb935296a2b693",
    ),
    FontJapanese.MPLUSROUNDED1C_REGULAR: FontResource(
        path="japanese_mplus_rounded1c/regular.ttf",
        md5="686088cf66e883b2d4c2e8c9cde6d32f",
    ),
    FontJapanese.MPLUSROUNDED1C_BOLD: FontResource(
        path="japanese_mplus_rounded1c/bold.ttf",
        md5="d4599c8dc8ba3353fd83af468838f1f8",
    ),
    FontJapanese.SAWARABI_GOTHIC: FontResource(
        path="japanese_sawarabi_gothic/regular.ttf",
        md5="28d35b15cdc5fc9937335bfed22e1838",
    ),
    FontJapanese.SAWARABI_MINCHO: FontResource(
        path="japanese_sawarabi_mincho/regular.ttf",
        md5="568e086e3451178636c5f10761df2c45",
    ),
    FontKorean.SANSSERIF_LIGHT: FontResource(
        path="korean_noto_sans/light.ttf",
        md5="e61301e66b058697c6031c39edb7c0d2",
    ),
    FontKorean.SANSSERIF_REGULAR: FontResource(
        path="korean_noto_sans/regular.ttf",
        md5="e910afbd441c5247227fb4a731d65799",
    ),
    FontKorean.SANSSERIF_BOLD: FontResource(
        path="korean_noto_sans/bold.ttf",
        md5="671db5f821991c90d7f8499bcf9fed7e",
    ),
    FontKorean.SERIF_LIGHT: FontResource(
        path="korean_noto_serif/light.ttf",
        md5="9922efae87ff1960a63efdc3466edd90",
    ),
    FontKorean.SERIF_REGULAR: FontResource(
        path="korean_noto_serif/regular.ttf",
        md5="80c68ab78fd0e67500929a9cdc53da0c",
    ),
    FontKorean.SERIF_BOLD: FontResource(
        path="korean_noto_serif/bold.ttf",
        md5="8c4085a8e0d34353e2f0d9285abef61e",
    ),
    FontThai.SANSSERIF_LIGHT: FontResource(
        path="thai_noto_sans/light.ttf",
        md5="fa192df61c8ef9a6a204c6323fdae9dc",
    ),
    FontThai.SANSSERIF_REGULAR: FontResource(
        path="thai_noto_sans/regular.ttf",
        md5="a84996ee5e940db8c7c2e1375728ca68",
    ),
    FontThai.SANSSERIF_BOLD: FontResource(
        path="thai_noto_sans/bold.ttf",
        md5="1296256d14a6c704f87967dc06583a64",
    ),
    FontThai.SERIF_LIGHT: FontResource(
        path="thai_noto_serif/light.ttf",
        md5="70c158b4144d83cba0f7266952ddad2f",
    ),
    FontThai.SERIF_REGULAR: FontResource(
        path="thai_noto_serif/regular.ttf",
        md5="fe28175fbf4e79f1562d30f60933cab7",
    ),
    FontThai.SERIF_BOLD: FontResource(
        path="thai_noto_serif/bold.ttf",
        md5="dc10158f174b8141c810880b98ba5a5a",
    ),
}
