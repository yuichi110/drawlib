::: block (0, 0) (1920, 1080)
```drawlib
import utils

utils.draw_chapter_divider(
    chapter_num=4,
    title="Multi-Layered Edge Victory",
    subtitle="Traffic Forensics, 5 Defense Pillars, and AI Adversary Profiling",
    topics=[
        "Cloudflare Pro Migration & The Sub-Threshold Botnet Leak (25%)",
        "Traffic Forensics: Datacenter VMs vs. Hijacked Residential PCs",
        "The 5-Layer Defense Architecture, AI Botnet Profile & SRE Rules",
    ],
    total_chapters=4,
)
```
:::

::: note
In Act 4, we bring the incident to its conclusion.
After migrating to flat-rate Cloudflare Pro ($20/month), our WAF billing risk dropped to zero—but 25% of the botnet traffic still leaked through per-IP rate limits by distributing requests across 5,000+ low-rate residential IPs.
We walk through how packet and HTTP log forensics revealed two distinct botnet fleets, how we combined 5 orthogonal edge defense layers to drop 100% of malicious traffic, what the attacker's behavior reveals about AI-assisted threat actors, and the 4 SRE Golden Rules for serverless defense.
:::
