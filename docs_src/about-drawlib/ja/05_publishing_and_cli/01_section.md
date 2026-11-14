::: block xy=(0, 0) width=1920 height=1080
```drawlib file=ch05_section_ja.svg
import utils

utils.draw_chapter_divider(
    5,
    "5つのプロジェクト種別と出力",
    subtitle="Site・Catalog・Doc・Slide・Images を単一コンパイラで",
    topics=[
        "5つのプロジェクト種別の全体像",
        "Web公開：SiteとCatalog",
        "技術白書：HTML・PDF・Word出力",
        "16:9スライド・発表者画面・PPTX",
    ],
    total_chapters=6,
    badge_text="Chapter 5 / 6",
)
```
:::

::: note
第5章「5つのプロジェクト種別と出力」に入ります。
ここまで、Drawlibの描画プリミティブ、SmartArts、Charts、Diagrams、そして自動グラフレイアウトを見てきました。
本章では個別の図解から一歩引き、MarkdownとPythonで書かれたリポジトリを単一のコンパイラからどのように公開成果物へ変換するかを解説します。体系的な技術ドキュメントサイト（`site`）、v0.3.10のAPI・スキーマリファレンス辞書（`catalog`）、表紙・目次付き技術白書（`doc`）、16:9プレゼンテーション（`slide`）、そして画像アセット一括生成（`images`）の5種別と、ベクターPDF・Word・PowerPoint出力を見ていきましょう。
:::
