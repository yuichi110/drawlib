# Drawlib `drawlib.graph` 純粋座標計算エンジン化（`calc` 専任化）計画書
(DRAWLIB GRAPH CALC-ONLY REFACTORING PLAN)

- **作成日**: 2026-10-13
- **対象バージョン**: Drawlib `v0.3.1`
- **対象モジュール**:
  - `src/drawlib/_graph/` (`_common/`, `_architecture/`, `_layered/`, `_tree/`, `_radial/`, `_grid/`)
  - `tests/drawlib/graph/test_graph.py`
  - `src/drawlib/_rules/` (`lib_graph.md`, `api.md`, `overview.md`, `anim_guide.md`, `agent_instruction.md`), `.agents/rules/drawlib.md`
  - `docs/docs_src/06_graph/`, `docs/docs_src/07_animations/graphs.md`, `docs/docs_src/05_diagrams/overview.md` 等

---

## 1. 背景と目的 (Executive Summary & Goals)

### 1.1. 現状の課題
`drawlib.graph`（`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`）は、本来「トポロジー（ノード・エッジ・クラスタ）から配置座標を自動計算するソルバー（`calc()`）」として設計されたが、現状では直接描画メソッド `draw()` やコード出力 `export_code()`、および多数の視覚スタイル属性（`style`, `text_style`, `shape`, `arrow_head`, `line_style`, `show`, `label` 等）を併せ持っている。

その結果、以下の問題が生じている：
1. **`drawlib.diagrams` / `drawlib.smartarts` との責務重複と混乱**:
   - `ArchitectureGraph` と `ArchitectureDiagram`、`LayerGraph` と `FlowDiagram`、`TreeGraph` と `TreeNode` のどちらで描画すべきかが曖昧になっている。
   - `graph.draw()` 自体は単純な `rectangle` / `circle` しか描画できないため、アイコンやリッチな装飾を入れたい場合に「ラベル先頭に `\n` を入れて `g.draw()` した後にアイコンを上書き描画する」といった不自然なワークアラウンドが必要になっていた。
2. **API とデータモデルの肥大化**:
   - 座標計算には無関係な `default_node_style`, `default_edge_style`, `style`, `text_style`, `arrow_head`, `show` 等がコンストラクタや `node()` / `edge()` / `cluster()` に並び、利用時の認知負荷が高くなっている。
3. **不要な上位レイヤー依存**:
   - 幾何計算パッケージでありながら、`l4_canvas`（`rectangle`, `circle`, `line`, `text`, `transform`）や `l3_styles`（`Style`, `Styles`）、`l3_fonts`（`Font`）に依存している。

### 1.2. リファクタリングの基本方針（2-Step ワークフローへの特化）
`drawlib.graph` から **`draw()` および `export_code()`、ならびにすべてのスタイル・描画属性を廃止** し、以下の **2-Step ワークフロー** に特化した **「純粋なトポロジー座標計算エンジン（Layout Calculator）」** として再定義する：

```text
[Step 1: 座標計算・確認 (drawlib.graph)]
  トポロジー（ID・サイズ・接続・グループ階層）を登録し、layout = g.calc() を実行
  -> AI / 開発者が print(layout) で座標を確認、またはスクリプト内で layout の座標変数を取得
          │
          ▼
[Step 2: リッチ描画 (drawlib.diagrams / drawlib.shapes)]
  calc() で得た座標（center / bottom_left / local_xy 等）をベースに変数を用意し、
  ArchitectureDiagram, FlowDiagram, ErDiagram, shapes 等でアイコン・装飾を含めて描画
```

---

## 2. API・データモデルの変更仕様

### 2.1. 廃止・削除する要素

| 対象 | 削除内容 |
| :--- | :--- |
| **モジュール削除** | ・`src/drawlib/_graph/_common/_renderer.py` (`render_layout` 等すべて)<br>・`src/drawlib/_graph/_common/_code_generator.py` (`generate_code` 等すべて) |
| **メソッド削除** | ・`BaseGraph.draw()` / `GraphLayout.draw()`<br>・`BaseGraph.export_code()` / `GraphLayout.to_code()`<br>・`BaseGraph._resolve_edge_style()` / `BaseGraph._default_cluster_text_style()` |
| **`BaseGraph` および各ソルバー `__init__`** | ・`default_node_style`, `default_node_text_style`, `default_edge_style`, `default_edge_text_style`, `default_container_style`<br>・`RadialGraph` の `draw_ring_guides`, `ring_guide_style`（※代わりに `GraphLayout` または `RadialGraph` からリング半径情報を参照可能にする） |
| **`Node` / `g.node()` / `.child()` / `.spoke()` / `.cell()`** | ・`label`, `style`, `text_style`, `shape`, `show` を削除<br>・幾何計算に必要な `id`, `width`, `height`（およびソルバー固有の `ring`, `row`, `col`, `layer`, `group`, `subgroup`）のみを残す |
| **`Edge` / `g.edge()`** | ・`label`, `style`, `text_style`, `arrow_head`, `line_style`, `show` を削除（`child()` / `spoke()` の `edge_label`, `edge_style`, `arrow_head`, `edge_show` も削除）<br>・`g.edge(src: str, dst: str) -> Edge` のみに単純化 |
| **`Cluster` / `g.cluster()` / `g.group()` / `.cluster_row()` / `.cluster_column()`** | ・`label`, `style`, `text_style`, `show` を削除<br>・`id`, `nodes`, `padding`, `header_height`（旧 `label` 有無による上部余白 `3.5` の代替、デフォルト `3.5`）, `parent`, `order`, `pos` のみを残す |
| **`NodeLayout` / `EdgeLayout` / `ClusterLayout`** | ・`style`, `text_style`, `label`, `shape`, `arrow_head`, `show` を削除 |

---

### 2.2. 新しい `BaseGraph` および登録 API シグネチャ

```python
class BaseGraph(ABC):
    def __init__(
        self,
        *,
        default_node_width: float = 20.0,
        default_node_height: float = 12.0,
    ) -> None: ...

    def node(
        self,
        id: str,
        *,
        width: float | None = None,
        height: float | None = None,
        ring: int | None = None,
        row: int | None = None,
        col: int | None = None,
        layer: int | None = None,
        group: str | None = None,
        subgroup: str | None = None,
    ) -> Node: ...

    def edge(self, src: str, dst: str) -> Edge: ...

    def cluster(
        self,
        id: str,
        nodes: list[str] | None = None,
        *,
        padding: float = 4.0,
        header_height: float = 3.5,
        parent: str | None = None,
        order: int | None = None,
        pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
    ) -> Cluster: ...

    def group(
        self,
        id: str,
        *,
        nodes: list[str] | None = None,
        padding: float = 4.0,
        header_height: float = 3.5,
        parent: str | None = None,
        order: int | None = None,
        pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
    ) -> Cluster: ...

    @abstractmethod
    def calc(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout: ...
```

各ソルバー固有のヘルパーメソッドも同様にスリム化する：
- `TreeGraph.child(parent: str, child_id: str, *, width: float | None = None, height: float | None = None) -> Node`
- `RadialGraph.spoke(parent: str, spoke_id: str, *, ring: int | None = None, width: float | None = None, height: float | None = None) -> Node`
- `GridGraph.cell(cell_id: str, row: int | None = None, col: int | None = None, *, width: float | None = None, height: float | None = None) -> Node`
- `GridGraph.cluster_row(row: int, cluster_id: str, *, padding: float = 4.0, header_height: float = 3.5) -> Cluster`
- `GridGraph.cluster_column(col: int, cluster_id: str, *, padding: float = 4.0, header_height: float = 3.5) -> Cluster`

---

### 2.3. Step 1 (`print` 確認) & Step 2 (`diagrams` 連携) のための `GraphLayout` 強化

`drawlib.diagrams` や `drawlib.shapes` の各コンポーネントへ座標をそのまま渡せるよう、計算結果モデル（`NodeLayout`, `ClusterLayout`, `EdgeLayout`, `GraphLayout`）の座標プロパティと文字列表現（`__str__`）を強化する。

#### 1. `NodeLayout`
- `id: str`
- `xy: tuple[float, float]` — 中心座標 `(cx, cy)`（`ArchitectureDiagram.add(node, xy=...)`, `FlowDiagram.add(node, xy=...)`, `shapes.rectangle(xy, ...)` に直結）
- `width: float`, `height: float`
- `parent_id: str | None = None` — 所属する最内クラスタ ID
- `local_xy: tuple[float, float]` — 所属クラスタの左下 `(cluster.left, cluster.bottom)` を原点とした相対中心座標（所属クラスタがない場合は `xy` と同値）。**`ArchitectureDiagram` の `group.add(node, xy=n.local_xy)` にそのまま渡せる**。
- プロパティ:
  - `.x -> float`, `.y -> float`, `.center -> tuple[float, float]`
  - `.size -> tuple[float, float]` (`(width, height)`)
  - `.left -> float`, `.right -> float`, `.bottom -> float`, `.top -> float`
  - `.bottom_left -> tuple[float, float]` (`(left, bottom)` — `ErDiagram`, `ClassDiagram`, `SmartArts` に直結)

#### 2. `ClusterLayout`
- `id: str`
- `bbox: tuple[float, float, float, float]` — `(cx, cy, width, height)`
- `parent_id: str | None = None` — 親クラスタ ID
- `local_bottom_left: tuple[float, float]` — 親クラスタの左下を原点とした相対左下座標（親がない場合は `bottom_left` と同値）。**ネストされた `parent_group.add(child_group, xy=c.local_bottom_left)` にそのまま渡せる**。
- プロパティ:
  - `.cx -> float`, `.cy -> float`, `.xy -> tuple[float, float]`, `.center -> tuple[float, float]` (`(cx, cy)` — `shapes.rectangle(c.xy, c.width, c.height)` に直結)
  - `.width -> float`, `.height -> float`, `.size -> tuple[float, float]` (`(width, height)`)
  - `.left -> float`, `.right -> float`, `.bottom -> float`, `.top -> float`
  - `.bottom_left -> tuple[float, float]` (`(left, bottom)` — **`ArchitectureDiagram.add(group, xy=c.bottom_left)` にそのまま渡せる**）

#### 3. `EdgeLayout`
- `src: str`, `dst: str`
- `src_port: tuple[float, float]`, `dst_port: tuple[float, float]`
- `waypoints: list[tuple[float, float]] = field(default_factory=list)`
- プロパティ:
  - `.points -> list[tuple[float, float]]` (`[src_port, *waypoints, dst_port]` — `lines(e.points)` に直結)
  - `.mid_xy -> tuple[float, float]`（経路の中点座標 — エッジラベル等の配置に直結）

#### 4. `GraphLayout`
- `nodes: dict[str, NodeLayout]`
- `edges: list[EdgeLayout]`
- `clusters: dict[str, ClusterLayout]`
- `width: float`, `height: float`
- `ring_radii: dict[int, float] = field(default_factory=dict)`（`RadialGraph` で算出された各リングの半径）
- `offset(node_id: str, dx: float = 0.0, dy: float = 0.0) -> Self`:
  - 指定ノードの中心座標と `local_xy`、および接続エッジのポートを `(dx, dy)` シフトし、メソッドチェーン可能（`return self`）にする。
- `__str__(self) -> str`（AI・開発者向けの視認性の高い座標レポート出力）:
  - `print(g.calc(width=120, height=80))` を実行した際、以下のような構造化サマリを出力する：
    ```text
    GraphLayout(width=120.0, height=80.0)
    Clusters:
      vpc        : bottom_left=(32.0, 10.0), center=(76.0, 45.0), size=(88.0, 70.0)
      app_tier   : bottom_left=(36.0, 14.0), center=(56.0, 43.0), size=(40.0, 58.0), parent='vpc', local_bottom_left=(4.0, 4.0)
    Nodes:
      client     : xy=(14.0, 45.0), bottom_left=(4.0, 39.0), size=(20.0, 12.0)
      api        : xy=(56.0, 56.0), bottom_left=(46.0, 50.0), size=(20.0, 12.0), parent='app_tier', local_xy=(20.0, 42.0)
    Edges:
      client -> api : points=[(24.0, 45.0), (35.0, 45.0), (35.0, 56.0), (46.0, 56.0)], mid_xy=(35.0, 50.5)
    ```

---

## 3. 利用イメージ（Before / After）

### Step 1 & Step 2 による `ArchitectureDiagram` との連携例

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Container, Edge, GcpIcon, Node
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=126, height=86)

# Step 1: ArchitectureGraph でトポロジーとサイズのみを宣言し座標を計算
g = ArchitectureGraph(direction="LR", default_node_width=20.0, default_node_height=16.0)
g.group("vpc")
g.cluster("app_tier", ["api", "worker"], parent="vpc", order=1, padding=5.0)
g.cluster("data_tier", ["db"], parent="vpc", order=2, padding=5.0)
g.node("client")
g.edge("client", "api")
g.edge("api", "worker")
g.edge("worker", "db")

layout = g.calc(width=126.0, height=86.0)
# AI 確認時は print(layout) で全座標を確認可能

# Step 2: 算出された座標をベースに ArchitectureDiagram でリッチに描画
d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral.patch(shape_r=1.5),
)

c_vpc = layout.clusters["vpc"]
c_app = layout.clusters["app_tier"]
c_data = layout.clusters["data_tier"]

vpc = d.add(Container("Production VPC", width=c_vpc.width, height=c_vpc.height, style=Styles.PrimaryNeutral), xy=c_vpc.bottom_left)
app_grp = vpc.add(Container("Compute Tier", width=c_app.width, height=c_app.height, style=Styles.White), xy=c_app.local_bottom_left)
data_grp = vpc.add(Container("Data Tier", width=c_data.width, height=c_data.height, style=Styles.SecondaryNeutral), xy=c_data.local_bottom_left)

n_client = d.add(Node("Client", icon=GcpIcon.CLOUD_CDN), xy=layout.nodes["client"].xy)
n_api = app_grp.add(Node("API Gateway", icon=GcpIcon.APIGEE_API_PLATFORM, card_style=Styles.PrimaryFlat, text_style=Styles.WhiteBold), xy=layout.nodes["api"].local_xy)
n_worker = app_grp.add(Node("Cloud Run", icon=GcpIcon.CLOUD_RUN), xy=layout.nodes["worker"].local_xy)
n_db = data_grp.add(Node("Cloud SQL", icon=GcpIcon.CLOUD_SQL), xy=layout.nodes["db"].local_xy)

d.add_edge(Edge(n_client, n_api, text="HTTPS"))
d.add_edge(Edge(n_api, n_worker, text="gRPC"))
d.add_edge(Edge(n_worker, n_db, text="SQL"))

d.draw()
save()
```

---

## 4. 実装フェーズと作業ステップ

| フェーズ | 対象 | 作業内容 |
| :--- | :--- | :--- |
| **Phase 1: コア実装 (`src/drawlib/_graph/`)** | `_common/_models.py`<br>`_common/_base.py`<br>`_common/_routing.py`<br>5つの `_*/*_graph.py`<br>`_renderer.py` (削除)<br>`_code_generator.py` (削除) | 1. `_renderer.py` と `_code_generator.py` を削除<br>2. `_models.py` からスタイル・描画属性を削除し、`bottom_left`, `local_xy`, `local_bottom_left`, `mid_xy`, `GraphLayout.__str__()` を実装<br>3. `_base.py` および5つのソルバー（`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`）から `draw()`, `export_code()`, スタイル引数を削除し、親子クラスタ相対座標の計算を組み込む<br>4. 同時に残りの内部モジュール（`_slide/helpers.py`, `_geomap.py`, `_cli/_visualizers/`）の公開ファサード import も内部レイヤーへ整理 |
| **Phase 2: 単体テスト更新 (`tests/drawlib/graph/`)** | `tests/drawlib/graph/test_graph.py` | 1. 全5ソルバーの `calc()` テストを新しいシグネチャに更新<br>2. `local_xy`, `local_bottom_left`, `bottom_left`, `mid_xy`, `offset()`, `str(layout)` の単体テストを追加 |
| **Phase 3: エージェントルール更新 (`src/drawlib/_rules/`, `.agents/rules/`)** | `lib_graph.md`<br>`api.md`<br>`overview.md`<br>`anim_guide.md`<br>`agent_instruction.md`<br>`.agents/rules/drawlib.md` | 1. `lib_graph.md` を「Step 1: `g.calc()` & `print(layout)` → Step 2: `diagrams` / `shapes` で描画」の2-Step ガイドへ全面改訂<br>2. `api.md`, `overview.md`, `anim_guide.md` のシグネチャとコード例を更新 |
| **Phase 4: ドキュメント更新 (`docs/*_src/`) & ビルド検証** | `docs/docs_src/06_graph/*.md`<br>`docs/docs_src/07_animations/graphs.md`<br>`docs/docs_src/05_diagrams/overview.md`<br>`docs/drawlib-dogfooding*_src/10_diagrams.md`<br>`docs/slide_about_drawlib_src/04_diagrams_and_graphs/*.md`<br>`docs/architecture_src/03_domain_subsystems/03_graph_autolayout.md` | 1. `06_graph/` 全6ページおよび関連ページのコードブロックと説明を `calc()` + `diagrams` / `shapes` 描画に刷新<br>2. `./dcli code-check all`、`./dcli test all`、`./dcli docs build` で全テストとドキュメントビルドを検証 |
