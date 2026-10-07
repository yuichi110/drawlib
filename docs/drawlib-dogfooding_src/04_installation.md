# 第4章: インストールと環境構築

Drawlib は、モダンな Python パッケージマネージャー `uv` を用いて、数秒でセットアップできます。

## 4.1 前提環境

- **Python**: 3.11 以上
- **パッケージマネージャー**: `uv`（推奨）または `pip`

## 4.2 Git からのワンライナー導入

PDF 出力機能（`playwright` 連携）を含めた完全な環境を Git リポジトリから直接インストールします:

```bash
# 1. PDF エクストラ付きで drawlib をインストール
uv add "drawlib[pdf] @ git+https://github.com/yuichi110/drawlib.git"

# 2. PDF 生成に必要な headless Chromium ブラウザをダウンロード
uv run playwright install chromium
```

> **Note (Linux ヘッドレスサーバー環境)**:  
> Ubuntu 等のサーバー環境で OS 共有ライブラリが不足している場合は、以下のように `--with-deps` を付与して実行してください:  
> `uv run playwright install --with-deps chromium`

## 4.3 インストールの動作確認

インストールが完了したら、以下のコマンドで CLI が利用可能であることを確認します:

```bash
# バージョンの確認
uv run drawlib --version

# 利用可能なプロジェクトテンプレート一覧の表示
uv run drawlib init list
```

以下のように `site`, `simple`, `pdf`, `image` が表示されれば環境構築は完了です。
