# drawlib.graph（自動レイアウトグラフエンジン）

`drawlib.graph` は、トポロジー宣言から重なりのないノード座標・ネストされたコンテナ境界・直交／直線エッジ経路を `get_layout()` で自動計算する 5 種類のグラフレイアウトソルバー（`ArchitectureGraph`・`LayerGraph`・`TreeGraph`・`RadialGraph`・`GridGraph`）を提供します。算出された `GraphLayout` を `drawlib.diagrams` や `drawlib.shapes`・`drawlib.lines` に渡す 2 ステップ構成で柔軟に描画できます。

```drawlib align=center code=fold file=25_graph_hero.png caption="2 ステップ・グラフレイアウトワークフロー: LayerGraph.get_layout() によるノード・クラスタ・エッジ座標の自動計算"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.icons import phosphor
from drawlib.lines import lines
from drawlib.shapes import rectangle
from drawlib.smartarts import BoxList
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=132, height=74)

rectangle(
    (66, 37),
    width=122,
    height=64,
    style=Styles.Neutral.patch(shape_fill_color=Colors.Transparent, line_style="dashed", shape_r=2.5),
)
text(
    (66, 64.5),
    "Step 1: layout = g.get_layout()   ->   Step 2: Render ClusterLayout, EdgeLayout & NodeLayout",
    style=Styles.DarkBold.patch(text_size=11.5),
)

g = LayerGraph(direction="LR", rank_sep=15.0, node_sep=5.0, default_node_width=26.0, default_node_height=10.5)
g.node("ingest")
g.node("validate")
g.node("enrich")
g.node("warehouse")
g.tier("stage", ["validate", "enrich"], layer=1)
g.cluster("etl_cluster", ["validate", "enrich"], padding=3.0, header_height=4.0)
g.edge("ingest", "validate")
g.edge("ingest", "enrich")
g.edge("validate", "warehouse")
g.edge("enrich", "warehouse")

raw = g.get_layout(width=116, height=38, margin=2.0)
cl = raw.clusters["etl_cluster"]
dy = 38.0 - cl.cy

rectangle(
    (cl.cx + 8.0, cl.cy + dy),
    width=cl.width,
    height=cl.height,
    style=Styles.PrimaryNeutral.patch(line_style="dashed", shape_r=2.0),
)
text(
    (cl.cx + 8.0, cl.top + dy - 2.3),
    "ClusterLayout ('etl_cluster')",
    style=Styles.PrimaryBold.patch(text_size=10.0),
)

for edge in raw.edges:
    pts = [(px + 8.0, py + dy) for px, py in edge.points]
    lines(pts, arrow_head="->", style=Styles.DarkBold)

node_specs = [
    ("ingest", "Ingest API", Styles.Neutral, Styles.DarkBold, Styles.PrimaryBold, phosphor.globe),
    ("validate", "Validate", Styles.Neutral, Styles.DarkBold, Styles.PrimaryBold, phosphor.check_circle),
    ("enrich", "DAG Solver", Styles.PrimaryFlat, Styles.WhiteBold, Styles.WhiteBold, phosphor.git_branch),
    ("warehouse", "Analytics DB", Styles.SecondaryNeutral, Styles.DarkBold, Styles.SecondaryBold, phosphor.database),
]
for nid, label, card_st, txt_st, ico_st, icon_fn in node_specs:
    n = raw.nodes[nid]
    cx, cy = n.x + 8.0, n.y + dy
    rectangle((cx, cy), width=n.width, height=n.height, style=card_st.patch(shape_r=1.8))
    icon_fn((cx - 8.5, cy), width=4.4, style=ico_st)
    text((cx + 2.2, cy), label, style=txt_st.patch(text_size=10.5))

solvers = BoxList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
solvers.add("ArchitectureGraph")
solvers.add("LayerGraph", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=10.0))
solvers.add("TreeGraph")
solvers.add("RadialGraph")
solvers.add("GridGraph", style=Styles.SecondaryNeutral)
solvers.draw(xy=(9.0, 8.0), box_width=22.8, box_height=7.0, direction="left")

save()
```

## `class` ArchitectureGraph

2 階層のマクロ／ミクロ構造に対応した宣言的アーキテクチャ・グラフレイアウトソルバーです。VPC・クラスタ・クライアントゾーン・外部 SaaS などの上位コンテナをマクロ軸や 5 方位ゾーンに沿って配置しつつ、内部サービス・サブネット・データベースの座標を各境界内で自動整列します。

```python
from drawlib.graph import ArchitectureGraph

ArchitectureGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    container_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_width: float = 24.0,
    default_node_height: float = 12.0,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `direction` | `Literal["LR", "TB"]` | `"LR"` | マクロフローの進行軸（`"LR"` 左→右、または `"TB"` 上→下）。 |
| `container_sep` | `float \| None` | `None` | トップレベルコンテナ間の固定間隔（キャンバス単位）。`None` の場合は自動調整。 |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | エッジ配線方式（`"orthogonal"` 直交折れ線、または `"straight"` 直線ポート接続）。 |
| `default_node_width` | `float` | `24.0` | `width` 省略時にノードへ割り当てられるデフォルト幅。 |
| `default_node_height` | `float` | `12.0` | `height` 省略時にノードへ割り当てられるデフォルト高さ。 |

### パブリックメソッド

| メソッド | シグネチャ | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | オプションの `group` / `subgroup` 所属指定付きでトポロジーにノードを登録します。 |
| `edge` | `(src, dst)` | [`Edge`](#edge) | `src` から `dst` への有向接続を登録します（未登録ノード ID は計算時に自動登録されます）。 |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | `parent` ネスト・兄弟順序 `order`・5 方位 `pos`（`"top"`, `"bottom"`, `"left"`, `"right"`, `"center"`）対応の境界クラスタを登録します。 |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | VPC・ゾーン・サブネット宣言に適したキーワード引数 `nodes` 版の `cluster()` エイリアスです。 |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | 描画を行わずに複合アーキテクチャ座標を計算します（省略時は現在のキャンバス寸法を使用）。 |

## `class` BaseGraph

5 種類すべてのグラフレイアウトソルバー（`ArchitectureGraph`・`LayerGraph`・`TreeGraph`・`RadialGraph`・`GridGraph`）の抽象基底クラスです。ノード・エッジ・クラスタ登録メソッドと共通の `get_layout()` インターフェースを提供します。

```python
from drawlib.graph import BaseGraph

BaseGraph(
    *,
    default_node_width: float = 20.0,
    default_node_height: float = 12.0,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `default_node_width` | `float` | `20.0` | `node()` で `width` が指定されなかった場合の標準ノード幅。 |
| `default_node_height` | `float` | `12.0` | `node()` で `height` が指定されなかった場合の標準ノード高さ。 |

### パブリックメソッド

| メソッド | シグネチャ | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | グラフトポロジーにノードを登録します。 |
| `edge` | `(src, dst)` | [`Edge`](#edge) | 2 つのノード ID 間の有向エッジを登録します。 |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | ノード群を囲むグルーピング境界を登録します。 |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | アーキテクチャコンテナ／グループ境界を登録します。 |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | キャンバスへ描画せずにノード・エッジ・クラスタの幾何座標を算出します。 |

## `class` Cluster

`g.cluster()` または `g.group()` によって返される、ユーザー登録済みのグルーピング境界を表すデータクラスです。

```python
from drawlib.graph import Cluster

Cluster(
    id: str,
    nodes: list[str] = ...,
    padding: float = 4.0,
    header_height: float = 3.5,
    parent: str | None = None,
    order: int | None = None,
    pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
) -> None
```

| 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(必須)* | クラスタまたはコンテナの一意な識別子。 |
| `nodes` | `list[str]` | `[]` | この境界に直接含まれるメンバーノード ID のリスト。 |
| `padding` | `float` | `4.0` | 内部ノードおよび子クラスタ周囲の内側余白。 |
| `header_height` | `float` | `3.5` | コンテナ上部のタイトルバナー用に確保される追加高さ。 |
| `parent` | `str \| None` | `None` | ネスト階層用の親クラスタ ID（VPC 内のサブネットなど）。 |
| `order` | `int \| None` | `None` | 兄弟コンテナ間の明示的な並び順インデックス。 |
| `pos` | `Literal["top", "bottom", "left", "right", "center"] \| None` | `None` | `ArchitectureGraph` で使用されるマクロ方位ゾーン配置ヒント。 |

## `class` ClusterLayout

`GraphLayout.clusters` に格納される計算済みクラスタ境界ボックスと階層座標モデルです。`ArchitectureDiagram` の `NodeGroup` 向けの左下基準座標と、基本図形向けの中心座標の両方を提供します。

```python
from drawlib.graph import ClusterLayout

ClusterLayout(
    id: str,
    bbox: tuple[float, float, float, float],
    parent_id: str | None = None,
    local_bottom_left: tuple[float, float] = (0.0, 0.0),
) -> None
```

| フィールド | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(必須)* | 登録された `Cluster.id` に対応するクラスタ識別子。 |
| `bbox` | `tuple[float, float, float, float]` | *(必須)* | キャンバス全体の境界タプル `(left, bottom, right, top)`。 |
| `parent_id` | `str \| None` | `None` | 外側コンテナにネストされている場合の親クラスタ ID（トップレベルは `None`）。 |
| `local_bottom_left` | `tuple[float, float]` | `(0.0, 0.0)` | 親クラスタの左下原点を基準としたローカル左下 `(x, y)` 座標。 |

### プロパティ

| プロパティ | 型 | 説明 |
| :--- | :--- | :--- |
| `bottom` | `float` | 下端 Y 座標（`bbox[1]`）。 |
| `bottom_left` | `tuple[float, float]` | グローバル左下 `(left, bottom)` 座標（トップレベル `NodeGroup` にそのまま渡せます）。 |
| `center` | `tuple[float, float]` | クラスタのグローバル中心 `(cx, cy)` 座標。 |
| `cx` | `float` | クラスタ中心の X 座標。 |
| `cy` | `float` | クラスタ中心の Y 座標。 |
| `height` | `float` | クラスタの高さ（`top - bottom`）。 |
| `left` | `float` | 左端 X 座標（`bbox[0]`）。 |
| `right` | `float` | 右端 X 座標（`bbox[2]`）。 |
| `size` | `tuple[float, float]` | クラスタの寸法 `(width, height)`。 |
| `top` | `float` | 上端 Y 座標（`bbox[3]`）。 |
| `width` | `float` | クラスタの幅（`right - left`）。 |
| `xy` | `tuple[float, float]` | `center`（`(cx, cy)`）のエイリアス。中心アンカーの `rectangle()` に最適です。 |

## `class` Edge

`g.edge(src, dst)` によって返される、2 つのノード間の有向接続を表すデータクラスです。

```python
from drawlib.graph import Edge

Edge(
    src: str,
    dst: str,
) -> None
```

| 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `src` | `str` | *(必須)* | 有向エッジの始点となるソースノード ID。 |
| `dst` | `str` | *(必須)* | 有向エッジの終点となる宛先ノード ID。 |

## `class` EdgeLayout

`GraphLayout.edges` に格納される計算済みエッジの接続ポート座標と中間折れ点（ウェイポイント）モデルです。

```python
from drawlib.graph import EdgeLayout

EdgeLayout(
    src: str,
    dst: str,
    src_port: tuple[float, float],
    dst_port: tuple[float, float],
    waypoints: list[tuple[float, float]] = ...,
) -> None
```

| フィールド | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `src` | `str` | *(必須)* | 始点ノード識別子。 |
| `dst` | `str` | *(必須)* | 終点ノード識別子。 |
| `src_port` | `tuple[float, float]` | *(必須)* | 始点ノード外周上の接続ポート `(x, y)` 座標。 |
| `dst_port` | `tuple[float, float]` | *(必須)* | 終点ノード外周上の接続ポート `(x, y)` 座標。 |
| `waypoints` | `list[tuple[float, float]]` | `[]` | `src_port` と `dst_port` の間の中間折れ点 `(x, y)` リスト。 |

### プロパティ

| プロパティ | 型 | 説明 |
| :--- | :--- | :--- |
| `points` | `list[tuple[float, float]]` | `lines(edge.points, arrow_head="->")` にそのまま渡せる全頂点列 `[src_port, *waypoints, dst_port]`。 |
| `mid_xy` | `tuple[float, float]` | エッジラベルの配置に適した経路上の幾何学的中点 `(mx, my)`。 |

## `class` GraphLayout

すべてのグラフソルバーの `get_layout()` が返す完全な幾何計算結果オブジェクトです。`layout[key]` によるノード／クラスタの辞書風ルックアップ、`print(layout)` による人間可読な座標ダンプ、および `.offset()` による計算後の微調整をサポートします。

```python
from drawlib.graph import GraphLayout

GraphLayout(
    nodes: dict[str, NodeLayout] = ...,
    edges: list[EdgeLayout] = ...,
    clusters: dict[str, ClusterLayout] = ...,
    width: float = 100.0,
    height: float = 100.0,
    ring_radii: dict[int, float] = ...,
) -> None
```

| フィールド | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `nodes` | `dict[str, NodeLayout]` | `{}` | ノード ID から計算済み [`NodeLayout`](#nodelayout) へのマッピング。 |
| `edges` | `list[EdgeLayout]` | `[]` | 計算済み [`EdgeLayout`](#edgelayout) 経路の順序付きリスト。 |
| `clusters` | `dict[str, ClusterLayout]` | `{}` | クラスタ ID から計算済み [`ClusterLayout`](#clusterlayout) へのマッピング。 |
| `width` | `float` | `100.0` | レイアウト対象のキャンバス幅。 |
| `height` | `float` | `100.0` | レイアウト対象のキャンバス高さ。 |
| `ring_radii` | `dict[int, float]` | `{}` | [`RadialGraph`](#radialgraph) が設定するリング番号から半径へのマッピング。 |

### パブリックメソッド

| メソッド | シグネチャ | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `offset` | `(node_id: str, dx: float = 0.0, dy: float = 0.0)` | `Self` | 指定ノードを `(dx, dy)` だけ平行移動し（`.xy`・`.local_xy`・接続エッジのポート座標も再計算）、メソッドチェーン用に `self` を返します。 |

## `class` GridGraph

宣言的 2D マトリクスグリッド・レイアウトソルバーです。設定可能な列数・充填順序（`"row-major"` / `"column-major"`）・明示的な `(row, col)` セル固定・セル間チャネル配線を用いてノードを規則的な格子状に配置します。

```python
from drawlib.graph import GridGraph

GridGraph(
    columns: int = 3,
    *,
    rows: int | None = None,
    order: Literal["row-major", "column-major"] = "row-major",
    col_sep: float | None = None,
    row_sep: float | None = None,
    edge_routing: Literal["smart", "orthogonal", "straight"] = "smart",
    default_node_width: float = 20.0,
    default_node_height: float = 12.0,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `columns` | `int` | `3` | グリッドの列数（`>= 1`）。 |
| `rows` | `int \| None` | `None` | 明示的な行数（`None` の場合はノード数から自動算出）。 |
| `order` | `Literal["row-major", "column-major"]` | `"row-major"` | 位置未指定ノードの自動スロット割り当て順序。 |
| `col_sep` | `float \| None` | `None` | 列間の水平ギャップ（`None` の場合はキャンバス幅に合わせて自動調整）。 |
| `row_sep` | `float \| None` | `None` | 行間の垂直ギャップ（`None` の場合はキャンバス高さに合わせて自動調整）。 |
| `edge_routing` | `Literal["smart", "orthogonal", "straight"]` | `"smart"` | エッジ配線方式（`"smart"` は非隣接セル間の接続をグリッド通路へ迂回させます）。 |
| `default_node_width` | `float` | `20.0` | デフォルトのセルノード幅。 |
| `default_node_height` | `float` | `12.0` | デフォルトのセルノード高さ。 |

### パブリックメソッド

| メソッド | シグネチャ | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `cell` | `(cell_id, row=None, col=None, *, width=None, height=None)` | [`Node`](#node) | オプションの 0 始まり `(row, col)` 位置を指定してグリッドセルノードを登録する便利メソッドです。 |
| `cluster_row` | `(row, cluster_id, *, padding=4.0, header_height=3.5)` | [`Cluster`](#cluster) | 指定した `row`（0 始まり）の全ノードを囲むクラスタ境界を登録します。 |
| `cluster_column` | `(col, cluster_id, *, padding=4.0, header_height=3.5)` | [`Cluster`](#cluster) | 指定した `col`（0 始まり）の全ノードを囲むクラスタ境界を登録します。 |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | グリッドトポロジーにノードを登録します。 |
| `edge` | `(src, dst)` | [`Edge`](#edge) | 2 つのグリッドノード間の接続を登録します。 |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | 任意のセル群を囲むカスタムクラスタを登録します。 |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | キーワード引数 `nodes` 版の `cluster()` エイリアスです。 |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | 描画を行わずにマトリクス座標とエッジ経路を算出します。 |

## `class` LayerGraph

杉山フレームワーク（閉路除去・最長経路レイヤー割り当て・重心法によるエッジ交差最小化）を用いた宣言的階層型 DAG レイアウトソルバーです。CI/CD パイプライン、ETL／Airflow データリネージ、タスク依存関係グラフに最適です。

```python
from drawlib.graph import LayerGraph

LayerGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    rank_sep: float | None = None,
    node_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_width: float = 22.0,
    default_node_height: float = 12.0,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `direction` | `Literal["LR", "TB"]` | `"LR"` | レイヤー進行軸（`"LR"` 左→右、または `"TB"` 上→下）。 |
| `rank_sep` | `float \| None` | `None` | 隣接ランク／レイヤー間の固定距離（`None` の場合は自動調整）。 |
| `node_sep` | `float \| None` | `None` | 同一ランク内の並列ノード間の固定距離（`None` の場合は自動調整）。 |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | エッジ配線方式（`"orthogonal"` 直交折れ線、または `"straight"` 直線接続）。 |
| `default_node_width` | `float` | `22.0` | デフォルトのノード幅。 |
| `default_node_height` | `float` | `12.0` | デフォルトのノード高さ。 |

### パブリックメソッド

| メソッド | シグネチャ | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `tier` | `(name, nodes, *, layer=None)` | `None` | 複数のノード ID を同一レイヤー／ランク番号（`0, 1, ...`）へ明示的に固定します。 |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | オプションの `layer` ランク指定付きでノードを登録します。 |
| `edge` | `(src, dst)` | [`Edge`](#edge) | `src` から `dst` への有向依存エッジを登録します。 |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | ステージ内のノード群を囲む境界クラスタを登録します。 |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | キーワード引数 `nodes` 版の `cluster()` エイリアスです。 |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | 描画を行わずに階層型 DAG 座標を計算します。 |

## `class` Node

`g.node()`・`g.cell()`・`g.spoke()`・`g.child()` によって返される、グラフトポロジー内のユーザー登録ノードを表すデータクラスです。

```python
from drawlib.graph import Node

Node(
    id: str,
    width: float | None = None,
    height: float | None = None,
    ring: int | None = None,
    row: int | None = None,
    col: int | None = None,
    layer: int | None = None,
    group: str | None = None,
    subgroup: str | None = None,
) -> None
```

| 属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(必須)* | 一意なノード識別子文字列。 |
| `width` | `float \| None` | `None` | 個別ノード幅（`None` の場合はソルバーの `default_node_width` を継承）。 |
| `height` | `float \| None` | `None` | 個別ノード高さ（`None` の場合はソルバーの `default_node_height` を継承）。 |
| `ring` | `int \| None` | `None` | `RadialGraph` 用の同心円リング番号（`0` = 中心ハブ）。 |
| `row` | `int \| None` | `None` | `GridGraph` 用の明示的な行番号（0 始まり）。 |
| `col` | `int \| None` | `None` | `GridGraph` 用の明示的な列番号（0 始まり）。 |
| `layer` | `int \| None` | `None` | `LayerGraph` 用の明示的なレイヤー／ランク番号（0 始まり）。 |
| `group` | `str \| None` | `None` | `ArchitectureGraph` 用のトップレベルコンテナ ID。 |
| `subgroup` | `str \| None` | `None` | `ArchitectureGraph` 用の `group` 内ネストサブコンテナ ID。 |

## `class` NodeLayout

`GraphLayout.nodes` に格納される計算済みノードのグローバル座標・親クラスタ相対座標・寸法モデルです。

```python
from drawlib.graph import NodeLayout

NodeLayout(
    id: str,
    xy: tuple[float, float],
    width: float,
    height: float,
    parent_id: str | None = None,
    local_xy: tuple[float, float] = (0.0, 0.0),
) -> None
```

| フィールド | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(必須)* | `Node.id` に対応するノード識別子。 |
| `xy` | `tuple[float, float]` | *(必須)* | キャンバス上のグローバル中心 `(cx, cy)` 座標。 |
| `width` | `float` | *(必須)* | 確定したノード幅（キャンバス単位）。 |
| `height` | `float` | *(必須)* | 確定したノード高さ（キャンバス単位）。 |
| `parent_id` | `str \| None` | `None` | クラスタに所属している場合の親クラスタ ID（未所属時は `None`）。 |
| `local_xy` | `tuple[float, float]` | `(0.0, 0.0)` | 親クラスタの `bottom_left` 原点からの相対中心 `(cx, cy)` 座標（`NodeGroup.add()` 用）。 |

### プロパティ

| プロパティ | 型 | 説明 |
| :--- | :--- | :--- |
| `bottom` | `float` | 下端 Y 座標（`y - height / 2`）。 |
| `bottom_left` | `tuple[float, float]` | グローバル左下 `(left, bottom)` コーナー座標。 |
| `center` | `tuple[float, float]` | `xy`（グローバル中心 `(x, y)`）のエイリアス。 |
| `left` | `float` | 左端 X 座標（`x - width / 2`）。 |
| `local_bottom_left` | `tuple[float, float]` | 親クラスタの `bottom_left` 原点からの相対左下コーナー座標。 |
| `right` | `float` | 右端 X 座標（`x + width / 2`）。 |
| `size` | `tuple[float, float]` | ノード寸法 `(width, height)`。 |
| `top` | `float` | 上端 Y 座標（`y + height / 2`）。 |
| `x` | `float` | グローバル中心 X 座標（`xy[0]`）。 |
| `y` | `float` | グローバル中心 Y 座標（`xy[1]`）。 |

## `class` RadialGraph

宣言的な放射状・同心円リング・グラフレイアウトソルバーです。中心ハブを `center` に配置し、接続されたスポークノードを等角度間隔で同心円軌道上に展開します（各リングの半径は `GraphLayout.ring_radii` から取得して軌道円の描画に利用できます）。

```python
from drawlib.graph import RadialGraph

RadialGraph(
    hub: str | None = None,
    *,
    center: tuple[float, float] | None = None,
    radius_step: float | None = None,
    start_angle: float = 0.0,
    angle_range: float = 360.0,
    default_node_width: float = 20.0,
    default_node_height: float = 12.0,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `hub` | `str \| None` | `None` | リング `0` に配置する中心ハブのノード ID（`None` の場合はトポロジーから自動推定）。 |
| `center` | `tuple[float, float] \| None` | `None` | ハブ中心の明示的な `(cx, cy)` 座標（`None` の場合はキャンバス中央）。 |
| `radius_step` | `float \| None` | `None` | 同心円リングごとの半径ステップ幅（`None` の場合はキャンバスに収まるよう自動調整）。 |
| `start_angle` | `float` | `0.0` | 開始角度（度数法、`0.0` = +X 軸方向、反時計回り）。 |
| `angle_range` | `float` | `360.0` | 展開する総角度範囲（`360.0` 全周、`180.0` 半円／扇形など）。 |
| `default_node_width` | `float` | `20.0` | デフォルトのノード幅。 |
| `default_node_height` | `float` | `12.0` | デフォルトのノード高さ。 |

### パブリックメソッド

| メソッド | シグネチャ | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `spoke` | `(parent, spoke_id, *, ring=None, width=None, height=None)` | [`Node`](#node) | スポークノード `spoke_id` を登録し、`parent` からのエッジを同時に張る便利メソッドです。 |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | オプションの同心円 `ring` インデックス付きでノードを登録します。 |
| `edge` | `(src, dst)` | [`Edge`](#edge) | 放射接続またはスポーク間エッジを登録します。 |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | ノード群を囲むグルーピング境界を登録します。 |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | キーワード引数 `nodes` 版の `cluster()` エイリアスです。 |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | 描画を行わずに放射状座標・エッジポート・`ring_radii` を計算します。 |

## `class` TreeGraph

Reingold-Tilford / Buchheim アルゴリズムを用いた宣言的ツリー・グラフレイアウトソルバーです。部分木同士の重なりを防ぎながら、親ノードを子グループの中央上部（`"TB"`）または中央左横（`"LR"`）へ対称的に整列します。

```python
from drawlib.graph import TreeGraph

TreeGraph(
    *,
    root: str | None = None,
    direction: Literal["TB", "LR"] = "TB",
    level_sep: float | None = None,
    sibling_sep: float | None = None,
    default_node_width: float = 22.0,
    default_node_height: float = 12.0,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `root` | `str \| None` | `None` | 明示的なルートノード ID（`None` の場合は入次数 0 のノードから自動検出）。 |
| `direction` | `Literal["TB", "LR"]` | `"TB"` | ツリーの展開方向（`"TB"` 上→下、または `"LR"` 左→右）。 |
| `level_sep` | `float \| None` | `None` | ツリー階層深さ間の固定距離（`None` の場合は自動調整）。 |
| `sibling_sep` | `float \| None` | `None` | 隣接する兄弟ノード／部分木間の最小間隔（`None` の場合は自動調整）。 |
| `default_node_width` | `float` | `22.0` | デフォルトのノード幅。 |
| `default_node_height` | `float` | `12.0` | デフォルトのノード高さ。 |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | 親子間コネクタの配線スタイル（`"orthogonal"` 直交エルボー分岐、または `"straight"` 直線）。 |

### パブリックメソッド

| メソッド | シグネチャ | 戻り値 | 説明 |
| :--- | :--- | :--- | :--- |
| `child` | `(parent, child_id, *, width=None, height=None)` | [`Node`](#node) | 子ノード `child_id`（および未登録の `parent`）を登録し、`parent -> child_id` エッジを追加する便利メソッドです。 |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | ツリーノードを登録します。 |
| `edge` | `(src, dst)` | [`Edge`](#edge) | 親から子へのツリーエッジを登録します。 |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | 部分木や階層レベルを囲む境界クラスタを登録します。 |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | キーワード引数 `nodes` 版の `cluster()` エイリアスです。 |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | 描画を行わずに整列されたツリー座標とコネクタ経路を計算します。 |
