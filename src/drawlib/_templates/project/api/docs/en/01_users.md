# Users API

Create, inspect, list, and deactivate user accounts through the `/v1/users` REST resource.

```drawlib align=center code=fold file=users_provisioning_sequence.png caption="User Provisioning & Idempotency Lifecycle"
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

setup(width=120, height=62)

sd = SequenceDiagram(
    node_style=Styles.Dark,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.Dark.patch(line_width=1.4),
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    col_width=34.0,
    step_y=7.5,
)

client = sd.add(Participant("Client SDK", icon=PhosphorIcon.LAPTOP, width=22, card_style=Styles.PrimaryNeutral))
gateway = sd.add(
    Participant(
        "API Gateway",
        icon=PhosphorIcon.SHIELD_CHECK,
        width=22,
        style=Styles.White,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat,
    )
)
store = sd.add(Participant("Users DB", icon=PhosphorIcon.DATABASE, width=22, card_style=Styles.Neutral))

client.request(gateway, "POST /v1/users")
gateway.request(store, "INSERT INTO users")
store.reply(gateway, "usr_01J9X8K2 (created)")
gateway.reply(client, "201 Created + User JSON")

sd.draw(xy=(60, 31), align="center")
save()
```

## `GET` /v1/users

Return a cursor-paginated list of user accounts sorted by creation timestamp descending.

| Query Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `limit` | `int` | `20` | Number of records per page (`1`–`100`). |
| `starting_after` | `str \| None` | `None` | Opaque user ID cursor (`usr_*`) to fetch the next page. |
| `role` | `str \| None` | `None` | Optional role filter (`"admin"`, `"member"`, `"viewer"`). |

## `POST` /v1/users

Provision a new user account and optionally send an onboarding invitation.

| Body Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `email` | `str` | Yes | Unique primary email address normalized to lowercase. |
| `display_name` | `str` | Yes | Human-readable display name (`1`–`120` characters). |
| `role` | `str` | No | Initial role assignment (`"member"` by default). |

<details>
<summary>Example <code>201 Created</code> JSON Response</summary>

```json
{
  "id": "usr_01J9X8K2M4R7",
  "email": "ada@example.com",
  "display_name": "Ada Lovelace",
  "role": "admin",
  "created_at": "2026-04-01T09:30:00Z"
}
```
</details>

## `GET` /v1/users/<id>

Retrieve a single [User](02_models.md#user) record by its unique identifier (`usr_*`).

| Path Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `str` | Unique user identifier (`usr_*`). Returns `404 Not Found` if unknown. |

## `DELETE` /v1/users/<id>

Permanently revoke active sessions and delete the specified user record.

| Path Parameter | Type | Description |
| :--- | :--- | :--- |
| `id` | `str` | Unique user identifier (`usr_*`) to remove. Returns `204 No Content` on success. |
