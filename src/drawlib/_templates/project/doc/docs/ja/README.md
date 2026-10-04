# Drawlib ドキュメントプロジェクト

このディレクトリには、Drawlib を使用して静的 HTML、ベクター PDF、Markdown、および図版画像にコンパイルされる仕様書・技術レポートの Markdown と作図コードが含まれています。

---

## 1. ディレクトリ構成

- `__SRC_DIR__/`: ドキュメントソースおよび設定ファイル (**編集対象 / Source of Truth**)。
  - `build.sh`: 全ビルドを一括実行するマスタービルドスクリプト。
  - `build_html.sh`: HTML の高速ビルド。
  - `build_pdf.sh`: 印刷・提出用ベクター PDF ビルド。
  - `build_markdown.sh`: GitHub 閲覧用 Markdown ビルド。
  - `build_image.sh`: 図版画像の一括エクスポート。
  - `serve.sh`: ローカルプレビューサーバーの起動。
  - `styles.py`: 全体スタイル設定 (テーマ、カラー、フォント)。
  - `utils.py`: 再利用可能な作図ヘルパー関数・マクロ。
  - `style.css`: ドキュメント装飾およびページ設定 CSS。
  - `template.html`: Jinja2 HTML テンプレート。
  - `README.md`: このカスタマイズガイド。
  - `00_cover.md`: 表紙 / カバーページ。
  - `01_overview.md`: 概要章。
  - `02_design.md`: 設計章。
- `__OUT_MARKDOWN_DIR__/`: 生成された Markdown ドキュメント。
- `__OUT_HTML_DIR__/`: 生成された HTML ドキュメント。
- `__OUT_PDF__`: 生成された PDF ドキュメント。
- `__OUT_IMAGES_DIR__/`: 抽出された図解画像。

---

## 2. ドキュメントのビルド

### スクリプトの実行
```bash
./build_html.sh       # HTML の生成
./build_pdf.sh        # ベクター PDF の生成
./build_markdown.sh   # Markdown の生成
./build_image.sh      # 図版画像のエクスポート
./build.sh            # 全ビルドの実行
```

### プレビュー
```bash
./serve.sh            # ローカルプレビューサーバーの起動
```
