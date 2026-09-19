from drawlib.apis import *

height = 50


def draw(text_, font_matrix, file_name, size1=16, size2=13):
    clear()
    config(width=100, height=height)
    style1 = TextStyle(size=size1)
    style2 = TextStyle(size=size2)
    y_pitch = height / (len(font_matrix) + 2)

    for i, fonts in enumerate(font_matrix, start=1):
        if len(fonts) == 4:
            name, light, regular, bold = fonts
        else:
            name, light, regular, bold, text_ = fonts

        y = y_pitch * i
        text((10, y), name, style=style2)

        if light is not None:
            style_light = style1.copy()
            style_light.font = light
            text((35, y), text=text_, style=style_light)

        if regular is not None:
            style_regular = style1.copy()
            style_regular.font = regular
            text((60, y), text=text_, style=style_regular)

        if bold is not None:
            style_bold = style1.copy()
            style_bold.font = bold
            text((85, y), text=text_, style=style_bold)

    y = y_pitch * (len(font_matrix) + 1)
    text((35, y), "light", style=style2)
    text((60, y), "regular", style=style2)
    text((85, y), "bold", style=style2)

    save(file_name)


draw(
    "Hello Drawlib!",
    [
        (
            "SansSerif",
            Font.SANSSERIF_LIGHT,
            Font.SANSSERIF_REGULAR,
            Font.SANSSERIF_BOLD,
        ),
        (
            "Serif",
            Font.SERIF_LIGHT,
            Font.SERIF_REGULAR,
            Font.SERIF_BOLD,
        ),
    ],
    "image_Font.png",
)

draw(
    "Hello Drawlib!",
    [
        (
            "Lato",
            FontSansSerif.LATO_LIGHT,
            FontSansSerif.LATO_REGULAR,
            FontSansSerif.LATO_BOLD,
        ),
        (
            "Montserrat",
            FontSansSerif.MONTSERRAT_LIGHT,
            FontSansSerif.MONTSERRAT_REGULAR,
            FontSansSerif.MONTSERRAT_BOLD,
        ),
        (
            "Oswald",
            FontSansSerif.OSWALD_LIGHT,
            FontSansSerif.OSWALD_REGULAR,
            FontSansSerif.OSWALD_BOLD,
        ),
        (
            "Poppins",
            FontSansSerif.POPPINS_LIGHT,
            FontSansSerif.POPPINS_REGULAR,
            FontSansSerif.POPPINS_BOLD,
        ),
        (
            "Raleways",
            FontSansSerif.RALEWAYS_LIGHT,
            FontSansSerif.RALEWAYS_REGULAR,
            FontSansSerif.RALEWAYS_BOLD,
        ),
    ],
    "image_FontSansSerif.png",
)

draw(
    "Hello Drawlib!",
    [
        (
            "Courier",
            None,
            FontSerif.COURIER_REGULAR,
            FontSerif.COURIER_BOLD,
        ),
        (
            "Merriweather",
            FontSerif.MERRIWEATHER_LIGHT,
            FontSerif.MERRIWEATHER_REGULAR,
            FontSerif.MERRIWEATHER_BOLD,
        ),
        (
            "Platypi",
            FontSerif.PLATYPI_LIGHT,
            FontSerif.PLATYPI_REGULAR,
            FontSerif.PLATYPI_BOLD,
        ),
        (
            "Play Fair Display",
            None,
            FontSerif.PLAYFAIRDISPLAY_REGULAR,
            FontSerif.PLAYFAIRDISPLAY_BOLD,
        ),
    ],
    "image_FontSerif.png",
)

draw(
    "Hello Drawlib!",
    [
        (
            "Courier",
            None,
            FontMonoSpace.COURIER_REGULAR,
            FontMonoSpace.COURIER_BOLD,
        ),
        (
            "Roboto Mono",
            FontMonoSpace.ROBOTO_MONO_LIGHT,
            FontMonoSpace.ROBOTO_MONO_REGULAR,
            FontMonoSpace.ROBOTO_MONO_BOLD,
        ),
        (
            "Source Code Pro",
            FontMonoSpace.SOURCECODEPRO_LIGHT,
            FontMonoSpace.SOURCECODEPRO_REGULAR,
            FontMonoSpace.SOURCECODEPRO_BOLD,
        ),
        (
            "Source Han Code JP",
            FontMonoSpace.SOURCEHANCODEJP_LIGHT,
            FontMonoSpace.SOURCEHANCODEJP_REGULAR,
            FontMonoSpace.SOURCEHANCODEJP_BOLD,
        ),
    ],
    "image_FontMonoSpace.png",
)

draw(
    "Hello Drawlib!",
    [
        (
            "Roboto",
            FontRoboto.ROBOTO_LIGHT,
            FontRoboto.ROBOTO_REGULAR,
            FontRoboto.ROBOTO_BOLD,
        ),
        (
            "Roboto Serif",
            FontRoboto.SERIF_LIGHT,
            FontRoboto.SERIF_REGULAR,
            FontRoboto.SERIF_BOLD,
        ),
        (
            "Roboto Mono",
            FontRoboto.MONO_LIGHT,
            FontRoboto.MONO_REGULAR,
            FontRoboto.MONO_BOLD,
        ),
        (
            "Roboto Condensed",
            FontRoboto.CONDENSED_LIGHT,
            FontRoboto.CONDENSED_REGULAR,
            FontRoboto.CONDENSED_BOLD,
        ),
        (
            "Roboto Slab",
            FontRoboto.SLAB_LIGHT,
            FontRoboto.SLAB_REGULAR,
            FontRoboto.SLAB_BOLD,
        ),
    ],
    "image_FontRoboto.png",
)

draw(
    "لمّا كان الاعتر ",
    [
        (
            "SansSerif",
            FontArabic.SANSSERIF_LIGHT,
            FontArabic.SANSSERIF_REGULAR,
            FontArabic.SANSSERIF_BOLD,
        ),
        (
            "Kufi",
            FontArabic.KUFI_LIGHT,
            FontArabic.KUFI_REGULAR,
            FontArabic.KUFI_BOLD,
        ),
        (
            "Naskh",
            None,
            FontArabic.NASKH_REGULAR,
            FontArabic.NASKH_BOLD,
        ),
    ],
    "image_FontArabic.png",
)

draw(
    "Hello Drawlib!",
    [
        (
            "Bengali SansSerif",
            FontBrahmic.BENGALI_SANSSERIF_LIGHT,
            FontBrahmic.BENGALI_SANSSERIF_REGULAR,
            FontBrahmic.BENGALI_SANSSERIF_BOLD,
            "যেহেতু মানব পরিবারের",
        ),
        (
            "Bengali Serif",
            FontBrahmic.BENGALI_SERIF_LIGHT,
            FontBrahmic.BENGALI_SERIF_REGULAR,
            FontBrahmic.BENGALI_SERIF_BOLD,
            "যেহেতু মানব পরিবারের",
        ),
        (
            "Devanagari SansSerif",
            FontBrahmic.DEVANAGARI_SANSSERIF_LIGHT,
            FontBrahmic.DEVANAGARI_SANSSERIF_REGULAR,
            FontBrahmic.DEVANAGARI_SANSSERIF_BOLD,
            "चूंकि मानव परिवार",
        ),
        (
            "Devanagari Serif",
            FontBrahmic.DEVANAGARI_SERIF_LIGHT,
            FontBrahmic.DEVANAGARI_SERIF_REGULAR,
            FontBrahmic.DEVANAGARI_SERIF_BOLD,
            "चूंकि मानव परिवार",
        ),
        (
            "Tamil SansSerif",
            FontBrahmic.TAMIL_SANSSERIF_LIGHT,
            FontBrahmic.TAMIL_SANSSERIF_REGULAR,
            FontBrahmic.TAMIL_SANSSERIF_BOLD,
            "மனிதக் குடும்பத்தி",
        ),
        (
            "Tamil Serif",
            FontBrahmic.TAMIL_SERIF_LIGHT,
            FontBrahmic.TAMIL_SERIF_REGULAR,
            FontBrahmic.TAMIL_SERIF_BOLD,
            "மனிதக் குடும்பத்தி",
        ),
        (
            "Telugu SansSerif",
            FontBrahmic.TELUGU_SANSSERIF_LIGHT,
            FontBrahmic.TELUGU_SANSSERIF_REGULAR,
            FontBrahmic.TELUGU_SANSSERIF_BOLD,
            "మానవకుటంబమునందలి",
        ),
        (
            "Telugu Serif",
            FontBrahmic.TELUGU_SERIF_LIGHT,
            FontBrahmic.TELUGU_SERIF_REGULAR,
            FontBrahmic.TELUGU_SERIF_BOLD,
            "మానవకుటంబమునందలి",
        ),
    ],
    "image_FontBrahmic.png",
)

draw(
    "今天天气很好。",
    [
        (
            "Simplified SansSerif",
            FontChinese.SIMPLIFIED_SANSSERIF_LIGHT,
            FontChinese.SIMPLIFIED_SANSSERIF_REGULAR,
            FontChinese.SIMPLIFIED_SANSSERIF_BOLD,
        ),
        (
            "Simplified Serif",
            FontChinese.SIMPLIFIED_SERIF_LIGHT,
            FontChinese.SIMPLIFIED_SERIF_REGULAR,
            FontChinese.SIMPLIFIED_SERIF_BOLD,
        ),
        (
            "Traditional SansSerif",
            FontChinese.TRADITIONAL_SANSSERIF_LIGHT,
            FontChinese.TRADITIONAL_SANSSERIF_REGULAR,
            FontChinese.TRADITIONAL_SANSSERIF_BOLD,
        ),
        (
            "Traditional Serif",
            FontChinese.TRADITIONAL_SERIF_LIGHT,
            FontChinese.TRADITIONAL_SERIF_REGULAR,
            FontChinese.TRADITIONAL_SERIF_BOLD,
        ),
        (
            "Hongkong SansSerif",
            FontChinese.HONGKONG_SANSSERIF_LIGHT,
            FontChinese.HONGKONG_SANSSERIF_REGULAR,
            FontChinese.HONGKONG_SANSSERIF_BOLD,
        ),
        (
            "Hongkong Serif",
            FontChinese.HONGKONG_SERIF_LIGHT,
            FontChinese.HONGKONG_SERIF_REGULAR,
            FontChinese.HONGKONG_SERIF_BOLD,
        ),
    ],
    "image_FontChinese.png",
)

draw(
    "今日はいい天気ですね。",
    [
        (
            "SansSerif",
            FontJapanese.SANSSERIF_LIGHT,
            FontJapanese.SANSSERIF_REGULAR,
            FontJapanese.SANSSERIF_BOLD,
        ),
        (
            "Serif",
            FontJapanese.SERIF_LIGHT,
            FontJapanese.SERIF_REGULAR,
            FontJapanese.SERIF_BOLD,
        ),
        (
            "MPlus 1P",
            FontJapanese.MPLUS1P_LIGHT,
            FontJapanese.MPLUS1P_REGULAR,
            FontJapanese.MPLUS1P_BOLD,
        ),
        (
            "MPlus Rounded1C",
            FontJapanese.MPLUSROUNDED1C_LIGHT,
            FontJapanese.MPLUSROUNDED1C_REGULAR,
            FontJapanese.MPLUSROUNDED1C_BOLD,
        ),
        (
            "Sawarabi Gothic",
            None,
            FontJapanese.SAWARABI_GOTHIC,
            None,
        ),
        (
            "Sawarabi Mincho",
            None,
            FontJapanese.SAWARABI_MINCHO,
            None,
        ),
    ],
    "image_FontJapanese.png",
    size1=15,
)

draw(
    "오늘은 날씨가 좋네요。",
    [
        (
            "SansSerif",
            FontKorean.SANSSERIF_LIGHT,
            FontKorean.SANSSERIF_REGULAR,
            FontKorean.SANSSERIF_BOLD,
        ),
        (
            "Serif",
            FontKorean.SERIF_LIGHT,
            FontKorean.SERIF_REGULAR,
            FontKorean.SERIF_BOLD,
        ),
    ],
    "image_FontKorean.png",
)

draw(
    "วันนี้อากาศดีจังเลย",
    [
        (
            "SansSerif",
            FontThai.SANSSERIF_LIGHT,
            FontThai.SANSSERIF_REGULAR,
            FontThai.SANSSERIF_BOLD,
        ),
        (
            "Serif",
            FontThai.SERIF_LIGHT,
            FontThai.SERIF_REGULAR,
            FontThai.SERIF_BOLD,
        ),
    ],
    "image_FontThai.png",
)
