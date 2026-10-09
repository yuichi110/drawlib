# AIとDrawlibによるドキュメント自動生成

AI時代の "Illustrated Documentation as Code"

```drawlib 640px center file:fig_cover_autonomous_loop.png caption:"AI Agent による作図・視覚的自律検証ループ"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=52)

ts = Styles.WhiteBold.patch(text_size=9.5)

# 1. コンテキスト読解
rectangle((20.5, 18), width=25, height=20, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.file_code(xy=(20.5, 23.5), width=5.5, style=Styles.White)
text((20.5, 13.5), text="1. コンテキスト読解\n(コード・設計意図)", style=ts)

# 2. 作図コード生成
rectangle((51.0, 18), width=25, height=20, style=Styles.AccentFlat.patch(shape_r=2.0))
phosphor.code(xy=(51.0, 23.5), width=5.5, style=Styles.White)
text((51.0, 13.5), text="2. 作図コード生成\n(Python 宣言的記述)", style=ts)

# 3. グリッド描画
rectangle((81.5, 18), width=25, height=20, style=Styles.SecondaryFlat.patch(shape_r=2.0))
phosphor.image(xy=(81.5, 23.5), width=5.5, style=Styles.White)
text((81.5, 13.5), text="3. グリッド描画\n(drawlib show -g)", style=ts)

# 4. 自律レビュー
rectangle((112.0, 18), width=25, height=20, style=Styles.SuccessFlat.patch(shape_r=2.0))
phosphor.eye(xy=(112.0, 23.5), width=5.5, style=Styles.White)
text((112.0, 13.5), text="4. 自律レビュー\n(視覚的セルフ検証)", style=ts)

# 順方向の矢印
line((33.0, 18), (38.5, 18), arrow_head="->", style=Styles.DarkBold)
line((63.5, 18), (69.0, 18), arrow_head="->", style=Styles.DarkBold)
line((94.0, 18), (99.5, 18), arrow_head="->", style=Styles.DarkBold)

# 自律フィードバックループ
line((112.0, 28.0), (112.0, 42.0), style=Styles.DangerBold)
line((112.0, 42.0), (51.0, 42.0), style=Styles.DangerBold)
line((51.0, 42.0), (51.0, 28.0), arrow_head="->", style=Styles.DangerBold)

# ループのラベルとアイコン
phosphor.arrows_clockwise(xy=(57.0, 46.0), width=4.0, style=Styles.Danger)
text((83.0, 46.0), text="不備があれば座標を自律修正して再試行 (Feedback Loop)", style=Styles.DangerBold.patch(text_size=9.5))
```

**作成者**: Drawlib Core Team  
**対象**: ソフトウェアエンジニア・アーキテクト・AI ペアプログラマー  
**バージョン**: 0.3.0  
**発行日**: 2026年10月
