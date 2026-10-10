::: block (80, 40) (1760, 70)
# Key Takeaways: 4 Golden Rules for Serverless DDoS Defense
:::

::: block (80, 140) (1060, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.smartarts import GridLayout
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=106, height=81)

rectangle((53.0, 40.5), width=102, height=77, style=Styles.Neutral.patch(shape_r=2.5))
text((53.0, 73.0), "4 SRE Golden Rules for Serverless & Edge Security", style=Styles.BlackBold.patch(text_size=14.5))

grid = GridLayout(
    num_column=2,
    num_row=2,
    style=Styles.White.patch(shape_r=2.0),
    text_style=Styles.DarkBold.patch(text_size=12.5),
)

# Top-Left (col=0, row=1)
grid.add(
    position=(0, 1),
    width=1,
    height=1,
    text="Rule 1: No Direct Serverless\n\nLock run.app to internal/LB only.\nPlace a flat-rate Anycast Edge\nin front of auto-scaling compute.",
    style=Styles.PrimaryFlat.patch(shape_r=2.0),
    text_style=Styles.WhiteBold.patch(text_size=12.5),
)

# Top-Right (col=1, row=1)
grid.add(
    position=(1, 1),
    width=1,
    height=1,
    text="Rule 2: Audit WAF EDoS Fees\n\nPer-request WAFs ($0.75/M) can\nbankrupt you during a 300M/day\nflood even at 99.9% block rate.",
    style=Styles.SecondaryNeutral.patch(shape_r=2.0),
    text_style=Styles.DarkBold.patch(text_size=12.5),
)

# Bottom-Left (col=0, row=0)
grid.add(
    position=(0, 0),
    width=1,
    height=1,
    text="Rule 3: Orthogonal Signals\n\nCombine Hosting ASN blocks,\nUA hygiene, HTTP/2+ ALPN checks,\nand composite edge rate limits.",
    style=Styles.PrimaryNeutral.patch(shape_r=2.0),
    text_style=Styles.DarkBold.patch(text_size=12.5),
)

# Bottom-Right (col=1, row=0)
grid.add(
    position=(1, 0),
    width=1,
    height=1,
    text="Rule 4: Asymmetric PoW\n\nClient JS secrets get cracked\nin hours. Use SHA-256 Web Worker\nPoW to invert CPU cost.",
    style=Styles.White.patch(shape_r=2.0),
    text_style=Styles.DarkBold.patch(text_size=12.5),
)

grid.draw(xy=(5.5, 5.5), width=95.0, height=62.5, margin=2.5)
```
:::

::: block (1180, 140) (660, 810)
```drawlib
from drawlib.canvas import setup
import utils

setup(width=68, height=84)
utils.draw_kpi_cards(
    [
        ("100%", "Service Availability", "Zero downtime for organic Japanese users"),
        ("0%", "Unauthorized TTS CPU", "SHA-256 PoW eliminated synthesis abuse"),
        ("99.9%", "Edge Drop Efficiency", "5-layer Cloudflare rules block 300M/day"),
        ("$20/mo", "Predictable Flat Cost", "Down from $6,750/mo projected WAF bill"),
    ],
    width=68,
    height=84,
)
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Let's close with the **4 Golden Rules** every cloud architect and solo developer should take away from this incident:
1. **Never Expose Auto-Scaling Serverless Origins Directly**: Publicly exposing a pay-per-use endpoint (`*.run.app`, AWS Lambda Function URLs) without an edge shield gives attackers a blank check drawn on your credit card.
2. **Audit Your WAF's EDoS Pricing Model Before an Attack**: Hyperscaler WAFs that charge per evaluated request ($0.60–$0.75 per million) turn volumetric floods into financial disasters even when 99.9% of requests are blocked. Use flat-rate unmetered edge mitigation (such as Cloudflare Pro at $20/mo) when cost predictability matters.
3. **Stack Orthogonal L3–L7 Signals**: Geographic IP blocks and simple rate limits fail against distributed residential proxies. Combine **Hosting ASN blocks**, **User-Agent hygiene**, and **HTTP/2+ ALPN wire protocol checks**.
4. **Replace Client-Side Obscurity with Cryptographic Proof-of-Work**: In the era of LLM-assisted reverse engineering, obfuscated JS logic survives Less than 3 hours. Use **asymmetric SHA-256 Proof-of-Work** so computational cost scales against the attacker.
:::
