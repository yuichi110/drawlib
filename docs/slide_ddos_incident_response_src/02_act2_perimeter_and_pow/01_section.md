::: block (0, 0) (1920, 1080)
```drawlib
import utils

utils.draw_chapter_divider(
    chapter_num=2,
    title="Perimeter WAF & Evasion Loops",
    subtitle="5-Step Adaptation Cycles, 4 Geo-Hopping Waves & JS Token Cracking",
    topics=[
        "Defender vs. Attacker: Two 5-Step Adaptation Cycles",
        "GCLB + Cloud Armor WAF & 4 Proxy Geo-Hopping Waves",
        "Static Client JS Token Spoofing (Cracked in 3 Hours)",
    ],
    total_chapters=4,
)
```
:::

::: note
In Act 2, we move defense from the origin container out to the network edge and enter a multi-round cat-and-mouse battle.
First, we look at the two competing 5-step adaptation cycles: how we iteratively analyzed leaked traffic, extracted bot signatures, deployed rules, and measured effectiveness—and how the attacker simultaneously probed our endpoints in parallel, inferred our WAF thresholds from response differences, and concentrated fire on unblocked blind spots. We then trace GCLB + Cloud Armor deployment, geo-blocking failure across 4 proxy waves (China, Asia, World, Domestic Japan), and JS token reverse-engineering in 3 hours.
:::
