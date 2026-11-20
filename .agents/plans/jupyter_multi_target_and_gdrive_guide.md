# 実装プラン：`jupyter` プロジェクトのマルチターゲット分離（`build html` / `build jupyter` / `build image`）＆ Google Drive + Colab 公開ガイド追加

## 1. 背景と目的

Drawlib の `doc` / `site` / `catalog` / `slide` プロジェクトが `drawlib.toml` を単一のソース設定として複数フォーマット（HTML / PDF / DOCX / PPTX / Markdown / Images）を責務分離してビルドできるのと同様に、**`jupyter` プロジェクト（`type = "jupyter"`）もコマンドごとに明確に責務分離**する。

1. **`drawlib build html <jupyter_src>`（既定出力: `<base>_html/`）**:
   - `drawlib.toml` の `[project].type == "jupyter"` および `[jupyter]` 設定を読み取り、**2 カラム HTML プレビューサイト＋同梱 `.ipynb` ダウンロード＋`images/`＋`_assets/`＋SEO** の統合バンドルを出力する。
   - `serve.sh` は `<base>_html/` をサーブする（他の全ドキュメント系プロジェクトと統一）。
2. **`drawlib build jupyter <jupyter_src>`（既定出力: `<base>_jupyter/`）**:
   - **自己完結型の `.ipynb` ファイルのみ（`<lang>/**/*.ipynb`）** を出力する（`.html`・`index.html`・`style.css`・`images/`・`_assets/`・`README.md`・SEO は一切出力しない）。
   - `cell=markdown` の図解画像は `TemporaryDirectory` 内でレンダリング（`.drawlib/cache.db` キャッシュとマルチコア並列を維持）し、Base64 Data URI 埋め込み後に破棄する。単一 `.md` ファイルビルド時（`foo.md -o out.ipynb`）にも余計な `*_images/` を残さない。
   - `[jupyter].execute`（および `--execute` / `--no-execute` / `--dry-run`）によるインプロセス AI Dry-Run 検証（例外ゼロ・`[Geometry Warning]` ゼロ保証）は引き続き動作させる。
3. **`drawlib build image <jupyter_src>`（既定出力: `<base>_images/`）**:
   - `jupyter` プロジェクト内の埋め込み図解画像を抽出する。
   - `cell=markdown` の `drawlib` ブロックはキャッシュ＋並列レンダリングで抽出し、`[jupyter].execute = true` の場合は `cell=code` の `drawlib` ブロックおよび `show()` 出力も共有ノートブック `globals` で順次実行して抽出する（`execute = false` の場合は `cell=markdown` の図解のみ安全に抽出）。
4. **未対応ビルドターゲットの明示ガード**:
   - `drawlib build pdf` / `docx` / `markdown` に `type = "jupyter"` プロジェクトを渡した場合、明確なエラーメッセージで `drawlib build jupyter` / `drawlib build html` を案内する。
5. **Google Drive（`rclone`）＋ Google Colab 公開ガイドの新設（日英バイリンガル）**:
   - `drawlib build jupyter`（`.ipynb` のみ書き出し）を活かした、GitHub 公開を使えないクローズド案件・顧客共有・社内チーム配布向けの **Google Drive 共有フォルダ公開＋Colab 実行ワークフロー** を `docs_src/site/{en,ja}/09_doc_builder_and_cli/jupyter_google_drive.md` としてドキュメント化する。

---

## 2. 実装ステップ

### Phase 1: コアビルダ・テンプレート・CLI・テストの整備

1. **Jupyter コンパイラ分離 (`src/drawlib/_builder/doc_builder/compiler/jupyter.py`, `html.py`, `__init__.py`)**
   - `_compile_jupyter_locales(..., emit_html: bool)` を導入。
   - `build_jupyter()` は `emit_html=False`（`.ipynb` のみ出力、不要な `css_mode` 引数を削除）。
   - `_build_single_jupyter_file()` も `tmp_dir` で中間画像を描画して `.ipynb` 単体のみ出力。
   - 内部関数 `build_jupyter_html()` を追加し、`compiler/html.py` から `type == "jupyter"` 時に委譲（`emit_html=True` で HTML + 同梱 `.ipynb` バンドルを出力）。
   - `compiler/pdf.py`, `docx.py`, `markdown.py` に `type == "jupyter"` 用の明示エラーガードを追加。
2. **`drawlib build image` の `jupyter` 対応 (`src/drawlib/_builder/image_builder.py`)**
   - `_MarkdownImageJob` に `jupyter_cfg: JupyterConfig | None = None` を追加。
   - `_build_directory_markdown_jobs()` / `_build_single_markdown_job()` で `type == "jupyter"` をサポート。
   - `_collect_md_image_block_jobs()` で `cell=markdown` ブロックのみ並列プリレンダリング対象化。
   - `_render_jupyter_markdown_job()` を追加し、`cell=markdown` 図解の抽出と、`execute = true` 時の `cell=code` 実行図解抽出を実装。
3. **CLI & テンプレート更新 (`src/drawlib/_cli/commands/build.py`, `src/drawlib/_templates/`)**
   - `_project.py`: `resolve_project_paths()` の `out_html_dir_name` を `jupyter` でも `<base>_html` に統一。
   - `src/drawlib/_templates/project/jupyter/`:
     - `build_html.sh.template` (`drawlib build html ... -o __OUT_HTML_DIR__/`)
     - `build_jupyter.sh.template` (`drawlib build jupyter ... -o __OUT_JUPYTER_DIR__/`)
     - `build_image.sh.template` (`drawlib build image ... -o __OUT_IMAGES_DIR__/`) を新規追加
     - `build.sh.template` (`build_html.sh` + `build_jupyter.sh` + `build_image.sh`)
     - `serve.sh.template` (`drawlib serve __OUT_HTML_DIR__/`)
     - `docs/{en,ja}/README.md` を更新
4. **公式ドッグフーディング `docs_src/jupyter/` 更新**
   - `docs_src/jupyter/build_html.sh` を `drawlib build html docs_src/jupyter/ -o docs/jupyter/` に更新し、`build.sh` から呼び出すことで `https://www.drawlib.com/jupyter/` と `./dcli docs build/serve jupyter` の動作を維持。
5. **単体・統合テスト更新 (`tests/`)**
   - `tests/drawlib/doc_builder/test_jupyter_builder.py`: `build_jupyter()` が `.ipynb` のみ出力すること（`.html` / `images/` / `style.css` なし）、単一ファイル出力で `*_images/` を残さないこと、`build_html()` が HTML + `.ipynb` を出力すること、`build_image()` が `jupyter` プロジェクトから `cell=markdown` + `cell=code` 図解を抽出できること（`execute=true/false` 両方）、`pdf`/`docx`/`markdown` が明確なエラーを返すことを検証。
   - `tests/drawlib/doc_builder/test_jupyter_docs_dryrun.py`: `build_jupyter`（`.ipynb` のみ）と `build_html`（HTML + `.ipynb`）の両方を検証。
   - `tests/drawlib/cli/test_cli_init.py`: `jupyter` テンプレートに `build_image.sh` を含め検証。

### Phase 2: 既存ドキュメント・API リファレンス・AI ルール更新 & Google Drive 共有ガイド執筆

1. **組み込み AI ルール更新 (`src/drawlib/_rules/`)**
   - `project_jupyter.md`, `project_overview.md`, `cli.md`, `lib_tools.md` を新仕様（`build html` / `build jupyter` / `build image`）に更新し、`project_jupyter.md` に Google Drive（`rclone`）＋ Colab 運用の要点を追記。
2. **API / CLI リファレンス更新 (`docs_src/api/{en,ja}/`)**
   - `27_tools.md`（`build_html`, `build_image`, `build_jupyter`）および `28_cli.md`（`drawlib build html/image/jupyter`, `drawlib init project jupyter`）を日英パリティで更新し、`test_api_docs_completeness.py` を通過させる。
3. **既存サイトドキュメント更新 (`docs_src/site/{en,ja}/`)**
   - `09_doc_builder_and_cli/project_jupyter.md`: 3 ターゲット（`build html` / `build jupyter` / `build image`）の責務分離を反映し、新規 Google Drive 共有ガイドへの相互リンクを追加。
   - `09_doc_builder_and_cli/cli_reference.md`, `01_getting_started/project_quicklook.md` を更新。
4. **新規ガイドページ追加 (`docs_src/site/{en,ja}/09_doc_builder_and_cli/jupyter_google_drive.md`)**
   - `navbar.md`（`en` / `ja`）の `project_jupyter.md` 直下へ登録。
   - 必須コンテンツ：
     1. 概要・メリット（クローズド配布、Base64 単体完結、`build jupyter` の `.ipynb` のみ出力、File ID 維持）
     2. Drawlib 図解 2 枚（`code=fold`、`text_size >= 10.0`、50%+ Neutral、公式アイコン `workspace.google_drive`, `code.colab`, `ai.jupyter`, `phosphor.*` + 高レベルコンポーネント使用）：
        - **図 1（Top Hero, Lines 6–15）**: Markdown Source → `drawlib build jupyter`（`.ipynb` only + Base64）→ `rclone copy` → Google Drive 共有フォルダ → Google Colab 実行の全体フロー
        - **図 2**: ビルドターゲット使い分け（`build html` vs `build jupyter` vs `build image`）および Google Drive 権限・Colab 実行ステップ（Viewer 一時実行 / コピー保存 / Colab シークレット＋アクセス ON）
     3. Step-by-Step 手順：
        - (A) `rclone` インストール・OAuth `client_id` 推奨・`scope = drive`・ヘッドレス `rclone authorize`・マイドライブ／共有フォルダ／共有ドライブ（`team_drive`）の正確な使い分け・`--drive-root-folder-id` 接続確認・`rclone dedupe` 補足
        - (B) Drawlib `jupyter` プロジェクト設定（`colab_base_url` を空にする重要性、`execute = true` vs `false` と `--dry-run` の挙動差・`ImportError` フォールバック、`-f webp` 軽量化、`build_jupyter.sh` でのクリーンビルド小技、単一言語 `<lang>/` フラット配置 vs 多言語構成、`.gitignore`）
        - (C) `sync_gdrive.sh`（環境変数化、非破壊 `copy` 既定、`sync`＋`--include "*.ipynb"` が他ファイル保護の安全装置となる理由、`--dry-run` 確認）および `build.sh` 連携（`--no-sync` を消費して残りを `build_jupyter.sh` へ渡す引数パース、安全スキップガード）
        - (D) 利用者側 Google Colab 実行フロー（閲覧者権限推奨＋SSOT 注意、アプリ追加、コピー保存、シークレット設定＋トグル ON、外部データ/相対リンクの制約）
        - (E) CI（GitHub Actions）自動公開（SA 最小権限、Workload Identity Federation 言及、`caching_and_cicd.md` 相互リンク）

### Phase 3: 3 段階マルチモーダル視覚レビュー＆全品質検証

1. **Stage 1 & 2**: 新規・変更した全 `drawlib` 図解を `uv run drawlib show ... -g -o .drawlib/scratch/..._grid.png` で出力し、目視確認・レイアウト修正。
2. **品質チェック & テスト**:
   - `./dcli code-check all`
   - `./dcli test all`
3. **ドキュメントビルド & Stage 3（ブラウザ HTML 検証）**:
   - `./dcli docs build site`, `./dcli docs build api`, `./dcli docs build jupyter`
   - `./dcli docs serve site --check`, `./dcli docs serve api --check`, `./dcli docs serve jupyter --check`
   - Playwright で `1280×900` スクリーンショットを撮影し、新規ページ（EN/JA）および更新した `project_jupyter.html` の Hero 配置・フォントバランスを目視検証。
   - `.drawlib/scratch/` 一時ファイルをクリーンアップ。
