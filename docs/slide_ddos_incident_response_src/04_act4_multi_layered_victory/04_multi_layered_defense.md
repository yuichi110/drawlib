::: block (80, 40) (1760, 70)
# The 5-Layer Defense-in-Depth Architecture
:::

::: block (80, 140) (1760, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import Pyramid
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=176, height=81)

rectangle((88.0, 40.5), width=172, height=77, style=Styles.Neutral.patch(shape_r=2.5))
text((88.0, 74.0), "5 Orthogonal Defense Layers: Filtering 300M Req/Day Down to 100% Clean Origin Traffic", style=Styles.BlackBold.patch(text_size=14.5))

# Left: Inverted Funnel Pyramid (align="top", order="base_to_vertex")
funnel = Pyramid(
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
)
funnel.add(
    "L1: Cloud ASN Block (-55%)",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=12.0),
)
funnel.add(
    "L2: UA Hygiene (-15%)",
    style=Styles.PrimaryNeutral,
)
funnel.add(
    "L3: HTTP/1.1 Block (-25%)",
    style=Styles.SecondaryNeutral,
)
funnel.add(
    "L4: Rate Limit",
    style=Styles.PrimaryNeutral,
)
funnel.add(
    "PoW",
    style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5, xy_shift=(0.0, 1.5)),
)
funnel.draw(xy=(6.5, 8.0), width=70.0, height=60.0, margin=1.8, align="top", order="base_to_vertex")

# Right: 5 Corresponding Layer Specification Cards aligned vertically with the 5 pyramid tiers
layers = [
    (62.2, "L1: Network ASN Filter (Cloudflare WAF)", "Drop commercial cloud/VPS ASNs (AWS, GCP, Azure, OVH)", phosphor.globe),
    (49.9, "L2: User-Agent Hygiene (Cloudflare WAF)", "Drop empty UAs, curl/python/go, and Chrome < v110", phosphor.magnifying_glass),
    (37.6, "L3: Wire Protocol Enforcement (ALPN Check)", "Block HTTP/1.1 relays; require HTTP/2 or HTTP/3", phosphor.shield_check),
    (25.3, "L4: Tighten Edge Rate Limit (Flat-Rate Edge)", "Composite IP + TLS limit on GET /challenge", phosphor.gauge),
    (13.0, "L5: SHA-256 Proof-of-Work (App Layer)", "Signed seed + Web Worker nonce (<50ms) for API", phosphor.cpu),
]

for cy, title_str, desc_str, icon_fn in layers:
    rectangle((126.0, cy), width=89.0, height=10.4, style=Styles.White.patch(shape_r=2.0))
    icon_fn((87.5, cy), width=5.2, style=Styles.Primary)
    text((93.0, cy + 2.1), title_str, style=Styles.BlackBold.patch(text_size=12.0, halign="left"))
    text((93.0, cy - 2.3), desc_str, style=Styles.Dark.patch(text_size=11.0, halign="left"))
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
No single rule stopped the attack alone. Victory required stacking **5 orthogonal defense layers** in an inverted funnel:
1. **Layer 1 — Network ASN Filtering (Blocks ~55%)**: Drops all commercial cloud, hosting, and VPS ASNs at the Cloudflare edge.
2. **Layer 2 — User-Agent Hygiene (Blocks ~15%)**: Drops default scripting libraries (`python-requests`, `Go-http-client`) and outdated browser versions (`Chrome < 110`).
3. **Layer 3 — HTTP/1.1 Wire Protocol Block (Blocks ~25%)**: Exploits the ALPN protocol mismatch of residential proxy relays by requiring **HTTP/2 or HTTP/3**.
4. **Layer 4 — Composite Edge Rate Limiting (Blocks ~4.9%)**: Throttles remaining high-frequency callers on `/challenge` at zero per-request cost.
5. **Layer 5 — Asymmetric SHA-256 Proof-of-Work (100% Origin Protection)**: Ensures any request that reaches `POST /synthesize` has proven real browser Web Worker computation.
:::
