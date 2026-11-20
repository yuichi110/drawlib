# __TARGET__ — Drawlib Jupyter & Google Colab プロジェクト

このディレクトリ（`__SRC_DIR__/`）は、図解付き Jupyter Notebook（`.ipynb`）・ブラウザ用 HTML プレビュー・抽出図解画像の Single Source of Truth（単一の情報源）です。

## クイックコマンド

```bash
# HTML プレビュー（.ipynb 同梱）・単体 .ipynb ノートブック・図解画像を一括ビルド
./__SRC_DIR__/build.sh

# 単体 .ipynb ノートブックのみをビルド（Google Drive + Colab 共有向け）-> __OUT_JUPYTER_DIR__/
./__SRC_DIR__/build_jupyter.sh

# .ipynb 同梱の 2 カラム HTML プレビューサイトをビルド -> __OUT_HTML_DIR__/
./__SRC_DIR__/build_html.sh

# 埋め込み図解画像のみを抽出 -> __OUT_IMAGES_DIR__/
./__SRC_DIR__/build_image.sh

# ファイル出力なしで AI Dry-Run 実行検証のみを実行
uv run drawlib build jupyter __SRC_DIR__/ --dry-run

# ブラウザで HTML ノートブックプレビューをローカル起動 (__OUT_HTML_DIR__/)
./__SRC_DIR__/serve.sh
```
