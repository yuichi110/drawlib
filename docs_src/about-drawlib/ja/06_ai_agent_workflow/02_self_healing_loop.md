::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — コードで描く図解と技術ドキュメント*
:::

::: block xy=(80, 36) width=1760 height=72
# マルチモーダル視覚検証による自律修正ループ
:::

::: block xy=(80, 130) width=1760 height=115
- **オンデマンド仕様参照**: AIエージェント（Gemini・Claude Code・Cursor）が `drawlib rules show` で必要な知識のみを都度取得。
- **視覚的な自己修正ループ**: `drawlib show -g` の座標グリッド画像をマルチモーダル検品し、重なりや余白を自律修正して出力。
:::

::: block xy=(80, 260) width=1760 height=685
```drawlib file=ai_self_healing_loop_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=68)

# Upper 4-step pipeline + final verified exit card
steps = [
    {
        "x": 2.0,
        "w": 30.0,
        "header": "1. ルール参照",
        "cmd": "drawlib rules show",
        "desc": "必要なAPIと設計規約を\nオンデマンドで取得\nコンテキスト節約",
        "icon": phosphor.book_open,
        "featured": False,
    },
    {
        "x": 36.2,
        "w": 30.0,
        "header": "2. コード生成",
        "cmd": "Write Python / MD",
        "desc": "SmartArts・Diagramsと\n::: block 座標を\n型安全に記述",
        "icon": phosphor.code,
        "featured": False,
    },
    {
        "x": 70.4,
        "w": 30.0,
        "header": "3. グリッド描画",
        "cmd": "drawlib show -g",
        "desc": "(X, Y) 目盛り付きの\n検証用PNG画像を\n1秒未満で出力",
        "icon": phosphor.squares_four,
        "featured": False,
    },
    {
        "x": 104.6,
        "w": 32.0,
        "header": "4. 視覚検品",
        "cmd": "Multimodal 検査",
        "desc": "余白バランス・文字サイズ\n要素の重なり有無を\n画像認識で判定",
        "icon": phosphor.robot,
        "featured": True,
    },
]

card_y = 26.5
card_h = 39.0

for idx, s in enumerate(steps):
    x0 = s["x"]
    w = s["w"]
    cx = x0 + w / 2.0
    feat = s["featured"]

    p = Panel(
        s["header"],
        style=(Styles.PrimaryNeutral if feat else Styles.White).patch(shape_r=2.0),
        header_style=Styles.PrimaryFlat if feat else Styles.SecondaryNeutral,
        text_style=(Styles.WhiteBold if feat else Styles.DarkBold).patch(text_size=13.0),
        header_variant="filled",
        header_height=8.4,
        header_align="center",
    )
    p.draw(xy=(x0, card_y), width=w, height=card_h)

    circle(
        (cx, 50.2),
        radius=4.4,
        style=Styles.WhiteFlat if feat else Styles.PrimaryNeutral,
    )
    s["icon"]((cx, 50.2), width=5.0, style=Styles.PrimaryBold)

    rectangle(
        (cx, 41.2),
        width=w - 3.6,
        height=5.2,
        style=(Styles.PrimaryFlat if feat else Styles.Neutral).patch(shape_r=1.2),
    )
    text(
        (cx, 41.2),
        s["cmd"],
        style=(Styles.WhiteBold if feat else Styles.PrimaryBold).patch(text_size=10.8),
    )

    text((cx, 32.5), s["desc"], style=Styles.Dark.patch(text_size=10.8))

    if idx < 3:
        nx = steps[idx + 1]["x"]
        line((x0 + w + 0.3, 46.0), (nx - 0.3, 46.0), arrow_head="->", style=Styles.PrimaryBold)

# Exit arrow -> Verified Artifact card
line((136.9, 46.0), (143.7, 46.0), arrow_head="->", style=Styles.SuccessBold)
text((140.3, 49.2), "合格", style=Styles.SuccessBold.patch(text_size=11.0))

exit_x = 144.0
exit_w = 30.0
exit_cx = exit_x + exit_w / 2.0
exit_panel = Panel(
    "検品済み成果物",
    style=Styles.White.patch(shape_r=2.0),
    header_style=Styles.SuccessFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.0),
    header_variant="filled",
    header_height=8.4,
    header_align="center",
)
exit_panel.draw(xy=(exit_x, card_y), width=exit_w, height=card_h)
circle((exit_cx, 50.2), radius=4.6, style=Styles.SecondaryNeutral)
phosphor.check_circle((exit_cx, 50.2), width=5.4, style=Styles.SuccessBold)
rectangle((exit_cx, 41.2), width=26.2, height=5.2, style=Styles.SecondaryNeutral.patch(shape_r=1.2))
text((exit_cx, 41.2), "✓ 公開ビルド完了", style=Styles.DarkBold.patch(text_size=10.8))
text(
    (exit_cx, 32.5),
    "高品質なHTML・PDF\nWord・16:9 PPTXを\n一括コンパイル",
    style=Styles.Dark.patch(text_size=10.8),
)

# Step 5: Bottom Feedback Self-Correction Loop (4 -> 5 -> 2)
loop_x = 57.5
loop_w = 57.5
loop_y = 3.5
loop_h = 16.5
loop_cy = loop_y + loop_h / 2.0

# Orthogonal path from Step 4 bottom (123.5, 26.5) -> (115.0, 11.75)
line((123.5, 26.5), (123.5, loop_cy), style=Styles.WarningBold)
line((123.5, loop_cy), (loop_x + loop_w + 0.4, loop_cy), arrow_head="->", style=Styles.WarningBold)
text((126.5, 14.8), "重なり・見切れを検知", style=Styles.DarkBold.patch(text_size=10.8, halign="left"))

# Step 5 Card
rectangle((loop_x + loop_w / 2.0, loop_cy), width=loop_w, height=loop_h, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
circle((loop_x + 6.5, loop_cy), radius=4.2, style=Styles.WhiteFlat)
phosphor.arrows_clockwise((loop_x + 6.5, loop_cy), width=4.8, style=Styles.PrimaryBold)
text(
    (loop_x + 12.5, loop_cy + 3.2),
    "5. 座標・サイズの自己修正",
    style=Styles.DarkBold.patch(text_size=12.6, halign="left"),
)
text(
    (loop_x + 12.5, loop_cy - 2.6),
    "-g 目盛りから (x, y) とサイズを自動補正",
    style=Styles.Dark.patch(text_size=10.6, halign="left"),
)

# Orthogonal return path from Step 5 left (57.5, 11.75) -> Step 2 bottom (51.2, 26.5)
line((loop_x, loop_cy), (51.2, loop_cy), style=Styles.PrimaryBold)
line((51.2, loop_cy), (51.2, card_y - 0.4), arrow_head="->", style=Styles.PrimaryBold)
text((49.2, 17.5), "再検証", style=Styles.PrimaryBold.patch(text_size=11.0, halign="right"))

save()
```
:::

::: note
従来のGUI作図ツールや生のSVG/XML出力では、AIエージェントは文字の重なりや余白の崩れに気づけないまま不完全な図を出力してしまいます。
Drawlibは5段階の自律フィードバックループでこの課題を解決します。
1. **`drawlib rules show`**：膨大なプロンプトを常時読み込むのではなく、必要なコンポーネント規約だけをオンデマンドで取得します。
2. **Python / Markdown生成**：型付きAPIと `::: block` 座標で明快なコードを記述します。
3. **`drawlib show -g`**：`(X, Y)` 座標グリッドを重ねた検証用PNGを1秒未満でヘッドレス描画します。
4. **マルチモーダル視覚検品**：画像認識モデルで実際の描画結果を見て、文字サイズ・余白・はみ出しを検査します。
5. **座標の自己修正**：重なりが見つかれば `-g` の目盛りから正確な補正量を読み取って `(x, y)` を自動修正し、合格した図版だけを公開成果物へコンパイルします。
:::
