::: block xy=(80, 40) width=1760 height=70
# Key Takeaways: 4 Golden Rules for Serverless DDoS Defense
:::

::: block xy=(80, 140) width=1060 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.smartarts import KpiCards, Panel
from drawlib.styles import Styles

setup(width=106, height=81)

panel = Panel(
    "4 SRE Golden Rules for Serverless & Edge Security",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=15.5),
    header_variant="underline",
    header_height=9.5,
    header_align="center",
)
panel.draw(xy=(2.0, 2.0), width=102.0, height=77.0)
c_xy, c_w, c_h = panel.get_content_box(xy=(2.0, 2.0), width=102.0, height=77.0, padding=(3.5, 3.0))

rules = KpiCards(
    style=Styles.White,
    metric_style=Styles.PrimaryBold.patch(text_size=18.5),
    text_style=Styles.BlackBold.patch(text_size=14.8),
    description_style=Styles.Dark.patch(text_size=12.5),
    accent_style=Styles.PrimaryFlat,
    icon_style=Styles.PrimaryBold,
    accent_position="top_bar",
    metric_layout="top_stack",
    spacing=3.5,
)
rules.add(
    "Rule 1",
    "No Direct Serverless",
    "Lock run.app to LB only;\nplace flat-rate Edge in front",
    icon=phosphor.lock_key,
    style=Styles.PrimaryNeutral,
)
rules.add(
    "Rule 2",
    "Audit WAF EDoS Fees",
    "$0.75/M WAF fees bankrupt\nyou at 300M req/day flood",
    icon=phosphor.currency_dollar,
    style=Styles.SecondaryNeutral,
    metric_style=Styles.AccentBold.patch(text_size=18.5),
    accent_style=Styles.AccentFlat,
    icon_style=Styles.AccentBold,
)
rules.add(
    "Rule 3",
    "Orthogonal Signals",
    "Combine Cloud ASN, UA/OS,\nHTTP/2+ ALPN & Rate Caps",
    icon=phosphor.funnel,
    style=Styles.White,
)
rules.add(
    "Rule 4",
    "Asymmetric PoW",
    "JS secrets crack in hours;\nuse SHA-256 Web Worker PoW",
    icon=phosphor.cpu,
    style=Styles.PrimaryNeutral,
)
rules.draw(c_xy, width=c_w, height=c_h, columns=2)
```
:::

::: block xy=(1180, 140) width=660 height=810
```drawlib
from drawlib.canvas import setup
import utils

setup(width=68, height=84)
utils.draw_kpi_cards(
    [
        ("100%", "Service Availability", "Zero downtime for JP users"),
        ("0%", "Unauthorized TTS CPU", "SHA-256 PoW stopped abuse"),
        ("99.9%", "Edge Drop Efficiency", "5-layer rules block 300M/d"),
        ("$20/mo", "Predictable Flat Cost", "Down from $6,750/mo WAF bill"),
    ],
    width=68,
    height=84,
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
Let's close with the **4 Golden Rules** every cloud architect and solo developer should take away from this incident:
1. **Never Expose Auto-Scaling Serverless Origins Directly**: Publicly exposing a pay-per-use endpoint (`*.run.app`, AWS Lambda Function URLs) without an edge shield gives attackers a blank check drawn on your credit card.
2. **Audit Your WAF's EDoS Pricing Model Before an Attack**: Hyperscaler WAFs that charge per evaluated request ($0.60–$0.75 per million) turn volumetric floods into financial disasters even when 99.9% of requests are blocked. Use flat-rate unmetered edge mitigation (such as Cloudflare Pro at $20/mo) when cost predictability matters.
3. **Stack Orthogonal L3–L7 Signals**: Geographic IP blocks and simple rate limits fail against distributed residential proxies. Combine **Hosting ASN blocks**, **User-Agent hygiene**, and **HTTP/2+ ALPN wire protocol checks**.
4. **Replace Client-Side Obscurity with Cryptographic Proof-of-Work**: In the era of LLM-assisted reverse engineering, obfuscated JS logic survives Less than 3 hours. Use **asymmetric SHA-256 Proof-of-Work** so computational cost scales against the attacker.
:::
