# 条件付き夜間フルテスト CI 導入計画書 (Conditional Nightly Cross-OS Matrix Plan)

- **作成日**: 2026-11-06
- **ステータス**: 保留（当面は日常の `ubuntu-latest` 高速 CI ＋ 必要時の手動 `workflow_dispatch` で運用し、自動化が必要になった段階で導入する）
- **対象ファイル**:
  - `.github/workflows/ut_github.yml`
  - `.github/workflows/ut_full.yml`（案A採用時に新規作成）
  - `docs_src/architecture/en/07_test_architecture/01_test_hierarchy_and_strategy.md`

---

## 1. 背景と目的

- **現状の構成**:
  - 日常の `push` / `pull_request`（`.github/workflows/ut_github.yml`）は、フィードバック速度とランナー効率を優先して `ubuntu-latest`（Python `3.12`、並列実行）のみを実行している。
  - マルチ OS（`ubuntu-latest`, `windows-latest`, `macos-latest`）× マルチ Python（`3.11`, `3.12`, `3.13`）の 9 ジョブ・フルマトリクスは、GitHub Actions UI からの手動実行（`workflow_dispatch` の `mode: full`）で任意に呼び出せるようにしている。
- **本プランの目的**:
  - 手動フルテストの実行忘れによる Windows 特有の不具合（パス区切り `\`、`cp932` エンコーディング、ファイルロック等）や Python 3.11 / 3.13 固有の非互換の見逃しを防ぎたくなった場合に備える。
  - 単純な毎晩実行（無変更の日も毎日 9 ジョブ空回りする構成）ではなく、**「その日に `src/drawlib/`・`tests/`・`pyproject.toml` に変更があった日の夜だけフルテストを回す」** 条件付き夜間バッチの設計を定義する。

### 導入を検討するトリガー（目安）
- 手動 `workflow_dispatch` の実行頻度が下がり、リリース直前にまとめて OS / Python バージョン固有の修正が発生するようになった場合。
- コントリビューターや PR 数が増え、`main` マージ後のクロスプラットフォーム回帰テストを自動化したい場合。

---

## 2. アーキテクチャ選択肢の比較

GitHub Actions の `on: schedule` には YAML レベルの `paths:` フィルタが存在しないため、「軽量な変更判定ジョブ（約 5〜10 秒）」を先頭に置き、対象パスにコミットがあった日のみ後続の 9 ジョブを起動する 2 段構成とする。

| 項目 | 案A：専用ワークフロー分離 (`ut_full.yml`) **【推奨】** | 案B：既存 `ut_github.yml` への統合 |
| :--- | :--- | :--- |
| **役割分担** | ・`ut_github.yml`: `push` / `pull_request` 専用（Linux 単体）<br>・`ut_full.yml`: 夜間 `schedule` ＋ 手動 `workflow_dispatch` 専用 | `ut_github.yml` 1本で `push` / `pull_request` / `schedule` / `workflow_dispatch` すべてを処理 |
| **Actions 履歴の見やすさ** | **◎ 非常にクリーン**（変更がない日の「5秒スキップ履歴」が普段の `Unit Tests` 一覧に混ざらない） | △ 毎晩 1 件ずつ `schedule` 実行履歴が `Unit Tests` 一覧に並ぶ |
| **README バッジへの影響** | 日常バッジ（`ut_github.yml`）と分離される（必要ならフルテスト用バッジも別途追加可能） | 夜間フルテストで Windows 等が落ちた際にも既存の `Unit Tests` バッジが赤くなる |
| **保守性** | 条件分岐がシンプルで読みやすい | イベント種別ごとの `if:` / `matrix:` 条件式がやや複雑になる |

---

## 3. 詳細設計（推奨：案A `ut_full.yml` 分離方式）

### 3.1. 変更検知ロジックの重要ポイント（実装時の落とし穴防止）

1. **`fetch-depth: 0`（または `--shallow-since`）の指定が必須**:
   - `actions/checkout@v4` のデフォルトは `fetch-depth: 1`（最新 1 コミットのみ取得）である。
   - デフォルトのままにすると、「日中に `src/drawlib/` を変更し、夜に `README.md` だけ修正して Push した日」に最新コミットしか見えず、変更なしと誤判定されてしまう。
   - 判定ジョブでは軽量な履歴取得（`fetch-depth: 50` または `fetch-depth: 0`）を行い、過去 25 時間分すべてのコミットを検査する。
2. **時間窓は `25 hours ago` に設定**:
   - GitHub Actions の `schedule`（cron）は混雑時に数分〜30 分程度遅延することがあるため、境界時刻のコミット取りこぼしを防ぐ目的で `24 hours` ではなく `25 hours ago` を使う。
3. **監視対象パス**:
   - `src/drawlib`（ライブラリ本体）
   - `tests`（テストコード・リファレンス画像）
   - `pyproject.toml`（依存パッケージ・Python 要件の変更）

---

### 3.2. `.github/workflows/ut_full.yml` 実装イメージ

以下は、日本時間 深夜 03:00（UTC `18:00`）に起動する場合のワークフロー定義案である。

```yaml
name: "Unit Tests (Full Matrix)"
run-name: event=${{ github.event_name }}, mode=${{ inputs.mode || 'full' }}, branch=${{ inputs.branch || github.ref_name }}

on:
  schedule:
    # 毎日 18:00 UTC (03:00 JST) に変更有無をチェック
    - cron: '0 18 * * *'
  workflow_dispatch:
    inputs:
      mode:
        description: 'Test matrix scope'
        required: true
        default: 'full'
        type: choice
        options:
          - 'full'
          - 'all-os'
          - 'ubuntu-only'

      python_version:
        description: 'Python version (ignored when mode is full)'
        required: true
        default: '3.12'
        type: choice
        options:
          - '3.11'
          - '3.12'
          - '3.13'

      branch:
        description: 'Branch'
        required: true
        default: 'main'
        type: string

permissions:
  contents: read

jobs:
  check-changes:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    outputs:
      should_run: ${{ steps.diff.outputs.should_run }}
    steps:
      - name: Check out recent commit history
        uses: actions/checkout@v4
        with:
          fetch-depth: 50

      - name: Check commits in last 25 hours
        id: diff
        shell: bash
        run: |
          CHANGED=$(git log --since="25 hours ago" --name-only --pretty=format: -- src/drawlib tests pyproject.toml | sed '/^$/d' | head -n 20)
          if [ -n "$CHANGED" ]; then
            echo "Changes detected in target paths within the last 25 hours:"
            echo "$CHANGED"
            echo "should_run=true" >> "$GITHUB_OUTPUT"
          else
            echo "No changes in src/drawlib, tests, or pyproject.toml in the last 25 hours. Skipping full matrix."
            echo "should_run=false" >> "$GITHUB_OUTPUT"
          fi

  full-matrix:
    needs: [check-changes]
    if: |
      always() && (
        github.event_name == 'workflow_dispatch' ||
        needs.check-changes.outputs.should_run == 'true'
      )
    strategy:
      fail-fast: false
      matrix:
        os: ${{ (github.event_name == 'schedule' || inputs.mode == 'full' || inputs.mode == 'all-os') && fromJSON('["ubuntu-latest", "windows-latest", "macos-latest"]') || fromJSON('["ubuntu-latest"]') }}
        python_version: ${{ (github.event_name == 'schedule' || inputs.mode == 'full') && fromJSON('["3.11", "3.12", "3.13"]') || fromJSON(format('["{0}"]', inputs.python_version || '3.12')) }}
    uses: ./.github/workflows/ut_template.yml
    with:
      os: "${{ matrix.os }}"
      python_version: "${{ matrix.python_version }}"
      install_from: 'github'
      branch: "${{ inputs.branch || '' }}"
      lib_version: 'latest'
```

### 3.3. 案A導入時の `.github/workflows/ut_github.yml` 側の整理

`ut_full.yml` に手動 `workflow_dispatch` を移管する場合は、`ut_github.yml` を純粋な `push` / `pull_request` 用の軽量ワークフローにスリム化できる（または `ut_github.yml` にも単体実行用の `workflow_dispatch` を残してもよい）。

---

## 4. 運用上の留意事項

1. **変更がない日の Actions 履歴**:
   - `check-changes` ジョブのみが約 5〜8 秒実行され、`full-matrix` は `Skipped` となって正常終了（緑チェック）する。Windows / macOS ランナーは一切消費されない。
2. **GitHub Actions の 60 日間非アクティブ制限**:
   - パブリックリポジトリで 60 日間一度もコミットがない場合、GitHub の仕様により `schedule` トリガーが自動停止される（Actions タブから 1 クリックで再有効化可能）。
3. **ドキュメント同期**:
   - 導入時は `docs_src/architecture/en/07_test_architecture/01_test_hierarchy_and_strategy.md` の CI 構成説明も合わせて更新し、`./dcli docs build architecture` で反映する。
