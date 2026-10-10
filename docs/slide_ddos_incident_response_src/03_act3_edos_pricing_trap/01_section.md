::: block (0, 0) (1920, 1080)
```drawlib
import utils

utils.draw_chapter_divider(
    chapter_num=3,
    title="The EDoS Pivot & WAF Pricing Trap",
    subtitle="When a 99.9% Effective WAF Threatens to Bankrupt the Defender",
    topics=[
        "Attacker Pivot: From TTS Resource Theft to 300M Req/Day Pure EDoS",
        "The Cloud Armor Trap: USD 1/Day Origin vs. USD 225/Day WAF Fees",
        "Midnight Emergency GCLB Teardown & Flat-Rate WAF Evaluation",
    ],
    total_chapters=4,
)
```
:::

::: note
In Act 3, the story takes a dramatic turn.
Blocked from stealing expensive TTS CPU cycles by our SHA-256 Proof-of-Work challenge, the attacker shifts strategy from technical disruption to **Economic Denial of Sustainability (EDoS)**—launching 300 million requests per day against lightweight endpoints just to trigger pay-per-request cloud billing.
We examine how Cloud Armor's $0.75-per-million request evaluation fee turned a 99.9% successful technical block into a $6,750/month financial crisis, forcing a midnight teardown of our Google Cloud Load Balancer.
:::
