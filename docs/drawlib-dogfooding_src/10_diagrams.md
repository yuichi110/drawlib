# 第10章: システムダイアグラム（アーキテクチャ・設計図）

`drawlib.diagrams` は、複雑なソフトウェアシステムやネットワーク構造をエンジニアリング標準記法で描画するための最上位モジュールです。

## 10.1 アーキテクチャ図 (`ArchitectureDiagram`)

VPC やサブネットなどの境界グループ（`NodeGroup`）、コンポーネント（`Node`）、サービス間の直交配線を直感的に定義できます。

```drawlib 640px center file:fig_architecture_diagram.png caption:"図 10.1: クラウドマイクロサービス構成図"
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
gw = vpc.add(Node((22, 16), "API Gateway", icon=GcpIcon.APIGEE, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(15.0, 26.0))
auth = vpc.add(Node((24, 16), "Auth Service", icon=GcpIcon.SECURITY_COMMAND_CENTER, icon_size=7.5), xy=(48.0, 38.0))
order = vpc.add(Node((24, 16), "Order Service", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=7.5), xy=(48.0, 14.0))
db = vpc.add(Node((26, 17), "Cloud SQL\n(PostgreSQL)", icon=GcpIcon.CLOUD_SQL, icon_size=7.5), xy=(90.0, 26.0))

# 外部クライアントノード (diag.add)
client = diag.add(Node((22, 17), "Client User\n(Web/App)", icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.5), xy=(13.0, 32.0))

# サービス間接続
diag.connect(client, gw, label="HTTPS (443)", padding=1.5)
gw.fork([auth, order], at_x=71.0, padding=1.5)
diag.connect(order, db, label="SQL Query", padding=1.5)

diag.draw(xy=(3.0, 3.0))
```

## 10.2 自動レイアウトエンジン (`drawlib.graph`)

ゼロからノードのトポロジー（論理関係）とピクセル座標（幾何美観）を同時に計算しようとすると、人間にとっても AI にとってもワーキングメモリが逼迫します（**コールドスタート問題**）。

Drawlib は Pure Python の自動レイアウトソルバー `drawlib.graph` を提供しており、外部ツール（Graphviz 等）に依存することなく、宣言的な記述から美しい座標を自動算出できます。

```drawlib 640px center file:fig_architecture_graph.png caption:"図 10.2: ArchitectureGraph による自動レイアウトとクラスタリング"
from drawlib.canvas import setup
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=195, height=80)

g = ArchitectureGraph(direction="LR", default_node_width=26.0, default_node_height=13.0)

ts_hero = Styles.WhiteBold.patch(text_size=9.5)
ts_body = Styles.Dark.patch(text_size=9.0)

# 外部クライアント (左側に固定配置)
g.cluster("external", ["client"], label="External Client", pos="left", padding=4.0)
g.node("client", "Web / Mobile\nClient", style=Styles.Neutral, text_style=ts_body)

# クラウド VPC (中央のメインクラスタ)
g.group("vpc", "Cloud VPC (ap-northeast-1)", pos="center", padding=5.0)
g.cluster("app_tier", ["api", "worker"], label="Application Tier", parent="vpc", order=1, padding=4.0)
g.cluster("data_tier", ["db", "cache"], label="Data Tier", parent="vpc", order=2, padding=4.0)

g.node("api", "API Gateway", style=Styles.PrimaryFlat, text_style=ts_hero)
g.node("worker", "Async Worker", style=Styles.SecondaryNeutral, text_style=ts_body)
g.node("db", "Primary DB", style=Styles.Neutral, text_style=ts_body)
g.node("cache", "Redis Cache", style=Styles.Neutral, text_style=ts_body)

# エッジ接続 (直交配線)
g.edge("client", "api", label="HTTPS")
g.edge("api", "worker", label="Queue")
g.edge("api", "cache", label="Get/Set")
g.edge("worker", "db", label="Write")

g.draw(margin=8)
```

### 下書きから清書への架け橋 (`export_code()`)
- `g.draw()`: 宣言したトポロジーを自動レイアウトして即座にキャンバスに描画します。
- `g.export_code()`: 計算された座標を変数化（例: `api_xy = (72.0, 42.0)`）した Drawlib Python コードを自動生成します。「**大枠は自動配置で下書きし、細部だけ手動で絶対座標微調整を行う**」という理想的な 2 段階ワークフローが完結します。

### 専門用途に応じた 5 大ソルバー
- **`ArchitectureGraph`**: 多層階層（Tier）と VPC / サブネット境界、方位（Compass: left/right/top/bottom/center）配置。
- **`LayerGraph`**: Sugiyama 法に基づく多段 DAG・データフロー・依存関係グラフ。
- **`TreeGraph`**: Reingold-Tilford 法による組織図・決定木・AST。
- **`RadialGraph`**: 同心円（Concentric Rings）によるイベント駆動・ハブ＆スポーク。
- **`GridGraph`**: 2D 行列グリッド整列とサービス一覧。

## 10.3 その他の専門ダイアグラム

- **`FlowDiagram`**: 処理ステップ、条件分岐（Decision）、ループ制御。
- **`SequenceDiagram`**: アクター、参加者、同期/非同期メッセージ、ノート。
- **`ERDiagram`**: 物理テーブル定義、PK/FK、Crow's Foot（鳥の足）記法によるリレーション。
- **`ClassDiagram`**: オブジェクト指向クラス、メソッド、継承・集約関係。
- **`StateDiagram`**: 状態遷移マシン、イベントトリガー、ガード条件。
