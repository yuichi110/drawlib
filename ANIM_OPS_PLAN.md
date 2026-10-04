# Drawlib アニメーション制御（APNG / WebP）設計計画書
(ANIMATION OPTIONS & PLAYBACK CONTROL PLAN)

- **作成日**: 2026-10-04
- **対象バージョン**: Drawlib 次期リリース
- **対象コンポーネント**: 
  - `src/drawlib/_builder/doc_builder/processor/options.py` (コードブロック属性パース)
  - `src/drawlib/_slide/compiler.py` (スライドHTMLコンパイル)
  - `src/drawlib/_templates/project/slide/slide.js` (スライドプレゼンテーションエンジン)
  - `src/drawlib/_templates/css/targets/slide.css` (スライドUIスタイル)
  - `docs_src/06_doc_builder_and_cli/` (ドキュメント)

---

## 1. エグゼクティブサマリー & ゴール (Executive Summary & Goals)

Drawlib は Python コードから APNG および Animated WebP 形式のアニメーション図版をネイティブ出力する機能（`from drawlib.anim import Animation`）を備えています。
しかし、スライドプレゼンテーション（`slide` プロジェクト）において、これらアニメーション図版は通常の `<img>` タグとして埋め込まれるため、**「スライドに到達した時点で既に裏で再生が完了してしまっている」**、**「発表者のトークの合間にクリックして動かしたいのに制御できない」** という課題が存在します。

本計画書は、**「発表者が意図した任意のタイミングでアニメーションを開始させ、1回だけ再生して停止する」**、あるいは **「常時ループさせて概念を動きで見せる」** という2大プレゼンテーションユースケースを、Markdown のコードブロック属性と `<canvas>` ベースの軽量 APNG プレイヤーによって完全に制御可能にするためのアーキテクチャ設計を定義します。

### 主要達成目標
1. **自己説明的なコードブロック属性の導入**:
   - `anim-trigger: auto | click`
   - `anim-loop: once | infinite`
2. **スライドエンジン (`slide.js`) の `<canvas>` APNG プレイヤー実装**:
   - 外部依存ライブラリなし（純粋な Vanilla JS）で APNG をパース＆コマ送り描画
   - `anim-trigger: click` 時は 1 フレーム目で静止待機し、クリックで再生開始
   - `anim-loop: once` 完了時は最終フレームでピタッと停止
   - 再クリックによる「最初からリプレイ（再再生）」機能
   - ホバー時に再生可能であることを示す視覚的 UI（▶ バッジ / pointer カーソル）
3. **規格準拠による静止画・PDF・GitHub エコシステムの整合性**:
   - APNG 仕様（第1フレームが標準静止画 IDAT）に完全準拠し、未再生時および PDF 出力時は確実に「第1フレーム」を代表画像（ポスター）として確定表示
4. **作図者向けガイドラインの策定**:
   - アニメーション設計時のベストプラクティス（開始状態・ステップ推移・完了状態の構成指針）を公式ドキュメントに明文化

---

## 2. 現状分析と技術的課題 (As-Is Analysis)

### 2.1. ブラウザ標準 `<img>` タグの仕様的制約
1. **ブラウザ読み込み時の自動再生**:
   ブラウザは APNG や Animated WebP を `<img>` タグとして読み込んだ瞬間（DOM生成時）から無条件に再生を開始します。
   スライドデッキには全スライドが事前に DOM 生成されるため、スライド 1 を発表している間にスライド 5 のアニメーションが裏で再生を終えてしまいます。
2. **制御 API の完全な欠如**:
   `<img>` 要素には `<video>` のような `.play()`, `.pause()`, `.currentTime` などの再生制御インターフェースが一切存在しません。
3. **リプレイの難しさ**:
   `img.src` をキャッシュバスターで書き換える手法は、一度限りのリスタートは可能ですが、一時停止や特定フレームでの静止、再生完了検知ができません。

### 2.2. 静止画（PDF・GitHub・画像ビューア）での見え方問題
- APNG は規格上、**「第1フレームが通常の静止画 PNG（IDATチャンク）」** として格納されます。
- そのため、アニメーション非対応のビューアや GitHub の Markdown 表示、OS のサムネイル生成はすべて **「第1フレーム」** を表示します。
- もし作図コードで「第1フレームがほぼ白紙の初期状態」になっていると、PDF レポートや GitHub 上で内容が伝わらない図面になってしまいます。

---

## 3. 目標設計 (To-Be Architecture)

```text
+-------------------------------------------------------------------------------+
| Markdown Source (05_workflows.md)                                             |
|                                                                               |
| ```drawlib file:pipeline.png anim-trigger:click anim-loop:once                |
| from drawlib.anim import Animation                                            |
| ...                                                                           |
| ```                                                                           |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| Drawlib Slide Compiler (_slide/compiler.py)                                   |
|                                                                               |
| HTML Output:                                                                  |
| <figure class="drawlib-image drawlib-anim-container"                          |
|         data-trigger="click" data-loop="once">                                |
|   <canvas class="drawlib-anim-canvas"                                         |
|           data-src="images/05_workflows/pipeline.png"></canvas>               |
|   <div class="anim-play-overlay"><span class="play-icon">▶</span></div>       |
| </figure>                                                                     |
+---------------------------------------+---------------------------------------+
                                        |
                   +--------------------+--------------------+
                   |                                         |
                   v (Web Presentation)                      v (Vector PDF Export)
+---------------------------------------+ +-------------------------------------+
| slide.js (Interactive Canvas Player)  | | Headless Chromium                   |
|                                       | |                                     |
| 1. APNG バイナリから第1フレームを抽出 | | 1. ページロード時:                   |
| 2. Canvas に第1フレームを描画して待機 | |    Canvas に第1フレーム（代表画像） |
| 3. クリック時: アニメーション再生開始 | |    が確実に描画される               |
| 4. anim-loop:once: 最終フレームで停止 | | 2. 16:9 高解像度ベクター PDF に     |
| 5. 再クリック時: 最初からリプレイ     | |    綺麗にキャプチャされる           |
+---------------------------------------+ +-------------------------------------+
```

---

## 4. 詳細技術仕様 (Detailed Technical Specifications)

### 4.1. Markdown コードブロック属性仕様

````markdown
```drawlib file:pipeline.png anim-trigger:click anim-loop:once
```
````

| 属性名 | 指定可能な値 | デフォルト値 | 役割と動作 |
| :--- | :--- | :--- | :--- |
| **`anim-trigger`** | `auto`<br>`click` | `auto` | **アニメーションの開始タイミング**<br>- `auto`: 該当スライドが表示された瞬間に自動で再生開始。<br>- `click`: 該当スライド表示時は第1フレームで静止待機し、図面をクリックした瞬間に再生開始。 |
| **`anim-loop`** | `once`<br>`infinite` | `infinite` | **繰り返し再生の振る舞い**<br>- `once`: 1回最後まで再生し、最終フレームでピタッと停止。<br>- `infinite`: 最後のコマまで行ったら先頭に戻り、常時ループ再生。 |

> **注**: `anim-` 属性が明示されていない通常の `drawlib` 静止画ブロック（`.svg`, 静止 `.png`）には何の影響も与えません。アニメーション拡張子（`.png`, `.apng`, `.webp`）かつ `anim-` 属性が指定された場合に有効化されます。

### 4.2. コンパイラ出力マークアップ仕様

`src/drawlib/_slide/compiler.py` の `_format_asset_markup` を拡張し、アニメーション制御が有効な場合は通常の `<img>` ではなく専用コンテナを出力します：

```html
<figure class="drawlib-image drawlib-anim-container" 
        data-anim-trigger="click" 
        data-anim-loop="once">
  <canvas class="drawlib-anim-canvas" 
          data-src="images/05_workflows/pipeline.png"
          role="img" 
          aria-label="Illustration"></canvas>
  <div class="anim-play-badge" title="Click to play animation">
    <svg class="play-icon" viewBox="0 0 24 24"><polygon points="6 4 20 12 6 20"></polygon></svg>
  </div>
</figure>
```

### 4.3. スライドエンジン (`slide.js`) APNG `<canvas>` プレイヤー

外部 npm ライブラリをバンドルせず、約 6〜8KB の軽量 Vanilla JS APNG デコーダーを `slide.js` 内に組み込みます。

#### 主要機能コンポーネント:
1. **APNG チャンクパーサー**:
   - `fetch(src)` で `ArrayBuffer` を取得。
   - PNG シグネチャ (`89 50 4E 47...`) を検証。
   - `acTL` (アニメーションコントロール), `fcTL` (フレームコントロール), `fdAT` (フレームデータ) チャンクを抽出。
   - 各フレームの `delay_num / delay_den` からフレーム表示時間をミリ秒単位で算出。
2. **ステートマシン管理**:
   - 状態: `READY` (待機中), `PLAYING` (再生中), `PAUSED` (一時停止), `ENDED` (完了停止)。
   - `anim-trigger: click`:
     - 初期状態 `READY`: 第1フレームを `<canvas>` にレンダリングして静止。
     - クリックイベント発火: `PLAYING` へ遷移し、`requestAnimationFrame` または精密タイマーでコマ送り開始。
   - `anim-trigger: auto`:
     - スライドがアクティブになったイベント（`goToSlide`）を契機に自動で `PLAYING` 開始。
3. **ループと停止制御 (`anim-loop`)**:
   - `anim-loop: once`: 最終フレームに達した時点でタイマーを解除し、`ENDED` 状態へ遷移。
   - `ENDED` 状態での再クリック: 先頭（Frame 1 または Frame 2）へ巻き戻して再再生（リプレイ機能）。
   - `anim-loop: infinite`: 最終フレーム後に自動的に Frame 1 にループ。
4. **複数スライド間のリソース管理**:
   - スライドから別のスライドへ切り替わった場合（スライド離脱時）、バックグラウンドでの不要な CPU 消費を防ぐため、再生中のアニメーションは自動停止（または初期状態へリセット）。

### 4.4. UI / UX デザイン (`slide.css`)

発表者がプレゼン中に迷わず操作できるよう、控えめで洗練された UI を提供します：

```css
/* アニメーションコンテナ */
.drawlib-anim-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* クリック再生待ち状態の Play バッジ */
.drawlib-anim-container[data-anim-trigger="click"] .anim-play-badge {
  position: absolute;
  bottom: 16px;
  right: 16px;
  width: 44px;
  height: 44px;
  background: rgba(32, 33, 36, 0.75);
  backdrop-filter: blur(6px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  opacity: 0.6;
  transition: opacity 0.2s, transform 0.2s;
  pointer-events: none;
}

.drawlib-anim-container:hover .anim-play-badge {
  opacity: 1.0;
  transform: scale(1.1);
  background: var(--slide-primary, #1a73e8);
}

/* 再生中・再生完了時のバッジ制御 */
.drawlib-anim-container.playing .anim-play-badge {
  opacity: 0;
  pointer-events: none;
}
.drawlib-anim-container.ended .anim-play-badge {
  opacity: 0.7;
} /* 完了後はリプレイ可能を示すアイコン（↺）に切り替え */
```

---

## 5. 静止画・PDF との整合性（第1フレーム代表仕様）

### 5.1. 「第1フレーム代表仕様」の根拠
- **APNG 規格との 100% 整合**:
  APNG フォーマットは、下位互換性のために **「第1フレーム（Frame 1）を必ず通常の静止画 PNG（IDAT）」** として保持します。
- **決定規則**:
  **「静止画（PDF 出力時、GitHub Markdown 閲覧時、スライドのクリック待機時）には、常に第1フレームが表示される」**
  この確固たる仕様により、どの環境でも表示崩れが一切生じません。

### 5.2. 作図者向けガイドライン（ドキュメント記載内容）

作図者がアニメーションを設計する際、以下の 2 つの推奨パターンを公式ドキュメントで案内します：

#### パターン A: 【全体図 $\rightarrow$ アニメーション開始】（推奨・王道のプレゼン構成）
- **構成**:
  - **Frame 1**: システム全体の完全な全体図（ポスター・静止画・PDF用）。
  - **Frame 2 〜 (N-1)**: リクエストの送信、パケットの移動、各コンポーネントのハイライト。
  - **Frame N**: 完了状態（結果表示）。
- **プレゼン時の体験**:
  1. スライドを開く $\rightarrow$ Frame 1（完全な全体図）が表示されている。概要を口頭で説明。
  2. クリックする $\rightarrow$ Frame 2 からパケットが滑らかに動き出す。
  3. 完了 $\rightarrow$ Frame N で停止。もう一度見せたいときはクリックで再再生。
  4. PDF 出力時 $\rightarrow$ Frame 1 の美しい全体図がそのまま収録される。

#### パターン B: 【初期状態 $\rightarrow$ 完了状態】（ジャンプのない完全連続フロー）
- **構成**:
  - **Frame 1**: アニメーションの最初の一歩（開始前の状態）。
  - **Frame 2 〜 N**: 順次描画・進行。
- **プレゼン時の体験**:
  - スライドを開いた時も、クリックして再生が始まった時も、1コマ目から寸分のズレもなく完全に滑らかにアニメーションが流れます。

---

## 6. 実装ステップと作業項目 (Implementation Roadmap)

| ステップ | 担当領域 | 作業内容 |
| :--- | :--- | :--- |
| **Phase 1** | **属性パーサー拡張** | `src/drawlib/_builder/doc_builder/processor/options.py`<br>- `anim-trigger: auto\|click`<br>- `anim-loop: once\|infinite`<br>のパース処理とデータモデルへの格納。 |
| **Phase 2** | **コンパイラ出力拡張** | `src/drawlib/_slide/compiler.py`<br>- `anim-*` 属性が存在する場合、`<figure>` および `<canvas>` マークアップを生成する出力分岐を実装。 |
| **Phase 3** | **Canvas APNG プレイヤー** | `src/drawlib/_templates/project/slide/slide.js`<br>- APNG チャンクパース、Canvas レンダリングループ、クリック/自動トリガー、ループ停止、リプレイのステートマシンを実装。 |
| **Phase 4** | **UI・CSS 装飾** | `src/drawlib/_templates/css/targets/slide.css` および `slide_src/slide.css`<br>- Play バッジ、ホバーアニメーション、リプレイアイコン、印刷メディア（`@media print`）対応スタイルを整備。 |
| **Phase 5** | **実機検証 & ドキュメント** | `slide_src/05_workflows.md` に `anim-trigger:click anim-loop:once` を適用。<br>- ブラウザ表示・クリック再生・PDF出力の整合性を検証。<br>- `docs_src` のスライド・アニメーション解説を更新。 |

---

## 7. 検証基準 (Verification Criteria)

1. **静的品質保証**:
   - `./dcli check all` がエラーゼロで通過すること。
2. **ブラウザ対話機能検証**:
   - `anim-trigger:click`: スライド表示時は Frame 1 で静止し、クリックするまで再生が始まらないこと。
   - クリック後、スムーズに再生が進行し、`anim-loop:once` では最終フレームで確実に停止すること。
   - 停止後に再クリックした際、先頭からリプレイされること。
   - `anim-trigger:auto`: スライド切り替えと同時に自動再生されること。
3. **PDF 出力整合性**:
   - `drawlib build pdf slide_src/ -o slide.pdf` を実行した際、エラーなく Frame 1 の高解像度静止画が PDF の該当スライドページに美しく収まっていること。
