# drawlib.diagrams.state（ステートマシン図）

`entry /`・`do /`・`exit /` 内部アクション区画、開始・終了・選択分岐（Choice）・並行同期バー（Fork/Join）疑似状態、自己遷移ループ、および曲線ガード遷移を備えた有限オートマトン（FSM）・UML 2.x ステートマシン図モジュールです。標準インポート: `from drawlib.diagrams.state import ChoiceState, FinalState, InitialState, State, StateDiagram`。

```drawlib align=center code=fold file=24_diagrams_state_hero.png caption="内部アクション区画・Choice 分岐ひし形・曲線リトライ遷移を用いた接続ステートマシン図"
from drawlib.canvas import save, setup
from drawlib.diagrams.state import ChoiceState, FinalState, InitialState, State, StateDiagram
from drawlib.styles import Colors, Styles

setup(width=120, height=54)

sd = StateDiagram(
    node_style=Styles.Neutral.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    margin=4.0,
)

init = sd.add(InitialState(), xy=(6.0, 34.0))
idle = sd.add(State("Idle", width=17, height=11), xy=(21.0, 34.0))
connecting = sd.add(
    State(
        "Connecting",
        entry="openSocket()",
        do="handshake()",
        width=29,
        style=Styles.PrimaryNeutral.patch(text_size=10.5),
    ),
    xy=(54.0, 34.0),
)
choice = sd.add(ChoiceState(style=Styles.SecondaryNeutral), xy=(80.0, 34.0))
connected = sd.add(
    State(
        "Connected",
        width=21,
        height=11,
        style=Styles.PrimaryFlat.patch(text_color=Colors.White, text_size=10.5),
    ),
    xy=(103.5, 34.0),
)
final = sd.add(FinalState(), xy=(103.5, 11.0))

sd.connect(init, idle, routing="direct", padding=0.8)
sd.connect(idle, connecting, event="connect", start_side="right", end_side="left", routing="direct", padding=0.8)
sd.connect(connecting, choice, event="done", start_side="right", end_side="left", routing="direct", padding=0.8)
sd.connect(choice, connected, guard="ok", start_side="right", end_side="left", routing="direct", padding=0.8)
sd.connect(choice, idle, guard="retry", start_side="bottom", end_side="bottom", bend=-0.26, padding=0.8)
sd.connect(
    connected,
    final,
    event="close",
    start_side="bottom",
    end_side="top",
    routing="direct",
    padding=0.8,
    text_style=Styles.Dark.patch(text_size=10.0, halign="left"),
)

sd.draw(xy=(60.0, 27.0), align="center")
save()
```

---

## `class` ChoiceState

ひし形（ダイヤモンド）として描画される UML 2.x の動的条件分岐（Choice）疑似状態です。[`StateNodeBase`](#statenodebase) のサブクラスです。

```python
ChoiceState(
    name: str = "",
    size: float = 4.5,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: `sd.add(choice, xy=(cx, cy))` で登録する際の**中心座標 `(cx, cy)`**。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | 分岐疑似状態の任意の識別子。 |
| `size` | `float` | `4.5` | ひし形の幅および高さ（ローカル単位）。 |
| `style` | `Style \| None` | `None` | 塗り・枠線のスタイル上書き（未指定時は `sd.node_style`）。 |
| `show` | `bool` | `True` | 表示フラグ（`False` の場合、ひし形と接続遷移を非表示化）。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | ひし形の相対中心座標 `(cx, cy)`。 |
| `effective_height` | `property` | `-> float` | 実効描画高さ（`size`）。 |
| `effective_width` | `property` | `-> float` | 実効描画幅（`size`）。 |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | 指定した `side` のひし形頂点／外周アンカー座標を返します。 |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | 中心 `(0, 0)` 基準のローカル境界 `(-size/2, -size/2, size/2, size/2)` を返します。 |
| `xy` | `property` | `-> tuple[float, float]` | 相対中心座標 `(cx, cy)` を返すエイリアス。 |

---

## `class` FinalState

外周リングと黒塗り内円からなる二重丸（ブルズアイ）として描画される UML 2.x 終了状態です。[`StateNodeBase`](#statenodebase) のサブクラスです。

```python
FinalState(
    name: str = "",
    radius: float = 2.2,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: `sd.add(final, xy=(cx, cy))` で登録する際の**中心座標 `(cx, cy)`**。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | 終了状態の任意の識別子。 |
| `radius` | `float` | `2.2` | 外周リングの半径（ローカル単位、全体の直径は `2 * radius`）。 |
| `style` | `Style \| None` | `None` | リングおよび内円の線・塗り色スタイル上書き。 |
| `show` | `bool` | `True` | 表示フラグ（`False` の場合、このノードと接続遷移を非表示化）。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | 二重丸の相対中心座標 `(cx, cy)`。 |
| `effective_height` | `property` | `-> float` | 実効描画直径（`2 * radius`）。 |
| `effective_width` | `property` | `-> float` | 実効描画直径（`2 * radius`）。 |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | 指定した `side` の外周リング境界座標を返します。 |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | 中心 `(0, 0)` 基準のローカル境界 `(-radius, -radius, radius, radius)` を返します。 |
| `xy` | `property` | `-> tuple[float, float]` | 相対中心座標 `(cx, cy)` を返すエイリアス。 |

---

## `class` ForkJoinState

単一遷移を複数の並行リージョンへ分岐（`fork`）または複数の並行リージョンを同期合流（`join`）させる UML 2.x の太線バー要素です。[`StateNodeBase`](#statenodebase) のサブクラスです。

```python
ForkJoinState(
    name: str = "",
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    length: float = 16.0,
    thickness: float = 1.8,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: `sd.add(bar, xy=(cx, cy))` で登録する際の**中心座標 `(cx, cy)`**。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | Fork/Join バーの任意の識別子。 |
| `orientation` | `Literal["horizontal", "vertical"]` | `"horizontal"` | バーの向き（上下フロー向けの横長バー `"horizontal"`、左右フロー向けの縦長バー `"vertical"`）。 |
| `length` | `float` | `16.0` | `orientation` 軸方向のバー長（ローカル単位）。 |
| `thickness` | `float` | `1.8` | 直交軸方向のバーの厚み（ローカル単位）。 |
| `style` | `Style \| None` | `None` | バーの塗りつぶしスタイル上書き。 |
| `show` | `bool` | `True` | 表示フラグ（`False` の場合、バーと接続遷移を非表示化）。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | 同期バーの相対中心座標 `(cx, cy)`。 |
| `effective_height` | `property` | `-> float` | 描画高さ（`"horizontal"` 時は `thickness`、`"vertical"` 時は `length`）。 |
| `effective_width` | `property` | `-> float` | 描画幅（`"horizontal"` 時は `length`、`"vertical"` 時は `thickness`）。 |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | 指定した `side` の境界座標を返します。 |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | 中心 `(0, 0)` 基準のローカル境界 `(min_x, min_y, max_x, max_y)` を返します。 |
| `xy` | `property` | `-> tuple[float, float]` | 相対中心座標 `(cx, cy)` を返すエイリアス。 |

---

## `class` InitialState

ステートマシンの開始点を示す塗りつぶし黒丸の UML 2.x 開始疑似状態です。[`StateNodeBase`](#statenodebase) のサブクラスです。

```python
InitialState(
    name: str = "",
    radius: float = 1.75,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: `sd.add(init, xy=(cx, cy))` で登録する際の**中心座標 `(cx, cy)`**。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | 開始疑似状態の任意の識別子。 |
| `radius` | `float` | `1.75` | 塗りつぶし円の半径（ローカル単位、直径は `3.5`）。 |
| `style` | `Style \| None` | `None` | 塗りつぶし色のスタイル上書き。 |
| `show` | `bool` | `True` | 表示フラグ（`False` の場合、このノードと出力遷移を非表示化）。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | 円の相対中心座標 `(cx, cy)`。 |
| `effective_height` | `property` | `-> float` | 実効描画直径（`2 * radius`）。 |
| `effective_width` | `property` | `-> float` | 実効描画直径（`2 * radius`）。 |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | 指定した `side` の外周アンカー座標を返します。 |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | 中心 `(0, 0)` 基準のローカル境界 `(-radius, -radius, radius, radius)` を返します。 |
| `xy` | `property` | `-> tuple[float, float]` | 相対中心座標 `(cx, cy)` を返すエイリアス。 |

---

## `type` PaddingType

[`StateTransition`](#statetransition) 矢印の両端に設けるクリアランス余白距離を表す Union 型エイリアスです。

```python
PaddingType = float | tuple[float, float]
```

- **座標アンカー**: `start` と `end` の状態ノード外周から遷移矢印の端点を外側に離す距離を指定します（対称な `float` または `(start_pad, end_pad)` タプル）。

---

## `type` RoutingType

[`StateTransition`](#statetransition) コネクタの曲線／折れ線ジオメトリを制御する Literal 型です。

```python
RoutingType = Literal["curved", "orthogonal", "direct"]
```

- **座標アンカー**: 解決された `start` と `end` の境界アンカー間の補間経路を制御します。

| リテラル値 | 経路ジオメトリ |
| :--- | :--- |
| `"curved"` | `bend` で曲率を制御する滑らかな二次曲線アーク（デフォルト。双方向 `A <-> B` 遷移の分離に最適）。 |
| `"orthogonal"` | 水平・垂直の直角マンハッタン折れ線セグメント。 |
| `"direct"` | 解決されたアンカー間を直線で結ぶユークリッド線分。 |

---

## `type` ShapeType

[`State`](#state) ノードの外形図形を選択する Literal 型です。

```python
ShapeType = Literal["box", "ellipse", "circle", "double_circle", "text_only"]
```

- **座標アンカー**: すべての状態図形は `(cx, cy)` を中心として描画されます。

| リテラル値 | 描画形状 | 主な用途 |
| :--- | :--- | :--- |
| `"box"` | 角丸長方形（内部アクション指定時は区切り線付き 2 区画） | UML 2.x 標準のステートチャート状態（デフォルト）。 |
| `"ellipse"` | 楕円 | 概念的な状態遷移図や Moore/Mealy マシン。 |
| `"circle"` | 一重円 | 形式言語・オートマトン理論の DFA / NFA 状態頂点（`q0`、`q1`）。 |
| `"double_circle"` | 同心二重円 | DFA / NFA の受理状態（Accepting State）。 |
| `"text_only"` | 枠線なしのテキストラベル | 最小構成のテキスト状態表現。 |

---

## `type` Side

[`StateNodeBase`](#statenodebase) ノード上の接続ポート位置（四隅の対角方向を含む）を指定する Literal 型です。

```python
Side = Literal[
    "left",
    "right",
    "top",
    "bottom",
    "auto",
    "top_right",
    "top_left",
    "bottom_right",
    "bottom_left",
]
```

- **座標アンカー**: 角丸長方形、円、楕円、ひし形の外周境界上の座標に解決されます（`"auto"` は対向する最近傍の位置を自動選択）。

---

## `class` State

UML 2.x の角丸ボックス状態（`entry /`・`do /`・`exit /` 内部振る舞い区画に対応）および形式オートマトンの円・二重円状態を表現する主要状態クラスです。[`StateNodeBase`](#statenodebase) のサブクラスです。

```python
State(
    name: str,
    shape: ShapeType = "box",
    entry: str = "",
    do: str = "",
    exit: str = "",
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: `sd.add(state, xy=(cx, cy))` で登録する際の**中心座標 `(cx, cy)`**。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(必須)* | メイン区画（内部アクションがある場合は上段ヘッダー）に描画される状態名。 |
| `shape` | [`ShapeType`](#shapetype) | `"box"` | ノード図形種別（`"box"`、`"ellipse"`、`"circle"`、`"double_circle"`、`"text_only"`）。 |
| `entry` | `str` | `""` | `"box"` 状態で `entry / <entry>` として整形表示される入場アクション。 |
| `do` | `str` | `""` | `"box"` 状態で `do / <do>` として整形表示される継続アクティビティ。 |
| `exit` | `str` | `""` | `"box"` 状態で `exit / <exit>` として整形表示される退場アクション。 |
| `width` | `float \| None` | `None` | 明示的な固定幅（`None` の場合は状態名およびアクション文字列長から自動算出）。 |
| `height` | `float \| None` | `None` | 明示的な固定高さ（`None` の場合はヘッダー＋アクション行数から自動算出）。 |
| `style` | `Style \| None` | `None` | 塗り・枠線・文字スタイルの任意上書き（未指定時は `sd.node_style`）。 |
| `show` | `bool` | `True` | 表示フラグ（`False` の場合、この状態と接続遷移を非表示化）。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `add_action` | `method` | `(self, kind: str, action: str) -> State` | 内部区画にカスタム [`StateAction`](#stateaction) 行（`"{kind} / {action}"`）を追加し、`self` を返します。 |
| `center` | `property` | `-> tuple[float, float]` | 状態ノードの相対中心座標 `(cx, cy)`。 |
| `effective_height` | `property` | `-> float` | 算出された実効描画高さ。 |
| `effective_width` | `property` | `-> float` | 算出された実効描画幅。 |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | 指定した `side` の外周アンカー座標を返します。 |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | 中心 `(0, 0)` 基準のローカル境界 `(-effective_width/2, -effective_height/2, ...)` を返します。 |
| `xy` | `property` | `-> tuple[float, float]` | 相対中心座標 `(cx, cy)` を返すエイリアス。 |

---

## `class` StateAction

[`State`](#state) ボックス内の内部アクティビティ 1 行（`entry /`、`do /`、`exit /`、または任意の内部イベントトリガー）を表すバリデーション付き Pydantic データモデルです。通常は `State(..., entry=..., do=..., exit=...)` または `state.add_action(kind, action)` から登録します。

```python
StateAction(
    *,
    kind: str,
    action: str,
) -> None
```

- **座標アンカー**: `"box"` 形状の [`State`](#state) の下段区画内に左揃えで描画されます。

### コンストラクタ引数・フィールド

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `kind` | `str` | *(必須)* | `"entry"`、`"do"`、`"exit"`、または内部イベント名などのトリガー種別（キーワード専用）。 |
| `action` | `str` | *(必須)* | 実行される振る舞い式または関数シグネチャ文字列（キーワード専用）。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `display_text` | `property` | `-> str` | フォーマット済みの UML 内部アクション文字列（`"{kind} / {action}"`）。 |
| `model_copy` | `method` | `(self, *, update: Mapping[str, Any] \| None = None, deep: bool = False) -> Self` | 任意のフィールド更新を伴う浅い／深いコピーを生成します（`pydantic.BaseModel`）。 |
| `model_dump` | `method` | `(self, *, mode: str = "python", ...) -> dict[str, Any]` | フィールドを Python 辞書へシリアライズします（`pydantic.BaseModel`）。 |
| `model_dump_json` | `method` | `(self, *, indent: int \| None = None, ...) -> str` | フィールドを JSON 文字列へシリアライズします（`pydantic.BaseModel`）。 |
| `model_validate` | `classmethod` | `(obj: Any, *, strict: bool \| None = None, ...) -> Self` | 任意の辞書やオブジェクトを検証して `StateAction` を生成します。 |
| `model_validate_json` | `classmethod` | `(json_data: str \| bytes \| bytearray, ...) -> Self` | JSON データをパース・検証して `StateAction` を生成します。 |
| `model_validate_strings` | `classmethod` | `(obj: Any, ...) -> Self` | 文字列値辞書を検証して `StateAction` を生成します。 |
| `model_construct` | `classmethod` | `(_fields_set: set[str] \| None = None, **values: Any) -> Self` | バリデーションを省略してフィールド値から直接インスタンスを構築します。 |
| `model_json_schema` | `classmethod` | `(by_alias: bool = True, ...) -> dict[str, Any]` | `StateAction` の JSON Schema 辞書を生成します。 |

*(このほか `pydantic.BaseModel` 標準の互換メンバー `model_extra`、`model_fields_set`、`model_parametrized_name`、`model_post_init`、`model_rebuild`、`construct`、`copy`、`dict`、`from_orm`、`json`、`parse_file`、`parse_obj`、`parse_raw`、`schema`、`schema_json`、`update_forward_refs`、`validate` を継承します。)*

---

## `class` StateDiagram

状態ノード、疑似状態、状態遷移エッジ、および全体のバウンディングボックス配置を統合管理する UML ステートチャート・FSM 図のトップレベルコンテナです。

```python
StateDiagram(
    *,
    node_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    title: str = "",
    title_style: Style | None = None,
    style: Style | None = None,
    width: float | None = None,
    height: float | None = None,
    margin: float = 5.0,
) -> None
```

- **座標アンカー**: `draw(xy=(0.0, 0.0), align="bottom_left")` はローカル座標を `xy` 分シフトして描画します（`align="center"` の場合は `get_bounds()` の包含中心を `xy` に配置）。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `node_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | 状態ノードおよび疑似状態に適用される基本スタイル（キーワード専用）。 |
| `edge_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | [`StateTransition`](#statetransition) 遷移線の基本ストローク・矢印スタイル（キーワード専用）。 |
| `edge_text_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | 遷移ラベル `event [guard] / action` の基本テキストスタイル（キーワード専用）。 |
| `title` | `str` | `""` | 図の上部中央に描画される任意のタイトル。 |
| `title_style` | `Style \| None` | `None` | `title` 用の任意のテキストスタイル上書き。 |
| `style` | `Style \| None` | `None` | 図全体を囲む外枠カードの任意の背景・枠線スタイル。 |
| `width` | `float \| None` | `None` | 固定幅の任意上書き（`None` の場合は `get_bounds()` + `margin` から自動算出）。 |
| `height` | `float \| None` | `None` | 固定高さの任意上書き（`None` の場合は `get_bounds()` + `margin` から自動算出）。 |
| `margin` | `float` | `5.0` | 全状態および自己遷移ループ周囲の外側マージン余白。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, item: NodeT, xy: tuple[float, float] = (0.0, 0.0), width: float \| None = None, height: float \| None = None, style: Style \| None = None, show: bool \| None = None) -> NodeT` | 座標 `xy` を中心として [`State`](#state) または疑似状態を登録し（サイズ・スタイルのその場上書きに対応）、返します。 |
| `add_transition` | `method` | `(self, trans: StateTransition) -> StateTransition` | 構築済みの [`StateTransition`](#statetransition) をこの図に登録します。 |
| `connect` | `method` | `(self, source: StateNodeBase, target: StateNodeBase, *, label: str = "", event: str = "", guard: str = "", action: str = "", side: LoopSide = "top", bend: float = 0.0, start_side: Side = "auto", end_side: Side = "auto", routing: RoutingType = "curved", style: Style \| None = None, text_style: Style \| None = None, padding: PaddingType = 0.0, loop_width: float \| None = None, loop_height: float \| None = None, loop_ratio: float = 0.88, show: bool = True) -> StateTransition` | [`StateTransition`](#statetransition)（`source is target` の場合は自己遷移ループ）を生成・登録します。 |
| `draw` | `method` | `(self, xy: tuple[float, float] = (0.0, 0.0), *, align: Literal["bottom_left", "center"] = "bottom_left", scale: PosFloat = 1.0) -> None` | アクティブなキャンバス上のアンカー `xy` にステートマシン図を描画します。 |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | 全状態ノードおよび自己遷移ループを囲む `(min_x, min_y, max_x, max_y)` を算出します。 |
| `get_size` | `method` | `(self) -> tuple[float, float]` | `margin` を含めた図全体の `(width, height)` を算出します。 |

---

## `class` StateNodeBase

[`State`](#state)、[`InitialState`](#initialstate)、[`FinalState`](#finalstate)、[`ChoiceState`](#choicestate)、および [`ForkJoinState`](#forkjoinstate) が共有する基底状態ノードクラスです。

```python
StateNodeBase(
    name: str = "",
    width: float = 20.0,
    height: float = 12.0,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: [`StateDiagram`](#statediagram) に登録する際の**中心座標 `(cx, cy)`**。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | 状態ノードの識別子またはラベル文字列。 |
| `width` | `float` | `20.0` | 基本バウンディング幅（ローカル単位）。 |
| `height` | `float` | `12.0` | 基本バウンディング高さ（ローカル単位）。 |
| `style` | `Style \| None` | `None` | 任意の [`Style`](05_styles_and_types.md#style) 上書き。 |
| `show` | `bool` | `True` | この状態ノードの表示フラグ。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | 状態ノードの相対中心座標 `(cx, cy)`。 |
| `effective_height` | `property` | `-> float` | 状態ノードの実効描画高さ。 |
| `effective_width` | `property` | `-> float` | 状態ノードの実効描画幅。 |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | 指定した `side` の境界アンカー座標を返します。 |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | 中心 `(0, 0)` 基準のローカル境界 `(min_x, min_y, max_x, max_y)` を返します。 |
| `xy` | `property` | `-> tuple[float, float]` | 相対中心座標 `(cx, cy)` を返すエイリアス。 |

---

## `class` StateTransition

UML 標準の `"event [guard] / action"` ラベル自動整形を備えた、2 つの [`StateNodeBase`](#statenodebase) 間を結ぶ有向状態遷移エッジ（または自己遷移楕円ループ）です。

```python
StateTransition(
    start: StateNodeBase,
    end: StateNodeBase,
    label: str = "",
    event: str = "",
    guard: str = "",
    action: str = "",
    bend: float = 0.0,
    start_side: Side = "auto",
    end_side: Side = "auto",
    routing: RoutingType = "curved",
    style: Style | None = None,
    text_style: Style | None = None,
    padding: PaddingType = 0.0,
    loop_side: LoopSide = "top",
    loop_width: float | None = None,
    loop_height: float | None = None,
    loop_ratio: float = 0.88,
    is_loop: bool = False,
    show: bool = True,
) -> None
```

- **座標アンカー**: `start` の `start_side` から `end` の `end_side` へ接続されます（`start is end` の場合は `loop_side` に自己遷移ループ円弧を描画）。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `start` | [`StateNodeBase`](#statenodebase) | *(必須)* | 遷移元の状態または疑似状態。 |
| `end` | [`StateNodeBase`](#statenodebase) | *(必須)* | 遷移先の状態または疑似状態（自己遷移の場合は `start` と同一）。 |
| `label` | `str` | `""` | 明示的な完全遷移ラベル（非空の場合は `event`/`guard`/`action` の自動整形より優先）。 |
| `event` | `str` | `""` | `"event [guard] / action"` の先頭に配置されるトリガーイベント名。 |
| `guard` | `str` | `""` | 自動的に角括弧 `[guard]` で囲まれるガード条件式。 |
| `action` | `str` | `""` | 自動的に `/ action` 形式で付加される遷移時アクション。 |
| `bend` | `float` | `0.0` | `"curved"` ルーティング時の弧のたわみ量（`0.0` で直線、`0.25`〜`0.45` で往復遷移の分離に有効）。 |
| `start_side` | [`Side`](#side) | `"auto"` | `start` 側の出発アンカー位置。 |
| `end_side` | [`Side`](#side) | `"auto"` | `end` 側の到着アンカー位置。 |
| `routing` | [`RoutingType`](#routingtype) | `"curved"` | 経路ルーティング方式（`"curved"`、`"orthogonal"`、`"direct"`）。 |
| `style` | `Style \| None` | `None` | 遷移線スタイルの任意上書き（未指定時は `sd.edge_style`）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字スタイルの任意上書き（未指定時は `sd.edge_text_style`）。 |
| `padding` | [`PaddingType`](#paddingtype) | `0.0` | 状態境界と遷移矢印端点間のクリアランス余白。 |
| `loop_side` | `Literal["top", "bottom", "left", "right", ...]` | `"top"` | 自己遷移ループの配置辺（`sd.connect(..., side=...)` から転送）。 |
| `loop_width` | `float \| None` | `None` | 自己遷移ループ楕円のカスタム幅。 |
| `loop_height` | `float \| None` | `None` | 自己遷移ループ楕円のカスタム高さ。 |
| `loop_ratio` | `float` | `0.88` | 自己遷移ループ楕円を描画する円周比率（`0.0`〜`1.0`）。 |
| `is_loop` | `bool` | `False` | 明示的な自己遷移フラグ（`start is end` の場合は自動的に `True`）。 |
| `show` | `bool` | `True` | この遷移を描画するかどうか。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `effective_label` | `property` | `-> str` | 解決された遷移ラベル文字列（`label` が非空ならその値、それ以外は `"event [guard] / action"` 整形結果）。 |
| `is_self_transition` | `property` | `-> bool` | 同一状態へ戻る自己遷移（`is_loop` または `start is end`）の場合に `True`。 |
