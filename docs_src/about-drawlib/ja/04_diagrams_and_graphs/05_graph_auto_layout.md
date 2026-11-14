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
# 自動座標ソルバー (drawlib.graph)
:::

::: block xy=(80, 145) width=680 height=790
## 自動配置と手動微調整のハイブリッド

- **自動座標計算**: `get_layout()` で交差のない `(x, y)` を算出
- **手動微調整**: `offset(dx, dy)` でブラックボックス化を回避
- **確定座標の出力**: `print(layout)` で座標を確認しコード固定

```python
g = LayerGraph(direction="LR")
g.edge("ingest", "validate")
g.edge("validate", "serve")
layout = g.get_layout(margin=8.0)
layout.offset("serve", dy=-4.0)
```
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=graph_hybrid_workflow_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.flow import End, FlowDiagram, Process, Start
from drawlib.graph import LayerGraph
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=80)

panel = Panel(
    "LayerGraph.get_layout() + offset()",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.0),
    icon=phosphor.graph,
    icon_style=Styles.PrimaryBold,
    header_height=9.0,
)
panel.draw((2.0, 2.0), width=100.0, height=76.0)

# Step 1: Solve crossing-minimized DAG coordinates via LayerGraph
g = LayerGraph(direction="LR", default_node_width=21.0, default_node_height=12.0)
g.tier("src", ["ingest"], layer=0)
g.tier("etl", ["validate", "enrich"], layer=1)
g.tier("out", ["serve"], layer=2)
g.cluster("stage", ["validate", "enrich"], padding=4.5, header_height=4.5)

g.edge("ingest", "validate")
g.edge("ingest", "enrich")
g.edge("validate", "serve")
g.edge("enrich", "serve")

layout = g.get_layout(width=94.0, height=58.0, margin=5.0).offset("serve", dy=-4.0)
ox, oy = 5.0, 5.0


def pt(xy: tuple[float, float]) -> tuple[float, float]:
    return (xy[0] + ox, xy[1] + oy)


# Step 2: Render stage cluster, FlowDiagram nodes, and offset() callout badge
stg = layout["stage"]
rectangle(pt(stg.xy), width=stg.width, height=stg.height, style=Styles.MutedDashed.patch(shape_r=2.0))
text(
    (stg.left + ox + 2.0, stg.top + oy - 2.6),
    "ETL ステージ",
    style=Styles.DarkBold.patch(text_size=13.5, halign="left"),
)

flow = FlowDiagram(
    node_style=Styles.Neutral.patch(text_size=13.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=13.5),
)
n_in = flow.add(
    Start("データ収集", width=21, height=11, style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=13.5)),
    xy=pt(layout["ingest"].xy),
)
n_val = flow.add(
    Process("スキーマ検証", width=21, height=12, style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=13.5)),
    xy=pt(layout["validate"].xy),
)
n_enr = flow.add(
    Process("特徴量付与", width=21, height=12, style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=13.5)),
    xy=pt(layout["enrich"].xy),
)
n_srv = flow.add(
    End("推論 API", width=22, height=12, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=14.0)),
    xy=pt(layout["serve"].xy),
)

flow.connect(n_in, n_val, start_side="right", end_side="left", padding=0.8)
flow.connect(n_in, n_enr, start_side="right", end_side="left", padding=0.8)
flow.connect(n_val, n_srv, start_side="right", end_side="left", padding=0.8)
flow.connect(n_enr, n_srv, start_side="right", end_side="left", padding=0.8)
flow.draw()

srv_xy = pt(layout["serve"].xy)
rectangle(
    (srv_xy[0], srv_xy[1] + 12.5),
    width=23.0,
    height=6.8,
    style=Styles.WarningNeutral.patch(shape_r=1.8),
    text="offset(dy=-4)",
    text_style=Styles.DarkBold.patch(text_size=13.5),
)
save()
```
:::

::: note
**`drawlib.graph` による自動座標計算と手動微調整のハイブリッド設計**:
- Graphviz や Mermaid などの従来の自動レイアウトツールは「描画まで一体化したブラックボックス」であるため、特定のノードだけを少しずらしたり注釈スペースを空けたりすることが困難でした。一方で、大規模な DAG やツリー構造の全座標を手計算するのも手間がかかります。
- **`drawlib.graph` は「純粋な座標計算機」としてこのジレンマを解消します**:
  1. **Step 1 (`get_layout()`)**: ノード・エッジ・クラスタを宣言して `get_layout()` を呼ぶだけで、交差を最小化したノード中心座標（`.xy`）やクラスタ境界、配線ポートを自動算出します。
  2. **Step 2 (`offset()` + 自由な描画)**: 算出後に `layout.offset("serve", dy=-4.0)` で任意のノードを微調整したり、`print(layout)` で確定座標を確認して `FlowDiagram` や `ArchitectureDiagram` にそのまま流し込めます。
:::
