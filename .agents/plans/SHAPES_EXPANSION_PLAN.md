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
| **完了 (Phase 2)** | **`cloud`** | `_basic.py` | クラウド境界・単体ノード（4種の `variant`: `"standard"`, `"flat"`, `"fluffy"`, `"simple"` ＋ `bump_ratio`） | **実装済** |
| **完了 (Phase 2)** | **`brace`** | `_basic.py` | 括弧図形（`{}` 中括弧 / `[]` 角括弧 / `()` 丸括弧、上下左右4方向、`tip_ratio` / `tip_position_ratio`、`style.line_width` 太さ制御） | **実装済** |
| **完了 (Phase 2)** | **`cube`** | `_basic.py` | 3D直方体・コンテナ・ノード・ブロック（`cylinder` の相棒、3面自動明度シェーディング） | **実装済** |
| **完了 (Phase 2)** | **`document`** | `_basic.py` | ドキュメント・ファイル記号（4種の `variant`: `"wave"`, `"folded"`, `"double_wave"`, `"folded_wave"` ＋ `stacked: int = 1` 複数重ね対応） | **実装済** |
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
  - 加算（Plus）: `"+"`, `"plus"`
  - 減算（Minus）: `"-"`, `"−"`, `"minus"`
  - 乗算（Multiply）: `"*"`, `"x"`, `"×"`, `"multiply"`
  - 除算（Divide）: `"/"`, `"÷"`, `"divide"`
  - 等号（Equal）: `"="`, `"equal"`
  - 不等号（Not Equal）: `"!="`, `"≠"`, `"not_equal"`

```python
MathSymbol = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal[
        "+", "-", "−", "*", "x", "×", "/", "÷", "=", "!=", "≠",
        "plus", "minus", "multiply", "divide", "equal", "not_equal",
    ],
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

### 3.3. `cloud`（クラウド / 雲形）— 【Phase 2：複数バリエーション＆モコモコ比率対応】

クラウド図形は「単体ノード（アイコン・カード風）」として使う場合と「複数要素を囲む大きなネットワーク境界枠」として使う場合で最適なシルエットが異なるため、**4種類の `variant`** と **`bump_ratio`（モコモコの深さ比率）** を提供する。

#### 3.3.1. シグネチャ & 型定義
```python
CloudVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["standard", "flat", "flat_bottom", "fluffy", "dense", "simple", "minimal"],
]

@validate_call
def cloud(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: CloudVariant = "standard",
    bump_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```

#### 3.3.2. `variant` と `bump_ratio` の仕様
| `variant` 値 | シルエットの特徴 | 主な用途 |
| :--- | :--- | :--- |
| **`"standard"`** *(デフォルト)* | 全周 8 個前後の大小バンプを持つバランスの良い王道クラウド | 汎用（Internet ノード、中規模の境界囲み） |
| **`"flat"`** (`"flat_bottom"`) | **底面が水平（フラット）**で、上部に3〜4個のドームが並ぶモダン形状 | 単体ノード・カード代替（内部にテキストやアイコンを置いたときの安定感・接地感が抜群） |
| **`"fluffy"`** (`"dense"`) | 全周 12 個前後の**細かいふくらみ**が連続する雲 | 大きな VPC / WAN / Public Cloud 領域を破線で囲む境界ボックス（大きく引き伸ばしても間延びしない） |
| **`"simple"`** (`"minimal"`) | 6 個の大きな弧だけで構成されたシンプル・対称寄りの雲 | 小さいサイズで配置するバッジや思考バブル |

- **`bump_ratio: Ratio | None = None`**:
  - 短辺 `min(width, height)` に対する「外周バンプ（ふくらみ・谷の切れ込み）の深さ」の比率（`None` 時は各 `variant` の最適デフォルト値 `0.20` 前後を適用）。
  - 小さくすると「浅く落ち着いた雲」、大きくすると「モコモコ感が強調された雲」になる。

---

### 3.4. `brace`（括弧図形：`{}` `[]` `()` ＋ `{` の尖り Ratio 制御）— 【Phase 2】

中括弧 `{}`・角括弧 `[]`・丸括弧 `()` の3種類と上下左右4方向に対応し、線の太さ・色・線種は `style`（`style.line_width` / `style.line_color` / `style.line_style`、または `shape_line_*` フォールバック）で直感的に調整できる設計とする。`{}` では尖り具合（`tip_ratio`）と尖り位置（`tip_position_ratio`）を柔軟に制御でき、`[]` では `style.shape_r` による角丸にも対応する。

#### 3.4.1. シグネチャ & 型定義
```python
BraceSymbol = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal[
        "{", "}", "{}", "curly",
        "[", "]", "[]", "square",
        "(", ")", "()", "round",
    ],
]

BraceDirection = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal["left", "right", "top", "bottom"],
]

@validate_call
def brace(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    symbol: BraceSymbol = "{",
    direction: BraceDirection | None = None,
    tip_ratio: Ratio | None = None,
    tip_position_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```

#### 3.4.2. パラメーター仕様
| 引数名 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 中心座標 `(cx, cy)`（Center-Anchored）。 |
| `width` / `height` | `PosFloat` | *必須* | 括弧全体のバウンディングボックスの幅・高さ。 |
| `symbol` | `BraceSymbol` | `"{"` | 括弧の種類：中括弧 (`"{"`, `"}"`, `"{}"`, `"curly"`)、角括弧 (`"["`, `"]"`, `"[]"`, `"square"`)、丸括弧 (`"("`, `")"`, `"()"`, `"round"`)。 |
| `direction` | `BraceDirection \| None` | `None` | 括弧を配置する側（尖り・背が向く方向）：`"left"`, `"right"`, `"top"`, `"bottom"`。`None` の場合、`"{"`/`"["`/`"("` は `"left"`（左側に置く括弧）、`"}"`/`"]"`/`")"` は `"right"`（右側に置く括弧）を自動選択。 |
| `tip_ratio` | `Ratio \| None` | `None` | **`{}` 専用**：奥行き（横向き配置なら `width`、上下配置なら `height`）のうち、**中央の尖り（突起 / Tip）が前に突き出る比率**（`None` 時は `0.50`）。大きくすると鋭く長く突き出し、小さくすると控えめな突起になる。 |
| `tip_position_ratio` | `Ratio \| None` | `None` | **`{}` 専用**：スパン方向における**中央の尖りの位置比率**（`None` 時は `0.50`＝中央）。`0.25` や `0.75` にすると非対称な中括弧になる。 |
| `style` | `Style` | *必須* | 線の太さ（`line_width` / `shape_line_width`）・色（`line_color` / `shape_line_color`）・線種（`line_style` / `shape_line_style`）・回転角（`angle`）・角丸（`shape_r`：`[]` のコーナー半径）スタイル。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | テキストとテキストスタイル。 |

---

### 3.5. `cube`（3Dキューブ / 直方体）— 【Phase 2】
- **シグネチャ**:
  ```python
  @validate_call
  def cube(
      self,
      xy: Coordinate,
      width: PosFloat,
      height: PosFloat,
      *,
      depth_ratio: Ratio | None = None,
      style: Style,
      text: str = "",
      text_style: Style | None = None,
  ) -> None:
  ```
- **設計ポイント**:
  - 外寸が `(width, height)` のバウンディングボックスに厳密に収まる3D直方体。
  - `depth_ratio`（`None` 時は `0.25`）で `min(width, height)` に対する奥行き幅を制御。
  - 既存の [`cylinder`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_core/l4_canvas/_shapes/_basic.py#L676-L892) と同じ思想で、`style.shape_fill_color` から **前面（ベース色）・上面（明度アップ）・右側面（明度ダウン）** を自動算出。
  - 3面の塗りと外周＋Y字稜線のストロークパスを分離して描画することで、`Dashed` / `Dotted` スタイルでも共有辺の破線が二重に重ならない。
  - `text` は前面（フロントフェイス）の中央に自動配置することで、立体稜線と重ならずにラベルを表示できる。

---

### 3.6. `document`（ドキュメント / ファイル / 書類）— 【Phase 2】

フローチャートの波底書類（`"wave"`）、右上角折れファイル／ノート（`"folded"`）、上下波線の抜粋／ログ断片（`"double_wave"`）、角折れ＋波底レポート（`"folded_wave"`）の4種の `variant` と、複数枚重ね（`stacked: PosInt = 1`）に対応する。

#### 3.6.1. シグネチャ & 型定義
```python
DocumentVariant = Annotated[
    str,
    BeforeValidator(_normalize_str),
    Literal[
        "wave", "standard",
        "folded", "page", "note",
        "double_wave", "snippet",
        "folded_wave", "report",
    ],
]

@validate_call
def document(
    self,
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    *,
    variant: DocumentVariant = "wave",
    stacked: PosInt = 1,
    wave_ratio: Ratio | None = None,
    fold_ratio: Ratio | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
```

#### 3.6.2. `variant` とパラメータ仕様
| `variant` 値（エイリアス） | 形状の特徴 | 主な用途 |
| :--- | :--- | :--- |
| **`"wave"`** (`"standard"`) *(デフォルト)* | 上辺・左右が直線で、**下辺がS字の3次ベジェ波線** | フローチャートの標準「書類・帳票・出力レポート」記号 |
| **`"folded"`** (`"page"`, `"note"`) | 長方形の**右上の角が内側に折れ曲がった（ドッグイヤー）**形状（折り返しフラップは自動シェーディング） | 設定ファイル（YAML/JSON）、ソースファイル、PDF/Markdown文書、UMLノート |
| **`"double_wave"`** (`"snippet"`) | **上辺と下辺の両方がS字の波線**になっている形状 | 連続ログファイル（Access Logs）、ストリームデータ断片、長文の一部抜粋 |
| **`"folded_wave"`** (`"report"`) | **右上のドッグイヤー（角折れ）＋ 下辺のS字波線**の組み合わせ | ファイル感と複数ページ／継続レポート感の両方を備えたドキュメント |

- **`stacked: PosInt = 1`**:
  - `stacked > 1`（例: `stacked=3`）のときは、全体の `(width, height)` バウンディングボックス内に収まるよう右上奥へ向かって `stacked` 枚のシートを重ねて描画する（全 `variant` で利用可能）。
- **`wave_ratio: Ratio | None = None`**:
  - シート高さに対する波の深さ比率（デフォルト `0.15`、`"wave"`, `"double_wave"`, `"folded_wave"` で有効）。
- **`fold_ratio: Ratio | None = None`**:
  - シート短辺 `min(sheet_w, sheet_h)` に対する右上角折れサイズ比率（デフォルト `0.24`、`"folded"`, `"folded_wave"` で有効）。

---

## 4. 検証・ドッグフーディング手順 (Verification Workflow)

各図形の実装時には以下のステップを必須とする：
1. **単体テスト (`tests/drawlib/_core/l4_canvas/test_<shape>.py`)**:
   - 各オプション・スタイル・角丸（`shape_r`）・回転（`angle`）・テキスト埋め込み・異常値バリデーション（`ValueError` / `ValidationError`）の網羅。
2. **静的解析 (`./dcli code-check all`)**:
   - Ruff lint/format（循環的複雑度 `C901 <= 10` を含む）、Ty 型チェック、`@validate_call` docstring チェックの完全パス。
3. **ルール＆ドキュメント更新・視覚確認**:
   - `src/drawlib/_rules/api.md`, `src/drawlib/_rules/lib_shapes.md`, `docs/docs_src/02_drawing_primitives/` を更新し、`./dcli docs build site` および `view_file` で実際のレンダリング画像を視覚レビューする。

