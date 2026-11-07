# `drawlib build` マルチコア並列化 設計・実装計画書 (Multi-Core Build Parallelization Plan)

- **作成日**: 2026-11-07
- **ステータス**: 設計策定済み（実装準備完了）
- **対象スコープ**: `drawlib build` 全サブコマンド（`image`, `markdown`, `html`, `pdf`, `docx`, `slide`, `pptx`）および `drawlib.tools.build_*` プログラマティック API
- **主な新規・変更対象ファイル**:
  - **新規作成**:
    - `src/drawlib/_builder/_common/parallel.py`（共通マルチプロセス描画ワーカープール・ジョブスケジューラ・進捗管理）
    - `tests/drawlib/_core/l3_external/test_download_lock.py`（プロセス間アセット排他ロック単体テスト）
    - `tests/drawlib/doc_builder/test_parallel_build.py`（並列ビルド・キャッシュ整合性・例外伝播・決定論性テスト）
  - **既存変更（コア・ビルダ・CLI）**:
    - `src/drawlib/_core/l3_external/_download.py`（初回フォント・アイコン・マップ展開時のプロセス間ファイルロック追加）
    - `src/drawlib/_builder/_common/__init__.py`
    - `src/drawlib/_builder/doc_builder/processor/processor.py`（インメモリ事前描画 Blob 参照の統合）
    - `src/drawlib/_builder/doc_builder/compiler/html.py`（`site` / `doc` / `catalog` 事前並列プリレンダ統合）
    - `src/drawlib/_builder/doc_builder/compiler/markdown.py`
    - `src/drawlib/_builder/doc_builder/compiler/pdf.py` / `src/drawlib/_builder/doc_builder/merger.py`
    - `src/drawlib/_builder/doc_builder/compiler/docx.py` / `src/drawlib/_builder/doc_builder/exporter_docx.py`
    - `src/drawlib/_slide/compiler.py` / `src/drawlib/_slide/compiler_pptx.py`
    - `src/drawlib/_builder/image_builder.py`（スタンドアロン `.py` スクリプトおよび `.md` 画像抽出の並列化）
    - `src/drawlib/_cli/commands/build.py`（全 7 サブコマンドへの `-w` / `--workers` オプション追加）
  - **ドキュメント・ルール更新対象**:
    - `src/drawlib/_rules/cli.md`, `src/drawlib/_rules/api.md`
    - `docs_src/api/{en,ja}/27_tools.md`, `docs_src/api/{en,ja}/28_cli.md`
    - `docs_src/site/{en,ja}/09_doc_builder_and_cli/cli_reference.md`, `caching_and_cicd.md`
    - `docs_src/architecture/en/05_document_and_slide_builders/`

---

## 1. 背景とボトルネック分析

### 1.1. 現状の課題
- 現在 `drawlib build` の全サブコマンド（`html`, `markdown`, `pdf`, `docx`, `slide`, `pptx`, `image`）は単一プロセス・1 コアで直列実行されている。
- キャッシュが空（コールドビルド、`--no-cache`、またはバージョン更新直後）の状態で大規模プロジェクト（例：`docs_src/site/` 225 ファイル、マルチフレーム `Animation` 多数）をビルドすると、8〜16 コア搭載マシンであっても 1 コア 100% 張り付きとなり完了まで **20〜30 分** を要する。

### 1.2. なぜスレッド並列ではなくプロセス並列が必要か
1. **グローバルシングルトン状態の競合**:
   - Drawlib の描画エンジンおよび Matplotlib はプロセス単位のグローバル状態（`drawlib._core.l4_canvas.canvas` シングルトン、`drawlib.styles.Styles` / `Colors`、`drawlib.utils`、`CanvasBase.DEFAULT_DPI`、`os.chdir()`、`sys.path`）を直接書き換えながら動作する。
   - そのため `ThreadPoolExecutor` で並列実行するとキャンバス状態やスタイルが相互破壊される。
2. **GIL 制約の回避**:
   - 図解のレイアウト計算・ベジェ分割・Matplotlib パッチ生成・Pillow Median Cut 減色／WebP エンコードは CPU バウンド処理であり、マルチコア性能を引き出すには別プロセス空間（`ProcessPoolExecutor`）への分散が不可欠である。
3. **時間配分の偏り（Amdahl の法則）**:
   - ビルド全体の **95% 以上** はキャッシュミス時の図解・アニメーション描画（`DrawlibBlockProcessor.render_block_to_file` / `DrawlibExecuter`）が占めており、Markdown パース・HTML テンプレート展開・DOCX OpenXML 構築・SEO メタ生成自体は合計数百ミリ秒で完了する。

---

## 2. アーキテクチャ選択肢の比較

| 比較軸 | **案A：2フェーズ「事前並列プリレンダ ＋ 既存コンパイラ逐次結合」【推奨】** | 案B：ページ／チャプター単位でのコンパイラ丸ごと並列化 | 案C：ブロック出現ごとの単発 `mp.Process` 起動 |
| :--- | :--- | :--- | :--- |
| **概要** | 対象 `.md`/`.py` から未キャッシュ図解ジョブを一括抽出し、`ProcessPoolExecutor` で並列描画＆親プロセスでキャッシュ保存後、既存コンパイラを無変更で走らせる | `html.py`, `merger.py`, `exporter_docx.py`, `_slide/compiler.py` の各ファイルループ自体をマルチプロセス化する | `render_block_to_file` 内で毎回 `mp.Process` を spawn して描画する |
| **負荷分散の粒度** | **◎ ブロック／スクリプト単位**（1 ページに重い `Animation` が 5 個あっても 5 ワーカーに均等分散できる） | △ ファイル単位（重いアニメーションが集中する 1 ページがボトルネックになりやすい） | △ 1 個ずつ直列待ちになるか制御が複雑 |
| **既存コンパイラへの影響** | **◎ 極めて小さい**（目次生成・リンク書き換え・`sitemap.xml`・DOCX 単一 `Document` 構築に一切手を入れる必要がない） | ✕ 7 系統のコンパイラすべてで IPC 集約・順序復元・共有状態分離の改修が必要 | ○ 小さい |
| **SQLite (`cache.db`) 競合** | **◎ 完全ゼロ**（親プロセス 1 つだけが `get()` / `put()` を行う Single-Writer 構成） | △ 複数ワーカーから同時 `put()` が発生しロック待ちが起きやすい | ○ 親で書けば回避可 |
| **全件キャッシュヒット時** | **◎ オーバーヘッド 0ms**（ミス 0 件ならワーカープール自体を起動しない） | △ ワーカー起動＋Matplotlib import（約 0.5〜1.0 秒）が無駄に走る | ◎ ヒット時は起動しない |
| **ワーカー起動コスト** | **◎ ワーカーあたり初回 1 回のみ**（プール再利用） | ◎ 初回 1 回のみ | ✕ ブロック数（数百回）分の Python + Matplotlib 起動コストが発生 |

以上の通り、保守性・スループット・キャッシュ安全性・決定論性のすべてにおいて優れる **案A（事前並列プリレンダ ＋ 既存コンパイラ逐次結合）** を採用する。

---

## 3. 詳細設計（案A）

### 3.1. 全体データフロー

```text
[入力 .md / .py 群]
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 1: ジョブ収集 & キャッシュ選別（親プロセス・シングルスレッド）    │
│  1. 重複出力パス検査（既存の check_document_output_duplicates 等）      │
│  2. 全対象からユニークな RenderJob を抽出（i18n 共有画像は 1 件に統合） │
│  3. BuildImageCache.get() で照会 → ヒット分は即時復元 / スキップ        │
│  4. ミスが 0〜1 件 or workers==1 ならワーカーを起動せず Phase 3 へ      │
│  5. ミス分を Longest-Job-First（Animation 優先 → 行数降順）にソート     │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ キャッシュミス RenderJob 群
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 2: マルチプロセス並列レンダリング（ProcessPoolExecutor）          │
│  [Worker 1]  [Worker 2]  ...  [Worker N]                                │
│    ・chdir(src_dir) / sys.path 設定 / SlideContext(idx, total) 復元     │
│    ・load_styles_and_utils() 実行 → コード exec() → 画像バイト列生成    │
│    ・ファイル出力型は target_abs へアトミック書き込み                   │
│                                   │                                     │
│                                   ▼ as_completed()                      │
│  [親プロセス Single-Writer]                                             │
│    ・BuildImageCache.put() を単一コネクションで順次コミット（競合ゼロ） │
│    ・embed_images & --no-cache 時はインメモリ prerendered_blobs に保持  │
│    ・進捗バー（render: k/M [####....]）をリアルタイム更新               │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 3: 既存のドキュメント組み立て（親プロセス・数ミリ秒〜数百ミリ秒） │
│  ・build_html / build_markdown / build_pdf / build_docx /               │
│    build_slide / build_pptx がそのまま実行                              │
│  ・全ブロックが _rendered_targets / cache / prerendered_blobs に即ヒット│
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 3.2. ワーカー数解決仕様（`resolve_build_workers`）

CLI オプション（`-w` / `--workers`）・Python API 引数（`workers`）・環境変数（`DRAWLIB_BUILD_WORKERS`）の優先順位と解決ルールを `src/drawlib/_builder/_common/parallel.py` に集約する。

1. **優先順位**:
   1. 明示指定された CLI `-w` / `--workers` または Python API `workers=...`（デフォルト `"auto"` 以外が指定された場合、または環境変数未設定時）
   2. 環境変数 `DRAWLIB_BUILD_WORKERS`（`"auto"` または正の整数文字列）
   3. デフォルト値：`"auto"`
2. **値の意味**:
   - `"auto"`（または整数 `0`）：`max(1, min((os.cpu_count() or 1) - 1, 8))`（すなわち **`1 <= (CPUコア数 - 1) <= 8`**）
     - **`CPUコア数 - 1` とする理由**: 親プロセス（SQLite `cache.db` コミット・進捗管理）および開発者の OS / エディタ / ブラウザ用に 1 コア分の余力を残し、ビルド中も端末がフリーズしないようにする（1〜2 コアの軽量コンテナ等では自動的に `1`＝直列となりプロセス起動コストも節約できる）。
     - **上限 `8` の理由**: Matplotlib + Pillow + フォントキャッシュを展開したワーカーは 1 プロセスあたり約 120〜180 MB の RSS メモリを消費する。多コア環境で無制限に起動するとメモリ圧迫やプロセス生成コストが勝るため、`"auto"` 時は最大 8 ワーカーを安全上限とする。
   - 正の整数 `N >= 1`（例：`4`, `"4"`, `1`, `"1"`）：指定値をそのまま使用する（例：全コア使い切りたい場合の `--workers 16` や、デバッグ・直列強制用の `--workers 1` / `-w 1`）。
   - 不正値（負数、`"0"` 以外の非正整数、数値でも `"auto"` でもない文字列）：`ValueError("workers must be 'auto' or a positive integer >= 1.")` を送出。
3. **自動直列フォールバック条件**（以下のいずれかに該当する場合はワーカープールを起動せず親プロセスで処理）：
   - 解決後の `effective_workers == 1`
   - キャッシュミスした実描画対象ジョブ数が `0` 件または `1` 件
   - `drawlib build image --disable-auto-clear`（`mode == "none"`：ファイル間でキャンバス状態を引き継ぐ仕様のため直列必須）

---

### 3.3. ジョブ定義モデルと Longest-Job-First スケジューリング

`ProcessPoolExecutor`（`spawn` コンテキスト互換）で安全にシリアライズできるよう、すべてプリミティブ型からなる frozen dataclass で定義する。

```python
@dataclass(frozen=True)
class BlockRenderJob:
    """単一の ```drawlib コードブロック（または <script type="text/drawlib">）描画タスク。"""

    job_id: str                           # 重複排除・結果紐付けキー（target_abs または cache_key）
    code: str                             # 実行する Python 描画コード
    source_filename: str                  # 元 .md / .html ファイル絶対パス
    line_number: int                      # エラー報告用の開始行番号
    target_abs_path: str | None           # ファイル書き出し先（embed_images のみの場合は None）
    cache_target_file: str                # キャッシュキー計算用ターゲットパス
    image_format: str                     # "png" | "webp" | "svg" | "gif" | "apng"
    dpi: int | None                       # None（標準 100）または 200 (docx) / 240 (pptx) 等
    grid: bool | None                     # None | True
    styles_path: str | None               # 解決済み styles.py 絶対パス
    utils_path: str | None                # 解決済み utils.py 絶対パス
    project_root: str | None              # プロジェクトルート絶対パス
    slide_ctx: tuple[int, int] | None     # slide / pptx 時の (slide_index, total_slides)
    static_anim_frame: Literal["first", "last"] | None  # pptx 等の静止フレーム化指定
    cache_key: str                        # 親プロセスで事前計算した cache_key（no_cache 時は ""）
    code_hash: str                        # 親プロセスで事前計算した code_hash
    config_hash: str                      # 親プロセスで事前計算した config_hash
    write_cache: bool                     # 完了後に cache.db へ保存するか（ブロック単位 no-cache 考慮）


@dataclass(frozen=True)
class BlockRenderResult:
    """ワーカーから親プロセスへ返却する描画結果。"""

    job_id: str
    normal_bytes: bytes
    grid_bytes: bytes | None
```

#### スケジューリング順序（Longest-Job-First）
マルチフレーム `Animation(...)` は 1 ブロックで数十フレームを描画するため、通常の静止画ブロックの 10〜40 倍の時間がかかる。これがキュー末尾に残ると残り全ワーカーがアイドル待機するため、ワーカー投入前に以下の優先度キーで降順ソートする：
1. `"Animation(" in job.code`（アニメーションブロックを最優先で先行投入）
2. `job.image_format in {"webp", "gif", "apng"}`
3. `len(job.code)`（コード量の大きい複雑な図解を優先）

---

### 3.4. ワーカープロセスの実行不変条件（直列実行との 100% 互換性保証）

ワーカー関数 `_execute_block_render_job(job: BlockRenderJob) -> BlockRenderResult` は、現行 `DrawlibBlockProcessor.render_block_to_file()` と完全に同一の副作用境界を再現する：

1. **カレントディレクトリと `sys.path` の隔離設定**:
   - `src_dir = os.path.dirname(job.source_filename)` に `os.chdir(src_dir)` し、`src_dir` を一時的に `sys.path[0]` へ追加（相対パスの CSV / GeoJSON / 画像読み込みをサポート）。ジョブ終了時の `finally` で `sys.path` を復元。
2. **スタイル・ユーティリティの毎回クリーンロード**:
   - あるブロック内で `Styles.Neutral.shape_fill_color = ...` のような破壊的変更が行われても次ジョブへ漏れないよう、現行 `processor.py`（198–203 行目）と同様にジョブごとに `_evict_project_utils_module()` ＋ `load_styles_and_utils(job.styles_path, job.utils_path, shared_globals)` を実行する。
3. **`SlideContext` と `DEFAULT_DPI` の正確な復元**:
   - `job.slide_ctx` が指定されている場合は `set_slide_context(index=idx, total=total)` を設定し、`finally` で `reset_slide_context()`。
   - `job.dpi` が指定されている場合は `CanvasBase.DEFAULT_DPI` を設定し、`finally` で復元。
4. **アトミックなファイル書き出し**:
   - `job.target_abs_path` がある場合、一時ファイル（`<dir>/.tmp_<pid>_<name>`）に書き出してから `os.replace()` で確定させ、同時にバイト列を `BlockRenderResult` に載せて親プロセスへ返す（ディスク再読み込み不要でそのまま `cache.put()` 可能）。
   - `job.static_anim_frame` 指定時（PPTX ビルド等）はワーカー側で静止画フレーム抽出まで完了させる。

---

### 3.5. `--no-cache` および `embed_images=True`（PDF / DOCX）への対応

- **`no_cache=False`（通常時）**:
  - 親プロセスが `BlockRenderResult` を受け取り次第 `cache.put(...)` を実行し、ファイル書き出し型では `cache.rendered_targets.add(target_abs_path)` も記録する。
  - Phase 3 の `merger.py`（PDF: `embed_images=True`）や `exporter_docx.py`（DOCX）では `render_block_to_data_url()` が `self._cache.get(cache_key)` に `< 1 ms` でヒットするため再描画は一切起きない。
- **`no_cache=True`（`--no-cache` 指定時）**:
  - ファイル書き出し型（`html`, `markdown`, `slide`, `image`）は Phase 2 で出力先ファイルが生成済みかつ `rendered_targets` に登録されるため、Phase 3 で即スキップされる。
  - インライン埋め込み型（`pdf`, `docx`）ではディスク上に永続出力先パスを持たないため、`DrawlibBlockProcessor` にオプショナルな `prerendered_blobs: dict[str, bytes]`（キー：`(source_filename, cache_target_file, fmt, dpi)` のハッシュ）を持たせる。Phase 2 で格納したバイト列を Phase 3 で参照して消費（`pop` でメモリ解放）することで、**`--no-cache` 指定時の PDF / DOCX ビルドでも `cache.db` を一切読み書きせずにフルマルチコア高速化**を実現する。

---

### 3.6. スタンドアロン `.py` スクリプト並列化（`drawlib build image`）

`src/drawlib/_builder/image_builder.py` の `DrawlibExecuter` についても同じ設計思想で並列化する：

1. **事前重複出力チェック**: 既存の `check_duplicate_script_outputs()` を親プロセスで実行。
2. **キャッシュヒット除外**: 単一静的 `save()` スクリプトは親プロセスで `_try_cache_or_prepare()` 相当の判定を行い、ヒット分はワーカーを起動せず即復元。
3. **ワーカー並列実行（`mode in {"auto_clear", "auto_initialize"}` かつミス `>= 2` 件）**:
   - 各 `.py` スクリプトを独立ジョブ `ScriptRenderJob` として `ProcessPoolExecutor` で実行。
   - ワーカー内で `_wrapped_save` をフックし、生成された `(resolved_abs, img_bytes, grid_bytes, cache_info)` のリストを親プロセスへ返却。
   - 親プロセス側で動的パスを含めた `_runtime_seen_outputs` の重複チェックと `self._cache.put()` を行う（重複検出時は直列時と同じ `Duplicate output file detected` エラーを送出）。

---

### 3.7. 必須の並行安全性ガード（4 項目）

#### ① 初回アセット自動ダウンロードのプロセス間ロック（`l3_external/_download.py`）
- **課題**: 現状 `download_if_not_exist()` にはプロセス間ロックがないため、アセット未取得のクリーン環境で 8 ワーカーが同時に同じフォント（例：`font_roboto`）やアイコン（`icon_phosphor`）を必要とすると、8 プロセスが同時に GitHub Releases からダウンロード＆同一ディレクトリへ ZIP 展開して競合する（`pytest -n auto` 実行時にも発生し得る潜在課題）。
- **対策**: `src/drawlib/_builder/_common/browser.py` の `_browser_install_lock()` と同様のクロスプラットフォーム排他ロック（POSIX: `fcntl.flock` / Windows: `msvcrt.locking`）を `_core/l3_external/_download.py` に導入する。
  - ロックファイル：`<cached_assets_dir>/.locks/<pkg.name>.lock`
  - ロック取得後に再度 `is_file_exist() and is_checksum_correct()` をダブルチェックし、先行ワーカーが展開済みならダウンロードを即スキップする。

#### ② `multiprocessing.Pool` ではなく `ProcessPoolExecutor`（非デーモン）を使用
- **課題**: 標準ライブラリの `multiprocessing.Pool` はワーカーを `daemon=True` で起動するため、図解コード内で `get_dimage_from_code()`（内部で `mp.Process` を起動）を呼ぶと `AssertionError: daemonic processes are not allowed to have children` でクラッシュする。
- **対策**: 非デーモンワーカーを使用する `concurrent.futures.ProcessPoolExecutor(max_workers=...)` を採用する。起動方式は Windows / macOS / Linux（Python 3.14 含む）で挙動が統一され Matplotlib / FreeType の fork 安全性問題も起きない `mp.get_context("spawn")` を基本とする。

#### ③ エラー発生時の即時フェイルファストと行番号付きトレース伝播
- いずれかのジョブで例外（構文エラー、`ValidationError`、ランタイムエラー等）が発生した場合：
  - 親プロセスで `executor.shutdown(wait=False, cancel_futures=True)` を呼び出して未開始キューを即座に破棄し、不要な待ち時間を防ぐ。
  - ワーカー側で整形したトレース情報（対象 `.md`/`.py` ファイルパス・ブロック行番号・元の例外メッセージ）を親プロセスで再送出し、既存の CLI エラーハンドラ（`_handle_build_error`）と完全に互換な出力を維持する。

#### ④ プログレス表示 UX の整理
- **直列実行時（`-w 1` / `--workers 1` またはミス `<= 1` 件）**: 既存のファイル単位表示（`file: 1/17 /index.md images: 2/2 : #################### 100%`）を 100% 維持（既存の CLI 出力テストとも完全互換）。
- **並列プリレンダ実行時（`effective_workers >= 2` かつミス `>= 2` 件）**:
  - Phase 2 で `Rendering 142 diagrams across 8 workers: [##########..........]  50% (71/142)` の進捗を表示（TTY 時は `\r` インプレース更新、非 TTY / CI 時は完了サマリー行のみ出力、`quiet` 時は非表示）。
  - Phase 3 のページ組み立てはキャッシュヒットにより一瞬で通過する。

---

## 4. CLI・Python API 変更仕様

### 4.1. CLI オプション追加（`src/drawlib/_cli/commands/build.py`）
全 7 サブコマンド（`image`, `markdown`, `html`, `pdf`, `docx`, `slide`, `pptx`）に共通オプション `-w` / `--workers` を追加する（短縮フラグ `-w` は既存オプション `-h`, `-o`, `-f`, `-s`, `-u`, `-g`, `-t` と一切競合しない）：

```python
workers: Annotated[
    str,
    typer.Option(
        "-w",
        "--workers",
        help="Number of parallel worker processes for diagram rendering ('auto' or positive integer; 1 = sequential).",
    ),
] = "auto"
```

```bash
# デフォルト（--workers auto: 1 <= (CPUコア数 - 1) <= 8 で自動並列化）
drawlib build html docs_src/site/ -o docs/

# ワーカー数を明示指定
drawlib build html docs_src/site/ -o docs/ --workers 4
drawlib build pdf report_src/ -w 8

# 1 ワーカー直列実行を強制（デバッグ時など）
drawlib build html docs_src/site/ -o docs/ -w 1
```

### 4.2. Python API 引数追加（`drawlib.tools.build_*`）
後方互換性を 100% 保つため、各ビルド関数のキーワード専用引数に `workers: int | Literal["auto"] = "auto"` を追加する（`ProcessPoolExecutor(max_workers=...)` の用語とも統一）：
- `build_image(..., *, ..., no_cache: bool = False, workers: int | Literal["auto"] = "auto") -> list[str]`
- `build_markdown(..., *, ..., no_cache: bool = False, workers: int | Literal["auto"] = "auto") -> str`
- `build_html(..., *, ..., no_cache: bool = False, css_mode: str = "external", workers: int | Literal["auto"] = "auto") -> str`
- `build_pdf(..., *, ..., no_cache: bool = False, timestamp: bool = False, workers: int | Literal["auto"] = "auto") -> str`
- `build_docx(..., *, ..., no_cache: bool = False, timestamp: bool = False, workers: int | Literal["auto"] = "auto") -> str`
- `build_slide(..., *, ..., no_cache: bool = False, workers: int | Literal["auto"] = "auto") -> str`
- `build_pptx(..., *, ..., no_cache: bool = False, timestamp: bool = False, workers: int | Literal["auto"] = "auto") -> str`

---

## 5. 実装ステップと検証計画

実装は以下の 5 ステップで段階的かつ安全に進める。

### Step 1: `l3_external` プロセス間アセットロックの実装・単体テスト
1. `src/drawlib/_core/l3_external/_download.py` にクロスプラットフォーム排他ファイルロック（`<cached_assets>/.locks/<pkg.name>.lock`）とロック後の再チェックを実装。
2. `tests/drawlib/_core/l3_external/test_download_lock.py` を作成し、複数プロセス／スレッドから同時に `download_if_not_exist()` を呼んでも `pkg.download_and_extract()` が **1 回だけ** 実行されることを検証。

### Step 2: 共通並列レンダリング基盤 `_builder/_common/parallel.py` の実装
1. `resolve_build_workers()`（引数・`DRAWLIB_BUILD_WORKERS`・`"auto"` 上限 8・バリデーション）を実装。
2. `BlockRenderJob` / `BlockRenderResult`、LJF ソート、`ProcessPoolExecutor`（`spawn`）ワーカー実行、親プロセス Single-Writer キャッシュ保存、進捗バー、例外時 `cancel_futures=True` を実装。
3. `DrawlibBlockProcessor` に `prerendered_blobs` 参照フックを追加。

### Step 3: 各ビルダおよび CLI への統合
1. **ドキュメント系**: `compiler/html.py`（`site` / `doc` / `catalog`）、`compiler/markdown.py`、`merger.py`（PDF）、`exporter_docx.py`（DOCX）に事前並列プリレンダ呼び出しを接続。
2. **スライド系**: `_slide/compiler.py`（`slide` および `pptx` 経由の呼び出し、`SlideContext`・`static_anim_frame` 対応）に接続。
3. **画像ビルド系**: `image_builder.py`（スタンドアロン `.py` スクリプト群および `.md` 画像抽出）に接続（`--disable-auto-clear` 時は自動で `workers=1` フォールバック）。
4. **CLI**: `_cli/commands/build.py` の全 7 サブコマンドに `-w` / `--workers` を追加。

### Step 4: ユニット・結合テスト & 静的解析
1. `tests/drawlib/doc_builder/test_parallel_build.py` を追加し、以下を網羅検証：
   - **決定論的等価性**: 同一プロジェクトに対する `-w 1` と `-w 4` のビルド出力（HTML / PDF / DOCX / Slide / Standalone Image）および `cache.db` エントリが一致すること。
   - **キャッシュ整合性**: 1 回目 `-w 4` で生成された `cache.db` に対し、2 回目ビルドでキャッシュミス 0 件（ワーカー未起動・高速完了）となること。
   - **`--no-cache` 並列動作**: `--no-cache -w 4`（HTML および `embed_images=True` の PDF/DOCX）で `cache.db` を作らずに並列描画され、二重描画が起きないこと。
   - **ネスト `get_dimage_from_code()`**: 並列ワーカー内の図解で `get_dimage_from_code()` が正常動作すること。
   - **エラー伝播・重複検出**: 1 ブロックが例外を送出した場合や動的重複出力がある場合に適切なエラーメッセージで即失敗すること。
2. `./dcli code-check all` および `./dcli test all`（Python 3.12 & Python 3.14）を実行し全件パスを確認。

### Step 5: 実プロジェクトでの速度計測（ドッグフーディング）& ドキュメント更新
1. `docs_src/architecture/` や `docs_src/site/` で `--no-cache -w 1` vs `--no-cache -w 8` の実測ビルド時間を比較検証。
2. API リファレンス（`docs_src/api/{en,ja}/27_tools.md`, `28_cli.md` — `test_api_docs_completeness.py` 準拠）、CLI ガイド（`docs_src/site/{en,ja}/09_doc_builder_and_cli/`）、埋め込みエージェントルール（`src/drawlib/_rules/cli.md`, `api.md`）を更新し、`./dcli docs build` & `--check` を通過させる。

---

## 6. Verification Plan（セキュリティ検証計画）

### Automated Security Check & Design Safeguards
- **Input Validation**: `-w` / `--workers` および環境変数 `DRAWLIB_BUILD_WORKERS` に対して `"auto"` または正の整数のみを許可する厳格なバリデーションを実施し、不正入力時は即座に `ValueError` で拒否する。
- **Path & File System Safety**: アセット排他ロック名には正規表現による安全な識別子サニタイズ（`[^a-zA-Z0-9_.-]` 除去および `os.path.basename` 相当の境界保証）を適用し、ワーカーの画像ファイル出力は出力先ディレクトリ内の一時ファイルから `os.replace()` でアトミックに確定させる。SQLite キャッシュ操作はすべて既存のプレースホルダ付きパラメータ化クエリを維持する。
- **Security Scanner & Audit**: 新規作成ファイルに対してセキュリティスキャナ（Ruff Bandit `S` ルールおよび SecureCoder スキャナ）を実行し、脆弱性が 0 件であることを確認する。

