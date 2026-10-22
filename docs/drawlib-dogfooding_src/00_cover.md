# AIとDrawlibによるドキュメント自動生成

AI時代の "Illustrated Documentation as Code"

```drawlib align=center file=fig_cover_autonomous_loop.png caption="AI Agent による作図・視覚的自律検証ループ"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=48)

ts_dark = Styles.DarkBold.patch(text_size=10.5)
ts_white = Styles.WhiteBold.patch(text_size=10.5)

# 1. コンテキスト読解 (Neutral)
rectangle((18.0, 16.5), width=25, height=21, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.file_code(xy=(18.0, 21.5), width=5.2, style=Styles.Dark)
text((18.0, 12.5), text="1. コンテキスト読解\n(コード・設計意図)", style=ts_dark)

# 2. 作図コード生成 (PrimaryFlat — Focal)
rectangle((48.0, 16.5), width=25, height=21, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.code(xy=(48.0, 21.5), width=5.2, style=Styles.White)
text((48.0, 12.5), text="2. 作図コード生成\n(Python 宣言的記述)", style=ts_white)

# 3. グリッド描画 (PrimaryNeutral)
rectangle((78.0, 16.5), width=25, height=21, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.image(xy=(78.0, 21.5), width=5.2, style=Styles.Primary)
text((78.0, 12.5), text="3. グリッド描画\n(drawlib show -g)", style=ts_dark)

# 4. 自律レビュー (SecondaryNeutral)
rectangle((108.0, 16.5), width=25, height=21, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.eye(xy=(108.0, 21.5), width=5.2, style=Styles.Secondary)
text((108.0, 12.5), text="4. 自律レビュー\n(視覚的セルフ検証)", style=ts_dark)

# 順方向の矢印
line((30.5, 16.5), (35.5, 16.5), arrow_head="->", style=Styles.DarkBold)
line((60.5, 16.5), (65.5, 16.5), arrow_head="->", style=Styles.DarkBold)
line((90.5, 16.5), (95.5, 16.5), arrow_head="->", style=Styles.DarkBold)

# 自律フィードバックループ
line((108.0, 27.0), (108.0, 38.5), style=Styles.DangerBold)
line((108.0, 38.5), (48.0, 38.5), style=Styles.DangerBold)
line((48.0, 38.5), (48.0, 27.0), arrow_head="->", style=Styles.DangerBold)

# ループのラベルとアイコン
phosphor.arrows_clockwise(xy=(51.5, 43.0), width=4.0, style=Styles.Danger)
text((55.0, 43.0), text="不備があれば座標を自律修正して再試行 (Feedback Loop)", style=Styles.DangerBold.patch(text_size=10.5, halign="left"))

save()
```

**作成者**: Drawlib Core Team  
**対象**: ソフトウェアエンジニア・アーキテクト・AI ペアプログラマー  
**バージョン**: 0.3.0  
**発行日**: 2026年10月
