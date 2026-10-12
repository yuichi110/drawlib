# Drawlib Shapes 拡張計画書 (`gear`, `math_symbol`, `cloud`, `cube`, `brace`, `document` ほか)
(DRAWLIB SHAPES EXPANSION PLAN)

- **作成日**: 2026-10-12
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x` / `v0.4.x`)
- **対象モジュール**:
  - `src/drawlib/shapes.py` (公開ファサード)
  - `src/drawlib/_core/l4_canvas/_shapes/_polygon.py` (多角形・パス系プリミティブ実装)
  - `src/drawlib/_core/l4_canvas/_shapes/_basic.py` (曲線・3Dシェーディング系プリミティブ実装)
  - `src/drawlib/_core/l4_canvas/_canvas.py`, `src/drawlib/_core/l4_canvas/__init__.py` (キャンバスメソッド公開)
  - `src/drawlib/_core/l2_types/` (型エイリアス・Literal定義)
  - `src/drawlib/_rules/lib_shapes.md`, `src/drawlib/_rules/api.md` (AIエージェント向けルールの更新)
  - `docs/docs_src/02_drawing_primitives/` (公式ドキュメント・ドッグフーディング図版)
  - `tests/drawlib/_core/l4_canvas/` (単体テスト・バリデーションテスト)

---

## 1. エグゼクティブサマリー & 設計原則 (Executive Summary & Design Principles)

### 1.1. なぜ `drawlib.shapes` の拡充が必要か
`drawlib` の図解では、高レベルな構造化コンポーネント（`smartarts`, `diagrams`, `graph`）と並び、スライドやアーキテクチャ図の表現力を支える基本図形プリミティブ（`drawlib.shapes`）が重要な役割を担っている。
しかし、従来の24種のプリミティブだけでは以下の課題があった：

1. **「概念の掛け算・足し算（Visual Equation）」における演算子図形の不足**:
   - スライドや概要図で頻出する `[要素A] + [要素B] = [成果C]` や `[要因A] × [要因B] = [事象C]` を `text("+")` で描くと、線が細く、枠線や塗りつぶし・角丸（`style.shape_r`）を持てないため、カード図形との視覚的バランスが崩れやすい。
2. **ベジェ曲線や複合パスを要する定番図形の手書きコスト**:
   - 歯車（`gear`）、雲（`cloud`）、中括弧（`brace`）、波底の書類（`document`）、3Dボックス（`cube`）などは、AIエージェントやユーザーが `shape(path_points=...)` でベジェ制御点を手計算して描くのが困難であり、プリミティブ関数として標準提供することで描画品質と再現性が劇的に向上する。
3. **アイコン（`drawlib.icons`）との明確な役割分担**:
   - `icons` は固定アスペクト比の小さなシンボル配置に適しているのに対し、`shapes` は **「任意の `width`/`height` や比率への変形」「`Style` による塗り・枠線・破線・角丸（`shape_r`）・回転（`angle`）の統一制御」「図形内部へのテキスト（`text`）埋め込み」** が可能である点に独自の価値がある。

### 1.2. 共通アーキテクチャ原則
1. **Center-Anchored (`is_default_center=True`) の徹底**:
   - 新規追加する図形は原則として `xy=(cx, cy)` を中心座標とし、`style.halign` / `style.valign` によるアライメント変更および `style.angle` による中心回転に完全対応する。
2. **名前空間の肥大化防止（関連図形のパラメータ集約）**:
   - 既存の `face(..., mood="smile")` や `cylinder(..., disks=3)` と同様、バリエーションは別関数に分割せず `math_symbol(..., symbol="+")` のように引数で切り替える設計とする。
3. **複合パス（Compound `PathPatch`）と自動シェーディングの活用**:
   - 穴あき図形（`gear` 等）や複数パーツ図形（`math_symbol` の `=`, `÷`, `!=` 等）は Matplotlib の `Path`（または `Path.make_compound_path`）を用いて単一の `PathPatch` として描画し、背景透過・枠線・角丸（`shape_r`）を一貫して適用する。

---

## 2. 追加候補一覧と優先度ロードマップ

| フェーズ / 優先度 | 関数名 | 分類・配置先 | 主な用途・特徴 | ステータス |
| :--- | :--- | :--- | :--- | :---: |
| **完了** | **`gear`** | `_polygon.py` | 歯車・ワーカー・自動化エンジン（1ピッチ比率、中心透過穴、円弧＆角丸対応） | **実装済** |
| **完了 (Phase 1)** | **`math_symbol`** | `_polygon.py` | スライド・概念図の数式演算子ブロック（`+`, `-`, `×`, `÷`, `=`, `≠`） | **実装済** |
| **Phase 2 (Tier 1)** | **`cloud`** | `_basic.py` | クラウド境界・インターネット・思考バブル（破線・任意縦横比・内部テキスト対応） | 計画中 |
| **Phase 2 (Tier 1)** | **`cube`** | `_basic.py` | 3D直方体・コンテナ・ノード・ブロック（`cylinder` の相棒、3面自動明度シェーディング） | 計画中 |
| **Phase 2 (Tier 1)** | **`brace`** | `_basic.py` | 複数要素を束ねるカーリーブレース／中括弧 `{` `}`（上下左右4方向・スパイン位置調整） | 計画中 |
| **Phase 2 (Tier 1)** | **`document`** | `_basic.py` | フローチャートの波底ドキュメント記号（`stacked: int = 1` で複数書類の重ね合わせに対応） | 計画中 |
| **Phase 3 (Tier 2)** | **`shield`** | `_polygon.py` | セキュリティ・WAF・認証（IAM/Auth）・ガードレールの盾型プリミティブ | 検討候補 |
| **Phase 3 (Tier 2)** | **`hexagon`** | `_polygon.py` | `width`, `height` を自由指定できる横長六角形（フローチャート準備記号・サービスバッジ） | 検討候補 |
| **Phase 3 (Tier 2)** | **`tag`** | `_polygon.py` | 片側が切り欠かれ丸穴が空いたラベル／タグ形状（バージョン表記・メタデータバッジ） | 検討候補 |

---

## 3. 各図形の詳細設計仕様

### 3.1. `gear`（歯車）— 【実装完了】
- **シグネチャ**:
  ```python
  def gear(
      xy: Coordinate,
      num_teeth: NumVertex,
      radius_ext: PosFloat,
      radius_int: PosFloat,
      *,
      tooth_ext_ratio: Ratio | None = None,  # デフォルト 0.35
      tooth_int_ratio: Ratio | None = None,  # デフォルト 0.55
      hole_radius: PosFloat | None = None,   # デフォルト None (穴なし)
      style: Style,
      text: str = "",
      text_style: Style | None = None,
  ) -> None:
  ```
- **幾何仕様**:
  - 1ピッチ角 $\Delta\theta = 360^\circ / \text{num\_teeth}$ に対する比率で歯先・歯元の角度幅を決定。
  - `style.shape_r` 未指定時は歯先・谷を正確な3次ベジェ円弧で結び、`shape_r` 指定時は $4N$ 頂点ポリゴンとして角丸化。
  - `hole_radius` 指定時は時計回り（CW）の円パスを `Path.make_compound_path` で合成し、中心を透過くり抜き。

---

### 3.2. `math_symbol`（数式・演算子記号ブロック）— 【実装完了】

スライドの「概念の足し算・掛け算（`A + B = C`, `A × B = C`）」や図解の視覚的オペレーターとして使える、塗り・枠線・角丸（`style.shape_r`）対応の演算子図形。

#### 3.2.1. シグネチャ & 型定義
- **サポートする記号（`MathSymbol` 型エイリアス in `l2_types`）**:
  - 加算（Plus）: `"+"`
  - 減算（Minus）: `"-"`, `"−"`
  - 乗算（Multiply）: `"*"`, `"x"`, `"×"`
  - 除算（Divide）: `"/"`, `"÷"`
  - 等号（Equal）: `"="`
  - 不等号（Not Equal）: `"!="`, `"≠"`

```python
MathSymbol = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["+", "-", "−", "*", "x", "×", "/", "÷", "=", "!=", "≠"],
]

@validate_call
def math_symbol(
    self,
    xy: Coordinate,
    symbol: MathSymbol,
    width: PosFloat,
    height: PosFloat | None = None,
    *,
    thickness_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```

#### 3.2.2. パラメーター仕様
| 引数名 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 中心座標 `(cx, cy)`（Center-Anchored）。 |
| `symbol` | `MathSymbol` | *必須* | 描画する演算子記号（`"+"`, `"-"`, `"*"`/`"x"`/`"×"`, `"/"`/`"÷"`, `"="`, `"!="`/`"≠"`）。 |
| `width` | `PosFloat` | *必須* | 図形全体の横幅（`> 0`）。 |
| `height` | `PosFloat \| None` | `None` | 図形全体の縦幅（`None` の場合は `width` と同値の正方形バウンディングボックス）。 |
| `thickness_ratio` | `Ratio \| None` | `None` | `min(width, height)` に対するバー（線）の太さの比率。`None` 時は `0.28`（`0.0 < thickness_ratio < 1.0`）。 |
| `style` | `Style` | *必須* | 塗り・枠線・回転角（`angle`）・角丸（`shape_r`）スタイル。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | 中央に配置するテキストとテキストスタイル。 |

#### 3.2.3. 各記号の幾何構築ロジック
基準サイズを $W = \text{width}$, $H = \text{height} \text{ (or } W\text{)}$, バーの太さを $t = \text{thickness\_ratio} \times \min(W, H)$, 半幅を $h_w = W/2$, $h_h = H/2$, $h_t = t/2$ とする。すべてのパーツはローカル中心 `(0, 0)` で生成し、`style.angle` 回転と `ShapeUtil.round_polygon_points(..., style.shape_r)` を適用した上で、複数パーツの場合は `Path.make_compound_path` で単一の `PathPatch` に統合する：

1. **`"+"` (Plus)**:
   - 水平バーと垂直バーが中央で交差する **12頂点の単一閉ポリゴン**（内部に余計な交差線が出ないシームレスな十字パス）：
     `[(h_t, h_t), (h_t, h_h), (-h_t, h_h), (-h_t, h_t), (-h_w, h_t), (-h_w, -h_t), (-h_t, -h_t), (-h_t, -h_h), (h_t, -h_h), (h_t, -h_t), (h_w, -h_t), (h_w, h_t)]`
2. **`"-"` / `"−"` (Minus)**:
   - 中央の水平バー **4頂点ポリゴン**：
     `[(-h_w, -h_t), (-h_w, h_t), (h_w, h_t), (h_w, -h_t)]`
3. **`"*"` / `"x"` / `"×"` (Multiply)**:
   - 正方形基準の十字ポリゴンを **45度回転** し、外接バウンディングボックスが $(W, H)$ 内に綺麗に収まるようスケール調整した **12頂点閉ポリゴン**（内部に交差線が出ない）。
4. **`"="` (Equal)**:
   - 上下2本の平行な水平バー（各4頂点ポリゴン $\times 2$ を `Path.make_compound_path` で結合）。
   - バーの中心Y座標は $\pm y_{\text{offset}}$（デフォルトでバー間の隙間が $t$ 程度になる位置、例: $y_{\text{offset}} = \min(h_h - h_t, 0.95 \cdot t)$）。
5. **`"/"` / `"÷"` (Divide)**:
   - 中央の水平バー（4頂点ポリゴン、それぞれ `shape_r` 対応）＋ 上下の円形ドット2個（中心 `(0, +y_dot)`, `(0, -y_dot)`、半径 $r_{\text{dot}} \approx 0.6 \cdot t$ のベジェ円パス）を `Path.make_compound_path` で単一 `PathPatch` に結合。
6. **`"!="` / `"≠"` (Not Equal)**:
   - `"="` の上下2本の水平バーと、斜めに貫くスラッシュバーを単一の複合輪郭（またはシームレスな結合パス）として構築。

---

### 3.3. `cloud`（クラウド / 雲形）— 【Phase 2】
- **シグネチャ案**:
  ```python
  def cloud(
      xy: Coordinate,
      width: PosFloat,
      height: PosFloat,
      *,
      style: Style,
      text: str = "",
      text_style: Style | None = None,
  ) -> None:
  ```
- **設計ポイント**:
  - 正規化された `[-0.5, 0.5] × [-0.5, 0.5]` 空間でバランス良く配置された複数の3次ベジェ曲線（モコモコした6〜8個のバンプ）を `(width, height)` にスケーリング＆ `style.angle` 回転して単一の閉じた `PathPatch` として描画。
  - 塗りつぶしだけでなく、`Styles.PrimaryDashed` 等による「クラウド境界枠（VPC / Internet 境界）」としても美しく見える外周シルエットにする。

---

### 3.4. `cube`（3Dキューブ / 直方体）— 【Phase 2】
- **シグネチャ案**:
  ```python
  def cube(
      xy: Coordinate,
      width: PosFloat,
      height: PosFloat,
      *,
      depth_ratio: Ratio = 0.28,
      depth_angle: Angle90 = 35.0,
      style: Style,
      text: str = "",
      text_style: Style | None = None,
  ) -> None:
  ```
- **設計ポイント**:
  - 既存の [`cylinder`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_core/l4_canvas/_shapes/_basic.py#L672-L887) と同じ思想で、`style.shape_fill_color` から **前面（ベース色）・上面（+25% 明度）・右側面（-18% 暗度）** を自動算出。
  - `text` は前面（フロントフェイス）の中央に自動配置することで、立体感を損なわずにラベルを表示できる。

---

### 3.5. `brace`（中括弧 `{` `}`）— 【Phase 2】
- **シグネチャ案**:
  ```python
  def brace(
      xy: Coordinate,
      width: PosFloat,
      height: PosFloat,
      *,
      direction: Literal["right", "left", "up", "down"] = "right",
      tip_ratio: Ratio = 0.5,
      style: Style,
      text: str = "",
      text_style: Style | None = None,
  ) -> None:
  ```
- **設計ポイント**:
  - `direction` でティップ（尖った中央の突起）が向く方向を指定し、`tip_ratio`（デフォルト `0.5`）で突起の位置を非対称にもずらせる設計。
  - 滑らかなS字ベジェ曲線で構成され、`text` を指定した場合はティップの外側にラベルを配置可能にする。

---

### 3.6. `document`（波底ドキュメント / 書類）— 【Phase 2】
- **シグネチャ案**:
  ```python
  def document(
      xy: Coordinate,
      width: PosFloat,
      height: PosFloat,
      *,
      stacked: PosInt = 1,
      wave_ratio: Ratio = 0.14,
      style: Style,
      text: str = "",
      text_style: Style | None = None,
  ) -> None:
  ```
- **設計ポイント**:
  - 上辺・左右辺が直線、下辺が滑らかな3次ベジェS字波線で構成されるフローチャート標準の「書類」図形。
  - `stacked > 1`（例: `stacked=3`）のときは、背後に少しずつオフセットした書類レイヤーを重ねて描画し、「複数ファイル／バッチドキュメント群」を1関数で表現可能にする。

---

## 4. 検証・ドッグフーディング手順 (Verification Workflow)

各図形の実装時には以下のステップを必須とする：
1. **単体テスト (`tests/drawlib/_core/l4_canvas/test_<shape>.py`)**:
   - 各オプション・スタイル・角丸（`shape_r`）・回転（`angle`）・テキスト埋め込み・異常値バリデーション（`ValueError` / `ValidationError`）の網羅。
2. **静的解析 (`./dcli code-check all`)**:
   - Ruff lint/format（循環的複雑度 `C901 <= 10` を含む）、Ty 型チェック、`@validate_call` docstring チェックの完全パス。
3. **ルール＆ドキュメント更新・視覚確認**:
   - `src/drawlib/_rules/api.md`, `src/drawlib/_rules/lib_shapes.md`, `docs/docs_src/02_drawing_primitives/` を更新し、`./dcli docs build site` および `view_file` で実際のレンダリング画像を視覚レビューする。
