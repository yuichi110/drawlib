# 第10章: システムダイアグラム（アーキテクチャ・設計図）

`drawlib.diagrams` は、複雑なソフトウェアシステムやネットワーク構造をエンジニアリング標準記法で描画するための最上位モジュールです。

## 10.1 アーキテクチャ図 (`ArchitectureDiagram`)

VPC やサブネットなどの境界グループ（`NodeGroup`）、コンポーネント（`Node`）、サービス間の直交配線を直感的に定義できます。

```drawlib width=640px align=center file=fig_architecture_diagram.png caption="図 10.1: クラウドマイクロサービス構成図"
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=155, height=78)

diag = ArchitectureDiagram(
    node_style=Styles.PrimaryFlat,
    node_text_style=Styles.Black,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Black,
    node_card_style=Styles.Neutral,
    title="クラウドマイクロサービス構成図",
)

# VPC 境界グループ
vpc = diag.add(
    NodeGroup(
        title="AWS / Cloud VPC (ap-northeast-1)",
        padding=6.0,
    ),
    xy=(40.0, 6.0),
)

# VPC 内のサービスノード (vpc.add)
gw = vpc.add(Node("API Gateway", width=22, height=16, icon=GcpIcon.APIGEE, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(15.0, 26.0))
auth = vpc.add(Node("Auth Service", width=24, height=16, icon=GcpIcon.SECURITY_COMMAND_CENTER, icon_size=7.5), xy=(48.0, 38.0))
order = vpc.add(Node("Order Service", width=24, height=16, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=7.5), xy=(48.0, 14.0))
db = vpc.add(Node("Cloud SQL\n(PostgreSQL)", width=26, height=17, icon=GcpIcon.CLOUD_SQL, icon_size=7.5), xy=(90.0, 26.0))

# 外部クライアントノード (diag.add)
client = diag.add(Node("Client User\n(Web/App)", width=22, height=17, icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.5), xy=(13.0, 32.0))

# サービス間接続
diag.connect(client, gw, label="HTTPS (443)", padding=1.5)
gw.fork([auth, order], at_x=71.0, padding=1.5)
diag.connect(order, db, label="SQL Query", padding=1.5)

diag.draw(xy=(3.0, 3.0))
```

## 10.2 自動レイアウトエンジン (`drawlib.graph`)

ゼロからノードのトポロジー（論理関係）とピクセル座標（幾何美観）を同時に計算しようとすると、人間にとっても AI にとってもワーキングメモリが逼迫します（**コールドスタート問題**）。

Drawlib の `drawlib.graph` は、外部バイナリ（Graphviz 等）に依存しない **Pure Python の座標・レイアウト計算エンジン（`get_layout()`）** です。描画スタイルやラベル属性を持たず、Step 1 でトポロジーから座標（`xy`, `local_xy`, `bottom_left`, `local_bottom_left`, `points`）を算出し、Step 2 で `drawlib.diagrams` や `drawlib.shapes` に渡して描画する **2 段階ワークフロー** を実現します。

```drawlib align=center file=fig_architecture_graph.png caption="図 10.2: ArchitectureGraph.get_layout() と ArchitectureDiagram の 2 段階連携"
from drawlib.canvas import setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    GcpIcon,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=205, height=88)

# Step 1: ArchitectureGraph でクラスタ境界とノード座標を自動計算
g = ArchitectureGraph(direction="LR", container_sep=16.0, default_node_width=24.0, default_node_height=15.0)
g.cluster("external", ["client"], pos="left", padding=5.0)
g.group("vpc", pos="center", padding=5.0)
g.cluster("app_tier", ["api", "worker"], parent="vpc", order=1, padding=5.0)
g.cluster("data_tier", ["db", "cache"], parent="vpc", order=2, padding=5.0)

g.edge("client", "api")
g.edge("api", "worker")
g.edge("worker", "db")
g.edge("worker", "cache")

layout = g.get_layout(margin=8.0)

# Step 2: 算出された座標 (bottom_left, local_bottom_left, local_xy) を ArchitectureDiagram に渡して描画
d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    node_card_style=Styles.Neutral,
)

ext = d.add(NodeGroup(title="External Client", padding=5.0, style=Styles.MutedDashed), xy=layout["external"].bottom_left)
vpc = d.add(NodeGroup(title="Cloud VPC (ap-northeast-1)", padding=5.0, style=Styles.MutedDashed), xy=layout["vpc"].bottom_left)
app = vpc.add(NodeGroup(title="Application Tier", padding=5.0, style=Styles.PrimaryNeutral), xy=layout["app_tier"].local_bottom_left)
data = vpc.add(NodeGroup(title="Data Tier", padding=5.0, style=Styles.SecondaryNeutral), xy=layout["data_tier"].local_bottom_left)

client = ext.add(Node("Web / Mobile", width=24, height=15, icon=PhosphorIcon.DEVICES), xy=layout["client"].local_xy)
api = app.add(
    Node("API Gateway", width=24, height=15, icon=GcpIcon.CLOUD_API_GATEWAY, style=Styles.White, card_style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=10.0)),
    xy=layout["api"].local_xy,
)
worker = app.add(Node("Async Worker", width=24, height=15, icon=GcpIcon.CLOUD_RUN), xy=layout["worker"].local_xy)
db = data.add(Node("Primary DB", width=24, height=15, icon=GcpIcon.CLOUD_SQL), xy=layout["db"].local_xy)
cache = data.add(Node("Redis Cache", width=24, height=15, icon=GcpIcon.MEMORYSTORE), xy=layout["cache"].local_xy)

d.connect(client, api, label="HTTPS")
d.connect(api, worker)
worker.fork([db, cache], at_x=145.0)

d.draw()
```

### 2 段階ワークフロー (`get_layout()` & `print(layout)`)
- **Step 1 — 座標解決 (`layout = g.get_layout()`)**: 宣言したトポロジーから全ノードとクラスタの座標を算出します。`print(layout)` で人間や AI が読みやすい座標一覧を出力してスクリプトに転記することも、`layout["id"]` を直接参照して `layout.offset("api", dy=-4.0)` で微調整することも可能です。
- **Step 2 — 表現力豊かな描画 (`drawlib.diagrams` / `drawlib.shapes`)**: 算出された `.xy`、`.local_xy`、`.bottom_left`、`.local_bottom_left`、`.points` を `ArchitectureDiagram`、`FlowDiagram`、または基本図形に渡すことで、自動配置とアイコン・スタイル表現を両立します。

### 専門用途に応じた 5 大ソルバー
- **`ArchitectureGraph`**: 多層階層（Tier）と VPC / サブネット境界、方位（Compass: left/right/top/bottom/center）配置。
- **`LayerGraph`**: Sugiyama 法に基づく多段 DAG・データフロー・依存関係グラフ（`.tier()` 対応）。
- **`TreeGraph`**: Reingold-Tilford 法による組織図・決定木・AST（`.child()` 対応）。
- **`RadialGraph`**: 同心円（Concentric Rings）によるイベント駆動・ハブ＆スポーク（`.spoke()`・`layout.ring_radii` 対応）。
- **`GridGraph`**: 2D 行列グリッド整列とスマートチャネル配線（`.cell()`・`.cluster_row()` 対応）。

## 10.3 その他の専門ダイアグラム

- **`FlowDiagram`**: 処理ステップ、条件分岐（Decision）、ループ制御。
- **`SequenceDiagram`**: アクター、参加者、同期/非同期メッセージ、ノート。
- **`ERDiagram`**: 物理テーブル定義、PK/FK、Crow's Foot（鳥の足）記法によるリレーション。
- **`ClassDiagram`**: オブジェクト指向クラス、メソッド、継承・集約関係。
- **`StateDiagram`**: 状態遷移マシン、イベントトリガー、ガード条件。
