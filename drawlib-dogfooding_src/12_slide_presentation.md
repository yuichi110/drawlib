# 第12章: プレゼンテーションスライドの作成 (`slide`)

Drawlib は、技術文書（`doc`）やWebサイト（`site`）だけでなく、**16:9 プレゼンテーションスライド**（`slide`）の作成をファーストクラスでサポートしています。

PowerPoint や Google Slides などの GUI ツールを使わずに、Markdown と Python 作図コードだけで、学会発表・カンファレンス・社内勉強会向けの美しいスライドデッキをコード管理できます。

```drawlib 650px center file:fig_slide_layout.png caption:"図 12.1: Drawlib スライド生成アーキテクチャとデュアル出力"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=56)

header_ts = Styles.WhiteBold.patch(text_size=9.5)
ts_body = Styles.Dark.patch(text_size=7.5, text_halign="left")

# 1. Slide Source Markdown & Canvas
rectangle((24.0, 26.0), width=36.0, height=38.0, r=2.0, style=Styles.PrimaryOutline)
rectangle((24.0, 42.0), width=34.0, height=5.5, r=1.5, style=Styles.PrimaryFlat, text="Markdown 16:9 Stage", text_style=header_ts)

phosphor.presentation(xy=(10.0, 33.0), width=4.5, style=Styles.Primary)
text((14.0, 33.0), text="1 Markdown = 1 Slide\n1920x1080 固定ステージ", style=ts_body)

phosphor.layout(xy=(10.0, 23.5), width=4.5, style=Styles.Primary)
text((14.0, 23.5), text="SlideContext & Layout\nヘッダー・本文・フッター", style=ts_body)

phosphor.code(xy=(10.0, 14.0), width=4.5, style=Styles.Primary)
text((14.0, 14.0), text="```drawlib コードブロック\nインラインアーキテクチャ図", style=ts_body)

# 2. Build Pipeline
rectangle((70.0, 26.0), width=28.0, height=38.0, r=2.0, style=Styles.AccentOutline)
rectangle((70.0, 42.0), width=26.0, height=5.5, r=1.5, style=Styles.AccentFlat, text="Compiler Engine", text_style=header_ts)

phosphor.gear(xy=(60.0, 31.0), width=4.5, style=Styles.Accent)
text((64.0, 31.0), text="drawlib build\nスライド構文解析", style=ts_body)

phosphor.arrows_split(xy=(60.0, 19.0), width=4.5, style=Styles.Accent)
text((64.0, 19.0), text="HTML & PDF\nデュアル生成パイプライン", style=ts_body)

# 3. Deliverables
rectangle((116.0, 26.0), width=36.0, height=38.0, r=2.0, style=Styles.SuccessOutline)
rectangle((116.0, 42.0), width=34.0, height=5.5, r=1.5, style=Styles.SuccessFlat, text="Dual Outputs", text_style=header_ts)

phosphor.desktop(xy=(102.0, 33.0), width=4.5, style=Styles.Success)
text((106.0, 33.0), text="Web Presentation\nキーボード操作・全画面(F)", style=ts_body)

phosphor.file_pdf(xy=(102.0, 23.5), width=4.5, style=Styles.Success)
text((106.0, 23.5), text="1-Slide-1-Page PDF\n配布・印刷用ベクターPDF", style=ts_body)

phosphor.image(xy=(102.0, 14.0), width=4.5, style=Styles.Success)
text((106.0, 14.0), text="slide_images/\n個別スライド図版の抽出", style=ts_body)

# Connections
line((43.0, 26.0), (55.0, 26.0), arrow_head="->", style=Styles.DarkBold)
text((49.0, 30.0), text="Compile", style=Styles.DarkBold.patch(text_size=7.5))

line((85.0, 26.0), (97.0, 26.0), arrow_head="->", style=Styles.DarkBold)
text((91.0, 30.0), text="Generate", style=Styles.DarkBold.patch(text_size=7.5))
```

## 12.1 スライドプロジェクトの作成 (`drawlib init slide`)

スライドプロジェクトは `drawlib init slide` コマンドで一発で足場生成できます:

```bash
# 標準のスライドプロジェクトを生成 (slide_src/ が作成されます)
drawlib init slide

# プロジェクト名やテーマ、言語を指定する場合
drawlib init slide my_presentation -s google -l ja
```

### 生成されるディレクトリ構成
```text
my_presentation/
├── slide_src/                 # [正本] スライドの Markdown ソース
│   ├── 01_title.md            # タイトルスライド
│   ├── 02_agenda.md           # アジェンダ
│   ├── 03_architecture.md     # アーキテクチャ図解スライド
│   ├── styles.py              # スライド全体のスタイル・テーマ定義
│   ├── utils.py               # スライド専用のレイアウト関数
│   ├── slide.js               # プレゼンテーション再生・キーボード制御エンジン
│   ├── build.sh               # 全ターゲット一括ビルドスクリプト
│   ├── build_html.sh          # Web プレゼン生成スクリプト
│   ├── build_pdf.sh           # 1スライド1ページの PDF 生成スクリプト
│   └── serve.sh               # プレゼン用ローカルサーバー起動スクリプト
├── slide_html/                # [成果物] Web プレゼンテーション (index.html)
├── slide.pdf                  # [成果物] ベクター PDF プレゼンテーション
└── slide_images/              # [成果物] 抽出された高解像度図面画像
```

## 12.2 16:9 プレゼンテーションの執筆モデル

Drawlib のスライドは、**「1 つの Markdown ファイル ＝ 1 つのスライド」** という極めて直感的なモデルを採用しています。

- ファイル名の昇順（`01_title.md`, `02_agenda.md`, `03_overview.md` など）でスライドの順番が決定されます。
- 各スライドは `1920 × 1080` ピクセルの固定ステージにマッピングされ、プロジェクターやブラウザのウィンドウサイズに合わせて自動的にアスペクト比を維持しながらスケールします。

### スライド Markdown の記述例
````markdown
# マイクロサービスアーキテクチャの刷新

<div class="subtitle">イベント駆動型アーキテクチャへの段階的移行計画</div>

```drawlib 1400px center file:arch_slide.png
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=160, height=45)
rectangle((30, 22.5), width=35, height=18, style=Styles.Neutral, text="API Gateway")
rectangle((80, 22.5), width=35, height=18, style=Styles.PrimaryFlat, text="Event Broker", text_style=Styles.WhiteBold)
rectangle((130, 22.5), width=35, height=18, style=Styles.SecondaryNeutral, text="Order Worker")
line((47.5, 22.5), (62.5, 22.5), arrow_head="->", style=Styles.DarkBold)
line((97.5, 22.5), (112.5, 22.5), arrow_head="->", style=Styles.DarkBold)
```
````

## 12.3 デュアル出力と発表者体験

スライドプロジェクトをビルドすると、利用シーンに応じた 2 つの形式が同時に生成されます:

1. **インタラクティブ Web プレゼンテーション (`slide_html/index.html`)**:
   - 会場での登壇やオンライン勉強会向けの HTML5 プレゼンテーション。
   - **キーボードナビゲーション**:
     - `Space` / `→` / `PageDown`: 次のスライドへ進む
     - `←` / `PageUp`: 前のスライドへ戻る
     - `F`: フルスクリーン（全画面）表示の切り替え
     - `O` / `Esc`: スライド全体をグリッド一覧表示するオーバービューモード
2. **1 スライド 1 ページのベクター PDF (`slide.pdf`)**:
   - 参加者への事前配布、DocSend / SpeakerDeck へのアップロード、印刷向けの PDF。
   - Playwright によるヘッドレスレンダリングにより、各スライドが 1 ページずつ欠けのない 16:9 ベクター PDF として忠実に焼き込まれます。
