::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — コードで描く図解と技術ドキュメント*
:::

::: block xy=(80, 36) width=1760 height=72
# 2層キャッシュ機構と統合CLIコマンド
:::

::: block xy=(80, 140) width=640 height=800
```drawlib file=cache_kpis_ja.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=64, height=80)
utils.draw_kpi_cards(
    [
        ("< 1s", "高速差分ビルド", "SQLite SHA-256 .drawlib/cache.db"),
        ("50+", "AIルールトピック", "drawlib rules show で都度参照"),
        ("Zero", "リンク切れゼロ", "drawlib serve --check で自動検証"),
    ],
    width=64,
    height=80,
)
save()
```
:::

::: block xy=(760, 140) width=1080 height=800
```drawlib file=two_tier_cache_cli_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import ChevronProcess, Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=108, height=80)

# ==============================================================================
# Top Panel: Two-Tier Cache Architecture
# ==============================================================================
top_panel = Panel(
    "2層キャッシュアーキテクチャ",
    style=Styles.White.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.0),
    icon=phosphor.database,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=9.2,
)
top_panel.draw(xy=(2.0, 38.5), width=104.0, height=38.5)

# Tier 1 Card: Package Asset Cache
rectangle((28.8, 53.2), width=47.5, height=23.5, style=Styles.Neutral.patch(shape_r=1.8))
circle((11.5, 58.8), radius=4.2, style=Styles.WhiteFlat)
phosphor.package((11.5, 58.8), width=4.8, style=Styles.PrimaryBold)
text((17.2, 60.2), "Tier 1: アセットキャッシュ", style=Styles.DarkBold.patch(text_size=14.5, halign="left"))
text((17.2, 56.2), "drawlib cache list / download", style=Styles.PrimaryBold.patch(text_size=12.5, halign="left"))
text(
    (7.8, 47.0),
    "フォント・34種アイコン・Chromiumを\nオンデマンド取得し事前キャッシュ",
    style=Styles.Dark.patch(text_size=12.8, halign="left"),
)

# Tier 2 Card: SQLite Build Cache (.drawlib/cache.db)
rectangle((79.2, 53.2), width=47.5, height=23.5, style=Styles.PrimaryNeutral.patch(shape_r=1.8))
circle((62.0, 58.8), radius=4.2, style=Styles.WhiteFlat)
phosphor.lightning((62.0, 58.8), width=4.8, style=Styles.PrimaryBold)
text((67.8, 60.2), "Tier 2: ビルドキャッシュ", style=Styles.DarkBold.patch(text_size=14.5, halign="left"))
text((67.8, 56.2), ".drawlib/cache.db (SQLite)", style=Styles.PrimaryBold.patch(text_size=12.5, halign="left"))
text(
    (58.2, 47.0),
    "SHA-256内容＋スタイルハッシュ管理\nHTML・PDF・Office間で高速共有",
    style=Styles.Dark.patch(text_size=12.8, halign="left"),
)

# ==============================================================================
# Bottom Panel: Unified CLI Workflow (uv run drawlib ...)
# ==============================================================================
bot_panel = Panel(
    "統合CLIワークフロー  —  uv run drawlib <command>",
    style=Styles.White.patch(shape_r=2.2),
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=16.0),
    icon=phosphor.terminal_window,
    icon_style=Styles.WhiteBold,
    header_variant="filled",
    header_height=9.2,
)
bot_panel.draw(xy=(2.0, 3.0), width=104.0, height=32.0)

cli_flow = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=13.8),
    description_style=Styles.Muted.patch(text_size=11.5),
    corner_angle=62.0,
    spacing=1.4,
    flat_left_end=True,
)
cli_flow.add("init", description="5種別作成")
cli_flow.add("rules", description="仕様を参照")
cli_flow.add("show -g", description="グリッド検品", style=Styles.PrimaryNeutral)
cli_flow.add("build", description="Web/Office")
cli_flow.add(
    "serve",
    description="--check",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.8),
    description_style=Styles.White.patch(text_size=11.5),
)
cli_flow.draw(xy=(4.5, 6.2), width=99.0, height=16.8)

save()
```
:::

::: note
人間の執筆でもAIエージェントの反復検証でも、ビルドの速さは生産性に直結します。Drawlibは2層キャッシュ機構によって1秒未満の高速差分ビルドを実現しています。
- **Tier 1 — パッケージアセットキャッシュ（`drawlib cache list / download / clear`）**：多言語フォント、34種類のアイコンパック、ヘッドレスChromiumをオンデマンドで取得して保持し、初期インストールを軽量に保ちながらオフラインCIでの事前取得にも対応します。
- **Tier 2 — プロジェクト図解ビルドキャッシュ（`.drawlib/cache.db`）**：コード・`styles.py`・`utils.py`・出力形式のSHA-256ハッシュをキーとするSQLiteデータベースです。未変更の図版はHTML・PDF・DOCX・PPTXのすべてでミリ秒単位で再利用され、CI検証時には `--no-cache` で完全再生成も行えます。
これらすべてが `uv run drawlib` の一貫したCLI（`init`・`rules`・`show -g`・`build`・`serve --check`）に統合されています。
:::
