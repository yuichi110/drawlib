# __TARGET__ — Drawlib Jupyter & Google Colab プロジェクト

このディレクトリ（`__SRC_DIR__/`）は、図解付き Jupyter Notebook（`.ipynb`）とブラウザ用 HTML プレビューの Single Source of Truth（単一の情報源）です。

## クイックコマンド

```bash
# .ipynb ノートブックと HTML プレビューをビルド（AI Dry-Run による全セル実行検証を含む）
./__SRC_DIR__/build.sh

# ファイル出力なしで AI Dry-Run 実行検証のみを実行
uv run drawlib build jupyter __SRC_DIR__/ --dry-run

# ブラウザで HTML ノートブックプレビューをローカル起動
./__SRC_DIR__/serve.sh
```
