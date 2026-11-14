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
# 宣言的な棒・折れ線・面チャート
:::

::: block xy=(80, 140) width=620 height=800
```drawlib file=chart_kpis_ja.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=62, height=80)
utils.draw_kpi_cards(
    [
        ("10", "標準内蔵チャート", "棒・箱ひげ・折れ線・面・円\nレーダー・散布・熱図・ガント"),
        ("100%", "テーマ完全同期", "Default / Google / Monochrome\n各パレットへ自動追従"),
        ("Auto", "目盛の自動最適化", "見やすい軸目盛・独立凡例と\ndraw_ratio アニメーション"),
    ],
    width=62,
    height=80,
)
save()
```
:::

::: block xy=(740, 140) width=1100 height=800
```drawlib file=bar_line_showcase_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.area import AreaChart
from drawlib.charts.bar import BarChart
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=110, height=80)

# 1. Top Panel: Grouped BarChart (Throughput across Q1-Q4)
p_top = Panel(
    "BarChart — 四半期別レンダリング処理量 (k/時)",
    "グループ棒",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.8),
    description_style=Styles.Muted.patch(text_size=12.0),
    icon=phosphor.chart_bar,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_top.draw((1.5, 41.5), width=107.0, height=37.0)

bar = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=100.0,
    height=26.5,
    orientation="vertical",
    bar_mode="group",
    bar_width_ratio=0.68,
    bar_r=0.9,
    axis_text_style=Styles.Dark.patch(text_size=13.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=12.5),
    value_format="{:.0f}k",
)
bar.add_series("v1 逐次実行", [18.0, 21.0, 24.0, 27.0], style=Styles.SecondaryNeutral)
bar.add_series("v2 キャッシュ並列", [34.0, 46.0, 61.0, 76.0], style=Styles.PrimaryFlat)
bar.configure_y_axis(min_value=0.0, max_value=100.0, tick_step=25.0, unit="k")
bar.draw(xy=(4.5, 43.2))
bar.draw_legend(
    xy=(54.0, 68.8),
    text_style=Styles.DarkBold.patch(text_size=12.5),
    orientation="horizontal",
    item_gap=4.5,
)

# 2. Bottom Panel: Smooth Multi-Series AreaChart (Latency p50 / p99 Trend)
p_bot = Panel(
    "AreaChart — ビルド遅延の推移 (p50 vs p99)",
    "平滑スプライン",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.8),
    description_style=Styles.Muted.patch(text_size=12.0),
    icon=phosphor.chart_line_up,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_bot.draw((1.5, 1.5), width=107.0, height=37.0)

area = AreaChart(
    axis_line_style=Styles.MutedDashed,
    categories=["v1.0", "v1.2", "v1.4", "v1.6", "v2.0"],
    width=100.0,
    height=26.5,
    mode="overlap",
    fill_alpha=0.24,
    smooth=True,
    show_points=True,
    point_shape="circle",
    point_size=0.75,
    axis_text_style=Styles.Dark.patch(text_size=13.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=12.5),
)
area.add_series(
    "p99 テール遅延",
    [50.0, 42.0, 34.0, 28.0, 23.0],
    style=Styles.PrimaryFlat,
    line_width=2.2,
)
area.add_series(
    "p50 中央値",
    [19.0, 15.0, 12.0, 9.0, 6.0],
    style=Styles.SecondaryFlat,
    line_width=2.0,
    line_style="dashed",
    point_shape="square",
)
area.configure_y_axis(min_value=0.0, max_value=60.0, tick_step=20.0, unit="ms")
area.draw(xy=(4.5, 3.2))
area.draw_legend(
    xy=(54.0, 28.8),
    text_style=Styles.DarkBold.patch(text_size=12.5),
    orientation="horizontal",
    item_gap=4.5,
)

save()
```
:::

::: note
`drawlib.charts` は外部プロット用ツールに依存せず、純 Python でベクターグラフをキャンバスへ直接描画します。
- 左側の `KpiCards` が示す通り、10種類の内蔵チャートクラス、`Default`・`Google`・`Monochrome` テーマとの100%パレット同期、そしてキリの良い数値を自動計算する Nice-Number 軸目盛（`1, 2, 5 × 10^k`）と `draw_ratio` アニメーション制御を標準搭載しています。
- 右側の上段ではグループ化 `BarChart` で四半期ごとの処理スループットを比較し、下段では平滑スプライン `AreaChart` で p50 中央値と p99 テール遅延の改善推移を視覚化しています。
:::
