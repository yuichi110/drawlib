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
# 既存ツールとの機能比較マトリクス
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=comparison_table_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles

clear()
setup(width=176, height=82)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=12.6),
    header_cell_style=Styles.DarkFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=13.8),
    border_style=Styles.MutedThin,
    has_header=True,
)

table.set_style_cell_evenodd(
    even_color=Colors.Neutral,
    even_text_style=Styles.Dark.patch(text_size=12.6),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=12.6),
)

table.set_style_cell_rowheader(
    background_color=Colors.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.5),
)

table.set_style_cell(
    background_color=Colors.PrimaryNeutral,
    text_style=Styles.PrimaryBold.patch(text_size=12.8),
    rows=[1, 2, 3, 4, 5, 6],
    columns=[4],
)

table.set_style_cell_header(
    background_color=Colors.Dark,
    text_style=Styles.WhiteBold.patch(text_size=13.8),
)

table.set_style_cell(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=14.5),
    rows=[0],
    columns=[4],
)

table.set_style_border(
    top=Styles.DarkBold.patch(line_width=1.8),
    top2=Styles.DarkBold.patch(line_width=1.4),
    bottom=Styles.DarkBold.patch(line_width=1.8),
    left2=Styles.Muted.patch(line_width=1.0),
    between_columns=Styles.MutedThin.patch(line_color=Colors.Gray3, line_width=0.7),
    between_rows=Styles.MutedThin.patch(line_color=Colors.Gray3, line_width=0.7),
)

data = [
    ["評価軸", "GUI ツール", "テキスト DSL", "グラフ描画系", "Drawlib"],
    ["Git 差分・PR レビュー", "× バイナリ不可", "✓ テキスト管理", "✓ Python コード", "✓ 明快な Python"],
    ["空間座標の精密制御", "✓ 手動ドラッグ", "× 自動配置のみ", "△ グラフ軸のみ", "✓ 座標指定＋自動"],
    ["クラウド構成図・UML", "✓ 手動アイコン", "△ 簡易ボックス", "× 非対応", "✓ 6種エンジン内蔵"],
    ["チャート・情報図解", "△ 手動で作図", "× ごく一部のみ", "✓ 統計図のみ", "✓ Charts & SmartArts"],
    ["Site / Catalog / Slide / Office", "× 画像書き出し", "× 図単体のみ", "× 画像出力のみ", "✓ 5型マルチ出力"],
    ["AI 視覚自己検証 (-g)", "× GUI 操作必須", "× 座標調整不可", "△ 個別実装のみ", "✓ 標準 -g CLI"],
]

table.draw_flexible(
    xy=(3.0, 77.5),
    column_widths=[46.0, 28.5, 28.5, 28.5, 38.5],
    row_heights=[11.0, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4],
    data=data,
    align="top_left",
)
save()
```
:::

::: note
この比較マトリクスは、6つの実務的な評価軸で既存ツールと Drawlib を対比したものです。
GUIホワイトボードは自由な手動配置ができるものの、Git差分レビューや多形式コンパイル、AIによる自律編集には不向きです。
Mermaid などのテキストDSLはGit管理しやすい反面、細かな座標制御や情報図解、ドキュメント・スライドの一括出力ができません。
また Matplotlib などのプロット系ライブラリは統計グラフ専用であり、クラウド構成図やUML、Web・Office出力を備えていません。
Drawlib は、明快なPythonコード、精密な座標制御と自動レイアウトの両立、6種の構成図エンジン、ChartsとSmartArts、5つのプロジェクト型による多形式出力、そして `-g` オプションによるAI視覚自己検証ループをすべて単一基盤で提供します。
:::
