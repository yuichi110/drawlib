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
        ("Act 2: Perimeter WAF & Proof-of-Work", "GCLB + Cloud Armor, Geo-Hopping & SHA-256 PoW"),
        ("Act 3: The EDoS Pivot & WAF Pricing Trap", "300M Req/Day Flood & $225/Day Cloud Armor Fee Crisis"),
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
2. **Act 2 — Perimeter WAF & Proof-of-Work**: We trace the deployment of Google Cloud Load Balancing and Cloud Armor, the failure of country-level geo-blocking across 4 rapid proxy waves, the defeat of static JS signatures within 3 hours, and the success of an asymmetric SHA-256 Proof-of-Work challenge.
3. **Act 3 — The EDoS Pivot & WAF Pricing Trap**: Blocked from stealing CPU via PoW, the attacker launched a 300M req/day volumetric flood. While Cloud Armor blocked 99.9% of requests, per-request WAF evaluation fees ($0.75/M) created a $225/day ($6,750/month) Economic Denial of Sustainability (EDoS) crisis.
4. **Act 4 — Multi-Layered Edge Victory**: We detail the midnight emergency teardown of GCLB, migration to flat-rate Cloudflare Pro ($20/month), traffic decomposition of datacenter vs. residential bots, the 5-layer defense-in-depth architecture, and lessons for defending against AI-assisted adversaries.
:::
