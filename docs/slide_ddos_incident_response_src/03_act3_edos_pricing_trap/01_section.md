::: block (0, 0) (1920, 1080)
```drawlib
import utils

utils.draw_chapter_divider(
    chapter_num=3,
    title="SHA-256 PoW & The EDoS Pricing Trap",
    subtitle="How Stopping TTS Abuse Triggered a 300M/Day Flood & $6,750/mo WAF Crisis",
    topics=[
        "Asymmetric SHA-256 Proof-of-Work & Attacker Goal Shift",
        "Cloud Armor Trap: USD 1/Day Origin vs. USD 225/Day WAF",
        "Midnight Emergency GCLB Teardown & Flat-Rate WAF Choice",
    ],
    total_chapters=4,
)
```
:::

::: note
In Act 3, we deploy an asymmetric SHA-256 Proof-of-Work challenge that completely shuts down unauthorized TTS synthesis calls.
However, that technical victory triggers a dramatic shift in the attacker's objective: giving up on the `/synthesize` API, the botnet pivots to flooding any lightweight endpoint just to sneak massive request volume through to our origin (300 million requests per day).
We then examine how Cloud Armor's $0.75-per-million request evaluation fee turned a 99.9% successful edge block into a $6,750/month Economic Denial of Sustainability (EDoS) crisis, forcing a midnight teardown of our Google Cloud Load Balancer.
:::
