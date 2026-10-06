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

## 11.2 利用可能なスタイルプリセット

- **`DefaultStyles` / `DefaultColors`**: Tailwind / VitePress にインスパイアされた開発者向け標準テーマ。
- **`GoogleStyles` / `GoogleColors`**: Material Design および Google Docs/Slides に準拠した親しみやすいテーマ。
- **`MonochromeStyles` / `MonochromeColors`**: 印刷物や公的文書に適した白黒・グレースケールテーマ。

## 11.3 既存スタイルの部分変更 (`.patch()`)

既存のスタイルをベースに、特定の色や線幅、フォントサイズだけを変更した新しいスタイルを簡単に派生できます:

```python
from drawlib.styles import Styles

# PrimaryFlat をベースに角丸と背景色を変更
my_card_style = Styles.PrimaryFlat.patch(
    shape_fill_color=(235, 248, 255),
    shape_line_color=(49, 130, 206),
    shape_line_width=1.5,
)
```

## 11.4 ドキュメントスタイル (`style.css`) との連動

`drawlib init` で `--style google` を指定すると、`styles.py` だけでなく `style.css` にも Google テーマ（青のアクセントカラー、Google Sans フォントスタック、クリーンなカード余白）が展開されます。これにより、**本文のテキストと作図のビジュアルが完全に調和した美しいドキュメント** が自動的に仕上がります。
