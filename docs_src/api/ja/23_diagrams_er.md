# drawlib.diagrams.er（ER データベース図）

IE（Information Engineering / Crow's Foot：カラスの足跡）記法の多重度マーカーと、行単位で厳密に揃う外部キー列アンカーを備えたリレーショナルデータベース ER（Entity-Relationship）スキーマ図モジュールです。標準インポート: `from drawlib.diagrams.er import Entity, ERDiagram, Relationship`。

```drawlib align=center code=fold file=23_diagrams_er_hero.png caption="カラム行単位の外部キーアンカーを用いた Crow's Foot 記法 ER スキーマ図"
from drawlib.canvas import save, setup
from drawlib.diagrams.er import Entity, ERDiagram
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.styles import Colors, Styles

setup(width=120, height=58)

erd = ERDiagram(
    node_style=Styles.Neutral.patch(text_font=FontSourceCode.ROBOTO_MONO, text_size=10.0),
    header_style=Styles.PrimaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=11.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)

users = erd.add(
    Entity("users", width=42, header_height=4.8, row_height=4.0)
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("email", "VARCHAR", nullable=False)
    .add_column("created_at", "TIMESTAMP", nullable=False),
    xy=(27.0, 43.0),
)

products = erd.add(
    Entity(
        "products",
        width=42,
        header_height=4.8,
        row_height=4.0,
        header_style=Styles.SecondaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=11.0),
    )
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("sku", "VARCHAR", nullable=False)
    .add_column("price", "INT", nullable=False),
    xy=(27.0, 15.0),
)

order_items = erd.add(
    Entity(
        "order_items",
        width=44,
        header_height=4.8,
        row_height=4.0,
        header_style=Styles.PrimaryFlat.patch(
            text_color=Colors.White, text_font=FontRoboto.ROBOTO_BOLD, text_size=11.0
        ),
    )
    .add_column("id", "BIGINT", pk=True, nullable=False)
    .add_column("user_id", "UUID", fk=True, nullable=False)
    .add_column("product_id", "UUID", fk=True, nullable=False)
    .add_column("qty", "INT", nullable=False),
    xy=(92.0, 29.0),
)

users.connect(
    order_items,
    cardinality="1:*",
    start_column="id",
    end_column="user_id",
    start_side="right",
    end_side="left",
)
products.connect(
    order_items,
    cardinality="1:*",
    start_column="id",
    end_column="product_id",
    start_side="right",
    end_side="left",
)

erd.draw(xy=(0.0, 0.0))
save()
```

---

## `type` Cardinality

[`Relationship`](#relationship) の始点 `start` と終点 `end` に描画される IE（Crow's Foot）記法の多重度マーカーを指定する Literal 型です。

```python
Cardinality = Literal["1:*", "1:1", "1:1..*", "1:0..1", "0..1:1", "0..1:*", "*:*"]
```

- **座標アンカー**: 解決された `start` および `end` のテーブル枠線またはカラム行アンカーの直外に描画されます。

| リテラル値 | `start` マーカー | `end` マーカー | リレーショナルモデルでの意味 |
| :--- | :--- | :--- | :--- |
| `"1:*"` | 必須 1（`\|\|`） | 0 以上・多（`o<` / `\|<`） | 標準的な 1 対多の外部キー参照（デフォルト）。 |
| `"1:1"` | 必須 1（`\|\|`） | 必須 1（`\|\|`） | 厳密な 1 対 1 対応。 |
| `"1:1..*"` | 必須 1（`\|\|`） | 1 以上・多（`\|<`） | 少なくとも 1 行の子レコードを必須とする 1 対多関連。 |
| `"1:0..1"` | 必須 1（`\|\|`） | 任意 0 または 1（`o\|`） | 親レコード必須・子レコード任意の 1 対 0..1 関連。 |
| `"0..1:1"` | 任意 0 または 1（`o\|`） | 必須 1（`\|\|`） | 始点任意・終点必須の 0..1 対 1 関連。 |
| `"0..1:*"` | 任意 0 または 1（`o\|`） | 多（`\|<`） | NULL 許容外部キーによる 0..1 対多関連。 |
| `"*:*"` | 多（`>\|`） | 多（`\|<`） | 多対多の論理関連。 |

---

## `class` ColumnInfo

[`Entity`](#entity) テーブル内の 1 カラム行を表すバリデーション付き Pydantic データモデルです。通常は `entity.add_column(...)` または `entity.add_columns([...])` から生成します。

```python
ColumnInfo(
    *,
    name: str,
    type: str = "",
    pk: bool = False,
    fk: bool = False,
    nullable: bool = True,
) -> None
```

- **座標アンカー**: [`Entity`](#entity) カード内に 3 列整列（`PK`/`FK` バッジ | カラム名 `name` | データ型 `type (NN)`）で描画され、`start_column` / `end_column` に `name` を指定することでその行の Y 座標に直接コネクタを接続できます。

### コンストラクタ引数・フィールド

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(必須)* | データベースカラム識別子（キーワード専用）。 |
| `type` | `str` | `""` | SQL データ型表記（例: `"UUID"`、`"VARCHAR(255)"`、`"BIGINT"`）。 |
| `pk` | `bool` | `False` | 主キー（Primary Key）としてマークします（`"PK"` バッジ表示・太字カラム名）。 |
| `fk` | `bool` | `False` | 外部キー（Foreign Key）としてマークします（`"FK"` または `"PK,FK"` バッジ表示）。 |
| `nullable` | `bool` | `True` | `False` の場合、データ型の横に `(NN)`（`NOT NULL`）を付加します。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `model_copy` | `method` | `(self, *, update: Mapping[str, Any] \| None = None, deep: bool = False) -> Self` | 任意のフィールド更新を伴う浅い／深いコピーを生成します（`pydantic.BaseModel`）。 |
| `model_dump` | `method` | `(self, *, mode: str = "python", ...) -> dict[str, Any]` | カラム情報を Python 辞書へシリアライズします（`pydantic.BaseModel`）。 |
| `model_dump_json` | `method` | `(self, *, indent: int \| None = None, ...) -> str` | カラム情報を JSON 文字列へシリアライズします（`pydantic.BaseModel`）。 |
| `model_validate` | `classmethod` | `(obj: Any, *, strict: bool \| None = None, ...) -> Self` | 任意の辞書やオブジェクトを検証して `ColumnInfo` を生成します。 |
| `model_validate_json` | `classmethod` | `(json_data: str \| bytes \| bytearray, ...) -> Self` | JSON データをパース・検証して `ColumnInfo` を生成します。 |
| `model_validate_strings` | `classmethod` | `(obj: Any, ...) -> Self` | 文字列値辞書を検証して `ColumnInfo` を生成します。 |
| `model_construct` | `classmethod` | `(_fields_set: set[str] \| None = None, **values: Any) -> Self` | バリデーションを省略してフィールド値から直接インスタンスを構築します。 |
| `model_json_schema` | `classmethod` | `(by_alias: bool = True, ...) -> dict[str, Any]` | `ColumnInfo` の JSON Schema 辞書を生成します。 |

*(このほか `pydantic.BaseModel` 標準の互換メンバー `model_extra`、`model_fields_set`、`model_parametrized_name`、`model_post_init`、`model_rebuild`、`construct`、`copy`、`dict`、`from_orm`、`json`、`parse_file`、`parse_obj`、`parse_raw`、`schema`、`schema_json`、`update_forward_refs`、`validate` を継承します。)*

---

## `class` ERDiagram

[`Entity`](#entity) テーブルカードおよび Crow's Foot 記法の [`Relationship`](#relationship) コネクタを管理する ER データベーススキーマ図のトップレベルコンテナです。

```python
ERDiagram(
    *,
    node_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    title: str = "",
    title_style: Style | None = None,
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
    header_style: Style | None = None,
) -> None
```

- **座標アンカー**: `draw(xy=(0.0, 0.0), align="bottom_left")` は図のローカル原点 `(0.0, 0.0)` をキャンバス座標 `xy` に配置します（`align="center"` の場合は `get_size()` の中心を `xy` に配置）。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `node_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | [`Entity`](#entity) テーブル本体、枠線、カラム文字列の基本スタイル（キーワード専用）。 |
| `edge_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | [`Relationship`](#relationship) 線および Crow's Foot マーカーの基本スタイル（キーワード専用）。 |
| `edge_text_style` | [`Style`](05_styles_and_types.md#style) | *(必須)* | リレーションラベルの基本テキストスタイル（キーワード専用）。 |
| `title` | `str` | `""` | スキーマ上部に中央揃えで描画される任意のタイトル。 |
| `title_style` | `Style \| None` | `None` | `title` 用の任意のテキストスタイル上書き。 |
| `width` | `float \| None` | `None` | ローカル単位での固定幅の任意上書き。 |
| `height` | `float \| None` | `None` | ローカル単位での固定高さの任意上書き。 |
| `style` | `Style \| None` | `None` | 図全体を囲む外枠コンテナの任意の背景・枠線スタイル。 |
| `header_style` | `Style \| None` | `None` | 個別指定がないエンティティのテーブル名ヘッダー帯に適用されるデフォルトスタイル。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, entity: Entity, xy: tuple[float, float], show: bool \| None = None) -> Entity` | ローカル座標 `xy` を中心として [`Entity`](#entity) テーブルを登録し、そのインスタンスを返します。 |
| `add_relationship` | `method` | `(self, relationship: Relationship) -> Relationship` | 構築済みの [`Relationship`](#relationship) インスタンスをこの図に登録します。 |
| `connect` | `method` | `(self, start: Entity, end: Entity, cardinality: Cardinality = "1:*", start_side: Side = "auto", end_side: Side = "auto", start_column: str \| None = None, end_column: str \| None = None, label: str = "", style: Style \| None = None, text_style: Style \| None = None, routing: RoutingType = "orthogonal", padding: PaddingType = 0.0, show: bool = True) -> Relationship` | `start` と `end` の間に Crow's Foot [`Relationship`](#relationship) を生成して登録します。 |
| `draw` | `method` | `(self, xy: tuple[float, float] = (0.0, 0.0), *, align: Literal["bottom_left", "center"] = "bottom_left", scale: PosFloat = 1.0) -> None` | アクティブなキャンバス上のアンカー `xy` に ER 図全体を描画します。 |
| `entities` | `property` | `-> list[Entity]` | 図に登録された [`Entity`](#entity) テーブルのリストを返します。 |
| `get_size` | `method` | `(self) -> tuple[float, float]` | スケール適用前のローカル単位での全体サイズ `(width, height)` を返します。 |
| `relationships` | `property` | `-> list[Relationship]` | 図に登録された [`Relationship`](#relationship) エッジのリストを返します。 |

---

## `class` Entity

上部ヘッダーバナーと 3 列構成のスキーマ行（`PK`/`FK` バッジ、カラム名、データ型＋NULL 制約）を持つデータベーステーブルカードです。

```python
Entity(
    name: str,
    width: float = 25.0,
    height: float | None = None,
    header_height: float = 4.0,
    row_height: float = 3.2,
    style: Style | None = None,
    header_style: Style | None = None,
    show: bool = True,
) -> None
```

- **座標アンカー**: `erd.add(entity, xy=(cx, cy))` で登録する際の**中心座標 `(cx, cy)`**。注目テーブルのヘッダーに `Styles.PrimaryFlat` を用いる場合は、必ず `header_style=Styles.PrimaryFlat.patch(text_color=Colors.White, text_size=11.0)` を指定して白文字のコントラストを確保してください。

### コンストラクタ引数

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(必須)* | 上部ヘッダー帯に表示されるテーブル名／エンティティ名。 |
| `width` | `float` | `25.0` | テーブルカード幅（SQL 型や `(NN)` を表示する場合は `36.0`〜`44.0` を推奨）。 |
| `height` | `float \| None` | `None` | 固定高さの上書き（`None` の場合は `header_height + max(len(columns), 1) * row_height` から自動算出）。 |
| `header_height` | `float` | `4.0` | 上部テーブル名ヘッダー帯の垂直高さ。 |
| `row_height` | `float` | `3.2` | カラム 1 行あたりの垂直高さ。 |
| `style` | `Style \| None` | `None` | カード本体・枠線・カラム文字列のスタイル上書き（未指定時は `erd.node_style`）。 |
| `header_style` | `Style \| None` | `None` | ヘッダー帯の塗り・枠線・文字スタイル上書き（未指定時は `erd.header_style`）。 |
| `show` | `bool` | `True` | 表示フラグ（`False` の場合、このエンティティと接続リレーションを非表示化）。 |

### パブリックメソッド・プロパティ

| メンバー | 種別 | シグネチャ | 説明 |
| :--- | :--- | :--- | :--- |
| `add_column` | `method` | `(self, name: str, type: str = "", pk: bool = False, fk: bool = False, nullable: bool = True) -> Entity` | [`ColumnInfo`](#columninfo) 行を末尾に追加し、メソッドチェーン用に `self` を返します。 |
| `add_columns` | `method` | `(self, columns: Sequence[Sequence[Any] \| ColumnInfo]) -> Entity` | タプル列 `(name, type, ...)` または `ColumnInfo` のリストを一括追加し、`self` を返します。 |
| `center` | `property` | `-> tuple[float, float]` | エンティティカードの相対中心座標 `(cx, cy)`。 |
| `connect` | `method` | `(self, target: Entity, cardinality: Cardinality = "1:*", start_side: Side = "auto", end_side: Side = "auto", start_column: str \| None = None, end_column: str \| None = None, label: str = "", style: Style \| None = None, text_style: Style \| None = None, routing: RoutingType = "orthogonal", padding: PaddingType = 0.0, show: bool = True) -> Relationship` | 登録済みエンティティから `target` への [`Relationship`](#relationship) を生成し、親 `ERDiagram` に登録します。 |
| `effective_height` | `property` | `-> float` | エンティティカードの実効描画高さ（ローカル単位）。 |
| `get_anchor` | `method` | `(self, side: Side, column_name: str \| None = None) -> tuple[float, float]` | 指定した `side` の境界座標を返します（`column_name` 指定時は該当行の Y 座標にスナップ）。 |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | 中心 `(0, 0)` 基準のローカル境界 `(-width/2, -effective_height/2, width/2, effective_height/2)` を返します。 |
| `xy` | `property` | `-> tuple[float, float]` | エンティティカードの相対中心座標 `(cx, cy)` を返すエイリアス。 |

---

## `class` Relationship

2 つの [`Entity`](#entity) テーブル間を、カード辺中点または厳密な外部キーカラム行（`start_column`、`end_column`）で結ぶ Crow's Foot リレーションエッジです。

```python
Relationship(
    start: Entity,
    end: Entity,
    cardinality: Cardinality = "1:*",
    start_side: Side = "auto",
    end_side: Side = "auto",
    start_column: str | None = None,
    end_column: str | None = None,
    label: str = "",
    style: Style | None = None,
    text_style: Style | None = None,
    routing: RoutingType = "orthogonal",
    padding: PaddingType = 0.0,
    show: bool = True,
) -> None
```

- **座標アンカー**: `start.get_anchor(start_side, start_column)` と `end.get_anchor(end_side, end_column)` に接続されます。`erd.connect(...)`、`entity.connect(...)`、または `erd.add_relationship(rel)` で登録します。

### コンストラクタ引数・属性

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `start` | [`Entity`](#entity) | *(必須)* | 始点となるエンティティテーブル。 |
| `end` | [`Entity`](#entity) | *(必須)* | 終点となるエンティティテーブル。 |
| `cardinality` | [`Cardinality`](#cardinality) | `"1:*"` | Crow's Foot 多重度表記（`"1:*"`、`"1:1"`、`"1:1..*"`、`"1:0..1"`、`"0..1:1"`、`"0..1:*"`、`"*:*"`）。 |
| `start_side` | [`Side`](#side) | `"auto"` | `start` 側の接続辺（`"left"`、`"right"`、`"top"`、`"bottom"`、`"auto"`）。 |
| `end_side` | [`Side`](#side) | `"auto"` | `end` 側の接続辺（`"left"`、`"right"`、`"top"`、`"bottom"`、`"auto"`）。 |
| `start_column` | `str \| None` | `None` | `start` 側で出発アンカーを一致させる対象カラム名（`"left"` / `"right"` 辺で行 Y スナップ）。 |
| `end_column` | `str \| None` | `None` | `end` 側で到着アンカーを一致させる対象カラム名（`"left"` / `"right"` 辺で行 Y スナップ）。 |
| `label` | `str` | `""` | コネクタ沿いに描画される任意の関連名・制約ラベル。 |
| `style` | `Style \| None` | `None` | 線スタイルの任意上書き（未指定時は `erd.edge_style`）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字スタイルの任意上書き（未指定時は `erd.edge_text_style`）。 |
| `routing` | [`RoutingType`](#routingtype) | `"orthogonal"` | 経路ルーティング方式（`"orthogonal"` または `"direct"`）。 |
| `padding` | `float \| tuple[float, float]` | `0.0` | エンティティ枠線と Crow's Foot 端点間のクリアランス余白。 |
| `show` | `bool` | `True` | このリレーションを描画するかどうか。 |

---

## `type` RoutingType

[`Relationship`](#relationship) コネクタの経路計算方式を指定する Literal 型です。

```python
RoutingType = Literal["orthogonal", "direct"]
```

- **座標アンカー**: 解決された `start` と `end` のエンティティ／カラムアンカー間の補間経路を制御します。

| リテラル値 | 経路ジオメトリ |
| :--- | :--- |
| `"orthogonal"` | 水平・垂直の直角マンハッタン折れ線セグメント（デフォルト。`start_column` / `end_column` との併用を推奨）。 |
| `"direct"` | 解決されたアンカー間を結ぶ直線セグメント。 |

---

## `type` Side

[`Entity`](#entity) カード上の接続辺を指定する Literal 型です。

```python
Side = Literal["left", "right", "top", "bottom", "auto"]
```

- **座標アンカー**: `"left"` と `"right"` は `start_column` / `end_column` と組み合わせることでカラム行単位の Y スナップを行います。`"auto"` は対向する最近傍の辺を自動選択します。
