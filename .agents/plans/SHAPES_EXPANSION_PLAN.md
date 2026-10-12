# Drawlib Shapes 拡張計画書（既存図形の `hole_ratio` 中抜き統合 ＆ 全 `variant` 対応の13新規シェイプ）
(DRAWLIB SHAPES EXPANSION PLAN)

- **更新日**: 2026-10-12
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x` / `v0.4.x`)
- **対象モジュール**:
  - `src/drawlib/shapes.py` (公開ファサード：`donuts` 廃止、新規13シェイプの公開)
  - `src/drawlib/_core/l4_canvas/_shapes/_util.py` (凸多角形・円・楕円の中抜き `hole_ratio` 複合パス構築ユーティリティ)
  - `src/drawlib/_core/l4_canvas/_shapes/_basic.py` (基本図形への `hole_ratio` 追加、`face` の `variant` 統一＆4種追加、`forbidden`, `checkmark`, `shield`, `ribbon`, `funnel`, `pin`, `heart`, `sun`, `moon`, `clock` 実装)
  - `src/drawlib/_core/l4_canvas/_shapes/_polygon.py` (多角形への `hole_ratio` 追加、`lightning`, `explosion`, `tag`, `plaque` 実装)
  - `src/drawlib/_core/l4_canvas/_canvas.py`, `src/drawlib/_core/l4_canvas/__init__.py` (キャンバスメソッド公開)
  - `src/drawlib/_core/l2_types/` (各 `Variant` 型エイリアス・`Literal` 定義)
  - `src/drawlib/_rules/lib_shapes.md`, `src/drawlib/_rules/api.md`, `src/drawlib/_rules/overview.md` (AIエージェント向けルールの更新)
  - `docs/` (公式ドキュメント・クイックスタート・スライドデッキ内の `donuts` / `face` 移行および新規図形のドッグフーディング)
  - `tests/drawlib/_core/l4_canvas/` (単体テスト・バリデーションテスト)

---

## 1. エグゼクティブサマリー & 設計原則 (Executive Summary & Design Principles)

### 1.1. 背景と目的
PowerPoint や Google Slides の「基本図形」「星とリボン」パレットで頻出する図形や、技術プレゼン・アーキテクチャ比較スライドで多用される記号（禁止マーク・チェックマーク・盾・稲妻・爆発・リボン・タグ・漏斗・ブローチ・ピン・ハート・太陽・月・時計）を `drawlib.shapes` に拡充する。

これにあたり、以下の3つの設計原則を徹底する：

1. **既存図形の中抜きオプション統合（`hole_ratio: Ratio | None = None`）と `donuts` の廃止**:
   - 中抜き矩形（Frame）や中抜き三角（`△`）、ドーナツ（`◯`）を別関数として乱立させるのではなく、既存の `circle`, `ellipse`, `rectangle`, `triangle`, `rhombus`, `parallelogram`, `trapezoid`, `regularpolygon` に共通のキーワード引数 **`hole_ratio: Ratio | None = None`**（`0.0 < hole_ratio < 1.0`）を導入する。
   - 絶対値の `thickness` ではなく比率 `hole_ratio`（中心から外周までのうち何割を穴としてくり抜くか）とすることで、AI エージェントが細長い矩形や小さな三角形に対して内接円半径を超える太さを指定して破綻する事故を100%防ぎ、既存の `bump_ratio` / `depth_ratio` / `wave_ratio` とも命名規則を統一する。
   - これに伴い、既存の **`donuts` は廃止して `circle(..., hole_ratio=...)` に一本化**する。
2. **全シェイプへの複数 `variant` パターンの導入と `face` の `variant` 統一**:
   - 新規追加するすべてのシェイプ関数に 2〜6 種類の実用的な `variant` を用意し、名前空間の肥大化を防ぎつつスライド表現の引き出しを最大化する。あわせて既存の `face` の引数名も `mood` から `variant` に統一し、`"dizzy"`, `"dead"`, `"skull"`, `"devil"` を追加する。
3. **Center-Anchored (`is_default_center=True`) と複合パス（Compound `PathPatch`）の徹底**:
   - 新規追加する13シェイプはすべて中心座標 `xy=(cx, cy)` を基準とし、`style.halign` / `style.valign`、`style.angle`（中心回転）、`style.shape_r`（角丸）、および `text` / `text_style` 埋め込みに完全対応する。
   - 穴あき図形（`forbidden`, `checkmark(variant="solid_circle")`, `tag`, `pin`, `heart(variant="broken")` 等）はすべて反時計回り（CCW）の外周パスと時計回り（CW）の内周穴パスを `Path.make_compound_path` で合成した単一の `PathPatch` として描画し、半透明（`alpha < 1.0`）や枠線指定時にも内部に不要な交差線が出ない設計とする。

---

## 2. 実装フェーズ一覧

| フェーズ | 対象機能 / 関数名 | 配置先 | 内容・主な `variant` |
| :--- | :--- | :--- | :--- |
| **Phase 1: 既存図形の中抜き統合・名称統一・`face` 拡張** | `circle`, `ellipse`, `rectangle`, `triangle`, `rhombus`, `parallelogram`, `trapezoid`, `regularpolygon`, `face` | `_util.py`<br>`_basic.py`<br>`_polygon.py` | 共通引数 `hole_ratio: Ratio \| None = None` の追加。`donuts` の削除。`State` / `MindMapNode` の `"oval"` → `"ellipse"` 統一。`face` の `mood` → `variant` 統一＋`"dizzy"`, `"dead"`, `"skull"`, `"devil"` 追加。 |
| **Phase 2: 禁止・判定・ステータスマーク系** | **`forbidden`**<br>**`checkmark`** | `_basic.py` | ・`forbidden`: `"slash"`, `"backslash"`, `"cross"`, `"no_entry"`<br>・`checkmark`: `"standard"`, `"circle"`, `"solid_circle"` |
| **Phase 3: セキュリティ・強調・バナー・ラベル系** | **`shield`**<br>**`lightning`**<br>**`explosion`**<br>**`ribbon`**<br>**`tag`** | `_basic.py`<br>`_polygon.py` | ・`shield`: `"classic"`, `"flat"`, `"round"`<br>・`lightning`: `"standard"`, `"flat"`, `"double"`, `"flat_double"`, `"angled"`, `"slanted"` (+ `mirror`)<br>・`explosion`: `"standard"`, `"heavy"`, `"curved"`<br>・`ribbon`: `"down"`, `"up"`, `"flat"`<br>・`tag`: `"angled"`, `"chamfered"`, `"rounded"` (+ `mirror`, `hole_ratio`) |
| **Phase 4: 構造・メタファー・基本図形系** | **`funnel`**<br>**`plaque`**<br>**`pin`**<br>**`heart`**<br>**`sun`**<br>**`moon`**<br>**`clock`** | `_basic.py`<br>`_polygon.py` | ・`funnel`: `"standard"`, `"3d"`, `"curved"`<br>・`plaque`: `"concave"`, `"chamfered"`, `"notched"`<br>・`pin`: `"pointer"`, `"teardrop"`, `"badge"` (+ `hole_ratio`)<br>・`heart`: `"standard"`, `"broken"`<br>・`sun`: `"rays"`, `"ring"`, `"beams"`<br>・`moon`: `"crescent"`, `"thin"`, `"half"` (+ `mirror`)<br>・`clock`: `"standard"`, `"ticks"`, `"stopwatch"`, `"alarm"` (+ `hour`, `minute`) |

---

## 3. Phase 1 詳細仕様：既存図形への `hole_ratio` 導入と `donuts` の廃止

### 3.1. 対象関数とシグネチャ変更
以下の8関数にキーワード専用引数 `hole_ratio: Ratio | None = None` を追加する：
- `circle(xy, radius, *, hole_ratio=None, style, text="", text_style=None)`
- `ellipse(xy, width, height, *, hole_ratio=None, style, text="", text_style=None)`
- `regularpolygon(xy, num_vertex, radius, *, hole_ratio=None, style, text="", text_style=None)`
- `rectangle(xy, width, height, *, hole_ratio=None, style, text="", text_style=None)`
- `triangle(xy, width, height, topvertex_x=None, *, hole_ratio=None, style, text="", text_style=None)`
- `parallelogram(xy, width, height, corner_angle, *, hole_ratio=None, style, text="", text_style=None)`
- `trapezoid(xy, height, bottomedge_width, topedge_width, topedge_x=None, *, hole_ratio=None, style, text="", text_style=None)`
- `rhombus(xy, width, height, *, hole_ratio=None, style, text="", text_style=None)`

### 3.2. 中抜き幾何アルゴリズム
1. **円・楕円 (`circle`, `ellipse`)**:
   - `hole_ratio is None` のときは従来通り `Circle` / `Ellipse` パッチを描画。
   - `0.0 < hole_ratio < 1.0` のときは、外周楕円（半径 $a = W/2, b = H/2$、反時計回り CCW 4セグメント3次ベジェ）と内周穴楕円（半径 $a_{\text{in}} = a \cdot \text{hole\_ratio}, b_{\text{in}} = b \cdot \text{hole\_ratio}$、時計回り CW 4セグメント3次ベジェ）を `Path.make_compound_path` で結合した `PathPatch` を生成する。
2. **凸多角形 (`rectangle`, `triangle`, `rhombus`, `parallelogram`, `trapezoid`, `regularpolygon`)**:
   - 各辺の法線ベクトル（内側向き）に沿って一定距離 $t$ だけオフセットした内周ポリゴンを求める。
   - 多角形の内接円半径（または重心から各辺への垂線距離の最小値 $d_{\min}$）に対し、枠の太さを $t = (1.0 - \text{hole\_ratio}) \cdot d_{\min}$ と定義することで、任意の `0.0 < hole_ratio < 1.0` で内周ポリゴンが自己交差せず常に均一な肉厚 $t$ のフレーム（中抜き図形）となる。
   - `style.shape_r` が指定されている場合は、外周ポリゴン（CCW）と内周ポリゴン（CW、角丸半径 $\max(0, r - t \cdot 0.5)$）の双方に `ShapeUtil.round_polygon_points` を適用してから複合パス化する。

### 3.3. `donuts` の廃止と移行対象
- `src/drawlib/shapes.py`, `src/drawlib/_core/l4_canvas/_shapes/_basic.py`, `src/drawlib/_core/l4_canvas/_canvas.py`, `src/drawlib/_core/l4_canvas/__init__.py` から `donuts` を削除する。
- 既存の `donuts(xy, radius=R, width=W)` 呼び出し箇所（`tests/drawlib/_core/l4_canvas/test_patches.py`, `docs/docs_src/01_getting_started/core_concepts.md`, `docs/docs_src/02_drawing_primitives/shapes_basic.md`, `docs/quickstart_src/04-shapes_and_lines.md`, `docs/drawlib-dogfooding-en_src/07_basic_drawing.md`, `docs/slide_about_drawlib_src/02_core_and_primitives/04_shapes_catalog.md`）を `circle(xy, radius=R, hole_ratio=...)` に移行する。

### 3.4. `State` および `MindMapNode` における `"oval"` → `"ellipse"` の名称統一
`drawlib.shapes.ellipse` との命名の一貫性を保つため、内部で `ellipse()` を呼び出している以下2箇所の `shape="oval"` 指定を **`"ellipse"`** に統一する：
- **`drawlib.diagrams.state` (`src/drawlib/_diagrams/state/_types.py`, `_state_node.py`, `_render_node.py`, `_render_transition.py`)**:
  - `State(..., shape="ellipse")` に変更（テスト・ドキュメント・`src/drawlib/_rules/lib_diagrams.md` を更新）。
- **`drawlib.smartarts.MindMapNode` (`src/drawlib/_smartarts/_mindmap.py`)**:
  - `shape: Literal["rectangle", "ellipse", "none"]` に変更（テスト・ドキュメント・`src/drawlib/_rules/lib_smartarts.md` を更新）。

### 3.5. `face` の引数名を `mood` → `variant` に統一 ＆ 新規4種（`"dizzy"`, `"dead"`, `"skull"`, `"devil"`）の追加
AI エージェントの引数名ハルシネーションを防ぐため、既存の `face` のキーワード引数を `mood` から他シェイプと共通の **`variant: FaceVariant = "smile"`** に変更し、障害・クラッシュ・セキュリティ攻撃者の表現に使える4種類のバリエーションを追加する：
- **既存5種**: `"smile"`, `"neutral"`, `"sad"`, `"angry"`, `"surprised"`
- **新規4種**:
  - **`"dizzy"`**: 目がバッテン（`×` `×`）＋波線の口（目が回る・過負荷・混乱状態）。
  - **`"dead"`**: 目がバッテン（`×` `×`）＋丸く開いた口（ノックアウト・応答不能・ダウン状態）。
  - **`"skull"`**: 頭蓋骨シルエット＋大きな両目穴＋三角鼻腔＋歯の縦線（致命的障害・死活監視NG・危険）。
  - **`"devil"`**: 内向きに反った2本の悪魔の角が一体化した頭部シルエット＋鋭い吊り眉＋不敵な笑み（アタッカー・悪意あるリクエスト・脅威アクター）。

---

## 4. Phase 2〜4 詳細仕様：新規12シェイプ関数

### 4.1. `forbidden`（禁止・進入禁止・遮断マーク）
```python
ForbiddenVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["slash", "standard", "backslash", "cross", "no_entry", "minus"],
]

@validate_call
def forbidden(
    self,
    xy: Coordinate,
    radius: PosFloat,
    *,
    variant: ForbiddenVariant = "slash",
    thickness_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"slash"` (`"standard"`): 丸枠＋左上から右下（`135° -> -45°`）の斜線（外周CCW円＋2つのD字型CW穴によるシームレスな単一複合パス）。
  - `"backslash"`: 丸枠＋左下から右上（`45° -> -135°`）の逆斜線。
  - `"cross"`: 丸枠＋十字バツ印（外周CCW円＋上下左右4つの扇形CW穴による単一複合パス）。
  - `"no_entry"` (`"minus"`): 塗りつぶし円＋中央の角丸水平バー抜き（外周CCW円＋中央CW角丸矩形穴）。
- **`thickness_ratio`**: `radius` に対するリング・斜線の太さ比率（デフォルト `0.22`）。

---

### 4.2. `checkmark`（チェックマーク・合格／完了記号）
```python
CheckmarkVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["standard", "check", "circle", "solid_circle"],
]

@validate_call
def checkmark(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat | None = None,
    *,
    variant: CheckmarkVariant = "standard",
    thickness_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"standard"` (`"check"`): 単体のレ点ポリゴン（`style.shape_r` で角丸調整可能）。
  - `"circle"`: 外周リング枠（CCW外円＋CW内円）＋中央のレ点（CCWポリゴン）。
  - `"solid_circle"`: 塗りつぶし円（CCW外円）＋中央を白抜きにしたレ点（CWポリゴン）。`forbidden(variant="no_entry")` と対になるバッジ表現。
- **`thickness_ratio`**: `min(width, height)` に対する線の太さ比率（デフォルト `0.24`）。

---

### 4.3. `shield`（セキュリティ・防衛・認証の盾）
```python
ShieldVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["classic", "standard", "crown", "flat", "heater", "round", "arch"],
]

@validate_call
def shield(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: ShieldVariant = "classic",
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"classic"` (`"standard"`, `"crown"`): 上辺中央と両肩が盛り上がった王冠カーブ＋下部へ収束する3次ベジェ曲線シールド。
  - `"flat"` (`"heater"`): 上辺が水平直線で、下部が3次ベジェ曲線で尖るヒーターシールド。
  - `"round"` (`"arch"`): 上辺が滑らかなドーム型アーチを描くバッジシールド。

---

### 4.4. `lightning`（稲妻・スパイク・トリガー）
```python
LightningVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal[
        "standard", "sharp",
        "flat", "flat_top",
        "double", "sharp_double",
        "flat_double",
        "angled",
        "slanted", "dynamic",
    ],
]

@validate_call
def lightning(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: LightningVariant = "standard",
    mirror: bool = False,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"standard"` (`"sharp"`): 1段ステップ・上部尖り・下部尖り（6頂点）。
  - `"flat"` (`"flat_top"`): 1段ステップ・上辺が水平フラット・下部尖り（7頂点）。
  - `"double"` (`"sharp_double"`): 2段ジグザグ・上部尖り・下部尖り（10頂点）。
  - `"flat_double"`: 2段ジグザグ・上辺が水平フラット・下部尖り（11頂点）。
  - `"angled"`: 1段の斜め落ちステップ・上部尖り（6頂点）。
  - `"slanted"` (`"dynamic"`): 1段の跳ね上がりステップ・上部尖り（6頂点）。
- **`mirror`**: `True` のとき左右反転。`style.shape_r` による頂点角丸にも対応。

---

### 4.5. `explosion`（爆発・クラッシュ・衝撃波バースト）
```python
ExplosionVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["standard", "irregular", "heavy", "wild", "curved", "comic"],
]

@validate_call
def explosion(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: ExplosionVariant = "standard",
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"standard"` (`"irregular"`): 非対称な大小10〜12本のスパイクを持つ PowerPoint「爆発1」相当のシルエット。
  - `"heavy"` (`"wild"`): より細かく鋭い16本の非対称スパイクが飛び散る PowerPoint「爆発2」相当の激しい爆発シルエット。
  - `"curved"` (`"comic"`): スパイク間の谷が内側に反った円弧（コンケーブアーク）で結ばれたマンガ・衝撃エフェクト風バースト。

---

### 4.6. `ribbon`（リボン・横断幕・バナー）
```python
RibbonVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["down", "standard", "up", "flat", "banner"],
]

@validate_call
def ribbon(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: RibbonVariant = "down",
    tail_width_ratio: Ratio | None = None,
    drop_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"down"` (`"standard"`): 中央の前面パネルに対し、左右の両端リボンテールが下側に段差をつけて折れ下がる3Dリボン（テール面・折り返し影面を `style.shape_fill_color` から自動明度シェーディング）。
  - `"up"`: 左右の両端リボンテールが上側に段差をつけて折れ上がる3Dリボン。
  - `"flat"` (`"banner"`): 段差のない1枚ものの両端Vノッチ入りバナーテープ。
- `text` は中央の前面パネルの重心に自動配置する。

---

### 4.7. `tag`（穴あきラベルタグ・荷札バッジ）
```python
TagVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["angled", "standard", "chamfered", "beveled", "rounded"],
]

@validate_call
def tag(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: TagVariant = "angled",
    mirror: bool = False,
    hole_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"angled"` (`"standard"`): 先端が三角形（`>`）に尖った五角形タグ＋先端寄りの透過丸穴。
  - `"chamfered"` (`"beveled"`): 先端の上下角を斜めに切り落とした六角形荷札タグ＋透過丸穴。
  - `"rounded"`: 先端が滑らかな半円ドーム状に丸まったタグ＋透過丸穴。
- **`mirror`**: `chevron` と同様、`True` のとき左右の向きを反転。任意の角度への回転とテキスト角度の独立制御は `style.angle` および `text_style.angle` で行う。
- **`hole_ratio`**: 短辺に対する丸穴の直径比率（デフォルト `0.24`）。`text` は穴を避けたボディ中央に自動オフセット配置する（`style.angle` 回転時もオフセット位置を回転追従させる）。

---

### 4.8. `funnel`（ファネル・漏斗）
```python
FunnelVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["standard", "flat", "3d", "cylinder", "curved"],
]

@validate_call
def funnel(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: FunnelVariant = "standard",
    neck_width_ratio: Ratio | None = None,
    neck_height_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"standard"` (`"flat"`): 上部の逆台形コーンと下部の直管スパウトからなる2Dフラット漏斗（`style.shape_r` 対応）。
  - `"3d"` (`"cylinder"`): `cylinder` と同じ自動明度計算により、上部の円形開口部を立体的な明色楕円キャップとして描画する3D漏斗。
  - `"curved"`: 上端から下部の直管スパウトへ滑らかなS字3次ベジェ曲線で絞り込まれる漏斗。

---

### 4.9. `plaque`（飾り枠・四隅カットプレート）
```python
PlaqueVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["concave", "standard", "chamfered", "octagon", "notched"],
]

@validate_call
def plaque(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: PlaqueVariant = "concave",
    cut_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"concave"` (`"standard"`): 四隅が内側に1/4円弧で丸く欠けた PowerPoint「ブローチ（Plaque）」形状。
  - `"chamfered"` (`"octagon"`): 四隅を45度斜めに切り落とした八角形プレート。
  - `"notched"`: 四隅を直角（正方形）に切り欠いたクロスコーナープレート。
- **`cut_ratio`**: `min(width, height)` に対する四隅の切り欠きサイズ比率（デフォルト `0.22`）。

---

### 4.10. `pin`（番号ポインタバッジ・マップピン・ティアドロップ）
```python
PinVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["pointer", "standard", "teardrop", "drop", "pin", "badge"],
]

@validate_call
def pin(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: PinVariant = "pointer",
    hole_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"pointer"` (`"standard"`): 真円のディスク外周から鋭い二等辺三角形のポインタ棘が突き出た、ステップ番号（`"1"`, `"2"`）や注釈コールアウトに最適なポインタバッジ。
  - `"teardrop"` (`"drop"`, `"pin"`): 円形ヘッドから先端へ接線で滑らかにつながるティアドロップ・マップピン形状（PowerPoint 基本図形の「涙型」）。
  - `"badge"`: 角丸四角形のボディから三角形のポインタ棘が突き出た、2文字以上のラベル（`"A1"`, `"Step 1"`）も収まりやすいUIマーカーピン。
- **回転とテキスト角度（`style.angle` & `text_style.angle`）**:
  - `direction` 引数は設けず、既存の全シェイプと同様に `style.angle` で任意の角度（上下左右だけでなく斜め45度等も可）に回転させる。
  - `text_style=Styles.Text.patch(angle=0)` を指定すれば、ピンをどの角度に回転させても中の番号・テキストを正立（`0°`）に保つことができる（[`ShapeUtil.get_shape_text`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_core/l4_canvas/_shapes/_util.py#L402-L446) の標準仕様）。
- **`hole_ratio`**: デフォルト `None`（穴なしソリッド：中に番号やテキストをそのまま配置可能）。`hole_ratio=0.4` 等を指定すると、ヘッド中央に透過丸穴が空いた地図ピン（`📍`）になる。
- **テキスト配置の自動補正**: `text` が指定された場合、棘を含めたバウンディングボックス中心ではなく、**`style.angle` に応じて回転変換された円形ヘッド（または角丸矩形ボディ）の幾何中心 `(head_cx, head_cy)` に自動センタリング**する。

---

### 4.11. `heart`（ハート・健全性／好感度シンボル）
```python
HeartVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["standard", "classic", "broken"],
]

@validate_call
def heart(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: HeartVariant = "standard",
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```
- **`variant`**:
  - `"standard"` (`"classic"`): 左右対称の滑らかな3次ベジェ曲線で描かれるハート形状（`❤️`）。
  - `"broken"`: 中央にジグザグの透過亀裂（CWパス）が走るブロークンハート形状（`💔`、ヘルスチェック異常・離脱・障害の視覚化に対応）。

---

### 4.12. `sun` ＆ `moon`（太陽・三日月：Light/Dark・昼夜・時差シンボル）
```python
SunVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["rays", "standard", "ring", "beams"],
]

MoonVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["crescent", "standard", "thin", "waxing", "half"],
]

@validate_call
def sun(
    self,
    xy: Coordinate,
    radius: PosFloat,
    *,
    variant: SunVariant = "rays",
    num_rays: PosInt = 8,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...

@validate_call
def moon(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: MoonVariant = "crescent",
    mirror: bool = False,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **`sun` の `variant`**:
  - `"rays"` (`"standard"`): 中央の円盤＋周囲に `num_rays` 個（デフォルト8個）の離れた二等辺三角形コロナを配した PowerPoint 基本図形の太陽。
  - `"ring"`: 中央が中抜きリングになった太陽＋周囲の三角形コロナ。
  - `"beams"`: 中央の円盤＋周囲に放射状のバー（矩形光線）を配した太陽。
- **`moon` の `variant`**:
  - `"crescent"` (`"standard"`): 標準の三日月（太さ比率 `0.46` 相当）。
  - `"thin"` (`"waxing"`): 繊細で細い三日月（太さ比率 `0.28` 相当）。
  - `"half"`: 半月（D字型、太さ比率 `1.0` 相当）。
  - `mirror=True` で左右の向きを反転可能。

---

### 4.13. `clock`（時計・ストップウォッチ・アラーム・7セグデジタル時計：時刻指定対応）
```python
ClockVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["standard", "ticks", "dial", "stopwatch", "timer", "alarm", "digital"],
]

@validate_call
def clock(
    self,
    xy: Coordinate,
    radius: PosFloat,
    *,
    variant: ClockVariant = "standard",
    hour: float = 10.0,
    minute: float = 10.0,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **静的アイコンに対する優位性**: Phosphor 等の時計アイコンは針の角度が固定されているため、障害タイムライン（`09:00` → `09:30` → `10:00`）の推移や `drawlib.anim` での時刻進行アニメーションを表現できない。`shapes.clock` では `hour` と `minute` からアナログ針または7セグデジタル表示を自動描画する。
- **`variant`**:
  - `"standard"`: 円形文字盤＋中心ピボット＋短針・長針（小サイズでも視認性が高いシンプル構成）。
  - `"ticks"` (`"dial"`): 12時間の目盛り線付き文字盤＋短針・長針。
  - `"stopwatch"` (`"timer"`): 上部リューズボタン＋斜めサイドボタン＋12時間目盛り付き（レイテンシ・SLA・タイムアウト計測表現）。
  - `"alarm"`: 上部左右のツインベル＋下部脚付きの目覚まし時計（アラート発火・PagerDuty・Cron定時バッチ表現）。
  - **`"digital"`**: **フォントを一切使わず純粋な7セグメント六角ポリゴン（`PathPatch`）で点灯セグメントのみ `HH:MM` を描くデジタル時計**。外部フォント依存ゼロ・DPIやサイズに依存する文字はみ出しゼロで、くっきり視認性の高い7セグデジタル表示を描画する。
- **`hour` / `minute`**: デフォルトは `hour=10.0, minute=10.0`（10時10分）。アナログ時は短針・長針角度、`"digital"` 時は24時間表記 `00:00`〜`23:59` の7セグ点灯パターンに変換する（`style.angle` 回転対応）。

---

## 5. 検証・ドッグフーディング手順 (Verification Workflow)

1. **単体テスト (`tests/drawlib/_core/l4_canvas/`)**:
   - Phase 1 の `hole_ratio`（8図形すべて＋`shape_r` 併用＋境界値バリデーション）、`face` の `variant` 統一＆新規4種、および Phase 2〜4 の新規13図形（全 `variant`・回転 `angle`・アライメント・テキスト埋め込み・異常値検証）の単体テストを作成し、`./dcli test all` をパスさせる。
2. **静的解析 (`./dcli code-check all`)**:
   - Ruff lint/format（循環的複雑度 `C901 <= 10` 遵守）、Ty 型チェック、`@validate_call` docstring チェック（内部型エイリアス名を docstring に露出させない）を完全パスさせる。
3. **ルール＆ドキュメント更新・視覚確認**:
   - `src/drawlib/_rules/api.md`, `src/drawlib/_rules/lib_shapes.md`, `src/drawlib/_rules/overview.md`、および `docs/` 内のドキュメント・スライドを更新し、`./dcli docs build --all` と `view_file` でレンダリング結果を視覚確認する。
