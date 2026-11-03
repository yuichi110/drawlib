# drawlib.fonts（タイポグラフィと多言語フォント）

多言語・技術図解向けフォント列挙体（`Font`, `FontSansSerif`, `FontSerif`, `FontMonoSpace`, `FontRoboto`, `FontSourceCode`、および地域言語スクリプト群）と外部フォントファイルローダー（`FontFile`）を提供します。`from drawlib.fonts import Font, FontFile, FontMonoSpace, FontRoboto, FontSansSerif, FontSerif` をインポートし、`Style.text_font` や `BaseStyles.patch_font()` に指定して使用します。

```drawlib align=center code=fold file=07_fonts_hero.png caption="drawlib.fonts の主要フォントファミリ — 多言語 CJK・欧文サンセリフ・セリフ・技術等幅フォント"
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

`drawlib.fonts` 内の全 12 種類の組み込みフォント列挙体が継承する抽象 `StrEnum` 基底クラスです（[`drawlib.types`](05_styles_and_types.md) からも再エクスポート）。フォントバイナリは初回描画時にオンデマンドで取得・ローカルキャッシュされ、`drawlib cache list` や `drawlib cache download --all` で管理できます。

```python
from drawlib.fonts import Font, FontBase
from drawlib.styles import Styles

assert isinstance(Font.SANSSERIF_REGULAR, FontBase)
label_style = Styles.Dark.patch(text_font=Font.SANSSERIF_BOLD, text_size=12.0)
```

| 項目 | 仕様 |
| :--- | :--- |
| **継承関係** | `enum.StrEnum`（直接の列挙メンバなし。`Font`, `FontSansSerif`, `FontSerif`, `FontMonoSpace`, `FontRoboto`, `FontSourceCode`, `FontJapanese`, `FontChinese`, `FontKorean`, `FontArabic`, `FontThai`, `FontBrahmic` の親クラス）。 |
| **主な用途** | `Style.text_font`（`FontBase \| FontFile \| None`）および `BaseStyles.patch_font()` の共通型指定。 |

---

## `class` FontFile

ローカルファイルシステム上の TrueType（`.ttf`）または OpenType（`.otf`）フォントファイルを読み込む Pydantic モデル（`drawlib.fonts.FontFile`）です。インスタンス生成時にファイルの存在確認バリデーションが行われます。

```python
from drawlib.fonts import FontFile
from drawlib.styles import Styles
from drawlib.text import text

brand_font = FontFile("_assets/fonts/Inter-SemiBold.ttf")
text((60, 30), "Custom Brand Header", style=Styles.Dark.patch(text_font=brand_font, text_size=14.0))
```

| 引数 / 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `file` | `str \| Path` | *必須* | 実在する `.ttf` または `.otf` フォントファイルへのパス（未存在時はバリデーションエラー）。 |

---

## `enum` Font

Noto Sans CJK / Noto Serif CJK をベースとする標準ユニバーサルフォント列挙体（`drawlib.fonts.Font`、全 `6` メンバ）です。欧文（ラテン文字）・日本語（漢字・かな）・中国語・韓国語を単一フォントで同時に描画でき、`Font.SANSSERIF_REGULAR` が Drawlib 全体の既定フォントとして使用されます。

```python
from drawlib.fonts import Font
from drawlib.styles import Styles

title_style = Styles.DarkBold.patch(text_font=Font.SANSSERIF_BOLD, text_size=13.0)
serif_style = Styles.Dark.patch(text_font=Font.SERIF_REGULAR, text_size=11.5)
```

| 列挙メンバ（`Thin` / `Regular` / `Bold`） | 書体ファミリ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | Noto Sans CJK JP（標準ゴシック・既定） | `font_cjk_japanese_noto_sans` |
| `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | Noto Serif CJK JP（明朝・セリフ） | `font_cjk_japanese_noto_serif` |

---

## `enum` FontSansSerif

欧文プレゼンテーション・UI デザイン向けのサンセリフ体フォント列挙体（`drawlib.fonts.FontSansSerif`、5 書体 × 3 ウェイト＝全 `15` メンバ）です。

```python
from drawlib.fonts import FontSansSerif
from drawlib.styles import Styles

heading = Styles.DarkBold.patch(text_font=FontSansSerif.MONTSERRAT_BOLD, text_size=13.5)
```

| 書体名 | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **Lato** | `LATO_THIN`, `LATO_REGULAR`, `LATO_BOLD` | `font_sans_lato` |
| **Montserrat** | `MONTSERRAT_THIN`, `MONTSERRAT_REGULAR`, `MONTSERRAT_BOLD` | `font_sans_monstserrat` |
| **Oswald** | `OSWALD_THIN`, `OSWALD_REGULAR`, `OSWALD_BOLD` | `font_sans_oswald` |
| **Poppins** | `POPPINS_THIN`, `POPPINS_REGULAR`, `POPPINS_BOLD` | `font_sans_poppins` |
| **Raleway** | `RALEWAYS_THIN`, `RALEWAYS_REGULAR`, `RALEWAYS_BOLD` | `font_sans_raleways` |

---

## `enum` FontSerif

ホワイトペーパー・報告書・出版物向けの欧文セリフ体フォント列挙体（`drawlib.fonts.FontSerif`、全 `10` メンバ）です。

```python
from drawlib.fonts import FontSerif
from drawlib.styles import Styles

editorial = Styles.Dark.patch(text_font=FontSerif.MERRIWEATHER_REGULAR, text_size=11.5)
```

| 書体名 | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **Courier** | `COURIER_REGULAR`, `COURIER_BOLD` | `font_mono_courier` |
| **Merriweather** | `MERRIWEATHER_THIN`, `MERRIWEATHER_REGULAR`, `MERRIWEATHER_BOLD` | `font_serif_merriweather` |
| **Platypi** | `PLATYPI_THIN`, `PLATYPI_REGULAR`, `PLATYPI_BOLD` | `font_serif_platypi` |
| **Playfair Display** | `PLAYFAIRDISPLAY_REGULAR`, `PLAYFAIRDISPLAY_BOLD` | `font_serif_playfairdisplay` |

---

## `enum` FontMonoSpace

IP アドレス・ポート番号・CLI オプション・REST エンドポイント・型定義などの技術表記に適した等幅フォント列挙体（`drawlib.fonts.FontMonoSpace`、全 `11` メンバ）です。

```python
from drawlib.fonts import FontMonoSpace
from drawlib.styles import Styles

endpoint_style = Styles.PrimaryBold.patch(
    text_font=FontMonoSpace.SOURCECODEPRO_BOLD,
    text_size=11.0,
)
```

| 書体名 | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **Roboto Mono** | `ROBOTO_MONO_THIN`, `ROBOTO_MONO_REGULAR`, `ROBOTO_MONO_BOLD` | `font_roboto_mono` |
| **Courier** | `COURIER_REGULAR`, `COURIER_BOLD` | `font_mono_courier` |
| **Source Code Pro** | `SOURCECODEPRO_THIN`, `SOURCECODEPRO_REGULAR`, `SOURCECODEPRO_BOLD` | `font_mono_source_code_pro` |
| **Source Han Code JP** | `SOURCEHANCODEJP_THIN`, `SOURCEHANCODEJP_REGULAR`, `SOURCEHANCODEJP_BOLD`（日本語対応等幅フォント） | `font_mono_source_han_code_jp` |

---

## `enum` FontRoboto

Google Roboto スーパーファミリ全体を網羅するフォント列挙体（`drawlib.fonts.FontRoboto`、短縮エイリアス `THIN`, `REGULAR`, `BOLD` を含む全 `18` メンバ名）です。

```python
from drawlib.fonts import FontRoboto
from drawlib.preset_styles import GoogleStyles

Styles = GoogleStyles().patch_font(
    FontRoboto.ROBOTO_REGULAR,
    bold=FontRoboto.ROBOTO_BOLD,
    thin=FontRoboto.ROBOTO_THIN,
)
```

| サブファミリ | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **Roboto Sans** | `ROBOTO_THIN`, `ROBOTO_REGULAR`, `ROBOTO_BOLD`（エイリアス: `THIN`, `REGULAR`, `BOLD`） | `font_roboto` |
| **Roboto Serif** | `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | `font_roboto_serif` |
| **Roboto Mono** | `MONO_THIN`, `MONO_REGULAR`, `MONO_BOLD` | `font_roboto_mono` |
| **Roboto Condensed** | `CONDENSED_THIN`, `CONDENSED_REGULAR`, `CONDENSED_BOLD` | `font_roboto_condensed` |
| **Roboto Slab** | `SLAB_THIN`, `SLAB_REGULAR`, `SLAB_BOLD` | `font_roboto_slab` |

---

## `enum` FontSourceCode

`SourceCode` SmartArt コンポーネントおよび `BaseStyles.sourcecode_font` 専用のソースコード用等幅フォントセレクタ列挙体（`drawlib.fonts.FontSourceCode`、全 `4` メンバ）です。シンタックスハイライト描画時に通常・太字・斜体ウェイトを自動解決します。

```python
from drawlib.fonts import FontSourceCode
from drawlib.preset_styles import DefaultStyles

Styles = DefaultStyles().patch_font(sourcecode=FontSourceCode.SOURCEHANCODEJP)
```

| 列挙メンバ | 書体 | 主な用途 |
| :--- | :--- | :--- |
| `ROBOTO_MONO` | Roboto Mono | モダンな欧文ソースコードスニペット。 |
| `COURIER` | Courier | クラシカルなターミナル出力やタイプライター表現。 |
| `SOURCECODEPRO` | Adobe Source Code Pro | `BaseStyles.sourcecode_font` の既定値（高い視認性のコードカード）。 |
| `SOURCEHANCODEJP` | Adobe 源ノ角ゴシック Code JP | 日本語コメントや日本語文字列を含むソースコード描画。 |

---

## `enum` FontJapanese

日本語ドキュメント・スライド向けの専用書体列挙体（`drawlib.fonts.FontJapanese`、全 `14` メンバ）です。角ゴシック・明朝・丸ゴシックの各書体を収録しています。

```python
from drawlib.fonts import FontJapanese
from drawlib.styles import Styles

ja_rounded = Styles.DarkBold.patch(text_font=FontJapanese.MPLUSROUNDED1C_BOLD, text_size=12.0)
```

| 書体名 | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **Noto Sans JP** | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | `font_japanese_noto_sans` |
| **Noto Serif JP** | `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | `font_japanese_noto_serif` |
| **M PLUS 1p** | `MPLUS1P_THIN`, `MPLUS1P_REGULAR`, `MPLUS1P_BOLD` | `font_japanese_mplus_1p` |
| **M PLUS Rounded 1c** | `MPLUSROUNDED1C_THIN`, `MPLUSROUNDED1C_REGULAR`, `MPLUSROUNDED1C_BOLD` | `font_japanese_mplus_rounded1c` |
| **さわらび書体** | `SAWARABI_GOTHIC`, `SAWARABI_MINCHO` | `font_japanese_sawarabi_gothic` / `mincho` |

---

## `enum` FontChinese

簡体字（`SC`）・繁体字台湾（`TC`）・香港字形（`HK`）のサンセリフ体およびセリフ体を網羅する中国語フォント列挙体（`drawlib.fonts.FontChinese`、全 `18` メンバ）です。

```python
from drawlib.fonts import FontChinese
from drawlib.styles import Styles

zh_sans = Styles.DarkBold.patch(text_font=FontChinese.SIMPLIFIED_SANSSERIF_BOLD, text_size=12.0)
```

| 字形規格 | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **簡体字（`SC`）** | `SIMPLIFIED_SANSSERIF_THIN`, `SIMPLIFIED_SANSSERIF_REGULAR`, `SIMPLIFIED_SANSSERIF_BOLD`, `SIMPLIFIED_SERIF_THIN`, `SIMPLIFIED_SERIF_REGULAR`, `SIMPLIFIED_SERIF_BOLD` | `font_chinese_simplified_noto_sans` / `serif` |
| **繁体字（`TC`）** | `TRADITIONAL_SANSSERIF_THIN`, `TRADITIONAL_SANSSERIF_REGULAR`, `TRADITIONAL_SANSSERIF_BOLD`, `TRADITIONAL_SERIF_THIN`, `TRADITIONAL_SERIF_REGULAR`, `TRADITIONAL_SERIF_BOLD` | `font_chinese_traditional_noto_sans` / `serif` |
| **香港繁体字（`HK`）** | `HONGKONG_SANSSERIF_THIN`, `HONGKONG_SANSSERIF_REGULAR`, `HONGKONG_SANSSERIF_BOLD`, `HONGKONG_SERIF_THIN`, `HONGKONG_SERIF_REGULAR`, `HONGKONG_SERIF_BOLD` | `font_chinese_hongkong_noto_sans` / `serif` |

---

## `enum` FontKorean

Noto Sans KR および Noto Serif KR をベースとする韓国語（ハングル・漢字）フォント列挙体（`drawlib.fonts.FontKorean`、全 `6` メンバ）です。

```python
from drawlib.fonts import FontKorean
from drawlib.styles import Styles

ko_bold = Styles.DarkBold.patch(text_font=FontKorean.SANSSERIF_BOLD, text_size=12.0)
```

| スタイル | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **サンセリフ（ゴシック）** | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | `font_korean_noto_sans` |
| **セリフ（明朝）** | `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | `font_korean_noto_serif` |

---

## `enum` FontArabic

Sans・Kufi・Naskh の 3 書体を収録したアラビア文字フォント列挙体（`drawlib.fonts.FontArabic`、全 `8` メンバ）です。

```python
from drawlib.fonts import FontArabic
from drawlib.styles import Styles

ar_kufi = Styles.DarkBold.patch(text_font=FontArabic.KUFI_BOLD, text_size=12.0)
```

| 書体名 | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **Noto Sans Arabic** | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | `font_arabic_noto_sans` |
| **Noto Kufi Arabic** | `KUFI_THIN`, `KUFI_REGULAR`, `KUFI_BOLD` | `font_arabic_noto_kufi` |
| **Noto Naskh Arabic** | `NASKH_REGULAR`, `NASKH_BOLD` | `font_arabic_noto_naskh` |

---

## `enum` FontThai

Noto Sans Thai および Noto Serif Thai をベースとするタイ文字フォント列挙体（`drawlib.fonts.FontThai`、全 `6` メンバ）です。

```python
from drawlib.fonts import FontThai
from drawlib.styles import Styles

th_sans = Styles.Dark.patch(text_font=FontThai.SANSSERIF_REGULAR, text_size=12.0)
```

| スタイル | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **サンセリフ** | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD` | `font_thai_noto_sans` |
| **セリフ** | `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | `font_thai_noto_serif` |

---

## `enum` FontBrahmic

ベンガル文字・デーヴァナーガリー文字・タミル文字・テルグ文字の 4 言語 × サンセリフ／セリフ体を収録するブラーフミー系インド諸言語フォント列挙体（`drawlib.fonts.FontBrahmic`、全 `24` メンバ）です。

```python
from drawlib.fonts import FontBrahmic
from drawlib.styles import Styles

hi_bold = Styles.DarkBold.patch(text_font=FontBrahmic.DEVANAGARI_SANSSERIF_BOLD, text_size=12.0)
```

| 文字体系 | 列挙メンバ | キャッシュパッケージ名 |
| :--- | :--- | :--- |
| **ベンガル文字** | `BENGALI_SANSSERIF_THIN`, `BENGALI_SANSSERIF_REGULAR`, `BENGALI_SANSSERIF_BOLD`, `BENGALI_SERIF_THIN`, `BENGALI_SERIF_REGULAR`, `BENGALI_SERIF_BOLD` | `font_brahmic_bengali_noto_sans` / `serif` |
| **デーヴァナーガリー** | `DEVANAGARI_SANSSERIF_THIN`, `DEVANAGARI_SANSSERIF_REGULAR`, `DEVANAGARI_SANSSERIF_BOLD`, `DEVANAGARI_SERIF_THIN`, `DEVANAGARI_SERIF_REGULAR`, `DEVANAGARI_SERIF_BOLD` | `font_brahmic_devanagari_noto_sans` / `serif` |
| **タミル文字** | `TAMIL_SANSSERIF_THIN`, `TAMIL_SANSSERIF_REGULAR`, `TAMIL_SANSSERIF_BOLD`, `TAMIL_SERIF_THIN`, `TAMIL_SERIF_REGULAR`, `TAMIL_SERIF_BOLD` | `font_brahmic_tamil_noto_sans` / `serif` |
| **テルグ文字** | `TELUGU_SANSSERIF_THIN`, `TELUGU_SANSSERIF_REGULAR`, `TELUGU_SANSSERIF_BOLD`, `TELUGU_SERIF_THIN`, `TELUGU_SERIF_REGULAR`, `TELUGU_SERIF_BOLD` | `font_brahmic_telugu_noto_sans` / `serif` |
