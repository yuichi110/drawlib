# 実装プラン：Jupyter / Google Colab プロジェクト（`type = "jupyter"`）の導入と公式ハンズオン構築

## 1. 背景と目的

### 1.1 新しい価値提案：「図解付きの Colab / Jupyter ドキュメントを作りたければ Drawlib」
機械学習チュートリアル、データサイエンス教材、LLM / RAG ハンズオン、OSS の入門ガイド、大学講義・社内研修資料など、Google Colab や Jupyter Notebook（`.ipynb`）で技術ドキュメントを作成する場面では、長年以下の課題が存在していました。

1. **ノートブックの解説パートに図解を入れるのが困難**:
   コードを実行する前にシステム構成図・データパイプライン・アルゴリズムの流れを図解したいにもかかわらず、`.ipynb` には図を描く仕組みがないため、外部 GUI ツール（draw.io やスライド等）で PNG を作って貼るか、図のない文字だけのノートブックにするしかなかった。
2. **`.ipynb`（巨大 JSON）が Git 管理・AI エージェントと相性が悪い**:
   `.ipynb` を直接編集すると Git diff が読みづらく、Claude Code や Cursor などの AI コーディングエージェントが「図解付きのわかりやすい Colab 教材」を自律的に作成・レビュー・保守することが難しかった。
3. **`drawlib` 自身のゼロインストール体験の提供**:
   `drawlib` を初めて知るユーザーが、ローカル環境構築なしでブラウザ上からワンクリック（`Open in Colab`）で `drawlib` の描画コードを実行・改造して学べる公式ハンズオン環境が求められていた。

そこで、`drawlib` の第6のプロジェクトアーキタイプとして **`jupyter`** を導入し、**「Markdown + Python で執筆・Git 管理し、図解入りの `.ipynb`（Jupyter / Google Colab ノートブック）と Web プレビュー HTML を同時ビルドできる仕組み（Illustrated Notebook / Colab as Code）」** を実現します。

---

## 2. 基本設計方針

### 2.1 プロジェクトタイプ名：`jupyter`（＋ Google Colab 連携の標準搭載）
- **正式アーキタイプ名**: **`jupyter`**（`drawlib.toml` の `type = "jupyter"`、エイリアスなし）
  - 既存の5アーキタイプ（`images`, `doc`, `site`, `catalog`, `slide`）と同様に、特定のクラウド製品名ではなく汎用規格名である `jupyter` を一貫して採用する（`colab` エイリアスは設けない）。
  - 生成される `.ipynb` は Google Colab はもちろん、VS Code Jupyter 拡張、ローカルの JupyterLab、JupyterHub、Kaggle Notebooks 等すべての環境でそのまま動作する。
- **Google Colab ファーストクラス連携**:
  - 生成される HTML プレビューおよびノートブック先頭には、ワンクリックで Google Colab を起動できる **`Open in Colab` バッジ** と `.ipynb` ダウンロード導線を標準搭載する。

### 2.2 本リポジトリ（`yuichi110/drawlib`）内での一元管理（Single Source of Truth）
- 公式の Colab / Jupyter チュートリアル群は別リポジトリ（`drawlib-colab`）へ分離せず、本リポジトリ内のドキュメントプロジェクトとして Git 管理する。
- **理由**:
  1. ライブラリの API 変更や新機能追加時に `./dcli docs build` で一括ビルド・検証（Dogfooding）でき、本体とサンプルコードの乖離を防げる。
  2. 編集用ソースは純粋な Markdown（`.md`）で管理し、出力 `.ipynb` には不要な巨大バイナリ出力を持たせない（または Web 公開画像 URL の参照・軽量埋め込みを選択できる）設計とすることで、Git リポジトリの肥大化を防げる。

---

## 3. コア仕様：Markdown から `.ipynb` & HTML への変換モデル

### 3.1 2種類のコードブロックの役割分担
Markdown ソース内のコードフェンスの種類と属性によって、`.ipynb` 内のセルへの変換方法を制御します。

````markdown
# 1. データパイプラインと可視化ハンズオン

まずはパイプラインの全体アーキテクチャを確認しましょう。

```drawlib align=center code=fold file=pipeline_arch.png caption="図1: データ処理パイプラインの全体像"
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=120, height=35)
# ... (Drawlib でアーキテクチャ図を描画)
save()
```

次に、実際のデータ処理を Colab 上で動かしてみましょう。以下のセルを実行してください。

```python
# Colab / Jupyter 上で読者が Shift+Enter で実行するコードセルになる
import numpy as np

data = np.linspace(0, 10, 5)
print("Sample data:", data)
```
````

| Markdown 内の記述 | `.ipynb` での出力（デフォルト） | HTML プレビューでの出力 | 主な用途 |
| :--- | :--- | :--- | :--- |
| **通常の Markdown 文章** | `markdown` セル | 通常の HTML 本文 | 解説文・見出し・箇条書き・数式 |
| **```` ```drawlib ```` ブロック**<br>*(デフォルト / `cell=markdown`)* | ビルド時に画像をレンダリングし、**`markdown` セル内に完成図を埋め込む** | 通常の Drawlib 図解カード（`code=fold` 等に対応） | 読者に描画コードを実行させず、開いた瞬間から見せたいアーキテクチャ図・概念図 |
| **```` ```drawlib cell=code ````**<br>*(または設定でコードセル化)* | `save(...)` を `show()` に自動変換した **実行可能な `code` セル**（＋直前にお手本図解プレビューも選択可） | Drawlib 図解カード（`code=show`） | **`drawlib` 自体の使い方を学ぶハンズオン**（読者がパラメータを書き換えて再描画を試せる） |
| **```` ```python ```` ブロック** | **実行可能な `code` セル** | シンタックスハイライト付き Python コードブロック | 読者が Colab / Jupyter 上で実際に実行する Python コード |
| **```` ```python cell=markdown ````**<br>*(または ` ```bash `, ` ```toml ` 等)* | `markdown` セル内のフェンス付きコードブロック（非実行） | シンタックスハイライト付きコードブロック | 実行させない設定ファイル例や参考スニペット |

### 3.2 `.ipynb` 内の図解画像の埋め込みモード（`image_mode`）
一般ユーザーが自身の GitHub リポジトリで使う場合と、公式サイト（`www.drawlib.com`）で軽量配布する場合の両方に対応するため、以下のモードをサポートします。

1. **`attachment` / `data_uri` モード（一般ユーザー向けデフォルト）**:
   - ビルド時に生成した図解画像（PNG / WebP）を `.ipynb` の Markdown セル内（Jupyter 標準の `attachments` またはインライン Base64 Data URI）に格納する。
   - **メリット**: GitHub Pages 等を立てていなくても、**`.ipynb` 1ファイルを GitHub に push するだけで、Google Colab や VS Code で開いた瞬間にすべての図解が表示される**。
2. **`url` / `relative` モード（公式ドキュメント・軽量 Git 管理向け）**:
   - `drawlib.toml` の `[seo].site_url`（例: `https://www.drawlib.com/jupyter`）または相対パスを用いて、Markdown セルから外部画像ファイル（`images/<file>.png`）を参照する。
   - **メリット**: **`.ipynb` ファイル自体に Base64 画像データが含まれないため、1ファイル 10〜20KB 程度の純粋なテキストサイズに収まり、Git リポジトリが一切肥大化しない**。かつ Google Colab で開いた際にも URL 経由でお手本図解が即座に表示される。

### 3.3 ノートブック先頭への自動挿入（Colab バッジ & セットアップセル）
各 `.md` ファイルから生成される `.ipynb` の先頭には、`drawlib.toml` の設定に基づいて以下を自動挿入できます：
1. **ヘッダー Markdown セル**:
   - ノートブックのタイトル、`Open in Colab` バッジ（設定時）、Web ドキュメント版へのリンク。
2. **環境セットアップ Code セル（オプション）**:
   - 例: `!pip install -q drawlib`（または任意のパッケージ一覧）。
   - もしプロジェクト内の `styles.py` / `utils.py` を `cell=code` の Drawlib セルから参照する場合は、初期化セルまたはインライン展開で Colab 上でも単体動作するように構成する。

### 3.4 AI 自律 Dry-Run（順次セル実行・出力キャプチャ・検証）エンジン
AI コーディングエージェントが作成したノートブックの品質を自律検証でき、かつ CI / `pytest` でも自動テストできるよう、外部の重い Jupyter カーネル（`ipykernel`）に依存しない **インプロセス Notebook Dry-Run エンジン** を組み込みます。

1. **同一名前空間での順次セル実行（State Persistence）**:
   - 1つの `.md`（＝1つの `.ipynb`）に含まれるすべての実行可能セル（```` ```python ```` および `cell=code` の ```` ```drawlib ````）を、上から順番に **共通の `globals` 辞書** 内で `exec()` / `eval()` 実行する。
   - 前のセルで定義した変数・関数・クラス・`import` が後続のセルへそのまま引き継がれるため、実際の Jupyter / Google Colab と同じ実行セマンティクスを再現できる。
   - `!pip install ...` などの IPython シェルマジック行（`!` や `%` 始まり）は Dry-Run 時には安全に自動スキップする。
   - ノートブック先頭および各 `drawlib` 描画セルの前後では `canvas.clear()` を適切に制御し、前のセルの描画オブジェクトが意図せず残らないようにする。
2. **`stdout` / 最終評価値 / 図解出力 / `[Geometry Warning]` の自動キャプチャ**:
   - 各セルの `print()` 等の標準出力（`stdout`）およびセル最終行の式評価結果（`repr`）をキャプチャし、生成される `.ipynb` のセル `outputs`（`stream` / `execute_result` 出力、テキストのみなので数バイト〜数百バイトで超軽量）および **HTML プレビューの `Out [n]:` セル出力欄** に自動反映する。
   - `cell=code` のセル内で `show()` が呼ばれた場合は、ヘッドレスで画像をレンダリングして HTML プレビュー側に表示しつつ、`[Geometry Warning]`（矢印の潰れや座標はみ出し）を検知して警告・エラー出力する。
3. **AI 自己修正ループ向けの単体・全体 Dry-Run 実行**:
   - **エラー位置の正確な特定**: 前のセルで定義し忘れた変数（`NameError`）や構文エラー・型エラーが発生した場合、「どの `.md` ファイルの、何番目のコードセル（`In [n]`）、Markdown 内の何行目で失敗したか」をトレースバック付きで即座にレポートする。
   - **単一ノートブックの高速 Dry-Run**: `drawlib build jupyter <path/to/notebook.md> --dry-run`（および `drawlib show <notebook.md> -g`）により、AI エージェントは執筆中の1ファイルだけを数秒で Dry-Run 実行＆グリッド視覚検査できる。

---

## 4. `drawlib` コア・CLI・マニフェストの拡張仕様

### 4.1 `setup(..., cwd=True)` による明示的なカレントディレクトリ基準パス解決
- **設計方針**:
  コールスタック推測による暗黙的な自動フォールバックは行わず、`0` / `1` の決定的なオプションとして `setup(..., cwd=True)`（および `drawlib_settings.set_cwd(True)`）を導入する。
- **挙動**:
  - `cwd=False`（デフォルト）: 従来通り呼び出し元スクリプト（`.py` / `.md`）の場所を基準に相対パス（`save()`, `image()`, `Dimage()` 等）を解決する。
  - `cwd=True`（`setup(width=100, height=50, cwd=True)` 指定時）: すべての相対ファイルパス解決（`get_script_relative_path()`）および引数なし `save()`（`<cwd>/output.png`）を確実にカレントワーキングディレクトリ（`os.getcwd()`）基準に切り替える。`clear()` 呼び出し時には `cwd=False` にリセットされる。

### 4.2 `drawlib.toml` マニフェスト拡張（`src/drawlib/_builder/_common/manifest.py`）
- `ProjectArchetype` に `"jupyter"` を追加。
- `_I18N_ARCHETYPES` に `"jupyter"` を追加し、単一言語（`en/` または `ja/`）および多言語（`langs = ["en", "ja"]`）の `<src_dir>/<lang>/*.md` 構造に完全対応させる。
- `[jupyter]` セクションのサポート：
  ```toml
  [project]
  name = "tutorials"
  type = "jupyter"
  style = "google"

  [i18n]
  default_lang = "en"
  langs = ["en", "ja"]

  [jupyter]
  github_repo = "yuichi110/drawlib"          # Open in Colab URL の自動生成用 (optional)
  github_branch = "main"                     # デフォルト: "main"
  notebook_dir_in_repo = "docs/jupyter"      # リポジトリルートからの .ipynb 配置パス (optional)
  setup_packages = ["drawlib"]               # 先頭セルに !pip install -q ... を生成 (optional)
  drawlib_cell_mode = "markdown"             # "markdown" (図解として表示) | "code" (実行セルとして出力)
  image_mode = "attachment"                  # "attachment" (単体完結) | "url" (site_url 参照で軽量化)
  execute = true                             # ビルド時に全コードセルを順次 Dry-Run 実行し stdout 出力を検証・記録する
  ```

### 4.3 CLI コマンドの追加（`src/drawlib/_cli/commands/`）
1. **`drawlib init project jupyter [target] [-l <langs>] [-s <style>] [-f]`**
   - `<target>_src/` をスキャフォールドする：
     - `drawlib.toml`（`type = "jupyter"`）
     - `styles.py`, `utils.py`, `_assets/`, `style.css`, `template.html`
     - `<lang>/01_sample_notebook.md`（図解 ```` ```drawlib ```` ブロックと実行用 ```` ```python ```` セルの両方を含むスターター）
     - `build.sh`（HTML と `.ipynb` を一括ビルド）、`build_jupyter.sh`、`build_html.sh`、`serve.sh`
2. **`drawlib build jupyter <input_path> [-o <output_dir>] [--execute/--no-execute] [--dry-run]`**
   - `<input_path>`（ディレクトリまたは単一 `.md` ファイル）から以下を生成・検証する：
     - 各 `.md` に対応する `.ipynb` ファイル（`nbformat v4.5` 準拠の JSON、外部依存パッケージ不要で標準 `json` モジュールのみで生成）
     - `--execute`（デフォルト有効）により全コードセルを順次 Dry-Run 実行し、エラーがないことを検証するとともに `stdout` 出力を `.ipynb` と HTML に記録する（`--dry-run` 指定時はファイル書き出しを行わず順次実行検証のみを高速実行）
     - 同時に Web ブラウザ・`drawlib serve` で閲覧できる **Notebook 風 HTML プレビューページ**（`In [1]:` / `Out [1]:` のセル表示、コードコピーボタン、描画された図解、各ページ上部の **`Open in Colab` バッジ** と **`.ipynb` ダウンロードボタン** 付き）を生成する

---

## 5. 本リポジトリ内でのドッグフーディング・ブラウザ試用・自動テスト構成

本リポジトリ自身の公式ハンズオン教材として `docs_src/jupyter/` を構築し、`./dcli docs` および `./dcli test` に統合します。

### 5.1 手元のブラウザで確認・インタラクティブ試用する2つの方法
1. **Notebook 風 HTML プレビューで確認する（`./dcli docs serve jupyter`）**:
   - `./dcli docs build jupyter` でビルド後、`./dcli docs serve jupyter` を実行すると、手元のブラウザ（`http://localhost:8000`）で Notebook 風 HTML プレビューが開く。
   - Dry-Run によって実際に実行された `In [1]:` コードセル、`Out [1]:` 出力結果、レンダリング済み図解、`Open in Colab` ボタン、`.ipynb` ダウンロードリンクをブラウザ上で即座に確認できる。
2. **手元のブラウザ上で `.ipynb` を実際に動かして試す（ローカル JupyterLab / Notebook モード）**:
   - 「Google Colab に push する前に、手元のブラウザ上で実際に `.ipynb` のセルを編集して `Shift + Enter` で動かして試したい」という場合のために、生成された `docs/jupyter/{en,ja}/*.ipynb` をローカルの JupyterLab（`uv run --with jupyterlab jupyter lab docs/jupyter`、または `./dcli docs serve jupyter --lab` オプション）や VS Code Jupyter 拡張で直接開き、ローカルの `drawlib` コードを使ってその場でインタラクティブにセル実行できる環境を提供する。

### 5.2 テストの自動化（`./dcli test` への組み込み）
1. **ビルダ・Dry-Run エンジンの単体テスト (`tests/drawlib/doc_builder/test_jupyter_builder.py`)**:
   - Markdown から `.ipynb`（`nbformat v4.5`）および HTML への変換精度検証。
   - Dry-Run エンジンによるセル間の状態引き継ぎ（前のセルの変数を後のセルで参照）、`stdout` キャプチャ、`save()` → `show()` 自動変換、シェルマジック（`!pip` 等）のスキップを検証。
   - 意図的にエラー（`NameError`, `ZeroDivisionError` 等）を含むセルを実行した際に、対象のファイル名・セル番号・行番号が正確に検出されることを検証。
2. **公式ノートブック全件の自動 Dry-Run 統合テスト (`tests/drawlib/doc_builder/test_jupyter_docs_dryrun.py`)**:
   - `./dcli test`（および CI）にて、`docs_src/jupyter/{en,ja}/*.md` の全ノートブックを対象に Dry-Run 検証を自動実行する。
   - 将来 `drawlib` 本体の API や内部実装を変更した際にも、公式ノートブック内の全コードセルがエラーや `[Geometry Warning]` なしに完走することを自動テストで保証する。

### 5.3 公式ハンズオンノートブックのカリキュラム案（全6編・日英対応）
1. `01_getting_started.md` — **Canvas と基本図形・座標系 (`setup`, `show`, `grid=True`)**
2. `02_styles_and_icons.md` — **デザイントークン (`Styles`, `Colors`) とアイコンスイート (`phosphor`, `gcp`)**
3. `03_smartarts.md` — **SmartArts による構造化ビジュアル (`ChevronProcess`, `CardList`, `Table`, `TreeNode`)**
4. `04_charts.md` — **定量データ可視化チャート (`BarChart`, `LineChart`, `PieChart`, `RadarChart`)**
5. `05_diagrams_and_graphs.md` — **システム構成図・シーケンス図・自動レイアウトグラフ (`architecture`, `sequence`, `graph`)**
6. `06_illustrated_notebook.md` — **応用：Drawlib で「図解付きデータ分析・ML ノートブック」を作る方法**

---

## 6. 段階的な実装ステップ（全5ステップ）

各ステップごとに単体テスト（`./dcli test target ...`）と静的解析（`./dcli code-check all`）を実行し、段階的に品質を固めながら進めます。

### Step 1: `setup(..., cwd=True)` による明示的パス解決の実装（`l1_core`, `l4_canvas`）
- **対象**:
  - `src/drawlib/_core/l1_core/_settings.py`, `_path_utils.py`
  - `src/drawlib/_core/l4_canvas/_base.py`
  - `tests/drawlib/_core/l1_core/test_path_utils.py`
- **内容**:
  - `setup(..., cwd=True)` 指定時に `os.getcwd()` 基準でパスを解決し、`clear()` で `cwd=False` に戻す決定的な仕組みを実装。
- **検証**: `./dcli test target core` & `./dcli test target canvas` & `./dcli code-check all`

### Step 2: マニフェスト拡張・`.ipynb` コンパイラ・AI Dry-Run エンジンの実装（`_builder`）
- **対象**:
  - `src/drawlib/_builder/_common/manifest.py`（`type = "jupyter"`、`JupyterConfig` `[jupyter]` セクション追加）
  - `src/drawlib/_builder/doc_builder/detector.py` & `i18n.py`（`jupyter` タイプ認識・多言語検証対応）
  - `src/drawlib/_builder/doc_builder/exporter_jupyter.py`（新規：`nbformat v4.5` `.ipynb` 生成器＋**インプロセス順次 Dry-Run 実行エンジン**）
  - `src/drawlib/_builder/doc_builder/compiler/jupyter.py`（新規：`build_jupyter()` 実装。`.ipynb` 出力、Notebook 風 HTML プレビュー生成、`In [n]:` / `Out [n]:` 表示、`Open in Colab` バッジ、`--dry-run` 対応）
  - `src/drawlib/_builder/doc_builder/__init__.py`（`build_jupyter` の公開）
  - `tests/drawlib/doc_builder/test_jupyter_builder.py`（新規：単体テスト）
- **検証**: `./dcli test target doc-builder` & `./dcli code-check all`

### Step 3: プロジェクトテンプレート・CSS・CLI コマンドの実装（`_templates`, `_cli`）
- **対象**:
  - `src/drawlib/_templates/_models.py` & `_project.py`（`jupyter` プロジェクトタイプ登録）
  - `src/drawlib/_templates/project/jupyter/`（新規：`drawlib.toml`, `build.sh`, `build_jupyter.sh`, `build_html.sh`, `serve.sh`, `template.html`, `<lang>/01_sample_notebook.md`）
  - `src/drawlib/_templates/css/targets/jupyter.css`（新規：Notebook セル UI と `Open in Colab` / `.ipynb` ダウンロードバーの CSS）
  - `src/drawlib/_cli/commands/init.py`（`drawlib init project jupyter` 追加）
  - `src/drawlib/_cli/commands/build.py`（`drawlib build jupyter` 追加、`--execute/--no-execute`, `--dry-run` 対応）
- **検証**: `./dcli test target cli` & `./dcli test target doc-builder` & `./dcli code-check all`

### Step 4: AI エージェントルールと公式 API / CLI リファレンスの更新
- **対象**:
  - `src/drawlib/_rules/project_jupyter.md`（新規：`uv run drawlib rules show project-jupyter` 用ルール）
  - `src/drawlib/_rules/project_overview.md`, `cli.md`, `api.md`
  - `docs_src/api/{en,ja}/28_cli.md`（新規追加した CLI コマンドを日英両方で記載し、機械的完全性テストをパスさせる）
- **検証**: `./dcli test target tests/drawlib/doc_builder/test_api_docs_completeness.py` & `./dcli code-check all`

### Step 5: 公式ハンズオン `docs_src/jupyter/` の構築・`dcli` 統合・ブラウザ視覚レビュー（Dogfooding）
- **対象**:
  - `docs_src/jupyter/`（日英バイリンガル `en/`, `ja/` の全6章ハンズオンノートブックを作成）
  - `tools/dcli/docs/builder.py`, `cli.py`, `banner.py`（`./dcli docs build jupyter`、`./dcli docs serve jupyter [--lab]`、ポータルバナー連携）
  - `tests/drawlib/doc_builder/test_jupyter_docs_dryrun.py`（`docs_src/jupyter/` 全ノートブックの自動 Dry-Run 統合テスト）
- **検証**:
  - `./dcli docs build jupyter` & `./dcli docs serve jupyter --check`
  - 3段階マルチモーダル視覚レビュー（`drawlib show -g` グリッド確認＋Playwright `1280×920` ブラウザスクリーンショット確認）
  - `./dcli code-check all` & `./dcli test all` の完走確認

