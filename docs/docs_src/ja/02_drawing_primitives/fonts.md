# フォントと多言語カタログ

Drawlib はホスト OS のシステムフォントに依存しません。OS 付属フォントは Linux・macOS・Windows 間で異なることが多く、CI 環境での文字切れやレイアウト崩れの原因となるためです。
その代わりに、`drawlib.fonts` はオープンソースの Google Noto、Roboto、M PLUS、および Adobe Source ファミリーをベースとする **14 個の厳選フォントクラス**を提供しており、必要に応じてオンデマンドでダウンロード・ローカルキャッシュすることで、環境に依存しない決定論的なクロスプラットフォーム描画を実現します。

---

## 1. 組み込みタイポグラフィの概要

```drawlib code=fold align=center file=fonts_overview.png caption="Drawlib のクロスプラットフォーム欧文・等幅・CJK フォントファミリー"
from drawlib.canvas import save, setup
from drawlib.fonts import (
    FontJapanese,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
)
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=56)

# Left card: Western & Monospace specimen
rectangle((34, 28), width=58, height=46, style=Styles.Neutral.patch(shape_r=2))
text((34, 43), "Roboto Bold (UI & Titles)", style=Styles.DarkBold.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=12.0))
text((34, 33), "Montserrat Regular (Geometric)", style=Styles.Dark.patch(text_font=FontSansSerif.MONTSERRAT_REGULAR, text_size=11.0))
text((34, 23), "Merriweather Serif (Editorial)", style=Styles.Dark.patch(text_font=FontSerif.MERRIWEATHER_REGULAR, text_size=11.0))
text((34, 13), "SELECT * FROM nodes;", style=Styles.Dark.patch(text_font=FontMonoSpace.SOURCECODEPRO_BOLD, text_size=11.0))

# Right card: Multilingual CJK specimen
rectangle((96, 28), width=56, height=46, style=Styles.PrimaryNeutral.patch(shape_r=2))
text((96, 42), "Noto Sans JP (日本語標準)", style=Styles.DarkBold.patch(text_font=FontJapanese.SANSSERIF_BOLD, text_size=12.0))
text((96, 30), "M PLUS Rounded (丸ゴシック)", style=Styles.Dark.patch(text_font=FontJapanese.MPLUSROUNDED1C_BOLD, text_size=12.0))
text((96, 18), "Sawarabi Mincho (明朝体)", style=Styles.Dark.patch(text_font=FontJapanese.SAWARABI_MINCHO, text_size=12.0))

save()
```

---

## 2. `drawlib.fonts` の全 14 クラス一覧

すべてのフォントクラスは `drawlib.fonts` から直接インポートします。

```python
from drawlib.fonts import (
    # 1. Universal Default, Custom File Loader & Base Class
    Font,
    FontFile,
    FontBase,
    # 2. Western & Code Typography
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontMonoSpace,
    FontSourceCode,
    # 3. CJK & International Scripts
    FontJapanese,
    FontChinese,
    FontKorean,
    FontArabic,
    FontThai,
    FontBrahmic,
)
```

### 2.1. システム・標準・カスタムフォントクラス（3 クラス）

| クラス | カテゴリ | メンバー／シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| **`Font`** | 標準デフォルト | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD`, `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` | 初期設定のまま欧文および東アジア文字（CJK）を幅広くカバーする標準のクロスプラットフォームフォントファミリー（Noto Sans / Noto Serif CJK）。 |
| **`FontFile`** | カスタムフォントローダー | `FontFile(file="path/to/font.ttf")` | 外部の `.ttf`、`.otf`、`.woff`、`.woff2` コーポレートフォントファイルを読み込みます（呼び出し元スクリプトからの相対パスで解決）。`_assets/avenger/regular.ttf` を用いた実践例は [カスタムフォントファイル (`FontFile`)](./font_file.md) を参照してください。 |
| **`FontBase`** | 抽象基底列挙型 | `class FontBase(str, Enum)` | 型チェックやスタイル検証のためにすべての組み込みフォント列挙型が継承する基底クラス。 |

### 2.2. 欧文・コードタイポグラフィクラス（5 クラス）

| クラス | 書体ファミリー | 利用可能なウェイト／スタイルバリアント |
| :--- | :--- | :--- |
| **`FontRoboto`** | Roboto, Roboto Serif, Roboto Mono, Roboto Condensed, Roboto Slab | `ROBOTO_THIN`, `ROBOTO_REGULAR`, `ROBOTO_BOLD`（エイリアス: `THIN`, `REGULAR`, `BOLD`）, `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD`, `MONO_THIN`, `MONO_REGULAR`, `MONO_BOLD`, `CONDENSED_THIN`, `CONDENSED_REGULAR`, `CONDENSED_BOLD`, `SLAB_THIN`, `SLAB_REGULAR`, `SLAB_BOLD` |
| **`FontSansSerif`** | Lato, Montserrat, Oswald, Poppins, Raleway | `LATO_THIN`, `LATO_REGULAR`, `LATO_BOLD`, `MONTSERRAT_THIN`, `MONTSERRAT_REGULAR`, `MONTSERRAT_BOLD`, `OSWALD_THIN`, `OSWALD_REGULAR`, `OSWALD_BOLD`, `POPPINS_THIN`, `POPPINS_REGULAR`, `POPPINS_BOLD`, `RALEWAYS_THIN`, `RALEWAYS_REGULAR`, `RALEWAYS_BOLD` |
| **`FontSerif`** | Courier, Merriweather, Platypi, Playfair Display | `COURIER_REGULAR`, `COURIER_BOLD`, `MERRIWEATHER_THIN`, `MERRIWEATHER_REGULAR`, `MERRIWEATHER_BOLD`, `PLATYPI_THIN`, `PLATYPI_REGULAR`, `PLATYPI_BOLD`, `PLAYFAIRDISPLAY_REGULAR`, `PLAYFAIRDISPLAY_BOLD` |
| **`FontMonoSpace`** | Roboto Mono, Courier, Source Code Pro, Source Han Code JP | `ROBOTO_MONO_THIN`, `ROBOTO_MONO_REGULAR`, `ROBOTO_MONO_BOLD`, `COURIER_REGULAR`, `COURIER_BOLD`, `SOURCECODEPRO_THIN`, `SOURCECODEPRO_REGULAR`, `SOURCECODEPRO_BOLD`, `SOURCEHANCODEJP_THIN`, `SOURCEHANCODEJP_REGULAR`, `SOURCEHANCODEJP_BOLD` |
| **`FontSourceCode`** | ソースコードブロック用 | `ROBOTO_MONO`, `COURIER`, `SOURCECODEPRO`, `SOURCEHANCODEJP`（`Styles.sourcecode_font` および `SourceCode` SmartArt で使用） |

### 2.3. CJK・多言語スクリプトクラス（6 クラス）

| クラス | 文字体系／地域 | 利用可能なウェイト／スタイルバリアント |
| :--- | :--- | :--- |
| **`FontJapanese`** | 日本語（漢字・ひらがな・カタカナ） | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD`, `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD`, `MPLUS1P_THIN`, `MPLUS1P_REGULAR`, `MPLUS1P_BOLD`, `MPLUSROUNDED1C_THIN`, `MPLUSROUNDED1C_REGULAR`, `MPLUSROUNDED1C_BOLD`, `SAWARABI_GOTHIC`, `SAWARABI_MINCHO` |
| **`FontChinese`** | 簡体字（SC）・繁体字（TC）・香港（HK） | `SIMPLIFIED_SANSSERIF_THIN`, `SIMPLIFIED_SANSSERIF_REGULAR`, `SIMPLIFIED_SANSSERIF_BOLD`, `SIMPLIFIED_SERIF_THIN`, `SIMPLIFIED_SERIF_REGULAR`, `SIMPLIFIED_SERIF_BOLD`, `TRADITIONAL_SANSSERIF_THIN`, `TRADITIONAL_SANSSERIF_REGULAR`, `TRADITIONAL_SANSSERIF_BOLD`, `TRADITIONAL_SERIF_THIN`, `TRADITIONAL_SERIF_REGULAR`, `TRADITIONAL_SERIF_BOLD`, `HONGKONG_SANSSERIF_THIN`, `HONGKONG_SANSSERIF_REGULAR`, `HONGKONG_SANSSERIF_BOLD`, `HONGKONG_SERIF_THIN`, `HONGKONG_SERIF_REGULAR`, `HONGKONG_SERIF_BOLD` |
| **`FontKorean`** | 韓国語（ハングル） | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD`, `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` |
| **`FontArabic`** | アラビア語（Sans, Kufi, Naskh） | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD`, `KUFI_THIN`, `KUFI_REGULAR`, `KUFI_BOLD`, `NASKH_REGULAR`, `NASKH_BOLD` |
| **`FontThai`** | タイ語 | `SANSSERIF_THIN`, `SANSSERIF_REGULAR`, `SANSSERIF_BOLD`, `SERIF_THIN`, `SERIF_REGULAR`, `SERIF_BOLD` |
| **`FontBrahmic`** | ベンガル文字・デーヴァナーガリー・タミル文字・テルグ文字 | `BENGALI_SANSSERIF_THIN`/`REGULAR`/`BOLD`, `BENGALI_SERIF_THIN`/`REGULAR`/`BOLD`, `DEVANAGARI_SANSSERIF_THIN`/`REGULAR`/`BOLD`, `DEVANAGARI_SERIF_THIN`/`REGULAR`/`BOLD`, `TAMIL_SANSSERIF_THIN`/`REGULAR`/`BOLD`, `TAMIL_SERIF_THIN`/`REGULAR`/`BOLD`, `TELUGU_SANSSERIF_THIN`/`REGULAR`/`BOLD`, `TELUGU_SERIF_THIN`/`REGULAR`/`BOLD` |

---

## 3. 書体見本: 欧文・等幅タイポグラフィ

個別のラベルやカードに特定のフォントファミリーやウェイト（`THIN`、`REGULAR`、`BOLD`）を適用するには、`style.patch(text_font=...)` を使用します。

```drawlib code=show align=center file=fonts_western_specimen.png caption="欧文サンセリフ・セリフ・等幅フォントの書体見本カタログ"
from drawlib.canvas import save, setup
from drawlib.fonts import (
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
)
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=70)

# Column 1: FontRoboto & FontSansSerif
rectangle((34, 35), width=58, height=60, style=Styles.Neutral.patch(shape_r=2))
text((34, 58), "Sans-Serif & Roboto", style=Styles.DarkBold.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=12.5))

specimens_left = [
    (47, FontRoboto.ROBOTO_THIN, "FontRoboto.ROBOTO_THIN"),
    (38, FontRoboto.ROBOTO_REGULAR, "FontRoboto.ROBOTO_REGULAR"),
    (29, FontRoboto.ROBOTO_BOLD, "FontRoboto.ROBOTO_BOLD"),
    (20, FontSansSerif.POPPINS_REGULAR, "FontSansSerif.POPPINS_REGULAR"),
    (11, FontSansSerif.OSWALD_BOLD, "FontSansSerif.OSWALD_BOLD"),
]
for y, font_enum, label in specimens_left:
    text((9, y), label, style=Styles.Dark.patch(text_font=font_enum, text_size=10.5, halign="left"))

# Column 2: FontSerif & FontMonoSpace
rectangle((98, 35), width=58, height=60, style=Styles.SecondaryNeutral.patch(shape_r=2))
text((98, 58), "Serif & Monospace", style=Styles.DarkBold.patch(text_font=FontSerif.MERRIWEATHER_BOLD, text_size=12.5))

specimens_right = [
    (47, FontSerif.MERRIWEATHER_REGULAR, "FontSerif.MERRIWEATHER"),
    (38, FontSerif.PLATYPI_BOLD, "FontSerif.PLATYPI_BOLD"),
    (29, FontRoboto.SLAB_BOLD, "FontRoboto.SLAB_BOLD"),
    (20, FontMonoSpace.ROBOTO_MONO_REGULAR, "ROBOTO_MONO: 10.0.0.1:443"),
    (11, FontMonoSpace.SOURCECODEPRO_BOLD, "SOURCECODEPRO: git commit"),
]
for y, font_enum, label in specimens_right:
    text((73, y), label, style=Styles.Dark.patch(text_font=font_enum, text_size=10.5, halign="left"))

save()
```

---

## 4. 書体見本: CJK・多言語タイポグラフィ

Drawlib は、日本語（`FontJapanese`）・中国語（`FontChinese`）・韓国語（`FontKorean`）をはじめ、`FontArabic`・`FontThai`・`FontBrahmic` といった地域別の専用フォントクラスを備えています。

```drawlib code=show align=center file=fonts_cjk_specimen.png caption="多言語 CJK タイポグラフィ見本（日本語・中国語・韓国語）"
from drawlib.canvas import save, setup
from drawlib.fonts import FontChinese, FontJapanese, FontKorean
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=130, height=58)

# 1. Japanese Fonts (FontJapanese)
rectangle((24, 29), width=38, height=46, style=Styles.PrimaryNeutral.patch(shape_r=2))
text((24, 45), "FontJapanese", style=Styles.DarkBold.patch(text_size=11.5))
text((24, 34), "標準ゴシック (Sans)", style=Styles.Dark.patch(text_font=FontJapanese.SANSSERIF_REGULAR, text_size=10.5))
text((24, 24), "明朝体 (Serif)", style=Styles.Dark.patch(text_font=FontJapanese.SERIF_BOLD, text_size=10.5))
text((24, 14), "丸ゴシック (Rounded)", style=Styles.Dark.patch(text_font=FontJapanese.MPLUSROUNDED1C_BOLD, text_size=10.5))

# 2. Chinese Fonts (FontChinese)
rectangle((65, 29), width=38, height=46, style=Styles.Neutral.patch(shape_r=2))
text((65, 45), "FontChinese", style=Styles.DarkBold.patch(text_size=11.5))
text((65, 34), "简体中文无衬线", style=Styles.Dark.patch(text_font=FontChinese.SIMPLIFIED_SANSSERIF_REGULAR, text_size=10.5))
text((65, 24), "简体中文衬线体", style=Styles.Dark.patch(text_font=FontChinese.SIMPLIFIED_SERIF_BOLD, text_size=10.5))
text((65, 14), "繁體中文設計規範", style=Styles.Dark.patch(text_font=FontChinese.TRADITIONAL_SANSSERIF_BOLD, text_size=10.5))

# 3. Korean Fonts (FontKorean)
rectangle((106, 29), width=38, height=46, style=Styles.SecondaryNeutral.patch(shape_r=2))
text((106, 45), "FontKorean", style=Styles.DarkBold.patch(text_size=11.5))
text((106, 34), "클라우드 아키텍처", style=Styles.Dark.patch(text_font=FontKorean.SANSSERIF_REGULAR, text_size=10.5))
text((106, 24), "시스템 설계 문서", style=Styles.Dark.patch(text_font=FontKorean.SANSSERIF_BOLD, text_size=10.5))
text((106, 14), "명조체 타이포그래피", style=Styles.Dark.patch(text_font=FontKorean.SERIF_BOLD, text_size=10.5))

save()
```

---

## 5. プロジェクト全体のフォント一括設定とアセットキャッシュ

### 5.1. プロジェクト全体のフォント切り替え (`Styles.patch_font()`)

描画呼び出しごとに `text_font` や `text_size` を個別にパッチする代わりに、プロジェクトの `styles.py` で `Styles.patch_font()` を呼び出すことで、すべてのプリセットトークンに対して標準（regular）・太字（bold）・細字（thin）・ソースコード用フォントおよび基準フォントサイズを一括更新できます。

```python
Styles.patch_font(
    regular: FontBase | FontFile | None = None,
    *,
    bold: FontBase | FontFile | None = None,
    thin: FontBase | FontFile | None = None,
    sourcecode: FontSourceCode | None = None,
    size: float | None = None,
) -> Self
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `regular` | `FontBase \| FontFile \| None` | `None` | 標準スタイルバリアントに適用されるベースラインフォント。`bold` または `thin` が省略された場合はそれらのフォールバックとしても使われます。 |
| `bold` | `FontBase \| FontFile \| None` | `None` | `Bold` および `*Bold` スタイルバリアントに適用されるキーワード専用フォント指定。 |
| `thin` | `FontBase \| FontFile \| None` | `None` | `Thin` および `*Thin` スタイルバリアントに適用されるキーワード専用フォント指定。 |
| `sourcecode` | `FontSourceCode \| None` | `None` | `Styles.sourcecode_font` に割り当てられるキーワード専用の等幅フォント指定。 |
| `size` | `float \| None` | `None` | カタログ内の全 `Style` トークンに一括適用されるポイント単位のフォントサイズ（`text_size`）上書き指定。 |

```python
# styles.py
from drawlib.fonts import FontJapanese, FontSourceCode
from drawlib.styles import Styles

Styles = Styles.patch_font(
    regular=FontJapanese.SANSSERIF_REGULAR,
    bold=FontJapanese.SANSSERIF_BOLD,
    thin=FontJapanese.SANSSERIF_THIN,
    sourcecode=FontSourceCode.SOURCEHANCODEJP,
    size=14.0,
)
```

`drawlib init` で新規プロジェクトを作成する際に `--lang ja`（または `zh`、`ko`）を渡すと、この `styles.py` 設定が自動生成されます。

### 5.2. オフライン・CI 向けのフォントアセットキャッシュ (`drawlib cache`)

`drawlib` 本体パッケージ（wheel）を軽量に保つため、フォントファイルは初回利用時にダウンロードされてローカルにキャッシュされます。エアギャップ環境、Docker イメージビルド、または CI パイプラインでは、CLI を使って事前にフォントパッケージを一括ダウンロードできます（詳細は [キャッシュ機構と CI/CD](../09_doc_builder_and_cli/caching_and_cicd.md) を参照してください）。

```bash
# Inspect cached font and icon packages
uv run drawlib cache list

# Pre-download all font and icon packages for offline builds
uv run drawlib cache download --all

# Clear cached font/icon assets if needed
uv run drawlib cache clear --all
```
