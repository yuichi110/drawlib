# 第12章: プレゼンテーションスライドの作成 (`slide`)

Drawlib は、技術文書（`doc`）やWebサイト（`site`）だけでなく、**16:9 プレゼンテーションスライド**（`slide`）の作成をファーストクラスでサポートしています。

PowerPoint や Google Slides などの GUI ツールを使わずに、Markdown と Python 作図コードだけで、学会発表・カンファレンス・社内勉強会向けの美しいスライドデッキをコード管理できます。

```drawlib align=center file=fig_slide_layout.png caption="図 12.1: Drawlib スライド生成アーキテクチャとデュアル出力"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=136, height=54)

header_ts = Styles.WhiteBold.patch(text_size=10.5)
ts_body = Styles.Dark.patch(text_size=10.0, halign="left")
ts_arrow = Styles.DarkBold.patch(text_size=10.0)

# 1. Slide Source Markdown & Canvas
rectangle((21.5, 27.0), width=35.0, height=44.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
rectangle((21.5, 45.0), width=33.0, height=6.0, style=Styles.PrimaryFlat.patch(shape_r=1.5), text="1. Markdown 16:9", text_style=header_ts)

phosphor.presentation(xy=(7.8, 35.0), width=4.4, style=Styles.Primary)
text((10.8, 35.0), text="1 MD = 1 Slide\n1920x1080 ステージ", style=ts_body)

phosphor.layout(xy=(7.8, 23.5), width=4.4, style=Styles.Primary)
text((10.8, 23.5), text="::: block / note\n視覚段組と発表ノート", style=ts_body)

phosphor.code(xy=(7.8, 12.0), width=4.4, style=Styles.Primary)
text((10.8, 12.0), text="current_slide\n余白座標を自動取得", style=ts_body)

# 2. Build Pipeline
rectangle((68.0, 27.0), width=35.0, height=44.0, style=Styles.Neutral.patch(shape_r=2.0))
rectangle((68.0, 45.0), width=33.0, height=6.0, style=Styles.AccentFlat.patch(shape_r=1.5), text="2. ビルドエンジン", text_style=header_ts)

phosphor.gear(xy=(54.3, 35.0), width=4.4, style=Styles.Accent)
text((57.3, 35.0), text="drawlib build\nスライド構文解析", style=ts_body)

phosphor.database(xy=(54.3, 23.5), width=4.4, style=Styles.Accent)
text((57.3, 23.5), text=".drawlib/cache.db\n差分のみ高速再描画", style=ts_body)

phosphor.arrows_split(xy=(54.3, 12.0), width=4.4, style=Styles.Accent)
text((57.3, 12.0), text="HTML & PDF 出力\nデュアル生成基盤", style=ts_body)

# 3. Deliverables
rectangle((114.5, 27.0), width=35.0, height=44.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
rectangle((114.5, 45.0), width=33.0, height=6.0, style=Styles.DarkFlat.patch(shape_r=1.5), text="3. デュアル成果物", text_style=header_ts)

phosphor.desktop(xy=(100.8, 35.0), width=4.4, style=Styles.Dark)
text((103.8, 35.0), text="Web スライド\n発表者ビュー (P)", style=ts_body)

phosphor.file_pdf(xy=(100.8, 23.5), width=4.4, style=Styles.Dark)
text((103.8, 23.5), text="ベクター PDF\n1スライド1ページ", style=ts_body)

phosphor.image(xy=(100.8, 12.0), width=4.4, style=Styles.Dark)
text((103.8, 12.0), text="*_images/\n高解像度図版の抽出", style=ts_body)

# Connections
line((39.5, 27.0), (50.0, 27.0), arrow_head="->", style=Styles.DarkBold)
text((44.75, 31.0), text="解析", style=ts_arrow)

line((86.0, 27.0), (96.5, 27.0), arrow_head="->", style=Styles.DarkBold)
text((91.25, 31.0), text="生成", style=ts_arrow)

save()
```

## 12.1 スライドプロジェクトの作成 (`drawlib init slide`)

スライドプロジェクトは `uv run drawlib init slide` コマンドで一発で足場生成できます:

```bash
# 標準のスライドプロジェクトを生成 (slide_src/ が作成されます)
uv run drawlib init slide

# プロジェクト名やテーマ、言語を指定する場合
uv run drawlib init slide my_presentation -s google -l ja
```

### 生成されるディレクトリ構成
`uv run drawlib init slide my_presentation -s google -l ja` を実行すると、以下のディレクトリ構成が構築されます:

```text
.
├── my_presentation_src/           # [正本] スライドの Markdown ソース
│   ├── _assets/                   # スライド内で参照する静的画像・ロゴ
│   ├── 01_title.md                # タイトルスライド
│   ├── 02_agenda.md               # アジェンダ
│   ├── 03_architecture.md         # アーキテクチャ図解スライド
│   ├── styles.py                  # スライド全体のスタイル・テーマ定義
│   ├── utils.py                   # スライド専用のレイアウト補助関数
│   ├── slide.js                   # プレゼン再生・発表者ビュー制御エンジン
│   ├── build.sh                   # 全ターゲット一括ビルドスクリプト
│   ├── build_html.sh              # Web プレゼン生成スクリプト
│   ├── build_pdf.sh               # 1スライド1ページの PDF 生成スクリプト
│   └── serve.sh                   # プレゼン用ローカルサーバー起動スクリプト
├── my_presentation_html/          # [成果物] Web プレゼンテーション (index.html)
├── my_presentation.pdf            # [成果物] 16:9 ベクター PDF プレゼンテーション
└── my_presentation_images/        # [成果物] 抽出された高解像度図面画像
```

## 12.2 16:9 プレゼンテーションの執筆モデル (`::: block` / `::: note` と `current_slide`)

Drawlib のスライドは、**「1 つの Markdown ファイル ＝ 1 つのスライド」** という直感的なモデルに加え、**デュアルレイヤー構造（`::: block` と `::: note`）** および **`current_slide` (`SlideContext`)** を備えています。

1. **デュアルレイヤー構造（`::: block` と `::: note`）**:
   - **`::: block`（ビジュアルステージ層）**: `1920 × 1080` スライドステージ上に表示されるカードやマルチカラム段組、および ````drawlib```` 図版を配置します。聴衆が一目で理解できるよう、テキストは簡潔なキーワードに絞ります。
   - **`::: note`（スピーカーノート・詳細解説層）**: スライド下部に記述する発表者用トークスクリプト兼、配布資料としての詳細解説文です。通常スライド表示時は非表示ですが、**発表者ビュー（Presenter View）** で手元に表示され、読み物としても機能します。
2. **`current_slide` (`SlideContext`) による動的領域取得**:
   - スライド内の ````drawlib```` ブロックで `from drawlib.slide import current_slide` をインポートすると、見出しや上部の `::: block` を除いた残りのキャンバス領域（`current_slide.content_box`）を自動計算して図版をぴったり配置できます。

### スライド Markdown の記述例
````markdown
# マイクロサービスアーキテクチャの刷新

<div class="subtitle">イベント駆動型アーキテクチャへの段階的移行計画</div>

::: block
- **疎結合化**: API Gateway とワーカー間を非同期イベントブローカーで分離
- **耐障害性**: スパイクアクセス時のバックプレッシャー制御と再試行の自動化
:::

```drawlib align=center code=fold file=arch_slide.png caption="イベント駆動型パイプライン"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.slide import current_slide
from drawlib.styles import Styles

# current_slide.content_box のアスペクト比に合わせてキャンバスをセットアップ
box = current_slide.content_box
setup(width=132, height=38)

ts_card = Styles.DarkBold.patch(text_size=11.0)
ts_primary = Styles.WhiteBold.patch(text_size=11.0)

rectangle((24, 19), width=34, height=18, style=Styles.Neutral, text="API Gateway", text_style=ts_card)
rectangle((66, 19), width=34, height=18, style=Styles.PrimaryFlat, text="Event Broker", text_style=ts_primary)
rectangle((108, 19), width=34, height=18, style=Styles.SecondaryNeutral, text="Order Worker", text_style=ts_card)

line((41, 19), (49, 19), arrow_head="->", style=Styles.DarkBold)
line((83, 19), (91, 19), arrow_head="->", style=Styles.DarkBold)
save()
```

::: note
このスライドでは、従来の同期 RPC 呼び出しから Event Broker を介した非同期メッセージングへの移行アーキテクチャを説明します。
特にピーク時の注文処理遅延を解消するため、Order Worker を水平スケール可能な構成に変更した点を強調してください。
:::
````

## 12.3 デュアル出力と発表者ビュー (Presenter View)

スライドプロジェクトをビルドすると、利用シーンに応じた 2 つの形式が同時に生成されます:

1. **インタラクティブ Web プレゼンテーション (`my_presentation_html/index.html`)**:
   - 会場での登壇やオンライン勉強会向けの HTML5 プレゼンテーション。
   - **キーボードナビゲーション & 発表者ビュー**:
     - `Space` / `→` / `PageDown`: 次のスライドへ進む
     - `←` / `PageUp`: 前のスライドへ戻る
     - `P` キー（または URL に `?presenter=1` を付与）: **発表者ビュー（Presenter View）** を起動。現在のスライド、次のスライドのプレビュー、経過タイマー、および `::: note` に記述したスピーカーノートが一画面に表示され、別ウィンドウの聴衆向けスクリーンとリアルタイム同期します。
     - `F`: フルスクリーン（全画面）表示の切り替え
     - `O` / `Esc`: スライド全体をグリッド一覧表示するオーバービューモード
2. **1 スライド 1 ページのベクター PDF (`my_presentation.pdf`)**:
   - 参加者への事前配布、SpeakerDeck / DocSend へのアップロード、印刷向けの PDF。
   - Playwright によるヘッドレスレンダリングにより、各スライドが 1 ページずつ欠けのない 16:9 ベクター PDF として忠実に焼き込まれます。
