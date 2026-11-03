# Users API

`/v1/users` REST リソースを通じてユーザーアカウントの作成・一覧取得・詳細参照・削除を行います。

```drawlib align=center code=fold file=users_provisioning_sequence.png caption="ユーザー作成と冪等キー検証のシーケンス"
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

作成日時の降順でカーソルページネーションされたユーザー一覧を取得します。

| クエリパラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `limit` | `int` | `20` | 1 ページあたりの取得件数（`1`〜`100`）。 |
| `starting_after` | `str \| None` | `None` | 次ページ取得用のユーザー ID カーソル（`usr_*`）。 |
| `role` | `str \| None` | `None` | ロールによる絞り込み（`"admin"`、`"member"`、`"viewer"`）。 |

## `POST` /v1/users

新しいユーザーアカウントを作成し、必要に応じて招待通知を送信します。

| ボディフィールド | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `email` | `str` | 必須 | 小文字正規化される一意のプライマリメールアドレス。 |
| `display_name` | `str` | 必須 | 表示名（`1`〜`120` 文字）。 |
| `role` | `str` | 任意 | 初期ロール（デフォルトは `"member"`）。 |

<details>
<summary><code>201 Created</code> JSON レスポンス例</summary>

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

一意の識別子（`usr_*`）を指定して単一の [User](02_models.md#user) レコードを取得します。

| パスパラメータ | 型 | 説明 |
| :--- | :--- | :--- |
| `id` | `str` | ユーザー識別子（`usr_*`）。存在しない場合は `404 Not Found` を返します。 |

## `DELETE` /v1/users/<id>

アクティブなセッションを失効させ、指定されたユーザーレコードを完全に削除します。

| パスパラメータ | 型 | 説明 |
| :--- | :--- | :--- |
| `id` | `str` | 削除対象のユーザー識別子（`usr_*`）。成功時は `204 No Content` を返します。 |
