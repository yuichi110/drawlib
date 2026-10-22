# 第5章: プロジェクト作成とビルド運用

Drawlib には、目的別のドキュメントプロジェクトを瞬時にスキャフォールドする `drawlib init` コマンドが用意されています。

## 5.1 プロジェクトテンプレートの種類

| テンプレート | 用途 | 主な生成成果物 |
| :--- | :--- | :--- |
| **`doc`** | 複数章の技術仕様書、設計レポート、提出資料 | `<target>.pdf`, `<target>_html/`, `<target>_markdown/`, `<target>_images/` |
| **`site`** | サイドバーナビゲーション付きの多ページドキュメントサイト | `<target>_html/`, `<target>_markdown/`, `<target>_images/` |
| **`slide`** | 16:9 プレゼンテーションスライド（Web 発表・PDF 配布） | `<target>_html/index.html`, `<target>.pdf`, `<target>_images/` |
| **`images`** | 独立した Python 作図スクリプト集 | `<target>_images/*.png`（または `<target>/*.png`, `*.webp`） |

## 5.2 日本語 Google スタイルのドキュメントプロジェクト作成

以下のコマンド 1 つで、日本語対応および Google スタイルの線形ドキュメントプロジェクト（`report_src/`）を作成できます:

```bash
uv run drawlib init doc report -l ja -s google
```

```drawlib align=center file=fig_project_lifecycle.png caption="図 5.1: プロジェクト作成から成果物生成までのライフサイクル"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=52)

header_ts = Styles.WhiteBold.patch(text_size=11.0)
ts_body = Styles.Dark.patch(text_size=10.0, halign="left")
ts_arrow = Styles.DarkBold.patch(text_size=10.0)

# 1. スキャフォールド: drawlib init
rectangle((22.5, 26.0), width=37.0, height=42.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
rectangle((22.5, 43.2), width=35.0, height=6.0, style=Styles.SecondaryFlat.patch(shape_r=1.5), text="1. drawlib init", text_style=header_ts)

phosphor.terminal_window(xy=(8.0, 33.5), width=4.4, style=Styles.Secondary)
text((11.2, 33.5), text="init doc report\nプロジェクト足場生成", style=ts_body)

phosphor.palette(xy=(8.0, 22.5), width=4.4, style=Styles.Secondary)
text((11.2, 22.5), text="-s google\nCSS・作図テーマ統一", style=ts_body)

phosphor.translate(xy=(8.0, 11.5), width=4.4, style=Styles.Secondary)
text((11.2, 11.5), text="-l ja\n日本語フォント設定", style=ts_body)

# 矢印 1
line((41.5, 26.0), (47.0, 26.0), arrow_head="->", style=Styles.DarkBold)
text((44.25, 30.0), text="生成", style=ts_arrow)

# 2. 編集ディレクトリ: report_src/ (Source of Truth)
rectangle((66.0, 26.0), width=37.0, height=42.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
rectangle((66.0, 43.2), width=35.0, height=6.0, style=Styles.PrimaryFlat.patch(shape_r=1.5), text="2. report_src/ (正本)", text_style=header_ts)

phosphor.file_text(xy=(51.5, 33.5), width=4.4, style=Styles.Primary)
text((54.7, 33.5), text="00_cover.md, *.md\n本文 + 埋め込み作図", style=ts_body)

phosphor.file_code(xy=(51.5, 22.5), width=4.4, style=Styles.Primary)
text((54.7, 22.5), text="styles.py / utils.py\n共通スタイル・関数", style=ts_body)

phosphor.folder_open(xy=(51.5, 11.5), width=4.4, style=Styles.Primary)
text((54.7, 11.5), text="_assets/ & build.sh\n素材管理・一括ビルド", style=ts_body)

# 矢印 2
line((85.0, 26.0), (90.5, 26.0), arrow_head="->", style=Styles.DarkBold)
text((87.75, 30.0), text="ビルド", style=ts_arrow)

# 3. 成果物: report.pdf / report_html/
rectangle((109.5, 26.0), width=37.0, height=42.0, style=Styles.Neutral.patch(shape_r=2.0))
rectangle((109.5, 43.2), width=35.0, height=6.0, style=Styles.DarkFlat.patch(shape_r=1.5), text="3. ビルド成果物", text_style=header_ts)

phosphor.file_pdf(xy=(95.0, 33.5), width=4.4, style=Styles.Dark)
text((98.2, 33.5), text="report.pdf\nA4 印刷・自動目次", style=ts_body)

phosphor.globe(xy=(95.0, 22.5), width=4.4, style=Styles.Dark)
text((98.2, 22.5), text="report_html/\nWeb 閲覧・リンク検証", style=ts_body)

phosphor.image(xy=(95.0, 11.5), width=4.4, style=Styles.Dark)
text((98.2, 11.5), text="report_images/\nMarkdown & 抽出図版", style=ts_body)

save()
```

### ターゲット引数による名前の連動仕様
`drawlib init doc report` を実行すると、以下の連動関係が自動的に構築されます:
- **ソースフォルダ**: `report_src/` がカレントディレクトリに作成されます。
- **ビルド出力**: `report.pdf`, `report_html/`, `report_markdown/`, `report_images/` が出力対象として自動設定されます。

## 5.3 ディレクトリ構造とインクリメンタルキャッシュ

生成された `report_src/` 内の各ファイルとディレクトリは以下の役割を持ちます:

```text
report_src/
├── _assets/              # ロゴや外部画像などの静的アセット格納ディレクトリ
├── 00_cover.md           # [必須] 表紙（タイトル・メタデータ）
├── 01_overview.md        # 第1章ドキュメント
├── 02_design.md          # 第2章ドキュメント
├── style.css             # PDF / HTML デザイン用スタイルシート (Google テーマ)
├── styles.py             # Python 作図用スタイル設定 (GoogleStyles + 日本語)
├── template.html         # Jinja2 印刷・Web レイアウトテンプレート
├── utils.py              # プロジェクト共通の作図ヘルパー関数・定数
├── build.sh              # [実行可能] 全ターゲット一括ビルドスクリプト
├── serve.sh              # ローカルプレビューサーバー起動スクリプト
└── README.md             # プロジェクト手引書
```

また、ビルド時にはワークスペース直下の `.drawlib/cache.db`（SQLite ベース）に **SHA-256 によるインクリメンタルビルドキャッシュ** が自動生成されます。各 ````drawlib```` コードブロックの内容、`styles.py`、`utils.py`、および `_assets/` 内の参照アセットのハッシュ値を追跡し、変更された図版のみを再レンダリングするため、2 回目以降のビルドが劇的に高速化されます。

## 5.4 ビルドの実行とリンク整合性チェック

ドキュメントを PDF や HTML、Markdown、抽出画像へ一括コンパイルするには、生成された `build.sh` を実行するだけです:

```bash
# 全成果物（HTML, PDF, Markdown, Images）を一括ビルド
./report_src/build.sh

# 生成された HTML のリンク切れや画像参照エラーを自動検証
uv run drawlib serve report_html/ --check
```

ビルドが完了すると、`report.pdf`、`report_html/`、`report_markdown/`、`report_images/` が出力され、`drawlib serve --check` によって壊れた内部リンクや画像欠損がないことを CI やローカルで即座に検証できます。
