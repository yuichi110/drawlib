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
# 16:9 スライド・発表者ビュー・PPTX出力
:::

::: block xy=(80, 130) width=1760 height=115
- **2層構造のスライド記述**: `::: block` で `1920×1080` の視覚ステージを定義し、`::: note` に発表原稿をGit管理。
- **リアルタイム同期とOffice出力**: `?presenter=1` で2画面発表者ビューを `BroadcastChannel` 同期し、PDFと `.pptx` も出力。
:::

::: block xy=(80, 260) width=1760 height=685
```drawlib file=slide_dual_engine_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=68)

dots = (Styles.DangerFlat, Styles.WarningFlat, Styles.SuccessFlat)

# 1. Left Source Panel: slide_src/
src_panel = Panel(
    "slide_src/",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=13.8),
    icon=phosphor.code,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=8.8,
)
src_panel.draw(xy=(2.0, 4.0), width=37.0, height=61.0)

# Layer 1 box inside source
rectangle((20.5, 44.5), width=32.0, height=18.5, style=Styles.White.patch(shape_r=1.6))
phosphor.presentation_chart((8.0, 49.5), width=4.0, style=Styles.PrimaryBold)
text((11.5, 49.5), "::: block (画面)", style=Styles.PrimaryBold.patch(text_size=12.2, halign="left"))
text(
    (6.8, 41.2),
    "1920x1080 座標配置\nPythonベクターSVG",
    style=Styles.Dark.patch(text_size=11.0, halign="left"),
)

# Layer 2 box inside source
rectangle((20.5, 22.0), width=32.0, height=18.5, style=Styles.White.patch(shape_r=1.6))
phosphor.note((8.0, 27.0), width=4.0, style=Styles.SecondaryBold)
text((11.5, 27.0), "::: note (原稿)", style=Styles.DarkBold.patch(text_size=12.2, halign="left"))
text(
    (6.8, 18.7),
    "発表トーク原稿を管理\n聴衆画面には非表示",
    style=Styles.Dark.patch(text_size=11.0, halign="left"),
)

rectangle((20.5, 8.2), width=32.0, height=5.2, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
text((20.5, 8.2), "日英 1:1 パリティ検証", style=Styles.PrimaryBold.patch(text_size=10.6))

# Compiler routing lines
line((39.0, 45.5), (46.5, 45.5), arrow_head="->", style=Styles.PrimaryBold)
line((42.2, 45.5), (42.2, 12.8), style=Styles.PrimaryBold)
circle((42.2, 45.5), radius=0.9, style=Styles.PrimaryFlat)
line((42.2, 12.8), (46.5, 12.8), arrow_head="->", style=Styles.PrimaryBold)

# 2. Top-Center: Audience Stage Window
stage_win = Panel(
    "聴衆用ステージ画面",
    style=Styles.White.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=13.0),
    dot_styles=dots,
    header_variant="window",
    header_height=8.2,
)
stage_win.draw(xy=(46.5, 25.5), width=53.0, height=39.5)

rectangle((73.0, 46.5), width=48.0, height=16.5, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.sparkle((55.0, 46.5), width=5.0, style=Styles.PrimaryBold)
text(
    (60.2, 48.8),
    "インライン ベクターSVG",
    style=Styles.DarkBold.patch(text_size=12.2, halign="left"),
)
text(
    (60.2, 43.5),
    "4K投影でも鮮明な1920x1080",
    style=Styles.Dark.patch(text_size=10.6, halign="left"),
)

rectangle((61.0, 31.8), width=24.0, height=6.6, style=Styles.Neutral.patch(shape_r=1.2))
text((61.0, 31.8), "Lキー: EN ⇄ JA", style=Styles.PrimaryBold.patch(text_size=11.0))
rectangle((86.2, 31.8), width=21.5, height=6.6, style=Styles.Neutral.patch(shape_r=1.2))
text((86.2, 31.8), "Pキー: 発表者用", style=Styles.DarkBold.patch(text_size=11.0))

# 3. BroadcastChannel Bidirectional Sync
line((99.8, 45.2), (116.2, 45.2), arrow_head="<->", style=Styles.PrimaryBold)
rectangle((108.0, 51.8), width=15.2, height=8.2, style=Styles.PrimaryFlat.patch(shape_r=1.6))
text((108.0, 53.6), "Broadcast", style=Styles.WhiteBold.patch(text_size=11.0))
text((108.0, 49.8), "Channel", style=Styles.White.patch(text_size=10.8))

# 4. Top-Right: Presenter Console (?presenter=1)
pres_win = Panel(
    "発表者ビュー (?presenter=1)",
    style=Styles.PrimaryNeutral.patch(shape_r=2.2),
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=12.8),
    dot_styles=dots,
    header_variant="window",
    header_height=8.2,
)
pres_win.draw(xy=(116.5, 25.5), width=57.5, height=39.5)

# Current / Next thumbnails + Timer
rectangle((130.8, 49.2), width=23.5, height=11.2, style=Styles.White.patch(shape_r=1.2))
text((130.8, 51.2), "現在のスライド", style=Styles.PrimaryBold.patch(text_size=11.0))
text((130.8, 46.8), "Slide 18 / 26", style=Styles.Muted.patch(text_size=10.5))

rectangle((157.8, 49.2), width=25.0, height=11.2, style=Styles.White.patch(shape_r=1.2))
text((157.8, 51.2), "次のスライド", style=Styles.DarkBold.patch(text_size=11.0))
text((157.8, 46.8), "タイマー 08:42", style=Styles.PrimaryBold.patch(text_size=10.5))

# Speaker Notes Pane
rectangle((145.2, 34.0), width=52.5, height=13.5, style=Styles.White.patch(shape_r=1.4))
phosphor.note((123.2, 36.2), width=3.8, style=Styles.PrimaryBold)
text(
    (126.8, 36.4),
    "::: note スピーカーノート表示",
    style=Styles.DarkBold.patch(text_size=11.5, halign="left"),
)
text(
    (126.8, 31.6),
    "発表原稿・想定Q&Aを同期表示",
    style=Styles.Muted.patch(text_size=10.6, halign="left"),
)

# 5. Bottom Offline & Office Export Strip
rectangle((110.2, 12.8), width=127.5, height=17.6, style=Styles.Neutral.patch(shape_r=2.0))

# Left export: Vector PDF
rectangle((78.5, 12.8), width=59.5, height=13.2, style=Styles.White.patch(shape_r=1.5))
phosphor.file_pdf((54.0, 12.8), width=5.0, style=Styles.PrimaryBold)
text((58.5, 15.2), "1920x1080 ベクターPDF", style=Styles.DarkBold.patch(text_size=12.5, halign="left"))
text((58.5, 10.2), "drawlib build pdf  •  配布用PDF", style=Styles.Muted.patch(text_size=10.8, halign="left"))

# Right export: Editable PPTX
rectangle((141.8, 12.8), width=59.5, height=13.2, style=Styles.White.patch(shape_r=1.5))
phosphor.presentation((117.2, 12.8), width=5.0, style=Styles.PrimaryBold)
text((121.8, 15.2), "編集可能 960x540pt .pptx", style=Styles.DarkBold.patch(text_size=12.5, halign="left"))
text((121.8, 10.2), "drawlib build pptx  •  ノート付PPTX", style=Styles.Muted.patch(text_size=10.8, halign="left"))

save()
```
:::

::: note
ご覧いただいているこのスライド自体も `type = "slide"` で構築されています。
各Markdownファイルは2層構造になっており、`::: block` で `1920×1080` ステージ上の座標とPythonベクター図解を定義し、`::: note` に発表用のトークスクリプトを記述してGitで一元管理します。
登壇時には `P` キー（または `?presenter=1`）で発表者ビューを開くと、ブラウザの `BroadcastChannel` を介して聴衆画面とリアルタイム同期し、現在・次のスライド、経過タイマー、`::: note` の原稿を確認しながら発表できます。さらに `L` キー1つで日本語・英語を即座に切り替えられます。
オフライン配布が必要な場面でも、`drawlib build pdf` で高精細なベクターPDF、`drawlib build pptx` でテキストやスピーカーノートまでネイティブ編集可能な `960×540pt` PowerPointファイルを出力できます。
:::
