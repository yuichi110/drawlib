# Drawlib 起動時間およびテスト実行速度のパフォーマンス分析レポート

本レポートは、Drawlib の起動およびテスト実行の遅延について、スタイル作成ループの影響有無を調査し、真のボトルネックの特定と具体的な改善施策をまとめた技術レポートです。

---

## 1. 調査サマリー (Executive Summary)

- **スタイル作成ループの影響**: **ボトルネックではありません（影響度: 0.7% / 約 0.055 秒）**。
  - 今回追加された `GoogleColors`（105色）および `StylesGoogle`（約1,050スタイル）の生成ループを含め、全スタイルのループ処理時間は合計 **55.6 ms** です。
  - さらに、モジュール読み込み時にシングルトンとして 1 回生成されるのみで、描画中やテスト実行中に再ループすることはありません。
- **真のボトルネック**: **`drawlib` インポート時の同期処理（合計 約 7.16 秒）**。
  1. **Phosphor アイコンの `@validate_call`**: **4.24 秒 (59.3%)**
  2. **`builder` のトップレベル無条件インポート**: **1.81 秒 (25.2%)**
  3. **GCP PNG アイコンのインポート**: **0.83 秒 (11.6%)**
- **テスト遅延の増幅メカニズム**:
  - `tests/cli/` などのテストは `subprocess` 経由で CLI コマンドを起動するため、**CLI コマンド 1 回ごとに毎回 7.16 秒のインポート待機時間が発生** します（例: `test_cli_rules.py` だけで 30 回 × 7.16 秒 ＝ 約 213 秒）。

---

## 2. スタイル作成処理のマイクロベンチマーク

各スタイルカタログの生成関数および属性アクセスの詳細な測定結果です。

### 2.1. スタイル生成関数の実行時間

| 対象関数 | 主な処理内容 | 生成スタイル数 | 実行時間 |
| :--- | :--- | :--- | :--- |
| `_create_default_styles("default")` | 30色 + 10ロールのバリアント展開 | 約 300 個 | **9.7 ms** |
| `_create_default_styles("light")` | Lightテーマのバリアント展開 | 約 300 個 | **10.7 ms** |
| `_create_default_styles("dark")` | Darkテーマのバリアント展開 | 約 300 個 | **15.4 ms** |
| `_create_monochrome_styles()` | 8色 + 6ロールのバリアント展開 | 約 140 個 | **3.2 ms** |
| `_create_google_styles()` | 105色 + 8ロールのバリアント展開 | 約 1,050 個 | **16.6 ms** |
| **全スタイル生成ループ合計** | - | **約 2,100 個** | **55.6 ms (0.055秒)** |

### 2.2. モジュール初期化時間

| モジュール | 行数 | クラス定義・型検証・インスタンス化合計時間 |
| :--- | :--- | :--- |
| `drawlib._preset_styles._style_default` | 1,284 行 | **0.197 秒** |
| `drawlib._preset_styles._style_google` | 1,913 行 | **0.099 秒** |
| `drawlib._preset_styles._style_monochrome` | 321 行 | **0.015 秒** |

### 2.3. 描画時の属性アクセス時間

```python
# 100,000 回の styles.primary_flat アクセス測定
Total time: 0.0099 s (1回あたり 0.10 μs)
```
- Pydantic モデル上のプロパティ・属性アクセスは 1 回あたり約 100 ナノ秒であり、描画ループ内でも実質オーバーヘッドはありません。

---

## 3. インポート時間のプロファイル分析

`python -X importtime -c "import drawlib"` を実行し、起動時の累積時間（Cumulative Time）と自己消費時間（Self Time）を測定しました。

### 3.1. インポート時間内訳グラフ

```text
合計起動時間: 7,159 ms (100.0%)
┌─────────────────────────────────────────────────────────────┬──────────┬────────┐
│ モジュール                                                  │ 累積時間 │ 割合   │
├─────────────────────────────────────────────────────────────┼──────────┼────────┤
│ drawlib._icons.font_icons.phosphor._generated               │ 4,242 ms │  59.3% │
│ drawlib.builder (doc_builder, Pygments, WeasyPrint, 等)     │ 1,806 ms │  25.2% │
│ drawlib._icons.png_icons.gcp._generated                     │   830 ms │  11.6% │
│ drawlib._core (canvas, matplotlib.pyplot, fonts 等)         │   729 ms │  10.2% │
│ drawlib._preset_styles / drawlib.styles                     │   350 ms │   4.9% │
│   └ 内訳: スタイル作成ループ (全5関数)                      │    55 ms │   0.7% │
└─────────────────────────────────────────────────────────────┴──────────┴────────┘
※上位モジュールに重複して含まれる時間があるため、個別割合の合算は 100% を超えます。
```

### 3.2. ボトルネックの技術的詳細

#### ① Phosphor アイコンの `@validate_call` (4.24 秒)
- ファイル: `src/drawlib/_icons/font_icons/phosphor/_generated.py` (32,148 行)
- コード生成された **1,500 個以上** の各アイコン関数すべてに Pydantic の `@validate_call` が付与されています。
- Python インポート時、Pydantic は各関数のシグネチャを走査し、引数・戻り値の型バリデータオブジェクトを 1,500 回連続で同期生成します。
- この Pydantic の初期化コストだけで **4.24 秒** を消費しています。

#### ② `drawlib/__init__.py` の一括先行インポート (1.81 秒)
- ファイル: `src/drawlib/__init__.py`
  ```python
  from drawlib import (
      builder,
      canvas,
      charts,
      diagrams,
      fonts,
      icons,
      images,
      lines,
      math,
      preset_colors,
      preset_styles,
      shapes,
      smartarts,
      styles,
      text,
      tools,
      types,
      utils,
  )
  ```
- ユーザーが `from drawlib.canvas import ...` や `from drawlib.styles import styles` と書いただけで、Python のパッケージ読み込み機構により親パッケージ `drawlib/__init__.py` が必ず読み込まれます。
- その結果、ドキュメントビルダー（Markdown パーサー、WeasyPrint、Pygments）や全アイコンライブラリが無条件に読み込まれます。

---

## 4. テスト実行時間への影響メカニズム

なぜテスト全体の実行に数分〜数十分かかるのか：

1. **インプロセス実行テスト (高速)**:
   - `pytest tests/preset_styles/`: **25 passed in 3.38s** (画像比較 5 件含む)
   - `pytest tests/l3_styles/`: **31 passed in 0.99s**
   - 1 つの Python プロセスで実行されるため、インポートペナルティ（7.16秒）は最初の 1 回のみ。
2. **CLI 関連テスト (極めて低速)**:
   - `tests/cli/` 配下のテスト（`test_cli_rules.py`, `test_cli_export.py`, `test_cli_init.py` 等）は、コマンドライン動作を検証するために `subprocess.run(["drawlib", ...])` を実行します。
   - CLI を 1 回実行するたびに別プロセスが起動するため、**毎回 7.16 秒** のインポートオーバーヘッドが発生します。
   - `test_cli_rules.py` だけで 30 回以上の CLI 呼び出しがあり、これだけで **200 秒（3 分以上）** を消費します。

---

## 5. 具体的・段階的な改善ロードマップ

以下の 3 つの対策を実施することで、起動時間を **7.16 秒 → 0.3 秒以下**（約 95% 削減）に短縮可能です。

### 施策 A: `drawlib/__init__.py` の遅延インポート (Lazy Import / PEP 562)
- **効果**: `builder`, `icons`, `diagrams` の読み込みを、実際に参照されたタイミングまで遅延。
- **削減見込み**: **約 6 秒削減**（単純な `drawlib.canvas` や `drawlib.styles` の読み込みが瞬時完了）。
- **実装方法**:
  Python 3.7+ のモジュールレベル `__getattr__` を使用：
  ```python
  # src/drawlib/__init__.py
  import importlib
  from typing import Any

  _LAZY_MODULES = {
      "builder", "charts", "diagrams", "icons", "smartarts", "tools"
  }

  def __getattr__(name: str) -> Any:
      if name in _LAZY_MODULES:
          module = importlib.import_module(f"drawlib.{name}")
          globals()[name] = module
          return module
      raise AttributeError(f"module 'drawlib' has no attribute '{name}'")
  ```

### 施策 B: Phosphor アイコン生成コードの `@validate_call` 最適化
- **効果**: アイコンモジュール自体のインポート時間を **4.24 秒 → 0.05 秒** に短縮。
- **背景**:
  各アイコン関数は内部関数 `_write(xy=xy, width=width, code=..., angle=angle, style=style)` を呼ぶだけの純粋なラッパーです。
- **改善案**:
  1. 個々の 1,500 関数に `@validate_call` を付けるのをやめ、呼び出し先の `_write` 側で検証する。
  2. または、コード生成スクリプト（`tools/dcli/gen_icon.py`）を修正し、オーバーヘッドのない軽量な型検証に切り替える。

### 施策 C: CLI エントリポイントの軽量化
- **効果**: CLI テスト（`dcli test cli`）全体の実行時間が 5 分以上から 30 秒程度に激減。
- **実装方法**:
  - `drawlib._cli.main` は現在 `import drawlib` を行っています。
  - サブコマンド（例: `rules`, `version`, `init` など）で不要な重いモジュールをインポートしないよう、サブコマンド実行関数内で遅延インポートする。

---

## 6. 実施結果 (Optimization Results)

ご提案いただいた「集約先への `@validate_call` 移動」を Phosphor および GCP アイコンに適用しました。

### 6.1. 適用前後のパフォーマンス比較

| 項目 | 最適化前 (Before) | 最適化後 (After) | 改善効果 |
| :--- | :--- | :--- | :--- |
| **`import drawlib` 全体起動時間** | **7.16 秒** | **2.12 秒** | **約 5.04 秒短縮 (3.4倍高速化)** |
| **Phosphor アイコンモジュール** | **4.24 秒** | **0.15 秒** | **約 28 倍高速化** |
| **GCP アイコンモジュール** | **0.83 秒** | **0.03 秒** | **約 27 倍高速化** |

### 6.2. 安全性と機能の維持
- **静的解析・型補完**: 各関数の型アノテーション（`Coordinate`, `PosFloat`, `Angle`, `Style`）および Docstring はそのまま維持（Ty / Pyright / Docstring チェック 100% パス）。
- **ランタイム検証**: 集約先（`FontIconProvider.write`, `PngIconProvider.write`）で Pydantic による引数の型・値検証を 100% 担保。
- **ユニットテスト**: `tests/l6_icons/` の全 17 件が完全一致（100.00% Exact pixel match）でパス。

---

## 7. まとめ

- ご懸念の「スタイル作成ループ」は合計 **55ms** であり、問題ありません。
- 最大のボトルネックであった **Phosphor および GCP アイコンの `@validate_call`（約 5.07 秒）が集約化により 0.18 秒へ短縮** され、drawlib の起動時間が **7.16 秒 → 2.12 秒** に大幅改善されました。
- 今後さらに高速化（2.12 秒 → 0.3 秒以下）を目指す場合は、残る主要因である `builder`（1.81 秒）の遅延インポート化（`drawlib/__init__.py` の Lazy Import）が有効です。
