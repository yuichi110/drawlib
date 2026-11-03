# SDK & データモデル

REST API と公式 Python SDK で共通利用される型付きデータモデルおよび Webhook 署名検証ユーティリティです。

```drawlib align=center code=fold file=users_data_schema.png caption="ユーザーと API キーの ER スキーマ"
from drawlib.canvas import save, setup
from drawlib.diagrams.er import Entity, ERDiagram
from drawlib.styles import Colors, Styles

setup(width=120, height=32)

erd = ERDiagram(
    node_style=Styles.Neutral.patch(text_size=10.2),
    header_style=Styles.SecondaryNeutral.patch(text_size=11.0),
    edge_style=Styles.Dark.patch(line_width=1.5),
    edge_text_style=Styles.Muted.patch(text_size=10.0),
)

users = erd.add(
    Entity(
        "users",
        width=38,
        header_style=Styles.PrimaryFlat.patch(text_color=Colors.White, text_size=11.0),
    )
    .add_column("id", "VARCHAR(24)", pk=True, nullable=False)
    .add_column("email", "VARCHAR(255)", nullable=False)
    .add_column("role", "VARCHAR(32)", nullable=False)
    .add_column("created_at", "TIMESTAMPTZ", nullable=False),
    xy=(28, 16),
)

keys = erd.add(
    Entity("api_keys", width=40)
    .add_column("id", "VARCHAR(24)", pk=True, nullable=False)
    .add_column("user_id", "VARCHAR(24)", fk=True, nullable=False)
    .add_column("prefix", "VARCHAR(16)", nullable=False)
    .add_column("expires_at", "TIMESTAMPTZ", nullable=True),
    xy=(90, 16),
)

erd.connect(users, keys, cardinality="1:*", start_column="id", end_column="user_id", label="owns")

erd.draw(xy=(0, 0))
save()
```

## `class` User

[Users API](01_users.md) の各エンドポイントから返却される認証済みアカウントの不変モデルです。

| 属性 | 型 | 説明 |
| :--- | :--- | :--- |
| `id` | `str` | プレフィックス付き一意 ULID（`usr_*`）。 |
| `email` | `str` | 検証済みプライマリメールアドレス。 |
| `display_name` | `str` | 監査ログ等に表示される氏名・表示名。 |
| `role` | `Literal["admin", "member", "viewer"]` | ワークスペース内の有効 RBAC ロール。 |
| `created_at` | `datetime` | アカウント作成日時（UTC）。 |

## `class` ApiError

HTTP ステータスコードが `400` 以上の際に返却される構造化エラー例外および JSON ペイロードです。

| 属性 | 型 | 説明 |
| :--- | :--- | :--- |
| `code` | `str` | 機械判読可能なエラーコード（例: `"rate_limit_exceeded"`、`"user_not_found"`）。 |
| `message` | `str` | ログ出力可能な開発者向けエラー説明文。 |
| `request_id` | `str` | `X-Request-Id` レスポンスヘッダーに対応するリクエスト相関 ID。 |

## `def` verify_signature(payload, header, secret)

受信した Webhook の `X-Webhook-Signature` ヘッダー（HMAC-SHA256）を定数時間で検証します。

| 引数 | 型 | 説明 |
| :--- | :--- | :--- |
| `payload` | `bytes` | 未パースの生の HTTP リクエストボディバイト列。 |
| `header` | `str` | `X-Webhook-Signature` ヘッダー文字列（`t=...,v1=...`）。 |
| `secret` | `str` | ダッシュボードで発行された署名シークレット（`whsec_*`）。 |

**戻り値:** `bool` — タイムスタンプ許容範囲と HMAC ダイジェストが一致した場合は `True`、不正な場合は `ApiError` を送出します。
