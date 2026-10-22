# 第4章: インストールと環境構築

Drawlib（`v0.3.0`）は公式 PyPI パッケージとして公開されており、モダンな Python パッケージマネージャー `uv` または `pip` を用いて数秒でセットアップできます。

## 4.1 前提環境

- **Python**: 3.11 以上（3.11 / 3.12 / 3.13 対応）
- **対応 OS**: Linux / macOS / Windows
- **パッケージマネージャー**: `uv`（推奨）または `pip`

## 4.2 PyPI からのインストール (`uv` / `pip` / `uvx`)

通常の作図・HTML ドキュメント・スライド・Markdown ビルドを行う場合は、PyPI から `drawlib` パッケージをインストールします:

```bash
# uv を使用する場合（推奨）
uv add drawlib
uv run drawlib --version

# プロジェクトに追加せず、一時環境で単発実行する場合 (uvx)
uvx drawlib --version
uvx drawlib init site

# pip を使用する場合
pip install drawlib
```

## 4.3 PDF エクスポート機能の有効化（オプション）

`doc` プロジェクト（A4 技術仕様書・ホワイトペーパー）や `slide` プロジェクト（16:9 スライドデッキ）でベクター PDF エクスポート機能（`playwright` 連携）を使用する場合は、`[pdf]` オプション付きでインストールし、ヘッドレス Chromium を導入します:

```bash
# 1. PDF エクストラ付きで drawlib をインストール
uv add "drawlib[pdf]"

# 2. PDF 生成に必要な headless Chromium ブラウザをダウンロード
uv run playwright install chromium
```

> **Note (`pip` を使用する場合)**:  
> `pip install "drawlib[pdf]"` を実行した後、`playwright install chromium` を実行してください。

> **Note (Linux ヘッドレスサーバー・CI 環境)**:  
> Ubuntu 等のサーバーやコンテナ環境で OS 共有ライブラリが不足している場合は、以下のように `--with-deps` を付与して実行してください:  
> `uv run playwright install --with-deps chromium`

## 4.4 アセット・ビルドキャッシュ管理 (`drawlib cache`)

PyPI パッケージ本体を軽量に保つため、以下の 2 種類のキャッシュ機構が備わっています:

1. **外部アセットキャッシュ (`drawlib/_cached_assets/`)**:
   多言語フォント（Roboto, Noto Sans JP 等）、ベクターアイコン（Phosphor, FontAwesome, 公式 GCP アイコン）、およびオフライン地図データ（`GeoMap`）は、初回描画時に GitHub Releases からオンデマンドで自動取得され、ローカルにキャッシュされます。
2. **図版差分ビルドキャッシュ (`.drawlib/cache.db`)**:
   `drawlib build` や `drawlib show` の実行時、コードブロック・`styles.py`・`utils.py`・参照アセットのハッシュ値を SQLite データベースに記録し、変更のない図版の再レンダリングをスキップしてビルドを高速化します。

オフライン環境や CI/CD コンテナ向けに全アセットを事前取得したい場合や、キャッシュをクリアしたい場合は `drawlib cache` コマンドを使用します:

```bash
# キャッシュ状態の一覧表示
uv run drawlib cache list

# オフライン・CI 環境向けに全アセット（フォント・アイコン・地図）を一括事前ダウンロード
uv run drawlib cache download --all
# カテゴリ別に取得する場合: --fonts / --icons / --maps

# 差分ビルドキャッシュ（.drawlib/cache.db）のみをクリアして全図版を強制再描画
uv run drawlib cache clear --images

# アセットと差分ビルドキャッシュをすべてクリア
uv run drawlib cache clear --all
```

## 4.5 インストールの動作確認

インストールが完了したら、以下のコマンドで CLI が利用可能であることを確認します:

```bash
# バージョンの確認 (drawlib 0.3.0)
uv run drawlib --version

# 利用可能なプロジェクトテンプレート一覧の表示
uv run drawlib init list
```

`doc`、`site`、`slide`、`images` の 4 種類のプロジェクトテンプレートが表示されれば環境構築は完了です。
