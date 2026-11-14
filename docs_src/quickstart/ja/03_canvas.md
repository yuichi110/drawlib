# 3. デカルト座標キャンバスとアンカー設計

Drawlib のすべての図解は、**左下隅を原点 `(0, 0)`** とし、`X` 軸が右方向（`0 -> width`）、`Y` 軸が上方向（`0 -> height`）へ増加する決定論的な **2 次元デカルト座標平面**上に描画されます。

**左下原点のデカルト座標系**・**`720pt` タイポグラフィ計算式**・**コンポーネント別の基準アンカー規則**の 3 点を押さえることで、人間のエンジニアも AI コーディングエージェントも文字重なりや配置ズレのない美しい図解を一発で設計できるようになります。

```drawlib align=center code=fold file=cartesian_canvas_ja.png caption="図 3.1: Drawlib の左下 (0, 0) デカルト座標系・安全マージン領域・プロット座標"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=148, height=72)

# 仮想キャンバス外枠 [26..126] x [16..64] と外周 6 単位内側の安全マージン領域
rectangle((76.0, 40.0), width=100.0, height=48.0, style=Styles.Neutral.patch(shape_line_width=1.2))
rectangle(
    (76.0, 40.0),
    width=88.0,
    height=36.0,
    style=Styles.PrimaryDashed.patch(shape_fill_color=Colors.White, shape_r=1.4),
)
text(
    (34.5, 55.2),
    "安全マージン領域 (外周から 4–6 単位内側)",
    style=Styles.MutedBold.patch(text_size=10.2, halign="left", valign="top"),
)

# 中心座標の補助クロスヘア（中央バッジの背面に描画）
line((32.0, 40.0), (120.0, 40.0), style=Styles.MutedDotted)
line((76.0, 22.0), (76.0, 50.5), style=Styles.MutedDotted)

# デカルト X 軸（右向き）と Y 軸（上向き）
line((26.0, 16.0), (136.0, 16.0), arrow_head="->", style=Styles.DarkBold)
text((138.0, 16.0), "+X", style=Styles.DarkBold.patch(text_size=11.5, halign="left", valign="center"))
text((76.0, 7.2), "X 軸：右方向へ増加 (0 -> width)", style=Styles.DarkBold.patch(text_size=11.0))

line((26.0, 16.0), (26.0, 67.5), arrow_head="->", style=Styles.DarkBold)
text((23.2, 66.8), "+Y", style=Styles.DarkBold.patch(text_size=11.5, halign="right", valign="center"))
text(
    (9.5, 40.0),
    "Y 軸：上方向へ増加 (0 -> height)",
    style=Styles.DarkBold.patch(text_size=11.0, angle=90),
)

# 四隅のマーカーとオフセット配置ラベル（軸線やドットとの重なりゼロ）
circle((26.0, 16.0), radius=1.25, style=Styles.PrimaryFlat)
text((24.0, 12.2), "原点 (0, 0)", style=Styles.DarkBold.patch(text_size=10.8, halign="right", valign="top"))

circle((126.0, 16.0), radius=0.95, style=Styles.DarkFlat)
text((126.0, 12.2), "(W, 0)", style=Styles.DarkBold.patch(text_size=10.5, halign="center", valign="top"))

circle((26.0, 64.0), radius=0.95, style=Styles.DarkFlat)
text((29.2, 64.8), "(0, H)", style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="bottom"))

circle((126.0, 64.0), radius=0.95, style=Styles.DarkFlat)
text((128.5, 64.0), "(W, H)", style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="center"))

# 中心アンカーバッジと 2 つのサンプル座標点
rectangle(
    (76.0, 40.0),
    width=34.0,
    height=9.8,
    style=Styles.PrimaryFlat.patch(shape_r=2.0),
    text="中心 (W/2, H/2)",
    text_style=Styles.WhiteBold.patch(text_size=10.8),
)

circle((45.0, 28.0), radius=1.05, style=Styles.DarkFlat)
text((47.6, 28.0), "P1 (25, 20)", style=Styles.DarkBold.patch(text_size=10.4, halign="left", valign="center"))

circle((108.0, 50.5), radius=1.05, style=Styles.DarkFlat)
text((105.4, 50.5), "P2 (95, 48)", style=Styles.DarkBold.patch(text_size=10.4, halign="right", valign="center"))

save()
```

---

## 3.1 デカルト座標系とブラウザ DOM / SVG 座標系の違い

HTML5 の `<canvas>` や CSS 配置、生の `<svg>` に慣れているエンジニアは、`Y` 座標の上下反転を防ぐために以下の違いを最初に確認してください。

| 座標特性 | **Drawlib デカルト座標系** | ブラウザ DOM / HTML `<svg>` |
| :--- | :--- | :--- |
| **原点 `(0, 0)` の位置** | **左下隅（Bottom-Left）** | 左上隅（Top-Left） |
| **水平 `+X` 方向** | 左から右へ増加（`0 -> width`） | 左から右へ増加（`0 -> width`） |
| **垂直 `+Y` 方向** | **下から上へ増加（`0 -> height`）** | 上から下へ増加（`0 -> height`） |
| **上部タイトルの配置** | 大きい `Y` 値（`height - 6` 付近） | 小さい `Y` 値（`16px` 付近） |
| **外周の安全マージン** | `[5, W - 5]` × `[5, H - 5]` の内側に配置 | CSS padding / viewBox |

数学のグラフや建築立面図と同じく `+Y` が上を向いているため、**「`Y` の値が大きいほど画面の上方に配置される」**という直感的なメンタルモデルで統一されています。図タイトルは `height - 6` 付近、メインの構成要素は `height / 2` 前後、注釈や凡例は `y = 6..10` 付近に置きます。また、枠線や角丸の見切れを防ぐため、キャンバス四辺には必ず **`4〜6` 単位の外周マージン**を確保してください。

---

## 3.2 キャンバスのライフサイクル：`setup()`・描画・`save()`

単体スクリプトでも Markdown 埋め込みブロックでも、Drawlib の作図コードは常に 3 ステップのライフサイクルで構成されます。

1. **`setup(width=..., height=..., dpi=..., background_color=..., grid=...)`**: キャンバスの幅と高さを**抽象的な仮想座標単位**（`width` / `height`、既定値 `100 × 100`）で定義し、出力画像のピクセル解像度を `dpi`（既定値 `100`）で指定します。座標計算と解像度が分離されているため、`dpi=100` を `dpi=200` に引き上げても `(x, y)` 座標を一切書き換えることなく出力ピクセル数だけを 2 倍に高精細化できます。また、配色テーマやフォント設定（`from drawlib.styles import Colors, Styles`）はプロジェクトの `styles.py`（`drawlib.toml` の `style = "google"` 等）から自動適用されます。
2. **宣言的な描画呼び出し**: 背面の境界枠や接続線から前面のノード・ラベルへと奥から手前（Back-to-Front）の順で基本図形・アイコン・SmartArts・チャートを配置します。
3. **`save()`**: キャンバスの描画内容を確定して出力します。**単体 `.py` スクリプトでも Markdown 内の ```` ```drawlib ```` ブロックでも、必ず末尾を `save()` で締めくくってください**。単体スクリプトでは `<スクリプト名>.png`（または指定パス）への書き出しを実行し、Markdown 埋め込みブロックでも `save()` を明記することでそのままコピー＆ペーストして単体実行できる自己完結性が保たれます（※1 つの `.py` ファイル内で複数画像を連続生成する場合は、各 `save(...)` の直後に `clear()` を呼び出してキャンバスを初期化します）。

```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# 1. 仮想座標 136x50 単位・解像度 150 DPI（出力サイズ 2040x750 px）で初期化
setup(width=136, height=50, dpi=150)

# 2. 奥から手前の順で描画（ニュートラル基調 + 主役ノード 1 個のみ PrimaryFlat）
line((44, 25), (54, 25), arrow_head="->", style=Styles.DarkBold)
line((82, 25), (92, 25), arrow_head="->", style=Styles.DarkBold)

rectangle((26, 25), width=36, height=18, style=Styles.Neutral, text="クライアント")
rectangle(
    (68, 25),
    width=28,
    height=18,
    style=Styles.PrimaryFlat,
    text="API コア",
    text_style=Styles.WhiteBold,
)
rectangle((110, 25), width=36, height=18, style=Styles.SecondaryNeutral, text="PostgreSQL")

# 3. ライフサイクル確定のため必ず save() を呼び出す
save()
```

---

## 3.3 `720pt` タイポグラフィ計算式とキャンバスサイズ設計

Drawlib の内部レンダラは図全体の基準幅を **`720pt` 固定**としてフォントサイズを正規化します。そのため、`dpi` の値にかかわらず、HTML・PDF・スライド上で画像が `Display Width`（表示幅ピクセル）で描画された際の見た目上の文字サイズは以下の式で厳密に決まります。

```text
Rendered Font Size (px) = text_size × (Display Width (px) / 720)
```

この比例関係を理解しておくと、ドキュメントに埋め込んだ際に図中の文字だけ極端に小さくなる問題を防げます。

- **`text_size >= 10.0` を厳守する**: 技術文書（`doc`・`site`・`catalog`）の本文カラム幅はおよそ `820px〜900px`（`Display Width / 720 ≈ 1.15〜1.25`）です。ノード本文に **`10.5〜12.0`**、見出しに **`12.0〜14.0`** を指定すれば画面上で `12px〜17px` 相当となり、周囲の `16px` HTML 本文と自然に調和します（目盛り補助ラベル等の最小下限でも `9.5` 未満には下げないでください）。
- **ドキュメント埋め込み図の最適幅は `width=120..150`**: `setup(width=140, height=60)` のように幅を `120〜150` 単位に設定すると、`10` 単位刻みのグリッド計算がしやすく、ファーストビューに収まりの良い横長比率になります。
- **フェンス属性で狭いピクセル幅を指定しない**: ```` ```drawlib ```` フェンスに `width=500px` や `600px` を指定すると、`Display Width / 720` が `0.69` まで縮小し、図内のすべての文字が 30% 以上小さくなってしまいます。

| 用途・出力先 | 推奨 `setup(width, height)` | 標準表示幅 | 推奨 `text_size` | 画面上の実表示文字サイズ |
| :--- | :--- | :--- | :--- | :--- |
| **技術文書・Web サイトの図解** | `140 × 60`（幅 `120..150`） | `~840px` | **`10.5〜12.0`**（見出し `12.0〜14.0`） | **`~12.5px〜16.5px`**（`16px` 本文と調和） |
| **情報密度の高い全体構成図** | `148 × 72` | `~840px` | **`10.0〜11.5`**（見出し `12.0〜13.5`） | **`~11.7px〜15.8px`** |
| **16:9 フル幅スライド図解** | `160 × 80` | `~1760px` | **`11.0〜13.0`**（見出し `14.0〜16.0`） | **`~27px〜39px`**（`26px` スライド本文と調和） |

---

## 3.4 テキスト配置（`halign` / `valign`）とコンポーネントのアンカー設計

単体テキスト `text(xy, label, style=...)` の基準点 `xy` に対する揃え位置は、既存の `Styles.*` トークンに `.patch(halign=..., valign=...)` を適用して制御します（`Style(...)` を直接インスタンス化せず、常に `.patch(...)` を使用します）。

- **`halign="left" | "center" | "right"`**: `x` を左端にして右へ伸ばす（`"left"`）、`x` を水平中央にする（`"center"`、既定値）、または `x` を右端にして左へ伸ばす（`"right"`）かを指定します。
- **`valign="bottom" | "center" | "top"`**: `y` のベースライン上に載せる（`"bottom"`）、`y` を垂直中央にする（`"center"`、既定値）、または `y` を上端にして下へ伸ばす（`"top"`）かを指定します。

さらに、Drawlib の全コンポーネントは以下の **3 種類の座標アンカー規則**のいずれかに明確に分類されます。

```drawlib align=center code=fold file=text_alignment_anchors_ja.png caption="図 3.2: テキスト配置（halign / valign）と 3 種のコンポーネント基準アンカー"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=68)

# 左パネル: halign / valign の基準点デモ（アンカードットと文字の重なりゼロ）
p_left = Panel(
    "テキスト配置 (halign & valign)",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    icon=phosphor.text_t,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
p_left.draw((5.0, 5.0), width=66.0, height=58.0)

# 1段目: halign="left", valign="center"
rectangle((38.0, 45.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
line((13.0, 41.2), (13.0, 48.8), style=Styles.MutedDashed)
circle((13.0, 45.0), radius=1.05, style=Styles.PrimaryFlat)
text(
    (16.0, 45.0),
    'halign="left", valign="center"',
    style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="center"),
)

# 2段目: halign="center", valign="bottom"
rectangle((38.0, 30.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
line((16.0, 26.5), (60.0, 26.5), style=Styles.MutedDashed)
circle((38.0, 26.5), radius=1.05, style=Styles.PrimaryFlat)
text(
    (38.0, 28.5),
    'halign="center", valign="bottom"',
    style=Styles.DarkBold.patch(text_size=10.5, halign="center", valign="bottom"),
)

# 3段目: halign="right", valign="top"
rectangle((38.0, 15.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
line((22.0, 18.5), (63.0, 18.5), style=Styles.MutedDashed)
circle((63.0, 18.5), radius=1.05, style=Styles.PrimaryFlat)
text(
    (60.2, 16.5),
    'halign="right", valign="top"',
    style=Styles.DarkBold.patch(text_size=10.5, halign="right", valign="top"),
)

# 右パネル: コンポーネントの 3 大基準アンカーモデル
p_right = Panel(
    "コンポーネントの基準アンカー設計",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    icon=phosphor.crosshair,
    icon_style=Styles.DarkBold,
    header_height=8.5,
)
p_right.draw((77.0, 5.0), width=66.0, height=58.0)

# 分類 1: 中央基準 Center (cx, cy) — 主役ノード PrimaryFlat 1個
rectangle((110.0, 45.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
rectangle((90.5, 45.0), width=14.5, height=7.8, style=Styles.PrimaryFlat.patch(shape_r=1.2))
circle((90.5, 45.0), radius=1.05, style=Styles.WhiteFlat)
text((100.8, 47.0), "中央基準 (cx, cy)", style=Styles.DarkBold.patch(text_size=10.8, halign="left"))
text((100.8, 42.6), "基本図形・アイコン・画像・text()", style=Styles.Dark.patch(text_size=10.0, halign="left"))

# 分類 2: 左下基準 Bottom-Left (x0, y0)
rectangle((110.0, 30.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
rectangle((90.5, 30.0), width=14.5, height=7.8, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
circle((83.25, 26.1), radius=1.05, style=Styles.PrimaryFlat)
text((100.8, 32.0), "左下基準 (x0, y0)", style=Styles.DarkBold.patch(text_size=10.8, halign="left"))
text((100.8, 27.6), "チャート・構成図・大半の SmartArts", style=Styles.Dark.patch(text_size=10.0, halign="left"))

# 分類 3: 左上基準 Top-Left (x0, y_top)
rectangle((110.0, 15.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
rectangle((90.5, 15.0), width=14.5, height=7.8, style=Styles.SecondaryNeutral.patch(shape_r=1.2))
circle((83.25, 18.9), radius=1.05, style=Styles.PrimaryFlat)
text((100.8, 17.0), "左上基準 (x0, y_top)", style=Styles.DarkBold.patch(text_size=10.8, halign="left"))
text((100.8, 12.6), "Table・TreeNode・SourceCode", style=Styles.Dark.patch(text_size=10.0, halign="left"))

save()
```

基本プリミティブと複合コンポーネント（SmartArts・Charts・Diagrams）を組み合わせる際は、常に以下の 3 分類を意識してください。

- **中央基準 `Center (cx, cy)`**: 基本図形（`shapes.*`）・`text()`・アイコン群（`phosphor.*`・`gcp.*`・`aws.*`・`azure.*`）・`images.image()`・`MindMapNode`・`Cycle`・および `ArchitectureDiagram` 内の個別 `Node` 配置で使用されます。要素は水平 `[cx - w/2, cx + w/2]`、垂直 `[cy - h/2, cy + h/2]` の範囲を占めます。
- **左下基準 `Bottom-Left (x0, y0)`**: すべての定量チャート（`charts.*`）・ダイアグラム全体の描画（`d.draw(xy=(x0, y0))` や `NodeGroup(..., xy=(x0, y0))`）・および大半の SmartArts（`Panel`・`CardList`・`ChevronProcess`・`GridLayout`・`KpiCards`・`BoxList`・`Pyramid`・`Roadmap`・`GeoMap`・`*Calendar`）で使用されます。幅 `W` のキャンバス中央に幅 `w` の部品を置く場合は `x0 = (W - w) / 2` を渡します（`W / 2` を渡すと右半分へはみ出すため注意してください）。
- **左上基準 `Top-Left (x0, y_top)`**: 文書構造系の SmartArts である `Table`・`TreeNode`・`BulletPoints`・`SourceCode` で使用され、固定した上端ライン `y_top` から下方向へ向かって行やツリーが自然に伸びる設計になっています。
