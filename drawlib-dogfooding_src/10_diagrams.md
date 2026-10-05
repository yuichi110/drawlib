# 第10章: システムダイアグラム（アーキテクチャ・設計図）

`drawlib.diagrams` は、複雑なソフトウェアシステムやネットワーク構造をエンジニアリング標準記法で描画するための最上位モジュールです。

## 10.1 アーキテクチャ図 (`ArchitectureDiagram`)

VPC やサブネットなどの境界グループ（`NodeGroup`）、コンポーネント（`Node`）、サービス間の直交配線を直感的に定義できます。

```drawlib 640px center file:fig_architecture_diagram.png caption:"図 10.1: クラウドマイクロサービス構成図"
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=115, height=65)

diag = ArchitectureDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.DarkBold,
    title="クラウドマイクロサービス構成図",
)

# VPC 境界グループ
vpc = diag.add(
    NodeGroup(
        title="AWS / Cloud VPC (ap-northeast-1)",
        padding=6.0,
    ),
    xy=(32.0, 6.0),
)

# VPC 内のサービスノード (vpc.add)
gw = vpc.add(Node("API Gateway", icon=GcpIcon.APIGEE, icon_size=7.5), xy=(12.0, 24.0))
auth = vpc.add(Node("Auth Service", icon=GcpIcon.SECURITY_COMMAND_CENTER, icon_size=7.5), xy=(38.0, 36.0))
order = vpc.add(Node("Order Service", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=7.5), xy=(38.0, 12.0))
db = vpc.add(Node("Cloud SQL\n(PostgreSQL)", icon=GcpIcon.CLOUD_SQL, icon_size=7.5), xy=(64.0, 24.0))

# 外部クライアントノード (diag.add)
client = diag.add(Node("Client User\n(Web/App)", icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.5), xy=(12.0, 30.0))

# サービス間接続
diag.connect(client, gw, label="HTTPS (443)", padding=2.0)
diag.connect(gw, auth, label="gRPC", padding=2.0)
diag.connect(gw, order, label="gRPC", padding=2.0)
diag.connect(order, db, label="SQL Query", padding=2.0)

diag.draw(xy=(5.0, 4.0))
```

## 10.2 その他の専門ダイアグラム

- **`FlowDiagram`**: 処理ステップ、条件分岐（Decision）、ループ制御。
- **`SequenceDiagram`**: アクター、参加者、同期/非同期メッセージ、ノート。
- **`ERDiagram`**: 物理テーブル定義、PK/FK、Crow's Foot（鳥の足）記法によるリレーション。
- **`ClassDiagram`**: オブジェクト指向クラス、メソッド、継承・集約関係。
- **`StateDiagram`**: 状態遷移マシン、イベントトリガー、ガード条件。
