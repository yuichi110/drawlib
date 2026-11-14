# 9. クラウド・システムアーキテクチャ構成図

分散システムの設計図は、信頼境界・ネットワーク階層・サービス間の依存関係を正確に伝える必要があります。`drawlib.diagrams.architecture` は、階層型の境界コンテナ `NodeGroup`・33種のクラウド／技術アイコン列挙型（`GcpIcon`、`AwsIcon`、`AzureIcon`、`PhosphorIcon` など）・境界認識エッジルーティング・交差のない `junction()` バス分岐を純粋な Python コードとして統合します。

```drawlib align=center code=fold file=cloud_vpc_architecture_ja.png caption="図 9.1: 外部クライアント・API Gateway・Junction 分岐・データ層を備えた本番クラウド VPC 構成図"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    GcpIcon,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.styles import Styles

setup(width=160, height=74)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.White,
)

# 外部アクターは必ずクラウドリージョン／VPC 境界の「外側」に配置する
client = d.add(
    Node(
        "Web・モバイル\nクライアント",
        width=25.0,
        height=18.5,
        icon=PhosphorIcon.DEVICES,
        icon_size=6.0,
        card_style=Styles.Neutral.patch(shape_r=2.0),
    ),
    xy=(14.5, 30.0),
)

# クラウドリージョン／VPC 境界（図全体座標系で左下 (41, 2)）
vpc = d.add(
    NodeGroup(
        title="Google Cloud リージョン — 本番 VPC (us-central1)",
        width=109.0,
        height=62.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.4),
        text_style=Styles.DarkBold.patch(text_size=11.0, halign="left"),
    ),
    xy=(41.0, 2.0),
)

# 注目の入口ノード API Gateway（vpc 左下を原点とするローカル中心座標）
gateway = vpc.add(
    Node(
        "API Gateway\n(Ingress 境界)",
        width=23.0,
        height=19.0,
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=6.0,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.0),
    ),
    xy=(16.5, 28.0),
)

# VPC 内のアプリケーション層（White カード + 公式 GcpIcon）
auth_svc = vpc.add(
    Node(
        "認証サービス\n(Cloud Run)",
        width=24.0,
        height=16.5,
        icon=GcpIcon.CLOUD_RUN,
        icon_size=6.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(52.5, 40.5),
)
order_svc = vpc.add(
    Node(
        "注文 API\n(Cloud Run)",
        width=24.0,
        height=16.5,
        icon=GcpIcon.CLOUD_RUN,
        icon_size=6.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(52.5, 15.5),
)

# ネストされたデータ層 NodeGroup（vpc 内のローカル左下座標）
data_tier = vpc.add(
    NodeGroup(
        title="データ層 (Private)",
        width=34.0,
        height=52.5,
        style=Styles.SecondaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
    ),
    xy=(71.0, 3.5),
)
sql_db = data_tier.add(
    Node(
        "Cloud SQL\n(メイン DB)",
        width=26.0,
        height=16.5,
        icon=GcpIcon.CLOUD_SQL,
        icon_size=6.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(17.0, 37.0),
)
cache_db = data_tier.add(
    Node(
        "Memorystore\n(Redis キャッシュ)",
        width=26.0,
        height=16.5,
        icon=GcpIcon.MEMORYSTORE,
        icon_size=6.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(17.0, 12.0),
)

# 外部 HTTPS 接続 + Junction による整然としたバス分岐
d.connect(
    client,
    gateway,
    label="HTTPS",
    routing="direct",
    padding=1.0,
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_shift=(-2.0, 2.6)),
)

j_mid = d.junction((75.0, 30.0))
j_top = d.junction((75.0, 42.5))
j_bot = d.junction((75.0, 17.5))
d.connect(gateway, j_mid, arrow="-", routing="direct", padding=(1.0, 0.0))
d.connect(j_mid, j_top, arrow="-", routing="direct")
d.connect(j_mid, j_bot, arrow="-", routing="direct")
d.connect(j_top, auth_svc, arrow="->", routing="direct", padding=(0.0, 1.0))
d.connect(j_bot, order_svc, arrow="->", routing="direct", padding=(0.0, 1.0))

d.connect(auth_svc, sql_db, arrow="->", routing="direct", padding=1.0)
d.connect(order_svc, cache_db, arrow="<->", routing="direct", padding=1.0)

d.draw(xy=(4.0, 4.0))
save()
```

## 9.1 コンテナ既定スタイル・`Node`・ローカル／グローバル座標系

`ArchitectureDiagram` は図全体のルートコンテナであり、**3段階のスタイル継承**（*個別要素の上書き -> 図全体の既定値 -> 組み込み初期値*）を提供します。コンストラクタの4つの必須キーワード引数（`node_style`、`node_text_style`、`edge_style`、`edge_text_style`）とオプションの `node_card_style` を定義しておけば、多数のマイクロサービス間で文字サイズや線幅を統一できます。

`d.add(..., xy=...)` と `group.add(..., xy=...)` では、対象の型と親コンテナによって `xy` の意味（中心か左下か・グローバルかローカルか）が明確に定められています。

| 要素登録メソッド | `xy` の基準点（アンカー） | 座標空間の原点 | 図全体のグローバル座標への換算式 |
| :--- | :--- | :--- | :--- |
| **`d.add(Node(...), xy=(cx, cy))`** | **中央 `Center`** `(cx, cy)` | 図全体のグローバル座標 | `(cx, cy)` |
| **`d.add(NodeGroup(...), xy=(x0, y0))`** | **左下 `Bottom-Left`** `(x0, y0)` | 図全体のグローバル座標 | 左下が `(x0, y0)` |
| **`group.add(Node(...), xy=(lx, ly))`** | **中央 `Center`** `(lx, ly)` | `group` 左下を `(0, 0)` とする **ローカル座標** | `(x0 + lx, y0 + ly)` |
| **`group.add(NodeGroup(...), xy=(lx0, ly0))`** | **左下 `Bottom-Left`** `(lx0, ly0)` | `group` 左下を `(0, 0)` とする **ローカル座標** | 左下が `(x0 + lx0, y0 + ly0)` |
| **`d.junction((jx, jy))`** | **正確な1点** `(jx, jy)` | 図全体のグローバル座標 | `(jx, jy)` |

### 9.1.1 公式クラウドアイコンとカード背景コントラストの設計原則

- **マルチカラー公式クラウド・技術アイコン（`GcpIcon`、`AwsIcon`、`AzureIcon`、`DataIcon`、`CnativeIcon` など）**: `512x512` のマルチカラー PNG アイコンとして描画されるため、`Styles.White` や淡い `Styles.Neutral` カード（`card_style=Styles.White.patch(shape_r=1.8)`）の上に配置するとブランドカラーが鮮明に際立ちます。
- **注目の主役ノード（`Styles.PrimaryFlat` / `Styles.AccentFlat`）**: 高彩度のベタ塗りカードは図内で1〜2個の最重要ノード（API Gateway やイベントルーターなど）に限定し、単色ベクターの `PhosphorIcon` に `style=Styles.WhiteBold` と `text_style=Styles.WhiteBold` を組み合わせて高い視認性を確保します。

## 9.2 `NodeGroup` による境界設計と外部アクター配置ルール

`NodeGroup` はクラウドリージョン・VPC・アベイラビリティゾーン・Kubernetes クラスタ・サブネット・セキュリティゾーンといった階層的な境界を表現します。`width=None, height=None` のまま `padding: float = 5.0` で子要素を自動包囲させることも、`width` と `height` を明示指定して複数ティアの枠サイズを美しく揃えることも可能です。

> **アーキテクチャ境界の鉄則 — 外部アクターは必ずクラウド `NodeGroup` の外側に置く**: エンドユーザー・ブラウザ・モバイル端末・外部 Webhook 送信元を、クラウドリージョンや VPC の `NodeGroup` の *内側* に配置してはいけません。外部アクターは必ず `d.add(Node(...), xy=...)` で外側のグローバル領域に配置し、CDN・ロードバランサ・API Gateway などの入口ノードを経由して境界線を跨がせます。

## 9.3 エッジルーティング・双方向矢印・`junction()` バス分岐

`d.connect(start, end, ...)`（および `node.connect(...)` / `Edge(...)`）は、`Node`・`NodeGroup`・`Junction` の外周境界で自動的にクリッピングされた接続線を描画します。

- **3種のルーティングモード（`routing`）**:
  - `"orthogonal"` *(既定)*: ティア間を直角の L 字・Z 字で結ぶマンハッタン配線。
  - `"direct"`: 水平・垂直に揃えたノード間やバス幹線を最短距離で結ぶ直線配線。
  - `"curved"`: `.via((x, y))` で弧の膨らみを制御できる滑らかな曲線配線（非同期イベントやレプリケーション経路に最適）。
- **境界ポート選択・余白 `padding`・双方向矢印**: 接続端は相手ノード（または最初の `.via((x, y))` 経由点）に最も近い辺を自動選択します。`padding=1.0`（または非対称タプル `padding=(1.0, 0.0)`）で矢印先端の余白を整え、`arrow="<->"` で双方向キャッシュ参照を表現し、`edge_text_style` の `xy_shift=(dx, dy)` でラベルと線の重なりを防ぎます。
- **スパゲッティ配線を防ぐバス分岐（`d.junction(xy)`、`node.fork()`、`edge.add_point()`）**: 1つのゲートウェイから N 個の後続サービスへ斜めの線を何本も引くのではなく、`arrow="-"` の幹線を共有の `d.junction((x, y))` へ接続してから分岐させます（`gateway.fork([svc1, svc2], at_x=...)` による1行記述も可能です）。

```drawlib align=center code=fold file=routing_and_junctions_ja.png caption="図 9.2: エッジ接続パターン比較 — Direct・Orthogonal・Curved と Junction バス分岐"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.styles import Styles

setup(width=160, height=70)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.2),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.White,
)

# 左パネル：3種のエッジルーティング比較
left = d.add(
    NodeGroup(
        title="3種のルーティング (direct / orthogonal / curved)",
        width=72.0,
        height=58.0,
        style=Styles.Neutral.patch(shape_r=2.2),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(2.0, 2.0),
)
a1 = left.add(Node("Edge LB", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(13.5, 43.0))
b1 = left.add(Node("認証 Pod", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(58.5, 43.0))
d.connect(
    a1,
    b1,
    label='direct ("<->")',
    arrow="<->",
    routing="direct",
    padding=1.0,
    text_style=Styles.DarkBold.patch(text_size=10.0, text_bg_fill_color=None, xy_shift=(0.0, 2.8)),
)

a2 = left.add(Node("API Pod", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(13.5, 28.5))
b2 = left.add(Node("SQL 参照", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(58.5, 22.5))
d.connect(
    a2,
    b2,
    label="orthogonal",
    arrow="->",
    routing="orthogonal",
    padding=1.0,
    text_style=Styles.DarkBold.patch(text_size=10.0, text_bg_fill_color=None, xy_shift=(6.5, 5.8)),
)

a3 = left.add(Node("送信元", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(13.5, 10.5))
b3 = left.add(Node("購読ワーカー", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(58.5, 10.5))
e_curved = d.connect(
    a3,
    b3,
    label="curved (非同期)",
    arrow="->",
    routing="curved",
    style=Styles.SecondaryBold.patch(line_style="dashed"),
    padding=1.0,
    text_style=Styles.DarkBold.patch(text_size=10.0, text_bg_fill_color=None, xy_shift=(2.5, 5.2)),
)
e_curved.via((28.0, 10.4), (33.0, 8.6), (38.0, 7.8), (43.0, 8.6), (48.0, 10.4))

# 右パネル：Junction による1対3のバス分岐
right = d.add(
    NodeGroup(
        title="junction() による交差ゼロのバス分岐",
        width=72.0,
        height=58.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.2),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(78.0, 2.0),
)
router = right.add(
    Node(
        "イベント\nルーター",
        width=21.0,
        height=17.0,
        icon=PhosphorIcon.GIT_BRANCH,
        icon_size=5.6,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat.patch(shape_r=1.8),
    ),
    xy=(14.5, 26.5),
)
w1 = right.add(
    Node("課金ワーカー", width=25.0, height=11.5, card_style=Styles.White.patch(shape_r=1.6)),
    xy=(55.0, 42.5),
)
w2 = right.add(
    Node("検索インデクサ", width=25.0, height=11.5, card_style=Styles.White.patch(shape_r=1.6)),
    xy=(55.0, 26.5),
)
w3 = right.add(
    Node("監査アーカイブ", width=25.0, height=11.5, card_style=Styles.SecondaryNeutral.patch(shape_r=1.6)),
    xy=(55.0, 10.5),
)

jb_mid = d.junction((112.0, 28.5))
jb_top = d.junction((112.0, 44.5))
jb_bot = d.junction((112.0, 12.5))
d.connect(router, jb_mid, arrow="-", routing="direct", padding=(1.0, 0.0))
d.connect(jb_mid, jb_top, arrow="-", routing="direct")
d.connect(jb_mid, jb_bot, arrow="-", routing="direct")
d.connect(jb_top, w1, arrow="->", routing="direct", padding=(0.0, 1.0))
d.connect(jb_mid, w2, arrow="->", routing="direct", padding=(0.0, 1.0))
d.connect(jb_bot, w3, arrow="->", routing="direct", padding=(0.0, 1.0))

d.draw(xy=(4.0, 4.0))
save()
```

定型的な1対Nの直交バス分岐や既存エッジ途中からの分岐（Dead Letter Queue への退避など）には、`node.fork(targets, at_x=...)` や `edge.add_point((x, y))` を使うことで1メソッドで簡潔に記述できます。

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, PhosphorIcon
from drawlib.styles import Styles

setup(width=124, height=54)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.2),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

lb = d.add(
    Node(
        "Ingress LB",
        width=24.0,
        height=16.0,
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=5.8,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat.patch(shape_r=1.8),
    ),
    xy=(20.0, 25.0),
)
pod_a = d.add(Node("ワーカー A", width=24.0, height=15.0, icon=GcpIcon.CLOUD_RUN, icon_size=5.8), xy=(84.0, 36.0))
pod_b = d.add(Node("ワーカー B", width=24.0, height=15.0, icon=GcpIcon.CLOUD_RUN, icon_size=5.8), xy=(84.0, 14.0))

# x=52.0 に共有 Junction を自動生成し、上下2つの Pod へ整然と分岐配線
lb.fork([pod_a, pod_b], at_x=52.0, padding=1.2)

d.draw(xy=(6.0, 2.0))
save()
```

全33種のアイコン列挙型やウェイポイント制御の詳細は、`uv run drawlib rules show lib-diagrams-architecture` および `uv run drawlib rules show lib-icons-overview` で確認できます。
