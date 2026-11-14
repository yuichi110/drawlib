::: block xy=(120, 250) width=880 height=580
# ご清聴ありがとうございました

## 図解もドキュメントも、すべてコードで。

---

- **Docs**: `https://www.drawlib.com/`
- **Quickstart Guide**: `https://www.drawlib.com/quickstart/`
- **API Catalog**: `https://www.drawlib.com/api/`
- **Examples & GitHub**: `https://examples.drawlib.com/` · `github.com/yuichi110/drawlib`
:::

::: block xy=(1040, 200) width=760 height=680
```drawlib file=thank_you_card_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=76, height=68)

# Soft PrimaryNeutral emblem card
rectangle((38.0, 34.0), width=70.0, height=62.0, style=Styles.PrimaryNeutral.patch(shape_r=3.5))

# Top subtle accent pill
rectangle((38.0, 55.5), width=44.0, height=5.8, style=Styles.WhiteFlat.patch(shape_r=2.8))
text((38.0, 55.5), "ILLUSTRATION & DOCS AS CODE", style=Styles.PrimaryBold.patch(text_size=12.2))

# 3 Large Emblem Icons (code, sparkle, presentation_chart)
emblems = [
    (18.5, phosphor.code, Styles.WhiteFlat, Styles.PrimaryBold, "コードで描く"),
    (38.0, phosphor.sparkle, Styles.PrimaryFlat, Styles.WhiteBold, "AIネイティブ"),
    (57.5, phosphor.presentation_chart, Styles.WhiteFlat, Styles.PrimaryBold, "自在に出力"),
]

line((18.5, 37.5), (57.5, 37.5), style=Styles.Primary)

for ex, eicon, cstyle, istyle, elabel in emblems:
    circle((ex, 37.5), radius=7.6, style=cstyle)
    eicon((ex, 37.5), width=8.2, style=istyle)
    text((ex, 25.5), elabel, style=Styles.DarkBold.patch(text_size=13.5))

line((13.0, 19.5), (63.0, 19.5), style=Styles.Primary)

# Bottom open-source badge & tagline
text((38.0, 13.5), "Drawlib — Apache 2.0 Open Source", style=Styles.DarkBold.patch(text_size=15.0))
text((38.0, 8.2), "pip / uv install drawlib", style=Styles.PrimaryBold.patch(text_size=13.5))

save()
```
:::

::: note
最後までご清聴いただき、誠にありがとうございました！
Drawlibは Apache 2.0 ライセンスのオープンソースソフトウェアとして公開されています。体系的なガイドは `www.drawlib.com`、全16章のクイックスタートハンドブックは `www.drawlib.com/quickstart/`、APIリファレンスは `www.drawlib.com/api/`、そして実例集は `examples.drawlib.com` および GitHub（`github.com/yuichi110/drawlib`）からご覧いただけます。
ご質問・ディスカッションをぜひお待ちしております！
:::
