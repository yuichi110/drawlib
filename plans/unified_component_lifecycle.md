# Unified Component Lifecycle & Spatial Rendering Plan

## 1. 背景と設計思想 (Core Philosophy)

`drawlib` の高レベルコンポーネント群（`smartarts`, `charts`, `diagrams`, `graph`）において、静止画の再利用性（複数配置・状態比較・条件付きハイライト）およびアニメーション（`drawlib.anim`）の表現力を最大化するため、**全モジュール共通のコンポーネント・ライフサイクル**を定義・標準化する。

### 基本原則：時間軸を描画クラスに持ち込まない（単一責任の原則）
- コンポーネント自身には `progress` のような「時間軸（タイムライン）」の概念を持たせない。
- コンポーネントの責務は **「現在の内部状態（要素の値・スタイル）を、指定された空間座標・サイズ・スケール `(xy, width, height, scale)` に純粋に描画すること」** に限定する。
- 時間変化や状態遷移は、呼び出し側（ユーザーの `for` ループやロジック）が **① `draw()` の空間引数を変える**、または **② `add` 系メソッドが返した要素インスタンスの属性を上書きする** ことで自在に表現する。
- **要素追加メソッドの名称統一 (`add` への一本化)**:
  これまで `SmartArts` 内で `add()`（`Pyramid`, `BulletPoints`, `GridLayout`）と `append()`（`BoxList`, `ChevronProcess`, `Cycle`）に分裂していたメソッド名を、ライブラリ全体（`diagrams`, `charts`, `smartarts`）で **`add()` に完全一本化**する（`append` は廃止し、`add` に統一する）。

---

## 2. 標準コンポーネント・ライフサイクル（4フェーズ）

すべての高レベルコンポーネントは、以下の4フェーズで統一的に操作できるようにする。

```text
[1. Construct]          [2. Populate]               [3. Mutate (任意)]                [4. Spatial Render]
comp = Component(...) ──► item = comp.add(...)   ──► item.show = True / False      ──► comp.draw(
                          s = chart.add_series(...)   s.draw_ratio = 0.6                xy=(x, y),
                          n = diag.add(...)           s.draw_direction = "left_to_right" width=w, height=h,
                          (要素インスタンスを返却)      item.style = ...                  scale=s
                                                      (描画制御・属性を直接上書き可能)   )
```

### コードイメージ

#### パターンA：コンポーネント全体の移動・拡大縮小（空間パラメータの変化）
```python
chart = BarChart(axis_line_style=Styles.Primary, categories=["Q1", "Q2", "Q3"])
chart.add_series("Revenue", [45, 68, 92], style=Styles.PrimaryFlat)

for x, s in [(10, 0.5), (20, 0.75), (30, 1.0)]:
    with anim.frame():
        chart.draw(xy=(x, 15), scale=s)
```

#### パターンB：グラフ軸の絶対値固定と `draw_ratio` / `draw_direction` による部分描画
元データ（`values`）を直接書き換えなくても、要素インスタンスの **`draw_ratio`（0.0〜1.0）** と **`draw_direction`（`"left_to_right"` / `"bottom_to_top"`）** を指定するだけで、棒グラフの伸長や折れ線グラフの左から右への描画が直感的に行える。

```python
# 1. BarChart の例：Y軸の絶対値 (0〜100) を固定し、下→上 (bottom_to_top) にバーを伸ばす
chart = BarChart(axis_line_style=Styles.Primary, categories=["Q1", "Q2", "Q3"])
chart.configure_y_axis(min_value=0, max_value=100)
s_2025 = chart.add_series("2025", [40, 55, 70], style=Styles.Neutral)
s_2026 = chart.add_series("2026", [60, 80, 95], style=Styles.PrimaryFlat)
s_2026.draw_direction = "bottom_to_top"

for r in [0.2, 0.4, 0.6, 0.8, 1.0]:
    with anim.frame():
        s_2026.draw_ratio = r
        chart.draw(xy=(10, 10))

# 2. LineChart の例：左→右 (left_to_right) に折れ線を伸ばす
line_chart = LineChart(axis_line_style=Styles.Primary, categories=["Jan", "Feb", "Mar", "Apr"])
line_chart.configure_y_axis(min_value=0, max_value=120)
trend = line_chart.add_series("Users", [30, 55, 80, 110], style=Styles.Primary)
trend.draw_direction = "left_to_right"

for r in [0.25, 0.5, 0.75, 1.0]:
    with anim.frame():
        trend.draw_ratio = r
        line_chart.draw(xy=(10, 10))
```

#### パターンC：`show` 属性によるレイアウト固定での順次出現・ハイライト
あらかじめ全要素を `add()` して全体レイアウト（箱のサイズや間隔、グラフの座標）を確定させた上で、各要素の **`show: bool`** や **`style`** を切り替えることで、レイアウトが途中でガタつくことなく要素を1つずつ出現・強調できる。

```python
pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold,
    description_style=Styles.Muted,
)
steps = [
    pipeline.add("1. Build", description="Compile", show=False),
    pipeline.add("2. Test", description="Unit & E2E", show=False),
    pipeline.add("3. Deploy", description="Production", show=False),
]

# 3ステップ分の全体レイアウト幅を維持したまま、左から1つずつ出現させる
for step in steps:
    step.show = True
    with anim.frame():
        pipeline.draw(xy=(10, 20), width=100, height=15)
```

---

## 3. 現状のモジュール別対応状況とギャップ分析

| モジュール | 要素追加メソッド名の統一 (`add` 系) | 要素追加時のインスタンス返却 | 要素単位の表示制御 (`show: bool`) | チャート部分描画 (`draw_ratio` / `draw_direction`) | `draw()` での位置 `xy`・サイズ (`width`/`height`) 指定 | `draw()` での比例拡大縮小 (`scale`) 指定 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`smartarts`** | ❌ (`add` と `append` が混在) | ❌ (`None` を返却) | ❌ 未対応 | ➖ | ✅ 大半が対応済 (`TreeNode` 等を除く) | ❌ 未対応 |
| **`charts`** | ✅ 対応済 (`add` / `add_*`) | ✅ 対応済 (`Series`, `Slice`, `Task` 等を返却) | ❌ 未対応 | ❌ 未対応 | ⚠️ `xy` のみ (`width`/`height` は `__init__` のみ) | ❌ 未対応 |
| **`diagrams`** | ✅ 対応済 (`add`) | ✅ 対応済 (`Node`, `Edge`, `Entity` 等を返却) | ❌ 未対応 | ➖ | ✅ `xy` 対応済 (サイズは各ノード座標ベース) | ❌ 未対応 |
| **`graph`** | ✅ 対応済 (`node`, `edge`, `cluster`) | ✅ 対応済 (`Node`, `Edge`, `Cluster` を返却) | ❌ 未対応 | ➖ | ⚠️ サイズのみ (`xy` は常に `(0,0)` 基準) | ❌ 未対応 |

---

## 4. 詳細設計仕様

### 4.1. 柱①：要素追加メソッドの `add` への完全統一とミュータブル・インスタンスの返却

#### A. `drawlib.smartarts` の改修（`append` の廃止と `add` への一本化）
- `BoxList`, `ChevronProcess`, `Cycle` の `append()`（および `insert()` / `extend()`）を廃止し、他の SmartArt（`Pyramid`, `BulletPoints`, `GridLayout`）や `diagrams` と同じく **`add()` に完全一本化**する。
- `TreeNode` および `MindMapNode` にも、子ノードを追加してそのインスタンスを返す `add()` メソッドを追加する。
- すべての `add()` メソッドは、追加された要素オブジェクト（ミュータブルなインスタンス）を返す。

| クラス | 統一後の要素追加メソッドと戻り値型 | 返却インスタンスの上書き可能な主な属性 |
| :--- | :--- | :--- |
| **`BoxList`** | `add(...) -> BoxListItem` | `show: bool`, `text: str`, `style: Style`, `text_style: Style` |
| **`BulletPoints`** | `add(...) -> BulletPointItem` | `show: bool`, `text: str`, `indent: int`, `text_style: Style \| None`, `custom_bullet_symbol: str \| None` |
| **`ChevronProcess`** | `add(...) -> ChevronItem` | `show: bool`, `text: str`, `description: str`, `style: Style`, `text_style: Style`, `description_style: Style` |
| **`Cycle`** | `add(...) -> CycleItem`<br>`set_center(...) -> CycleCenter` | `CycleItem`: `show`, `text`, `description`, `style`, `text_style`, `description_style`, `arrow_style`<br>`CycleCenter`: `show`, `text`, `description`, `radius`, `style`, `text_style`, `description_style` |
| **`GridLayout`** | `add(...) -> GridItem` | `show: bool`, `position: tuple[int, int]`, `width: int`, `height: int`, `r: float \| None`, `style: Style`, `text: str`, `text_style: Style`, `text_angle: float \| None`, `text_xy_shift: tuple[float, float] \| None` |
| **`Pyramid`** | `add(...) -> PyramidItem` | `show: bool`, `text: str`, `style: Style`, `text_style: Style`, `text_angle: float \| None`, `text_xy_shift: tuple[float, float] \| None` |
| **`TreeNode`** | `add(...) -> TreeNode` *(新規追加)* | `show: bool`, `text`, `text_style`, `line_style`, `children` 等（コンストラクタ生成も引き続き利用可能） |
| **`MindMapNode`** | `add(...) -> MindMapNode` *(新規追加)* | `show: bool`, `text`, `branch`, `shape`, `size`, `style`, `text_style`, `line_style`, `children` 等 |

> **重要実装ルール（遅延スタイル解決）**:
> 現在 `Pyramid.add()` や `GridLayout.add()` では、`add()` が呼ばれた時点で `text_angle` や `text_xy_shift` を `text_style.patch(...)` に焼き込んでいる。
> これだと後から `item.text_style = Styles.WhiteBold` や `item.text_angle = 30.0` と上書きした際に整合性が崩れるため、**属性はそのままアイテムに保持し、`draw()` 実行時に最終的な `Style` を合成する（遅延解決）** 方式に統一する。

---

### 4.2. 柱②：要素単位の表示切り替え (`show: bool = True`) とレイアウト保持

複数の要素を追加するすべてのコンポーネント（`smartarts`, `charts`, `diagrams`, `graph`）において、返却される要素インスタンスに **`show: bool = True`** 属性（および `add(..., show: bool = True)` 引数）を導入する。

#### 設計ルール：「レイアウト計算には含め、描画のみをスキップする」
- 要素を1つずつ出現させるアニメーションを作る際、`add()` 自体をループ内で増やすと、要素数に応じて1個あたりの幅やオートレイアウト座標が毎フレーム変動してしまい、画面がガタつく。
- そのため、`item.show = False` の要素であっても **全体のレイアウト計算（`ChevronProcess` の分割数、`BarChart` のグループ幅や軸スケール、`BaseGraph` のノード配置計算など）には通常通り参加させ、最終的なキャンバスへの描画命令のみをスキップする**。
- `TreeNode` や `MindMapNode`、`diagrams` / `graph` において親ノードや接続先ノードが `show = False` の場合、そのノードに接続するエッジ（親子線・矢印）も自動的に非表示とする。

---

### 4.3. 柱③：グラフ（`charts`）の軸の絶対値指定と要素別部分描画 (`draw_ratio` / `draw_direction`)

#### A. 軸の絶対値（`min_value` / `max_value`）指定の強化と自動スケール安定化
1. **明示的な軸の絶対値指定**:
   - `BarChart`, `LineChart`, `AreaChart`, `ScatterChart` の `configure_y_axis(min_value=..., max_value=...)` / `configure_x_axis(min_value=..., max_value=...)` に加え、`RadarChart` にも `configure_axis(min_value=..., max_value=..., levels=...)` メソッドを提供する（コンストラクタ引数での指定も引き続きサポート）。
2. **`show=False` や `draw_ratio < 1.0` 時における自動スケールの安定化**:
   - 万が一ユーザーが `min_value` / `max_value` を明示指定しなかった場合でも、軸の自動スケール計算は **全登録要素の元の100%データ値（`show=False` の系列も含む）** を基準に算出する。これにより、`draw_ratio` を `0.0 -> 1.0` に変化させている最中に目盛りが勝手に変動する現象を防ぐ。

#### B. 要素インスタンスの描画割合 (`draw_ratio`) と描画方向 (`draw_direction`)
- **命名の根拠 (`draw_ratio` vs `progress`)**:
  - `GanttChart` の `Task` クラスにはすでに業務データとしての「タスク完了率（0.0〜1.0）」を表す `task.progress` が存在するため、名前衝突を避け、かつ「時間軸ではなく空間的な描画制御である」ことを明確にするため **`draw_ratio`** および **`draw_direction`** を採用する。
- **共通属性仕様**:
  - `draw_ratio: float = 1.0`: `0.0`（非描画）〜 `1.0`（100%描画）の範囲で指定。`0.0` の場合は該当要素の図形描画をスキップする。
  - `draw_direction: DrawDirection`: `"bottom_to_top"`（下→上）または `"left_to_right"`（左→右）を指定可能（チャート種別ごとに最適なデフォルト値を持つ）。

| チャート種別 | 対象要素クラス | デフォルトの `draw_direction` | `"bottom_to_top"`（下→上）の挙動 | `"left_to_right"`（左→右）の挙動 |
| :--- | :--- | :---: | :--- | :--- |
| **`BarChart`** (垂直) | `Series` | `"bottom_to_top"` | 各バーの高さがベースライン（下）から上へ `draw_ratio` 倍に伸びる | 左のカテゴリから右へ向かって、`draw_ratio` の進行度に応じたバーが順次伸びる |
| **`BarChart`** (水平) | `Series` | `"left_to_right"` | 下のカテゴリから上へ向かって、`draw_ratio` の進行度に応じたバーが順次伸びる | 各バーの長さがベースライン（左）から右へ `draw_ratio` 倍に伸びる |
| **`LineChart`** | `Series` | `"left_to_right"` | 各データ点のY座標がベースライン（下）から上へ `draw_ratio` 倍に立ち上がる | 左端の点から右端の点へ向かって、折れ線が `draw_ratio` のX位置まで補間描画される |
| **`AreaChart`** | `Series` | `"left_to_right"` | 各データ点のY座標（および塗りつぶし領域）が下から上へ `draw_ratio` 倍に立ち上がる | 左端から右端へ向かって、折れ線と塗りつぶし領域が `draw_ratio` のX位置まで進行する |
| **`ScatterChart`** | `Series` | `"left_to_right"` | Y軸の下から上へ向かって、`draw_ratio` の範囲内にあるデータ点が描画される | X軸の左から右へ向かって、`draw_ratio` の範囲内にあるデータ点が描画される |
| **`PieChart`** | `Slice` | 扇形展開 | 中心から外周（半径方向）に向かって `draw_ratio` 倍の半径で描画 | 開始角度から時計回りに中心角を `draw_ratio` 倍だけ展開して描画（デフォルト） |
| **`RadarChart`** | `Series` | 放射展開 | 中心（`min_value`）から各頂点（外周）に向かって `draw_ratio` 倍の位置にポリゴンを展開 | 同左 |
| **`GanttChart`** | `Task` | `"left_to_right"` | ➖（水平バーのため `"left_to_right"` と同等） | タスクの `start`（左端）から `end`（右端）に向かってバーの長さを `draw_ratio` 倍だけ描画（内部の `task.progress` 完了率バーとも共存） |

---

### 4.4. 柱④：`draw()` における空間配置・サイズ・比例スケールの統一

#### A. 「リサイズ (`width`, `height`)」と「比例スケール (`scale`)」の明確な役割分担
1. **`width` / `height`（または `radius`）**:
   - コンポーネントが配置される**レイアウト領域（箱の寸法）**を変更する。
   - フォントサイズ（`text_size`）や線幅（`line_width`）は元の `Style` のまま維持される（アスペクト比の変更や領域調整に最適）。
2. **`scale: PosFloat = 1.0`**:
   - 基準座標 `xy` を起点として、**図形の寸法・余白・半径だけでなく、`Style` 内のフォントサイズ（`text_size`）、線幅（`line_width`）、角丸（`r`）、矢印ヘッドサイズ、アイコンサイズ等もすべて `scale` 倍に比例拡大・縮小**する。
   - これにより、動画でのズームイン／ズームアウトや、スライド・ドキュメント内での縮小サムネイル配置時に「小さな箱から大きな文字がハミ出る」問題を完全に防ぐことができる。

#### B. 共通スケーリング基盤の設計 (`_core`)
- `Style` や描画プリミティブを `scale` 倍に変換する内部ユーティリティ（またはキャンバスレベルのローカル座標変換・スケールコンテキスト）を用意する。
  - **アプローチ（Canvas Transform Context 方式 — 推奨）**:
    `canvas` に `with canvas.transform(origin=xy, scale=scale, translate=(dx, dy)):` のような内部コンテキストマネージャを導入する。
    コンテキスト内で呼ばれる `canvas.rectangle`, `canvas.line`, `canvas.text`, `canvas.image` 等に対して、座標 `(x, y)` のアフィン変換 $(x', y') = (x_0 + (x - x_0) \cdot s, y_0 + (y - y_0) \cdot s)$ と、サイズ (`width`, `height`, `radius`, `r`) および `Style` (`text_size`, `line_width`, `icon` サイズ) の `scale` 倍を透過的に適用する。
    - **メリット**: 個別の SmartArt / Chart / Diagram / Graph の複雑な内部描画ロジック（何十箇所もの `canvas_text` や `canvas_line`）を1箇所ずつ書き換える必要がなく、**全コンポーネントで完全に一貫したズーム・平行移動が最小のコード変更で実現できる**。

#### C. 各モジュールの `draw()` シグネチャ拡張一覧

1. **`drawlib.charts`**（後方互換性を100%維持しつつ `width`, `height` / `radius`, `scale` を追加）
   - `BarChart.draw(xy=(0.0, 0.0), *, width: PosFloat | None = None, height: PosFloat | None = None, scale: PosFloat = 1.0)`
   - `LineChart.draw(xy=(0.0, 0.0), *, width: PosFloat | None = None, height: PosFloat | None = None, scale: PosFloat = 1.0)`
   - `AreaChart.draw(xy=(0.0, 0.0), *, width: PosFloat | None = None, height: PosFloat | None = None, scale: PosFloat = 1.0)`
   - `ScatterChart.draw(xy=(0.0, 0.0), *, width: PosFloat | None = None, height: PosFloat | None = None, scale: PosFloat = 1.0)`
   - `PieChart.draw(xy=(0.0, 0.0), *, radius: PosFloat | None = None, width: PosFloat | None = None, height: PosFloat | None = None, scale: PosFloat = 1.0)`
   - `RadarChart.draw(xy=(0.0, 0.0), *, radius: PosFloat | None = None, width: PosFloat | None = None, height: PosFloat | None = None, scale: PosFloat = 1.0)`
   - `GanttChart.draw(xy=(0.0, 0.0), *, width: PosFloat | None = None, height: PosFloat | None = None, scale: PosFloat = 1.0)`
   - 各チャートの `draw_legend(..., scale: PosFloat = 1.0)`

2. **`drawlib.smartarts`**
   - 全 SmartArt の `draw(...)`（および `draw_flexible(...)`）にキーワード引数 `scale: PosFloat = 1.0` を追加。
   - `ChevronProcess`, `GridLayout`, `Pyramid`, `Table`, `BoxList`, `Cycle`, `TreeNode`, `MindMapNode`, `BulletPoints`, `SourceCode` すべてで `xy` を基準とした `scale` 拡大縮小をサポート。

3. **`drawlib.diagrams`**
   - `ArchitectureDiagram.draw(xy=(0.0, 0.0), *, scale: PosFloat = 1.0)`
   - `FlowDiagram.draw(xy=(0.0, 0.0), *, scale: PosFloat = 1.0)`
   - `SequenceDiagram.draw(xy=(0.0, 0.0), *, scale: PosFloat = 1.0)`
   - `StateDiagram.draw(xy=(0.0, 0.0), *, scale: PosFloat = 1.0)`
   - `ClassDiagram.draw(xy=(0.0, 0.0), *, scale: PosFloat = 1.0)`
   - `ERDiagram.draw(xy=(0.0, 0.0), *, scale: PosFloat = 1.0)`

4. **`drawlib.graph`**
   - `BaseGraph.draw(*, xy: Coordinate = (0.0, 0.0), width: PosFloat | None = None, height: PosFloat | None = None, margin: PosFloat = 10.0, scale: PosFloat = 1.0) -> GraphLayout`
   - `GraphLayout.draw(*, xy: Coordinate = (0.0, 0.0), scale: PosFloat = 1.0) -> None`

---

## 5. 段階的実装ロードマップ (Implementation Phases)

各モジュール（`smartarts` ➔ `charts` ➔ `diagrams` / `graph`）を1つずつ縦割りで実装し、**各フェーズの完了ごとに `drawlib.anim` を用いたアニメーションサンプルを作成・レンダリングして視覚確認（Visual Review）を行ってから次のモジュールへ進む**。

```text
[Step 1: smartarts] ──(anim サンプルで視覚確認)──► [Step 2: charts] ──(anim サンプルで視覚確認)──► [Step 3: diagrams & graph] ──(anim サンプルで視覚確認)──► [Step 4: Docs & Rules 統合]
```

### Step 1: `smartarts`（＋ 共通の Canvas `scale` 基盤）と `anim` サンプル検証
1. **Canvas スケーリング基盤の実装 (`_core/l4_canvas`)**
   - [x] `Canvas` に空間変換（基準点 `origin`、スケール倍率 `scale`、オフセット `translate`）を透過的に適用するコンテキストマネージャまたは変換レイヤを実装する。
   - [x] 図形 (`shapes`)、線 (`lines`)、テキスト (`text` の `text_size` やシフト量)、画像・アイコン (`images`) が `scale` 倍で正確にスケーリングされる単体テストを追加する。
2. **`smartarts` の改修**
   - [x] `BoxList`, `ChevronProcess`, `Cycle` の `append()` / `insert()` / `extend()` を廃止して `add()` に一本化し、`BulletPoints`, `GridLayout`, `Pyramid` とともに `add()` が要素インスタンスを返すように更新する。
   - [x] `TreeNode.add()` および `MindMapNode.add()` メソッドを追加する。
   - [x] 全 SmartArt の要素インスタンスに `show: bool = True` を追加し、全体レイアウトを維持したまま非表示化できるようにする。
   - [x] `Pyramid` や `GridLayout` 等のスタイル合成を `add()` 時から `draw()` 時に遅延させ、追加後の属性上書き（`item.style = ...`, `item.text_style = ...`, `item.text = ...`）が完全に反映されるようにする。
   - [x] 全 SmartArt の `draw()` / `draw_flexible()` に `scale: PosFloat = 1.0` を追加する。
   - [x] 既存の `tests/drawlib/smartarts/`・ドキュメント・ルール内の `.append()` 呼び出しを `.add()` に更新し、単体テストを追加する。
3. **`anim` サンプル作成と視覚確認 (Visual Check)**
   - [x] `ChevronProcess` や `BoxList`, `Pyramid` を使い、「`show` によるステップの順次出現」「`style` 上書きによるアクティブステップのハイライト遷移」「`xy` と `scale` による移動・拡大縮小」のアニメーションサンプルを作成・描画し、文字サイズやレイアウト崩れがないか視覚確認する。

### Step 2: `charts` の拡張と `anim` サンプル検証
1. **`charts` の改修**
   - [ ] 全7種のチャート要素（`Series`, `Slice`, `Task` 等）に `show: bool = True`、`draw_ratio: float = 1.0`、`draw_direction: DrawDirection` を追加する。
   - [ ] `BarChart`, `LineChart`, `AreaChart`, `ScatterChart`, `PieChart`, `RadarChart`, `GanttChart` の各レンダラーで `"bottom_to_top"`（下→上）および `"left_to_right"`（左→右）の部分描画ロジックを実装する。
   - [ ] 軸の絶対値指定（`min_value`, `max_value`）の整備と、`show=False` / `draw_ratio < 1.0` 時でも元データ基準で軸スケールを安定計算する仕組みを実装する。
   - [ ] 全チャートの `draw()` に `width`, `height`（または `radius`）, `scale` のオーバーライド引数を追加し、インスタンス自身のデフォルト寸法を破壊せずに一時的な描画サイズとして計算されるようにする。
   - [ ] `show`, `draw_ratio`, `draw_direction`, `scale` の単体テストを追加する。
2. **`anim` サンプル作成と視覚確認 (Visual Check)**
   - [ ] `BarChart`（下→上への伸長、左→右への順次出現）、`LineChart` / `AreaChart`（左→右への折れ線伸長）、`PieChart` / `RadarChart`（展開アニメーション）、およびチャート全体のズームイン／移動のアニメーションサンプルを作成・描画し、軸目盛りの安定性や補間描画の美しさを視覚確認する。

### Step 3: `diagrams` および `graph` の拡張と `anim` サンプル検証
1. **`diagrams` / `graph` の改修**
   - [ ] 全6種の `diagrams` および `graph` の要素（`Node`, `Edge`, `Cluster` 等）に `show: bool = True` を追加し、レイアウト（座標）を維持したまま個別表示・非表示を切り替えられるようにする（非表示ノードに接続するエッジの自動非表示を含む）。
   - [ ] 全6種の `diagrams` の `draw()` に `scale: PosFloat = 1.0` を追加する。
   - [ ] `graph`（`BaseGraph.draw()` および `GraphLayout.draw()`）に `xy: Coordinate = (0.0, 0.0)` と `scale: PosFloat = 1.0` を追加する。
   - [ ] ノードやエッジの `show` / `style` / `label` を書き換えながら再描画する単体テストを追加する。
2. **`anim` サンプル作成と視覚確認 (Visual Check)**
   - [ ] `ArchitectureDiagram`, `FlowDiagram`, `SequenceDiagram`, `BaseGraph` 等を使い、「オートレイアウトや全体配置を固定したままノードとエッジが順番に出現する」「処理フローに沿ってノードがハイライトされる」「図全体がズーム・移動する」アニメーションサンプルを作成・描画して視覚確認する。

### Step 4: ドキュメント・エージェントルール更新と全体ドッグフーディング
- [ ] `src/drawlib/_rules/`（`lib_smartarts.md`, `lib_charts.md`, `lib_diagrams.md`, `lib_graph.md`, `lib_anim.md`, `api.md`）に、統一された `add()`・`show`・`draw_ratio` / `draw_direction`・`draw(xy, width, height, scale)` の仕様を反映する。
- [ ] Step 1〜3 で検証したアニメーションサンプルを `docs_src/02_drawing_primitives/animation.md`（および各モジュールの解説ページ）に組み込み、`./dcli code-check all`・`./dcli test all`・`./dcli docs build --all` を実行して全体を完成させる。

