# drawlib.fonts

Multilingual and technical typography enumerations (`Font`, `FontSansSerif`, `FontSerif`, `FontMonoSpace`, `FontRoboto`, `FontSourceCode`, and regional scripts) plus custom TrueType/OpenType loading (`FontFile`). Import font families via `from drawlib.fonts import Font, FontFile, FontMonoSpace, FontRoboto, FontSansSerif, FontSerif` and pass them to `Style.text_font` or `BaseStyles.patch_font()`.

```drawlib align=center code=fold file=07_fonts_hero.png caption="Typography Families in drawlib.fonts — Universal CJK, Sans-Serif, Editorial Serif, and Technical Monospace"
from drawlib.canvas import save, setup
from drawlib.fonts import Font, FontMonoSpace, FontRoboto, FontSansSerif, FontSerif
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=58)

phosphor.text_aa((27.0, 52.2), width=4.2, style=Styles.PrimaryBold)
text(
    (30.8, 52.2),
    "Multilingual & Technical Typography  (drawlib.fonts)",
    style=Styles.DarkBold.patch(text_size=12.0, halign="left"),
)

# Card 1 (Top-Left, Focal Hero): Universal CJK + Latin (Font)
rectangle((31.5, 37.0), width=53, height=18.5, style=Styles.PrimaryFlat.patch(shape_r=2.0))
text(
    (31.5, 40.5),
    "Font  (Universal CJK + Latin)",
    style=Styles.WhiteBold.patch(text_font=Font.SANSSERIF_BOLD, text_size=11.2),
)
text(
    (31.5, 33.2),
    "System Architecture / 図解・日本語",
    style=Styles.White.patch(text_font=Font.SANSSERIF_REGULAR, text_size=10.5),
)

# Card 2 (Top-Right, Neutral): Western Sans-Serif (FontRoboto / FontSansSerif)
rectangle((88.5, 37.0), width=53, height=18.5, style=Styles.Neutral.patch(shape_r=2.0))
text(
    (88.5, 40.5),
    "FontRoboto & FontSansSerif",
    style=Styles.DarkBold.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=11.2),
)
text(
    (88.5, 33.2),
    "Geometric UI  ·  Thin / Regular / Bold",
    style=Styles.Dark.patch(text_font=FontSansSerif.POPPINS_REGULAR, text_size=10.2),
)

# Card 3 (Bottom-Left, PrimaryNeutral): Editorial Serif (FontSerif)
rectangle((31.5, 14.5), width=53, height=18.5, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
text(
    (31.5, 18.0),
    "FontSerif  (Merriweather & Platypi)",
    style=Styles.DarkBold.patch(text_font=FontSerif.MERRIWEATHER_BOLD, text_size=10.8),
)
text(
    (31.5, 10.8),
    "Editorial Reports & Whitepapers",
    style=Styles.Dark.patch(text_font=FontSerif.MERRIWEATHER_REGULAR, text_size=10.2),
)

# Card 4 (Bottom-Right, SecondaryNeutral): Technical Monospace (FontMonoSpace)
rectangle((88.5, 14.5), width=53, height=18.5, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
text(
    (88.5, 18.0),
    "FontMonoSpace & FontSourceCode",
    style=Styles.DarkBold.patch(text_font=FontMonoSpace.SOURCECODEPRO_BOLD, text_size=10.5),
)
text(
    (88.5, 10.8),
    "POST /v1/nodes -> 10.0.4.12:8080",
    style=Styles.PrimaryBold.patch(text_font=FontMonoSpace.ROBOTO_MONO_REGULAR, text_size=10.0),
)

save()
```

---

## `enum` FontBase

Abstract `StrEnum` base class inherited by all 12 built-in font enumerations in `drawlib.fonts` (also re-exported by [`drawlib.types`](05_styles_and_types.md)). Font archives are downloaded automatically on first render and cached locally (manageable via `drawlib cache list` and `drawlib cache download --all`).

```python
from drawlib.fonts import Font, FontBase
from drawlib.styles import Styles

assert isinstance(Font.SANSSERIF_REGULAR, FontBase)
label_style = Styles.Dark.patch(text_font=Font.SANSSERIF_BOLD, text_size=12.0)
```

| Property | Specification |
| :--- | :--- |
| **Inheritance** | `enum.StrEnum` (0 direct members; parent of `Font`, `FontSansSerif`, `FontSerif`, `FontMonoSpace`, `FontRoboto`, `FontSourceCode`, `FontJapanese`, `FontChinese`, `FontKorean`, `FontArabic`, `FontThai`, `FontBrahmic`). |
| **Usage** | Type annotation for `Style.text_font` (`FontBase \| FontFile \| None`) and `BaseStyles.patch_font()`. |

---

## `class` FontFile

Pydantic model loading an external TrueType (`.ttf`) or OpenType (`.otf`) font file from disk (`drawlib.fonts.FontFile`). Validates that `file` resolves to an existing readable file path at construction time.

```python
from drawlib.fonts import FontFile
from drawlib.styles import Styles
from drawlib.text import text

brand_font = FontFile("_assets/fonts/Inter-SemiBold.ttf")
text((60, 30), "Custom Brand Header", style=Styles.Dark.patch(text_font=brand_font, text_size=14.0))
```

| Parameter / Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `file` | `str \| Path` | *Required* | Path to an existing `.ttf` or `.otf` font file (raises validation error if missing). |

---

## `enum` Font

Default universal font enumeration (`drawlib.fonts.Font`, `6` members) backed by Noto Sans CJK and Noto Serif CJK. Supports Latin, Japanese (Kanji/Kana), Chinese, and Korean glyphs simultaneously; `Font.SANSSERIF_REGULAR` is Drawlib's default `text_font`.

```python
from drawlib.fonts import Font
from drawlib.styles import Styles

title_style = Styles.DarkBold.patch(text_font=Font.SANSSERIF_BOLD, text_size=13.0)
serif_style = Styles.Dark.patch(text_font=Font.SERIF_REGULAR, text_size=11.5)
```

| Enum Members (`Thin` / `Regular` / `Bold`) | Typeface Family | Asset Cache Package |
| :--- | :--- | :--- |
| `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | Noto Sans CJK JP (Universal Sans-Serif, default) | `font_cjk_japanese_noto_sans` |
| `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | Noto Serif CJK JP (Universal Serif) | `font_cjk_japanese_noto_serif` |

---

## `enum` FontSansSerif

Curated Western sans-serif display and UI font enumeration (`drawlib.fonts.FontSansSerif`, `15` members across 5 typefaces × 3 weights).

```python
from drawlib.fonts import FontSansSerif
from drawlib.styles import Styles

heading = Styles.DarkBold.patch(text_font=FontSansSerif.MONTSERRAT_BOLD, text_size=13.5)
```

| Typeface | Enum Members | Asset Cache Package |
| :--- | :--- | :--- |
| **Lato** | `LATO_THIN`, `LATO_REGULAR`, `LATO_BOLD` | `font_sans_lato` |
| **Montserrat** | `MONTSERRAT_THIN`, `MONTSERRAT_REGULAR`, `MONTSERRAT_BOLD` | `font_sans_monstserrat` |
| **Oswald** | `OSWALD_THIN`, `OSWALD_REGULAR`, `OSWALD_BOLD` | `font_sans_oswald` |
| **Poppins** | `POPPINS_THIN`, `POPPINS_REGULAR`, `POPPINS_BOLD` | `font_sans_poppins` |
| **Raleway** | `RALEWAYS_THIN`, `RALEWAYS_REGULAR`, `RALEWAYS_BOLD` | `font_sans_raleways` |

---

## `enum` FontSerif

Western editorial, slab, and typewriter serif font enumeration (`drawlib.fonts.FontSerif`, `10` members).

```python
from drawlib.fonts import FontSerif
from drawlib.styles import Styles

editorial = Styles.Dark.patch(text_font=FontSerif.MERRIWEATHER_REGULAR, text_size=11.5)
```

| Typeface | Enum Members | Asset Cache Package |
| :--- | :--- | :--- |
| **Courier** | `COURIER_REGULAR`, `COURIER_BOLD` | `font_mono_courier` |
| **Merriweather** | `MERRIWEATHER_THIN`, `MERRIWEATHER_REGULAR`, `MERRIWEATHER_BOLD` | `font_serif_merriweather` |
| **Platypi** | `PLATYPI_THIN`, `PLATYPI_REGULAR`, `PLATYPI_BOLD` | `font_serif_platypi` |
| **Playfair Display** | `PLAYFAIRDISPLAY_REGULAR`, `PLAYFAIRDISPLAY_BOLD` | `font_serif_playfairdisplay` |

---

## `enum` FontMonoSpace

Fixed-width monospace font enumeration (`drawlib.fonts.FontMonoSpace`, `11` members) ideal for IP addresses, CLI flags, HTTP routes, SQL types, and aligned metric labels.

```python
from drawlib.fonts import FontMonoSpace
from drawlib.styles import Styles

endpoint_style = Styles.PrimaryBold.patch(
    text_font=FontMonoSpace.SOURCECODEPRO_BOLD,
    text_size=11.0,
)
```

| Typeface | Enum Members | Asset Cache Package |
| :--- | :--- | :--- |
| **Roboto Mono** | `ROBOTO_MONO_THIN`, `ROBOTO_MONO_REGULAR`, `ROBOTO_MONO_BOLD` | `font_roboto_mono` |
| **Courier** | `COURIER_REGULAR`, `COURIER_BOLD` | `font_mono_courier` |
| **Source Code Pro** | `SOURCECODEPRO_THIN`, `SOURCECODEPRO_REGULAR`, `SOURCECODEPRO_BOLD` | `font_mono_source_code_pro` |
| **Source Han Code JP** | `SOURCEHANCODEJP_THIN`, `SOURCEHANCODEJP_REGULAR`, `SOURCEHANCODEJP_BOLD` (Japanese + Latin monospace) | `font_mono_source_han_code_jp` |

---

## `enum` FontRoboto

Complete Google Roboto superfamily enumeration (`drawlib.fonts.FontRoboto`, `18` member names including shorthand aliases `THIN`, `REGULAR`, `BOLD`).

```python
from drawlib.fonts import FontRoboto
from drawlib.preset_styles import GoogleStyles

Styles = GoogleStyles().patch_font(
    FontRoboto.ROBOTO_REGULAR,
    bold=FontRoboto.ROBOTO_BOLD,
    thin=FontRoboto.ROBOTO_THIN,
)
```

| Subfamily | Enum Members | Asset Cache Package |
| :--- | :--- | :--- |
| **Roboto Sans** | `ROBOTO_THIN`, `ROBOTO_REGULAR`, `ROBOTO_BOLD` (aliases: `THIN`, `REGULAR`, `BOLD`) | `font_roboto` |
| **Roboto Serif** | `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | `font_roboto_serif` |
| **Roboto Mono** | `MONO_THIN`, `MONO_REGULAR`, `MONO_BOLD` | `font_roboto_mono` |
| **Roboto Condensed** | `CONDENSED_THIN`, `CONDENSED_REGULAR`, `CONDENSED_BOLD` | `font_roboto_condensed` |
| **Roboto Slab** | `SLAB_THIN`, `SLAB_REGULAR`, `SLAB_BOLD` | `font_roboto_slab` |

---

## `enum` FontSourceCode

Multi-weight monospace font family selector (`drawlib.fonts.FontSourceCode`, `4` members) designed specifically for syntax-highlighted `SourceCode` SmartArt blocks and `BaseStyles.sourcecode_font` (automatically pairing regular/bold/italic faces during lexer token rendering).

```python
from drawlib.fonts import FontSourceCode
from drawlib.preset_styles import DefaultStyles

Styles = DefaultStyles().patch_font(sourcecode=FontSourceCode.SOURCEHANCODEJP)
```

| Member | Typeface | Best Suited For |
| :--- | :--- | :--- |
| `ROBOTO_MONO` | Roboto Mono | Modern geometric code snippets (`ASCII` / Latin). |
| `COURIER` | Courier | Classic typewriter / terminal listings. |
| `SOURCECODEPRO` | Adobe Source Code Pro | Default `BaseStyles.sourcecode_font` for high-legibility code cards. |
| `SOURCEHANCODEJP` | Adobe Source Han Code JP | Bilingual code blocks containing Japanese comments or strings. |

---

## `enum` FontJapanese

Dedicated Japanese typography enumeration (`drawlib.fonts.FontJapanese`, `14` members) spanning Gothic (sans-serif), Mincho (serif), and rounded UI families.

```python
from drawlib.fonts import FontJapanese
from drawlib.styles import Styles

ja_rounded = Styles.DarkBold.patch(text_font=FontJapanese.MPLUSROUNDED1C_BOLD, text_size=12.0)
```

| Typeface | Enum Members | Asset Cache Package |
| :--- | :--- | :--- |
| **Noto Sans JP** | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | `font_japanese_noto_sans` |
| **Noto Serif JP** | `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | `font_japanese_noto_serif` |
| **M PLUS 1p** | `MPLUS1P_THIN`, `MPLUS1P_REGULAR`, `MPLUS1P_BOLD` | `font_japanese_mplus_1p` |
| **M PLUS Rounded 1c** | `MPLUSROUNDED1C_THIN`, `MPLUSROUNDED1C_REGULAR`, `MPLUSROUNDED1C_BOLD` | `font_japanese_mplus_rounded1c` |
| **Sawarabi** | `SAWARABI_GOTHIC`, `SAWARABI_MINCHO` | `font_japanese_sawarabi_gothic` / `mincho` |

---

## `enum` FontChinese

Regional Chinese typography enumeration (`drawlib.fonts.FontChinese`, `18` members) supporting Simplified Chinese (`zh-CN`), Traditional Chinese (`zh-TW`), and Hong Kong (`zh-HK`) glyph standards in both Sans-Serif and Serif styles.

```python
from drawlib.fonts import FontChinese
from drawlib.styles import Styles

zh_sans = Styles.DarkBold.patch(text_font=FontChinese.SIMPLIFIED_SANSSERIF_BOLD, text_size=12.0)
```

| Script Standard | Enum Members | Asset Cache Packages |
| :--- | :--- | :--- |
| **Simplified (`SC`)** | `SIMPLIFIED_SANSSERIF_THIN`, `SIMPLIFIED_SANSSERIF_REGULAR`, `SIMPLIFIED_SANSSERIF_BOLD`, `SIMPLIFIED_SERIF_THIN`, `SIMPLIFIED_SERIF_REGULAR`, `SIMPLIFIED_SERIF_BOLD` | `font_chinese_simplified_noto_sans` / `serif` |
| **Traditional (`TC`)** | `TRADITIONAL_SANSSERIF_THIN`, `TRADITIONAL_SANSSERIF_REGULAR`, `TRADITIONAL_SANSSERIF_BOLD`, `TRADITIONAL_SERIF_THIN`, `TRADITIONAL_SERIF_REGULAR`, `TRADITIONAL_SERIF_BOLD` | `font_chinese_traditional_noto_sans` / `serif` |
| **Hong Kong (`HK`)** | `HONGKONG_SANSSERIF_THIN`, `HONGKONG_SANSSERIF_REGULAR`, `HONGKONG_SANSSERIF_BOLD`, `HONGKONG_SERIF_THIN`, `HONGKONG_SERIF_REGULAR`, `HONGKONG_SERIF_BOLD` | `font_chinese_hongkong_noto_sans` / `serif` |

---

## `enum` FontKorean

Korean Hangul and Hanja typography enumeration (`drawlib.fonts.FontKorean`, `6` members) backed by Noto Sans KR and Noto Serif KR.

```python
from drawlib.fonts import FontKorean
from drawlib.styles import Styles

ko_bold = Styles.DarkBold.patch(text_font=FontKorean.SANSSERIF_BOLD, text_size=12.0)
```

| Style | Enum Members | Asset Cache Package |
| :--- | :--- | :--- |
| **Sans-Serif** | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | `font_korean_noto_sans` |
| **Serif** | `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | `font_korean_noto_serif` |

---

## `enum` FontArabic

Arabic script typography enumeration (`drawlib.fonts.FontArabic`, `8` members) providing Sans, Kufi, and Naskh styles.

```python
from drawlib.fonts import FontArabic
from drawlib.styles import Styles

ar_kufi = Styles.DarkBold.patch(text_font=FontArabic.KUFI_BOLD, text_size=12.0)
```

| Style | Enum Members | Asset Cache Package |
| :--- | :--- | :--- |
| **Noto Sans Arabic** | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | `font_arabic_noto_sans` |
| **Noto Kufi Arabic** | `KUFI_THIN`, `KUFI_REGULAR`, `KUFI_BOLD` | `font_arabic_noto_kufi` |
| **Noto Naskh Arabic** | `NASKH_REGULAR`, `NASKH_BOLD` | `font_arabic_noto_naskh` |

---

## `enum` FontThai

Thai script typography enumeration (`drawlib.fonts.FontThai`, `6` members) backed by Noto Sans Thai and Noto Serif Thai.

```python
from drawlib.fonts import FontThai
from drawlib.styles import Styles

th_sans = Styles.Dark.patch(text_font=FontThai.SANSSERIF_REGULAR, text_size=12.0)
```

| Style | Enum Members | Asset Cache Package |
| :--- | :--- | :--- |
| **Sans-Serif** | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | `font_thai_noto_sans` |
| **Serif** | `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | `font_thai_noto_serif` |

---

## `enum` FontBrahmic

South Asian Brahmic-family script enumeration (`drawlib.fonts.FontBrahmic`, `24` members) covering Bengali, Devanagari, Tamil, and Telugu in Sans-Serif and Serif styles.

```python
from drawlib.fonts import FontBrahmic
from drawlib.styles import Styles

hi_bold = Styles.DarkBold.patch(text_font=FontBrahmic.DEVANAGARI_SANSSERIF_BOLD, text_size=12.0)
```

| Script | Enum Members | Asset Cache Packages |
| :--- | :--- | :--- |
| **Bengali** | `BENGALI_SANSSERIF_THIN`, `BENGALI_SANSSERIF_REGULAR`, `BENGALI_SANSSERIF_BOLD`, `BENGALI_SERIF_THIN`, `BENGALI_SERIF_REGULAR`, `BENGALI_SERIF_BOLD` | `font_brahmic_bengali_noto_sans` / `serif` |
| **Devanagari** | `DEVANAGARI_SANSSERIF_THIN`, `DEVANAGARI_SANSSERIF_REGULAR`, `DEVANAGARI_SANSSERIF_BOLD`, `DEVANAGARI_SERIF_THIN`, `DEVANAGARI_SERIF_REGULAR`, `DEVANAGARI_SERIF_BOLD` | `font_brahmic_devanagari_noto_sans` / `serif` |
| **Tamil** | `TAMIL_SANSSERIF_THIN`, `TAMIL_SANSSERIF_REGULAR`, `TAMIL_SANSSERIF_BOLD`, `TAMIL_SERIF_THIN`, `TAMIL_SERIF_REGULAR`, `TAMIL_SERIF_BOLD` | `font_brahmic_tamil_noto_sans` / `serif` |
| **Telugu** | `TELUGU_SANSSERIF_THIN`, `TELUGU_SANSSERIF_REGULAR`, `TELUGU_SANSSERIF_BOLD`, `TELUGU_SERIF_THIN`, `TELUGU_SERIF_REGULAR`, `TELUGU_SERIF_BOLD` | `font_brahmic_telugu_noto_sans` / `serif` |
