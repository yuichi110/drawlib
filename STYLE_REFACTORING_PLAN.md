# drawlib v0.3 Style Architecture Refactoring Plan

## 1. 背景と目的 (Background & Motivation)

### 1.1. 現行アーキテクチャ (v0.2 以前) の課題
- **暗黙的解決 (Magic Defaults) による不透明性**:
  - `style="blue_flat"` などの文字列ショートカットは実行時に文字列走査・パース（`get_style()`）されて解決されるため、IDE での補完が効かず、typo しても静的解析（Pyright/Mypy）で検知できない。
  - プロパティの省略時に `SYSTEM_DEFAULT_*.merge()` で裏で勝手に値が補完されるため、意図しない描画崩れがサイレントに発生する。
- **属性のオーバーロード（用途の衝突）**:
  - `line_color` や `line_width` が「Shape の枠線」と「独立した Line / Arrow」で共用されており、`patch` やプリセット定義時に意図の衝突が発生する。
  - アイコンに `text_color`、画像の枠線に `line_color`、画像の着色に `fill_color` が流用され、属性名と役割の乖離が著しい。
- **ミュータブルな設計と防御的コピーのオーバーヘッド**:
  - `Style` がミュータブルであるため、副作用を防ぐ目的でライブラリ内の至る所で `.copy()`（ディープコピー）が呼ばれ、性能とコードの透明性を損ねている。

### 1.2. v0.3 の方針: AIファースト & 完全型安全
- **v0.3.0 において後方互換性を完全に切る（Breaking Change）**。
- **AI によるコード生成と自己修正ループ（Run -> Pyright -> Fix）を第一級市民とする**。
- 暗黙のデフォルトや推測による補完を一切排除し、完全に決定論的かつ型安全なアーキテクチャへとフルリファクタリングする。

---

## 2. コア設計原則 (Core Principles)

1. **Explicit is Better than Implicit (明示性の徹底)**:
   - スタイルの指定を省略可能にせず、**すべての描画関数・コンポーネントでスタイル受け取りを完全必須（デフォルト値なし）** とする。
   - ライブラリ側での「忖度したデフォルト値補完」を全廃する。
2. **Immutable & Minimal (完全不変と最小主義)**:
   - `Style` は `ConfigDict(frozen=True)` とし、インスタンス化後は一切変更不可とする。
   - `copy()` は不要のため廃止。`merge()` も廃止。
   - スタイルの差分生成メソッドは唯一 **`patch(...)` のみ** とする。
3. **Domain-Specific Attribute Segregation (ドメインプレフィックスによる完全分離: 案A)**:
   - `drawlib` のモジュール構造（`shapes`, `lines`, `text`, `icons`, `images`）に 1:1 で対応した属性名を採用：
     - `shape_*`: 面の塗り、枠線
     - `line_*`: 線、矢印
     - `text_*`: 文字、フォント、背景枠
     - `icon_*`: アイコン色、スタイル
     - `image_*`: 画像枠線、ティント
4. **Contextual Fail-Fast Validation (コンテキストに応じた即時エラー終了)**:
   - 描画関数ごとに必要なコア属性が `None` の場合、即座に `ValueError` で終了する。
5. **No Static Global Singletons (明示的なカタログ取得)**:
   - モジュールレベルの省略形（`ds` など）は作らず、**`styles = get_default_styles()`** のようにユーザーがファクトリ関数から明示的に取得する。

---

## 3. 詳細アーキテクチャ仕様 (Detailed Architecture Specifications)

### 3.1. `Style` クラス (`src/drawlib/_core/l3_styles/_style_models.py`)

基底クラス `_StyleModel` を廃止し、`Style` を直接 Pydantic `BaseModel` として実装する。

```python
from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from drawlib._core.l2_types import (
    TypeAlpha, TypeAngle, TypeColor, TypeCoordinate, TypeFont,
    TypeHAlign, TypeIconStyle, TypeLineStyle, TypePosFloat, TypeSize, TypeVAlign
)

class Style(BaseModel):
    """Immutable universal style model for drawlib."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )

    # --- Shape Properties (shapes.rectangle, shapes.circle, etc.) ---
    shape_fill_color: TypeColor | None = None
    shape_fill_alpha: TypeAlpha | None = None
    shape_line_color: TypeColor | None = None
    shape_line_width: TypePosFloat | None = None
    shape_line_style: TypeLineStyle | None = None

    # --- Line / Arrow Properties (lines.line, lines.arrow, etc.) ---
    line_color: TypeColor | None = None
    line_width: TypePosFloat | None = None
    line_style: TypeLineStyle | None = None
    line_alpha: TypeAlpha | None = None
    line_arrow_head_fill: bool | None = None
    line_arrow_head_scale: TypePosFloat | None = None

    # --- Text Properties (text.text, text.text_vertical, shape embedded text) ---
    text_color: TypeColor | None = None
    text_size: TypeSize | None = None
    text_font: TypeFont | None = None
    text_halign: TypeHAlign | None = None
    text_valign: TypeVAlign | None = None
    text_angle: TypeAngle | None = None
    text_flip: bool | None = None
    text_xy_shift: TypeCoordinate | None = None
    text_xy_abs_shift: TypeCoordinate | None = None
    text_bg_fill_color: TypeColor | None = None
    text_bg_fill_alpha: TypeAlpha | None = None
    text_bg_line_color: TypeColor | None = None
    text_bg_line_width: TypePosFloat | None = None
    text_bg_line_style: TypeLineStyle | None = None

    # --- Icon Properties (icons.phosphor, icons.font_icon, icons.gcp) ---
    icon_color: TypeColor | None = None
    icon_style: TypeIconStyle | None = None

    # --- Image Properties (images.image) ---
    image_tint_color: TypeColor | None = None
    image_alpha: TypeAlpha | None = None
    image_border_color: TypeColor | None = None
    image_border_width: TypePosFloat | None = None
    image_border_style: TypeLineStyle | None = None

    def patch(
        self,
        *,
        shape_fill_color: TypeColor | None = None,
        shape_fill_alpha: TypeAlpha | None = None,
        shape_line_color: TypeColor | None = None,
        shape_line_width: TypePosFloat | None = None,
        shape_line_style: TypeLineStyle | None = None,
        line_color: TypeColor | None = None,
        line_width: TypePosFloat | None = None,
        line_style: TypeLineStyle | None = None,
        line_alpha: TypeAlpha | None = None,
        line_arrow_head_fill: bool | None = None,
        line_arrow_head_scale: TypePosFloat | None = None,
        text_color: TypeColor | None = None,
        text_size: TypeSize | None = None,
        text_font: TypeFont | None = None,
        text_halign: TypeHAlign | None = None,
        text_valign: TypeVAlign | None = None,
        text_angle: TypeAngle | None = None,
        text_flip: bool | None = None,
        text_xy_shift: TypeCoordinate | None = None,
        text_xy_abs_shift: TypeCoordinate | None = None,
        text_bg_fill_color: TypeColor | None = None,
        text_bg_fill_alpha: TypeAlpha | None = None,
        text_bg_line_color: TypeColor | None = None,
        text_bg_line_width: TypePosFloat | None = None,
        text_bg_line_style: TypeLineStyle | None = None,
        icon_color: TypeColor | None = None,
        icon_style: TypeIconStyle | None = None,
        image_tint_color: TypeColor | None = None,
        image_alpha: TypeAlpha | None = None,
        image_border_color: TypeColor | None = None,
        image_border_width: TypePosFloat | None = None,
        image_border_style: TypeLineStyle | None = None,
    ) -> Style:
        """Return a new Style instance with specified attributes updated."""
        updates = {
            k: v for k, v in locals().items()
            if k not in ("self", "updates") and v is not None
        }
        return self.model_copy(update=updates)
```

---

### 3.2. プリセットカタログ (`src/drawlib/_preset_styles/`)

#### カタログ取得ファクトリ関数
- `get_default_styles() -> DefaultStyles`
- `get_essentials_styles() -> EssentialsStyles`
- `get_monochrome_styles() -> MonochromeStyles`
- `get_styles(name: str) -> BasePresetStyles`

#### カタログモデルのプロパティ構造
カタログクラス（`DefaultStyles` 等）は、完全な属性を持つ `Style` オブジェクトをプロパティとして提供する：
- **セマンティックロール**:
  - `styles.primary`: テーマのメインスタイル
  - `styles.light`: 細線・軽量フォント
  - `styles.bold`: 太線・太字フォント
  - `styles.flat`: 枠線なしベタ塗り（`shape_line_width=0`）
  - `styles.solid`: 塗り透過、枠線あり（`shape_fill_color=Colors.Transparent`）
  - `styles.dashed`: 塗り透過、破線枠線（`shape_line_style="dashed"`）
- **カラー別スタイル**:
  - `styles.blue`, `styles.blue_flat`, `styles.blue_solid`, `styles.blue_bold`
  - `styles.red`, `styles.red_flat`, `styles.red_solid`, `styles.red_bold`
  - `styles.green`, `styles.green_flat`, etc.
  - `styles.charcoal`, `styles.white`, `styles.white_bold`, etc.

**※ 完全充填ルール**:
公式カタログの各 `Style` は、`shape_*`, `line_*`, `text_*`, `icon_*` の **すべてのコア属性が最初から完全に定義** されている。そのため、単一の `styles.blue` を図形・線・テキスト・アイコンのどこに渡しても調和して動作する。

#### 廃止するもの
- 文字列パース・トークン分割処理（旧 `_officials.py` 内の `get_style("blue_flat")` 等）は完全削除する。

---

### 3.3. レンダリング層と Fail-Fast バリデーション (`src/drawlib/_core/l4_canvas_utils/`)

`SYSTEM_DEFAULT_*.merge(...)` による穴埋めマージを全廃する。
描画時に、その描画コンテキストで必要な属性が `None` の場合は即座に `ValueError` を送出する。

#### 必須コア属性の境界定義

| 描画モジュール | 必須コア属性（`None` なら即座に `ValueError`） | 任意（`None` で装飾無効） |
| :--- | :--- | :--- |
| **`shapes.*`** | `shape_fill_color`, `shape_line_color`, `shape_line_width` | `shape_fill_alpha`, `shape_line_style` |
| **`lines.*`** | `line_color`, `line_width` | `line_style`, `line_alpha`, `line_arrow_*` |
| **`text.*`** | `text_color`, `text_size`, `text_font` | `text_angle`, `text_bg_*` |
| **`icons.*`** | `icon_color` | `icon_style` |
| **`images.*`** | （画像描画自体の必須属性はなし） | `image_tint_color`, `image_border_*` |

---

### 3.4. 公開描画 API のシグネチャ (`src/drawlib/_core/l4_canvas/`)

全描画関数で `style: Style` を **キーワード必須引数（デフォルト値なし）** に変更する。

```python
# shapes (rectangle, circle, polygon, etc.)
def rectangle(
    xy: TypeCoordinate,
    width: TypePosFloat,
    height: TypePosFloat,
    *,
    style: Style,                     # 完全必須
    r: TypePosFloat = 0.0,
    angle: TypeAngle = 0.0,
    text: TypeStr = "",
    textstyle: Style | None = None,   # text 指定時のみ有効（None なら style の text_* を適用）
) -> None: ...

# lines (line, lines, arrow, bezier, etc.)
def line(
    xy1: TypeCoordinate,
    xy2: TypeCoordinate,
    *,
    style: Style,                     # 完全必須
    arrowhead: TypeArrowHead = "",
) -> None: ...

# text (text, text_vertical)
def text(
    xy: TypeCoordinate,
    text: TypeStr,
    *,
    style: Style,                     # 完全必須
    size: TypeSize | None = None,
    angle: TypeAngle = 0.0,
) -> None: ...
```

---

### 3.5. 高レベル複合コンポーネントのシグネチャ

- **単一要素 (`_icons/`)**:
  - `phosphor.*`, `font_icon.*`, `gcp.*`: **`style: Style` を完全必須**。
- **複合コンポーネント (`_smartarts/`, `_diagrams/`, `_charts/`)**:
  - 複数の要素・色で構成されるため、単一の `Style` ではなく **`styles: BasePresetStyles`（カタログオブジェクト）をコンストラクタで完全必須** とする。

```python
# SmartArts
process = ChevronProcess(
    (50, 50), width=80, height=20,
    styles=styles,  # 完全必須
)
process.add_step("Step 1", style=styles.blue)  # 個別オーバーライド

# Diagrams
flow = FlowDiagram(styles=styles)  # 完全必須
flow.node("A", style=styles.blue_flat)

# Charts
chart = BarChart(
    xy=(50, 50), width=80, height=50,
    styles=styles,  # 完全必須
)
```

---

## 4. コード移行例 (Before & After)

### 【Before】(v0.2 以前: 暗黙的文字列解決とマージ)
```python
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=100, height=50)

# 文字列指定（typo しても静的検査不可、style 省略時の暗黙デフォルト）
rectangle((25, 25), 20, 15, style="blue_flat", text="Client", textstyle="white_bold")
rectangle((75, 25), 20, 15, style="green_solid_bold", text="Server", textstyle="green_bold")
line((35, 25), (65, 25), style="charcoal_dashed", arrowhead="->")

save()
```

### 【After】(v0.3: 型安全・イミュータブル・明示必須)
```python
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.preset_styles import get_default_styles
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=100, height=50)

# 1. スタイルカタログを取得
styles = get_default_styles()

# 2. 完全な型ヒント付きで明示的に渡す（typo は即座に静的解析でエラー）
rectangle((25, 25), 20, 15, style=styles.blue_flat, text="Client", textstyle=styles.white_bold)
rectangle((75, 25), 20, 15, style=styles.green_solid, text="Server", textstyle=styles.green_bold)

# 3. 差分は patch() で安全かつインラインで適用
line(
    (35, 25), (65, 25),
    style=styles.charcoal.patch(line_width=1.8, line_style="dashed"),
    arrowhead="->",
)

save()
```

---

## 5. 実装ロードマップとタスク一覧 (Implementation Roadmap)

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     Phase 1     │ ──► │     Phase 2     │ ──► │     Phase 3     │
│ Core Style &    │     │ Canvas Utils &  │     │ High-level APIs │
│ Preset Catalogs │     │ Canvas API      │     │ & Components    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │     Phase 4     │
                                                │ Tests, Docs &   │
                                                │ Full Validation │
                                                └─────────────────┘
```

### Phase 1: コアモデル & プリセットカタログの再実装
- [ ] **Task 1.1: `Style` クラスの再実装** (`src/drawlib/_core/l3_styles/_style_models.py`)
  - `_StyleModel` 削除、`frozen=True`、新属性群（`shape_*`, `line_*`, `text_*`, etc.）実装。
  - `patch(...)` メソッド実装。`copy()` / `merge()` 削除。
- [ ] **Task 1.2: `_system_default.py` の整理** (`src/drawlib/_core/l3_styles/_system_default.py`)
  - 不要なマージ用定数を削除。
- [ ] **Task 1.3: カタログモデルの再構築** (`src/drawlib/_preset_styles/_models.py`)
  - `BasePresetStyles`, `DefaultStyles`, `EssentialsStyles`, `MonochromeStyles` に型付きカラー属性を定義。
- [ ] **Task 1.4: 公式カタログ実装 & 文字列パース削除** (`src/drawlib/_preset_styles/_officials.py`)
  - 完全充填された `Style` インスタンス群を構築するファクトリ実装。
  - `get_style()` の文字列パースロジックを完全削除。

### Phase 2: レンダリング層 & Canvas 公開 API の厳格化
- [ ] **Task 2.1: Canvas ユーティリティ改修** (`src/drawlib/_core/l4_canvas_utils/`)
  - `ShapeUtil`, `LineUtil`, `TextUtil`, `ImageUtil` の属性アクセス先を新プレフィックスへ変更。
  - 必須コア属性の Fail-Fast バリデーション（欠落時 `ValueError`）を実装。
- [ ] **Task 2.2: 描画関数シグネチャの更新** (`src/drawlib/_core/l4_canvas/`)
  - `_patches.py`, `_line.py`, `_arrow.py`, `_polygon.py`, `_text.py`, `_image.py` の全メソッドで `style: Style`（必須）に変更。

### Phase 3: 上位コンポーネントのシグネチャ更新
- [ ] **Task 3.1: アイコン API の更新** (`src/drawlib/_icons/`)
  - `phosphor.*`, `font_icon.*`, `gcp.*` で `style: Style` を必須引数に変更。
- [ ] **Task 3.2: SmartArts の更新** (`src/drawlib/_smartarts/`)
  - `ChevronProcess`, `Tree`, `Table`, `MindMap`, `GridLayout` 等で `styles: BasePresetStyles` を必須引数に変更。
- [ ] **Task 3.3: Diagrams & Charts の更新** (`src/drawlib/_diagrams/`, `src/drawlib/_charts/`)
  - `FlowDiagram`, `SequenceDiagram`, `BarChart`, `LineChart` 等で `styles: BasePresetStyles` を必須引数に変更。

### Phase 4: テスト・ドキュメント更新 & プロジェクト全体検証
- [ ] **Task 4.1: 単体テスト・統合テストの更新** (`tests/`)
  - `pytest tests/` を実行しながら、テストコード内のスタイル指定をすべて新 API に修正。
- [ ] **Task 4.2: ドキュメントソース・ルールの更新** (`docs_src/`, `src/drawlib/_rules/`)
  - `preset_styles.md`, `shapes.md`, `lines.md`, `overview.md` 等のサンプルコードとルール記述を更新。
- [ ] **Task 4.3: 全体品質チェックの実行**
  - `./dcli check all` (Ruff lint/format, Pyright type check, docstrings, tests) を完全通過させる。
