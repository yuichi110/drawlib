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
# プロセス・サイクル・ロードマップ
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=process_cycle_roadmap_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import ChevronProcess, Cycle, Panel, Roadmap
from drawlib.styles import Styles

clear()
setup(width=176, height=81)

# 1. Top Wide Panel: ChevronProcess
p_top = Panel(
    "ChevronProcess — 段階的ビルド・配信パイプライン",
    "4ステージ工程",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.5),
    icon=phosphor.arrow_right,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_top.draw((1.5, 53.0), width=173.0, height=26.5)
t_xy, t_w, t_h = p_top.get_content_box((1.5, 53.0), width=173.0, height=26.5, padding=(3.5, 2.6))

proc = ChevronProcess(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=12.5),
    description_style=Styles.Muted.patch(text_size=11.0),
    corner_angle=62.0,
    spacing=2.0,
    flat_left_end=True,
)
proc.add("1. Author", description="MD + Python 記述", style=Styles.PrimaryNeutral)
proc.add(
    "2. Render -g",
    description="グリッド視覚検証",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=12.5),
    description_style=Styles.White.patch(text_size=11.0),
)
proc.add("3. Cache", description="SQLite 差分キャッシュ", style=Styles.SecondaryNeutral)
proc.add("4. Publish", description="HTML / PDF / PPTX", style=Styles.White)
proc.draw(t_xy, width=t_w, height=t_h)

# 2. Bottom-Left Panel: Cycle with CycleCenter
p_bl = Panel(
    "Cycle — 自律改善ループ",
    "4ノード円軌道",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.5),
    icon=phosphor.arrows_clockwise,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_bl.draw((1.5, 1.5), width=84.5, height=49.0)
c_xy, _, _ = p_bl.get_content_box(
    (1.5, 1.5), width=84.5, height=49.0, padding=(3.0, 2.0), content_align="center"
)

cyc = Cycle(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=11.8),
    description_style=Styles.Muted.patch(text_size=10.5),
    arrow_style=Styles.PrimaryBold,
    clockwise=True,
    start_angle=135.0,
    node_shape="rectangle",
    node_width=20.5,
    node_height=8.0,
    arrow_type="arc",
    arrow_width=1.4,
    arrow_head_width=3.6,
    arrow_color_mode="monochrome",
    arrow_gap=2.2,
)
cyc.add(
    "1. 記述",
    description="API 実装",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.8),
    description_style=Styles.White.patch(text_size=10.5),
)
cyc.add("2. 検証", description="show -g", style=Styles.PrimaryNeutral)
cyc.add("3. 調整", description="座標補正", style=Styles.SecondaryNeutral)
cyc.add("4. 確定", description="Git 管理", style=Styles.White)
cyc.set_center(
    "AI ループ",
    description="自己修復",
    radius=7.0,
    style=Styles.DarkFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.5),
    description_style=Styles.White.patch(text_size=10.2),
)
cyc.draw(c_xy, radius=18.2, align="center")

# 3. Bottom-Right Panel: Roadmap
p_br = Panel(
    "Roadmap — マイルストーン工程",
    "曲線スパイン",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.5),
    icon=phosphor.git_branch,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_br.draw((90.0, 1.5), width=84.5, height=49.0)
r_xy, r_w, r_h = p_br.get_content_box((90.0, 1.5), width=84.5, height=49.0, padding=(3.5, 2.0))

rm = Roadmap(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=11.6),
    description_style=Styles.Muted.patch(text_size=10.5),
    spine_style=Styles.PrimaryBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=11.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.14,
    card_shape="rounded_rect",
    spacing=2.2,
)
rm.add("ベクター描画基盤", "図形プリミティブ・アイコン・テーマ", badge_text="P1", icon=phosphor.pencil_simple)
rm.add(
    "SmartArts・標準チャート",
    "18種の構造化図解と10種のグラフ",
    badge_text="P2",
    icon=phosphor.chart_bar,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=11.0),
)
rm.add("ダイアグラム・自動配置", "6種の図解エンジンとレイアウト計算", badge_text="P3", icon=phosphor.tree_structure)
rm.add("マルチ形式ビルドとCLI", "HTML・PDF・PPTX出力とAIルール", badge_text="P4", icon=phosphor.rocket_launch)
rm.draw(r_xy, width=r_w, height=r_h)

save()
```
:::

::: note
このスライドでは、`Panel`（`get_content_box`）を用いて3つのフロー・時系列系 SmartArts を1枚のキャンバス上に統合しています。
- **上部（`ChevronProcess`）**: CI/CD パイプラインやドキュメントのビルド工程（`1. Author` → `2. Render -g` → `3. Cache` → `4. Publish`）など、一方向の段階的プロセスを連結シェブロンで自動配置します。
- **左下（`Cycle` + `CycleCenter`）**: 円軌道上のステップと曲線矢印、さらに中央ハブ（`AI ループ`）を組み合わせ、PDCA や自律検証ループを明快に可視化します。
- **右下（`Roadmap`）**: ベジェ曲線または直線スパイン上のフェーズバッジとアイコン付きマイルストーンカードを連動させ、リリース計画や移行フェーズを表現します。
:::
