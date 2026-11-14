# 12. マルチフレームアニメーションと 16:9 スライド作成

静的な構成図がシステムの断面を切り取るのに対し、時系列アニメーションとワイドスクリーン発表資料は「処理の流れ」と「ストーリー」を動的に伝えます。Drawlib は `drawlib.anim` により **APNG（`.png`）**・**Animated WebP（`.webp`）**・**ディザノイズのない Animated GIF（`.gif`）** を純粋な Python コードから直接出力でき、さらに `drawlib.slide` により Markdown 原稿から **16:9 Web スライド**・**ベクター PDF**・**編集可能な PowerPoint（`.pptx`）** を一括生成します。

```drawlib align=center code=fold file=anim_pipeline_ja.png caption="図 12.1: Animation と ChevronProcess によるプログレッシブ表示ループ APNG アニメーション"
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles
from drawlib.text import text

setup(width=156, height=52)
anim = Animation(fps=1.5, loop=0)

stages = [
    ("1. 原稿管理", "Git 統合"),
    ("2. 構文検証", "静的チェック"),
    ("3. 図面描画", "グリッド検証"),
    ("4. 文書変換", "HTML / PDF"),
    ("5. 公開配信", "Web ポータル"),
]

for step in range(len(stages)):
    is_last = step == len(stages) - 1
    with anim.frame(duration=2.5 if is_last else 0.75):
        rectangle((78, 26), width=146, height=42, style=Styles.MutedDashed.patch(shape_r=2.2))
        phosphor.play_circle((10.5, 41.0), width=4.4, style=Styles.DarkBold)
        text(
            (14.5, 41.0),
            "段階的リリースパイプライン（マルチフレーム APNG）",
            style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
        )
        rectangle(
            (134.5, 41.0),
            width=25.0,
            height=6.2,
            style=Styles.PrimaryNeutral.patch(shape_r=1.5),
            text=f"フレーム {step + 1} / {len(stages)}",
            text_style=Styles.DarkBold.patch(text_size=10.0),
        )
        line((10, 20.5), (146, 20.5), style=Styles.MutedDashed)

        proc = ChevronProcess(
            style=Styles.Neutral,
            text_style=Styles.DarkBold.patch(text_size=10.5),
            description_style=Styles.Dark.patch(text_size=10.0),
            corner_angle=62.0,
            spacing=1.6,
            flat_left_end=True,
        )
        for i, (title, desc) in enumerate(stages):
            is_active = i == step
            c_style = Styles.PrimaryFlat if is_active else (Styles.PrimaryNeutral if i < step else Styles.Neutral)
            t_style = Styles.WhiteBold.patch(text_size=10.5) if is_active else Styles.DarkBold.patch(text_size=10.5)
            d_style = Styles.White.patch(text_size=10.0) if is_active else Styles.Dark.patch(text_size=10.0)
            proc.add(
                title,
                description=desc,
                style=c_style,
                text_style=t_style,
                description_style=d_style,
                show=(i <= step),
            )
        proc.draw(xy=(10.0, 10.0), width=136.0, height=21.0)

save()
```

---

## 12.1 drawlib.anim によるマルチフレームアニメーション

### キャンバスライフサイクルと `Animation` API

`drawlib.anim` から `Animation` をインポートし、フレームループの**前に 1 回だけ** `setup(width=..., height=...)` を呼び出したうえで、各フレームの描画処理を `with anim.frame(duration=..., clear=True):` コンテキスト内に記述します。

- **正確なコンストラクタ引数**: `anim = Animation(fps=10.0, loop=0)`（`fps` の別名として `frame_rate=10.0` も指定可能。`loop=0` は無限ループ再生）。
- **`Animation` に `file=` 引数は存在しない**: `Animation` は初期化時にアクティブなキャンバスへ自動登録されるため、`file=...` 引数は取りません。単体 Python スクリプトでは `save("out.png")`・`save("out.webp")`・`save("out.gif")` に出力パスを渡し、Markdown の ```` ```drawlib ```` ブロックではフェンス属性に `file=name.png`（または `.webp` / `.gif`）を指定して末尾で `save()` を呼びます。
- **フレーム毎クリア（`clear=True`）と最終フレーム保持**: 既定の `with anim.frame(duration=None, clear=True):` はフレーム開始時にキャンバスをクリアするため、移動やハイライト色の切り替えが残像なく行えます（要素を単純追記する場合のみ `clear=False` も選択可能）。最終フレームには `duration=2.0`〜`3.0` 秒の静止時間を設けると全体像を落ち着いて読み取れます。

| 出力形式 | 拡張子 | エンコード特性・画質 | 主な活用先 |
| :--- | :--- | :--- | :--- |
| **APNG** | `.png` / `.apng` | 可逆 24bit RGB + 8bit 透過。ブラウザで滑らかに再生され、PDF 等では自動的に鮮明な静止画として表示 | HTML ドキュメント（`site` / `doc`）、スライド、印刷用 PDF |
| **Animated WebP** | `.webp` | 可逆 24bit RGB + 8bit 透過のまま APNG 比で約 50% 軽量（`minimize_size=True`） | 大規模 Web ドキュメントサイト、モバイル Web アプリ |
| **Animated GIF** | `.gif` | `v0.3.10` のディザなし 256 色グローバル Median Cut 量子化（`Image.Dither.NONE`）により粒状ノイズ皆無 | GitHub README、Slack、Notion、Confluence、X/Twitter |

### プログレッシブ描画の定石（`show=False`・`draw_ratio`・補間関数）

Drawlib の全高レベルモジュールは、フレーム間でレイアウトがガタつかないアニメーション機構を備えています。

- **枠幅を固定した段階表示（`show=False`）**: `SmartArts`（`ChevronProcess`, `Table`, `GridLayout`, `Cycle`）の `show=False` や `Diagrams`（`FlowDiagram`, `ArchitectureDiagram`, `SequenceDiagram`）の `node.show = False` を使うと、非表示要素や接続エッジを隠しつつ配置スロットや列幅を 100% 固定したままステップ表示できます。
- **チャートの滑らかな伸長（`draw_ratio`）**: `LineChart`・`BarChart`・`AreaChart`・`PieChart`・`GanttChart` の各データ系列は `s.draw_ratio`（`0.0`〜`1.0`）と `s.draw_direction`（`"bottom_to_top"` / `"left_to_right"`）を備え、軸目盛りを固定したままグラフを成長させられます。
- **座標・カラー補間とイージング**: `drawlib.math.get_intermediate_points()` / `get_intermediate_path_points()` によるパケット移動（$t^2(3 - 2t)$ などのイージング比率併用）や、`drawlib.styles.get_intermediate_colors(c1, c2, num=..., include_ends=True)` による塗りのフェード遷移が標準関数だけで完結します。

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Styles

setup(width=110, height=64)
anim = Animation(fps=10.0, loop=0)

chart = BarChart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Dark.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    width=86,
    height=44,
    title="Quarterly API Throughput (kRPS)",
    title_style=Styles.DarkBold.patch(text_size=12.5),
)
chart.configure_y_axis(min_value=0, max_value=120)
series = chart.add_series("Throughput", [42, 68, 94, 112], style=Styles.PrimaryFlat)

steps = 6
for i in range(1, steps + 1):
    t = i / steps
    eased = t * t * (3.0 - 2.0 * t)  # Smoothstep イージング (0 -> 1)
    series.draw_ratio = eased
    with anim.frame(duration=2.2 if i == steps else 0.12):
        chart.draw(xy=(12, 8))

save("throughput_growth.gif")
```

---

## 12.2 16:9 プレゼンテーションスライドと PowerPoint 出力（drawlib.slide）

`uv run drawlib init project slide pitch -l en,ja -s google` でスライドプロジェクトを初期化すると、`pitch_src/<lang>/*.md` の連番 Markdown ファイル群から `1920×1080`（`16:9`）のマルチターゲット発表資料が生成されます。

- **2 層分離オーサリング（`::: block` と `::: note`）**:
  - **`::: block xy=(x, y) width=W height=H`**: 左上 `(0, 0)` 基準の `1920×1080` ピクセル座標でカード・2 カラム構成・`---` 区切り線・埋め込み ```` ```drawlib ```` 図面を配置します（図面側は `setup(width=W/10, height=H/10)` で縦横比を一致させます）。
  - **`::: note`**: 詳細な口頭スクリプトや技術背景を聴衆向け画面から分離し、同期型**発表者ビュー（`?presenter=1`、`P` / `S` キー）**および PowerPoint（`.pptx`）の発表者ノート欄へ自動格納します。
- **ランタイムスライド番号とプログレッシブビルド（`drawlib.slide`）**:
  - `from drawlib.slide import current_slide, draw_page_number, draw_section_header` により、コンパイル中のスライド番号 `current_slide.index`・総枚数 `current_slide.total`・整形文字列 `current_slide.text`（`"4 / 12"`）を参照でき、ページ番号バッジや複数スライドに跨がる段階ビルド、4 種類の章扉（`variant="split" | "centered" | "banner" | "minimal"`）を簡潔に実装できます。
  - スライド内のアニメーション図面には `anim_trigger=click anim_loop=once anim_pause=(1, 3)` を指定でき、クリックや `A` キーで任意のフレーム毎に一時停止・再開できます。

````markdown
::: block xy=(1700, 1010) width=140 height=30
```drawlib file=page.svg
from drawlib.slide import draw_page_number

draw_page_number()
```
:::

::: block xy=(80, 40) width=1760 height=60
# ゼロトラスト API ゲートウェイ展開計画
:::

::: block xy=(80, 140) width=720 height=820
## 主要マイルストーン

- **エッジ mTLS**: クライアント証明書による相互認証
- **JWT キャッシュ**: Redis によるミリ秒未満の検証
- **カナリア判定**: SLO 違反時の自動ロールバック

---

*現在の発表位置: スライド 3*
:::

::: block xy=(840, 140) width=1000 height=820
```drawlib file=gateway_stage_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.slide import current_slide
from drawlib.styles import Styles

clear()
setup(width=100, height=82)
rectangle(
    (50, 41),
    width=76,
    height=34,
    style=Styles.PrimaryFlat.patch(shape_r=2.5),
    text=f"ゲートウェイ構成 ({current_slide.text})",
    text_style=Styles.WhiteBold.patch(text_size=14.5),
)
save()
```
:::

::: note
左カラムの 3 つの要点を順に説明したあと、右図で `current_slide` が HTML・PDF・`.pptx` ビルド時に自動でページ番号を解決する仕組みを補足します。
:::
````

```drawlib align=center code=fold file=slide_anatomy_ja.png caption="図 12.2: 16:9 スライドデッキのコンパイル構造 — Markdown 原稿・ノートから HTML・ベクター PDF・編集可能 .pptx へ変換"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=158, height=62)

d = ArchitectureDiagram(
    node_style=Styles.DarkBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

src = d.add(
    NodeGroup(
        title="スライド原稿 (slide_src/<lang>/*.md)",
        width=48.0,
        height=52.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.2),
        text_style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
    ),
    xy=(2.0, 3.0),
)
b_stage = src.add(
    Node(
        "::: block & # 見出し\n(1920x1080 ステージ)",
        width=39.0,
        height=12.0,
        icon=PhosphorIcon.LAYOUT,
        icon_size=4.8,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(24.0, 39.5),
)
b_code = src.add(
    Node(
        "埋め込み drawlib 図面\n& current_slide",
        width=39.0,
        height=12.0,
        icon=PhosphorIcon.CODE,
        icon_size=4.8,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(24.0, 25.0),
)
b_note = src.add(
    Node(
        "::: note 発表台本\n(スピーカーノート)",
        width=39.0,
        height=12.0,
        icon=PhosphorIcon.NOTE,
        icon_size=4.8,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(24.0, 10.5),
)

compiler = d.add(
    Node(
        "Slide コンパイラ\n& Chromium DOM 計測",
        width=33.0,
        height=20.0,
        icon=PhosphorIcon.CPU,
        icon_size=5.6,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.8),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.2),
    ),
    xy=(75.5, 29.0),
)

out_html = d.add(
    Node(
        "16:9 HTML スライド\n(発表者ビュー & SVG)",
        width=41.0,
        height=13.0,
        icon=PhosphorIcon.PRESENTATION_CHART,
        icon_size=4.8,
        card_style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    ),
    xy=(131.5, 45.5),
)
out_pdf = d.add(
    Node(
        "16:9 ベクター PDF\n(slide_<lang>.pdf)",
        width=41.0,
        height=13.0,
        icon=PhosphorIcon.FILE_PDF,
        icon_size=4.8,
        card_style=Styles.Neutral.patch(shape_r=1.8),
    ),
    xy=(131.5, 29.0),
)
out_pptx = d.add(
    Node(
        "編集可能 .pptx 資料\n(ネイティブ図形 & ノート)",
        width=41.0,
        height=13.0,
        icon=PhosphorIcon.SLIDESHOW,
        icon_size=4.8,
        card_style=Styles.SecondaryNeutral.patch(shape_r=1.8),
    ),
    xy=(131.5, 12.5),
)

d.connect(src, compiler, routing="direct", padding=0.8)
j_mid = d.junction((101.5, 29.0))
j_top = d.junction((101.5, 45.5))
j_bot = d.junction((101.5, 12.5))
d.connect(compiler, j_mid, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_mid, j_top, arrow="-", routing="direct")
d.connect(j_mid, j_bot, arrow="-", routing="direct")
d.connect(j_top, out_html, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_mid, out_pdf, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_bot, out_pptx, arrow="->", routing="direct", padding=(0.0, 0.8))

d.draw(xy=(2.0, 2.0))
save()
```

### プロジェクト作成と HTML・PDF・編集可能 PowerPoint（`.pptx`）のビルド

生成された `slide` プロジェクトには、Web スライド・ベクター PDF に加えてネイティブ Microsoft PowerPoint 出力用のスクリプト（`build_pptx.sh`）が標準同梱されています。`drawlib build pptx` は `::: block` カード・テキスト枠・箇条書き・表・`::: note` 発表者ノートを編集可能な `960×540 pt` の PowerPoint オブジェクトへ変換し、図面を `240 DPI` の高精細画像として配置します。

```bash
# 1. 日英 2 言語対応の 16:9 スライドプロジェクトを初期化
uv run drawlib init project slide pitch -l en,ja -s google

# 2. インタラクティブ 16:9 HTML スライド + ベクター PDF + 画像アセットを一括ビルド
./pitch_src/build.sh

# 3. 編集可能な PowerPoint ファイル（pitch_en.pptx / pitch_ja.pptx）を出力
./pitch_src/build_pptx.sh
# 同等の CLI コマンド:
uv run drawlib build pptx pitch_src/ -o pitch.pptx -s pitch_src/styles.py -u pitch_src/utils.py
```
