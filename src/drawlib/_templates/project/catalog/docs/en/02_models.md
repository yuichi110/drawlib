# SDK & Data Models

Typed data models and webhook verification utilities shared across the REST API and official Python SDK.

```drawlib align=center code=fold file=users_data_schema.png caption="Core Identity & API Key Entity Schema"
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

Immutable representation of an authenticated account returned by [Users API](01_users.md) endpoints.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `id` | `str` | Globally unique prefixed ULID (`usr_*`). |
| `email` | `str` | Verified primary email address. |
| `display_name` | `str` | Full display name shown in audit logs. |
| `role` | `Literal["admin", "member", "viewer"]` | Effective RBAC role within the workspace. |
| `created_at` | `datetime` | UTC timestamp when the account was provisioned. |

## `class` ApiError

Structured exception and JSON error payload returned whenever an HTTP status code is `400` or higher.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `code` | `str` | Machine-readable error slug (e.g. `"rate_limit_exceeded"`, `"user_not_found"`). |
| `message` | `str` | Developer-facing explanation safe to log. |
| `request_id` | `str` | Server correlation ID matching the `X-Request-Id` response header. |

## `def` verify_signature(payload, header, secret)

Verify the HMAC-SHA256 `X-Webhook-Signature` header on incoming webhook deliveries in constant time.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `payload` | `bytes` | Raw unparsed HTTP request body bytes. |
| `header` | `str` | Value of the `X-Webhook-Signature` HTTP header (`t=...,v1=...`). |
| `secret` | `str` | Endpoint signing secret (`whsec_*`) from dashboard settings. |

**Returns:** `bool` — `True` when the timestamp tolerance and HMAC digest match; raises `ApiError` otherwise.
