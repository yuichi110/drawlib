::: block xy=(0, 0) width=1920 height=1080
```drawlib
from drawlib.canvas import setup
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=192, height=108)

# Full-bleed calm neutral stage with subtle corner accents
rectangle((96.0, 54.0), width=192.0, height=108.0, style=Styles.Neutral)
circle(
    (16.0, 88.0),
    radius=24.0,
    style=Styles.PrimaryNeutral.patch(alpha=0.45, shape_line_width=0.0),
)
circle(
    (176.0, 18.0),
    radius=22.0,
    style=Styles.SecondaryNeutral.patch(alpha=0.45, shape_line_width=0.0),
)

# Top brand bar
rectangle((96.0, 106.8), width=192.0, height=2.4, style=Styles.PrimaryFlat)

# Top pill badge
rectangle(
    (96.0, 72.0),
    width=44.0,
    height=6.8,
    style=Styles.PrimaryFlat.patch(shape_r=3.4, shape_line_width=0.0),
)
text(
    (96.0, 72.0),
    "THANK YOU  •  Q&A",
    style=Styles.WhiteBold.patch(text_size=11.5),
)

# Main message
text(
    (96.0, 55.0),
    "Thank You!",
    style=Styles.BlackBold.patch(text_size=40.0),
)
text(
    (96.0, 41.5),
    "Questions & Discussion",
    style=Styles.PrimaryBold.patch(text_size=18.5),
)

# Center accent rule
rectangle(
    (96.0, 33.5),
    width=26.0,
    height=1.2,
    style=Styles.PrimaryFlat.patch(shape_r=0.6, shape_line_width=0.0),
)

# Subtle footer credit
text(
    (96.0, 24.5),
    "Surviving a 300M+ Req/Day DDoS & EDoS Attack on Google Cloud Run & Edge WAF",
    style=Styles.Dark.patch(text_size=12.5),
)
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Thank you very much for your time and attention! I would be happy to take any questions or discuss our Cloud Run, Cloud Armor, Cloudflare WAF, and Web Worker Proof-of-Work implementation in detail.
:::
