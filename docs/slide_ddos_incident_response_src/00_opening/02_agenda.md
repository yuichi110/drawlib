::: block (80, 40) (1760, 70)
# Agenda & Incident Executive Summary
:::

::: block (80, 150) (1020, 810)
```drawlib
from drawlib.canvas import setup
import utils

setup(width=104, height=84)
utils.draw_curved_agenda(
    [
        ("Act 1: The Incident Onset", "10 Years of VPS Peace to Serverless Cloud Run Bill Shock"),
        ("Act 2: Perimeter WAF & Evasion Loops", "Adaptation Cycles, GCLB WAF, 4 Geo-Waves & JS Cracking"),
        ("Act 3: PoW, EDoS Pivot & WAF Pricing Trap", "SHA-256 PoW, 300M/Day Flood & $225/Day Cloud Armor Crisis"),
        ("Act 4: Multi-Layered Edge Victory", "Flat-Rate Cloudflare Pro, 5 Defense Pillars & AI Forensics"),
    ],
    width=104,
    height=84,
)
```
:::

::: block (1140, 150) (700, 810)
```drawlib
from drawlib.canvas import setup
import utils

setup(width=72, height=84)
utils.draw_kpi_cards(
    [
        ("300M+", "Peak Attack Volume / Day", "Volumetric HTTP flood across 5,000+ nodes"),
        ("$6,750", "Projected Monthly WAF Bill", "$225/day Cloud Armor rule evaluation trap"),
        ("<50ms", "Browser SHA-256 PoW", "Asymmetric Web Worker hash puzzle"),
        ("$20/mo", "Final Flat-Rate Defense", "Cloudflare Pro + 5 orthogonal edge layers"),
    ],
    width=72,
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
This presentation is structured into four chronological acts that mirror the real-world incident response timeline:

1. **Act 1 — The Incident Onset**: We examine why 10 years of peaceful operation on a fixed-cost VPS ended abruptly after migrating to Google Cloud Run, where cache-busting TTS requests drove CPU utilization to 100% and multiplied weekly compute bills by 4-5x.
2. **Act 2 — Perimeter WAF & Evasion Loops**: We contrast the 5-step adaptation cycles of the defender and the attacker, trace the deployment of Google Cloud Load Balancing and Cloud Armor, and see how the botnet defeated country-level geo-blocking across 4 rapid proxy waves and cracked our static JS signatures in 3 hours.
3. **Act 3 — PoW, EDoS Pivot & WAF Pricing Trap**: We deploy an asymmetric SHA-256 Proof-of-Work challenge that stops unauthorized TTS synthesis—triggering a shift in the attacker's goal toward pure origin penetration (300M req/day) and a $225/day ($6,750/month) Cloud Armor evaluation fee crisis.
4. **Act 4 — Multi-Layered Edge Victory**: We detail the midnight emergency teardown of GCLB, migration to flat-rate Cloudflare Pro ($20/month), traffic decomposition of datacenter vs. residential bots, the 5-layer defense-in-depth architecture, and lessons for defending against AI-assisted adversaries.
:::
