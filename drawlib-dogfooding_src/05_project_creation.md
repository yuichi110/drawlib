# 第5章: プロジェクト作成とビルド運用

Drawlib には、目的別のドキュメントプロジェクトを瞬時にスキャフォールドする `drawlib init` コマンドが用意されています。

## 5.1 プロジェクトテンプレートの種類

| テンプレート | 用途 | 主な生成成果物 |
| :--- | :--- | :--- |
| **`pdf`** | 複数章からなる技術仕様書、設計レポート、提出資料 | `<name>.pdf`（目次付き） |
| **`site`** | サイドバーナビゲーション付きの多ページドキュメントサイト | `<name>_html/` および `<name>/` |
| **`simple`** | 単一の仕様書、RFC、README | `<name>_html/doc.html` |
| **`image`** | 独立した Python 作図スクリプト集 | `<name>/*.png` |

## 5.2 日本語 Google スタイルの PDF プロジェクト作成

以下のコマンド 1 つで、日本語対応および Google スタイルの PDF プロジェクトを作成できます:

```bash
uv run drawlib init pdf my_report/ -o report -l ja -s google
```

```drawlib 640px center file:fig_project_lifecycle.png caption:"図 5.1: プロジェクト作成から成果物生成までのライフサイクル"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=135, height=54)

ts_sec_body = Styles.secondary.patch(text_size=8.5, text_halign="left")
ts_body = Styles.primary.patch(text_size=8.5, text_halign="left")
ts_acc_body = Styles.accent.patch(text_size=8.5, text_halign="left")

# 1. スキャフォールド: drawlib init
rectangle((23.5, 24.0), width=35.0, height=38.0, r=2.0, style=Styles.muted_dashed)
rectangle((23.5, 40.0), width=33.0, height=5.5, r=1.5, style=Styles.secondary_flat, text="1. drawlib init", textstyle=Styles.white_bold)

phosphor.terminal_window(xy=(11.0, 31.0), width=5.0, style=Styles.secondary)
text((16.0, 31.0), text="-o report\nフォルダと出力名の連動", style=ts_sec_body)

phosphor.palette(xy=(11.0, 21.5), width=5.0, style=Styles.secondary)
text((16.0, 21.5), text="-s google\nCSS と Python の統一", style=ts_sec_body)

phosphor.translate(xy=(11.0, 12.0), width=5.0, style=Styles.secondary)
text((16.0, 12.0), text="-l ja\n日本語フォント設定", style=ts_sec_body)

# 矢印 1
line((42.0, 24.0), (49.0, 24.0), arrowhead="->", style=Styles.bold)
text((45.5, 27.5), text="自動生成", style=Styles.secondary_bold, size=8.5)

# 2. 編集ディレクトリ: report_src/ (Source of Truth)
rectangle((67.5, 24.0), width=35.0, height=38.0, r=2.0, style=Styles.primary_outline)
rectangle((67.5, 40.0), width=33.0, height=5.5, r=1.5, style=Styles.primary_flat, text="2. report_src/ (編集源)", textstyle=Styles.white_bold)

phosphor.file_text(xy=(55.0, 31.0), width=5.0, style=Styles.primary)
text((60.0, 31.0), text="00_cover.md, 01_*.md\n文章 + 埋め込み作図コード", style=ts_body)

phosphor.file_code(xy=(55.0, 21.5), width=5.0, style=Styles.primary)
text((60.0, 21.5), text="styles.py / style.css\n統一デザイン定義", style=ts_body)

phosphor.play_circle(xy=(55.0, 12.0), width=5.0, style=Styles.primary)
text((60.0, 12.0), text="build.sh\nコンパイルスクリプト", style=ts_body)

# 矢印 2
line((86.0, 24.0), (93.0, 24.0), arrowhead="->", style=Styles.bold)
text((89.5, 27.5), text="build.sh", style=Styles.primary_bold, size=8.5)

# 3. 成果物: report.pdf
rectangle((111.5, 24.0), width=35.0, height=38.0, r=2.0, style=Styles.accent_outline)
rectangle((111.5, 40.0), width=33.0, height=5.5, r=1.5, style=Styles.accent_flat, text="3. report.pdf (成果物)", textstyle=Styles.white_bold)

phosphor.file_pdf(xy=(99.0, 31.0), width=5.0, style=Styles.accent)
text((104.0, 31.0), text="A4 印刷最適化\nChromium による描画", style=ts_acc_body)

phosphor.list_numbers(xy=(99.0, 21.5), width=5.0, style=Styles.accent)
text((104.0, 21.5), text="自動目次生成\nページ番号の完全連動", style=ts_acc_body)

phosphor.image(xy=(99.0, 12.0), width=5.0, style=Styles.accent)
text((104.0, 12.0), text="ベクター図版統合\n高解像度レンダリング", style=ts_acc_body)
```

### `-o` オプションによる名前の連動仕様
`-o report` を指定すると、以下の連動関係が自動的に構築されます:
- **ソースフォルダ**: `my_report/report_src/` が作成されます。
- **ビルド出力**: `my_report/report.pdf` が出力対象として自動設定されます。

## 5.3 ディレクトリ構造

生成された `report_src/` 内の各ファイルは以下の役割を持ちます:

```text
my_report/
├── report_src/
│   ├── 00_cover.md           # [必須] 表紙（タイトル・メタデータ）
│   ├── 01_overview.md        # 第1章ドキュメント
│   ├── 02_design.md          # 第2章ドキュメント
│   ├── style.css             # PDF デザイン用スタイルシート (Google テーマ)
│   ├── styles.py             # Python 作図用スタイル設定 (GoogleStyles + 日本語)
│   ├── template.html         # Jinja2 印刷レイアウトテンプレート
│   ├── utils.py              # プロジェクト共通の作図ヘルパー関数
│   ├── build.sh              # [実行可能] ワンクリックビルドスクリプト
│   └── README.md             # プロジェクト手引書
```

## 5.4 ビルドの実行

ドキュメントを PDF にコンパイルするには、生成された `build.sh` を実行するだけです:

```bash
# プロジェクトフォルダへ移動してビルドスクリプトを実行
./my_report/report_src/build.sh
```

ビルドが完了すると、`my_report/report.pdf` が出力されます。
