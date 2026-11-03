# drawlib.diagrams.sequence（シーケンス図）

自動等間隔ライフライン、参加者グループ、アクティベーション（実行区間）バー、付箋ノート、および複合フラグメント（`alt`、`loop`、`opt`、`par`）を備えた時系列 UML シーケンス図モジュールです。標準インポート: `from drawlib.diagrams.sequence import GcpIcon, Participant, ParticipantGroup, PhosphorIcon, SequenceDiagram`。

```drawlib align=center code=fold file=21_diagrams_sequence_hero.png caption="ParticipantGroup・アクティベーション区間・alt 分岐ブロックを用いたトークン検証シーケンス図"
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import GcpIcon, Participant, ParticipantGroup, PhosphorIcon, SequenceDiagram
from drawlib.styles import Colors, Styles

setup(width=120, height=78)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    autonumber=True,
    col_width=34.0,
    step_y=7.0,
    margin=4.0,
)

client = d.add(Participant("Web App", width=22, height=15, icon=PhosphorIcon.BROWSER, icon_size=6.5))

platform = d.add(
    ParticipantGroup(
        title="Auth Platform",
        padding=4.0,
        style=Styles.PrimaryNeutral.patch(line_style="dashed"),
        text_style=Styles.PrimaryBold.patch(text_size=10.5, halign="left"),
    )
)
api = platform.add(
    Participant(
        "Auth API",
        width=22,
        height=15,
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=6.5,
        style=Styles.White,
        text_style=Styles.WhiteBold.patch(text_color=Colors.White, text_size=10.5),
        card_style=Styles.PrimaryFlat,
    )
)
db = platform.add(
    Participant("User DB", width=22, height=15, icon=GcpIcon.CLOUD_SQL, icon_size=6.5, card_style=Styles.SecondaryNeutral)
)

api.activate()
client.request(api, "POST /v1/token")
api.request(db, "SELECT user_hash")
db.reply(api, "Row record")

with d.alt("Valid hash") as blk:
    blk.style = Styles.Neutral.patch(line_style="dashed")
    api.reply(client, "200 OK (JWT)")

api.deactivate()

d.draw(xy=(60.0, 39.0), align="center")
save()
```

---

## `class` SequenceDiagram

シーケンス図全体のレイアウトと垂直タイムラインを管理するトップレベルコンテナです。参加者を水平方向に `col_width` 間隔で自動配置し、イベントごとに下方向へ `step_y` ずつ時間を進行させます。

```python
SequenceDiagram(
    *,
    node_style: Style,
    node_text_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    node_card_style: Style | None = None,
    title: str = "",
    autonumber: bool = False,
    width: float | None = None,
    height: float | None = None,
    col_width: float = 20.0,
    step_y: float = 7.0,
    margin: float = 5.0,
    style: Style | None = None,
    title_style: Style | None = None,
) -> None
```

- **座標アンカー**: `draw(xy=(0.0, 0.0), align="bottom_left")` はシーケンス図の左下隅をキャンバス座標 `xy` に配置します（`align="center"` の場合はバウンディングボックス中心を `xy` に配置）。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `node_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | 参加者ベクターアイコンおよびフォールバック要素の基本スタイル（キーワード専用）。 |
| `node_text_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | 参加者ラベルおよびグループ見出しの基本テキストスタイル（キーワード専用）。 |
| `edge_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | メッセージ矢印線の基本ストローク・矢印スタイル（キーワード専用）。 |
| `edge_text_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | メッセージラベル、ブロック見出し、ノート用の基本テキストスタイル（キーワード専用）。 |
| `node_card_style` | `Style \| None` | `None` | [`Participant`](#participant) ヘッダーカードのデフォルト背景・枠線スタイル（`None` の場合は背景透過）。 |
| `title` | `str` | `""` | 上部ヘッダーの上方に中央揃えで描画される任意の図タイトル。 |
| `autonumber` | `bool` | `False` | `True` の場合、各メッセージラベルの先頭に連番（`1.`、`2.`、`3.` ...）を自動付与します。 |
| `width` | `float \| None` | `None` | ローカル単位での固定幅の任意上書き。 |
| `height` | `float \| None` | `None` | ローカル単位での固定高さの任意上書き。 |
| `col_width` | `float` | `20.0` | 自動配置される参加者ライフライン間のデフォルト水平間隔（中心間距離）。 |
| `step_y` | `float` | `7.0` | メッセージ・ノート・ブロック各ステップで下方向へ進む垂直間隔。 |
| `margin` | `float` | `5.0` | 参加者ヘッダーおよびライフライン周囲の外側マージン余白。 |
| `style` | `Style \| None` | `None` | 図全体を囲む外枠カードの任意の背景・枠線スタイル。 |
| `title_style` | `Style \| None` | `None` | `title` 用の任意のテキストスタイル上書き。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, item: Participant \| ParticipantGroup, x: float \| None = None, *, show: bool \| None = None) -> Participant \| ParticipantGroup` | [`Participant`](#participant)（任意で水平座標 `x` を固定可能）または [`ParticipantGroup`](#participantgroup) を登録します。 |
| `alt` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | 条件分岐を表す `alt` [`Block`](#block) コンテキストマネージャを返します（`with d.alt("条件"):`）。 |
| `connect` | `method` | `(self, source: Participant, target: Participant, label: str = "", arrow: ArrowType = "->", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | 任意の矢印形状（双方向 `"<->"` 等）を持つ [`Message`](#message) を記録します。 |
| `draw` | `method` | `(self, xy: tuple[float, float] = (0.0, 0.0), *, align: Literal["bottom_left", "center"] = "bottom_left", scale: PosFloat = 1.0) -> None` | アクティブなキャンバス上にシーケンス図全体を描画します。 |
| `else_` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | アクティブな `alt` ブロック内に破線の `else` 分岐区切りを挿入します（`with` ブロックとしても利用可能）。 |
| `events` | `property` | `-> list[object]` | 記録されたタイムラインイベント列を宣言順で返します。 |
| `get_size` | `method` | `(self) -> tuple[float, float]` | スケール適用前のローカル単位での推定全体サイズ `(width, height)` を返します。 |
| `groups` | `property` | `-> list[ParticipantGroup]` | 登録済みの [`ParticipantGroup`](#participantgroup) 一覧を返します。 |
| `loop` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | 反復処理を表す `loop` [`Block`](#block) コンテキストマネージャを返します。 |
| `note` | `method` | `(self, text: str, on: Participant \| None = None, over: list[Participant] \| None = None, pos: NotePosition = "right", style: Style \| None = None, show: bool = True) -> Note` | 現在ステップで単一参加者 `on` の脇、または複数参加者 `over` を跨ぐ [`Note`](#note) を記録します。 |
| `opt` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | 単一条件の任意実行を表す `opt` [`Block`](#block) コンテキストマネージャを返します。 |
| `par` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | 並列実行を表す `par` [`Block`](#block) コンテキストマネージャを返します。 |
| `participants` | `property` | `-> list[Participant]` | 登録順の [`Participant`](#participant) インスタンス一覧を返します。 |
| `reply` | `method` | `(self, source: Participant, target: Participant, label: str = "", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | `source` から `target` への破線応答 [`Message`](#message) を記録します。 |
| `request` | `method` | `(self, source: Participant, target: Participant, label: str = "", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | `source` から `target` への実線リクエスト [`Message`](#message) を記録します（`source is target` の自己呼び出しループにも対応）。 |
| `space` | `method` | `(self, dy: float = 5.0) -> None` | イベントを描画せずに垂直タイムラインを追加で `dy` 単位進めます。 |

---

## `class` Participant

上部ヘッダーカードと垂直破線ライフラインを持つ、シーケンス図のアクター・サービス・API エンドポイント・データベース列です。

```python
Participant(
    text: str = "",
    width: float = 20.0,
    height: float = 16.0,
    icon: IconType = None,
    icon_size: float = 8.0,
    style: Style | None = None,
    text_style: Style | None = None,
    card_style: Style | None = None,
    lifeline_style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: デフォルトでは上部ヘッダー行に沿って左から右へ `diagram.col_width` 間隔で自動配置されます。`d.add(p, x=...)` または `p.set_x(x)` で水平 X 座標を明示固定することも可能です。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `text` | `str` | `""` | ヘッダーカード内に表示する参加者ラベル（`\n` 改行対応）。 |
| `width` | `float` | `20.0` | ヘッダーカードの幅（ローカル単位）。 |
| `height` | `float` | `16.0` | ヘッダーカードの高さ（ローカル単位）。 |
| `icon` | `IconType` | `None` | [34 種類のアイコン列挙型](#icon-enums)、アイコン関数、[`CustomIcon`](#customicon)、[`Dimage`](04_images_and_math.md#dimage)、`PIL.Image.Image`、または画像パス。 |
| `icon_size` | `float` | `8.0` | アイコンの描画サイズ（ローカル単位）。 |
| `style` | `Style \| None` | `None` | ベクターアイコン着色用のスタイル上書き（未指定時は `diagram.node_style`）。 |
| `text_style` | `Style \| None` | `None` | ラベル用のテキストスタイル上書き（未指定時は `diagram.node_text_style`）。 |
| `card_style` | `Style \| None` | `None` | ヘッダーカードの背景・枠線スタイル上書き（未指定時は `diagram.node_card_style`）。 |
| `lifeline_style` | `Style \| None` | `None` | 垂直破線ライフライン用のストロークスタイル上書き。 |
| `show` | `bool` | `True` | 表示フラグ（`False` の場合、参加者・ライフライン・関連メッセージを非表示化）。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `activate` | `method` | `(self) -> None` | 現在のタイムラインステップから、この参加者のライフライン上に実行区間（アクティベーションバー）を開始します。 |
| `connect` | `method` | `(self, target: Participant, label: str = "", arrow: ArrowType = "->", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | `self` から `target` へカスタム矢印 [`Message`](#message) を送信します。 |
| `deactivate` | `method` | `(self) -> None` | この参加者のライフライン上で現在アクティブな実行区間バーを終了します。 |
| `get_header_size` | `method` | `(self) -> tuple[float, float]` | ヘッダーカードの `(width, height)` を返します。 |
| `get_size` | `method` | `(self) -> tuple[float, float]` | ヘッダーカードの `(width, height)` を返すエイリアスメソッドです。 |
| `note` | `method` | `(self, text: str, pos: Literal["left", "right"] = "right", style: Style \| None = None, show: bool = True) -> Note` | このライフラインの左側（`"left"`）または右側（`"right"`）に [`Note`](#note) 注釈カードを配置します。 |
| `reply` | `method` | `(self, target: Participant, label: str = "", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | `self` から `target` へ破線の応答 [`Message`](#message) を送信します。 |
| `request` | `method` | `(self, target: Participant, label: str = "", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | `self` から `target` へ実線のリクエスト [`Message`](#message) を送信します。 |
| `set_x` | `method` | `(self, x: float) -> Participant` | この参加者の水平ライフライン座標を `x` に明示固定し、`self` を返します。 |

---

## `class` ParticipantGroup

シーケンス図上部の連続する [`Participant`](#participant) ヘッダーカード群を囲むラベル付き境界ボックスです。

```python
ParticipantGroup(
    title: str = "",
    padding: float = 4.0,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: `group.add(participant)` で追加されたメンバー参加者のヘッダーカード群を囲むように水平・垂直範囲が自動計算されます。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `title` | `str` | `""` | グループ化された参加者ヘッダーの上部に描画されるバナータイトル。 |
| `padding` | `float` | `4.0` | 内包する参加者ヘッダーカード周囲の余白。 |
| `style` | `Style \| None` | `None` | 境界ボックスの背景・枠線スタイル。 |
| `text_style` | `Style \| None` | `None` | `title` 用のテキストスタイル上書き（左揃えを維持する場合は `halign="left"` を指定）。 |
| `show` | `bool` | `True` | グループ境界ボックスとタイトルを描画するかどうか。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, participant: Participant, *, show: bool \| None = None) -> Participant` | `participant` をこのグループに追加します（親 `SequenceDiagram` に接続済みの場合は図にも同時登録されます）。 |
| `participants` | `property` | `-> list[Participant]` | このグループに属する [`Participant`](#participant) の順序付きリストを返します。 |

---

## `class` Message

2 つの [`Participant`](#participant) ライフライン間（または自己呼び出しループ）の相互作用を表すメッセージ矢印オブジェクトです。`request()`、`reply()`、`connect()` から返されます。

```python
Message(
    source: Participant,
    target: Participant,
    label: str = "",
    is_reply: bool = False,
    is_async: bool = False,
    arrow: ArrowType = "->",
    style: Style | None = None,
    text_style: Style | None = None,
    padding: PaddingType = 0.0,
    show: bool = True,
) -> None
```

- **座標アンカー**: 該当ステップのタイムライン Y 座標において、`source` のライフライン X から `target` のライフライン X まで水平に描画されます（`source is target` の場合は右側へ折り返すループ矢印）。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `source` | [`Participant`](#participant) | *(必須)* | 送信元の参加者。 |
| `target` | [`Participant`](#participant) | *(必須)* | 宛先の参加者（自己再帰呼び出しの場合は `source` と同一インスタンスを指定）。 |
| `label` | `str` | `""` | 矢印の上部に描画されるメッセージ名・ペイロード説明。 |
| `is_reply` | `bool` | `False` | `True` の場合、実線ではなく破線の応答ラインとして描画します。 |
| `is_async` | `bool` | `False` | `True` の場合、塗りつぶし三角形ではなく開いた非同期矢印を描画します。 |
| `arrow` | `Literal["->", "<-", "<->", "-"]` | `"->"` | 矢印マーカーの方向設定。 |
| `style` | `Style \| None` | `None` | 矢印線のスタイル上書き（未指定時は `diagram.edge_style`）。 |
| `text_style` | `Style \| None` | `None` | ラベルテキストのスタイル上書き（未指定時は `diagram.edge_text_style`）。 |
| `padding` | `float \| tuple[float, float]` | `0.0` | 送受信ライフラインからの端点クリアランス余白。 |
| `show` | `bool` | `True` | このメッセージ矢印とラベルを描画するかどうか。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `is_self_call` | `property` | `-> bool` | `source is target`（右側折り返し自己呼び出しループ）の場合に `True` を返します。 |
| `set_arrow` | `method` | `(self, arrow: ArrowType) -> Message` | 矢印マーカーを更新し、`self` を返します。 |
| `set_async` | `method` | `(self, is_async: bool = True) -> Message` | 非同期オープン矢印スタイルを切り替え、`self` を返します。 |
| `set_label` | `method` | `(self, text: str) -> Message` | メッセージラベル文字列を更新し、`self` を返します。 |
| `set_padding` | `method` | `(self, padding: PaddingType) -> Message` | ライフライン端点の余白パディングを更新し、`self` を返します。 |
| `set_reply` | `method` | `(self, is_reply: bool = True) -> Message` | 破線応答ライン表示を切り替え、`self` を返します。 |
| `set_style` | `method` | `(self, style: Style) -> Message` | メッセージ線の [`Style`](05_styles_and_types.md#style) を上書きし、`self` を返します。 |
| `set_text_style` | `method` | `(self, text_style: Style) -> Message` | メッセージラベルの [`Style`](05_styles_and_types.md#style) を上書きし、`self` を返します。 |

---

## `class` Block

`d.loop()`、`d.alt()`、`d.else_()`、`d.opt()`、`d.par()` から Python の `with` コンテキストマネージャとして利用する UML 2.0 複合フラグメント（`loop`、`alt`、`else`、`opt`、`par`）です。

```python
Block(
    block_type: BlockType,
    label: str = "",
    diagram: SequenceDiagram | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: `with` ブロック内で記録された全メッセージの水平ライフライン範囲と垂直タイムライン区間を自動的に囲みます。

### コンストラクタ引数・変更可能属性

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `block_type` | `Literal["loop", "alt", "else", "opt", "par"]` | *(必須)* | 左上の五角形タブに表示される複合フラグメント演算子バッジ。 |
| `label` | `str` | `""` | 演算子バッジの横に表示されるガード条件またはループ反復式。 |
| `diagram` | `SequenceDiagram \| None` | `None` | 所属先の [`SequenceDiagram`](#sequencediagram) タイムラインマネージャ。 |
| `style` | `Style \| None` | `None` | フレーム枠線・背景スタイル（`with d.alt(...) as blk: blk.style = ...` で代入可能）。 |
| `text_style` | `Style \| None` | `None` | 演算子タブおよびガード条件のテキストスタイル。 |
| `show` | `bool` | `True` | ブロック枠線およびラベルタブを描画するかどうか。 |

---

## `class` Note

現在のタイムラインステップにおいて、単一の [`Participant`](#participant) ライフラインの脇、または複数のライフラインを跨いで配置される付箋ノート注釈カードです。

```python
Note(
    text: str,
    on: Participant | None = None,
    over: list[Participant] | None = None,
    pos: NotePosition = "right",
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: 現在の垂直タイムラインステップ位置で、`on` の `"left"` / `"right"`、または `over` 参加者群の水平スパン中央（`"over"`）に配置されます。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *(必須)* | ノートカード内に描画される注釈テキスト（`\n` 改行対応）。 |
| `on` | `Participant \| None` | `None` | 単一ライフライン基準で配置する場合の対象 [`Participant`](#participant)。 |
| `over` | `list[Participant] \| None` | `None` | 水平方向に跨いで配置する場合の対象参加者リスト。 |
| `pos` | `Literal["left", "right", "over"]` | `"right"` | `on` に対する配置位置（`"left"`、`"right"`、`"over"`）。 |
| `style` | `Style \| None` | `None` | ノートカード背景・枠線のスタイル上書き。 |
| `text_style` | `Style \| None` | `None` | ノート内テキストのタイポグラフィスタイル上書き。 |
| `show` | `bool` | `True` | このノートカードを描画するかどうか。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `set_style` | `method` | `(self, style: Style) -> Note` | ノートカード背景・枠線の [`Style`](05_styles_and_types.md#style) を上書きし、`self` を返します。 |
| `set_text` | `method` | `(self, text: str) -> Note` | ノートのテキスト内容を更新し、`self` を返します。 |
| `set_text_style` | `method` | `(self, text_style: Style) -> Note` | ノートテキストの [`Style`](05_styles_and_types.md#style) を上書きし、`self` を返します。 |

---

## `class` CustomIcon

任意のラスター画像ファイル、[`Dimage`](04_images_and_math.md#dimage) オブジェクト、または `PIL.Image.Image` インスタンスをラップし、`Participant(..., icon=CustomIcon(...))` として利用可能にするアダプタクラスです。

```python
CustomIcon(
    image: str | Path | Dimage | Image | CustomIcon,
) -> None
```

- **座標アンカー**: [`Participant`](#participant) ヘッダーカードのアイコンスロット中央に `icon_size` で自動配置されます。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `image` | `str \| Path \| Dimage \| Image \| CustomIcon` | *(必須)* | 画像ファイルパス、[`Dimage`](04_images_and_math.md#dimage) オブジェクト、`PIL.Image.Image`、または既存の `CustomIcon`。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `copy` | `method` | `(self) -> CustomIcon` | この `CustomIcon` の独立したディープコピーを返します。 |
| `dimage` | `property` | `-> Dimage` | 内部の [`Dimage`](04_images_and_math.md#dimage) インスタンスを返します。 |

---

## `type` icons

[`CustomIcon`](#customicon)、`IconType`、および全 34 種類のアイコン列挙型を再公開するサブモジュール名前空間（`drawlib.diagrams.sequence.icons`、[`drawlib.diagrams.architecture.icons`](19_diagrams_architecture.md#icons) と共通）です。

```python
from drawlib.diagrams.sequence import icons

api = Participant("Gateway", icon=icons.GcpIcon.CLOUD_ENDPOINTS)
```

- **座標アンカー**: 該当なし（40 個のアイコン型およびヘルパーを再公開する名前空間モジュール）。

| 公開グループ | 公開シンボル | 説明 |
| :--- | :--- | :--- |
| **アイコン列挙型 (34)** | `icons.AiIcon` .. `icons.WorkspaceIcon` | [`Icon Enums (34 Suites)`](#icon-enums) に一覧されている全 34 種類の `StrEnum` カタログ。 |
| **カスタムラッパー** | `icons.CustomIcon` | 参加者ヘッダー用カスタム画像の [`CustomIcon`](#customicon) エイリアス。 |
| **型エイリアス・ヘルパー** | `icons.IconType`, `icons.draw_node_icon` | `Participant(icon=...)` が受け付ける Union 型エイリアスおよび内部描画ヘルパー。 |

---

## `enum` Icon Enums (34 Suites)

`Participant(..., icon=<Enum>.<MEMBER>)` のヘッダーカードに宣言的に指定可能な、全 34 種類の標準アイコン `StrEnum` クラス群です（`drawlib.diagrams.sequence` 直下および `drawlib.diagrams.sequence.icons` の双方から再エクスポートされています）。`PhosphorIcon` は `participant.style` / `diagram.node_style` で着色され、残り 33 スイートは [`drawlib.icons`](08_icons.md) の PNG アセットを描画します。

| アイコン列挙型 | 対応する `drawlib.icons` スイート | カテゴリ・アセット種別 |
| :--- | :--- | :--- |
| `AiIcon` | [`drawlib.icons.ai`](08_icons.md#ai) | AI・LLM・機械学習プラットフォーム公式ブランドアイコン |
| `AwsIcon` | [`drawlib.icons.aws`](08_icons.md#aws) | Amazon Web Services 公式アーキテクチャアイコン |
| `AzureIcon` | [`drawlib.icons.azure`](08_icons.md#azure) | Microsoft Azure 公式アーキテクチャアイコン |
| `BusinessIcon` | [`drawlib.icons.business`](08_icons.md#business) | エンタープライズ SaaS・ERP・CRM・FinTech ブランドアイコン |
| `ClientIcon` | [`drawlib.icons.client`](08_icons.md#client) | ブラウザ・モバイル／デスクトップ OS・クライアント端末アイコン |
| `CloudIcon` | [`drawlib.icons.cloud`](08_icons.md#cloud) | クラウド・PaaS・CDN・ホスティングプロバイダアイコン |
| `CnativeIcon` | [`drawlib.icons.cnative`](08_icons.md#cnative) | Kubernetes および CNCF クラウドネイティブエコシステムアイコン |
| `CodeIcon` | [`drawlib.icons.code`](08_icons.md#code) | プログラミング言語・フレームワーク・ランタイムアイコン |
| `DataIcon` | [`drawlib.icons.data`](08_icons.md#data) | RDBMS・NoSQL・キャッシュ・ストリーミング基盤アイコン |
| `DevopsIcon` | [`drawlib.icons.devops`](08_icons.md#devops) | CI/CD・IaC・コンテナ・オブザーバビリティツールアイコン |
| `FacilityIcon` | [`drawlib.icons.facility`](08_icons.md#facility) | データセンター・ラック・通信キャリア・ハードウェアアイコン |
| `GcpIcon` | [`drawlib.icons.gcp`](08_icons.md#gcp) | Google Cloud Platform 公式アーキテクチャアイコン |
| `ItserviceIcon` | [`drawlib.icons.itservice`](08_icons.md#itservice) | IT サービス管理・コンサルティング・SIer ブランドアイコン |
| `NetworkIcon` | [`drawlib.icons.network`](08_icons.md#network) | ルータ・スイッチ・ファイアウォール・DNS・ネットワーク機器アイコン |
| `OriginalAiIcon` | [`drawlib.icons.original_ai`](08_icons.md#original-ai) | Drawlib ベンダー中立フラット AI・ML アイコン |
| `OriginalBusinessIcon` | [`drawlib.icons.original_business`](08_icons.md#original-business) | Drawlib ベンダー中立フラット ビジネス・業務アイコン |
| `OriginalClientIcon` | [`drawlib.icons.original_client`](08_icons.md#original-client) | Drawlib ベンダー中立フラット クライアント・端末アイコン |
| `OriginalCloudIcon` | [`drawlib.icons.original_cloud`](08_icons.md#original-cloud) | Drawlib ベンダー中立フラット クラウドサービスアイコン |
| `OriginalCnativeIcon` | [`drawlib.icons.original_cnative`](08_icons.md#original-cnative) | Drawlib ベンダー中立フラット クラウドネイティブアイコン |
| `OriginalCodeIcon` | [`drawlib.icons.original_code`](08_icons.md#original-code) | Drawlib ベンダー中立フラット コード・開発アイコン |
| `OriginalDataIcon` | [`drawlib.icons.original_data`](08_icons.md#original-data) | Drawlib ベンダー中立フラット データベース・ストレージアイコン |
| `OriginalDevopsIcon` | [`drawlib.icons.original_devops`](08_icons.md#original-devops) | Drawlib ベンダー中立フラット DevOps・パイプラインアイコン |
| `OriginalFacilityIcon` | [`drawlib.icons.original_facility`](08_icons.md#original-facility) | Drawlib ベンダー中立フラット 施設・ビルディングアイコン |
| `OriginalItserviceIcon` | [`drawlib.icons.original_itservice`](08_icons.md#original-itservice) | Drawlib ベンダー中立フラット IT 運用・サポートアイコン |
| `OriginalNetworkIcon` | [`drawlib.icons.original_network`](08_icons.md#original-network) | Drawlib ベンダー中立フラット ネットワーク機器アイコン |
| `OriginalSecurityIcon` | [`drawlib.icons.original_security`](08_icons.md#original-security) | Drawlib ベンダー中立フラット セキュリティ・IAM アイコン |
| `OriginalServerIcon` | [`drawlib.icons.original_server`](08_icons.md#original-server) | Drawlib ベンダー中立フラット サーバー・コンピュートアイコン |
| `OriginalSocialIcon` | [`drawlib.icons.original_social`](08_icons.md#original-social) | Drawlib ベンダー中立フラット ソーシャル・メッセージングアイコン |
| `OriginalWorkspaceIcon` | [`drawlib.icons.original_workspace`](08_icons.md#original-workspace) | Drawlib ベンダー中立フラット ワークスペース・コラボレーションアイコン |
| `PhosphorIcon` | [`drawlib.icons.phosphor`](08_icons.md#phosphor) | 1,530 種以上の単色着色対応 Phosphor UI ベクターフォントアイコン |
| `SecurityIcon` | [`drawlib.icons.security`](08_icons.md#security) | サイバーセキュリティ・IAM・コンプライアンス公式ブランドアイコン |
| `ServerIcon` | [`drawlib.icons.server`](08_icons.md#server) | Linux/Windows OS・ハイパーバイザ・サーバーハードウェアアイコン |
| `SocialIcon` | [`drawlib.icons.social`](08_icons.md#social) | ソーシャルプラットフォーム・開発者コミュニティ・チャットアイコン |
| `WorkspaceIcon` | [`drawlib.icons.workspace`](08_icons.md#workspace) | ドキュメント・グループウェア・チームコラボレーション SaaS アイコン |
