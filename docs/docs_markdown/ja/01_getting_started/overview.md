# Drawlib とは

従来の技術ドキュメント作成では、**ソースコード**（Git）、**図版**（外部の GUI 作図ツール）、**文章**（外部の Wiki 等）がそれぞれ分断されており、コードの進化に伴ってアーキテクチャ図が必然的に陳腐化してしまいます。

Drawlib は **「Illustration as Code（コードとしての図解）」** と **「Illustrated Documentation as Code（コードとしての図解ドキュメント）」** によってこの分断を解消し、Python コード・図版・マルチフォーマットのドキュメント出力を単一の Git リポジトリ内で常に同期させます。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/01_getting_started/overview/overview_paradigm_shift.png" alt="overview_1" />
  <figcaption class="drawlib-caption">従来のワークフローと Drawlib ワークフローの比較（APNG アニメーション）</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from __future__ import annotations

import os
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import ai, code, devops, phosphor, workspace
from drawlib.images import image
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

# 16:9 widescreen canvas matching index.md (128 x 72)
setup(width=128, height=72)
anim = Animation(fps=10.0, loop=0)

FAVICON_PATH = (
    "_assets/favicon.png"
    if os.path.exists("_assets/favicon.png")
    else "../_assets/favicon.png"
)

TITLE_TRAD = Styles.DarkBold.patch(text_size=15.5, halign="left")
TITLE_DRAWLIB = Styles.PrimaryBold.patch(text_size=15.5, halign="left")
SUB_MUTED = Styles.MutedBold.patch(text_size=10.5, halign="right")
SUB_PRIMARY = Styles.PrimaryBold.patch(text_size=10.5, halign="right")

TOOL_TEXT = Styles.DarkBold.patch(text_size=11.0, halign="left")
STEP_TEXT = Styles.DarkBold.patch(text_size=11.5, halign="left")
STEP_TEXT_WHITE = Styles.WhiteBold.patch(text_size=11.5, halign="left")

TOOL_CARD = Styles.Neutral.patch(
    shape_fill_color=(246, 248, 252),
    shape_line_color=(200, 212, 228),
    shape_line_width=1.2,
    shape_r=1.6,
)
STEP_CARD = Styles.Neutral.patch(
    shape_fill_color=(255, 255, 255),
    shape_line_color=(208, 218, 232),
    shape_line_width=1.2,
    shape_r=1.6,
)
STEP_CARD_HERO = Styles.PrimaryFlat.patch(shape_r=1.6)


def draw_drawio_badge(xy: tuple[float, float], size: float = 5.0) -> None:
    """Draw a clean Draw.io-style orange diagram app icon."""
    cx, cy = xy
    rectangle(
        xy,
        width=size,
        height=size,
        style=Styles.Neutral.patch(
            shape_fill_color=(240, 135, 5),
            shape_line_width=0,
            shape_r=0.9,
        ),
    )
    top_pt = (cx, cy + size * 0.23)
    bl_pt = (cx - size * 0.24, cy - size * 0.23)
    br_pt = (cx + size * 0.24, cy - size * 0.23)
    wire = Styles.White.patch(line_width=1.1)
    line(top_pt, bl_pt, style=wire)
    line(top_pt, br_pt, style=wire)
    node_st = Styles.Neutral.patch(shape_fill_color=(255, 255, 255), shape_line_width=0, shape_r=0.2)
    for pt in (top_pt, bl_pt, br_pt):
        rectangle(pt, width=size * 0.30, height=size * 0.22, style=node_st)


def draw_step_badge(xy: tuple[float, float], num: str, *, inverted: bool = False) -> None:
    """Draw numbered circular step badge."""
    if inverted:
        circle(
            xy,
            radius=2.6,
            style=Styles.Neutral.patch(
                shape_fill_color=(255, 255, 255),
                shape_line_width=0,
            ),
        )
        text(xy, num, style=Styles.PrimaryBold.patch(text_size=10.5))
    else:
        circle(
            xy,
            radius=2.6,
            style=Styles.Neutral.patch(
                shape_fill_color=(238, 244, 255),
                shape_line_color=(180, 198, 228),
                shape_line_width=1.1,
            ),
        )
        text(xy, num, style=Styles.PrimaryBold.patch(text_size=10.5))


def draw_traditional_scene(visible_steps: int) -> None:
    """Scene 1: Traditional 4-step workflow across Word, VS Code, and Draw.io."""
    # Header
    phosphor.arrows_left_right((10.5, 64.0), width=4.8, style=Styles.Danger)
    text((14.8, 64.0), "Traditional Workflow", style=TITLE_TRAD)
    text((120.0, 64.0), "Switching Across 3 Disconnected Tools", style=SUB_MUTED)
    line((8.0, 58.2), (120.0, 58.2), style=Styles.MutedThin)

    steps = [
        ("1", "word", "Word", "Write initial design spec in Word", 49.5),
        ("2", "vscode_ai", "VS Code", "Develop application code", 37.0),
        ("3", "drawio", "Draw.io", "Read code & manually draw diagrams in Draw.io", 24.5),
        ("4", "word", "Word", "Read code, write Word spec & paste diagrams", 12.0),
    ]

    for idx in range(visible_steps):
        num, tool_key, tool_label, desc, y = steps[idx]

        # Context-switch connector between different tools
        if idx > 0:
            prev_y = steps[idx - 1][4]
            line(
                (21.5, prev_y - 4.7),
                (21.5, y + 4.7),
                arrow_head="->",
                style=Styles.DangerDashed.patch(line_width=1.3),
            )

        # Left tool pill (x = 8.0 .. 35.0, cx = 21.5, width = 27.0)
        rectangle((21.5, y), width=27.0, height=9.2, style=TOOL_CARD)
        if tool_key == "word":
            workspace.word((15.0, y), width=5.0, style=Styles.Neutral)
            text((19.2, y), tool_label, style=TOOL_TEXT)
        elif tool_key == "vscode_ai":
            code.vscode((12.4, y), width=4.4, style=Styles.Neutral)
            ai.gemini((17.3, y), width=4.3, style=Styles.Neutral)
            text((21.2, y), tool_label, style=TOOL_TEXT)
        else:
            draw_drawio_badge((15.0, y), size=4.8)
            text((19.2, y), tool_label, style=TOOL_TEXT)

        # Right action card (x = 37.5 .. 120.0, cx = 78.75, width = 82.5)
        rectangle((78.75, y), width=82.5, height=9.2, style=STEP_CARD)
        draw_step_badge((42.5, y), num)
        text((47.0, y), desc, style=STEP_TEXT)


def draw_drawlib_scene(visible_steps: int) -> None:
    """Scene 2: Drawlib 3-step workflow unified inside VS Code + GitHub Repo + AI Agent."""
    # Header
    image((10.5, 64.0), width=5.4, image=FAVICON_PATH)
    text((15.0, 64.0), "Drawlib Workflow", style=TITLE_DRAWLIB)
    text((120.0, 64.0), "Unified in VS Code + GitHub Repository", style=SUB_PRIMARY)
    line((8.0, 58.2), (120.0, 58.2), style=Styles.MutedThin)

    # Unified GitHub / Git Repository container (x = 7.0 .. 121.0, y = 6.0 .. 55.0)
    rectangle(
        (64.0, 30.5),
        width=114.0,
        height=49.0,
        style=Styles.PrimaryNeutral.patch(
            shape_fill_color=(245, 248, 255),
            shape_line_color=(165, 185, 232),
            shape_line_width=1.4,
            shape_r=2.2,
        ),
    )
    devops.github((11.8, 51.0), width=4.2, style=Styles.Neutral)
    text(
        (15.4, 51.0),
        "GitHub / Git Repository (Specs, Source Code & Illustrated Docs Together)",
        style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
    )

    steps = [
        ("1", "Design specs in Git Repo with AI Agent & Drawlib", 40.2, False),
        ("2", "Develop application code", 26.8, False),
        ("3", "AI Agent reads repo code & auto-writes illustrated docs", 13.4, True),
    ]

    for idx in range(visible_steps):
        num, desc, y, is_hero = steps[idx]

        if idx > 0:
            prev_y = steps[idx - 1][2]
            line(
                (23.5, prev_y - 4.9),
                (23.5, y + 4.9),
                arrow_head="->",
                style=Styles.PrimaryBold.patch(line_width=1.4),
            )

        # Left tool pill: Always VS Code + Gemini AI Agent across all 3 steps
        rectangle(
            (23.5, y),
            width=27.0,
            height=9.6,
            style=STEP_CARD.patch(shape_line_color=(175, 192, 230)),
        )
        code.vscode((14.4, y), width=4.4, style=Styles.Neutral)
        ai.gemini((19.3, y), width=4.3, style=Styles.Neutral)
        text((23.2, y), "VS Code", style=TOOL_TEXT)

        # Right action card (x = 39.5 .. 118.0, cx = 78.75, width = 78.5)
        rectangle(
            (78.75, y),
            width=78.5,
            height=9.6,
            style=STEP_CARD_HERO if is_hero else STEP_CARD,
        )
        draw_step_badge((44.2, y), num, inverted=is_hero)
        text(
            (48.6, y),
            desc,
            style=STEP_TEXT_WHITE if is_hero else STEP_TEXT,
        )


# -------------------------------------------------------------------------
# Scene 1: Traditional Workflow (4 progressive steps + read hold)
# -------------------------------------------------------------------------
with anim.frame(duration=0.95):
    draw_traditional_scene(1)

with anim.frame(duration=0.95):
    draw_traditional_scene(2)

with anim.frame(duration=0.95):
    draw_traditional_scene(3)

with anim.frame(duration=2.70):
    draw_traditional_scene(4)

# -------------------------------------------------------------------------
# Scene 2: Drawlib Workflow (3 progressive steps + read hold)
# -------------------------------------------------------------------------
with anim.frame(duration=1.05):
    draw_drawlib_scene(1)

with anim.frame(duration=1.00):
    draw_drawlib_scene(2)

with anim.frame(duration=3.20):
    draw_drawlib_scene(3)

save()
```

</details>



---

## パラダイムシフト: なぜ「Illustration as Code」なのか？

AI コーディングアシスタントによって加速する現代のソフトウェア開発では、コードのリファクタリングや機能追加がかつてないスピードで進みます。しかしその一方で、システムアーキテクチャ設計書、データベーススキーマ、ワークフロー図などの更新は置き去りにされがちであり、**ドキュメントの形骸化（Documentation Rot）** やオンボーディングのボトルネックを引き起こしています。

### 現代のワークフローにおける GUI ツールの限界

従来の技術作図は、ドラッグ＆ドロップ操作の GUI ツール（Draw.io、Visio、Lucidchart、Figma など）に依存してきました。ホワイトボード代わりの素早いラフスケッチには便利ですが、書き出したバイナリ画像（PNG、JPEG）を別管理の Wiki に貼り付けて運用する手法には、看過できない構造的欠陥があります。

- **深刻なツールの分断**: マイクロサービスの経路を 1 つ変更するだけでも、Git 上でコードを編集し、外部の GUI ツールを手動で開いて箱を描き直し、PNG を書き出して外部ドキュメントや Wiki に再アップロードする手間が発生します。
- **意味のあるバージョン管理の欠如**: バイナリ画像はプルリクエスト上で意味のある Git diff を生成できません。レビュアーはどのアーキテクチャ要素が変更されたのかを正確に把握できません。
- **AI エージェントがバイナリアセットを編集できない**: AI コーディングエージェントはコードベースの読み書きをシームレスに行えますが、GUI ソフトウェア上のピクセル操作やドラッグ＆ドロップ編集を行うことはできません。
- **デザインとブランドの一貫性の崩れ**: 色使い、線の太さ、余白、フォントサイズが担当者ごとにばらつき、組織としてのデザイン基準が徐々に損なわれていきます。

### 生の SVG 生成や Matplotlib 直接記述の落とし穴

作図をコードで自動化しようと試みる際、エンジニアは AI エージェントに生の SVG XML や低レベルな Matplotlib スクリプトを直接生成させがちです。しかし実務においては、どちらのアプローチもすぐに限界に突き当たります。

- **生の SVG 生成**:
  - LLM はブラウザのレイアウトエンジンなしではフォントのグリフ幅や動的な複数行折り返しを正確に計算できないため、テキストが枠線からはみ出す問題が頻発します。
  - 正確な接続ベクトル、直交ルーティング、矢印の向きを手計算で求めるには複雑な三角関数の計算が必要となり、わずかなズレが簡単に発生します。
  - 何百もの生の `<path>` や `<polygon>` 要素を羅列した XML は保守不能な塊となり、人間がレビューや監査を行うことが困難です。
- **Matplotlib の直接スクリプティング**:
  - Matplotlib は本来、学術・科学計算向けのデータ可視化（散布図、ヒストグラム、折れ線グラフ）のために設計されており、ソフトウェアシステム設計向けではありません。
  - アーキテクチャ要素（ノード、境界コンテナ、シーケンスのライフライン、分岐ゲート、標準クラウドアイコンなど）を表すネイティブな抽象化が存在しません。
  - アイコン付きのラベルボックスを 1 つ描画してスタイリングするだけでも、何十行もの低レベルなボイラープレートコードを記述する必要があります。

### Drawlib の解決策: 「Illustration as Code」

Drawlib は、アーキテクチャ図や技術ドキュメントを、標準的なソフトウェアエンジニアリング手法で管理されるファーストクラスの成果物として扱います。

1. **Git 内の単一の情報源（Single Source of Truth）**: ソースコード、Markdown の本文、そして宣言的な Python 作図コードが同じリポジトリ内に共存し、1 つのコミットでアトミックに更新できます。
2. **決定論的かつ再現可能**: 幾何配置、間隔、カラーパレットの階調、タイポグラフィがすべてコード上で数学的に定義されるため、再ビルドしてもビット単位で完全に同一の視覚出力が保証されます。
3. **高水準なドメインプリミティブ**: 宣言的な抽象コンポーネント（`ArchitectureDiagram`、`ChevronProcess`、`Table`、`ArchitectureGraph`）により、ピクセル単位の精密な制御を維持しつつレイアウトのボイラープレートを排除します。
4. **マルチフォーマットへの一括コンパイル**: 単一の Markdown ソースから、静的 HTML サイト、GitHub 用 Markdown、鮮明なベクター PDF、MS Word（`.docx`）文書、さらに 16:9 の HTML / PDF / PowerPoint（`.pptx`）スライドデッキへとコンパイルできます。
5. **一元化されたスタイルガバナンス**: テーマトークン（`DefaultStyles`、`GoogleStyles`、`MonochromeStyles`）により、図形・コネクタ・テキスト・アイコンのすべてが統一された視覚的階層に従います。

---

## AI ネイティブ設計

Drawlib は、**AI 支援ソフトウェア開発** の時代を見据えて意図的に設計されています。

大規模言語モデル（LLM）や AI コーディングエージェント（Claude Code、Cursor、Gemini など）は宣言的なコードを書くことに長けている一方、手作業の GUI ツールを扱うことは苦手です。Drawlib の図版はすべてクリーンな Python コードまたは Markdown 埋め込みブロック（` ```drawlib `）として記述されるため、AI エージェントは以下の作業を自在に遂行できます。

- **既存図版の理解とリファクタリング**: Python ソースコードを読むだけで、既存の図版の構造を正確に解析・改修できます。
- **複雑な図版の自動生成**: リポジトリのコード解析に基づき、本格的なクラウド構成図、シーケンス図、フローチャートを自律的に作成できます。
- **構文ルールのオンデマンド参照**: CLI（`drawlib rules show <topic>`）を通じて、組み込みのリファレンスマニュアルをいつでも直接照会できます。
- **自律的な視覚的自己修正**: 座標グリッドを重ねた画像（`drawlib show -g`）を出力し、マルチモーダル視覚ツールで自ら確認することで、ラベルの見切れや線の重なりを自律的に修正できます。

---

## レイヤードアーキテクチャ

Drawlib は密接に連携する 4 つのレイヤーで構成されており、低レベルの柔軟性と高レベルの生産性を両立しています。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/01_getting_started/overview/drawlib_layered_architecture.png" alt="overview_2" />
  <figcaption class="drawlib-caption">Drawlib のレイヤードアーキテクチャ</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=54)

title_dark = Styles.DarkBold.patch(text_size=11.5, halign="left")
sub_dark = Styles.Dark.patch(text_size=10.5, halign="left")
title_white = Styles.WhiteBold.patch(text_size=11.5, halign="left")
sub_white = Styles.White.patch(text_size=10.5, halign="left")

# Layer 4: Animation, Slide & Doc Builder
rectangle((60.0, 45.0), width=112.0, height=10.0, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.stack((10.5, 45.0), width=5.2, style=Styles.Primary)
text((15.5, 47.0), "Layer 4: Animation, Slide & Doc Builder", style=title_dark)
text((15.5, 42.8), "drawlib.anim • drawlib.slide • drawlib.tools • CLI Compiler", style=sub_dark)

# Layer 3: High-Level Visualizations
rectangle((60.0, 33.0), width=112.0, height=10.0, style=Styles.Neutral.patch(shape_r=1.5))
phosphor.cube((10.5, 33.0), width=5.2, style=Styles.Primary)
text((15.5, 35.0), "Layer 3: High-Level Visualizations & Geometry", style=title_dark)
text((15.5, 30.8), "drawlib.graph • diagrams • smartarts • charts • math", style=sub_dark)

# Layer 2: Drawing Primitives
rectangle((60.0, 21.0), width=112.0, height=10.0, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
phosphor.paint_brush((10.5, 21.0), width=5.2, style=Styles.Primary)
text((15.5, 23.0), "Layer 2: Drawing Primitives & Assets", style=title_dark)
text((15.5, 18.8), "drawlib.shapes (43 shapes) • lines • text • icons • images", style=sub_dark)

# Layer 1: Core Engine (Hero anchor)
rectangle((60.0, 9.0), width=112.0, height=10.0, style=Styles.PrimaryFlat.patch(shape_r=1.5))
phosphor.gear((10.5, 9.0), width=5.2, style=Styles.WhiteBold)
text((15.5, 11.0), "Layer 1: Core Engine (Foundation)", style=title_white)
text((15.5, 6.8), "drawlib.canvas • styles • types • fonts (Cartesian Engine)", style=sub_white)

save()
```

</details>



1. **Layer 1: コアエンジン (`drawlib.canvas`, `drawlib.styles`, `drawlib.types`, `drawlib.fonts`)**  
   キャンバスのライフサイクル、デカルト座標系、ローカル座標変換、テーマ解決、および多言語対応フォントのタイポグラフィを管理します。
2. **Layer 2: 描画プリミティブ (`drawlib.shapes`, `drawlib.lines`, `drawlib.text`, `drawlib.icons`, `drawlib.images`)**  
   **43 種** のベクター図形（`cylinder`、`cube`、`document`、`cloud`、`brace`、`gear`、`math_symbol`、`face`、`bubblespeech` など）、ルーティングや矢印を備えた柔軟なコネクタ線、タイポグラフィ、および合計 **4,538 個のアイコン** を収録する **34 の標準アイコンモジュール**（`phosphor` ベクターアイコン、`gcp` / `aws` / `azure` クラウドアイコン、15 種の公式ドメインブランドパック、15 種の Drawlib Original 2D パステルパック）を提供します。
3. **Layer 3: 高水準ビジュアライゼーションと幾何計算 (`drawlib.graph`, `drawlib.smartarts`, `drawlib.charts`, `drawlib.diagrams`, `drawlib.math`)**  
   すぐに使えるドメイン別コンポーネント群です。自動レイアウトグラフ（`LayerGraph`、`ArchitectureGraph`、`TreeGraph`、`RadialGraph`、`GridGraph`）、クラウドアーキテクチャ図、フロー図、シーケンス図、UML クラス図・ステートマシン図、ER 図、データチャート、プロセスフロー、地理マップ（`drawlib.smartarts.GeoMap`）、および幾何計算・パス／カラー補間ユーティリティ（`drawlib.math`）を備えています。
4. **Layer 4: アニメーション・プレゼンテーション・ドキュメントビルダ (`drawlib.anim`, `drawlib.slide`, `drawlib.tools`)**  
   マルチフレームアニメーション（APNG および Animated WebP 対応の `drawlib.anim`）、16:9 ワイドスクリーンのスライドステージ＆コンパイラ（`drawlib.slide`）、および `drawlib` ブロックを埋め込んだ Markdown ファイルをレスポンシブな静的 HTML サイト・GitHub 対応 Markdown・スタンドアロンの PDF／MS Word（`.docx`）文書・16:9 の HTML／PDF／PowerPoint（`.pptx`）スライドデッキへとコンパイルするプログラマティックなビルド・プレビューサーバー・キャッシュ API（`drawlib.tools`）を提供します。
