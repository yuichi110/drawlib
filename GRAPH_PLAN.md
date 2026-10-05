# Drawlib グラフレイアウトエンジン設計計画書
(DRAWLIB GRAPH ENGINE PLAN)

- **作成日**: 2026-10-05
- **対象バージョン**: Drawlib 次期マイナーリリース
- **対象モジュール**:
  - `src/drawlib/graph.py` (公開ファサード)
  - `src/drawlib/_graph/` (内部レイアウト計算・レンダリングエンジン)
  - `tests/test_graph.py` (単体テスト・結合テスト)
  - `docs_src/05_diagrams/graph.md` (公式ドキュメント)
  - `src/drawlib/_rules/` (AIエージェント向けルール・ガイドライン)

---

## 1. エグゼクティブサマリー & 背景 (Executive Summary & Background)

### 1.1. 課題認識（コールドスタート問題）
Drawlib は「決定論的で崩れない美しい図版をコードで作成する（Illustration as Code）」という理念に基づき、絶対座標による厳密なレイアウト制御を提供しています。
しかし、ドッグフーディングにおいて以下のフィードバックが寄せられました：

> 「最初からコンポーネントの綺麗な座標を求めるのが難しそうなので、一発目は Graphviz で書いて、それを見たうえで調整をかけて具体的な座標を定めるなどのアプローチができるとよさそう」

ゼロからノードのトポロジー（論理関係）とピクセル座標（幾何美観）を同時に計算しようとすると、人間にとっても AI にとってもワーキングメモリが逼迫します（**コールドスタート問題**）。

### 1.2. 本計画のゴール
Drawlib は外部の C バイナリ（Graphviz 等）に一切依存しない **Pure Python** のライブラリです。
本計画では、Graphviz 等の外部ツールを導入することなく、Drawlib 内部に **「用途に応じた軽量・堅牢な自動配置エンジン（Layout Solver）」** を構築し、以下の3大価値を実現します：

1. **トポロジーの宣言的記述**: ノード・エッジ・クラスタを宣言するだけで、美しい座標を自動算出。
2. **計算と描画の責務分離 (`calc()` vs `draw()`)**:
   - `calc()`: 座標計算のみを行い、幾何データ構造（`GraphLayout`）を返す。
   - `draw()`: 計算結果を Drawlib の標準スタイルでキャンバスに一括描画する。
3. **下書きから清書への架け橋 (`export_code()`)**:
   - 自動配置された座標を変数化した Drawlib Python コードを書き出すことで、「大枠は自動配置 → こだわりたい箇所だけ絶対座標で微調整」という理想の二段階ワークフローをライブラリ単体で完結させる。
4. **用途別の専門クラス分離**:
   - `ArchitectureGraph`: クラウド・Web・多層アーキテクチャ（階層型・VPCクラスタ境界）
   - `TreeGraph`: 組織図・決定木・AST（対称整列ツリー）
   - `RadialGraph`: イベント駆動・Kafka/PubSub・ハブ＆スポーク（同心円・放射状）

---

## 2. アーキテクチャ設計 (Architecture Design)

### 2.1. モジュール構成 (Package Structure)

```text
src/drawlib/
├── graph.py                      # 公開ファサード (ArchitectureGraph, TreeGraph, RadialGraph, GraphLayout)
└── _graph/                       # 内部実装パッケージ
    ├── __init__.py
    ├── _models.py                # データ構造 (Node, Edge, Cluster, Port, GraphLayout)
    ├── _base.py                  # BaseGraph (ノード・エッジ登録, calc, draw, export_code の共通骨格)
    ├── _architecture.py          # ArchitectureGraph (多層階層型 DAG レイアウトエンジン)
    ├── _tree.py                  # TreeGraph (Reingold-Tilford 対称ツリーレイアウトエンジン)
    ├── _radial.py                # RadialGraph (同心円・放射状レイアウトエンジン)
    ├── _renderer.py              # Drawlib プリミティブ (shapes, lines, text) による自動描画アダプタ
    └── _code_generator.py        # 計算済み座標を変数化した Python コード生成器
```

### 2.2. レイヤーと責務の分離 (Layer Separation)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        User / Agent Python Script                      │
│   g = ArchitectureGraph(direction="LR")                                │
│   g.node(...), g.edge(...), g.cluster(...)                             │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
                   ▼ (1. 座標だけ欲しい)             ▼ (2. そのまま描画したい)
           ┌──────────────┐                  ┌──────────────┐
           │   g.calc()   │                  │   g.draw()   │
           └──────┬───────┘                  └──────┬───────┘
                  │                                 │
                  ▼                                 │
         ┌───────────────────┐                      │
         │    GraphLayout    │                      │
         │ - nodes: dict     │                      │
         │ - clusters: dict  │                      │
         │ - edges: list     │                      │
         └────────┬──────────┘                      │
                  │                                 │
      ┌───────────┴───────────┐                     │
      ▼                       ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ export_code() │     │ 手動微調整    │     │ _renderer.py  │
│ (コード出力)  │     │ (Offset/Override)   │ (canvas描画)  │
└───────────────┘     └───────────────┘     └───────────────┘
```

---

## 3. クラス別 API 仕様とアルゴリズム (Class Specifications & Algorithms)

### 3.1. 共通基底クラス: `BaseGraph`

すべてのグラフクラスは `BaseGraph` を継承し、ノード・エッジの登録構文と、出力メソッドを完全に共有します。

```python
class BaseGraph(ABC):
    """Abstract base class for all declarative graph layout solvers."""

    def node(
        self,
        id: str,
        label: str | None = None,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        shape: Literal["rectangle", "circle", "rounded_rectangle"] = "rectangle",
        icon: str | None = None,
        width: float | None = None,
        height: float | None = None,
    ) -> Node:
        """Register a node in the graph."""

    def edge(
        self,
        src: str,
        dst: str,
        label: str | None = None,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        arrow_head: Literal["->", "<-", "<->", "-"] = "->",
        line_style: Literal["solid", "dashed", "dotted"] | None = None,
    ) -> Edge:
        """Register a directed or undirected edge between two nodes."""

    @abstractmethod
    def calc(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Compute coordinates without rendering. Returns GraphLayout geometry."""

    def draw(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Calculate layout and render onto current canvas in a single step."""
        layout = self.calc(width=width, height=height, margin=margin)
        layout.draw()
        return layout

    def export_code(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> str:
        """Calculate layout and return copy-pasteable Drawlib Python code."""
        layout = self.calc(width=width, height=height, margin=margin)
        return layout.to_code()
```

---

### 3.2. `ArchitectureGraph`（クラウド・多層アーキテクチャ）

#### 目的
Web システム、マイクロサービス、クラウドインフラ（VPC・サブネット）、ETL パイプラインなど、**「左から右（LR）」** または **「上から下（TB）」** に流れる多層構造の自動配置。

#### 特有の API
```python
class ArchitectureGraph(BaseGraph):
    def __init__(
        self,
        *,
        direction: Literal["LR", "TB"] = "LR",
        rank_sep: float | None = None,    # 階層（ランク）間の距離
        node_sep: float | None = None,    # 同一階層内のノード間距離
        default_node_style: Style | None = None,
        default_edge_style: Style | None = None,
    ) -> None: ...

    def cluster(
        self,
        id: str,
        nodes: list[str],
        label: str | None = None,
        *,
        style: Style | None = None,       # 例: Styles.MutedDashed
        text_style: Style | None = None,
        padding: float = 4.0,
    ) -> Cluster:
        """Register a grouping boundary surrounding a subset of nodes."""

    def tier(
        self,
        name: str,
        nodes: list[str],
        rank_order: int | None = None,
    ) -> None:
        """Explicitly pin specific nodes to a semantic tier/rank."""
```

#### 配置アルゴリズム（Lightweight Sugiyama Framework）
1. **Cycle Breaking**: DFS によりバックエッジを検出し、トポロジカルソート可能な DAG に一時反転。
2. **Rank Assignment**: 
   - `tier()` で明示されたランクを最優先。
   - 未指定のノードは、ルート（入次数0）からの最長経路長により Rank $0, 1, 2, \dots$ を自動決定。
3. **Cluster Cohesion**: 同一クラスタに属するノード同士が散り散りにならないよう、クラスタ内ノードを隣接ランク・スロットにグループ化。
4. **Crossing Reduction (Barycenter Heuristic)**: 前後ランクの接続先重心を計算し、同階層内の並び順をソートして線の交差を最小化。
5. **Coordinate Mapping**: キャンバスの `width` と `height`（未指定時は `drawlib.canvas` の現在設定から取得）にスケーリングし、外周マージンを均等確保。クラスタのバウンディングボックスもノードを内包する形で自動計算。

---

### 3.3. `TreeGraph`（木構造・組織図・AST）

#### 目的
決定木、組織図、ディレクトリツリー、文法解析木など、1つまたは少数の親ノードから放射状に子ツリーが広がる構造の自動配置。

#### 特有の API
```python
class TreeGraph(BaseGraph):
    def __init__(
        self,
        *,
        root: str | None = None,          # 明示的なルートノード（省略時は入次数0のノード）
        direction: Literal["TB", "LR"] = "TB",
        level_sep: float | None = None,   # 世代間の距離
        sibling_sep: float | None = None, # 兄弟ノード間の距離
        subtree_sep: float | None = None, # サブツリー間の最小余白
    ) -> None: ...

    def child(
        self,
        parent: str,
        child_id: str,
        label: str | None = None,
        *,
        style: Style | None = None,
        edge_label: str | None = None,
    ) -> Node:
        """Convenient shorthand for parent-child registration."""
```

#### 配置アルゴリズム（Reingold-Tilford / Walker Tidy Tree）
1. **後順走査（Post-order Traversal）**:
   - 各サブツリーの輪郭（Left/Right Contour）を計算し、隣接するサブツリー同士が絶対に重ならない最小オフセットを算出。
2. **前順走査（Pre-order Traversal）**:
   - 親ノードを子ノード群の幾何学的中心（中点）に配置しながら、全体をシフトして対称性を確立。
3. 矢印は直角配線（Manhattan routing）または滑らかなベジェ線を選択可能。

---

### 3.4. `RadialGraph`（放射状・ハブ＆スポーク）

#### 目的
Kafka や EventBus を中心としたイベント駆動アーキテクチャ、API Hub、トピック購読トポロジー、同心円概念図の自動配置。

#### 特有の API
```python
class RadialGraph(BaseGraph):
    def __init__(
        self,
        hub: str,                         # 中心ハブノードID
        *,
        radius_step: float | None = None, # 同心円リングの間隔
        start_angle: float = 0.0,         # 配置開始角度（度）
        angle_range: float = 360.0,       # 扇状配置時の展開角度（180度で半円等）
    ) -> None: ...

    def spoke(
        self,
        spoke_id: str,
        label: str | None = None,
        *,
        style: Style | None = None,
        ring: int = 1,                    # 所属する同心円リング番号 (1, 2, ...)
        edge_label: str | None = None,
    ) -> Node:
        """Register a spoke node directly connected to hub or specific ring."""
```

#### 配置アルゴリズム（Concentric Ring Partitioning）
1. **Ring Assignment**: ハブからのホップ数（BFS）または明示された `ring` 番号に基づき、ノードを同心円 $R_1, R_2, \dots$ に分類。
2. **Angle Equidistant Distribution**:
   - 各リング $k$ に含まれるノード数 $N_k$ に応じて、角度を均等分割（$\theta_i = \theta_{start} + i \cdot \frac{\text{angle\_range}}{N_k}$）。
   - 中心座標 $(cx, cy)$ から $(cx + R_k \cos\theta_i, cy + R_k \sin\theta_i)$ に極座標変換。
3. エッジ接続はハブの外周からスポーク外周への最短幾何交点（放射線）を自動計算。

---

### 3.5. 幾何計算結果オブジェクト: `GraphLayout`

`calc()` メソッドが返すデータ構造です。描画に必要なすべての幾何情報を保持し、ユーザーが手動で介入・微調整できるよう設計します。

```python
@dataclass
class NodeLayout:
    id: str
    xy: tuple[float, float]               # 中心座標 (cx, cy)
    width: float
    height: float
    style: Style
    text_style: Style
    label: str
    shape: str
    icon: str | None = None

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        """(x_min, y_min, x_max, y_max) bounding box."""

@dataclass
class EdgeLayout:
    src: str
    dst: str
    src_port: tuple[float, float]         # 接続開始点（ノード外周境界）
    dst_port: tuple[float, float]         # 接続終了点（ノード外周境界）
    waypoints: list[tuple[float, float]]  # 直角配線時の中間経路
    label: str | None
    style: Style
    text_style: Style
    arrow_head: str

@dataclass
class ClusterLayout:
    id: str
    label: str | None
    bbox: tuple[float, float, float, float] # (cx, cy, width, height)
    style: Style
    text_style: Style

class GraphLayout:
    """Complete geometrical result calculated by graph solvers."""
    nodes: dict[str, NodeLayout]
    edges: list[EdgeLayout]
    clusters: dict[str, ClusterLayout]
    width: float
    height: float

    def offset(self, node_id: str, dx: float = 0.0, dy: float = 0.0) -> None:
        """Fine-tune individual node coordinate after auto-calculation."""

    def draw(self) -> None:
        """Render all elements to current canvas using Drawlib primitives."""

    def to_code(self) -> str:
        """Export clean, formatted Drawlib Python script."""
```

---

## 4. `export_code()` の出力コード例 (Code Export Format)

ユーザーが `print(g.export_code())` を実行した際に出力されるコードの具体例です。
Drawlib の [style-guide.md](file:///usr/local/google/home/yuichiito/git_github/drawlib/.agents/rules/style_guide.md)（セマンティック座標変数、Z-Order、等間隔配置）に 100% 準拠したクリーンな Python コードが生成されます。

```python
from drawlib.canvas import setup, save
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=140, height=70)

# =============================================================================
# 1. Semantic Coordinates (Calculated by ArchitectureGraph)
# =============================================================================
client_xy  = (22.5, 35.0)
gateway_xy = (55.0, 35.0)
auth_xy    = (87.5, 48.0)
orders_xy  = (87.5, 22.0)
db_xy      = (120.0, 22.0)

# =============================================================================
# 2. Clusters & Boundaries (Z-Order Layer 1)
# =============================================================================
# Internal VPC Cluster
rectangle((97.5, 35.0), width=58.0, height=44.0, style=Styles.MutedDashed, text="Internal VPC")

# =============================================================================
# 3. Connections & Edges (Z-Order Layer 2)
# =============================================================================
line((33.5, 35.0), (44.0, 35.0), arrow_head="->", style=Styles.DarkBold)  # client -> gateway
line((66.0, 39.0), (76.5, 48.0), arrow_head="->", style=Styles.DarkBold)  # gateway -> auth
line((66.0, 31.0), (76.5, 22.0), arrow_head="->", style=Styles.DarkBold)  # gateway -> orders
line((98.5, 22.0), (109.0, 22.0), arrow_head="->", style=Styles.DarkBold) # orders -> db

# =============================================================================
# 4. Nodes (Z-Order Layer 3)
# =============================================================================
rectangle(client_xy, width=22.0, height=14.0, style=Styles.AccentFlat, text="Web App")
rectangle(gateway_xy, width=22.0, height=14.0, style=Styles.PrimaryFlat, text="API Gateway")
rectangle(auth_xy, width=22.0, height=14.0, style=Styles.SecondaryFlat, text="Auth Service")
rectangle(orders_xy, width=22.0, height=14.0, style=Styles.SecondaryFlat, text="Order Service")
rectangle(db_xy, width=22.0, height=14.0, style=Styles.SecondaryFlat, text="Primary DB")

save()
```

---

## 5. 実装ロードマップ (Phased Implementation Roadmap)

### フェーズ 1: コア幾何モデル ＆ `ArchitectureGraph`（MVP 実装）
- `src/drawlib/_graph/_models.py`（Node, Edge, Cluster, GraphLayout）
- `src/drawlib/_graph/_base.py`（BaseGraph 共通抽象クラス）
- `src/drawlib/_graph/_architecture.py`（多層階層型 Sugiyama 配置エンジン）
- `src/drawlib/_graph/_renderer.py`（Drawlib 描画アダプタ）
- `src/drawlib/_graph/_code_generator.py`（`export_code` 生成器）
- `src/drawlib/graph.py`（公開ファサード）
- **動作検証**: サンプルコードによる画像描画と `export_code()` の出力テスト

### フェーズ 2: `TreeGraph` ＆ `RadialGraph` の追加
- `src/drawlib/_graph/_tree.py`（Reingold-Tilford 左右/上下整列ツリー）
- `src/drawlib/_graph/_radial.py`（ハブ＆スポーク同心円・角度均等分割配置）
- `graph.py` からのエクスポートと単体テスト

### フェーズ 3: 堅牢性強化 ＆ テストスイート
- 閉路（Cycles）や多重エッジを含む複雑な有向グラフのストレステスト
- 10〜30ノード規模の大規模トポロジーでの自動スケーリング検証
- `tests/test_graph.py` による自動テスト網羅（カバレッジ > 90%）
- `./dcli check all`（Ruff, Ty, Docstrings）の完全パス

### フェーズ 4: 公式ドキュメント ＆ AI エージェントガイド更新
- `docs_src/05_diagrams/graph.md`（利用ガイドと埋め込みサンプル図版）
- `src/drawlib/_rules/agent_instruction.md` および `.agents/rules/docs.md` の更新
  - AI エージェントが作図時に `ArchitectureGraph` 等を活用してコールドスタートを回避する指示を追加。

---

## 6. 検証方針 (Testing & Verification)

1. **アルゴリズム整合性テスト**:
   - 閉路グラフ（A -> B -> C -> A）を入力しても無限ループにならず DAG として整列されること。
   - クラスタ指定時、クラスタ内の全ノードがバウンディングボックス内に収まり、他クラスタと交差しないこと。
2. **キャンバス枠収束テスト**:
   - 指定された `width` / `height` および `margin` の境界内に、すべてのノード・エッジ・ラベルが収まり、はみ出し（Clipping）が発生しないこと。
3. **視覚的一致性テスト (Pixel Matching)**:
   - `test_graph.py` において、`ArchitectureGraph`, `TreeGraph`, `RadialGraph` でレンダリングした画像をスナップショット比較（Match Rate > 95%）。
4. **Code Export 再現性テスト**:
   - `export_code()` で出力された Python スクリプトを実行して生成された画像と、`g.draw()` で直接レンダリングされた画像がピクセル単位で完全一致すること。
