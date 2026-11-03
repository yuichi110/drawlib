# API 概要

**__TARGET__** API & SDK リファレンスへようこそ。すべてのエンドポイントと SDK シンボルは、[Drawlib](https://github.com/yuichi110/drawlib) による宣言的な構成図・シーケンス図とともに Git 上で一元管理されています。

```drawlib align=center code=fold file=api_gateway_topology.png caption="API ゲートウェイとバックエンドサービス構成"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=120, height=50)

d = ArchitectureDiagram(
    node_style=Styles.Dark,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.Dark.patch(line_width=1.5),
    edge_text_style=Styles.Muted.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

sdk = d.add(
    Node("Client / SDK", icon=PhosphorIcon.TERMINAL_WINDOW, width=22, height=15, card_style=Styles.PrimaryNeutral),
    xy=(16, 25),
)

vpc = d.add(
    NodeGroup(
        "API Platform",
        width=78,
        height=42,
        style=Styles.SecondaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=11.0, halign="left", valign="top"),
    ),
    xy=(36, 4),
)
gw = vpc.add(
    Node(
        "API Gateway",
        icon=PhosphorIcon.SHIELD_CHECK,
        width=22,
        height=15,
        style=Styles.White,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat,
    ),
    xy=(20, 21),
)
svc = vpc.add(
    Node("Users Service", icon=PhosphorIcon.USERS, width=22, height=15, card_style=Styles.Neutral),
    xy=(58, 30),
)
db = vpc.add(
    Node("Primary DB", icon=PhosphorIcon.DATABASE, width=22, height=15, card_style=Styles.Neutral),
    xy=(58, 11),
)

sdk.connect(gw, label="HTTPS")
gw.connect(svc, label="gRPC")
svc.connect(db, label="SQL")

d.draw(xy=(0, 0))
save()
```

## Authentication

`/v1/*` エンドポイントへのすべてのリクエストには、`Authorization` HTTP ヘッダーに Bearer API キーを指定します:

```http
Authorization: Bearer sk_live_98a7b6c5d4e3f2a1
Content-Type: application/json
```

| ヘッダー | 必須 | 説明 |
| :--- | :--- | :--- |
| `Authorization` | 必須 | 形式: `Bearer <api_key>`。環境ごとに `sk_test_*` または `sk_live_*` が発行されます。 |
| `Idempotency-Key` | 任意 | `POST` / `PATCH` 更新系の安全なリトライ用 UUIDv4 トークン（有効期間 24 時間）。 |
| `X-Request-Id` | レスポンス | 分散トレーシング用にすべてのレスポンスで返却される相関 ID。 |

## Rate Limits & Errors

API キー単位でスライディングトークンバケット方式のレート制限が適用されます:

| プラン | リクエスト上限 / 分 | バースト許容数 | リトライヘッダー |
| :--- | :--- | :--- | :--- |
| Standard | `600 req/min` | `100 req` | `Retry-After`（秒） |
| Enterprise | `6,000 req/min` | `1,000 req` | `Retry-After`（秒） |

非 2xx レスポンスでは、[SDK & データモデル](02_models.md#apierror) で定義された構造化 JSON エラーが返却されます。各エンドポイントの詳細は [Users API](01_users.md) を参照してください。
