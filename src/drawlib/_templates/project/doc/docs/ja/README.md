# Drawlib ドキュメントプロジェクト

このディレクトリには、Drawlib を使用して静的 HTML、ベクター PDF、Markdown、および図版画像にコンパイルされる仕様書・技術レポートの Markdown と作図コードが含まれています。

---

## 1. ディレクトリ構成

- `__SRC_DIR__/`: ドキュメントソースおよび設定ファイル (**編集対象 / Source of Truth**)。
  - `drawlib.toml`: プロジェクトマニフェスト (`[project]` 設定および `[i18n]` 言語構成)。
  - `__DEFAULT_LANG__/`: デフォルト言語のチャプターディレクトリ (多言語化する場合は `<lang>/` を追加し `drawlib.toml` の `langs` に追記):
    - `00_cover.md`: 表紙 / カバーページ。
    - `01_overview.md`: 概要章。
    - `02_design.md`: 設計章。
  - `_assets/`: 全言語で共有される画像アセット (`favicon.png`, `linux.png`)。
  - `build.sh`: 標準ビルド（HTML, PDF, Markdown, Images）を一括実行するマスタービルドスクリプト。
  - `build_html.sh`: HTML の高速ビルド。
  - `build_pdf.sh`: 印刷・提出用ベクター PDF ビルド。
  - `build_docx.sh`: 編集可能な MS Word（`.docx`）のオンデマンド出力スクリプト。
  - `build_markdown.sh`: GitHub 閲覧用 Markdown ビルド。
  - `build_image.sh`: 図版画像の一括エクスポート。
  - `serve.sh`: ローカルプレビューサーバーの起動。
  - `styles.py`: 全体スタイル設定 (テーマ、カラー、フォント。言語別の `<lang>/styles.py` 上書きも可能)。
  - `utils.py`: 再利用可能な作図ヘルパー関数・マクロ。
  - `style.css`: ドキュメント装飾およびページ設定 CSS。
  - `template.html`: Jinja2 HTML テンプレート。
  - `README.md`: このカスタマイズガイド。
- `__OUT_MARKDOWN_DIR__/`: 生成された Markdown ドキュメント (`<lang>/...`)。
- `__OUT_HTML_DIR__/`: 生成された HTML ドキュメント (`index.html`, `<lang>/index.html`)。
- `__TARGET___<lang>.pdf` (例: `__TARGET_____DEFAULT_LANG__.pdf`): 言語ごとに生成されたベクター PDF ドキュメント。
- `__TARGET___<lang>.docx` (例: `__TARGET_____DEFAULT_LANG__.docx`): 言語ごとにオンデマンド出力される編集可能な MS Word ドキュメント。
- `__OUT_IMAGES_DIR__/`: 抽出された図解画像。

---

## 2. ドキュメントのビルド

### スクリプトの実行
```bash
./build_html.sh       # HTML の生成
./build_pdf.sh        # ベクター PDF (<base>_<lang>.pdf) の生成
./build_docx.sh       # 編集可能な MS Word (<base>_<lang>.docx) のオンデマンド出力
./build_markdown.sh   # Markdown の生成
./build_image.sh      # 図版画像のエクスポート
./build.sh            # 標準ビルド（HTML + PDF + Markdown + Images）の実行
```

### プレビュー
```bash
./serve.sh            # ローカルプレビューサーバーの起動
```
