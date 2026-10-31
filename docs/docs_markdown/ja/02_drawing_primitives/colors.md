# カラーパレットと色モデル

Drawlib は、厳選されたテーマパレット（`DefaultColors`、`GoogleColors`、`MonochromeColors`、`CssColors`）と線形色補間ユーティリティを備えたイミュータブルな RGBA **`Color`** モデルによって色を表現します。

---

## 1. セマンティックカラーロールと明度階調の概要



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/colors/colors_overview.png" alt="colors_1" />
  <figcaption class="drawlib-caption">Drawlib の 7 種類のセマンティックカラーロールと 6 段階のトーンランプ</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=130, height=62)

roles = [
    ("Primary", [Colors.Primary1, Colors.Primary2, Colors.Primary3, Colors.Primary4, Colors.Primary5, Colors.Primary6]),
    ("Secondary", [Colors.Secondary1, Colors.Secondary2, Colors.Secondary3, Colors.Secondary4, Colors.Secondary5, Colors.Secondary6]),
    ("Accent", [Colors.Accent1, Colors.Accent2, Colors.Accent3, Colors.Accent4, Colors.Accent5, Colors.Accent6]),
    ("Success", [Colors.Success1, Colors.Success2, Colors.Success3, Colors.Success4, Colors.Success5, Colors.Success6]),
    ("Warning", [Colors.Warning1, Colors.Warning2, Colors.Warning3, Colors.Warning4, Colors.Warning5, Colors.Warning6]),
    ("Danger", [Colors.Danger1, Colors.Danger2, Colors.Danger3, Colors.Danger4, Colors.Danger5, Colors.Danger6]),
    ("Muted", [Colors.Muted1, Colors.Muted2, Colors.Muted3, Colors.Muted4, Colors.Muted5, Colors.Muted6]),
]

for col_idx, (role_name, shades) in enumerate(roles):
    cx = 13.5 + col_idx * 17.2
    text((cx, 55.5), role_name, style=Styles.DarkBold.patch(text_size=10.0))
    for row_idx, shade in enumerate(shades):
        cy = 45.5 - row_idx * 7.5
        txt_st = Styles.DarkBold if row_idx < 3 else Styles.WhiteBold
        rectangle(
            (cx, cy),
            width=15.4,
            height=6.6,
            style=Styles.NeutralFlat.patch(shape_fill_color=shade, shape_r=1),
            text=f"{role_name[0]}{row_idx + 1}",
            text_style=txt_st.patch(text_size=10.0),
        )

save()
```

</details>



---

## 2. `Color` クラス (`drawlib.preset_colors.Color`)

Drawlib のすべての色定数は `Color` のインスタンスです（`drawlib.styles` または `drawlib.preset_colors` からインポート可能）。`Color` はイミュータブルな RGBA モデルであると同時に、4 要素タプル `(r, g, b, alpha)` のようにも振る舞います。



```python
from drawlib.canvas import save, setup
from drawlib.preset_colors import Color
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=126, height=50)

# Left Panel: Custom RGB and Hex Color construction
rectangle((26, 25), width=42, height=40, style=Styles.Neutral.patch(shape_r=2))
text((26, 40), "Custom RGB & Hex", style=Styles.DarkBold.patch(text_size=10.5))

c_rgb = Color(37, 99, 235)
c_hex = Color("#10B981")

rectangle(
    (26, 29),
    width=36,
    height=11,
    style=Styles.NeutralFlat.patch(shape_fill_color=c_rgb, shape_r=1.5),
    text="Color(37, 99, 235)",
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)
rectangle(
    (26, 14),
    width=36,
    height=11,
    style=Styles.NeutralFlat.patch(shape_fill_color=c_hex, shape_r=1.5),
    text='Color("#10B981")',
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)

# Right Panel: Alpha opacity patching on Colors.Blue4
rectangle((87, 25), width=68, height=40, style=Styles.Neutral.patch(shape_r=2))
text((87, 40), "Colors.Blue4.patch(alpha=...)", style=Styles.DarkBold.patch(text_size=10.5))

for i, a_val in enumerate([0.2, 0.5, 0.8, 1.0]):
    cx = 62.2 + i * 16.5
    col = Colors.Blue4.patch(alpha=a_val)
    lbl_st = Styles.DarkBold if a_val <= 0.5 else Styles.WhiteBold
    rectangle(
        (cx, 22),
        width=14.8,
        height=22,
        style=Styles.Neutral.patch(shape_fill_color=col, shape_line_width=0.8, shape_r=1.5),
        text=f"alpha\n{a_val}",
        text_style=lbl_st.patch(text_size=10.0),
    )

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/colors/colors_alpha_and_hex.png" alt="colors_2" />
  <figcaption class="drawlib-caption">カスタム RGB／Hex カラーの生成とアルファ不透明度のレイヤリング</figcaption>
</figure>



| プロパティ／メソッド | 戻り値の型 | 説明 |
| :--- | :--- | :--- |
| `color.r`, `color.g`, `color.b` | `int` (`0..255`) | 赤（Red）・緑（Green）・青（Blue）の各チャンネル値。 |
| `color.alpha` / `color.a` | `float` (`0.0..1.0`) | 不透明度チャンネル（`0.0` = 完全透明、`1.0` = 完全不透明）。 |
| `color.rgb` | `tuple[int, int, int]` | 標準の 3 要素タプル `(r, g, b)`。 |
| `color.rgba` | `tuple[int, int, int, float]` | 標準の 4 要素タプル `(r, g, b, alpha)`。 |
| `color.hex` | `str` | 小文字の 16 進カラーコード文字列（`"#rrggbb"`、または `alpha < 1.0` の場合は `"#rrggbbaa"`）。 |
| `Color.from_hex(hexcode, alpha=None)` | `Color` | 3 桁・4 桁・6 桁・8 桁の 16 進カラー文字列を解析して `Color` を生成します（任意の `alpha` 上書き対応）。 |
| `color.patch(r=..., g=..., b=..., alpha=...)` | `Color` | 指定したチャンネルまたは不透明度を更新した新しい `Color` を返します。 |
| `color.to_mplot_rgba()` | `tuple[float, float, float, float]` | Matplotlib バックエンド向けの `0.0..1.0` 正規化 RGBA タプル。 |

---

## 3. プリセットカラーパレットと明度階調

すべてのカラーカタログは `drawlib.preset_colors` からインポートします（現在有効なパレットは `drawlib.styles` の `Colors` として公開されます）。

```python
from drawlib.preset_colors import (
    CssColors,
    DefaultColors,
    DefaultColors1,
    DefaultColors2,
    DefaultColors3,
    DefaultColors4,
    DefaultColors5,
    DefaultColors6,
    GoogleColors,
    MonochromeColors,
)
```

### 3.1. 明度階調（トーン）とサーフェストークン

`DefaultColors` および `GoogleColors` では、すべてのセマンティックロール（`Primary`、`Secondary`、`Accent`、`Warning`、`Danger`、`Success`、`Muted`）と有彩色相（`Blue`、`Green`、`Red`、`Orange`、`Amber`、`Purple`、`Teal`、`Pink`）が **6 段階の明度階調（トーン）** とサーフェストークンに体系化されています。

| トーン／トークン | 属性の例 | 視覚的役割 |
| :--- | :--- | :--- |
| **トーン `1`（極淡色／パステル）** | `Colors.Primary1`, `Colors.Blue1`, `Colors.PrimaryNeutral` | 淡く色付けされたニュートラルカードの塗り色（`Styles.*Neutral`）。 |
| **トーン `2`（淡色）** | `Colors.Primary2`, `Colors.Gray2`, `Colors.Neutral` | 落ち着いた標準ニュートラルカードの背景面（`Styles.Neutral`）。 |
| **トーン `3`（ソフト中間色）** | `Colors.Primary3`, `Colors.Blue3`, `Colors.Gray3` | 色付きニュートラルカードの枠線や控えめな区切り線。 |
| **トーン `4`（標準／ベース）** | `Colors.Primary` (`Primary4`), `Colors.Blue4` | 標準の鮮やかなヒーロー塗りつぶし色（`Styles.PrimaryFlat`）。 |
| **トーン `5`（濃色）** | `Colors.Primary5`, `Colors.Blue5`, `Colors.Gray5` | 強調された枠線やアクティブ状態。 |
| **トーン `6`（最濃色）** | `Colors.Primary6`, `Colors.Blue6` | 色付きニュートラルカード内の高コントラスト文字色。 |
| **サーフェス・チャコール系** | `Colors.Canvas`, `Colors.Light` (`White`), `Colors.Dark` (`Gray7`), `Colors.Gray1`..`Gray8`, `Colors.Black` | キャンバス背景、カード面、枠線、および本文のチャコール文字色。 |



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/colors/colors_chromatic_and_surface_swatches.png" alt="colors_3" />
  <figcaption class="drawlib-caption">8 種類の有彩色相ファミリー（トーン 1〜6）とグレースケール・サーフェスランプ</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=134, height=74)

hues = ["Blue", "Green", "Red", "Orange", "Amber", "Purple", "Teal", "Pink"]

for col_idx, hue in enumerate(hues):
    cx = 12.2 + col_idx * 15.6
    text((cx, 68.5), hue, style=Styles.DarkBold.patch(text_size=10.0))
    for tier in range(1, 7):
        cy = 60.0 - (tier - 1) * 6.8
        col = getattr(Colors, f"{hue}{tier}")
        txt_st = Styles.DarkBold if tier <= 3 else Styles.WhiteBold
        rectangle(
            (cx, cy),
            width=14.2,
            height=6.0,
            style=Styles.NeutralFlat.patch(shape_fill_color=col, shape_r=1),
            text=f"{hue[0]}{tier}",
            text_style=txt_st.patch(text_size=10.0),
        )

# Bottom row: Grayscale & Surface Ramp (Light, Gray1..Gray8, Dark)
text((67, 17.5), "Surface & Grayscale Ramp (Light, Gray1..Gray8, Dark)", style=Styles.DarkBold.patch(text_size=10.5))
surfaces = [
    ("L", Colors.Light),
    *[(f"G{i}", getattr(Colors, f"Gray{i}")) for i in range(1, 9)],
    ("D", Colors.Dark),
]
for s_idx, (s_lbl, s_col) in enumerate(surfaces):
    sx = 11.8 + s_idx * 12.3
    s_txt = Styles.DarkBold if s_idx < 5 else Styles.WhiteBold
    rectangle(
        (sx, 9.0),
        width=11.2,
        height=8.0,
        style=Styles.Neutral.patch(shape_fill_color=s_col, shape_line_width=0.6, shape_r=1),
        text=s_lbl,
        text_style=s_txt.patch(text_size=10.0),
    )

save()
```

</details>



### 3.2. テーマパレットの比較 (`DefaultColors1..6`, `GoogleColors`, `MonochromeColors`, `CssColors`)

- **`DefaultColors` (`DefaultColors1`..`DefaultColors6`)**: `DefaultColors` はセマンティックロールの中心をトーン 4（`DefaultColors4`）に置きます。一方 `DefaultColors1`〜`DefaultColors6` はデフォルトの `Primary`／`Secondary`／`Accent` トークンをトーン 1〜6 にシフトさせます。
- **`GoogleColors`**: Google Workspace／Material の公式トーン（`GoogleBlue`、`GoogleRed`、`GoogleYellow`、`GoogleGreen`、`GoogleOrange`、`GooglePurple`、`CornflowerBlue1..6`、`RedBerry1..6`）。
- **`MonochromeColors`**: 印刷物や学術論文向けの 10 段階の純粋なグレースケールランプ（`White`、`Gray1`..`Gray8`、`Black`）。
- **`CssColors`**: W3C CSS の全 140 種類の名前付きカラー（`CssColors.AliceBlue`、`CssColors.CornflowerBlue`、`CssColors.DarkSlateGray` など）。



```python
from drawlib.canvas import save, setup
from drawlib.preset_colors import DefaultColors, GoogleColors, MonochromeColors
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=56)

palettes = [
    (44, "DefaultColors", [DefaultColors.Primary, DefaultColors.Secondary, DefaultColors.Accent, DefaultColors.Success, DefaultColors.Warning, DefaultColors.Danger]),
    (28, "GoogleColors", [GoogleColors.Primary, GoogleColors.Secondary, GoogleColors.Accent, GoogleColors.Success, GoogleColors.Warning, GoogleColors.Danger]),
    (12, "Monochrome", [MonochromeColors.Gray1, MonochromeColors.Gray2, MonochromeColors.Gray4, MonochromeColors.Gray6, MonochromeColors.Gray8, MonochromeColors.Black]),
]

headers = ["Primary", "Secondary", "Accent", "Success", "Warning", "Danger"]
for idx, h in enumerate(headers):
    text((44 + idx * 15.5, 52), h, style=Styles.DarkBold.patch(text_size=10.0))

for y, label, swatch_list in palettes:
    text((6, y), label, style=Styles.DarkBold.patch(text_size=10.5, halign="left"))
    for idx, col in enumerate(swatch_list):
        cx = 44 + idx * 15.5
        rectangle(
            (cx, y),
            width=13.5,
            height=10,
            style=Styles.Neutral.patch(shape_fill_color=col, shape_line_width=0.8, shape_r=1.5),
        )

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/colors/colors_theme_palettes.png" alt="colors_4" />
  <figcaption class="drawlib-caption">DefaultColors、GoogleColors、MonochromeColors のカラースウォッチ比較</figcaption>
</figure>



---

## 4. 色の線形補間 (`get_intermediate_color` と `get_intermediate_colors`)

ヒートマップ、多段階パイプライン、あるいは滑らかなアニメーション遷移を作成する際は、`drawlib.styles`（または `drawlib.preset_colors`）の `get_intermediate_color` と `get_intermediate_colors` を利用します。

- **`get_intermediate_color(color1, color2) -> Color`**: `color1` と `color2` のちょうど 50% 中間にあたる `Color` を返します。
- **`get_intermediate_colors(color1, color2, num=1, *, include_ends=False) -> list[Color]`**: `color1` から `color2` への線形 RGBA 遷移を `num + 1` 等分し、`num` 個の中間色（`include_ends=True` の場合は両端を含む `num + 2` 個の色）をリストとして返します。



```python
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles, get_intermediate_colors
from drawlib.text import text

setup(width=130, height=44)

# Generate 7 steps including endpoints from Primary1 (light pastel) to Primary6 (dark shade)
steps = get_intermediate_colors(Colors.Primary1, Colors.Primary6, num=5, include_ends=True)

text((65, 36.5), "get_intermediate_colors(Colors.Primary1, Colors.Primary6, num=5, include_ends=True)", style=Styles.DarkBold.patch(text_size=10.5))

for i, col in enumerate(steps):
    cx = 13.5 + i * 17.2
    label_style = Styles.DarkBold if i < 3 else Styles.WhiteBold
    rectangle(
        (cx, 18.5),
        width=15.5,
        height=18,
        style=Styles.NeutralFlat.patch(shape_fill_color=col, shape_r=1.5),
        text=col.hex,
        text_style=label_style.patch(text_size=10.0),
    )

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/colors/colors_interpolation.png" alt="colors_5" />
  <figcaption class="drawlib-caption">get_intermediate_colors() で生成した滑らかなカラーグラデーション</figcaption>
</figure>


