# 11. 自動グラフレイアウトソルバー（drawlib.graph）

ノード数が増えるにつれて `(x, y)` 座標を手作業で管理するのは煩雑になりますが、ブラックボックス型の自動描画ツールではアイコンやフォント、デザインシステム（`Styles`）の細かな制御が失われます。`drawlib.graph` は**純粋かつ決定論的な座標計算ソルバー**としてこの課題を解決します。ノード・クラスタ・エッジの接続関係だけを宣言して `layout = g.get_layout(...)` で座標を算出し、Drawlib の任意の描画コンポーネントへ渡すことで「自動配置」と「完全な表現力」を両立します。

```drawlib align=center code=fold file=layer_graph_dag_ja.png caption="図 11.1: LayerGraph.get_layout() で座標解決しスタイル付きカードへ描画したデータ基盤 DAG パイプライン"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.icons import phosphor
from drawlib.lines import lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=78)

# ステップ 1: DAG トポロジーを宣言し決定論的な座標を算出
g = LayerGraph(direction="LR", default_node_width=34.0, default_node_height=14.5)
g.node("ingest", layer=0)
g.tier("processing", ["transform", "validate"], layer=1)
g.cluster("etl_stage", ["transform", "validate"], padding=5.0, header_height=4.5)
g.tier("serving", ["feature", "warehouse"], layer=2)

g.edge("ingest", "transform")
g.edge("ingest", "validate")
g.edge("transform", "feature")
g.edge("transform", "warehouse")
g.edge("validate", "warehouse")

layout = g.get_layout(margin=13.0)

# ステップ 2: 算出されたクラスタ境界・直交エッジ・ノードカードを描画
stage = layout["etl_stage"]
rectangle(stage.xy, width=stage.width, height=stage.height, style=Styles.MutedDashed.patch(shape_r=2.2))
text(
    (stage.left + 2.5, stage.top - 2.8),
    "ストリーム処理層",
    style=Styles.DarkBold.patch(halign="left", text_size=10.2),
)

for edge in layout.edges:
    lines(edge.points, arrow_head="->", style=Styles.DarkBold)

cards = [
    ("ingest", "イベント収集", "Kafka / PubSub", Styles.Neutral, Styles.DarkBold, Styles.Dark, phosphor.cloud_arrow_up),
    ("transform", "ストリーム変換", "Stateful Flink", Styles.PrimaryFlat, Styles.WhiteBold, Styles.White, phosphor.lightning),
    ("validate", "スキーマ検証", "品質ゲート", Styles.PrimaryNeutral, Styles.DarkBold, Styles.Dark, phosphor.shield_check),
    ("feature", "特徴量ストア", "低遅延 KV 配信", Styles.SecondaryNeutral, Styles.DarkBold, Styles.Dark, phosphor.cpu),
    ("warehouse", "分析用 DWH", "列指向 SQL", Styles.Neutral, Styles.DarkBold, Styles.Dark, phosphor.database),
]

for nid, title, sub, card_st, title_st, sub_st, icon_fn in cards:
    n = layout[nid]
    rectangle(n.xy, width=n.width, height=n.height, style=card_st.patch(shape_r=1.8))
    icon_fn((n.x - 11.5, n.y), width=4.8, style=title_st)
    text((n.x + 2.2, n.y + 2.4), title, style=title_st.patch(text_size=10.5))
    text((n.x + 2.2, n.y - 2.8), sub, style=sub_st.patch(text_size=10.0))

save()
```

---

## 11.1 2 段階レイアウト設計と座標取得（get_layout）

`drawlib.graph` は**それ自体には `.draw()` メソッドや色・フォント属性を持たず**、「幾何計算」と「視覚レンダリング」を明確な 2 段階に分離します。

1. **トポロジー宣言と座標解決（`layout = g.get_layout(...)`）**: ノード（`g.node("id", width=..., height=...)`）、有向エッジ（`g.edge("src", "dst")`）、およびグループ境界（`g.cluster("id", nodes=[...], padding=..., header_height=...)`）を登録し、`g.get_layout(width=..., height=..., margin=10.0)` を呼び出して `GraphLayout` オブジェクト（`layout["id"]` で辞書参照可能）を取得します。
2. **自由なビジュアル描画**: 解決済みの座標を `ArchitectureDiagram`・`FlowDiagram`・`SmartArts`・基本図形（`shapes` / `icons` / `lines`）へ渡して描画します。
   - **中心座標（`.xy` と `.local_xy`）**: `NodeLayout` と `ClusterLayout` はグローバル中心 `.xy`（`(cx, cy)`）を公開しており、`rectangle()`・`circle()`・`FlowDiagram`・トップレベルの `ArchitectureDiagram` ノードへそのまま渡せます。また親クラスタ左下基準の相対中心 `.local_xy` は `NodeGroup` 内の子ノード配置に対応します。
   - **左下コーナー座標（`.bottom_left` と `.local_bottom_left`）**: 左下アンカーを採用するトップレベル `NodeGroup(..., xy=cl.bottom_left)`、入れ子の `parent_grp.add(NodeGroup(...), xy=cl.local_bottom_left)`、`SmartArts`、`Charts` へ直接渡せます。
   - **エッジ経路ポリライン（`edge.points`, `edge.src_port`, `edge.dst_port`, `edge.mid_xy`）**: `layout.edges` の各 `EdgeLayout` はノード境界にスナップ済みのポート座標と直交ウェイポイント列を保持し、`lines(edge.points, arrow_head="->")` で即座に結線できます。
   - **座標の出力固定と微調整（`print(layout)` & `layout.offset()`）**: 自動配置をベースに手動調整コードへ移行したい場合は、`print(layout)`（`str(layout)`）を実行すると全クラスタ・ノードの `.xy` / `.bottom_left`・エッジ経路が一覧出力され、明示的な Python 作図コードの雛形として転記できます。また `layout.offset("node_id", dx=0.0, dy=-5.0)` を使えば、接続エッジのポート座標を自動追従させたまま特定ノードだけを平行移動できます。

---

## 11.2 5 種類のグラフレイアウトソルバーの使い分け

`drawlib.graph` には `BaseGraph` を継承した 5 つの専用ソルバーが用意されており、システムの構造特性に応じて最適なアルゴリズムを選択できます。

| ソルバークラス | レイアウトアルゴリズム | 主な構築ヘルパー | 最適なアーキテクチャ用途 |
| :--- | :--- | :--- | :--- |
| **`ArchitectureGraph`** | 2 階層マクロ／ミクロ箱詰め＋5 方位コンパス配置 | `g.group()`, `g.cluster(..., parent=..., pos="left"\|"center"\|..., order=...)` | マルチゾーン VPC、入れ子サブネット、クラウド構成図（`ArchitectureDiagram` 連携） |
| **`LayerGraph`** | Sugiyama 階層型 DAG（閉路除去・最長経路ランク・交差最小化） | `g.tier(name, nodes, layer=...)`, `g.cluster()`, `direction="LR"\|"TB"` | ETL／データ系譜パイプライン、CI/CD ステージ、依存関係 DAG |
| **`TreeGraph`** | Reingold-Tilford / Buchheim 対称コンパクト木配置 | `g.child(parent, child_id)`, `root=...`, `direction="TB"\|"LR"` | 組織図、構文木（AST）、障害木、厳密な単一親ツリー |
| **`RadialGraph`** | 同心円 BFS リング＋部分木重み付き角度配分 | `g.spoke(parent, spoke_id, ring=...)`, `hub=...`, `layout.ring_radii` | イベントメッシュ、Pub/Sub ハブ＆スポーク、API エコシステム図 |
| **`GridGraph`** | 2 次元 `(row, col)` マトリクス配置＋チャネル回廊配線 | `g.cell(id, row=..., col=...)`, `g.cluster_row()`, `g.cluster_column()`, `edge_routing="smart"` | サービスカタログ、状態マトリクス、均等グリッド構成図 |

---

## 11.3 階層ツリー（TreeGraph）と放射状トポロジー（RadialGraph）

直線的なパイプライン以外の階層構造やブローカー中心のネットワークでは、`TreeGraph` と `RadialGraph` が三角関数や部分木幅のバランス計算を自動化します。

- **`TreeGraph`**: 単一親・非巡回の木構造制約を厳密に検証し（ダイヤモンド型 DAG が誤って渡された場合は `ValueError` で通知）、親ノードを子ノード群の中央に美しく揃えて直交ステップ線（`edge_routing="orthogonal"`）または直線（`"straight"`）を生成します。
- **`RadialGraph`**: 中心ノード `hub` を `ring=0` に据え、接続スポークを同心円リング（`ring=1, 2, ...`）へ均等配分します。算出された各リングの半径は `layout.ring_radii: dict[int, float]` に格納されるため、破線の軌道ガイド円（`circle(hub.xy, radius=r, style=Styles.MutedDashed)`）を寸分の狂いなく重ねられます。

```drawlib align=center code=fold file=tree_or_radial_graph_ja.png caption="図 11.2: 非線形トポロジーの自動配置 — 対称階層 TreeGraph（左）と同心円 RadialGraph イベントメッシュ（右）"
from drawlib.canvas import save, setup
from drawlib.graph import RadialGraph, TreeGraph
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=160, height=78)

# 左パネル: TreeGraph（階層タクソノミー）
rectangle((41, 39), width=74, height=68, style=Styles.MutedDashed.patch(shape_r=2.2))
phosphor.tree_structure((9.5, 68.0), width=4.2, style=Styles.DarkBold)
text(
    (13.5, 68.0),
    "TreeGraph: 基盤階層ツリー",
    style=Styles.DarkBold.patch(text_size=11.0, halign="left"),
)

tg = TreeGraph(root="root", direction="TB", sibling_sep=3.2, default_node_width=16.5, default_node_height=9.0)
tg.node("root", width=22.5, height=9.5)
tg.child("root", "compute", width=19.5, height=9.0)
tg.child("root", "data", width=19.5, height=9.0)
tg.child("compute", "k8s", width=16.5, height=9.0)
tg.child("compute", "jobs", width=16.5, height=9.0)
tg.child("data", "sql", width=16.5, height=9.0)

t_layout = tg.get_layout(width=60.0, height=52.0, margin=4.0)
ox1, oy1 = 11.0, 7.0

for e in t_layout.edges:
    pts = [(px + ox1, py + oy1) for px, py in e.points]
    lines(pts, arrow_head="->", style=Styles.DarkBold)

tree_nodes = [
    ("root", "クラウド基盤", Styles.PrimaryFlat, Styles.WhiteBold),
    ("compute", "計算リソース層", Styles.PrimaryNeutral, Styles.DarkBold),
    ("data", "データ永続層", Styles.SecondaryNeutral, Styles.DarkBold),
    ("k8s", "GKE クラスタ", Styles.Neutral, Styles.DarkBold),
    ("jobs", "バッチ実行", Styles.Neutral, Styles.DarkBold),
    ("sql", "Cloud SQL", Styles.Neutral, Styles.DarkBold),
]
for nid, label, st, txt_st in tree_nodes:
    n = t_layout[nid]
    rectangle(
        (n.x + ox1, n.y + oy1),
        width=n.width,
        height=n.height,
        style=st.patch(shape_r=1.6),
        text=label,
        text_style=txt_st.patch(text_size=10.0),
    )

# 右パネル: RadialGraph（ハブ＆スポーク）
rectangle((119, 39), width=74, height=68, style=Styles.MutedDashed.patch(shape_r=2.2))
phosphor.share_network((87.5, 68.0), width=4.2, style=Styles.DarkBold)
text(
    (91.5, 68.0),
    "RadialGraph: 放射状メッシュ",
    style=Styles.DarkBold.patch(text_size=11.0, halign="left"),
)

rg = RadialGraph(
    hub="hub",
    center=(35.0, 26.5),
    radius_step=22.0,
    start_angle=18.0,
    default_node_width=17.5,
    default_node_height=8.5,
)
rg.node("hub", width=15.0, height=15.0)
for sid in ["auth", "orders", "billing", "notify", "search"]:
    rg.spoke("hub", sid)

r_layout = rg.get_layout(width=70.0, height=54.0, margin=4.0)
ox2, oy2 = 84.0, 7.0
hub_n = r_layout["hub"]
hub_xy = (hub_n.x + ox2, hub_n.y + oy2)

for r in r_layout.ring_radii.values():
    circle(hub_xy, radius=r, style=Styles.MutedDashed)

for e in r_layout.edges:
    sp = (e.src_port[0] + ox2, e.src_port[1] + oy2)
    dp = (e.dst_port[0] + ox2, e.dst_port[1] + oy2)
    line(sp, dp, arrow_head="->", style=Styles.DarkBold)

circle(
    hub_xy,
    radius=hub_n.width / 2,
    style=Styles.PrimaryFlat,
    text="イベント\nハブ",
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)

spokes = [
    ("auth", "認証 API", Styles.PrimaryNeutral),
    ("orders", "注文管理", Styles.Neutral),
    ("billing", "課金決済", Styles.SecondaryNeutral),
    ("notify", "通知配信", Styles.Neutral),
    ("search", "検索基盤", Styles.PrimaryNeutral),
]
for sid, label, st in spokes:
    n = r_layout[sid]
    rectangle(
        (n.x + ox2, n.y + oy2),
        width=n.width,
        height=n.height,
        style=st.patch(shape_r=1.6),
        text=label,
        text_style=Styles.DarkBold.patch(text_size=10.0),
    )

save()
```

---

## 11.4 クラスタ境界（ArchitectureGraph）とマトリクス配置（GridGraph）

複数ゾーンに跨がるクラウド境界図や整然としたマトリクス構成図では、`ArchitectureGraph` と `GridGraph` がノード座標と同時にコンテナの外枠サイズも自動計算します。

- **`ArchitectureGraph` と `ArchitectureDiagram` の連携**: マクロ領域を `pos="left" | "center" | "right" | "top" | "bottom"` で方位指定し、VPC 内のサブネット順序を `parent="vpc", order=1, 2` で整列します。描画時はトップレベル `NodeGroup` に `.bottom_left`、入れ子 `NodeGroup` に `.local_bottom_left`、内部 `Node` に `.local_xy` を渡し、両ステップで同じ `padding` と `(width, height)` を揃えます。
- **`GridGraph` のスマート回廊ルーティング**: `g.cell("id", row=0, col=1)` でセル番地を指定し、`g.cluster_row(0, "fe_tier")` や `g.cluster_column(col, id)` で行・列単位のグループ枠を生成できます。既定の `edge_routing="smart"` により、離れたセル間の矢印も他ノードを横切らず行間・列間の回廊を通ってクリーンに配線されます。

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=168, height=78)

# ステップ 1: ArchitectureGraph で入れ子 VPC とサブネット座標を解決
g = ArchitectureGraph(direction="LR", container_sep=14.0, default_node_width=24.0, default_node_height=14.0)
g.cluster("edge", ["client"], pos="left", padding=5.0)
g.group("vpc", pos="center", padding=5.0)
g.cluster("app_tier", ["api", "worker"], parent="vpc", order=1, padding=5.0)
g.cluster("data_tier", ["db"], parent="vpc", order=2, padding=5.0)

g.edge("client", "api")
g.edge("api", "worker")
g.edge("worker", "db")

layout = g.get_layout(margin=8.0)

# ステップ 2: .bottom_left / .local_bottom_left / .local_xy を用いて描画
d = ArchitectureDiagram(
    node_style=Styles.DarkBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

edge_grp = d.add(NodeGroup(title="External", padding=5.0, style=Styles.MutedDashed), xy=layout["edge"].bottom_left)
vpc_grp = d.add(NodeGroup(title="Production VPC", padding=5.0, style=Styles.MutedDashed), xy=layout["vpc"].bottom_left)
app_grp = vpc_grp.add(NodeGroup(title="Compute", padding=5.0, style=Styles.PrimaryNeutral), xy=layout["app_tier"].local_bottom_left)
data_grp = vpc_grp.add(NodeGroup(title="Storage", padding=5.0, style=Styles.SecondaryNeutral), xy=layout["data_tier"].local_bottom_left)

client = edge_grp.add(Node("Client", width=24, height=14, icon=PhosphorIcon.DEVICES), xy=layout["client"].local_xy)
api = app_grp.add(
    Node(
        "API Gateway",
        width=24,
        height=14,
        icon=GcpIcon.CLOUD_API_GATEWAY,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat,
    ),
    xy=layout["api"].local_xy,
)
worker = app_grp.add(Node("Worker", width=24, height=14, icon=GcpIcon.CLOUD_RUN), xy=layout["worker"].local_xy)
db = data_grp.add(Node("Cloud SQL", width=24, height=14, icon=GcpIcon.CLOUD_SQL), xy=layout["db"].local_xy)

d.connect(client, api, label="HTTPS")
d.connect(api, worker)
d.connect(worker, db)

d.draw()
save("arch_graph_vpc.png")
```
