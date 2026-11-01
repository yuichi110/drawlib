# 第4章: インストールと環境構築

Drawlib（`v0.3.2`）は公式 PyPI パッケージとして公開されており、モダンな Python パッケージマネージャー `uv` または `pip` を用いて数秒でセットアップできます。

## 4.1 前提環境

- **Python**: 3.11 以上（3.11 / 3.12 / 3.13 対応）
- **対応 OS**: Linux / macOS / Windows
- **パッケージマネージャー**: `uv`（推奨）または `pip`

## 4.2 PyPI からのインストール (`uv` / `pip` / `uvx`)

標準の `drawlib` パッケージをインストールするだけで、作図・HTML ドキュメント・16:9 Web スライド・Markdown に加え、**ベクター PDF（`drawlib build pdf`）**、**編集可能な MS Word（`drawlib build docx`）**、**編集可能な 16:9 MS PowerPoint（`drawlib build pptx`）** のすべてのエクスポート機能が追加オプションなしでそのまま利用できます:

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

## 4.3 PDF・Office（Word / PowerPoint）出力とヘッドレスブラウザ自動取得

Drawlib は標準インストールだけでドキュメントおよびスライドの各種オフィス・印刷フォーマット出力を完結させます:

- **ベクター PDF / 16:9 PowerPoint 出力 (`drawlib build pdf`, `drawlib build pptx`)**:
  初回の PDF または PPTX ビルド実行時に、Playwright 経由で管理対象の **ヘッドレス Chromium バイナリが自動的にダウンロード・キャッシュ** されます。手動でブラウザをセットアップする必要はありません。
- **編集可能な MS Word 出力 (`drawlib build docx`)**:
  ピュア Python（`python-docx`）のみで動作し、ヘッドレスブラウザ不要で `doc` プロジェクトから編集可能な `.docx` 仕様書（`--generate-index` による目次生成対応）を直接出力できます。

> **Note (最小構成の Linux Docker コンテナ環境)**:  
> Ubuntu / Debian 等の最小コンテナイメージで、ヘッドレス Chromium の起動に必要な OS 共有ライブラリが不足している場合は、以下のコマンドでシステム依存パッケージを一括導入できます:  
> `uv run playwright install-deps chromium`

## 4.4 アセット・ビルドキャッシュ管理 (`drawlib cache`)

PyPI パッケージ本体を軽量に保つため、以下の 2 種類のキャッシュ機構が備わっています:

1. **外部アセット & ヘッドレスブラウザキャッシュ**:
   多言語フォント（Roboto, Noto Sans JP 等）、ベクターアイコン（Phosphor, FontAwesome, 公式 GCP アイコン）、オフライン地図データ（`GeoMap`）、および PDF / PPTX 出力用のヘッドレス Chromium は、初回利用時にオンデマンドで自動取得され、ローカルにキャッシュされます。
2. **図版差分ビルドキャッシュ (`.drawlib/cache.db`)**:
   `drawlib build` や `drawlib show` の実行時、コードブロック・`styles.py`・`utils.py`・参照アセットのハッシュ値を SQLite データベースに記録し、変更のない図版の再レンダリングをスキップしてビルドを高速化します。

オフライン環境や CI/CD コンテナ向けに全アセット・ブラウザを事前取得したい場合や、キャッシュをクリアしたい場合は `drawlib cache` コマンドを使用します:

```bash
# キャッシュ状態の一覧表示
uv run drawlib cache list

# オフライン・CI 環境向けに全アセット（フォント・アイコン・地図・ヘッドレス Chromium）を一括事前取得
uv run drawlib cache download --all
# カテゴリ別に取得する場合: --fonts / --icons / --maps / --browser

# 差分ビルドキャッシュ（.drawlib/cache.db）のみをクリアして全図版を強制再描画
uv run drawlib cache clear --images

# アセットと差分ビルドキャッシュをすべてクリア
uv run drawlib cache clear --all
```

## 4.5 インストールの動作確認

インストールが完了したら、以下のコマンドで CLI が利用可能であることを確認します:

```bash
# バージョンの確認 (0.3.2)
uv run drawlib --version

# 利用可能なプロジェクトテンプレート一覧の表示
uv run drawlib init list
```

`doc`、`site`、`slide`、`images` の 4 種類のプロジェクトテンプレートが表示されれば環境構築は完了です。
