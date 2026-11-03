# drawlib.smartarts（フロー・ツリー・マップ・カレンダー）

`from drawlib.smartarts import ...` からインポートできる高水準 SmartArt コンポーネントのうち、シェブロン工程図・円形サイクル・階層ピラミッド・マイルストーンロードマップ・ディレクトリツリー・放射状マインドマップ・GeoJSON ベクター地図・日次／週次／月次スケジュールカレンダーを網羅します。ボックスリスト・箇条書き・バッジ付きカード・パネル・KPI カード・グリッド・ソースコード・テーブルについては [drawlib.smartarts（リスト・カード・KPI・テーブル）](09_smartarts_lists_cards.md) を参照してください。

```drawlib align=center code=fold file=10_smartarts_flows_trees_maps_hero.png caption="SmartArts パート2 — ChevronProcess・TreeNode・放射状 Cycle"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.smartarts import ChevronProcess, Cycle, TreeNode
from drawlib.styles import Colors, Styles

setup(width=120, height=56)

# Left Top: Sequential ChevronProcess Pipeline (Bottom-Left at (5, 38))
pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
pipeline.add("1. Plan", description="RFC")
pipeline.add("2. Build", description="Verify", style=Styles.PrimaryNeutral)
pipeline.add(
    "3. Ship",
    description="Canary",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=10.0),
)
pipeline.draw(xy=(5.0, 38.0), width=59.0, height=13.0, align="bottom_left")

# Left Bottom: TreeNode Hierarchy with Phosphor Icons (Top-Left at (6, 31))
TreeNode.register_drawing_item(
    name="hero_dir",
    location="before",
    padding_width=4.2,
    function=phosphor.folder,
    style=Styles.Primary.patch(icon_color=Colors.Primary),
    args={"width": 2.8},
)
TreeNode.register_drawing_item(
    name="hero_py",
    location="before",
    padding_width=4.2,
    function=phosphor.file_py,
    style=Styles.Dark,
    args={"width": 2.8},
)

root = TreeNode(
    "drawlib-service/",
    text_style=Styles.DarkBold.patch(text_size=10.5),
    line_style=Styles.Muted.patch(line_width=1.1),
    line_horizontal_margin=2.8,
    line_horizontal_length=2.8,
    line_vertical_margin=6.0,
    children=[
        TreeNode(
            "src/api/",
            text_style=Styles.DarkBold.patch(text_size=10.2),
            children=[
                TreeNode("router.py", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("hero_py"),
                TreeNode("worker.py", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("hero_py"),
            ],
        ).set_drawing_item("hero_dir"),
        TreeNode("deploy.py", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("hero_py"),
    ],
).set_drawing_item("hero_dir")
root.draw(xy=(6.0, 31.0))

line((67.5, 6.0), (67.5, 50.0), style=Styles.MutedDashed)

# Right: Radial Cycle with Central Hub (Center anchored at (93, 28))
cycle = Cycle(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    arrow_style=Styles.DarkFlat,
    clockwise=True,
    start_angle=90.0,
    node_shape="circle",
    node_radius=6.6,
    arrow_type="arc",
    arrow_width=1.4,
    arrow_head_width=3.6,
    arrow_color_mode="monochrome",
    arrow_gap=2.2,
)
cycle.add("Plan", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=10.5))
cycle.add("Code", style=Styles.PrimaryNeutral)
cycle.add("Test", style=Styles.SecondaryNeutral)
cycle.add("Ops", style=Styles.Neutral)
cycle.set_center(
    "PDCA",
    radius=6.8,
    style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
cycle.draw(xy=(93.0, 28.0), radius=15.2, align="center")

save()
```

## `class` ChevronProcess

矢羽根型（シェブロン）ブロックが水平方向に噛み合う順次プロセスパイプラインを描画します。各ステップへの補足説明（`description`）・先頭左端の垂直フラット化（`flat_left_end=True`）・特定フェーズのハイライト装飾に対応します。

- **座標アンカー:** デフォルトは **左下（Bottom-Left）** `(x, y)`（`align="bottom_left"`）、または **中央（Center）** `(cx, cy)`（`align="center"`）。

```python
ChevronProcess(
    *,
    style: Style,
    text_style: Style,
    description_style: Style,
    corner_angle: Angle90 = 60.0,
    spacing: PosFloat = 1.5,
    flat_left_end: bool = False,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *必須* | シェブロン多角形のデフォルト塗り・枠線スタイル。 |
| `text_style` | `Style` | *必須* | ステップ主タイトルのデフォルトテキストスタイル。 |
| `description_style` | `Style` | *必須* | ステップ補足説明のデフォルトテキストスタイル。 |
| `corner_angle` | `Angle90` | `60.0` | 矢羽根先端の傾斜角（度数法 `10.0`〜`80.0`、先端の食い込み深さを制御）。 |
| `spacing` | `PosFloat` | `1.5` | 隣接シェブロン間の水平ギャップ（キャンバス単位）。 |
| `flat_left_end` | `bool` | `False` | `True` の場合、先頭シェブロンの左端をくぼみなしの垂直線として描画します。 |

### メソッド・プロパティ

```python
pipeline.items -> list[ChevronItem]

pipeline.add(
    text: str,
    *,
    description: str = "",
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> ChevronItem

pipeline.draw(
    xy: Coordinate,
    width: PosFloat = 90.0,
    height: PosFloat = 12.0,
    item_width: PosFloat | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `items` | `property` | 登録済み `ChevronItem` インスタンスのリスト（`list[ChevronItem]`）を返します。 |
| `add(text, *, description="", style=None, text_style=None, description_style=None, show=True)` | `method` | プロセスステップを追加し、`ChevronItem` を返します。`show=False` にすると他のステップ幅・座標を保ったまま非表示にします。 |
| `draw(xy, width=90.0, height=12.0, item_width=None, align="bottom_left", scale=1.0)` | `method` | `xy` にパイプラインを描画します（`item_width=None` 時は全体幅 `width` から各ブロック幅を均等自動配分）。`self` を返します。 |

## `class` ChevronItem

`ChevronProcess` 内の単一ステップのテキスト・スタイル・表示状態を保持する可変 Pydantic モデルです。

- **座標アンカー:** 親 `ChevronProcess` の水平軸上に自動配置されます。

```python
ChevronItem(
    *,
    text: str,
    style: Style,
    text_style: Style,
    description_style: Style,
    description: str = "",
    show: bool = True,
) -> None
```

| 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *必須* | シェブロン中央に描画される主タイトル文字列。 |
| `style` | `Style` | *必須* | シェブロン多角形の塗り・枠線スタイル。 |
| `text_style` | `Style` | *必須* | `text` のテキストスタイル。 |
| `description_style` | `Style` | *必須* | `description` のテキストスタイル。 |
| `description` | `str` | `""` | `text` の下に描画される任意の補足説明文字列。 |
| `show` | `bool` | `True` | 表示フラグ。`False` の場合、パイプライン全体の配置を保ったまま描画をスキップします。 |

### メソッド・プロパティ

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | フィールド更新を伴うステップモデルの複製を返します（`pydantic.BaseModel`）。 |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Pydantic 標準の直列化・検証メソッド群（`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`）。 |

## `class` Cycle

PDCA ループ・SRE インシデント対応ライフサイクル・トークン更新サイクルなどの循環プロセスを描画するコンポーネントです。円形・矩形・枠なしの周回ノード、円弧ブロック矢印または曲線矢印、さらに中央ハブノード（`CycleCenter`）に対応します。

- **座標アンカー:** デフォルトは周回軌道の **中央（Center）** `(cx, cy)`（`align="center"`）、または全体外接枠の **左下（Bottom-Left）** `(x, y)`（`align="bottom_left"`）。

```python
Cycle(
    *,
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    arrow_style: Style | None = None,
    clockwise: bool = True,
    start_angle: Angle = 90.0,
    node_shape: Literal["circle", "rectangle", "none"] = "circle",
    node_radius: PosFloat = 8.0,
    node_width: PosFloat = 18.0,
    node_height: PosFloat = 10.0,
    description_placement: Literal["inside", "outside"] = "inside",
    arrow_type: Literal["arc", "line", "none"] = "arc",
    arrow_width: PosFloat = 2.0,
    arrow_head_width: PosFloat = 4.5,
    arrow_color_mode: Literal["monochrome", "match_source", "match_target"] = "match_source",
    arrow_gap: PosFloat = 2.5,
    center_text: str = "",
    center_description: str = "",
    center_radius: PosFloat = 10.0,
    center_style: Style | None = None,
    center_text_style: Style | None = None,
    center_description_style: Style | None = None,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *必須* | 周回ノードのデフォルト塗り・枠線スタイル。 |
| `text_style` | `Style` | *必須* | 周回ノードタイトルのデフォルトテキストスタイル。 |
| `description_style` | `Style \| None` | `None` | 周回ノード補足説明のデフォルトテキストスタイル。 |
| `arrow_style` | `Style \| None` | `None` | 矢印のデフォルトスタイル（`arrow_color_mode="monochrome"` かつ `arrow_type != "none"` 時は必須）。 |
| `clockwise` | `bool` | `True` | `True` は `start_angle` から時計回り、`False` は反時計回りに配置します。 |
| `start_angle` | `Angle` | `90.0` | 先頭要素 `items[0]` の極座標角度（`90.0` で12時方向）。 |
| `node_shape` | `Literal["circle", "rectangle", "none"]` | `"circle"` | 周回ノードの図形種別（`"none"` は枠なしテキストのみ）。 |
| `node_radius` | `PosFloat` | `8.0` | `node_shape="circle"` 時の各ノード半径。 |
| `node_width` | `PosFloat` | `18.0` | `node_shape="rectangle"` 時の各ノード幅。 |
| `node_height` | `PosFloat` | `10.0` | `node_shape="rectangle"` 時の各ノード高さ。 |
| `description_placement` | `Literal["inside", "outside"]` | `"inside"` | `description` をノード内部に配置するか、軌道外側へ放射配置するか。 |
| `arrow_type` | `Literal["arc", "line", "none"]` | `"arc"` | ノード間矢印の種別（`"arc"` 円弧ブロック矢印、`"line"` 曲線矢印、`"none"` 非表示）。 |
| `arrow_width` | `PosFloat` | `2.0` | 円弧ブロック矢印（`arrow_type="arc"`）の胴体太さ。 |
| `arrow_head_width` | `PosFloat` | `4.5` | 円弧ブロック矢印（`arrow_type="arc"`）の矢じり幅。 |
| `arrow_color_mode` | `Literal["monochrome", "match_source", "match_target"]` | `"match_source"` | 矢印色の決定モード（単色指定、始点ノード追従、終点ノード追従）。 |
| `arrow_gap` | `PosFloat` | `2.5` | ノード境界と矢印端点の間のクリアランス距離（キャンバス単位）。 |
| `center_text` | `str` | `""` | 中央ハブ円の主テキスト（`set_center()` でも設定可能）。 |
| `center_description` | `str` | `""` | 中央ハブ内の補足説明テキスト。 |
| `center_radius` | `PosFloat` | `10.0` | 中央ハブ円の半径。 |
| `center_style` | `Style \| None` | `None` | 中央ハブ円の図形スタイル。 |
| `center_text_style` | `Style \| None` | `None` | `center_text` のテキストスタイル。 |
| `center_description_style` | `Style \| None` | `None` | `center_description` のテキストスタイル。 |

### メソッド・プロパティ

```python
cycle.items -> list[CycleItem]
cycle.center -> CycleCenter

cycle.add(
    text: str,
    *,
    style: Style | None = None,
    description: str = "",
    text_style: Style | None = None,
    description_style: Style | None = None,
    arrow_style: Style | None = None,
    show: bool = True,
) -> CycleItem

cycle.set_center(
    text: str,
    *,
    style: Style | None = None,
    description: str = "",
    radius: PosFloat | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CycleCenter

cycle.draw(
    xy: Coordinate,
    radius: PosFloat = 35.0,
    align: Literal["center", "bottom_left"] = "center",
    scale: PosFloat = 1.0,
) -> Self
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `items` | `property` | 登録済み `CycleItem` モデルのリスト（`list[CycleItem]`）を返します。 |
| `center` | `property` | 中央ハブを表す可変 `CycleCenter` モデルを返します。 |
| `add(text, *, style=None, description="", text_style=None, description_style=None, arrow_style=None, show=True)` | `method` | 周回ステップを追加し、`CycleItem` を返します。 |
| `set_center(text, *, style=None, description="", radius=None, text_style=None, description_style=None, show=True)` | `method` | 中央ハブノードを設定・有効化し、`CycleCenter` を返します。 |
| `draw(xy, radius=35.0, align="center", scale=1.0)` | `method` | 軌道半径 `radius` で `xy`（`"center"` または `"bottom_left"`）にサイクル図を描画し、`self` を返します。 |

## `class` CycleCenter

放射状 `Cycle` の中央ハブノードを表す可変 Pydantic モデルです（`cycle.center` プロパティまたは `cycle.set_center()` の戻り値として取得できます）。

- **座標アンカー:** 親 `Cycle` の軌道中心 `(cx, cy)` に配置されます。

```python
CycleCenter(
    *,
    text: str,
    description: str = "",
    radius: float = 10.0,
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> None
```

| 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *必須* | 中央ハブの主タイトル文字列（空文字列 `""` の場合は描画されません）。 |
| `description` | `str` | `""` | 中央ハブ内の補足サブタイトル文字列。 |
| `radius` | `float` | `10.0` | 中央ハブ円の半径（キャンバス単位）。 |
| `style` | `Style \| None` | `None` | 中央ハブ円の塗り・枠線スタイル。 |
| `text_style` | `Style \| None` | `None` | `text` のテキストスタイル。 |
| `description_style` | `Style \| None` | `None` | `description` のテキストスタイル。 |
| `show` | `bool` | `True` | 中央ハブノードの表示フラグ。 |

### メソッド・プロパティ

```python
center.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
center.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | フィールド更新を伴う中央ハブモデルの複製を返します（`pydantic.BaseModel`）。 |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Pydantic 標準の直列化・検証メソッド群（`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`）。 |

## `class` CycleItem

`Cycle` 内の単一周回ノードおよび送出矢印スタイルを保持する可変 Pydantic モデルです。

- **座標アンカー:** 親 `Cycle` の中心から距離 `radius`、極角 $\theta_i = \text{start\_angle} \mp i \cdot (360^\circ / N)$ の位置に配置されます。

```python
CycleItem(
    *,
    text: str,
    style: Style,
    description: str = "",
    text_style: Style | None = None,
    description_style: Style | None = None,
    arrow_style: Style | None = None,
    show: bool = True,
) -> None
```

| 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *必須* | 周回ノード内に表示される主ラベル文字列。 |
| `style` | `Style` | *必須* | この周回ノードの塗り・枠線スタイル。 |
| `description` | `str` | `""` | 任意の補足説明文字列（`Cycle` 設定に従い `"inside"` または `"outside"` に配置）。 |
| `text_style` | `Style \| None` | `None` | `text` スタイルの個別オーバーライド。 |
| `description_style` | `Style \| None` | `None` | `description` スタイルの個別オーバーライド。 |
| `arrow_style` | `Style \| None` | `None` | このノードから次ノードへ向かう矢印の個別スタイルオーバーライド。 |
| `show` | `bool` | `True` | 表示フラグ。`False` の場合、他のノードの角度位置を維持したままこのノードと接続矢印を非表示にします。 |

### メソッド・プロパティ

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | フィールド更新を伴うサイクル要素モデルの複製を返します（`pydantic.BaseModel`）。 |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Pydantic 標準の直列化・検証メソッド群（`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`）。 |

## `class` Pyramid

頂点の三角形と底辺に向かって広がる台形スライスで構成される階層ピラミッドを4方向（`"bottom"`, `"top"`, `"left"`, `"right"`）で描画します。均等段高（`draw`）と段ごとの高さ指定（`draw_flexible`）の両方に対応します。

- **座標アンカー:** デフォルトは **左下（Bottom-Left）** `(x, y)`（`align="bottom_left"`）、または **中央（Center）** `(cx, cy)`（`align="center"`）。

```python
Pyramid(
    *,
    style: Style,
    text_style: Style,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *必須* | ピラミッド各段のデフォルト塗り・枠線スタイル。 |
| `text_style` | `Style` | *必須* | 各段ラベルのデフォルトテキストスタイル。 |

### メソッド・プロパティ

```python
pyramid.items -> list[PyramidItem]

pyramid.add(
    text: str,
    *,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> PyramidItem

pyramid.draw(
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    margin: PosFloat,
    direction: Literal["bottom", "top", "left", "right"] = "bottom",
    order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self

pyramid.draw_flexible(
    xy: Coordinate,
    width: PosFloat,
    item_heights: list[PosFloat],
    margins: list[PosFloat],
    direction: Literal["bottom", "top", "left", "right"] = "bottom",
    order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `items` | `property` | 登録済み `PyramidItem` インスタンスのリスト（`list[PyramidItem]`）を返します。 |
| `add(text, *, style=None, text_style=None, show=True)` | `method` | ピラミッドの段を追加し、`PyramidItem` を返します。 |
| `draw(xy, width, height, margin, direction="bottom", order="vertex_to_base", align="bottom_left", scale=1.0)` | `method` | 均等段高でピラミッドを描画します（`direction` は底辺の位置、`order` は `items[0]` を頂点側・底辺側のどちらに置くかを指定）。`self` を返します。 |
| `draw_flexible(xy, width, item_heights, margins, direction="bottom", order="vertex_to_base", align="bottom_left", scale=1.0)` | `method` | 段ごとの高さリスト `item_heights`（長さ `N`）と段間余白リスト `margins`（長さ `N - 1`）を指定して描画し、`self` を返します。 |

## `class` PyramidItem

`Pyramid` 内の単一段のテキスト・多角形スタイル・表示状態を保持する可変 Pydantic モデルです。

- **座標アンカー:** 親 `Pyramid` のバウンディングボックス内に自動配置されます。

```python
PyramidItem(
    *,
    style: Style,
    text: str,
    text_style: Style,
    show: bool = True,
) -> None
```

| 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *必須* | この段の三角形／台形の塗り・枠線スタイル。 |
| `text` | `str` | *必須* | スライス中央に描画されるラベル文字列。 |
| `text_style` | `Style` | *必須* | `text` のテキストスタイル。 |
| `show` | `bool` | `True` | 表示フラグ。`False` の場合、他の段の形状・位置を保ったまま非表示にします。 |

### メソッド・プロパティ

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | フィールド更新を伴うピラミッド段モデルの複製を返します（`pydantic.BaseModel`）。 |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Pydantic 標準の直列化・検証メソッド群（`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`）。 |

## `class` Roadmap

直線または2次ベジェ曲線の垂直スパイン（`direction="vertical"`）、あるいは単列／上下交互配置の水平スパイン（`direction="horizontal"`）に沿って、スパイン上のバッジ（`badge_text`）と角丸矩形・ピル型のマイルストーンカードを接続描画するタイムラインコンポーネントです。

- **座標アンカー:** デフォルトは **左下（Bottom-Left）** `(x, y)`（`align="bottom_left"`）、または **中央（Center）** `(cx, cy)`（`align="center"`）。

```python
Roadmap(
    *,
    style: Style,
    text_style: Style,
    spine_style: Style,
    badge_style: Style,
    badge_text_style: Style,
    description_style: Style | None = None,
    icon_style: Style | None = None,
    direction: Literal["vertical", "horizontal"] = "vertical",
    curve_bend: float = 0.0,
    card_shape: Literal["pill", "rounded_rect"] = "rounded_rect",
    alternating: bool = False,
    spacing: PosFloat = 2.5,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *必須* | マイルストーンカード外枠のデフォルトスタイル。 |
| `text_style` | `Style` | *必須* | マイルストーンタイトルのデフォルトテキストスタイル。 |
| `spine_style` | `Style` | *必須* | タイムライン軸（スパイン）矢印および接続枝線の線スタイル。 |
| `badge_style` | `Style` | *必須* | スパイン上のマイルストーンバッジ図形のデフォルトスタイル。 |
| `badge_text_style` | `Style` | *必須* | バッジラベル（`badge_text`）のデフォルトテキストスタイル。 |
| `description_style` | `Style \| None` | `None` | 補足説明のデフォルトテキストスタイル（`description` 指定時は必須）。 |
| `icon_style` | `Style \| None` | `None` | カード内 `icon` 関数へ渡すデフォルトスタイル（`icon` 指定時は必須）。 |
| `direction` | `Literal["vertical", "horizontal"]` | `"vertical"` | スパインの向き（`"vertical"` 上から下、`"horizontal"` 左から右）。 |
| `curve_bend` | `float` | `0.0` | `direction="vertical"` 時の2次ベジェ湾曲率（`-0.5`〜`0.5`、`0.0` は直線）。 |
| `card_shape` | `Literal["pill", "rounded_rect"]` | `"rounded_rect"` | マイルストーンカードの形状。 |
| `alternating` | `bool` | `False` | `direction="horizontal"` 時に `True` にすると、中央水平軸の上下にカードを交互配置します。 |
| `spacing` | `PosFloat` | `2.5` | マイルストーンカード間の余白幅（キャンバス単位）。 |

### メソッド・プロパティ

```python
rm.items -> list[RoadmapItem]

rm.add(
    text: str,
    description: str = "",
    *,
    badge_text: str | None = None,
    icon: Callable[..., Any] | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    badge_style: Style | None = None,
    badge_text_style: Style | None = None,
    icon_style: Style | None = None,
    show: bool = True,
) -> RoadmapItem

rm.draw(
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `items` | `property` | 登録済み `RoadmapItem` モデルのリスト（`list[RoadmapItem]`）を返します。 |
| `add(text, description="", *, badge_text=None, icon=None, ...)` | `method` | マイルストーンを追加し（`badge_text=None` 時は `"1"`, `"2"`, ... を自動採番）、`RoadmapItem` を返します。 |
| `draw(xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | `xy` を基準とする `(width, height)` 領域内にロードマップを描画し、`self` を返します。 |

## `class` RoadmapItem

`Roadmap` 内の単一マイルストーンバッジ・カードを表す可変 Pydantic モデルです。

- **座標アンカー:** 親 `Roadmap` の垂直または水平スパインに沿って自動配置されます。

```python
RoadmapItem(
    *,
    text: str,
    description: str = "",
    badge_text: str | None = None,
    icon: Callable[..., Any] | None = None,
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    badge_style: Style,
    badge_text_style: Style,
    icon_style: Style | None = None,
    show: bool = True,
) -> None
```

| 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *必須* | マイルストーンまたはフェーズの主タイトル文字列。 |
| `description` | `str` | `""` | 任意のサブタイトル・詳細説明テキスト。 |
| `badge_text` | `str \| None` | `None` | スパイン上のバッジに表示される短いラベル（例: `"1"`, `"Q1"`, `"T+0m"`）。 |
| `icon` | `Callable[..., Any] \| None` | `None` | カード内に表示される任意のアイコン描画関数。 |
| `style` | `Style` | *必須* | マイルストーンカード外枠のスタイル。 |
| `text_style` | `Style` | *必須* | `text` のテキストスタイル。 |
| `description_style` | `Style \| None` | `None` | `description` のテキストスタイル。 |
| `badge_style` | `Style` | *必須* | スパイン上のバッジ図形スタイル。 |
| `badge_text_style` | `Style` | *必須* | `badge_text` のテキストスタイル。 |
| `icon_style` | `Style \| None` | `None` | `icon` に渡されるスタイル。 |
| `show` | `bool` | `True` | 表示フラグ。`False` の場合、スパインと他マイルストーン位置を保ったまま非表示にします。 |

### メソッド・プロパティ

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | フィールド更新を伴うロードマップ要素モデルの複製を返します（`pydantic.BaseModel`）。 |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Pydantic 標準の直列化・検証メソッド群（`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`）。 |

## `class` TreeNode

直交L字コネクタ線・ルートノードからのスタイル継承・前後に付与可能なアイコン要素（`register_drawing_item` + `set_drawing_item`）を備えた、ディレクトリ構造・ファイルツリー描画クラスです。

- **座標アンカー:** **左上固定（Top-Left）** `(x, y)` — ルートラベルが `xy` に描画され、子孫行は下方向（`-line_vertical_margin`）へ順に展開されます。ルートノードには `text_style`, `line_style`, `line_horizontal_margin`, `line_horizontal_length`, `line_vertical_margin` の5項目すべての指定が必須です。

```python
TreeNode(
    text: str,
    *,
    text_style: Style | None = None,
    line_style: Style | None = None,
    line_horizontal_margin: PosFloat | None = None,
    line_horizontal_length: PosFloat | None = None,
    line_vertical_margin: PosFloat | None = None,
    children: list[TreeNode] | None = None,
    show: bool = True,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *必須* | ノードの表示ラベル（例: `"src/"`, `"main.py"`）。 |
| `text_style` | `Style \| None` | `None` | ノードテキストのスタイル（ルートでは必須、`None` の子ノードは親から継承）。 |
| `line_style` | `Style \| None` | `None` | 直交コネクタ線のスタイル（ルートでは必須、`None` の子ノードは親から継承）。 |
| `line_horizontal_margin` | `PosFloat \| None` | `None` | 垂直幹線の開始位置までの水平インデント幅（ルートでは必須、子へ継承）。 |
| `line_horizontal_length` | `PosFloat \| None` | `None` | 垂直幹線から子ラベルへ向かう水平枝線の長さ（ルートでは必須、子へ継承）。 |
| `line_vertical_margin` | `PosFloat \| None` | `None` | 連続するツリー行間の垂直送り幅（ルートでは必須、子へ継承）。 |
| `children` | `list[TreeNode] \| None` | `None` | 構築済み子 `TreeNode` インスタンスのリスト。 |
| `show` | `bool` | `True` | 表示フラグ。`show=False` にすると後続行の高さを維持したまま該当ノードと枝線を非表示にします。 |

### メソッド・プロパティ

```python
node.text -> str
node.text_style -> Style | None
node.line_style -> Style | None
node.children -> list[TreeNode]

node.add(
    text: str,
    *,
    text_style: Style | None = None,
    line_style: Style | None = None,
    line_horizontal_margin: PosFloat | None = None,
    line_horizontal_length: PosFloat | None = None,
    line_vertical_margin: PosFloat | None = None,
    show: bool = True,
) -> Self

TreeNode.register_drawing_item(
    name: str,
    location: Literal["before", "after"],
    padding_width: float,
    function: Callable[..., Any],
    style: Style,
    args: dict[str, Any],
) -> None

node.set_drawing_item(name: str) -> Self

node.draw(
    xy: Coordinate,
    scale: PosFloat = 1.0,
) -> Self
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `text` | `property` | ノード文字列の取得・設定（`str`）。 |
| `text_style` | `property` | ノードテキストスタイルの取得・設定（`Style \| None`）。 |
| `line_style` | `property` | コネクタ線スタイルの取得・設定（`Style \| None`）。 |
| `children` | `property` | 子 `TreeNode` のリスト（`list[TreeNode]`）を返します。 |
| `add(text, *, ...)` | `method` | ラベル文字列 `text: str` から新しい子 `TreeNode` を生成・追加し、生成した子ノードを返します（構築済み `TreeNode` は `children=[...]` で渡します）。 |
| `register_drawing_item(name, location, padding_width, function, style, args)` | `classmethod` | テキストの前（`"before"`）または後（`"after"`）に描画する再利用可能なアイコン／図形を `name` で登録します。 |
| `set_drawing_item(name)` | `method` | 登録済み描画アイテム `name` をこのノードに紐付け、メソッドチェーン用に `self` を返します。 |
| `draw(xy, scale=1.0)` | `method` | 左上座標 `xy` を起点にツリー全体を描画し、`self` を返します。 |

## `class` MindMapNode

2パスの部分木バウンディング計測と自動直交フォーク配線により、階層ツリー・組織図・4方向放射状マインドマップ（`branch="bottom" | "top" | "left" | "right"`）を描画するクラスです。

- **座標アンカー:** **ルート中心固定（Center）** `(cx, cy)` — `draw(xy)` はルートノードの中心点を `xy` に配置します。ルートノードには `style`, `text_style`, `line_style` の指定が必須です。

```python
MindMapNode(
    text: str,
    *,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "ellipse", "none"] | None = None,
    width: PosFloat | None = None,
    height: PosFloat | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    line_style: Style | None = None,
    horizontal_margin: PosFloat | None = None,
    vertical_margin: PosFloat | None = None,
    line_length: PosFloat | None = None,
    xy_shift: Coordinate | None = None,
    children: list[MindMapNode] | None = None,
    show: bool = True,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *必須* | ノードの表示ラベル。 |
| `branch` | `Literal["bottom", "top", "left", "right"] \| None` | `None` | このノードおよび部分木の展開方向（ルート直下の子ノードごとに異なる方向を指定すると4方向放射マインドマップになります）。 |
| `shape` | `Literal["rectangle", "ellipse", "none"] \| None` | `None` | ノード図形（ルート省略時は `"rectangle"`、`"none"` は枠線なしのテキストノード）。 |
| `width` | `PosFloat \| None` | `None` | ノード幅（キャンバス単位、子孫へカスケード継承）。 |
| `height` | `PosFloat \| None` | `None` | ノード高さ（キャンバス単位、子孫へカスケード継承）。 |
| `style` | `Style \| None` | `None` | ノード図形の塗り・枠線スタイル（ルートでは必須、子へ継承）。 |
| `text_style` | `Style \| None` | `None` | ノードテキストスタイル（ルートでは必須、子へ継承）。 |
| `line_style` | `Style \| None` | `None` | 直交フォーク接続線のスタイル（ルートでは必須、子へ継承）。 |
| `horizontal_margin` | `PosFloat \| None` | `None` | 兄弟ノード間の水平マージン（キャンバス単位）。 |
| `vertical_margin` | `PosFloat \| None` | `None` | 兄弟ノード間の垂直マージン（キャンバス単位）。 |
| `line_length` | `PosFloat \| None` | `None` | 親子階層間の接続線長（キャンバス単位）。 |
| `xy_shift` | `Coordinate \| None` | `None` | レイアウト計算後に適用する位置微調整オフセット `(dx, dy)`。 |
| `children` | `list[MindMapNode] \| None` | `None` | 構築済み子 `MindMapNode` インスタンスのリスト。 |
| `show` | `bool` | `True` | 表示フラグ。`False` の場合、兄弟ノードの2パス配置座標を固定したまま非表示にします。 |

### メソッド・プロパティ

```python
node.text -> str
node.branch -> Literal["bottom", "top", "left", "right"] | None
node.shape -> Literal["rectangle", "ellipse", "none"] | None
node.width -> float | None
node.height -> float | None
node.style -> Style | None
node.text_style -> Style | None
node.line_style -> Style | None
node.children -> list[MindMapNode]

node.add(
    text: str,
    *,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "ellipse", "none"] | None = None,
    width: PosFloat | None = None,
    height: PosFloat | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    line_style: Style | None = None,
    horizontal_margin: PosFloat | None = None,
    vertical_margin: PosFloat | None = None,
    line_length: PosFloat | None = None,
    xy_shift: Coordinate | None = None,
    show: bool = True,
) -> Self

node.draw(
    xy: Coordinate,
    branch: Literal["bottom", "top", "left", "right"] = "bottom",
    scale: PosFloat = 1.0,
) -> Self
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `text`, `branch`, `shape`, `width`, `height`, `style`, `text_style`, `line_style` | `property` | フレーム間でノード形状やスタイルを参照・変更できる読み書きプロパティ群。 |
| `children` | `property` | 子 `MindMapNode` のリスト（`list[MindMapNode]`）を返します。 |
| `add(text, *, ...)` | `method` | ラベル文字列 `text: str` から新しい子 `MindMapNode` を生成・追加し、生成した子ノードを返します。 |
| `draw(xy, branch="bottom", scale=1.0)` | `method` | ルート中心座標 `xy` を基準に2パスレイアウト計算と描画を実行し、`self` を返します（`branch` は未指定ノードの既定方向）。 |

## `class` GeoMap

外部 GIS ライブラリ不要でベクター地図を描画するコンポーネントです。世界・地域プリセット（`GeoMap.World.*`：`All`, `Asia`, `Europe`, `NorthAmerica` 等）、215の国と地域（`GeoMap.Countries.*`）、主要16都市圏（`GeoMap.Cities.*`）、および任意の `.geojson` ファイルパスや辞書データをサポートします。

- **座標アンカー:** デフォルトは **左下（Bottom-Left）** `(x, y)`（`align="bottom_left"`）、または **中央（Center）** `(cx, cy)`（`align="center"`）。`draw()` 呼び出し時には `width` または `height` の少なくとも一方の指定が必須です。

```python
GeoMap(
    target: World | type[World] | Countries | Cities | str | Path | dict[str, Any],
    *,
    area_style: Style | None = None,
    background_style: Style | None = None,
    id_key: str | None = None,
    name_key: str | None = None,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `target` | `World \| type[World] \| Countries \| Cities \| str \| Path \| dict[str, Any]` | *必須* | 地図プリセット（`GeoMap.World.Asia`, `GeoMap.Countries.Japan`, `GeoMap.Cities.Japan_Tokyo` 等）または GeoJSON パス／`dict`。 |
| `area_style` | `Style \| None` | `None` | 各リージョン多角形のデフォルト塗り・境界線スタイル（`None` 時は内部で `Styles.Neutral` を使用）。 |
| `background_style` | `Style \| None` | `None` | 地図背面に描画する海域・外枠背景矩形のスタイル。 |
| `id_key` | `str \| None` | `None` | カスタム GeoJSON の `properties` から識別子を取得するキー名。 |
| `name_key` | `str \| None` | `None` | カスタム GeoJSON の `properties` から表示名を取得するキー名。 |

### メソッド・プロパティ

```python
m.data -> GeoData

m.get_areas() -> list[str]

m.set_area_styles(
    areas: list[str],
    style: Style,
) -> Self

m.draw(
    xy: tuple[float, float] = (0.0, 0.0),
    width: float | None = None,
    height: float | None = None,
    *,
    lon_range: tuple[float, float] | None = None,
    lat_range: tuple[float, float] | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self

m.get_area_xy(area: str) -> tuple[float, float]

m.lonlat_to_xy(lon: float, lat: float) -> tuple[float, float]
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `data` | `property` | 正規化済みポリゴン・境界ボックス・ビューポート情報を保持する `GeoData` モデルを返します。 |
| `get_areas()` | `method` | 地図に含まれる正規化エリア名の一覧を返します（`draw()` の前後どちらでも呼び出し可能）。 |
| `set_area_styles(areas, style)` | `method` | 英語名・ISO コード（`"JP"`, `"JPN"`）・日本語名（`"日本"`）で指定した地域に `style` を割り当て、`self` を返します。 |
| `draw(xy=(0.0, 0.0), width=None, height=None, *, lon_range=None, lat_range=None, align="bottom_left", scale=1.0)` | `method` | 地図をキャンバスへ描画します（片方の寸法のみ渡すと緯度コサイン補正アスペクト比で自動算出）。`self` を返します。 |
| `get_area_xy(area)` | `method` | 指定エリアの代表キャンバス座標 `(x, y)` を返します（**必ず `draw()` 実行後に呼び出してください**）。 |
| `lonlat_to_xy(lon, lat)` | `method` | 経度・緯度 `(lon, lat)` を直近に描画した地図上のキャンバス座標 `(x, y)` に変換します（**必ず `draw()` 実行後に呼び出してください**）。 |

## `class` DayCalendar

単一日のスケジュールを縦タイムライン（`direction="vertical"`：上から下へ時間軸、重複予定は水平レーンへ自動分割）または横タイムライン（`direction="horizontal"`：左から右へ時間軸、重複予定は垂直レーンへ自動分割）で描画します。厳密な ISO 8601 形式（`"YYYY-MM-DD"` および `"YYYY-MM-DD HH:MM"`）のみを受け付けます（`sunday_text_style` / `saturday_text_style` 引数はありません）。

- **座標アンカー:** デフォルトは **左下（Bottom-Left）** `(x, y)`（`align="bottom_left"`）、または `"center"` / `"top_left"`。

```python
DayCalendar(
    *,
    date: str = "2026-10-13",
    direction: Literal["vertical", "horizontal"] = "vertical",
    start_hour: int = 9,
    end_hour: int = 18,
    hour_step: PosInt = 1,
    show_all_day: bool | None = None,
    all_day_label: str | None = None,
    title: str | None = None,
    lang: Literal["en", "ja"] = "en",
    cell_style: Style,
    text_style: Style,
    header_style: Style,
    header_text_style: Style,
    border_style: Style,
    event_style: Style | None = None,
    event_text_style: Style | None = None,
    title_style: Style | None = None,
    title_text_style: Style | None = None,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `date` | `str` | `"2026-10-13"` | 対象日付（厳密な `"YYYY-MM-DD"` 形式）。 |
| `direction` | `Literal["vertical", "horizontal"]` | `"vertical"` | 時間軸の方向（`"vertical"` 縦軸、`"horizontal"` 横軸）。 |
| `start_hour` | `int` | `9` | 時間グリッドの開始時刻（`0`〜`23`）。 |
| `end_hour` | `int` | `18` | 時間グリッドの終了時刻（`> start_hour`、最大 `24`）。 |
| `hour_step` | `PosInt` | `1` | 時刻ラベルの表示間隔（時間単位、`>= 1`）。 |
| `show_all_day` | `bool \| None` | `None` | `None` の場合は終日予定が1件以上ある時に終日欄を自動表示し、`True`/`False` で強制切り替えします。 |
| `all_day_label` | `str \| None` | `None` | 終日欄のカスタムラベル（省略時は `"en"` が `"All-day"`、`"ja"` が `"全日"`）。 |
| `title` | `str \| None` | `None` | タイトルバー文字列（`None` で日付＋曜日を自動生成、`""` で非表示）。 |
| `lang` | `Literal["en", "ja"]` | `"en"` | 自動生成される曜日・終日ラベルの表示言語。 |
| `cell_style` | `Style` | *必須* | 時間セルの背景スタイル。 |
| `text_style` | `Style` | *必須* | 時刻目盛りラベルのテキストスタイル。 |
| `header_style` | `Style` | *必須* | 時刻・列ヘッダーの背景スタイル。 |
| `header_text_style` | `Style` | *必須* | ヘッダーラベルのテキストスタイル。 |
| `border_style` | `Style` | *必須* | グリッドおよび外枠の罫線スタイル。 |
| `event_style` | `Style \| None` | `None` | 追加予定ブロックのデフォルト図形スタイル。 |
| `event_text_style` | `Style \| None` | `None` | 予定タイトルのデフォルトテキストスタイル。 |
| `title_style` | `Style \| None` | `None` | 上部タイトルバー背景スタイルのオーバーライド。 |
| `title_text_style` | `Style \| None` | `None` | 上部タイトルバー文字スタイルのオーバーライド。 |

### メソッド・プロパティ

```python
dcal.items -> list[CalendarItem]

dcal.add(
    start: str,
    end: str | None = None,
    text: str = "",
    *,
    description: str = "",
    all_day: bool | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CalendarItem

dcal.get_time_xy(
    dt: str,
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> tuple[float, float]

dcal.draw(
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `items` | `property` | 登録済み `CalendarItem` モデルのリスト（`list[CalendarItem]`）を返します。 |
| `add(start, end=None, text="", *, description="", all_day=None, style=None, text_style=None, description_style=None, show=True)` | `method` | 時間指定ブロック（`"YYYY-MM-DD HH:MM"`）または終日バナー（`"YYYY-MM-DD"`）を登録し、`CalendarItem` を返します。 |
| `get_time_xy(dt, xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | `"YYYY-MM-DD"`（終日欄）または `"YYYY-MM-DD HH:MM"`（指定時刻）に対応するキャンバス中心座標 `(cx, cy)` を返します。 |
| `draw(xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | 日次スケジュールをキャンバスに描画し、`self` を返します。 |

## `class` WeekCalendar

7日間・平日5日間・または任意の期間（`start_date`..`end_date`／カスタム列見出し `columns`）の時間軸グリッドカレンダーを描画します。上部の終日（All-day / 全日）横断バーと、複数日またぎの時間指定予定に対する3種の描画モード（`span_mode="columns" | "box" | "all_day"`）を備えます。

- **座標アンカー:** デフォルトは **左下（Bottom-Left）** `(x, y)`（`align="bottom_left"`）、または `"center"` / `"top_left"`。

```python
WeekCalendar(
    *,
    start_date: str = "2026-10-11",
    end_date: str | None = None,
    num_days: PosInt = 7,
    columns: list[str] | None = None,
    start_hour: int = 9,
    end_hour: int = 18,
    hour_step: PosInt = 1,
    show_all_day: bool | None = None,
    all_day_label: str | None = None,
    title: str | None = None,
    lang: Literal["en", "ja"] = "en",
    cell_style: Style,
    text_style: Style,
    header_style: Style,
    header_text_style: Style,
    border_style: Style,
    event_style: Style | None = None,
    event_text_style: Style | None = None,
    sunday_text_style: Style | None = None,
    saturday_text_style: Style | None = None,
    title_style: Style | None = None,
    title_text_style: Style | None = None,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `start_date` | `str` | `"2026-10-11"` | 表示開始日（厳密な `"YYYY-MM-DD"` 形式）。 |
| `end_date` | `str \| None` | `None` | 任意の表示終了日（`"YYYY-MM-DD"`、指定時は `num_days` より優先）。 |
| `num_days` | `PosInt` | `7` | `end_date=None` 時に表示する日数列数。 |
| `columns` | `list[str] \| None` | `None` | 表示日数に対応するカスタム列ヘッダー文字列のリスト。 |
| `start_hour` | `int` | `9` | 縦時間グリッドの開始時刻（`0`〜`23`）。 |
| `end_hour` | `int` | `18` | 縦時間グリッドの終了時刻（`> start_hour`、最大 `24`）。 |
| `hour_step` | `PosInt` | `1` | 左ガター時刻ラベルの間隔（時間単位）。 |
| `show_all_day` | `bool \| None` | `None` | `None` で終日予定がある場合に自動表示、`True`/`False` で明示制御。 |
| `all_day_label` | `str \| None` | `None` | 終日ガターのラベル文字列（既定は `"All-day"` / `"全日"`）。 |
| `title` | `str \| None` | `None` | 上部タイトルバー文字列（`None` で期間見出しを自動生成、`""` で非表示）。 |
| `lang` | `Literal["en", "ja"]` | `"en"` | 曜日見出しおよび既定ラベルの言語。 |
| `cell_style` | `Style` | *必須* | 時間スロットセルの背景スタイル。 |
| `text_style` | `Style` | *必須* | 時刻ガターおよび標準テキストのスタイル。 |
| `header_style` | `Style` | *必須* | 日付列ヘッダーの背景スタイル。 |
| `header_text_style` | `Style` | *必須* | 日付列ヘッダーのテキストスタイル。 |
| `border_style` | `Style` | *必須* | グリッド罫線のスタイル。 |
| `event_style` | `Style \| None` | `None` | 予定ブロック／バーのデフォルト図形スタイル。 |
| `event_text_style` | `Style \| None` | `None` | 予定タイトルのデフォルトテキストスタイル。 |
| `sunday_text_style` | `Style \| None` | `None` | 日曜日列ヘッダーのテキストスタイルオーバーライド。 |
| `saturday_text_style` | `Style \| None` | `None` | 土曜日列ヘッダーのテキストスタイルオーバーライド。 |
| `title_style` | `Style \| None` | `None` | 上部タイトルバー背景スタイルのオーバーライド。 |
| `title_text_style` | `Style \| None` | `None` | 上部タイトルバー文字スタイルのオーバーライド。 |

### メソッド・プロパティ

```python
wcal.items -> list[CalendarItem]

wcal.add(
    start: str,
    end: str | None = None,
    text: str = "",
    *,
    description: str = "",
    all_day: bool | None = None,
    span_mode: Literal["columns", "box", "all_day"] = "columns",
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CalendarItem

wcal.get_slot_xy(
    dt: str,
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> tuple[float, float]

wcal.draw(
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `items` | `property` | 登録済み `CalendarItem` モデルのリスト（`list[CalendarItem]`）を返します。 |
| `add(start, end=None, text="", *, description="", all_day=None, span_mode="columns", ...)` | `method` | 終日バーまたは時間指定予定（`span_mode="columns"`, `"box"`, `"all_day"`）を登録し、`CalendarItem` を返します。 |
| `get_slot_xy(dt, xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | `"YYYY-MM-DD"`（終日セル）または `"YYYY-MM-DD HH:MM"`（時間スロット）のキャンバス座標 `(cx, cy)` を返します。 |
| `draw(xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | 週次カレンダーをキャンバスに描画し、`self` を返します。 |

## `class` MonthCalendar

Outlook / Google カレンダー風の7列月間グリッド（`end_date=None`）または月またぎ複数週グリッド（`end_date="YYYY-MM-DD"`）を描画します。週をまたぐ長期イベントバーの自動折り返し（`←` / `→`）と複数段レーン積み上げ（`max_tracks`）に対応します。

- **座標アンカー:** デフォルトは **左下（Bottom-Left）** `(x, y)`（`align="bottom_left"`）、または `"center"` / `"top_left"`。

```python
MonthCalendar(
    *,
    start_date: str = "2026-10-01",
    end_date: str | None = None,
    first_weekday: Literal["sun", "mon"] = "sun",
    title: str | None = None,
    lang: Literal["en", "ja"] = "en",
    max_tracks: PosInt = 3,
    cell_style: Style,
    text_style: Style,
    header_style: Style,
    header_text_style: Style,
    border_style: Style,
    event_style: Style | None = None,
    event_text_style: Style | None = None,
    sunday_text_style: Style | None = None,
    saturday_text_style: Style | None = None,
    title_style: Style | None = None,
    title_text_style: Style | None = None,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `start_date` | `str` | `"2026-10-01"` | 対象月の基準日（`end_date` 指定時は表示開始日、`"YYYY-MM-DD"` 形式）。 |
| `end_date` | `str \| None` | `None` | 月またぎ・複数週表示を行う場合の終了日（`"YYYY-MM-DD"`）。`None` 時は `start_date` の月全体を表示。 |
| `first_weekday` | `Literal["sun", "mon"]` | `"sun"` | 週の左端曜日（`"sun"` 日曜始まり、または `"mon"` 月曜始まり）。 |
| `title` | `str \| None` | `None` | 上部タイトル文字列（`None` で年月見出しを自動生成、`""` で非表示）。 |
| `lang` | `Literal["en", "ja"]` | `"en"` | 年月タイトルおよび曜日ヘッダーの表示言語。 |
| `max_tracks` | `PosInt` | `3` | 各週行内に積み上げ表示するイベントバーの最大段数（`>= 1`）。 |
| `cell_style` | `Style` | *必須* | 日付セルの背景スタイル。 |
| `text_style` | `Style` | *必須* | 日付番号のテキストスタイル。 |
| `header_style` | `Style` | *必須* | 曜日ヘッダー行の背景スタイル。 |
| `header_text_style` | `Style` | *必須* | 曜日ヘッダー行のテキストスタイル。 |
| `border_style` | `Style` | *必須* | カレンダーセル格子の罫線スタイル。 |
| `event_style` | `Style \| None` | `None` | 横断イベントバーのデフォルトスタイル。 |
| `event_text_style` | `Style \| None` | `None` | イベントバー文字列のデフォルトテキストスタイル。 |
| `sunday_text_style` | `Style \| None` | `None` | 日曜日の日付・曜日テキストスタイルオーバーライド。 |
| `saturday_text_style` | `Style \| None` | `None` | 土曜日の日付・曜日テキストスタイルオーバーライド。 |
| `title_style` | `Style \| None` | `None` | 上部タイトルバー背景スタイルのオーバーライド。 |
| `title_text_style` | `Style \| None` | `None` | 上部タイトルバー文字スタイルのオーバーライド。 |

### メソッド・プロパティ

```python
mcal.items -> list[CalendarItem]

mcal.add(
    start: str,
    end: str | None = None,
    text: str = "",
    *,
    description: str = "",
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CalendarItem

mcal.get_date_xy(
    date: str,
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> tuple[float, float]

mcal.draw(
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `items` | `property` | 登録済み `CalendarItem` モデルのリスト（`list[CalendarItem]`）を返します。 |
| `add(start, end=None, text="", *, description="", style=None, text_style=None, description_style=None, show=True)` | `method` | 単日または複数日横断のイベントバーを登録し、`CalendarItem` を返します。 |
| `get_date_xy(date, xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | 指定日 `"YYYY-MM-DD"` のセル中心座標 `(cx, cy)` を返します。 |
| `draw(xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | 月間／複数週カレンダーをキャンバスへ描画し、`self` を返します。 |

## `class` CalendarItem

`DayCalendar`・`WeekCalendar`・`MonthCalendar` で共通利用される予定ブロック／終日横断バーの可変 Pydantic モデルです。

- **座標アンカー:** ISO 8601 形式の `start` / `end` 日時から親カレンダーの日付・時刻グリッドへ自動マッピングされます。

```python
CalendarItem(
    *,
    start: str,
    end: str | None = None,
    text: str = "",
    description: str = "",
    all_day: bool | None = None,
    span_mode: Literal["columns", "box", "all_day"] = "columns",
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    show: bool = True,
) -> None
```

| 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `start` | `str` | *必須* | 開始日（`"YYYY-MM-DD"`）または開始日時（`"YYYY-MM-DD HH:MM"`）。 |
| `end` | `str \| None` | `None` | 終了日または終了日時（単日イベントで `None` の場合は `start` と同日扱い）。 |
| `text` | `str` | `""` | イベント枠内に表示される主タイトル文字列。 |
| `description` | `str` | `""` | 任意の補足サブタイトル・時刻メモ。 |
| `all_day` | `bool \| None` | `None` | 終日欄への明示的オーバーライド（`None` の場合、`"YYYY-MM-DD"` は `True`、`"YYYY-MM-DD HH:MM"` は `False` と自動判定）。 |
| `span_mode` | `Literal["columns", "box", "all_day"]` | `"columns"` | `WeekCalendar` における複数日時間指定イベントの描画方式（`"columns"` 列分割、`"box"` 単一矩形横断、`"all_day"` 上部終日欄）。 |
| `style` | `Style` | *必須* | イベント枠／バーの塗り・枠線スタイル。 |
| `text_style` | `Style` | *必須* | `text` のテキストスタイル。 |
| `description_style` | `Style \| None` | `None` | `description` のテキストスタイル。 |
| `show` | `bool` | `True` | 表示フラグ。`False` の場合、カレンダートラック／レーン配置を保ったまま非表示にします。 |

### メソッド・プロパティ

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| メンバ | 種別 | 説明 |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | フィールド更新を伴うカレンダー予定モデルの複製を返します（`pydantic.BaseModel`）。 |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Pydantic 標準の直列化・検証メソッド群（`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`）。 |
