# Drawlib アニメーション制御（APNG / WebP）設計計画書
(ANIMATION OPTIONS & PLAYBACK CONTROL PLAN)

- **作成日**: 2026-10-04 (2026-10-07 更新)
- **対象バージョン**: Drawlib 次期リリース
- **対象コンポーネント**: 
  - `src/drawlib/_builder/doc_builder/processor/options.py` (コードブロック属性パース)
  - `src/drawlib/_slide/compiler.py` (スライドHTMLコンパイル)
  - `src/drawlib/_templates/project/slide/slide.js` (スライドプレゼンテーションエンジン)
  - `src/drawlib/_templates/css/targets/slide.css` (スライドUIスタイル)
  - `docs_src/06_animations/`, `docs_src/07_doc_builder_and_cli/` (ドキュメント)

---

## 1. エグゼクティブサマリー & ゴール (Executive Summary & Goals)

Drawlib は Python コードから APNG および Animated WebP 形式のアニメーション図版をネイティブ出力する機能（`from drawlib.anim import Animation`）を備えています。
しかし、スライドプレゼンテーション（`slide` プロジェクト）において、これらアニメーション図版は通常の `<img>` タグとして埋め込まれるため、**「スライドに到達した時点で既に裏で再生が完了してしまっている」**、**「発表者のトークの合間にクリックして段階的に動かしたいのに制御できない」** という課題が存在します。

本計画書は、**「発表者が意図した任意のタイミングでアニメーションを開始させ、指定したフレームで一旦停止（ステップ実行）したり、1回だけ再生して停止する」**、あるいは **「常時ループさせて概念を動きで見せる」** というプレゼンテーションユースケースを、Markdown のコードブロック属性と `<canvas>` ベースの軽量 APNG / WebP プレイヤーによって完全に制御可能にするためのアーキテクチャ設計を定義します。

### 主要達成目標
1. **自己説明的なコードブロック属性の導入**:
   - `anim-trigger: auto | click`（開始トリガー）
   - `anim-loop: once | infinite`（ループ制御）
   - `anim-pause: 4,9`（指定フレーム番号での一旦停止／ステップ再生）
2. **スライドエンジン (`slide.js`) の `<canvas>` APNG / WebP プレイヤー実装**:
   - 外部依存ライブラリなし（ブラウザ標準 `ImageDecoder` API ＋ Vanilla JS APNG フォールバック）で APNG・Animated WebP をフレーム単位デコード＆コマ送り描画
   - `anim-trigger: click` 時は最初のフレーム（Frame 0）で静止待機し、クリックで再生開始
   - `anim-pause: 4,9` 指定時は、該当フレーム（Frame 4, Frame 9）に到達した瞬間に一時停止（`PAUSED`）し、次のクリックで続きのフレームから再開（PowerPoint のビルド／ステップアニメーション体験）
   - `anim-loop: once` 完了時は最終フレームでピタッと停止（`ENDED`）
   - 完了後の再クリックによる「最初からリプレイ（再再生）」機能
   - ホバー時・一時停止時に再生可能であることを示す視覚的 UI（▶ バッジ / ↺ リプレイバッジ / pointer カーソル）
3. **規格準拠による静止画・PDF・GitHub エコシステムの整合性**:
   - APNG / WebP の先頭フレーム（Frame 0）を未再生時および PDF 出力時の代表画像（ポスター）として確定表示
4. **作図者向けガイドラインの策定**:
   - アニメーション設計時のベストプラクティス（開始状態・ステップ一時停止・完了状態の構成指針）を公式ドキュメントに明文化

---

## 2. 現状分析と技術的課題 (As-Is Analysis)

### 2.1. ブラウザ標準 `<img>` タグの仕様的制約
1. **ブラウザ読み込み時の自動再生**:
   ブラウザは APNG や Animated WebP を `<img>` タグとして読み込んだ瞬間（DOM生成時）から無条件に再生を開始します。
   スライドデッキには全スライドが事前に DOM 生成されるため、スライド 1 を発表している間にスライド 5 のアニメーションが裏で再生を終えてしまいます。
2. **制御 API の完全な欠如**:
   `<img>` 要素には `<video>` のような `.play()`, `.pause()`, `.currentTime` などの再生制御インターフェースが一切存在せず、「Nフレーム目で止める」といった制御が不可能です。
3. **リプレイの難しさ**:
   `img.src` をキャッシュバスターで書き換える手法は、一度限りのリスタートは可能ですが、一時停止や特定フレームでの静止、再生完了検知ができません。

### 2.2. 静止画（PDF・GitHub・画像ビューア）での見え方問題
- APNG は規格上、**「先頭フレーム（Frame 0）が通常の静止画 PNG（IDATチャンク）」** として格納されます。
- そのため、アニメーション非対応のビューアや GitHub の Markdown 表示、OS のサムネイル生成はすべて **「先頭フレーム」** を表示します。
- もし作図コードで「先頭フレームがほぼ白紙の初期状態」になっていると、PDF レポートや GitHub 上で内容が伝わらない図面になってしまいます。

---

## 3. 目標設計 (To-Be Architecture)

```text
+-------------------------------------------------------------------------------+
| Markdown Source (05_workflows.md)                                             |
|                                                                               |
| ```drawlib file:pipeline.webp anim-trigger:click anim-loop:once anim-pause:4,9|
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
|         data-anim-trigger="click"                                             |
|         data-anim-loop="once"                                                 |
|         data-anim-pause="4,9">                                                |
|   <canvas class="drawlib-anim-canvas"                                         |
|           data-src="images/05_workflows/pipeline.webp"></canvas>              |
|   <div class="anim-play-badge"><svg class="play-icon">...</svg></div>         |
| </figure>                                                                     |
+---------------------------------------+---------------------------------------+
                                        |
                   +--------------------+--------------------+
                   |                                         |
                   v (Web Presentation)                      v (Vector PDF Export)
+---------------------------------------+ +-------------------------------------+
| slide.js (Interactive Canvas Player)  | | Headless Chromium                   |
|                                       | |                                     |
| 1. Frame 0 を Canvas に描画して待機   | | 1. ページロード時:                   |
| 2. クリック時: アニメーション再生開始 | |    Canvas に Frame 0（代表画像）     |
| 3. anim-pause(4,9): 指定フレームで    | |    が確実に描画される               |
|    一時停止し、次クリックで続き再生   | | 2. 16:9 高解像度ベクター PDF に     |
| 4. anim-loop:once: 最終フレームで停止 | |    綺麗にキャプチャされる           |
| 5. 完了後クリック: 先頭からリプレイ   | |                                     |
+---------------------------------------+ +-------------------------------------+
```

---

## 4. 詳細技術仕様 (Detailed Technical Specifications)

### 4.1. Markdown コードブロック属性仕様

````markdown
```drawlib file:pipeline.webp anim-trigger:click anim-loop:once anim-pause:4,9
```
````

| 属性名 | 指定可能な値 | デフォルト値 | 役割と動作 |
| :--- | :--- | :--- | :--- |
| **`anim-trigger`** | `auto`<br>`click` | `auto` | **アニメーションの開始タイミング**<br>- `auto`: 該当スライドが表示された瞬間に自動で再生開始。<br>- `click`: 該当スライド表示時は先頭フレーム（Frame 0）で静止待機し、図面をクリックした瞬間に再生開始。 |
| **`anim-loop`** | `once`<br>`infinite` | `infinite` | **繰り返し再生の振る舞い**<br>- `once`: 1回最後まで再生し、最終フレームでピタッと停止。<br>- `infinite`: 最終フレームまで到達したら先頭フレームに戻り、常時ループ再生。 |
| **`anim-pause`** | カンマ区切り整数<br>(例: `4,9` / `5`) | なし (`None`) | **指定フレーム番号での一時停止（ステップ実行）**<br>- 0始まりのフレーム番号（Frame 0, 1, 2, ...）をカンマ区切りで指定。<br>- 再生中に指定フレームへ到達した瞬間にそのフレームを描画した状態で一時停止（`PAUSED`）し、次のクリックで続きのフレーム（`frame + 1`）から再開する。 |

> **注**: `anim-` 属性が明示されていない通常の `drawlib` 静止画ブロック（`.svg`, 静止 `.png`）には何の影響も与えません。アニメーション拡張子（`.png`, `.apng`, `.webp`）かつ `anim-` 属性が指定された場合に有効化されます（`anim-pause` が指定された場合、`anim-loop` が未指定ならステップ実行向けに `once` 相当として扱うか、明示指定に従います）。

### 4.2. コンパイラ出力マークアップ仕様

`src/drawlib/_slide/compiler.py` の `_format_asset_markup` を拡張し、アニメーション制御が有効な場合は通常の `<img>` ではなく専用コンテナを出力します：

```html
<figure class="drawlib-image drawlib-anim-container" 
        data-anim-trigger="click" 
        data-anim-loop="once"
        data-anim-pause="4,9">
  <canvas class="drawlib-anim-canvas" 
          data-src="images/05_workflows/pipeline.webp"
          role="img" 
          aria-label="Illustration"></canvas>
  <div class="anim-play-badge" title="Click to play / continue animation">
    <svg class="play-icon" viewBox="0 0 24 24"><polygon points="6 4 20 12 6 20"></polygon></svg>
  </div>
</figure>
```

### 4.3. スライドエンジン (`slide.js`) APNG / WebP `<canvas>` プレイヤー

外部 npm ライブラリをバンドルせず、ブラウザ標準の `ImageDecoder` API と軽量 Vanilla JS APNG フォールバックデコーダーを `slide.js` 内に組み込みます。

#### 主要機能コンポーネント:
1. **ハイブリッド・フレームデコーダー（APNG & Animated WebP 対応）**:
   - **第一選択 (`window.ImageDecoder`)**:
     - Chromium 系・Firefox 等で利用可能な WebCodecs `ImageDecoder` API を使用し、`image/png` (APNG) と `image/webp` (Animated WebP) の両方をネイティブデコード。
     - `decoder.tracks.selectedTrack.frameCount` から総フレーム数を取得し、`decoder.decode({ frameIndex: i })` で各フレームの描画データと `duration`（表示時間ミリ秒）を取得。
   - **フォールバック（Pure JS APNG チャンクパーサー）**:
     - `ImageDecoder` 非対応ブラウザ向けに、PNG の `acTL`, `fcTL`, `fdAT` チャンクを解析して各フレームの `ImageBitmap` と `delay` を抽出する軽量デコーダーを内蔵。
2. **ステートマシン管理**:
   - 状態:
     - `READY`: 初期待機中（Frame 0 を `<canvas>` に描画して静止）
     - `PLAYING`: コマ送り再生中
     - `PAUSED`: `anim-pause` で指定されたフレーム番号に到達して一時停止中
     - `ENDED`: 最終フレームまで再生完了して停止中
   - **状態遷移ルール**:
     - **`READY` 状態**:
       - `anim-trigger: click`: Frame 0 で待機。クリックされると Frame 1 から `PLAYING` 開始。
       - `anim-trigger: auto`: スライド表示時（`goToSlide`）に自動で Frame 0 から `PLAYING` 開始（ただし Frame 0 が `anim-pause` に含まれる場合は別扱いせず Frame 1 以降の停止点で止まる）。
     - **`PLAYING` 状態 → `PAUSED` 状態（`anim-pause` 判定）**:
       - フレーム `k` を描画した時点で、`pauseFrames.has(k)`（かつ最終フレームではない）場合、次フレームへのタイマー予約を行わず即座に `PAUSED` 状態へ遷移する。
     - **`PAUSED` 状態でのクリック**:
       - `currentFrame + 1` から `PLAYING` を再開し、次の `anim-pause` フレームまたは最終フレームへ向かって進行する。
     - **最終フレーム到達時（`anim-loop` 判定）**:
       - `anim-loop: once`: 最終フレームを描画した状態でタイマーを解除し、`ENDED` 状態へ遷移。
       - `anim-loop: infinite`: 最終フレームの表示時間経過後、Frame 0 に戻ってループ継続（`anim-pause` がある場合は次周でも各停止点で止まるか、1周目のみ止まるかはシンプルに毎回停止点を有効化）。
     - **`ENDED` 状態での再クリック（リプレイ）**:
       - 先頭（Frame 0）へ巻き戻して最初から再再生を開始する。
3. **複数スライド間のリソース管理**:
   - スライドから別のスライドへ切り替わった場合（スライド離脱時）、バックグラウンドでの不要なタイマー実行を防ぐため再生タイマーを停止し、再度そのスライドに戻った際は初期状態へリセットする。

### 4.4. UI / UX デザイン (`slide.css`)

発表者がプレゼン中に「今クリック待機中なのか・ステップ一時停止中なのか・再生完了なのか」を直感的に把握できるよう、控えめで洗練された UI を提供します：

```css
/* アニメーションコンテナ */
.drawlib-anim-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* クリック再生待ち / 一時停止状態の Play バッジ */
.drawlib-anim-container .anim-play-badge {
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

/* 再生中はバッジを非表示 */
.drawlib-anim-container.playing .anim-play-badge {
  opacity: 0;
  pointer-events: none;
}

/* anim-pause による一時停止中は Play バッジ（▶）を表示して「続きがある」ことを示す */
.drawlib-anim-container.paused .anim-play-badge {
  opacity: 0.75;
}

/* 再生完了後はリプレイ可能を示すアイコン（↺）に切り替え */
.drawlib-anim-container.ended .anim-play-badge {
  opacity: 0.7;
}
```

---

## 5. 静止画・PDF との整合性（先頭フレーム代表仕様）

### 5.1. 「先頭フレーム（Frame 0）代表仕様」の根拠
- **APNG / WebP 規格との 100% 整合**:
  APNG フォーマットは下位互換性のために **「先頭フレーム（Frame 0）を必ず通常の静止画 PNG（IDAT）」** として保持します。
- **決定規則**:
  **「静止画（PDF 出力時、GitHub Markdown 閲覧時、スライドのクリック待機時）には、常に先頭フレーム（Frame 0）が表示される」**
  この確固たる仕様により、どの環境でも表示崩れが一切生じません。

### 5.2. 作図者向けガイドライン（ドキュメント記載内容）

作図者がアニメーションを設計する際、以下の 3 つの推奨パターンを公式ドキュメントで案内します：

#### パターン A: 【ステップバイステップ一時停止 (`anim-pause`)】（プレゼンでの段階的解説）
- **構成**:
  - 例：全 12 フレーム（Frame 0 〜 11）で、Phase 1 完了が Frame 4、Phase 2 完了が Frame 8、最終 Phase 3 完了が Frame 11 の場合：
  - `anim-trigger:click anim-loop:once anim-pause:4,8` を指定。
- **プレゼン時の体験**:
  1. スライドを開く $\rightarrow$ Frame 0 で待機。
  2. 1回目のクリック $\rightarrow$ Frame 4 まで動いてピタッと一時停止。Phase 1 を口頭で説明。
  3. 2回目のクリック $\rightarrow$ Frame 5〜8 まで動いて再び一時停止。Phase 2 を口頭で説明。
  4. 3回目のクリック $\rightarrow$ Frame 9〜11（最終フレーム）まで動いて完了停止。

#### パターン B: 【全体図 $\rightarrow$ アニメーション開始】（PDF 重視のプレゼン構成）
- **構成**:
  - **Frame 0**: システム全体の完全な全体図（ポスター・静止画・PDF用）。
  - **Frame 1 〜 (N-2)**: リクエストの送信、パケットの移動、各コンポーネントのハイライト。
  - **Frame (N-1)**: 完了状態（結果表示）。

#### パターン C: 【初期状態 $\rightarrow$ 完了状態】（ジャンプのない完全連続フロー）
- **構成**:
  - **Frame 0**: アニメーションの最初の一歩（開始前の状態）。
  - **Frame 1 〜 (N-1)**: 順次描画・進行。

---

## 6. 実装ステップと作業項目 (Implementation Roadmap)

| ステップ | 担当領域 | 作業内容 |
| :--- | :--- | :--- |
| **Phase 1** | **属性パーサー拡張** | `src/drawlib/_builder/doc_builder/processor/options.py`<br>- `anim_trigger: Literal["auto", "click"] \| None = None`<br>- `anim_loop: Literal["once", "infinite"] \| None = None`<br>- `anim_pause: list[int] \| None = None` (`anim-pause:4,9` のパース処理とモデル格納) |
| **Phase 2** | **コンパイラ出力拡張** | `src/drawlib/_slide/compiler.py`<br>- `anim-*` 属性が存在する場合、`data-anim-trigger`, `data-anim-loop`, `data-anim-pause` を持つ `<figure>` および `<canvas>` マークアップを生成する出力分岐を実装。 |
| **Phase 3** | **Canvas APNG/WebP プレイヤー** | `src/drawlib/_templates/project/slide/slide.js`<br>- `ImageDecoder` API ＋ APNG フォールバックデコーダー、Canvas レンダリングループ、`READY` / `PLAYING` / `PAUSED` (`anim-pause`) / `ENDED` のステートマシンを実装。 |
| **Phase 4** | **UI・CSS 装飾** | `src/drawlib/_templates/css/targets/slide.css` および `slide_about_drawlib_src/slide.css`<br>- Play バッジ、`.paused` 状態表示、リプレイアイコン（↺）、印刷メディア（`@media print`）対応スタイルを整備。 |
| **Phase 5** | **実機検証 & ドキュメント** | `slide_about_drawlib_src/05_workflows.md` 等に `anim-trigger:click anim-loop:once` / `anim-pause` を適用。<br>- ブラウザ表示・クリック再生・ステップ一時停止・PDF出力の整合性を検証。<br>- `docs_src/06_animations/` および `docs_src/07_doc_builder_and_cli/` の解説を更新。 |

---

## 7. 検証基準 (Verification Criteria)

1. **静的品質保証**:
   - `./dcli code-check all` がエラーゼロで通過すること。
2. **ブラウザ対話機能検証**:
   - `anim-trigger:click`: スライド表示時は Frame 0 で静止し、クリックするまで再生が始まらないこと。
   - `anim-pause:4,9`: 再生中に Frame 4 で一旦停止（`PAUSED`）し、次のクリックで Frame 5 から再開して Frame 9 で再び停止すること。
   - `anim-loop:once`: 最終フレームで確実に停止（`ENDED`）し、再クリックした際に先頭（Frame 0）からリプレイされること。
   - `anim-trigger:auto`: スライド切り替えと同時に自動再生されること。
3. **PDF 出力整合性**:
   - `drawlib build pdf slide_about_drawlib_src/ -o slide_about_drawlib.pdf` を実行した際、エラーなく Frame 0 の高解像度静止画が PDF の該当スライドページに美しく収まっていること。
