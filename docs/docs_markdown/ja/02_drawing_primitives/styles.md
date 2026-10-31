# スタイルとテーマ設定

複雑な技術図解において、描画呼び出しのたびに RGB タプルや線幅、フォントウェイトを手動で指定すると、視覚的な一貫性が損なわれ、保守しづらいコードになってしまいます。
Drawlib は `drawlib.styles` と `drawlib.preset_styles` による**統一デザイントークンシステム**によってこの課題を解決します。

---

## 1. セマンティックスタイルとバリアントの概要



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/styles/styles_overview.png" alt="styles_1" />
  <figcaption class="drawlib-caption">セマンティックスタイルトークンと直交バリアントの概要</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=128, height=52)

# Row 1: Core Semantic Card & Hero Roles
rectangle((24, 37), width=35, height=18, style=Styles.PrimaryFlat.patch(shape_r=2), text="PrimaryFlat\n(Hero Focal)", text_style=Styles.WhiteBold.patch(text_size=10.5))
rectangle((64, 37), width=35, height=18, style=Styles.Neutral.patch(shape_r=2), text="Neutral\n(50%+ Baseline)", text_style=Styles.DarkBold.patch(text_size=10.5))
rectangle((104, 37), width=35, height=18, style=Styles.SecondaryNeutral.patch(shape_r=2), text="SecondaryNeutral\n(Auxiliary Card)", text_style=Styles.DarkBold.patch(text_size=10.5))

# Row 2: Structural & Status Variants
rectangle((24, 15), width=35, height=18, style=Styles.SuccessNeutral.patch(shape_r=2), text="SuccessNeutral\n(Verified State)", text_style=Styles.DarkBold.patch(text_size=10.5))
rectangle((64, 15), width=35, height=18, style=Styles.DangerFlat.patch(shape_r=2), text="DangerFlat\n(Critical Alert)", text_style=Styles.WhiteBold.patch(text_size=10.5))
rectangle((104, 15), width=35, height=18, style=Styles.MutedDashed.patch(shape_r=2), text="MutedDashed\n(VPC / Boundary)", text_style=Styles.DarkBold.patch(text_size=10.5))

save()
```

</details>



---

## 2. `styles.py` による一元管理アーキテクチャ

Drawlib は、**プロジェクトで有効なトークン**（`drawlib.styles`）と**イミュータブルなファクトリカタログ**（`drawlib.preset_styles` および `drawlib.preset_colors`）を明確に分離しています。

```python
# Recommended in all drawing scripts and markdown blocks:
from drawlib.styles import Colors, Styles
```

| インポートパターン | モジュール | 挙動とユースケース |
| :--- | :--- | :--- |
| `from drawlib.styles import Colors, Styles` | `drawlib.styles` | **推奨。** 現在のプロジェクトテーマを参照します。プロジェクトの `styles.py` や `--styles` オプションで指定された上書き設定が自動的に反映されます。 |
| `from drawlib.preset_styles import DefaultStyles, GoogleStyles, MonochromeStyles` | `drawlib.preset_styles` | 静的なファクトリカタログ。`styles.py` 内でベーステーマを選択する場合や、複数のテーマを並べて比較する場合に使用します。 |

> [!IMPORTANT]
> `drawlib.styles` からは必ず PascalCase の `Styles` と `Colors` をインポートしてください。小文字の `styles` や `colors` 変数を使うと、`drawlib.styles` モジュール自体をシャドーイングしてしまうため避けてください。

### `styles.py` によるプロジェクト全体のデフォルトカスタマイズ

`drawlib init` で生成されたすべてのプロジェクトには、ルートに `styles.py` ファイルが含まれています。`drawlib build` や `drawlib show` の実行時、Drawlib は `styles.py` を読み込み、その `Styles` オブジェクトと `Colors` オブジェクトを `drawlib.styles` にバインドします。

```python
# styles.py
from drawlib.fonts import FontRoboto
from drawlib.preset_colors import GoogleColors
from drawlib.preset_styles import GoogleStyles

Colors = GoogleColors()
Styles = GoogleStyles().patch_font(
    regular=FontRoboto.ROBOTO_REGULAR,
    bold=FontRoboto.ROBOTO_BOLD,
    thin=FontRoboto.ROBOTO_THIN,
)
```



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/styles/styles_centralized_architecture.png" alt="styles_2" />
  <figcaption class="drawlib-caption">styles.py による一元化されたテーマ・トークンアーキテクチャ</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=132, height=44)

stages = [
    (18.5, Styles.Neutral, "Immutable Presets\npreset_colors\npreset_styles", Styles.DarkBold),
    (50.2, Styles.SecondaryNeutral, "Project styles.py\nGlobal Theme &\nFont Patching", Styles.DarkBold),
    (81.8, Styles.PrimaryFlat, "Runtime Singleton\ndrawlib.styles\nColors, Styles", Styles.WhiteBold),
    (113.5, Styles.PrimaryNeutral, "Drawing Scripts\n& Docs Blocks\nSingle Source", Styles.DarkBold),
]

for cx, st, label, txt_st in stages:
    rectangle(
        (cx, 22),
        width=27,
        height=28,
        style=st.patch(shape_r=2),
        text=label,
        text_style=txt_st.patch(text_size=10.0),
    )

for x1, x2 in [(32, 36.7), (63.7, 68.3), (95.3, 100)]:
    line((x1, 22), (x2, 22), arrow_head="->", style=Styles.DarkBold)

save()
```

</details>



---

## 3. 統合 `Style` トークンモデル

`ShapeStyle`、`LineStyle`、`TextStyle`、`IconStyle`、`ImageStyle` のようにスタイルクラスを細分化する代わりに、Drawlib はドメイン別の接頭辞付き属性と明示的な対象ドメイン指定（`supports={"shape", "line", "text", "icon", "image"}`）を備えた単一のイミュータブルな **`Style`** クラス（`from drawlib.types import Style`）を採用しています。

| 対象ドメイン | `Style` 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- | :--- |
| **図形** (`"shape"`) | `shape_fill_color` | `Color \| tuple \| str` | テーマ塗り色 | 図形内部の塗りつぶし色（ワイヤーフレームにする場合は `Colors.Transparent`）。 |
| | `shape_line_color` | `Color \| tuple \| str` | テーマ枠線色 | 外周の枠線ストローク色。 |
| | `shape_line_width` | `float` | `1.5`（Flat は `0.0`） | ポイント単位の外周枠線の太さ。 |
| | `shape_line_style` | `"solid" \| "dashed" \| "dotted" \| "dashdot"` | `"solid"` | 外周枠線の破線パターン。 |
| | `shape_r` | `float \| tuple[float, ...]` | `0.0` | キャンバス単位での角丸半径（単一スカラーまたは頂点ごとのタプル）。 |
| **線・矢印** (`"line"`) | `line_color` | `Color \| tuple \| str` | テーマ線色 | コネクタ線および矢印のストローク色。 |
| | `line_width` | `float` | `1.5`（Bold は `2.5`） | ポイント単位のコネクタ線の太さ。 |
| | `line_style` | `"solid" \| "dashed" \| "dotted" \| "dashdot"` | `"solid"` | コネクタ線の破線パターン。 |
| | `line_arrow_head_fill` | `bool` | `False` | `False` = 開いた線矢印（`->`）、`True` = 塗りつぶし三角形矢印（`-\|>`）。 |
| | `line_arrow_head_scale` | `float` | `20.0` | 端点の矢印に対する物理サイズの倍率。 |
| **テキスト・バッジ** (`"text"`) | `text_color` | `Color \| tuple \| str` | テーマ文字色 | 文字グリフの塗りつぶし色。 |
| | `text_size` | `float \| str` | `16.0` | ポイント単位のフォントサイズ、または `"small"`、`"medium"`、`"large"`。 |
| | `text_font` | `FontBase \| FontFile` | `Font.SANSSERIF_REGULAR` | [`drawlib.fonts`](fonts.md) のフォントファミリーおよびウェイトトークン。 |
| | `text_line_spacing` | `float` | `1.2` | `\n` を含む複数行テキストの行高倍率。 |
| | `text_flip` | `bool` | `False` | 図形への埋め込みテキストを `180°` 回転させ、上下逆転を防ぎます。 |
| | `text_bg_fill_color` | `Color \| tuple \| str` | `None` | テキスト背面のパディング付き背景バッジの塗りつぶし色。 |
| | `text_bg_line_color` | `Color \| tuple \| str` | `None` | 背景バッジの枠線色。 |
| | `text_bg_line_width` | `float` | `1.0` | 背景バッジの枠線幅（枠線なしは `0`）。 |
| | `text_bg_line_style` | `"solid" \| "dashed" \| "dotted" \| "dashdot"` | `"solid"` | 背景バッジの枠線破線パターン。 |
| **アイコン** (`"icon"`) | `icon_color` | `Color \| tuple \| str` | テーマアイコン色 | ベクターグリフの塗り／線色（`phosphor`、`font_icon`）。 |
| | `icon_style` | `"thin" \| "light" \| "regular" \| "bold" \| "fill"` | `"regular"` | Phosphor ベクターアイコンのウェイト種別。 |
| **画像** (`"image"`) | `image_tint_color` | `Color \| tuple \| str` | `None` | 画像の透過背景ピクセルを単色で塗りつぶします。 |
| | `image_border_color` | `Color \| tuple \| str` | `(0, 0, 0)` | 画像の外周を囲む矩形枠線の色。 |
| | `image_border_width` | `float` | `0.0` | ポイント単位の矩形枠線の太さ（`> 0` で枠線有効化）。 |
| | `image_border_style` | `"solid" \| "dashed" \| "dotted" \| "dashdot"` | `"solid"` | 画像外周の矩形枠線の破線パターン。 |
| **共通の座標変換** | `halign` | `"left" \| "center" \| "right"` | `"center"` | `xy[0]` に対する水平方向のアンカー配置揃え。 |
| | `valign` | `"bottom" \| "center" \| "top"` | `"center"` | `xy[1]` に対する垂直方向のアンカー配置揃え。 |
| | `xy_shift` | `tuple[float, float]` | `None` | `angle` の回転に追従する相対 `(dx, dy)` 座標シフト。 |
| | `xy_abs_shift` | `tuple[float, float]` | `None` | `angle` に依存しない絶対 `(dx, dy)` 座標シフト。 |
| | `angle` | `float` | `0.0` | アンカー `xy` を中心とした反時計回りの回転角（度）。 |
| | `alpha` | `float` | `1.0` | 要素全体の不透明度（`0.0` の完全透明から `1.0` の完全不透明まで）。 |

### 3.2. 非破壊なスタイル派生 (`.patch()`)

`Style` インスタンスは凍結（frozen）された Pydantic モデルです（`dataclasses.replace` を使う frozen dataclass と同様の設計）。グローバルなプリセット状態を変更せずにカスタムスタイルを派生させるには、`.patch()` を呼び出します。



```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=124, height=46)

rectangle((62, 23), width=116, height=38, style=Styles.Neutral.patch(shape_r=2))

# 1. Original preset remains completely unchanged
rectangle(
    (28, 23),
    width=36,
    height=22,
    style=Styles.Primary,
    text="Styles.Primary\n(Original Preset)",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

# 2. Derive a custom card & connector style via .patch()
highlight_card = Styles.Primary.patch(
    shape_r=4,
    shape_line_width=2.5,
    shape_line_style="dashed",
    line_width=2.5,
    line_style="dashed",
)

line((46, 23), (76, 23), arrow_head="->", style=highlight_card)
text((61, 29), ".patch()", style=Styles.DarkBold.patch(text_size=10.5))

rectangle(
    (95, 23),
    width=38,
    height=22,
    style=highlight_card,
    text="highlight_card\n(shape_r=4, dashed)",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/styles/styles_unified_token_domains.png" alt="styles_3" />
  <figcaption class="drawlib-caption">プリセットを変更せずに .patch() でカスタムスタイルを派生させる</figcaption>
</figure>




---

## 4. バリアント命名規則マトリクス

すべてのセマンティックロール（`Primary`、`Secondary`、`Accent`、`Warning`、`Danger`、`Success`、`Neutral`、`Muted`、`Light`、`Dark`）および色相名（`Blue`、`Green`、`Red`、`Orange`、`Amber`、`Purple`、`Teal`、`Pink`、`Gray1`..`Gray8`）には、**`Styles.<RoleOrColor><Variant><Weight>`** の命名規則に従った直交する視覚バリアントが用意されています。

| バリアントパターン | トークン例 | 図形の塗り | 図形／線のストローク | 線種 | フォント・アイコンウェイト |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`<Role>` / `<Role>Bordered`** | `Styles.Primary` | ロール色 | 濃色枠線（`1.5`） | `"solid"` | Regular（`16pt`） |
| **`<Role>Bold`** | `Styles.PrimaryBold` | ロール色 | 太線ストローク（`2.5`） | `"solid"` | Bold フォント・`"bold"` アイコン |
| **`<Role>Thin`** | `Styles.PrimaryThin` | ロール色 | 極細ストローク（`0.75`） | `"solid"` | Thin フォント・`"thin"` アイコン |
| **`<Role>Flat`** | `Styles.PrimaryFlat` | ロール色 | 枠線なし（`0.0`） | `"solid"` | Regular（または `"fill"` アイコン） |
| **`<Role>Neutral`** | `Styles.PrimaryNeutral` | トーン 1 パステル | トーン 3 枠線（`1.5`） | `"solid"` | トーン 6 の高コントラスト文字色 |
| **`<Role>NeutralFlat`** | `Styles.PrimaryNeutralFlat` | トーン 1 パステル | 枠線なし（`0.0`） | `"solid"` | トーン 6 の高コントラスト文字色 |
| **`<Role>Outline` / `<Role>Solid`** | `Styles.PrimaryOutline` | 透明 | ロール色（`1.5`） | `"solid"` | 図形外枠・線のみ |
| **`<Role>OutlineBold` / `SolidBold`** | `Styles.PrimarySolidBold` | 透明 | ロール色（`2.5`） | `"solid"` | 太線のワイヤーフレーム・コネクタ |
| **`<Role>OutlineThin` / `SolidThin`** | `Styles.PrimarySolidThin` | 透明 | ロール色（`0.75`） | `"solid"` | 細線のワイヤーフレーム・コネクタ |
| **`<Role>Dashed` (`Bold` / `Thin`)** | `Styles.MutedDashed` | 透明 | ロール色（`1.5`） | `"dashed"` | VPC・クラスタ境界枠 |
| **`<Role>Dotted` (`Bold` / `Thin`)** | `Styles.WarningDotted` | 透明 | ロール色（`1.5`） | `"dotted"` | 一時的・フォールバック接続線 |



```python
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=58)

# Row 1: Filled & Tinted Card Variants
row1 = [
    (18.5, Styles.Neutral, "Neutral", Styles.DarkBold),
    (48.8, Styles.PrimaryNeutral, "PrimaryNeutral", Styles.DarkBold),
    (79.2, Styles.PrimaryFlat, "PrimaryFlat", Styles.WhiteBold),
    (109.5, Styles.PrimaryBold, "PrimaryBold", Styles.WhiteBold),
]
for x, st, label, txt_st in row1:
    rectangle((x, 42), width=27, height=18, style=st.patch(shape_r=2), text=label, text_style=txt_st.patch(text_size=10.0))

# Row 2: Wireframe / Stroke Variants (Outline/Solid, Dashed, Dotted)
row2 = [
    (18.5, Styles.PrimarySolid, "PrimarySolid"),
    (48.8, Styles.PrimarySolidBold, "SolidBold"),
    (79.2, Styles.MutedDashed, "MutedDashed"),
    (109.5, Styles.PrimaryDottedBold, "DottedBold"),
]
for x, st, label in row2:
    rectangle((x, 16), width=27, height=18, style=st.patch(shape_r=2))
    text((x, 16), label, style=Styles.DarkBold.patch(text_size=10.0))

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/styles/styles_variant_matrix.png" alt="styles_4" />
  <figcaption class="drawlib-caption">Drawlib スタイルバリアントのビジュアルマトリクス（Neutral, Flat, Bordered, Solid, Dashed, Dotted）</figcaption>
</figure>



---

## 5. プリセットテーマカタログ (`drawlib.preset_styles`)

Drawlib は `drawlib.preset_styles` において、3 つのデザインファミリーにわたる **9 個のプリセットスタイルクラス**を提供しています。

| テーマクラス | CLI `--styles` 名 | 説明 |
| :--- | :--- | :--- |
| **`DefaultStyles`** | `default` | 標準的なバランスの取れた技術図解テーマ（トーン 4 のセマンティックカラーと、落ち着いたトーン 1〜2 のニュートラルカードを中心に構成）。 |
| **`DefaultStyles1` .. `DefaultStyles6`** | `1` .. `6`（`light`, `dark`） | 極淡いパステル調のトーン 1 から最濃色のトーン 6 まで基準トーンをシフトさせた `DefaultStyles` のバリエーション。 |
| **`GoogleStyles`** | `google` | Google Workspace／Slides のマテリアルパレット（Google Blue、Purple、Orange、Green、Red、Yellow）。 |
| **`MonochromeStyles`** | `monochrome` | 学術論文、特許図面、白黒印刷向けの高コントラストなグレースケールカタログ（`Primary`、`Secondary`、`Accent`、`Neutral`、`Muted`）。 |



```python
from drawlib.canvas import save, setup
from drawlib.preset_styles import DefaultStyles, GoogleStyles, MonochromeStyles
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=60)

themes = [
    (23, "DefaultStyles", DefaultStyles()),
    (64, "GoogleStyles", GoogleStyles()),
    (105, "Monochrome", MonochromeStyles()),
]

for cx, title, theme in themes:
    # Boundary container
    rectangle((cx, 30), width=37, height=48, style=theme.MutedDashed.patch(shape_r=2))
    text((cx, 48), title, style=Styles.DarkBold.patch(text_size=11.0))

    # Hero node (PrimaryFlat)
    rectangle((cx, 34), width=30, height=12, style=theme.PrimaryFlat.patch(shape_r=1.5), text="Hero Node", text_style=theme.WhiteBold.patch(text_size=10.5))

    # Supporting neutral card (SecondaryNeutral)
    rectangle((cx, 17), width=30, height=12, style=theme.SecondaryNeutral.patch(shape_r=1.5), text="Neutral Card", text_style=theme.DarkBold.patch(text_size=10.5))

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/styles/styles_theme_comparison.png" alt="styles_5" />
  <figcaption class="drawlib-caption">DefaultStyles、GoogleStyles、MonochromeStyles の並列比較</figcaption>
</figure>


