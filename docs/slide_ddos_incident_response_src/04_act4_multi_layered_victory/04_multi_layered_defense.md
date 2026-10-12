::: block xy=(80, 40) width=1760 height=70
# The 5-Layer Defense-in-Depth Architecture
:::

::: block xy=(80, 140) width=1760 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, Panel, Pyramid
from drawlib.styles import Styles

setup(width=176, height=81)

panel = Panel(
    "5 Orthogonal Defense Layers: Filtering Multi-Vector Bot Swarms Down to Clean Origin Traffic",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=15.0),
    header_variant="underline",
    header_height=9.0,
    header_align="center",
)
panel.draw(xy=(2.0, 2.0), width=172.0, height=77.0)

# Left: Inverted Funnel Pyramid (direction="top", order="base_to_vertex")
funnel = Pyramid(
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.5),
)
funnel.add(
    "L1: Cloud ASN & Tor (-31%)",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.0),
)
funnel.add(
    "L2: OS/UA & Hdrs (-8%)",
    style=Styles.PrimaryNeutral,
)
funnel.add(
    "L3: HTTP/1.1 (-19%)",
    style=Styles.SecondaryNeutral,
)
funnel.add(
    "L4: Rate (-17%)",
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
)
funnel.add(
    "PoW",
    style=Styles.AccentFlat,
    text_style=Styles.BlackBold.patch(text_size=12.0, xy_shift=(0.0, 1.8)),
)
funnel.draw(xy=(5.5, 6.5), width=71.0, height=60.5, margin=1.8, direction="top", order="base_to_vertex")

# Right: 5 Corresponding Layer Specification Cards via CardList
layers = CardList(
    style=Styles.White,
    text_style=Styles.BlackBold.patch(text_size=12.2),
    description_style=Styles.Dark.patch(text_size=10.8),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=10.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=1.8,
)
layers.add(
    "L1: Network ASN & Tor Filter (~31% of Blocks)",
    "Drop Cloud/VPS ASNs + Tor & Anon proxies (T1, A1, XX)",
    badge_text="L1",
    icon=phosphor.globe,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.5),
    icon_style=Styles.White,
)
layers.add(
    "L2: Fingerprint & Header Hygiene (~8% of Blocks)",
    "Drop unknown OS/UA, bad Sec-Fetch hdrs & /cdn-cgi/trace",
    badge_text="L2",
    icon=phosphor.magnifying_glass,
)
layers.add(
    "L3: Wire Protocol Enforcement (~19% of Blocks)",
    "Block legacy HTTP/1.1 on /api/*; require HTTP/2 or HTTP/3",
    badge_text="L3",
    icon=phosphor.shield_check,
)
layers.add(
    "L4: Dual-Speed Edge Rate Limit (~17% of Blocks)",
    "Strict 5 req/30s on /api/challenge + 15 req/30s global cap",
    badge_text="L4",
    icon=phosphor.gauge,
)
layers.add(
    "L5: Page Challenge + Cookie Gate + PoW (~25%)",
    "Page Managed Challenge -> cf_clearance on /api/* + PoW",
    badge_text="L5",
    icon=phosphor.cpu,
    badge_style=Styles.AccentFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.5),
    icon_style=Styles.White,
)
layers.draw(xy=(80.0, 6.5), width=90.5, height=60.5)
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
No single rule stopped the attack alone. Victory required stacking **5 orthogonal defense layers** in an inverted funnel:
1. **Layer 1 — Network ASN & Tor Filtering (~31% of blocks)**: Drops all commercial cloud/VPS ASNs plus Tor and anonymous proxy country codes (`T1, A1, XX`) right at the edge.
2. **Layer 2 — Fingerprint & Header Hygiene (~8% of blocks)**: Drops requests with spoofed or unknown OS/Browser combinations, missing `Sec-Fetch` / custom client headers, and `/cdn-cgi/trace` reconnaissance probes.
3. **Layer 3 — HTTP/1.1 Wire Protocol Block (~19% of blocks)**: Exploits the ALPN protocol mismatch of residential proxy relays by blocking `HTTP/1.1` on `/api/*`.
4. **Layer 4 — Dual-Speed Edge Rate Limiting (~17% of blocks)**: Combines a strict burst limit (`5 req / 30s` on `/api/challenge`) with a global per-IP ceiling (`15 req / 30s` across `*`).
5. **Layer 5 — Page Managed Challenge + API Cookie Gate + SHA-256 PoW (~25% of blocks)**: Challenges users once on HTML page entry (`Managed Challenge`), blocks any direct `/api/*` call lacking the resulting `cf_clearance` cookie, and verifies SHA-256 PoW before synthesis.
:::
