# 15. ビジュアル設計原則と本番チェックリスト

優れた技術アーキテクチャ図は、派手な色を塗り重ねるのではなく、数学的に計算された文字サイズ・落ち着いたニュートラル配色・正確な座標アンカー・再利用可能なコンポーネントマクロによって、3 秒以内にシステムの全体構造を読み手に伝達します。

最終章となる本章では、エンジニアと AI コーディングエージェントが図版・技術白書・ドキュメントサイト・API 辞書・16:9 スライドを本番公開する前に確認すべき「設計原則と最終チェックリスト」を 1 ページのリファレンスに集約します。

```drawlib align=center code=fold file=color_do_vs_dont_ja.png caption="図 15.1: 配色とコントラストの規律 — DON'T（虹色の乱用）対 DO（50%以上のニュートラル基調＋焦点ハイライト）"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=68)

# 左パネル: DON'T（原色の乱用と低コントラスト）
dont_panel = Panel(
    "DON'T: 虹色の乱用・低コントラスト",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.DangerNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.4),
    icon=phosphor.x_circle,
    icon_style=Styles.DangerBold,
    header_height=8.8,
)
dont_panel.draw((6.0, 6.0), width=70.0, height=56.0)

rectangle(
    (24.0, 42.5),
    width=25.0,
    height=11.5,
    style=Styles.AccentFlat.patch(shape_r=1.6),
    text="クライアント",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
rectangle(
    (57.0, 42.5),
    width=27.0,
    height=11.5,
    style=Styles.WarningFlat.patch(shape_r=1.6),
    text="API ゲートウェイ",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
rectangle(
    (24.0, 25.5),
    width=25.0,
    height=11.5,
    style=Styles.SuccessFlat.patch(shape_r=1.6),
    text="認証ワーカー",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
rectangle(
    (57.0, 25.5),
    width=27.0,
    height=11.5,
    style=Styles.DangerFlat.patch(shape_r=1.6),
    text="プライマリ DB",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

line((36.5, 42.5), (43.5, 42.5), arrow_head="->", style=Styles.AccentBold)
line((57.0, 36.7), (57.0, 31.3), arrow_head="->", style=Styles.DangerBold)
lines([(43.5, 39.5), (39.5, 39.5), (39.5, 25.5), (36.5, 25.5)], arrow_head="->", style=Styles.PrimaryBold)

rectangle((41.0, 12.2), width=62.0, height=7.4, style=Styles.White.patch(shape_r=1.4))
text(
    (41.0, 12.2),
    "全ノードが原色で主張し合い視覚的な主役が消失",
    style=Styles.DangerBold.patch(text_size=10.0),
)

# 右パネル: DO（50%以上のニュートラル基調＋焦点ハイライト 1 箇所）
do_panel = Panel(
    "DO: 50%以上ニュートラル＋1点ハイライト",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.4),
    icon=phosphor.check_circle,
    icon_style=Styles.PrimaryBold,
    header_height=8.8,
)
do_panel.draw((82.0, 6.0), width=70.0, height=56.0)

rectangle((117.0, 34.0), width=63.0, height=33.5, style=Styles.MutedDashed.patch(shape_r=1.8))

rectangle(
    (100.0, 42.5),
    width=25.0,
    height=11.5,
    style=Styles.White.patch(shape_r=1.6),
    text="クライアント",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
rectangle(
    (133.0, 42.5),
    width=27.0,
    height=11.5,
    style=Styles.PrimaryFlat.patch(shape_r=1.6),
    text="API ゲートウェイ",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
rectangle(
    (100.0, 25.5),
    width=25.0,
    height=11.5,
    style=Styles.SecondaryNeutral.patch(shape_r=1.6),
    text="認証ワーカー",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
rectangle(
    (133.0, 25.5),
    width=27.0,
    height=11.5,
    style=Styles.PrimaryNeutral.patch(shape_r=1.6),
    text="プライマリ DB",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

line((112.5, 42.5), (119.5, 42.5), arrow_head="->", style=Styles.DarkBold)
line((133.0, 36.7), (133.0, 31.3), arrow_head="->", style=Styles.DarkBold)
lines([(119.5, 39.5), (115.5, 39.5), (115.5, 25.5), (112.5, 25.5)], arrow_head="->", style=Styles.DarkBold)

rectangle((117.0, 12.2), width=62.0, height=7.4, style=Styles.White.patch(shape_r=1.4))
text(
    (117.0, 12.2),
    "落ち着いたニュートラル基調で主役が一目で際立つ",
    style=Styles.PrimaryBold.patch(text_size=10.0),
)

save()
```

---

## 15.1 `720pt` タイポグラフィスケールと横幅設計

Drawlib は `setup(width=W, height=H)` の論理幅にかかわらずキャンバス横幅を **`10 inch = 720 pt`** に固定して描画するため、HTML や PDF 上での実表示フォントサイズは `text_size × 表示カラム幅 / 720` で決まります。Markdown フェンスに `width=500px` や `600px` のような狭いピクセル上限を書くと画像全体が縮小され、`16px` の本文に対して図中文字だけが極端に小さくなります。ドキュメントフェンスではピクセル幅指定を必ず省略し、以下のスケール表に従ってください。

| テキスト階層 | 推奨 `text_size` | 推奨 `Styles` トークン | `~900px` カラムでの実描画サイズ |
| :--- | :--- | :--- | :--- |
| **キャンバスタイトル** | **`14.0 – 16.0`** | `Styles.DarkBold.patch(text_size=14.5)` | `~17.5px – 20.0px`（明快な図タイトル） |
| **セクション・枠見出し** | **`12.0 – 13.5`** | `Styles.DarkBold.patch(text_size=12.5)` | `~15.0px – 16.9px`（小見出しと同等） |
| **ノード・カード本文** | **`10.5 – 12.0`** | `Styles.DarkBold`（淡色上）／`Styles.WhiteBold`（`*Flat` 上） | `~13.1px – 15.0px`（`16px` 本文と調和） |
| **接続線・軸ラベル** | **`10.0`** | `Styles.Dark` または `Styles.Muted` | `~12.5px`（プロトコル・単位表記） |
| **絶対下限（目盛り・コード）** | **`9.5`（`9.5` 未満禁止）** | `Styles.Dark` / `SourceCode` | `~11.9px`（判読可能な最小限界値） |

> **16:9 スライド（`1920×1080` ステージ）での補正ルール**: スライドの本文フォントは `26px` と Web 文書（`16px`）より大きく設計されています。左右 2 カラム分割の `::: block`（`width=960..1040`）に図を配置する場合は、ノード／軸ラベルの `text_size` を **`13.5 – 15.5`**（タイトルは `16.0 – 18.5`）へ引き上げ、同時にボックス幅を `25%〜40%` 広げて本文との文字サイズ比を揃えてください。

---

## 15.2 `50%+` ニュートラル基調とコントラスト規律

プロフェッショナルな設計図は、すべての箱をカラフルに塗るのではなく、彩度を抑えた背景の中に主役だけを際立たせます。

- **図形・カードの `50%` 以上をニュートラルに保つ**: 一般のマイクロサービス・ワーカー・コンテナは `Styles.Neutral`・`Styles.PrimaryNeutral`・`Styles.SecondaryNeutral`・`Styles.White` を基調とし、VPC やクラスタ境界には `Styles.MutedDashed` を使います。
- **高彩度の `*Flat` 塗りは `1〜2` 箇所の焦点に限定**: `Styles.PrimaryFlat` や `Styles.AccentFlat` はその図で最も注目させたい中核コンポーネントだけに絞り、視線の入り口を明確にします。
- **明度コントラストの厳格なペアリング**:
  - 濃いベタ塗り（`Styles.PrimaryFlat`, `Styles.AccentFlat`, `Styles.DangerFlat`）の上には**必ず** `Styles.WhiteBold`（見出し）および `Styles.White`（補足・アイコン）を組み合わせます。
  - 淡色・ニュートラル塗り（`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.White`）の上には**必ず** `Styles.DarkBold` および `Styles.Dark` を使います（白カード上の本文を青や紫にしない）。
- **接続線は既定でニュートラル（`Styles.DarkBold`）**: 通常の処理フロー矢印には `Styles.DarkBold`（または `Styles.Dark`）を使い、`Styles.DangerBold`（異常系・ロールバック）・`Styles.SuccessBold`（正常コミット）・`Styles.PrimaryBold`（最重要クリティカルパス）は意味のある強調にのみ限定します。
- **PascalCase でのトークン読み込み**: 常に `from drawlib.styles import Colors, Styles` と大文字始まりでインポートします（小文字の `styles` / `colors` はモジュール名と衝突し `styles.py` の設定を無効化するため禁止）。

---

## 15.3 座標アンカー完全早見表（Center・Bottom-Left・Top-Left）

Drawlib のキャンバス座標系は常に**左下 `(0, 0)` 原点**（右が `+X`、上が `+Y`）ですが、各コンポーネントに渡す `xy` 引数が「中央・左下・左上」のどれを指すかはモジュール群ごとに明確に定まっています。以下の対応表を押さえることで、「半分だけ右や上へズレる」配置バグを 100% 防げます。

| アンカー種別 | 対象モジュール・クラス群 | `xy` の解釈 | 占有領域（X / Y スパン） |
| :--- | :--- | :--- | :--- |
| **中央 `Center (cx, cy)`** | `shapes.*`（`rectangle`, `circle`, `cylinder` 等）<br>`text.text()`, `icons.*`（`phosphor`, `gcp`, `aws`, `azure` 等）<br>`images.image()`<br>`smartarts.Cycle`, `smartarts.MindMapNode`<br>`diagrams.*` の `Node(..., xy=(cx, cy))` | 要素の**幾何学的中心** | `x: [cx - w/2, cx + w/2]`<br>`y: [cy - h/2, cy + h/2]` |
| **左下 `Bottom-Left (x0, y0)`** | `charts.*`（全 10 種の定量チャート）<br>`diagrams.*` の `d.draw(xy=(x0, y0))` & `NodeGroup(..., xy=(x0, y0))`<br>大半の `smartarts.*`（`BoxList`, `CardList`, `ChevronProcess`, `GridLayout`, `Pyramid`, `KpiCards`, `Roadmap`, `Panel`, `GeoMap`, `*Calendar`） | 領域の**左下隅**（右・上へ伸長）。幅 `W` のキャンバス中央配置は `x0 = (W - width) / 2` | `x: [x0, x0 + width]`<br>`y: [y0, y0 + height]` |
| **左上 `Top-Left (x0, y_top)`** | `smartarts.Table`<br>`smartarts.TreeNode`<br>`smartarts.BulletPoints`<br>`smartarts.SourceCode` | 領域の**左上隅**（行やツリー枝が `y = 0` に向かって**下方向へ伸長**） | `x: [x0, x0 + width]`<br>`y: [y_top - height, y_top]` |
| **両方保持（`get_layout()`）** | `graph.*`（`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`） | 自動計算されたレイアウト結果が中心と左下の両プロパティを提供 | `.xy` / `.local_xy`（中央）<br>`.bottom_left` / `.local_bottom_left`（左下） |

```drawlib align=center code=fold file=anchor_cheatsheet_visual_ja.png caption="図 15.2: 座標アンカー視覚早見表 — 中央 (cx, cy)・左下 (x0, y0)・左上 (x0, y_top)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=70)

# カード 1: 中央アンカー Center (cx, cy)
p1 = Panel(
    "1. 中央 (cx, cy)",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.2),
    icon=phosphor.crosshair,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
p1.draw((6.0, 6.0), width=46.0, height=58.0)

text((29.0, 51.5), "基準点: 中央 (cx, cy)", style=Styles.PrimaryBold.patch(text_size=10.2))
rectangle((29.0, 41.0), width=28.0, height=13.0, style=Styles.White.patch(shape_r=1.5))
line((15.0, 41.0), (43.0, 41.0), style=Styles.MutedDashed)
line((29.0, 34.5), (29.0, 47.5), style=Styles.MutedDashed)
circle((29.0, 41.0), radius=2.3, style=Styles.PrimaryOutlineBold)
circle((29.0, 41.0), radius=1.3, style=Styles.PrimaryFlat)

line((10.5, 29.0), (47.5, 29.0), style=Styles.Muted)
text(
    (29.0, 17.5),
    "• shapes.* & text()\n• icons.* & images.*\n• Cycle & MindMapNode\n• Diagram Node(xy=...)",
    style=Styles.Dark.patch(text_size=10.0),
)

# カード 2: 左下アンカー Bottom-Left (x0, y0)
p2 = Panel(
    "2. 左下 (x0, y0)",
    style=Styles.PrimaryNeutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.2),
    icon=phosphor.corners_out,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
p2.draw((56.0, 6.0), width=46.0, height=58.0)

rectangle((79.0, 43.5), width=28.0, height=13.0, style=Styles.White.patch(shape_r=1.5))
rectangle((71.5, 40.5), width=4.2, height=5.0, style=Styles.SecondaryNeutral)
rectangle((79.0, 42.5), width=4.2, height=9.0, style=Styles.PrimaryNeutral)
rectangle((86.5, 41.5), width=4.2, height=7.0, style=Styles.SecondaryNeutral)
line((65.0, 37.0), (94.8, 37.0), arrow_head="->", style=Styles.DarkBold)
line((65.0, 37.0), (65.0, 51.8), arrow_head="->", style=Styles.DarkBold)
circle((65.0, 37.0), radius=1.6, style=Styles.AccentFlat)
text((79.0, 32.5), "基準点: 左下隅 (x0, y0)", style=Styles.DarkBold.patch(text_size=10.2))

line((60.5, 29.0), (97.5, 29.0), style=Styles.Muted)
text(
    (79.0, 17.5),
    "• 全 10 種の Charts\n• Diagrams draw(xy=...)\n• ChevronProcess, Panel\n• CardList, KpiCards",
    style=Styles.Dark.patch(text_size=10.0),
)

# カード 3: 左上アンカー Top-Left (x0, y_top)
p3 = Panel(
    "3. 左上 (x0, y_top)",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.2),
    icon=phosphor.squares_four,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
p3.draw((106.0, 6.0), width=46.0, height=58.0)

text((129.0, 51.5), "基準点: 左上隅 (x0, y_top)", style=Styles.PrimaryBold.patch(text_size=10.2))
rectangle((129.0, 40.0), width=28.0, height=13.0, style=Styles.White.patch(shape_r=1.5))
rectangle((129.0, 44.5), width=28.0, height=4.0, style=Styles.PrimaryNeutral)
line((115.0, 38.0), (143.0, 38.0), style=Styles.Muted)
line((115.0, 46.5), (144.8, 46.5), arrow_head="->", style=Styles.DarkBold)
line((115.0, 46.5), (115.0, 32.0), arrow_head="->", style=Styles.DarkBold)
circle((115.0, 46.5), radius=1.6, style=Styles.PrimaryFlat)

line((110.5, 29.0), (147.5, 29.0), style=Styles.Muted)
text(
    (129.0, 17.5),
    "• Table\n• TreeNode\n• BulletPoints\n• SourceCode",
    style=Styles.Dark.patch(text_size=10.0),
)

save()
```

---

## 15.4 再利用マクロと多言語テーマ設計（`utils.py` & `styles.py`）

プロジェクト内の図版が 5 枚を超えた段階で、カード寸法やサブタイトル位置・日本語フォント指定を各 Markdown ブロックへコピー＆ペーストし始めると保守性が急速に低下します。以下の 2 ファイルへ責務を分離して **DRY（Don't Repeat Yourself）** を徹底してください。

- **`styles.py` と `<lang>/styles.py`（テーマ・言語別フォントの上書き）**: ルートの `styles.py` で `Colors = GoogleColors()` と `Styles = GoogleStyles()` を定義し、日本語図版向けのフォント設定（`Styles = GoogleStyles().patch_font(regular=FontJapanese.SANSSERIF_REGULAR, bold=FontJapanese.SANSSERIF_BOLD)`）は `ja/styles.py` に分離します。`styles.py` は `.drawlib/cache.db` のハッシュ対象に含まれるため、配色変更時は関連図版が自動で再描画されます。
- **`utils.py`（チーム共通の描画マクロ関数）**: `service_card()` やラベル付き `connect()` のような定型パーツを `utils.py` に定義し、各章から `from drawlib.utils import connect, service_card` で呼び出します。

```python
# 各章ブロックやスクリプト内 — utils.py と styles.py の共通マクロを再利用
from drawlib.canvas import save, setup
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=128, height=42)

# 共通マクロで焦点ノード 1 個＋ニュートラル補助ノードを簡潔に描画
service_card((26, 21), "Ingress Proxy", "Envoy :443", width=32, height=18, style=Styles.PrimaryFlat)
service_card((96, 21), "Billing API", "Python / gRPC", width=32, height=18, style=Styles.SecondaryNeutral)
connect((42, 21), (80, 21), label="mTLS gRPC", style=Styles.DarkBold)

save()
```

---

## 15.5 本番リリース前の最終チェックリスト

プルリクエストのマージや成果物の配布前に、以下の 5 項目を満たしているか最終確認を行ってください。

- [ ] **1. 相対リンクとアセットパスの衛生管理**: 章間リンク（`02_architecture.md`, `../01_intro/index.md`）や画像参照（Markdown 本文からは `../_assets/logo.png`、`drawlib` Python コード内からは `"_assets/logo.png"`）がすべてポータブルな相対パスで書かれていること。ローカル URI スキームや `/abs/local/path`・`C:\local\path` のような環境依存の絶対パスが一切含まれていないこと（混入時は `drawlib build` がエラーで拒否します）。
- [ ] **2. キャンバス外周マージン（`4〜6` 単位以上）とグリッド確認（`-g`）**: 変更したすべての図版を `drawlib show ... -g --no-cache` で出力して視覚確認し、上下左右の端から `4〜6` 座標単位以上の余白があること・文字のはみ出しや重なりがゼロであること・`text_size >= 10.0` であることを確認済みであること。
- [ ] **3. `50%+` ニュートラル配色と Top Hero 配置**: ノードやカードの半数以上がニュートラル系（`Neutral`, `PrimaryNeutral`, `SecondaryNeutral`, `White`）で統一され、`*Flat` 焦点ノードには `WhiteBold` が組み合わされていること。各ページの **5〜15 行目に `code=fold` の Top Hero 図**があり、ページあたり `2` 図以上を含むこと。
- [ ] **4. 多言語（`i18n`）スケルトン整合性**: 多言語プロジェクト（`langs = ["en", "ja"]` 等）では、全言語で相対ファイル構成・`#` / `##` / `###` 見出し順序・コードブロック順序が完全一致し、翻訳図版に `<stem>_<lang>.png` が付与されていること。
- [ ] **5. 自動リンク検査とマルチ形式出力の確認**: `./<target>_src/build.sh` と `uv run drawlib serve <target>_html/ --check` が終了コード `0` で通過し、`1280×920` ブラウザ表示でのファーストビューと文字サイズ整合、`PDF` / `.docx` / `.pptx` の改ページ品質を確認の上、一時ファイル（`.drawlib/scratch/`）を削除済みであること。
