# Drawlib Style & Color Architecture Refactoring Plan: `supports`, Semantics, and Orthogonal 10-Variant System

This document specifies the complete technical design, object model, API contracts, and implementation plan for refactoring the Drawlib Color and Style system.
It establishes semantic colors as the foundation, introduces strict fail-fast validation via `Style.supports`, and implements a fully orthogonal 10-variant naming scheme optimized for AI code generation and human developer ergonomics.

---

## 1. 背景と課題 (Background & Issues)

### 1.1. 現行実装の課題
1. **視覚的不整合（枠線の消失）**:
   - `_make_variants()` において、`white` と `primary` 以外は `shape_line_color = color`（塗りと同色）に設定されていた。
   - その結果、赤色ボックスの外枠に赤色の線が引かれ、**「枠線が存在するのに塗りに溶けて見えない（`flat` と見分けがつかない）」** という不整合が発生していた。
2. **単一 Style モデルによる用途の衝突（Text vs Shape）**:
   - `Style` が `shape_*`, `line_*`, `text_*`, `icon_*` を1つのオブジェクトで兼ねている。
   - 例えば `styles.red` の `text_color` を赤にすると `text(..., style=styles.red)` は赤文字になるが、`rectangle(..., style=styles.red, text="Server")` は赤地に赤文字となって読めなくなる。
   - 逆に `styles.red` の `text_color` を白にすると、キャンバスに直接 `text(..., style=styles.red)` を描いた際に白文字（見えない文字）になってしまう。
3. **未サポート属性（None）の呼び出し時の曖昧さ**:
   - どのスタイルがどの描画コンテキスト（図形・線・テキスト・アイコン）に対応しているかが明示されておらず、誤ったコンテキストで使われた際のエラーや挙動が一貫していない。
   - AI がスタイルを選択する際、`solid`（実際は透明枠線）など誤解を招きやすい名称が存在し、意図しない描画結果になりやすい。
4. **色のセマンティクス（意味的役割）の欠如**:
   - 図版の美しさを保つための中心概念である `primary` が `Styles` 側だけに孤立して存在しており、下層の `Colors` にセマンティクスがない。
   - 補助サービスや境界線、注目要素に使う推奨カラーが未定義なため、AI が具象カラー（赤・青・緑・黄）をランダムに散りばめて図のデザインが崩れる。

---

## 2. コア設計原則 (Core Principles)

1. **Colors First (色のセマンティクスが最下層の基盤)**:
   - レイヤー構造（`Colors` ➔ `Styles`）に従い、まず `BaseColors` にセマンティックカラー（`Primary`, `Secondary`, `Accent`, `Muted`）を定義する。
   - `Styles` は `Colors` のセマンティックカラーを参照してセマンティックスタイルを構築する（Single Source of Truth）。
2. **Strict Fail-Fast (厳格な即時エラー終了)**:
   - スタイルがサポートしていない描画対象（例: `flat` スタイルを `text()` に渡す、テキスト専用スタイルを `rectangle()` に渡す）で呼び出された場合、または必須属性が `None` の場合、即座に明確な `ValueError` で実行を停止する。
3. **Explicit Target Declaration (`Style.supports`)**:
   - すべての `Style` インスタンスは、自身が有効な描画ターゲットの集合（`supports: frozenset[SupportType]`）を明示的に保持する。
4. **Orthogonal 10-Variant Naming Scheme (完全直交な10バリアント体系)**:
   - 「形状タイプ（4種: `bordered`, `flat`, `outline`, `dashed`）」×「線の太さ・重み（3種: 通常, `bold`, `light`）」を完全に網羅し、穴のない対称な命名体系を提供する。
5. **Focused Semantic Roles (厳選された4大セマンティックロール)**:
   - モノクロ印刷やグレースケールでも100%美しく破綻しない、Twitter Bootstrap / Material 3 由来の4大ロール（`primary`, `secondary`, `accent`, `muted`）を採用する。
6. **Universal Simple Styles (単純系スタイルの保証)**:
   - `text()` や `line()`、`rectangle()` で自然に使える短縮形（`red`, `blue`, `white`, `charcoal` 等）および強弱形（`red_bold`, `white_bold` 等）を万能スタイルとして提供する。
7. **Consistent Class Naming (`Styles*` / `Colors*`)**:
   - カタログクラス名を `StylesDefault`, `StylesGoogle`, `StylesMonochrome` に統一し、IDE オートコンプリートを最適化する。

---

## 3. レイヤー別詳細仕様 (Detailed Layer Specifications)

```text
┌────────────────────────────────────────────────────────┐
│  Layer 4: Canvas Public APIs (rectangle, line, text)   │
│  - Fail-Fast check: "target in style.supports"         │
│  - Smart embedded text contrast fallback               │
└────────────────────────────────────────────────────────┘
                           ▲
┌────────────────────────────────────────────────────────┐
│  Layer 3B: Preset Styles (StylesDefault, StylesGoogle)  │
│  - 4 Semantic Roles x 10 Variants                      │
│  - Palette Colors x 10 Variants                        │
│  - Text-only styles (white, white_bold, etc.)          │
└────────────────────────────────────────────────────────┘
                           ▲
┌────────────────────────────────────────────────────────┐
│  Layer 3A: Core Style Model (Style.supports)           │
│  - frozenset[SupportType] + Invariants validation      │
└────────────────────────────────────────────────────────┘
                           ▲
┌────────────────────────────────────────────────────────┐
│  Layer 2: Colors Architecture (BaseColors, Default)    │
│  - Primary, Secondary, Accent, Muted semantic tokens   │
└────────────────────────────────────────────────────────┘
```

---

### 3.1. Layer 2: Colors アーキテクチャ改修 (`_preset_colors/`, `_core/l3_styles/`)

基底クラス `BaseColors` に 4 大セマンティックカラーを定義し、各具象カラーパレットで割り当てる。

```python
class BaseColors(BaseModel):
    """Base model for preset colors."""
    ...
    Primary: Color
    Secondary: Color
    Accent: Color
    Muted: Color

    # 小文字プロパティによるショートカットアクセス
    @property
    def primary(self) -> Color:
        return self.Primary

    @property
    def secondary(self) -> Color:
        return self.Secondary

    @property
    def accent(self) -> Color:
        return self.Accent

    @property
    def muted(self) -> Color:
        return self.Muted
```

#### 各カラーパレットでのセマンティック定義一覧表

| セマンティックカラー | 役割・意味 | `DefaultColors` | `GoogleColors` | `MonochromeColors` |
| :--- | :--- | :--- | :--- | :--- |
| **`Primary`** | **主役・メイン要素** | `LightBlue` | `CornflowerBlue` | `White` |
| **`Secondary`** | **準主役・サブ要素** | `Teal` (または `Steel`) | `Cyan` | `LightGray` |
| **`Accent`** | **注目・強調・入口** | `Orange` | `Amber` | `Black` |
| **`Muted`** | **背景コンテナ・境界線** | `Snow` (または `Gray`) | `LightGray2` | `Snow` |

---

### 3.2. Layer 3A: `Style` クラスの改修 (`_core/l3_styles/_style_models.py`)

`Style` に `supports` フィールドを追加し、不変条件のバリデーションを組み込む。

```python
SupportType = Literal["shape", "line", "text", "icon", "image"]
ALL_SUPPORTS: frozenset[SupportType] = frozenset({"shape", "line", "text", "icon", "image"})


class Style(BaseModel):
    """Immutable universal style model with explicit target support declaration."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )

    # 許可する描画ターゲット
    supports: frozenset[SupportType] = Field(default=ALL_SUPPORTS)

    # Shape properties
    shape_fill_color: ColorType | None = None
    shape_fill_alpha: Alpha | None = None
    shape_line_color: ColorType | None = None
    shape_line_width: PosFloat | None = None
    shape_line_style: LineStyle | None = None

    # Line properties
    line_color: ColorType | None = None
    line_width: PosFloat | None = None
    line_style: LineStyle | None = None
    line_alpha: Alpha | None = None
    line_arrow_head_fill: bool | None = None
    line_arrow_head_scale: PosFloat | None = None

    # Text properties
    text_color: ColorType | None = None
    text_size: Size | None = None
    text_font: Font | None = None
    text_halign: HAlign | None = None
    text_valign: VAlign | None = None
    text_angle: Angle | None = None
    text_flip: bool | None = None

    # Icon properties
    icon_color: ColorType | None = None
    icon_style: IconStyle | None = None

    # Image properties
    image_tint_color: ColorType | None = None
    image_alpha: Alpha | None = None
    image_border_color: ColorType | None = None
    image_border_width: PosFloat | None = None
    image_border_style: LineStyle | None = None

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        if "supports" in data and not isinstance(data["supports"], frozenset):
            data["supports"] = frozenset(data["supports"])
        try:
            super().__init__(**data)
        except ValidationError as e:
            raise ValueError(str(e)) from e

        self._validate_invariants()

    def _validate_invariants(self) -> None:
        """Validate that all targets declared in supports have required attributes populated."""
        if "shape" in self.supports:
            missing = [k for k in ("shape_fill_color", "shape_line_color", "shape_line_width") if getattr(self, k) is None]
            if missing:
                raise ValueError(f"Style declares 'shape' support, but required attributes {missing} are None.")

        if "line" in self.supports:
            missing = [k for k in ("line_color", "line_width") if getattr(self, k) is None]
            if missing:
                raise ValueError(f"Style declares 'line' support, but required attributes {missing} are None.")

        if "text" in self.supports:
            missing = [k for k in ("text_color", "text_size", "text_font") if getattr(self, k) is None]
            if missing:
                raise ValueError(f"Style declares 'text' support, but required attributes {missing} are None.")

        if "icon" in self.supports:
            if self.icon_color is None:
                raise ValueError("Style declares 'icon' support, but required attribute 'icon_color' is None.")
```

---

### 3.3. Layer 3B: スタイル命名体系（完全直交 10 バリアント）

すべての色（`red` など）およびセマンティックロール（`primary`, `secondary`, `accent`, `muted`）は、以下の **10個の完全直交バリアント** を持ちます。

```text
                                  ┌─── Regular (1.5px)  ──── <name> (or <name>_bordered)
         ┌── 枠あり (bordered) ───┼─── Bold    (2.5px)  ──── <name>_bold
         │                        └─── Light   (0.75px) ──── <name>_light
塗りあり ─┤
         └── 枠なし (flat) ───────────────────────────────── <name>_flat
                                  ┌─── Regular (1.5px)  ──── <name>_outline
         ┌── 実線 (outline)  ─────┼─── Bold    (2.5px)  ──── <name>_outline_bold
         │                        └─── Light   (0.75px) ──── <name>_outline_light
塗りなし ─┤
(透明)   │                        ┌─── Regular (1.5px)  ──── <name>_dashed
         └── 破線 (dashed)   ─────┼─── Bold    (2.5px)  ──── <name>_dashed_bold
                                  └─── Light   (0.75px) ──── <name>_dashed_light
```

#### バリアント別仕様・属性マトリクス

| バリアント名 | `supports` | 形状（Shape）設定 | 線（Line）設定 | テキスト設定 | 主な用途 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`<name>`**<br>(alias: `<name>_bordered`) | `{"shape", "line", "text", "icon"}` | 塗り=Color<br>枠=Charcoal (1.5) | 線=Color (1.5, solid) | 色=Color, Regular | 万能標準（カード、通常文字、通常矢印） |
| **`<name>_bold`** | `{"shape", "line", "text", "icon"}` | 塗り=Color<br>枠=Charcoal (2.5) | 線=Color (2.5, solid) | 色=Color, Bold | 強調ノード（太枠カード、太字、太矢印） |
| **`<name>_light`** | `{"shape", "line", "text", "icon"}` | 塗り=Color<br>枠=Charcoal (0.75) | 線=Color (0.75, solid) | 色=Color, Light | 控えめノード（細枠カード、細字、細矢印） |
| **`<name>_flat`** | `{"shape"}` | 塗り=Color<br>枠=None (0.0) | *(None)* | *(None)* | フラットバッジ、背景パネル（線・文字不可） |
| **`<name>_outline`** | `{"shape", "line"}` | 塗り=透明<br>枠=Color (1.5, solid) | 線=Color (1.5, solid) | *(None)* | 境界枠、透明コンテナ、標準実線矢印 |
| **`<name>_outline_bold`** | `{"shape", "line"}` | 塗り=透明<br>枠=Color (2.5, solid) | 線=Color (2.5, solid) | *(None)* | 重要境界線（VPC/外枠）、太い実線矢印 |
| **`<name>_outline_light`** | `{"shape", "line"}` | 塗り=透明<br>枠=Color (0.75, solid)| 線=Color (0.75, solid)| *(None)* | 補助境界線、細い実線矢印 |
| **`<name>_dashed`** | `{"shape", "line"}` | 塗り=透明<br>枠=Color (1.5, dashed)| 線=Color (1.5, dashed)| *(None)* | 論理グループ、サブネット、標準破線矢印 |
| **`<name>_dashed_bold`** | `{"shape", "line"}` | 塗り=透明<br>枠=Color (2.5, dashed)| 線=Color (2.5, dashed)| *(None)* | 強調破線境界、太い破線矢印 |
| **`<name>_dashed_light`** | `{"shape", "line"}` | 塗り=透明<br>枠=Color (0.75, dashed)|線=Color (0.75, dashed)| *(None)* | 控えめな論理グループ、細い破線矢印 |

#### テキスト専用スタイル (Text-Only Styles)
文字描画（`text()`）や `textstyle=` で文字色を明示指定するために完備：
- `styles.white`: `supports={"text"}`, text_color=White, regular
- `styles.white_bold`: `supports={"text"}`, text_color=White, bold
- `styles.white_light`: `supports={"text"}`, text_color=White, light
- `styles.charcoal_bold`: `supports={"text"}`, text_color=Charcoal, bold
- `styles.charcoal_light`: `supports={"text"}`, text_color=Charcoal, light

---

### 3.4. Layer 4: Canvas レンダラー・ユーティリティの Fail-Fast 検証 (`_core/l4_canvas_utils/`)

描画関数が呼ばれた際、渡された `style` が該当コンテキストをサポートしているか検証し、非対応なら即座に `ValueError` を送出する。

```python
# ShapeUtil.validate_shape_style(style: Style)
if "shape" not in style.supports:
    raise ValueError(f"Style cannot be used for shapes. Declared supports: {set(style.supports)}.")

# LineUtil.validate_line_style(style: Style)
if "line" not in style.supports:
    raise ValueError(f"Style cannot be used for lines. Declared supports: {set(style.supports)}.")

# TextUtil.validate_text_style(style: Style)
if "text" not in style.supports:
    raise ValueError(f"Style cannot be used for text. Declared supports: {set(style.supports)}.")

# IconUtil.validate_icon_style(style: Style)
if "icon" not in style.supports:
    raise ValueError(f"Style cannot be used for icons. Declared supports: {set(style.supports)}.")
```

#### 形状内テキストのスマートフォールバック (`_base.py` / `_shape.py`)
四角形等に `text="Server"` を指定した際、`textstyle` が省略されていれば、塗りの明度（Luminance）に応じた高コントラスト文字（White または Charcoal）を自動解決し、文字の不可読化を完全に防ぐ。

---

### 3.5. クラス名の統一規則

IDE のオートコンプリート（`Styles` や `Colors` での絞り込み）を最適化するため、プレフィックス記法に統一する：

- **Styles クラス**:
  - `StylesDefault` (旧 `DefaultStyles`)
  - `StylesGoogle` (旧 `GoogleStyles`)
  - `StylesMonochrome` (旧 `MonochromeStyles`)
  - ※ 後方互換エイリアス（`DefaultStyles = StylesDefault` 等）を必要に応じて配置。
- **Colors クラス**:
  - `DefaultColors`, `GoogleColors`, `MonochromeColors` (現状維持)

---

### 3.6. CLI カタログ表示 (`drawlib styles show` & `drawlib colors show`)

1. **`drawlib styles show`**:
   - 10列構成（bordered, bold, light, flat, outline, outline_bold, outline_light, dashed, dashed_bold, dashed_light）。
   - 最上段に **4大セマンティックロール**（primary, secondary, accent, muted）の専用行を常時表示。
   - 各スウォッチにサポート対象バッジ（`[S L T I]`, `[S]`, `[S L]`）を表示。
2. **`drawlib colors show`**:
   - 最上段に `Primary / Secondary / Accent / Muted` のセマンティックカラー行を表示。

---

## 4. AI 向けデザインガイドライン (`Rules`)

`.agents/rules/docs.md` およびライブラリ内部ルールに、以下の **デザイン黄金律** を明記する：

```markdown
## Diagram Styling & Semantic Best Practices

1. **The 60-30-10 Rule for Diagram Colors**:
   - **60% Neutral/Muted**: Canvas background, structural group boundaries (`styles.muted_dashed`).
   - **30% Primary/Secondary**: Main architectural flow (`styles.primary`, `styles.primary_flat`, `styles.secondary`).
   - **10% Accent/State**: Entry points (`styles.accent`), callouts, and key milestones.

2. **Prefer Semantic Roles over Raw Palette Colors**:
   - Use `styles.primary` for core application components.
   - Use `styles.secondary` for databases, caches, queues, and auxiliary services.
   - Use `styles.muted_outline` or `styles.muted_dashed` for VPC, Subnets, and Cluster boundaries.
   - Use `styles.accent` for Clients, Users, Gateways, and triggers.
   - Use raw palette colors (`styles.red`, `styles.green`) strictly for specific states (danger/success) or multi-brand differentiation.

3. **Recommended Palette Pairings (When needing 4+ colors)**:
   - **StylesDefault**: Companion colors matching Primary (LightBlue) are `teal`, `steel`, `navy`. Accent is `orange` or `purple`.
   - **StylesMonochrome**: Use `graphite`, `gray`, `silver` for subtle hierarchical tiers.
```

---

## 5. 実装ロードマップとタスク一覧 (Implementation Tasks)

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     Phase 0     │ ──► │     Phase 1     │ ──► │     Phase 2     │
│ Colors Semantic │     │ Style.supports  │     │ Canvas Fail-Fast│
│ Tokens Setup    │     │ Invariants Core │     │ & Contrast Logic│
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     Phase 5     │ ◄── │     Phase 4     │ ◄── │     Phase 3     │
│ Tests, Rules    │     │ CLI Catalogs    │     │ Styles 10-Var   │
│ & Verification  │     │ Update (10-col) │     │ & Classes Setup │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Phase 0: Colors 側のセマンティックカラー整備 (`_preset_colors/`)
- [ ] **Task 0.1**: `BaseColors` (`_core/l3_styles/_colors.py`) に `Primary`, `Secondary`, `Accent`, `Muted` 属性と小文字プロパティを定義。
- [ ] **Task 0.2**: `DefaultColors` (`_color_default.py`) にセマンティックカラーを割り当て。
- [ ] **Task 0.3**: `GoogleColors` (`_color_google.py`) にセマンティックカラーを割り当て。
- [ ] **Task 0.4**: `MonochromeColors` (`_color_monochrome.py`) にセマンティックカラーを割り当て。
- [ ] **Task 0.5**: `drawlib colors show` CLI でセマンティック行の表示に対応。

### Phase 1: コアモデル改修 (`_core/l3_styles/`)
- [ ] **Task 1.1**: `Style` モデルに `supports: frozenset[SupportType]` フィールドを追加。
- [ ] **Task 1.2**: `Style._validate_invariants()` を実装し、`supports` に含まれるターゲットの必須属性が `None` の場合に `ValueError` を送出するよう強制。
- [ ] **Task 1.3**: `Style.patch(...)` メソッドで `supports` の引き継ぎ・更新に対応。

### Phase 2: Canvas レンダラー・ユーティリティの Fail-Fast 検証 (`_core/l4_canvas_utils/`)
- [ ] **Task 2.1**: `ShapeUtil.validate_shape_style()` に `"shape" in style.supports` チェックを追加。
- [ ] **Task 2.2**: `LineUtil.validate_line_style()` に `"line" in style.supports` チェックを追加。
- [ ] **Task 2.3**: `TextUtil.validate_text_style()` に `"text" in style.supports` チェックを追加。
- [ ] **Task 2.4**: `IconUtil.validate_icon_style()` に `"icon" in style.supports` チェックを追加。
- [ ] **Task 2.5**: `ShapeUtil.resolve_embedded_text_style()` を実装し、四角形等の埋め込みテキストのコントラスト自動解決ロジックを統合。

### Phase 3: プリセット生成エンジン改修 (`_preset_styles/`)
- [ ] **Task 3.1**: `_utils.py` の `_create_style` および `_make_variants` を改修し、10バリアントの生成と正確な `supports` の付与を実装。
- [ ] **Task 3.2**: `StylesDefault` (`_style_default.py`) を実装（4大セマンティックロール ＋ 全25色の10バリアント、テキスト専用スタイル）。
- [ ] **Task 3.3**: `StylesMonochrome` (`_style_monochrome.py`) を実装（4大セマンティックロール ＋ モノクロ7色の10バリアント）。
- [ ] **Task 3.4**: `StylesGoogle` (`_style_google.py`) を実装（4大セマンティックロール ＋ Googleパレット色の10バリアント）。
- [ ] **Task 3.5**: クラス名を `StylesDefault`, `StylesGoogle`, `StylesMonochrome` に更新し、公開ファサードを整備。

### Phase 4: CLI カタログ改修 (`_cli/_styles.py`)
- [ ] **Task 4.1**: `_COL_HEADERS` を10列ヘッダーに更新。
- [ ] **Task 4.2**: 4大セマンティックロール行を最上部に表示。
- [ ] **Task 4.3**: サポート対象バッジ（`[S L T I]`, `[S]`, `[S L]`）をスウォッチに表示。
- [ ] **Task 4.4**: ページネーション（25色/ページ）との描画整合性を確認。

### Phase 5: テスト・Rules 更新 & プロジェクト全体検証 (`tests/`, `_rules/`)
- [ ] **Task 5.1**: `Style.supports` の単体テスト（未サポート呼び出し時の `ValueError` 発生確認）。
- [ ] **Task 5.2**: 各プリセットスタイルの完全性テスト（10バリアント網羅、欠落ゼロの確認）。
- [ ] **Task 5.3**: CLI `drawlib styles show` および `drawlib colors show` の結合テスト。
- [ ] **Task 5.4**: `.agents/rules/docs.md` および `src/drawlib/_rules/` にデザイン黄金律を反映。
- [ ] **Task 5.5**: プロジェクト全体の `./dcli check all`（Ruff, Ty, docstrings）および全 pytest の通過確認。
