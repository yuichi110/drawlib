# Drawlib パッケージ概要

Drawlib は **Illustration as Code**（コードとしての図解）および **Illustrated Documentation as Code**（図解入りドキュメントのコード管理）を実現する純粋 Python ライブラリです。`import drawlib` 配下に 20 個の遅延ロード対応トップレベルサブモジュール（`PEP 562`）と、`drawlib.charts`・`drawlib.diagrams` サブパッケージを公開しています。各機能は `from drawlib.<module> import ...` で直接インポートできます。

```drawlib align=center code=fold file=00_overview_hero.png caption="Drawlib 統合 Python パッケージ構成 (import drawlib)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=58, dpi=150)

# Outer package frame
rectangle((60, 29), width=112, height=50, style=Styles.MutedDashed.patch(shape_r=2.5))
phosphor.package((38.0, 48.5), width=4.4, style=Styles.DarkBold)
text(
    (63.5, 48.5),
    "Drawlib Package Architecture (v0.3.5)",
    style=Styles.DarkBold.patch(text_size=12.5),
)

# 1. Core Primitives & Styling
rectangle((23.5, 24), width=31, height=34, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.shapes((12.5, 35.5), width=4.2, style=Styles.DarkBold)
text((25.5, 35.5), "Core Primitives", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (23.5, 21.5),
    "canvas / shapes\nlines / text / images\nmath / styles / fonts",
    style=Styles.Dark.patch(text_size=10.0, text_line_spacing=1.35),
)

line((39.0, 24), (44.0, 24), arrow_head="->", style=Styles.DarkBold)

# 2. High-Level Components (Focal Hero)
rectangle((60, 24), width=32, height=34, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.graph((48.5, 35.5), width=4.2, style=Styles.WhiteBold)
text((62.0, 35.5), "High-Level API", style=Styles.WhiteBold.patch(text_size=11.5))
text(
    (60, 21.5),
    "smartarts / charts\ndiagrams / graph\nicons (34 suites)",
    style=Styles.White.patch(text_size=10.0, text_color=Colors.White, text_line_spacing=1.35),
)

line((76.0, 24), (81.0, 24), arrow_head="->", style=Styles.DarkBold)

# 3. Docs, Animation & CLI
rectangle((96.5, 24), width=31, height=34, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.terminal_window((86.0, 35.5), width=4.2, style=Styles.DarkBold)
text((98.5, 35.5), "Docs & CLI", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (96.5, 21.5),
    "anim / slide / tools\ndrawlib build & show\nHTML / PDF / PPTX",
    style=Styles.Dark.patch(text_size=10.0, text_line_spacing=1.35),
)

save()
```

### パッケージ・サブパッケージの再エクスポート一覧 (`__all__`)

Drawlib は `PEP 562` に基づく遅延モジュールロードを採用しており、`import drawlib` 時の起動オーバーヘッドを最小化しつつ、`dir()` や静的型チェッカーからすべての公開サブモジュールを参照できます。

| パッケージ名前空間 | 再エクスポートされるサブモジュール (`__all__`) |
| :--- | :--- |
| `drawlib` | `anim`, `canvas`, `charts`, `diagrams`, `fonts`, `graph`, `icons`, `images`, `lines`, `math`, `preset_colors`, `preset_styles`, `shapes`, `slide`, `smartarts`, `styles`, `text`, `tools`, `types`, `utils` |
| `drawlib.charts` | `area`, `bar`, `gantt`, `heatmap`, `line`, `pie`, `radar`, `scatter`（および共通型エイリアス `DrawDirection`） |
| `drawlib.diagrams` | `architecture`, `class_diagram`, `er`, `flow`, `sequence`, `state` |

### 全モジュール・CLI リファレンス一覧（全 29 ページ）

| ページ | 対象モジュール | 主な収録内容 |
| :--- | :--- | :--- |
| [00. Drawlib パッケージ概要](00_overview.md) | `drawlib`, `drawlib.utils`, `drawlib.charts`, `drawlib.diagrams` | パッケージ定数、遅延ロード一覧、`drawlib.utils`、`DrawDirection` |
| [01. drawlib.canvas](01_canvas.md) | `drawlib.canvas` | 左下原点 `(0, 0)` キャンバスのライフサイクル（`setup`, `save`, `clear`, `show`, `get_dimage`, `canvas`） |
| [02. drawlib.shapes](02_shapes.md) | `drawlib.shapes` | 基本図形・ブロック矢印・3D コンテナ・バッジ・記号など全 43 シェイプ関数 |
| [03. drawlib.lines & drawlib.text](03_lines_and_text.md) | `drawlib.lines`, `drawlib.text` | 直線・円弧・ベジェ曲線・角丸ポリライン描画と横書き・縦書きテキスト |
| [04. drawlib.images & drawlib.math](04_images_and_math.md) | `drawlib.images`, `drawlib.math` | `image()`、不変 `Dimage` 画像変換、`get_dimage_from_code()`、2D 幾何計算 |
| [05. drawlib.styles & drawlib.types](05_styles_and_types.md) | `drawlib.styles`, `drawlib.types` | アクティブ `Styles` / `Colors`、不変 `Style`・`Color` モデル、型エイリアス |
| [06. drawlib.preset_styles & preset_colors](06_presets.md) | `drawlib.preset_styles`, `drawlib.preset_colors` | `DefaultStyles`、`GoogleStyles`、`MonochromeStyles`、`CssColors` 等のプリセット |
| [07. drawlib.fonts](07_fonts.md) | `drawlib.fonts` | 環境非依存の標準フォント群（`Font`、日本語・多言語フォント、`FontFile`） |
| [08. drawlib.icons](08_icons.md) | `drawlib.icons` | 全 34 アイコンスイート（`phosphor`, `gcp`, `aws`, `azure`, ドメイン別アイコン） |
| [09. drawlib.smartarts（リスト・カード・テーブル）](09_smartarts_lists_cards.md) | `drawlib.smartarts` | `Table`, `BoxList`, `CardList`, `KpiCards`, `BulletPoints`, `Panel`, `SourceCode`, `GridLayout` |
| [10. drawlib.smartarts（フロー・ツリー・マップ）](10_smartarts_flows_trees_maps.md) | `drawlib.smartarts` | `ChevronProcess`, `Cycle`, `Pyramid`, `Roadmap`, `TreeNode`, `MindMapNode`, `GeoMap`, `*Calendar` |
| [11. drawlib.charts.bar](11_charts_bar.md) | `drawlib.charts.bar` | 集合・積み上げ・横向き対応の棒グラフ `BarChart` |
| [12. drawlib.charts.line](12_charts_line.md) | `drawlib.charts.line` | 複数系列・マーカー・閾値線対応の折れ線グラフ `LineChart` |
| [13. drawlib.charts.area](13_charts_area.md) | `drawlib.charts.area` | 積み上げ・重ね合わせ対応の面グラフ `AreaChart` |
| [14. drawlib.charts.pie](14_charts_pie.md) | `drawlib.charts.pie` | 円グラフ・ドーナツグラフ `PieChart` |
| [15. drawlib.charts.radar](15_charts_radar.md) | `drawlib.charts.radar` | 多軸レーダーチャート `RadarChart` |
| [16. drawlib.charts.scatter](16_charts_scatter.md) | `drawlib.charts.scatter` | 散布図・バブルチャート `ScatterChart` |
| [17. drawlib.charts.gantt](17_charts_gantt.md) | `drawlib.charts.gantt` | スケジュール・マイルストーン・依存関係を表す `GanttChart` |
| [18. drawlib.charts.heatmap](18_charts_heatmap.md) | `drawlib.charts.heatmap` | マトリクス `HeatmapChart` と空間サーマルオーバーレイ `HeatmapOverlay` |
| [19. drawlib.diagrams.architecture](19_diagrams_architecture.md) | `drawlib.diagrams.architecture` | クラウド・マイクロサービス構成図 `ArchitectureDiagram` |
| [20. drawlib.diagrams.flow](20_diagrams_flow.md) | `drawlib.diagrams.flow` | フローチャート・スイムレーン図 `FlowDiagram` |
| [21. drawlib.diagrams.sequence](21_diagrams_sequence.md) | `drawlib.diagrams.sequence` | シーケンス図 `SequenceDiagram`（ライフライン・複合フラグメント・ノート） |
| [22. drawlib.diagrams.class_diagram](22_diagrams_class.md) | `drawlib.diagrams.class_diagram` | UML クラス図 `ClassDiagram` |
| [23. drawlib.diagrams.er](23_diagrams_er.md) | `drawlib.diagrams.er` | ER データベース設計図 `ERDiagram` |
| [24. drawlib.diagrams.state](24_diagrams_state.md) | `drawlib.diagrams.state` | ステートマシン図 `StateDiagram` |
| [25. drawlib.graph](25_graph.md) | `drawlib.graph` | 5 種の決定論的自動レイアウトソルバー（`get_layout()`） |
| [26. drawlib.anim & drawlib.slide](26_anim_and_slide.md) | `drawlib.anim`, `drawlib.slide` | マルチフレーム WebP `Animation` と 16:9 スライド `SlideDeck` / `.pptx` 出力 |
| [27. drawlib.tools](27_tools.md) | `drawlib.tools` | プロジェクトビルド・キャッシュ管理・プレビューサーバー・ルール取得 API |
| [28. CLI リファレンス (drawlib)](28_cli.md) | `drawlib._cli` | コマンドラインツール（`init`, `build`, `show`, `serve`, `cache`, `rules`） |

---

## `const` __version__

`drawlib.__version__` として公開される標準 PEP 396 パッケージバージョン文字列（`LIB_VERSION` のエイリアス）です。

```python
from drawlib import __version__

__version__: Final[str] = "0.3.5"
```

| 定数名 | 型 | 値 | 説明 |
| :--- | :--- | :--- | :--- |
| `__version__` | `Final[str]` | `'0.3.5'` | インストールされている Drawlib のセマンティックバージョン文字列。 |

---

## `const` LIB_NAME

`drawlib.LIB_NAME` として公開される正規パッケージ識別子定数です。

```python
from drawlib import LIB_NAME

LIB_NAME: Final[str] = "drawlib"
```

| 定数名 | 型 | 値 | 説明 |
| :--- | :--- | :--- | :--- |
| `LIB_NAME` | `Final[str]` | `'drawlib'` | メタデータ・キャッシュ管理・CLI 表示で使用される正規ライブラリ名。 |

---

## `const` LIB_VERSION

`drawlib.LIB_VERSION` として公開されるセマンティックバージョン定数です。

```python
from drawlib import LIB_VERSION

LIB_VERSION: Final[str] = "0.3.5"
```

| 定数名 | 型 | 値 | 説明 |
| :--- | :--- | :--- | :--- |
| `LIB_VERSION` | `Final[str]` | `'0.3.5'` | `drawlib.__version__` と同一のセマンティックバージョン文字列。 |

---

## `type` drawlib.utils

プロジェクト内の `utils.py`（または `drawlib show -u <path>` で指定したファイル）で定義されたトップレベル関数・クラス・定数がビルド／描画時に自動注入される動的ユーティリティ名前空間モジュール（`import drawlib.utils` または `from drawlib import utils`）です。

```python
# プロジェクトの utils.py 側:
# def service_card(xy: tuple[float, float], title: str) -> None: ...

from drawlib import utils

utils.service_card((60, 30), "API Gateway")
```

| 挙動・属性 | 型 | 説明 |
| :--- | :--- | :--- |
| `drawlib.utils.<name>` | `Any` | `utils.py` から読み込まれた任意のヘルパー関数・クラス・定数を解決します。 |
| 未定義属性へのアクセス | `AttributeError` | `utils.py` での定義方法および `--utils` オプションの案内を含む `AttributeError` を送出します。 |

---

## `type` drawlib.charts.DrawDirection

`drawlib.charts` から公開される共通リテラル型エイリアスで、チャート要素（`BarChart`、`LineChart`、`AreaChart` など）の段階的描画や伸長方向を指定します。

```python
from typing import Literal
from drawlib.charts import DrawDirection

DrawDirection = Literal["bottom_to_top", "left_to_right"]
```

| 指定可能なリテラル値 | 説明 |
| :--- | :--- |
| `'bottom_to_top'` | 下端（`y0`）から上方向へ向けてチャート要素を描画・伸長します。 |
| `'left_to_right'` | 左端（`x0`）から右方向へ向けてチャート要素を描画・伸長します。 |
