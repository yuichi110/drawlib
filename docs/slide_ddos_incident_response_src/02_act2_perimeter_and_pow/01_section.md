::: block (0, 0) (1920, 1080)
```drawlib
import utils

utils.draw_chapter_divider(
    chapter_num=2,
    title="Perimeter WAF & Proof-of-Work",
    subtitle="Cat-and-Mouse Geo-Blocking, JS Header Spoofing, and Asymmetric PoW",
    topics=[
        "Perimeter Hardening with GCLB Anycast Edge & Cloud Armor WAF",
        "Why Geo-Blocking Failed: 4 Rapid Proxy Hopping Waves",
        "Static JS Token Spoofing vs. Asymmetric SHA-256 Proof-of-Work",
    ],
    total_chapters=4,
)
```
:::

::: note
In Act 2, we move defense from the origin container out to the network edge.
We examine the architectural overhaul using Google Cloud Load Balancing (GCLB) and Cloud Armor WAF, see why geographic IP blocking failed within hours as the attacker rotated through global and domestic residential proxy pools, analyze how the adversary reverse-engineered our client-side JavaScript signature in 3 hours, and finally regain control of the synthesis API using an asymmetric SHA-256 Proof-of-Work puzzle.
:::
