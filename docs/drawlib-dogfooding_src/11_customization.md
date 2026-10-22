# 第11章: スタイルとテーマのカスタマイズ

Drawlib では、ドキュメント全体の配色や作図トーンをプロジェクト単位で柔軟にカスタマイズできます。

## 11.1 `styles.py` による作図テーマの制御

プロジェクトのルート（またはソースディレクトリ）にある `styles.py` で、作図時に使用される `Colors` と `Styles` を決定します:

```python
from drawlib.fonts import FontJapanese
from drawlib.preset_colors import GoogleColors
from drawlib.preset_styles import GoogleStyles

# カラーパレットとスタイルの初期化
Colors = GoogleColors()
Styles = GoogleStyles().patch_font(
    regular=FontJapanese.SANSSERIF_REGULAR,
    bold=FontJapanese.SANSSERIF_BOLD,
    thin=FontJapanese.SANSSERIF_THIN,
)
```

## 11.2 利用可能なスタイルプリセットとニュートラルカードトークン

Drawlib には 3 つの全体テーマプリセットが用意されています:

- **`DefaultStyles` / `DefaultColors`**: Tailwind / VitePress にインスパイアされた開発者向け標準テーマ。
- **`GoogleStyles` / `GoogleColors`**: Material Design および Google Docs/Slides に準拠した親しみやすいテーマ。
- **`MonochromeStyles` / `MonochromeColors`**: 印刷物や公的文書に適した白黒・グレースケールテーマ。

いずれのテーマプリセットでも、図面が派手な「虹色（レインボー）ダイアグラム」になるのを防ぐため、**50% 以上の要素を落ち着いたニュートラルカードで組む（50%+ Neutral Baseline Rule）** ための専用トークンが標準搭載されています:

- **`Styles.Neutral`**: 白〜淡いグレー背景の標準カードスタイル（一般的なノードやコンテナ用）。
- **`Styles.PrimaryNeutral`**: プライマリカラーの極淡色背景＋細枠線カード（主要グループやサブシステム用）。
- **`Styles.SecondaryNeutral`**: セカンダリカラーの極淡色背景＋細枠線カード（補助コンポーネントや周辺系用）。
- **`Styles.PrimaryFlat` / `Styles.AccentFlat` / `Styles.DarkFlat`**: 視線を集める 1〜2 個の主役ノードやコンテナのヘッダーバーに限定して使用する高彩度・高コントラストな塗りスタイル。

## 11.3 既存スタイルの部分変更 (`.patch()`) と `utils.py` の共通化

既存のスタイルをベースに、特定の色や線幅、角丸、フォントサイズだけを変更した新しいスタイルを `.patch()` で簡単に派生できます。また、プロジェクト内の `utils.py` に定義した定数やヘルパー関数は、各 Markdown の ````drawlib```` コードブロックから `from drawlib.utils import ...` として直接インポートできます:

```python
# utils.py での定義例
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# PrimaryNeutral をベースに角丸と線幅をカスタマイズ
CARD_STYLE = Styles.PrimaryNeutral.patch(shape_r=2.0, shape_line_width=1.5)
HEADER_STYLE = Styles.PrimaryFlat.patch(shape_r=1.5)


def draw_titled_card(xy: tuple[float, float], width: float, height: float, title: str) -> None:
    """ヘッダーバー付きのニュートラルカードを描画する共通ヘルパー。"""
    cx, cy = xy
    rectangle((cx, cy), width=width, height=height, style=CARD_STYLE)
    rectangle(
        (cx, cy + height / 2 - 3.5),
        width=width - 2.0,
        height=5.5,
        style=HEADER_STYLE,
        text=title,
        text_style=Styles.WhiteBold.patch(text_size=11.0),
    )
```

各章の ````drawlib```` コードブロックからは以下のように呼び出せます:

```python
from drawlib.utils import CARD_STYLE, draw_titled_card

draw_titled_card((50, 25), width=40, height=30, title="Auth Service")
```

## 11.4 ドキュメントスタイル (`style.css`) との連動

`drawlib init` で `--style google` を指定すると、`styles.py` だけでなく `style.css` にも Google テーマ（青のアクセントカラー、Google Sans フォントスタック、クリーンなカード余白）が展開されます。これにより、**本文のテキストと作図のビジュアルが完全に調和した美しいドキュメント** が自動的に仕上がります。
