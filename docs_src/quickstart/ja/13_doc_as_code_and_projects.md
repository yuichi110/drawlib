# 13. Documentation as Code と 5つのプロジェクト種別

単体のアーキテクチャ図をコードで描けるだけでは、実務のドキュメント運用課題の半分しか解決できません。実際の開発組織では、設計図は複数章からなる技術設計書・検索可能な API ポータル・RFC 白書・経営層向けスライドの内部に組み込まれ、多言語や多様な配布形式の間で常に整合性を保つ必要があります。

Drawlib は **Illustration as Code** をさらに発展させた **Illustrated Documentation as Code** を実現します。純粋 Python による作図コードと Markdown 原稿を単一の Git リポジトリで一元管理し、静的 HTML サイト・A4 ベクター PDF・編集可能な Microsoft Word（`.docx`）仕様書・16:9 HTML/PDF スライド・ネイティブ PowerPoint（`.pptx`）・アニメーション画像群へと決定論的に一括コンパイルします。

```drawlib align=center code=fold file=five_project_archetypes_ja.png caption="図 13.1: 単一の Git リポジトリから 5 つのプロジェクト種別へ展開する Drawlib の全体像 (v0.3.10)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=74)

text(
    (79.0, 68.2),
    "Drawlib v0.3.10 — 単一の Git ソースから展開する 5 つのプロジェクト種別",
    style=Styles.DarkBold.patch(text_size=12.8),
)

# 左側の焦点ハブ（PrimaryFlat は 1 箇所のみ）
rectangle((24.0, 34.5), width=34.0, height=55.0, style=Styles.PrimaryFlat.patch(shape_r=2.2))
phosphor.git_branch((24.0, 55.0), width=5.6, style=Styles.WhiteBold)
text((24.0, 46.2), "Git 単一情報源\n(<target>_src/)", style=Styles.WhiteBold.patch(text_size=11.5))
line((11.0, 39.8), (37.0, 39.8), style=Styles.White)
text(
    (24.0, 23.2),
    "• drawlib.toml\n• styles.py\n• <lang>/styles.py\n• utils.py\n• _assets/\n• build.sh",
    style=Styles.White.patch(text_size=10.2),
)

# 右側 3 段への直交バス接続
line((41.0, 34.5), (47.5, 34.5), style=Styles.DarkBold)
lines([(47.5, 34.5), (47.5, 53.5), (53.0, 53.5)], arrow_head="->", style=Styles.DarkBold)
line((47.5, 34.5), (53.0, 34.5), arrow_head="->", style=Styles.DarkBold)
lines([(47.5, 34.5), (47.5, 15.5), (53.0, 15.5)], arrow_head="->", style=Styles.DarkBold)

# 1段目: images & doc（ニュートラル基調カード）
rectangle((76.5, 53.5), width=47.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.images((58.0, 57.5), width=4.6, style=Styles.PrimaryBold)
text((79.5, 57.5), "1. images — 単体図解群", style=Styles.DarkBold.patch(text_size=11.0))
text((76.5, 49.3), "*.py -> PNG / WebP / GIF / PDF / SVG", style=Styles.Dark.patch(text_size=10.0))

rectangle((128.5, 53.5), width=47.0, height=16.5, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.file_pdf((110.0, 57.5), width=4.6, style=Styles.PrimaryBold)
text((131.5, 57.5), "2. doc — 技術白書・仕様書", style=Styles.DarkBold.patch(text_size=11.0))
text((128.5, 49.3), "<lang>/*.md -> HTML / A4 PDF / DOCX", style=Styles.Dark.patch(text_size=10.0))

# 2段目: site & catalog
rectangle((76.5, 34.5), width=47.0, height=16.5, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.globe((58.0, 38.5), width=4.6, style=Styles.SecondaryBold)
text((79.5, 38.5), "3. site — ドキュメントサイト", style=Styles.DarkBold.patch(text_size=11.0))
text((76.5, 30.3), "navbar.md -> 階層 HTML / 検索 / PDF", style=Styles.Dark.patch(text_size=10.0))

rectangle((128.5, 34.5), width=47.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.brackets_curly((110.0, 38.5), width=4.6, style=Styles.SecondaryBold)
text((132.0, 38.5), "4. catalog — API 辞書", style=Styles.DarkBold.patch(text_size=11.0))
text((128.5, 30.3), "# H1・## GET -> 2列 UI + / 即時検索", style=Styles.Dark.patch(text_size=10.0))

# 3段目: slide（ワイドカード）
rectangle((102.5, 15.5), width=99.0, height=16.5, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.presentation_chart((61.0, 19.5), width=4.8, style=Styles.PrimaryBold)
text((104.5, 19.5), "5. slide — 16:9 ワイドスクリーンプレゼンテーション", style=Styles.DarkBold.patch(text_size=11.2))
text(
    (102.5, 11.3),
    "1920x1080 ::: block & ::: note -> Web スライド / 16:9 PDF / 編集可能 PPTX",
    style=Styles.Dark.patch(text_size=10.2),
)

save()
```

---

## 13.1 プロジェクトファースト原則（`drawlib init project`）

1 枚のシステム構成図を描く場合でも、複数章の技術マニュアルを構築する場合でも、Drawlib では必ず**プロジェクトファースト原則（Project-First Rule）**に従います。空のディレクトリに裸の `.py` スクリプトを直接置いたり手作業でフォルダを作ったりせず、まず `drawlib init project` で `<target>_src/` プロジェクトを自動生成します。

最初にプロジェクトの骨格を生成することで、以下の 5 つのエンジニアリング基盤が即座に整います。

- **統一マニフェスト（`drawlib.toml`）**: プロジェクト種別（`images` / `doc` / `site` / `catalog` / `slide`）・ビジュアルテーマ（`default` / `google` / `monochrome`）・多言語 `[i18n]` 設定・`[seo]` メタデータを 1 ファイルで宣言的に管理します。
- **テーマと CJK フォントの一元管理（`styles.py` & `<lang>/styles.py`）**: `-l ja` や `-l en,ja` を指定するだけで、`FontJapanese` などの日本語フォント設定と配色トークンが自動構成され、各図でフォント指定を繰り返す必要がなくなります。
- **DRY な再利用マクロ（`utils.py`）**: `utils.py` に定義した関数や定数はすべての図から `from drawlib.utils import <helper>` で呼び出せ、数十ページにわたるカード形状や接続線のスタイルを完全に統一できます。
- **ポータブルな静的アセット管理（`_assets/`）**: `_assets/favicon.png` が初期配置され、社内ロゴやカスタム `.ttf` フォントを相対パスで安全に参照・SHA-256 キャッシュ追跡できます。
- **再現可能なワンコマンドビルド（`build.sh` & `build_*.sh`）**: 編集対象の信頼できる唯一の情報源（`<target>_src/`）と、読み取り専用の生成物ディレクトリを厳格に分離したビルドスクリプト群が自動生成されます。

5 つのプロジェクト種別はいずれも `drawlib init project <type> [target] -l <langs> -s <style>` で初期化できます（初期化後はサンプル用の `sample*.py` を削除または置き換えて運用します）。

```bash
# 利用可能な 5 つのスターターテンプレート一覧を確認
uv run drawlib init project list

# 1. 単体 Python 図解・アニメーション管理プロジェクト (images_src/)
uv run drawlib init project images diagrams -l ja -s google

# 2. 日英バイリンガルの技術白書・仕様書 -> HTML + A4 PDF + MS Word (.docx)
uv run drawlib init project doc whitepaper -l en,ja -s google

# 3. サイドバー付きマルチページ・ドキュメントポータル (docs_src/)
uv run drawlib init project site docs -l en,ja -s default

# 4. 検索可能な API / CLI / スキーマリファレンス辞書 (catalog_src/)
uv run drawlib init project catalog api_ref -l en,ja -s google

# 5. 日英バイリンガル 16:9 プレゼンスライド -> HTML + PDF + PowerPoint (.pptx)
uv run drawlib init project slide pitch -l en,ja -s google
```

---

## 13.2 Markdown 埋め込み作図ブロックと 720pt タイポグラフィ整合

`doc`・`site`・`catalog`・`slide` プロジェクトの Markdown 原稿（`<target>_src/<lang>/**/*.md`）では、`drawlib` コードフェンスを使って Python 作図コードを本文中に直接埋め込みます。ビルド時に各ブロックは独立したキャンバス状態で実行され、`.drawlib/cache.db` にキャッシュされた上でレスポンシブな図表要素へと変換されます。

````markdown
```drawlib align=center code=fold file=gateway_flow_ja.png caption="図 13.3: リージョナル API ゲートウェイの基本構成"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=136, height=44)

rectangle((28, 22), width=32, height=18, style=Styles.Neutral, text="クライアント")
rectangle(
    (68, 22),
    width=32,
    height=18,
    style=Styles.PrimaryFlat,
    text="API ゲートウェイ",
    text_style=Styles.WhiteBold,
)
rectangle((108, 22), width=32, height=18, style=Styles.SecondaryNeutral, text="認証サービス")

line((44, 22), (52, 22), arrow_head="->", style=Styles.DarkBold)
line((84, 22), (92, 22), arrow_head="->", style=Styles.DarkBold)
save()
```
````

埋め込み `drawlib` フェンスでは、以下の 4 つのヘッダ属性で出力ファイル名・配置・コード表示モードを制御します。

| フェンス属性 | 指定可能な値 | 推奨される使い分け |
| :--- | :--- | :--- |
| **`file=`** | `<stem>.png` / `.webp` / `.svg` | **必須。** 出力画像名を明示します（言語共通図は `file=arch.png`、日本語ローカライズ図は `file=arch_ja.png`）。`drawlib show <md> <file>` での個別検証にも使われます。 |
| **`caption=`** | `"図 X.Y: ..."` | **文書では必須。** HTML/PDF では `<figcaption>`、Word（`.docx`）では図キャプション段落として出力されます。 |
| **`align=`** | `center` \| `left` \| `right` | 本文カラム内での水平配置を指定します（標準は `align=center`）。 |
| **`code=`** | `hide` \| `fold` \| `show` | `code=hide`（既定）は図のみを表示する白書・仕様書向け、`code=fold` は図の直下に折りたたみ `<details>` でコードを格納（**5〜15行目の Top Hero 図で必須**）、`code=show` はコードと図を両方展開する入門解説向けです。 |

### ピクセル幅指定（`width=...px`）を省略すべき数学的理由（`720pt` 法則）

Drawlib の描画エンジンは、`setup(width=W, height=H)` の論理幅 `W` が `100` でも `160` でも、画像全体の物理幅を常に **`10 inch = 720 pt`** に正規化して出力します。この画像が HTML 本文カラム（幅 $W_{\text{HTML}}$、通常 `880px〜960px`）に表示されるとき、図中の `text_size`（単位 `pt`）は以下の画面ピクセルサイズで描画されます。

$$\text{画面上の描画文字サイズ (px)} = \text{text\_size} \times \frac{W_{\text{HTML}}}{720}$$

- **ピクセル幅上限を省略した場合（カラム幅 `100%` ≒ `900px`）**: `text_size=11.0` は `11.0 × 900 / 720 = 13.75px` となり、`16px` の HTML 本文や A4 PDF の本文フォントと美しく調和します。
- **狭いピクセル幅を指定した場合（`width=500px` / `600px` — 禁止）**: 画像が `500px` に縮小されると `text_size=11.0` がわずか `7.6px` に潰れ、単体 PNG では読めた文字が Web や PDF 上で判読不能になります。フェンスにはピクセル幅を指定せず、常に `text_size >= 10.0` を維持してください。

---

## 13.3 5つのプロジェクト種別の徹底比較

Drawlib `v0.3.10` は用途に応じた 5 つのプロジェクト種別を備えています。Markdown ベースの 4 種別（`doc`・`site`・`catalog`・`slide`）はすべて共通の `<target>_src/<lang>/` ディレクトリ構造を採用しているため、`git mv` でファイルを移動することなく後からいつでも対応言語を追加できます。

| 種別 | ソース構成 | ナビゲーション・構造 | 生成される成果物 | 主なエンジニアリング用途 |
| :--- | :--- | :--- | :--- | :--- |
| **`images`** | `images_src/*.py` | 単体／階層 Python スクリプト・AST 重複出力検査 | `.png`（`APNG` 含む）・`.webp`・`.gif`・`.pdf`・`.svg` | 構成図アセット集、README 図版、CI チャート生成、プロトコル解説アニメーション |
| **`doc`** | `doc_src/<lang>/*.md` (`00_cover.md`, `01_*`...) | ファイル名順の章結合＋`--generate-index` 目次自動挿入（`navbar.md` 不要） | 単一ページ `HTML` 本・A4 ベクター `PDF`・編集可能 Word `.docx`・GitHub `MD` | 技術 RFC、アーキテクチャ白書、オンボーディング教本、印刷用設計書、Word レビュー文書 |
| **`site`** | `docs_src/<lang>/**/*.md` + `<lang>/navbar.md` | `navbar.md` による階層サイドバー・ダークモード・検索 | マルチページ `HTML` ポータル・個別 `PDF`・GitHub `MD`・`llms.txt` | プロダクト公式ドキュメント、開発者ポータル、複数チームの設計 Wiki |
| **`catalog`** | `catalog_src/<lang>/*.md` *(自動インデックス)* | `# H1` カテゴリ＆`## H2` 項目の固定 2 ペイン UI＋`/` 即時ライブ検索 | 2 カラム検索対応 `HTML` 辞書・GitHub `MD`・`llms.txt` | REST/gRPC API 辞書、CLI オプション辞典、イベント／メトリクス一覧、DB スキーマ定義書 |
| **`slide`** | `slide_src/<lang>/*.md` (`01_title.md`...) | `1920×1080` `::: block` ステージ＋`::: note` 台本＋発表者ビュー | `16:9` 対話型 `HTML` スライド・`16:9` ベクター `PDF`・編集可能 `.pptx` | 技術カンファレンス登壇資料、アーキテクチャ審査会、スプリントデモ、顧客提案スライド |

実務で使い分ける際の各アーキタイプの特徴は以下の通りです。

1. **`images`（単体図解・アニメーション集）**: `save()` を呼ぶ各 `*.py` スクリプトから `<script_stem>.png`（`Animation()` 使用時は `.webp` / `.gif` 等も対応）を一括生成します。実行前に Python の `ast` モジュールで全スクリプトを静的解析し、出力ファイル名の衝突があれば実行前に即座にエラー停止します。1 スクリプト内で複数画像を出力する場合は、次の `setup()` の前に必ず `clear()` を呼びます。
2. **`doc`（章立て技術白書・A4 PDF・Word `.docx`）**: 番号付き章ファイル（`00_cover.md`, `01_overview.md`, ...）を辞書順に結合し、改ページ（`--page-break`）と多言語対応の自動目次（`--generate-index`）を `00_cover.md` の直後に挿入します。標準の `./doc_src/build.sh`（`HTML` + A4 `PDF`）に加え、`./doc_src/build_docx.sh`（`drawlib build docx`）を実行すればネイティブ編集可能な Word 文書（`.docx`）を出力できます。
3. **`site`（マルチページ・ドキュメントポータル）**: `<lang>/navbar.md` の定義に従い、階層化された Markdown 群をライト／ダークモード切り替え・多言語スイッチャー・シンタックスハイライト付きの Web ポータルへ変換します（内部 `.md` リンクは自動で `.html` に書き換えられます）。
4. **`catalog`（検索可能な API・スキーマリファレンス辞書）**: 手動の `navbar.md` 管理を不要にした `1 Markdown = 1 HTML ページ` 構成です。各ファイルの `# H1` が左サイドバーのアコーディオン項目、すべての `## H2` がスクロール連動 `#slug` リンクとなり、`/` キーによる即時インクリメンタルフィルタと意味別カラーバッジ（HTTP メソッド `` ## `GET` /v1/users/<id> ``、コード要素 `` ## `def` setup() ``、基盤要素 `` ## `service` auth-api ``・`` ## `table` accounts ``・`` ## `cmd` drawlib build `` など）を自動レンダリングします。
5. **`slide`（`16:9` ワイドスクリーンスライド & 編集可能 `.pptx`）**: 聴衆が見るスライド面（`1920×1080` ピクセル座標の `::: block xy=(x, y) width=W height=H`）と発表者用の読み上げ台本（`::: note`）を明確に分離します。デュアルウィンドウ発表者ビュー付き HTML や `16:9` ベクター PDF に加え、`./slide_src/build_pptx.sh`（`drawlib build pptx`）で Chromium DOM を計測し、編集可能なネイティブ PowerPoint 図形・テキスト・表・スピーカーノート・`240 DPI` 図版を生成します。

```drawlib align=center code=fold file=project_directory_anatomy_ja.png caption="図 13.2: 多言語対応プロジェクトのディレクトリ構造（TreeNode ソース構成から docs/ 成果物群へのコンパイル）"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.smartarts import CardList, Panel, TreeNode
from drawlib.styles import Colors, Styles

setup(width=158, height=74)

# 左パネル: 信頼できる唯一の情報源 (docs_src/)
src_panel = Panel(
    "ソースディレクトリ (docs_src/)",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    icon=phosphor.folder,
    icon_style=Styles.PrimaryBold,
    header_height=8.8,
)
src_panel.draw((6.0, 6.0), width=76.0, height=62.0)

TreeNode.register_drawing_item(
    name="dir_item",
    location="before",
    padding_width=4.4,
    function=phosphor.folder,
    style=Styles.Primary.patch(icon_color=Colors.Primary),
    args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="py_item",
    location="before",
    padding_width=4.4,
    function=phosphor.file_py,
    style=Styles.Secondary.patch(icon_color=Colors.Secondary),
    args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="cfg_item",
    location="before",
    padding_width=4.4,
    function=phosphor.file_code,
    style=Styles.Dark.patch(icon_color=Colors.Dark),
    args={"width": 3.0},
)

root = TreeNode(
    "docs_src/",
    text_style=Styles.DarkBold.patch(text_size=10.5),
    line_style=Styles.MutedBold.patch(line_width=1.2),
    line_horizontal_margin=2.8,
    line_horizontal_length=2.8,
    line_vertical_margin=4.8,
    children=[
        TreeNode("drawlib.toml  ([project], [i18n], [seo])", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("cfg_item"),
        TreeNode("styles.py & utils.py  (共通テーマ定義)", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("py_item"),
        TreeNode("_assets/  (favicon.png・ロゴ素材)", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("dir_item"),
        TreeNode(
            "en/  (英語デフォルト原稿)",
            children=[
                TreeNode("navbar.md & index.md", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("cfg_item"),
            ],
        ).set_drawing_item("dir_item"),
        TreeNode(
            "ja/  (日本語ローカライズ原稿)",
            children=[
                TreeNode("styles.py, navbar.md & index.md", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("py_item"),
            ],
        ).set_drawing_item("dir_item"),
        TreeNode("build.sh & serve.sh", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("cfg_item"),
    ],
).set_drawing_item("dir_item")
root.draw(xy=(10.5, 54.5))

# コンパイラ接続矢印
line((83.2, 37.0), (89.8, 37.0), arrow_head="->", style=Styles.DarkBold)

# 右パネル: コンパイル生成物 (docs/)
out_panel = Panel(
    "コンパイル生成物 (docs/)",
    style=Styles.PrimaryNeutral.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    icon=phosphor.globe,
    icon_style=Styles.PrimaryBold,
    header_height=8.8,
)
out_panel.draw((91.0, 6.0), width=61.0, height=62.0)

outputs = CardList(
    style=Styles.White.patch(shape_r=1.6),
    text_style=Styles.DarkBold.patch(text_size=10.8),
    description_style=Styles.Dark.patch(text_size=10.0),
    badge_shape="none",
    icon_style=Styles.DarkBold,
    spacing=2.2,
)
outputs.add(
    "docs/ (または docs_html/)",
    "en/・ja/・共有 images/・言語切替 UI",
    icon=phosphor.globe,
    style=Styles.PrimaryFlat.patch(shape_r=1.6),
    text_style=Styles.WhiteBold.patch(text_size=10.8),
    description_style=Styles.White.patch(text_size=10.0),
    icon_style=Styles.WhiteBold,
)
outputs.add(
    "PDF & Office ドキュメント",
    "*_<lang>.pdf / .docx / .pptx",
    icon=phosphor.file_pdf,
)
outputs.add(
    "SEO & AI エージェント索引",
    "sitemap.xml・robots.txt・llms.txt",
    icon=phosphor.brackets_curly,
)
outputs.add(
    "差分ビルドキャッシュ (.drawlib/)",
    "SHA-256 SQLite cache.db (<1ms 復元)",
    icon=phosphor.database,
    style=Styles.SecondaryNeutral.patch(shape_r=1.6),
)
outputs.draw((94.5, 9.0), width=54.0, height=46.5)

save()
```

---

## 13.4 `drawlib.toml` の設計：`[project]`・`[i18n]`・`[seo]`

Markdown ベースのすべてのプロジェクト（`doc`・`site`・`catalog`・`slide`）は、`<target>_src/drawlib.toml` によって宣言的に制御されます。メタデータや出力ポリシーを `drawlib.toml` に集約することで、シェルスクリプトや CI 設定でのオプション指定漏れを防げます。

```toml
[project]
name = "platform_docs"
type = "site"                 # "images" | "doc" | "site" | "catalog" | "slide"
title = "Cloud Platform Architecture"
description = "Unified architecture portal and API guide."
style = "google"              # "default" | "google" | "monochrome"

[i18n]
default_lang = "en"
langs = ["en", "ja"]          # doc/site/catalog/slide では単一言語でも必須

[i18n.labels]
en = "English"
ja = "日本語"

[i18n.descriptions]
en = "Cloud Platform architecture documentation and operational runbooks."
ja = "クラウドプラットフォームのアーキテクチャ設計書および運用ガイド。"

[seo]
site_url = "https://docs.example.com"
og_image = "_assets/ogp.png"
twitter_card = "summary_large_image"
sitemap = true
robots = true
llms_txt = true
```

### 多言語スケルトン整合検査（`[i18n]`）と AI 検索最適化（`[seo]`）

`langs` に複数言語（`["en", "ja"]` など）を設定すると、Drawlib はビルド開始時に**4 段階の機械的パリティ検査（構造整合チェック）**を自動実行し、翻訳漏れや構造崩れを本番デプロイ前に検出します。

- **1. ファイル構成と `navbar.md` の完全一致**: すべての `<lang>/` フォルダが同一の相対 `.md` ファイル集合を持ち、`site` プロジェクトでは `navbar.md` のセクション数とリンク先ターゲットが一致していることを検証します。
- **2. Markdown 構造スケルトン一致**: 各ページの `#` / `##` / `###` 見出し階層（`H1`〜`H3`）・本文スロット（`MarkdownText`）・通常のコードブロック言語（`CodeBlock`）・`drawlib` ブロック属性（`align`, `code`, `caption` の有無）の順序が `default_lang` と一致することを検証します。連続する段落・箇条書き・表は単一の `MarkdownText` トークンに畳み込まれるため、日本語として自然な段落分割や言い回しを自由に記述できます。
- **3. 共通図版とローカライズ図版の自動判別**: `ja/` 側で同一ファイル名（`file=arch.png`）を使った場合は Python コードの完全一致が検証され、全言語で **1 回だけ**描画して共有されます。図中テキストを日本語化する場合は `ja/styles.py`（`FontJapanese`）と組み合わせ、`file=arch_ja.png` のように言語サフィックス付きファイル名を指定します。
- **4. SEO タグと `llms.txt` の自動出力（`[seo]`）**: `[seo]` を設定すると、各 HTML の `<head>` に `<link rel="canonical">`・多言語 `hreflang`・Open Graph（`og:*`）・Twitter Card タグが自動挿入されるほか、ルート直下に `sitemap.xml`・`robots.txt`・および AI エージェント向けのドキュメント索引規格である **`llms.txt`**（`llmstxt.org` 準拠）が自動生成されます。
