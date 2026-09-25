# Font Classes


In Drawlib, fonts are categorized into various Font Classes, each serving different purposes and supporting different styles and languages. 
Here's an overview of the supported Font Classes:

- Default Fonts

    - `Font`: Supports both SanSerif and Serif fonts for Alphabet and CJK (Chinese, Japanese, Korean) characters.

- Alphabet Fonts

    - `FontSansSerif`: Specifically SanSerif fonts for Alphabet characters.
    - `FontSerif`: Specifically Serif fonts for Alphabet characters.
    - `FontMonoSpace`: Monospace fonts, where each character occupies the same amount of horizontal space.
    - `FontSourcecode`:  A subset of FontMonoSpace fonts, optimized for source code display using `SourceCode`.
    - `FontRoboto`: Fonts from the Roboto family, tailored for Alphabet characters.

- Local Language Fonts

    - `FontArabic`: Fonts specifically designed for Arabic script.
    - `FontBrahmic`: Fonts for Brahmic scripts used in India and neighboring countries.
    - `FontChinese`: Fonts tailored for Chinese characters.
    - `FontJapanese`: Fonts designed for Japanese characters.
    - `FontKorean`: Fonts specifically for Korean characters.
    - `FontThai`: Fonts optimized for Thai script.

Each font class supports various styles, though some fonts may have fewer styles available:

- Light: A lighter weight variant of the font.
- Regular: The standard, normal-weight variant of the font.
- Bold: A heavier, bold-weight variant of the font.

Due to the large file sizes of font files, Drawlib does not include them in the initial package when installed via pip. 
Instead, the necessary font files are downloaded dynamically the first time they are used. 
This approach minimizes the initial package size and allows for on-demand fetching of resources. 
Once downloaded, these font files are cached on your local machine.

If needed, you can manage the font cache using the `drawlib cache clear` command (or `drawlib cache list`). 
This command clears the cached font files from your system, freeing up storage space if necessary.



# FontFile


The `FontFile` class in Drawlib allows users to utilize custom fonts for rendering text using the `text()` function and similar methods. 
Here's how you can use the FontFile class in your Python code:


```python
from drawlib.canvas import config
from drawlib.fonts import FontFile
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=50)
text(
    (50, 25),
    "Hello Drawlib!",
    style=Style(
        text_size=36,
        text_font=FontFile("../_assets/avenger/regular.ttf"),
    ),
)
```

Executing this code generates the output:


```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontFile
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=50)
text(
    (50, 25),
    "Hello Drawlib!",
    style=Style(
        text_size=36,
        text_font=FontFile("../_assets/avenger/regular.ttf"),
    ),
)
```


# Font


The `Font` class in Drawlib provides default fonts. 
Here's an overview of the fonts available in the Font class:

- SanSerif Fonts

    - `SANSSERIF_LIGHT`: Noto SansSerif CJK(Chinese, Japanese, Korean)
    - `SANSSERIF_REGULAR`
    - `SANSSERIF_BOLD`

- Serif Fonts

    - `SERIF_LIGHT`: Noto Serif CJK Japanese
    - `SERIF_REGULAR`
    - `SERIF_BOLD`

By default, Drawlib's default preset styles use `Font.SANSSERIF_REGULAR`. 
This font choice is based on its standard shape and wide coverage across different languages and populations.

The following image illustrates the fonts available in the Font class:


```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import Font
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("SansSerif", Font.SANSSERIF_LIGHT, Font.SANSSERIF_REGULAR, Font.SANSSERIF_BOLD),
    ("Serif", Font.SERIF_LIGHT, Font.SERIF_REGULAR, Font.SERIF_BOLD),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), "Hello Drawlib!", style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), "Hello Drawlib!", style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), "Hello Drawlib!", style=Style(text_size=16, text_font=bold))

```


# FontSansSerif


Class `FontSansSerif` contains popular SansSerif fonts for alphabet languages.

- Lato

    - `LATO_LIGHT`
    - `LATO_REGULAR`
    - `LATO_BOLD`

- Raleways

    - `RALEWAYS_LIGHT`
    - `RALEWAYS_REGULAR`
    - `RALEWAYS_BOLD`

- Montserrat

    - `MONTSERRAT_LIGHT`
    - `MONTSERRAT_REGULAR`
    - `MONTSERRAT_BOLD`

- Oswald

    - `OSWALD_LIGHT`
    - `OSWALD_REGULAR`
    - `OSWALD_BOLD`

- Poppins

    - `POPPINS_LIGHT`
    - `POPPINS_REGULAR`
    - `POPPINS_BOLD`

```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontSansSerif
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("Lato", FontSansSerif.LATO_LIGHT, FontSansSerif.LATO_REGULAR, FontSansSerif.LATO_BOLD),
    ("Raleways", FontSansSerif.RALEWAYS_LIGHT, FontSansSerif.RALEWAYS_REGULAR, FontSansSerif.RALEWAYS_BOLD),
    ("Montserrat", FontSansSerif.MONTSERRAT_LIGHT, FontSansSerif.MONTSERRAT_REGULAR, FontSansSerif.MONTSERRAT_BOLD),
    ("Oswald", FontSansSerif.OSWALD_LIGHT, FontSansSerif.OSWALD_REGULAR, FontSansSerif.OSWALD_BOLD),
    ("Poppins", FontSansSerif.POPPINS_LIGHT, FontSansSerif.POPPINS_REGULAR, FontSansSerif.POPPINS_BOLD),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), "Hello Drawlib!", style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), "Hello Drawlib!", style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), "Hello Drawlib!", style=Style(text_size=16, text_font=bold))

```


# FontSerif


Class `FontSerif` contains popular Serif fonts for alphabet languages.

- Courier

    - `COURIER_REGULAR`
    - `COURIER_BOLD`

- Merriweather

    - `MERRIWEATHER_LIGHT`
    - `MERRIWEATHER_REGULAR`
    - `MERRIWEATHER_BOLD`

- Platypi

    - `PLATYPI_LIGHT`
    - `PLATYPI_REGULAR`
    - `PLATYPI_BOLD`

- PlayFairDisplay

    - `PLAYFAIRDISPLAY_LIGHT`
    - `PLAYFAIRDISPLAY_REGULAR`
    - `PLAYFAIRDISPLAY_BOLD`

```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontSerif
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("Courier", None, FontSerif.COURIER_REGULAR, FontSerif.COURIER_BOLD),
    ("Merriweather", FontSerif.MERRIWEATHER_LIGHT, FontSerif.MERRIWEATHER_REGULAR, FontSerif.MERRIWEATHER_BOLD),
    ("Platypi", FontSerif.PLATYPI_LIGHT, FontSerif.PLATYPI_REGULAR, FontSerif.PLATYPI_BOLD),
    ("Play Fair Display", None, FontSerif.PLAYFAIRDISPLAY_REGULAR, FontSerif.PLAYFAIRDISPLAY_BOLD),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), "Hello Drawlib!", style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), "Hello Drawlib!", style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), "Hello Drawlib!", style=Style(text_size=16, text_font=bold))

```


# FontRoboto


Class `FontRoboto` famous and popular Roboto group fonts.

- Roboto

    - `ROBOTO_LIGHT`
    - `ROBOTO_REGULAR`
    - `ROBOTO_BOLD`

- Roboto Serif

    - `SERIF_LIGHT`
    - `SERIF_REGULAR`
    - `SERIF_BOLD`

- Roboto Mono

    - `MONO_LIGHT`
    - `MONO_REGULAR`
    - `MONO_BOLD`

- Roboto Condensed

    - `CONDENSED_LIGHT`
    - `CONDENSED_REGULAR`
    - `CONDENSED_BOLD`

- Roboto Slab

    - `SLAB_LIGHT`
    - `SLAB_REGULAR`
    - `SLAB_BOLD`

```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontRoboto
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("Roboto", FontRoboto.ROBOTO_LIGHT, FontRoboto.ROBOTO_REGULAR, FontRoboto.ROBOTO_BOLD),
    ("Roboto Serif", FontRoboto.SERIF_LIGHT, FontRoboto.SERIF_REGULAR, FontRoboto.SERIF_BOLD),
    ("Roboto Mono", FontRoboto.MONO_LIGHT, FontRoboto.MONO_REGULAR, FontRoboto.MONO_BOLD),
    ("Roboto Condensed", FontRoboto.CONDENSED_LIGHT, FontRoboto.CONDENSED_REGULAR, FontRoboto.CONDENSED_BOLD),
    ("Roboto Slab", FontRoboto.SLAB_LIGHT, FontRoboto.SLAB_REGULAR, FontRoboto.SLAB_BOLD),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), "Hello Drawlib!", style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), "Hello Drawlib!", style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), "Hello Drawlib!", style=Style(text_size=16, text_font=bold))

```


# FontMonoSpace


Class `FontMonoSpace` contains  mono space fonts.
Almost all are for alphabet, but SourceHanCodeJP supports Japanese.

- Courier

    - `COURIER_REGULAR`
    - `COURIER_BOLD`

- Roboto Mono

    - `ROBOTO_MONO_LIGHT`
    - `ROBOTO_MONO_REGULAR`
    - `ROBOTO_MONO_BOLD`

- SourceCodePro

    - `SOURCECODEPRO_LIGHT`
    - `SOURCECODEPRO_REGULAR`
    - `SOURCECODEPRO_BOLD`

- SourceHanCodeJP

    - `SOURCEHANCODEJP_LIGHT`
    - `SOURCEHANCODEJP_REGULAR`
    - `SOURCEHANCODEJP_BOLD`


```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontMonoSpace
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("Courier", None, FontMonoSpace.COURIER_REGULAR, FontMonoSpace.COURIER_BOLD),
    ("Roboto Mono", FontMonoSpace.ROBOTO_MONO_LIGHT, FontMonoSpace.ROBOTO_MONO_REGULAR, FontMonoSpace.ROBOTO_MONO_BOLD),
    ("Source Code Pro", FontMonoSpace.SOURCECODEPRO_LIGHT, FontMonoSpace.SOURCECODEPRO_REGULAR, FontMonoSpace.SOURCECODEPRO_BOLD),
    ("Source Han Code JP", FontMonoSpace.SOURCEHANCODEJP_LIGHT, FontMonoSpace.SOURCEHANCODEJP_REGULAR, FontMonoSpace.SOURCEHANCODEJP_BOLD),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), "Hello Drawlib!", style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), "Hello Drawlib!", style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), "Hello Drawlib!", style=Style(text_size=16, text_font=bold))

```


# FontArabic


Class `FontArabic` contains Arabic fonts.

- Sans Serif

    - `SANSSERIF_LIGHT`
    - `SANSSERIF_REGULAR`
    - `SANSSERIF_BOLD`

- Kufi

    - `KUFI_LIGHT`
    - `KUFI_REGULAR`
    - `KUFI_BOLD`

- Naskh

    - `NASKH_LIGHT`
    - `NASKH_REGULAR`
    - `NASKH_BOLD`

```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontArabic
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("SansSerif", FontArabic.SANSSERIF_LIGHT, FontArabic.SANSSERIF_REGULAR, FontArabic.SANSSERIF_BOLD),
    ("Kufi", FontArabic.KUFI_LIGHT, FontArabic.KUFI_REGULAR, FontArabic.KUFI_BOLD),
    ("Naskh", None, FontArabic.NASKH_REGULAR, FontArabic.NASKH_BOLD),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

sample = "لمّا كان الاعتر "
for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), sample, style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), sample, style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), sample, style=Style(text_size=16, text_font=bold))

```


# FontBrahmic


Class `FontBrahmic` contains fonts for characters which delived from Brahmic.

- Bengali

    - `BENGALI_SANSSERIF_LIGHT`
    - `BENGALI_SANSSERIF_REGULAR`
    - `BENGALI_SANSSERIF_BOLD`
    - `BENGALI_SERIF_LIGHT`
    - `BENGALI_SERIF_REGULAR`
    - `BENGALI_SERIF_BOLD`

- Devanagari

    - `DEVANAGARI_SANSSERIF_LIGHT`
    - `DEVANAGARI_SANSSERIF_REGULAR`
    - `DEVANAGARI_SANSSERIF_BOLD`
    - `DEVANAGARI_SERIF_LIGHT`
    - `DEVANAGARI_SERIF_REGULAR`
    - `DEVANAGARI_SERIF_BOLD`

- Tamil

    - `TAMIL_SANSSERIF_LIGHT`
    - `TAMIL_SANSSERIF_REGULAR`
    - `TAMIL_SANSSERIF_BOLD`
    - `TAMIL_SERIF_LIGHT`
    - `TAMIL_SERIF_REGULAR`
    - `TAMIL_SERIF_BOLD`

- Telugu

    - `TELUGU_SANSSERIF_LIGHT`
    - `TELUGU_SANSSERIF_REGULAR`
    - `TELUGU_SANSSERIF_BOLD`
    - `TELUGU_SERIF_LIGHT`
    - `TELUGU_SERIF_REGULAR`
    - `TELUGU_SERIF_BOLD`

```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontBrahmic
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("Bengali SansSerif", FontBrahmic.BENGALI_SANSSERIF_LIGHT, FontBrahmic.BENGALI_SANSSERIF_REGULAR, FontBrahmic.BENGALI_SANSSERIF_BOLD, "যেহেতু মানব পরিবারের"),
    ("Bengali Serif", FontBrahmic.BENGALI_SERIF_LIGHT, FontBrahmic.BENGALI_SERIF_REGULAR, FontBrahmic.BENGALI_SERIF_BOLD, "যেহেতু মানব পরিবারের"),
    ("Devanagari SansSerif", FontBrahmic.DEVANAGARI_SANSSERIF_LIGHT, FontBrahmic.DEVANAGARI_SANSSERIF_REGULAR, FontBrahmic.DEVANAGARI_SANSSERIF_BOLD, "चूंकि मानव परिवार"),
    ("Devanagari Serif", FontBrahmic.DEVANAGARI_SERIF_LIGHT, FontBrahmic.DEVANAGARI_SERIF_REGULAR, FontBrahmic.DEVANAGARI_SERIF_BOLD, "चूंकि मानव परिवार"),
    ("Tamil SansSerif", FontBrahmic.TAMIL_SANSSERIF_LIGHT, FontBrahmic.TAMIL_SANSSERIF_REGULAR, FontBrahmic.TAMIL_SANSSERIF_BOLD, "மனிதக் குடும்பத்தி"),
    ("Tamil Serif", FontBrahmic.TAMIL_SERIF_LIGHT, FontBrahmic.TAMIL_SERIF_REGULAR, FontBrahmic.TAMIL_SERIF_BOLD, "மனிதக் குடும்பத்தி"),
    ("Telugu SansSerif", FontBrahmic.TELUGU_SANSSERIF_LIGHT, FontBrahmic.TELUGU_SANSSERIF_REGULAR, FontBrahmic.TELUGU_SANSSERIF_BOLD, "మానవకుటంబమునందలి"),
    ("Telugu Serif", FontBrahmic.TELUGU_SERIF_LIGHT, FontBrahmic.TELUGU_SERIF_REGULAR, FontBrahmic.TELUGU_SERIF_BOLD, "మానవకుటంబమునందలి"),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

for i, (name, light, regular, bold, sample) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), sample, style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), sample, style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), sample, style=Style(text_size=16, text_font=bold))

```


# FontChinese


Class `FontChinese` contains Chinese fonts.

- Simplified

    - `SIMPLIFIED_SANSSERIF_LIGHT`
    - `SIMPLIFIED_SANSSERIF_REGULAR`
    - `SIMPLIFIED_SANSSERIF_BOLD`
    - `SIMPLIFIED_SERIF_LIGHT`
    - `SIMPLIFIED_SERIF_REGULAR`
    - `SIMPLIFIED_SERIF_BOLD`

- Traditional

    - `TRADITIONAL_SANSSERIF_LIGHT`
    - `TRADITIONAL_SANSSERIF_REGULAR`
    - `TRADITIONAL_SANSSERIF_BOLD`
    - `TRADITIONAL_SERIF_LIGHT`
    - `TRADITIONAL_SERIF_REGULAR`
    - `TRADITIONAL_SERIF_BOLD`

- HongKong

    - `HONGKONG_SANSSERIF_LIGHT`
    - `HONGKONG_SANSSERIF_REGULAR`
    - `HONGKONG_SANSSERIF_BOLD`
    - `HONGKONG_SERIF_LIGHT`
    - `HONGKONG_SERIF_REGULAR`
    - `HONGKONG_SERIF_BOLD`

```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontChinese
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("Simplified SansSerif", FontChinese.SIMPLIFIED_SANSSERIF_LIGHT, FontChinese.SIMPLIFIED_SANSSERIF_REGULAR, FontChinese.SIMPLIFIED_SANSSERIF_BOLD),
    ("Simplified Serif", FontChinese.SIMPLIFIED_SERIF_LIGHT, FontChinese.SIMPLIFIED_SERIF_REGULAR, FontChinese.SIMPLIFIED_SERIF_BOLD),
    ("Traditional SansSerif", FontChinese.TRADITIONAL_SANSSERIF_LIGHT, FontChinese.TRADITIONAL_SANSSERIF_REGULAR, FontChinese.TRADITIONAL_SANSSERIF_BOLD),
    ("Traditional Serif", FontChinese.TRADITIONAL_SERIF_LIGHT, FontChinese.TRADITIONAL_SERIF_REGULAR, FontChinese.TRADITIONAL_SERIF_BOLD),
    ("Hongkong SansSerif", FontChinese.HONGKONG_SANSSERIF_LIGHT, FontChinese.HONGKONG_SANSSERIF_REGULAR, FontChinese.HONGKONG_SANSSERIF_BOLD),
    ("Hongkong Serif", FontChinese.HONGKONG_SERIF_LIGHT, FontChinese.HONGKONG_SERIF_REGULAR, FontChinese.HONGKONG_SERIF_BOLD),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

sample = "今天天气很好。"
for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), sample, style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), sample, style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), sample, style=Style(text_size=16, text_font=bold))

```


# FontJapanese


Class `FontJapanese` contains Japanese fonts.

- Sans Serif

    - `SANSSERIF_LIGHT`
    - `SANSSERIF_REGULAR`
    - `SANSSERIF_BOLD`

- Serif

    - `SERIF_LIGHT`
    - `SERIF_REGULAR`
    - `SERIF_BOLD`

- Mplus 1P

    - `MPLUS1P_LIGHT`
    - `MPLUS1P_REGULAR`
    - `MPLUS1P_BOLD`

- Mplus Rounded 1C

    - `MPLUSROUNDED1C_LIGHT`
    - `MPLUSROUNDED1C_REGULAR`
    - `MPLUSROUNDED1C_BOLD`

- Sawarabi

    - `SAWARABI_GOTHIC`
    - `SAWARABI_MINCHO`

```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontJapanese
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("SansSerif", FontJapanese.SANSSERIF_LIGHT, FontJapanese.SANSSERIF_REGULAR, FontJapanese.SANSSERIF_BOLD),
    ("Serif", FontJapanese.SERIF_LIGHT, FontJapanese.SERIF_REGULAR, FontJapanese.SERIF_BOLD),
    ("MPlus 1P", FontJapanese.MPLUS1P_LIGHT, FontJapanese.MPLUS1P_REGULAR, FontJapanese.MPLUS1P_BOLD),
    ("MPlus Rounded1C", FontJapanese.MPLUSROUNDED1C_LIGHT, FontJapanese.MPLUSROUNDED1C_REGULAR, FontJapanese.MPLUSROUNDED1C_BOLD),
    ("Sawarabi Gothic", None, FontJapanese.SAWARABI_GOTHIC, None),
    ("Sawarabi Mincho", None, FontJapanese.SAWARABI_MINCHO, None),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

sample = "今日はいい天気ですね。"
for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), sample, style=Style(text_size=15, text_font=light))
    if regular is not None:
        text((60, y), sample, style=Style(text_size=15, text_font=regular))
    if bold is not None:
        text((85, y), sample, style=Style(text_size=15, text_font=bold))

```


# FontKorean


Class `FontKorean` contains Korean fonts.

- Sans Serif

    - `SANSSERIF_LIGHT`
    - `SANSSERIF_REGULAR`
    - `SANSSERIF_BOLD`

- Serif

    - `SERIF_LIGHT`
    - `SERIF_REGULAR`
    - `SERIF_BOLD`

```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontKorean
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("SansSerif", FontKorean.SANSSERIF_LIGHT, FontKorean.SANSSERIF_REGULAR, FontKorean.SANSSERIF_BOLD),
    ("Serif", FontKorean.SERIF_LIGHT, FontKorean.SERIF_REGULAR, FontKorean.SERIF_BOLD),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

sample = "오늘은 날씨가 좋네요。"
for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), sample, style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), sample, style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), sample, style=Style(text_size=16, text_font=bold))

```


# FontThai


Class `FontThai` contains Thai fonts.

- Sans Serif

    - `SANSSERIF_LIGHT`
    - `SANSSERIF_REGULAR`
    - `SANSSERIF_BOLD`

- Serif

    - `SERIF_LIGHT`
    - `SERIF_REGULAR`
    - `SERIF_BOLD`

```drawlib 600px center
from drawlib.canvas import config
from drawlib.fonts import FontThai
from drawlib.text import text
from drawlib.types import Style

font_matrix = [
    ("SansSerif", FontThai.SANSSERIF_LIGHT, FontThai.SANSSERIF_REGULAR, FontThai.SANSSERIF_BOLD),
    ("Serif", FontThai.SERIF_LIGHT, FontThai.SERIF_REGULAR, FontThai.SERIF_BOLD),
]

config(width=100, height=50)
y_pitch = 50 / (len(font_matrix) + 2)

text((35, y_pitch * (len(font_matrix) + 1)), "light", style=Style(text_size=13))
text((60, y_pitch * (len(font_matrix) + 1)), "regular", style=Style(text_size=13))
text((85, y_pitch * (len(font_matrix) + 1)), "bold", style=Style(text_size=13))

sample = "วันนี้อากาศดีจังเลย"
for i, (name, light, regular, bold) in enumerate(font_matrix):
    y = y_pitch * (len(font_matrix) - i)
    text((10, y), name, style=Style(text_size=13))
    if light is not None:
        text((35, y), sample, style=Style(text_size=16, text_font=light))
    if regular is not None:
        text((60, y), sample, style=Style(text_size=16, text_font=regular))
    if bold is not None:
        text((85, y), sample, style=Style(text_size=16, text_font=bold))

```


# Request for Adding Fonts


We welcome suggestions for adding new fonts to our Drawlib library. 
To ensure compatibility and usability, please consider the following criteria before making a request:

- Free License: The font must be available under a free license.
- Compatibility: The font should work seamlessly with Drawlib. Note that emoji fonts may not be fully supported at this time.
- Language Support: Fonts for languages currently not supported by Drawlib are prioritized, including minor languages.
- Global Popularity: The font should be widely recognized and used globally.
- Regional Popularity: Fonts for local languages that are popular in specific regions are also highly considered.

Before submitting a request, we recommend testing the font using the `FontFile()` class to ensure it meets your requirements. 
At present, Drawlib does not include decorative or ornamental fonts.

Your input is valuable to us, and if your font suggestion meets these criteria, we will consider adding it in a future release.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
