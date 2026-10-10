# Drawlib SmartArts 拡張計画書 (`KpiCards`, `CardList`, `Roadmap`)
(DRAWLIB SMARTARTS EXPANSION PLAN)

- **作成日**: 2026-10-10
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x` / `v0.4.x`)
- **関連計画書**: [`.agents/plans/SLIDE_HELPERS_PLAN.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/.agents/plans/SLIDE_HELPERS_PLAN.md)（スライド固有ステージヘルパーの `drawlib.slide` への集約計画）
- **対象モジュール**:
  - `src/drawlib/smartarts.py` (公開ファサード: `KpiCards`, `KpiCardItem`, `CardList`, `CardListItem`, `Roadmap`, `RoadmapItem` をエクスポート)
  - `src/drawlib/_smartarts/_kpicards.py` (KPI・メトリクス強調カード群の実装)
  - `src/drawlib/_smartarts/_cardlist.py` (アイコン・番号バッジ・サブテキスト・矢印付きリッチカードリストの実装)
  - `src/drawlib/_smartarts/_roadmap.py` (直線・曲線対応のタイムライン／ロードマップの実装)
  - `src/drawlib/_smartarts/_geomap/_projection.py` (関連検討項目: `GeoMap` のデフォルトサイズ＆アスペクト比自動拡張オプション)
  - `src/drawlib/_rules/lib_smartarts.md`, `api.md` (AIエージェント向けルールの更新)
  - `tests/drawlib/smartarts/` (単体テスト・ビジュアルピクセル比較テスト)

---

## 1. エグゼクティブサマリー & 役割分担 (Executive Summary & Architectural Boundary)

### 1.1. `drawlib.smartarts` と `drawlib.slide` の責務分離
リポジトリ内の全ドッグフーディングプロジェクト（`docs/docs_src/`, `docs/slide_about_drawlib_src/`, `docs/slide_ddos_incident_response_src/`, `docs/drawlib-dogfooding_src/`, `docs/quickstart_src/`）およびテンプレートの `utils.py` を横断調査した結果、独自ヘルパーや手書きパターンは大きく以下の2種類に分類されることが判明した。

1. **汎用図解コンポーネント（`drawlib.smartarts` に収録すべきもの — 本計画書の対象）**:
   - 左下アンカー `xy` と `width`, `height` を受け取り、Webドキュメント（`site`）、PDF白書（`doc`）、単体画像（`images`）、スライド内の図版ブロック（`slide`）の**すべてのプロジェクト種別で共通利用できるキャンバス非依存のコンポーネント**。
   - **対象**: **`KpiCards`**、**`CardList`**、**`Roadmap`**（および既存 **`GeoMap`** の改善）。
2. **スライド専用ステージヘルパー（`drawlib.slide` に収録すべきもの — [`SLIDE_HELPERS_PLAN.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/.agents/plans/SLIDE_HELPERS_PLAN.md) で定義）**:
   - `current_slide` コンテキストや 16:9 フルブリードキャンバス（`192×108`）、スライドの章扉・アジェンダ・ページ番号・上部フェーズバー・下部 Takeaway バナーなど、**プレゼンテーションステージ固有のヘルパー関数群**。
   - **対象**: `draw_page_number()`, `draw_chapter_divider()`, `draw_curved_agenda()`, `draw_phase_bar()`, `draw_takeaway_banner()`。

### 1.2. なぜ `KpiCards`, `CardList`, `Roadmap` が `drawlib.smartarts` に必要か
1. **既存 `BoxList` の機能不足による「手書き `for` ループ」の乱立**:
   - 既存の `drawlib.smartarts.BoxList`（`src/drawlib/_smartarts/_boxlist.py`）は、「マージン0で単一テキストの矩形を隣接配置するのみ（アイコン不可・サブテキスト不可・番号バッジ不可・ボックス間ギャップ不可・接続矢印不可）」というプリミティブな仕様にとどまっている。
   - その結果、実際のドキュメントやスライドでは **「アイコン／番号バッジ ＋ 太字タイトル ＋ 1〜2行の補足説明文」** を持つリッチなカードリスト（例：5層防御ピラミッド横のL1〜L5解説カード、AIボットネットの3段フォレンジック証拠カード、ドキュメントのTop Heroステップ図など）が、毎回30〜50行の `rectangle` + `icon` + `text` の `for` ループで手書きされている。
2. **KPI メトリクスカードとタイムラインの汎用性**:
   - 従来スライドの `utils.py` に置かれていた `draw_kpi_cards` のようなメトリクス強調カードや、時系列のマイルストーンを示すロードマップ／タイムラインは、スライドだけでなく技術白書（`doc`）やドキュメントサイト（`site`）のサマリー図でも頻繁に求められる。
3. **既存 SmartArts ライフサイクル規約との100%統一**:
   - 他のステートフル SmartArts（`ChevronProcess`, `Cycle`, `Pyramid`, `GridLayout`）と同様、コンストラクタでデフォルトスタイルを受け取り、`add(..., show=True) -> Item` でミュータブルな要素オブジェクトを返し、`draw(xy, width, height, ..., scale=1.0)` で左下アンカー `xy` を基準に描画する。
   - アニメーション（`Animation` フレーム内での `item.show = True / False` 切り替えによるプログレッシブ・リビール）に完全対応する。

---

## 2. 調査結果：パターン棚卸しと収録先の整理

| パターン / 関数名 | 現在の実装場所 | 出現頻度 | 収録先モジュール・対応方針 |
| :--- | :--- | :---: | :--- |
| **`KpiCards`**<br>(旧 `draw_kpi_cards`) | `slide_*/utils.py`<br>`_templates/project/slide/utils/*` | 高（要約ページ・白書） | **`drawlib.smartarts.KpiCards`** として新設（縦スタック・横並び・2×2グリッド対応） |
| **`CardList`**<br>(手書きアイコン／バッジ付きカード配列) | 各ドキュメント・スライド内のインライン `for` ループ（20箇所以上） | 極高（全プロジェクト種別） | **`drawlib.smartarts.CardList`** として新設（縦・横・番号バッジ・アイコン・矢印対応） |
| **`Roadmap`**<br>(タイムライン・マイルストーン図) | 各ドキュメント・インシデント年表の手書きループ | 中〜高（工程表・年表） | **`drawlib.smartarts.Roadmap`** として新設（水平・垂直・曲線スパイン対応） |
| **`draw_page_number`** / **`draw_chapter_divider`** / **`draw_curved_agenda`** 等 | `slide_*/utils.py`<br>`_templates/project/slide/utils/*` | スライド専用 | **`drawlib.slide`** へ集約（詳細は [`SLIDE_HELPERS_PLAN.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/.agents/plans/SLIDE_HELPERS_PLAN.md) 参照） |
| **`service_card` / `connect`** | `_templates/project/_shared/utils.py` | サンプル用途のみ | 既に `ArchitectureDiagram` / `FlowDiagram` が公式提供されているため SmartArt 化は不要 |

---

## 3. 新規 SmartArt コンポーネント詳細設計

### 3.1. Component 1: `KpiCards` (`src/drawlib/_smartarts/_kpicards.py`)

大きなメトリクス数値（例：`300M+`, `$6,750`, `<50ms`, `99.9%`）とタイトル・補足説明文・アイコンを組み合わせた KPI カードを、縦スタック・横一列・グリッド（例：2×2）で自動整列するコンポーネント。

#### 3.1.1. データモデル & クラスシグネチャ
```python
class KpiCardItem(BaseModel):
    """Mutable item model for a single KPI card."""
    metric: str
    title: str
    description: str = ""
    style: Style
    metric_style: Style
    title_style: Style
    description_style: Style
    accent_style: Style | None = None
    icon: Callable[..., None] | None = None
    icon_style: Style | None = None
    show: bool = True


class KpiCards:
    """SmartArt component for rendering KPI / metric highlight cards."""

    @validate_call
    def __init__(
        self,
        *,
        style: Style = Styles.Neutral,
        metric_style: Style | None = None,
        title_style: Style | None = None,
        description_style: Style | None = None,
        accent_style: Style | None = None,
        accent_palette: Sequence[Color | tuple[int, int, int]] | None = None,
        accent_position: Literal["left_pill", "top_bar", "none"] = "left_pill",
        metric_layout: Literal["left_column", "top_stack"] = "left_column",
        metric_width_ratio: float = 0.28,
        spacing: float = 3.0,
    ) -> None: ...

    @validate_call
    def add(
        self,
        metric: str,
        title: str,
        description: str = "",
        *,
        style: Style | None = None,
        metric_style: Style | None = None,
        title_style: Style | None = None,
        description_style: Style | None = None,
        accent_style: Style | None = None,
        icon: Callable[..., None] | None = None,
        icon_style: Style | None = None,
        show: bool = True,
    ) -> KpiCardItem: ...

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        columns: int = 1,
        scale: PosFloat = 1.0,
    ) -> Self: ...
```

#### 3.1.2. レイアウト・ジオメトリ仕様
- **アンカー (`xy`)**: バウンディングボックス全体の **左下座標 `(x0, y0)`**。
- **グリッド分割 (`columns`)**:
  - `columns=1`（デフォルト）：上から下へ $N$ 枚のカードを等間隔 `spacing` で縦積み配置。
  - `columns=N`（横並び）または `columns=2`（2×2 グリッド）：指定された `width × height` を `columns` 列 $\times \lceil N / \text{columns} \rceil$ 行に自動分割して配置。
- **カード内部の2つのレイアウトモード (`metric_layout`)**:
  1. `"left_column"`（縦積みカード向けデフォルト）：
     - 左端 `x_left + card_w * 0.025` にアクセントピル（`accent_position="left_pill"`）を描画。
     - 左側領域（`card_w * metric_width_ratio`、デフォルト `28%`〜`30%`）に `metric` を大きく描画。
     - 右側領域（`x_left + card_w * metric_width_ratio` 以降）の上段に `title`、下段に `description` を左揃えで描画。
  2. `"top_stack"`（横並び・2×2グリッド向け）：
     - カード上段に `metric`（および任意の `icon`）、中段に `title`、下段に `description` を中央揃えまたは左揃えで配置。

---

### 3.2. Component 2: `CardList` (`src/drawlib/_smartarts/_cardlist.py`)

「アイコンバッジまたは番号バッジ ＋ 太字タイトル ＋ 補足説明文（1〜複数行）」を持つリッチなカードを、縦または横に等間隔で整列し、オプションでカード間に矢印（`->`）を描画する汎用コンポーネント。

#### 3.2.1. データモデル & クラスシグネチャ
```python
class CardListItem(BaseModel):
    """Mutable item model for a single rich card in CardList."""
    title: str
    description: str = ""
    badge_text: str | None = None
    icon: Callable[..., None] | None = None
    style: Style
    title_style: Style
    description_style: Style
    badge_style: Style | None = None
    badge_text_style: Style | None = None
    icon_style: Style | None = None
    show: bool = True


class CardList:
    """SmartArt component for rendering icon/badge-equipped feature or step cards."""

    @validate_call
    def __init__(
        self,
        *,
        style: Style = Styles.White,
        title_style: Style | None = None,
        description_style: Style | None = None,
        badge_shape: Literal["circle", "rounded_rect", "none"] = "rounded_rect",
        badge_style: Style | None = None,
        badge_text_style: Style | None = None,
        icon_style: Style | None = None,
        direction: Literal["vertical", "horizontal"] = "vertical",
        spacing: float = 2.5,
        show_arrows: bool = False,
        arrow_style: Style | None = None,
    ) -> None: ...

    @validate_call
    def add(
        self,
        title: str,
        description: str = "",
        *,
        badge_text: str | None = None,
        icon: Callable[..., None] | None = None,
        style: Style | None = None,
        title_style: Style | None = None,
        description_style: Style | None = None,
        badge_style: Style | None = None,
        badge_text_style: Style | None = None,
        icon_style: Style | None = None,
        show: bool = True,
    ) -> CardListItem: ...

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        scale: PosFloat = 1.0,
    ) -> Self: ...
```

#### 3.2.2. レイアウト・ジオメトリ仕様
- **アンカー (`xy`)**: バウンディングボックス全体の **左下座標 `(x0, y0)`**。
- **`direction="vertical"`（縦スタック）**:
  - 上から下へカードを配置。各カードの左側に `badge_shape`（丸バッジまたは角丸正方形バッジ）を配置し、`icon` が指定されていればアイコンを、`badge_text` が指定されていればテキスト（例：`"1"`, `"1.1"`, `"L1"`）を描画。
  - 右側に `title`（上段）と `description`（下段、`\n` による複数行対応）を左揃えで配置。
  - `show_arrows=True` の場合、上下のカード間に下向き矢印（`->`）を描画。
- **`direction="horizontal"`（横並びステップ）**:
  - 左から右へカードを配置。各カードの上部にアイコン／バッジ、中段に `title`、下段に `description` を中央揃えで配置。
  - `show_arrows=True` の場合、隣接カード間に右向き矢印（`->`）を自動描画（ドキュメントの Top Hero 5段階ライフサイクル図などを数行で記述可能になる）。

---

### 3.3. Component 3: `Roadmap` (`src/drawlib/_smartarts/_roadmap.py`)

水平・垂直・またはベジェ曲線のスパイン（背骨線）に沿ってマイルストーン／フェーズノードを配置し、トピックカードを展開するタイムライン・ロードマップ用コンポーネント。

#### 3.3.1. データモデル & クラスシグネチャ
```python
class RoadmapItem(BaseModel):
    """Mutable item model for a single milestone/phase node in Roadmap."""
    title: str
    subtitle: str = ""
    badge_text: str | None = None
    icon: Callable[..., None] | None = None
    card_style: Style
    title_style: Style
    subtitle_style: Style
    badge_style: Style
    badge_text_style: Style
    show: bool = True


class Roadmap:
    """SmartArt component for rendering linear timelines and curved roadmaps."""

    @validate_call
    def __init__(
        self,
        *,
        direction: Literal["vertical", "horizontal"] = "vertical",
        card_style: Style | None = None,
        title_style: Style | None = None,
        subtitle_style: Style | None = None,
        badge_style: Style | None = None,
        badge_text_style: Style | None = None,
        spine_style: Style | None = None,
        badge_palette: Sequence[Color | tuple[int, int, int]] | None = None,
        curve_bend: float = 0.0,
        card_shape: Literal["pill", "rounded_rect"] = "rounded_rect",
        alternating: bool = False,
    ) -> None: ...

    @validate_call
    def add(
        self,
        title: str,
        subtitle: str = "",
        *,
        badge_text: str | None = None,
        icon: Callable[..., None] | None = None,
        card_style: Style | None = None,
        title_style: Style | None = None,
        subtitle_style: Style | None = None,
        badge_style: Style | None = None,
        badge_text_style: Style | None = None,
        show: bool = True,
    ) -> RoadmapItem: ...

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        scale: PosFloat = 1.0,
    ) -> Self: ...
```

#### 3.3.2. レイアウト・ジオメトリ仕様
- **アンカー (`xy`)**: バウンディングボックス全体の **左下座標 `(x0, y0)`**。
- **`direction="vertical"`（垂直タイムライン／曲線アジェンダ）**:
  - `curve_bend == 0.0`（デフォルト）：垂直な直線スパインを描画し、インシデントタイムラインやリリース履歴（例：`badge_text="0h"`, `"+15m"`, `"+1h"`, `"+4h"`）として右側にカードを整列配置する。
  - `curve_bend > 0`（例：`0.12`）：二次ベジェ曲線 `line_bezier1` で滑らかな右凸アークを描画し、曲線上にバッジとピル型カードを配置する（`drawlib.slide.draw_curved_agenda` の内部エンジンとしても利用可能）。
- **`direction="horizontal"`（水平ロードマップ）**:
  - 左から右への水平タイムライン軸を描画し、各マイルストーンマーカーの上下交互（`alternating=True`）または片側にフェーズカードを配置する。

---

## 4. 関連検討項目：`GeoMap` のユーザビリティ改善案（将来検討）

今回の `GeoMap` ドッグフーディングで判明した以下の2点について、将来的に API 側で改善する場合の設計案を記録する（現時点では `_rules/lib_smartarts.md` および docstring での明記により対応済み）。

1. **`draw(width=None, height=None)` のデフォルトサイズフォールバック**:
   - 現在、`width` と `height` の両方を省略して `m.draw()` を呼ぶと `ValueError` が送出される。
   - 他の SmartArts と揃えて `width is None and height is None` の場合はデフォルト幅（例：`width=80.0`）を適用するように変更すれば、引数なしの簡易呼び出しでもエラーにならなくなる。
2. **`width` と `height` の両方 ＋ `lon_range`/`lat_range` 指定時の `viewport_mode` オプション**:
   - 現在、`width` と `height` の両方を指定すると、`background_style` は `width × height` 全体に塗られる一方、ポリゴンは `lon_range`/`lat_range` でクリップされて内側に中央寄せされるため、アスペクト比が合わないと「海（背景）の途中で大陸が垂直・水平に切り落とされる」現象が起きる。
   - 将来案として `viewport_mode: Literal["expand", "contain"] = "expand"` を導入し、`"expand"`（Matplotlib の `datalim` 相当）では指定された `lon_range`/`lat_range` の中心を維持したまま、外枠 `width / height` のアスペクト比に一致するよう経度幅または緯度幅を自動拡張してクリップすることで、どんな `lon_range`/`lat_range` を渡しても常に枠ぴったりに大陸が描画されるようにできる。

---

## 5. 実装フェーズと検証計画 (Implementation & Verification Roadmap)

### Phase 1: コア実装と単体テスト
1. `src/drawlib/_smartarts/_kpicards.py`, `_cardlist.py`, `_roadmap.py` を実装し、`src/drawlib/_smartarts/__init__.py` および `src/drawlib/smartarts.py` からエクスポートする。
2. `tests/drawlib/smartarts/` に `test_kpicards.py`, `test_cardlist.py`, `test_roadmap.py` を追加し、バリデーション・`show=False` による非表示・スケーリング（`scale`）を検証する。
3. `./dcli code-check all` および `./dcli test target smartarts` をパスさせる。

### Phase 2: ルール・ドキュメントの更新とドッグフーディング
1. `src/drawlib/_rules/lib_smartarts.md` および `src/drawlib/_rules/api.md` に `KpiCards`, `CardList`, `Roadmap` の仕様とコード例を追加する。
2. `docs/docs_src/03_smartarts/` に各コンポーネントのリファレンスページを追加し、`./dcli docs build site` とマルチモーダル視覚レビュー（`view_file`）を実施する。
