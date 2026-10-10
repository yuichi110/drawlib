::: block (0, 0) (1920, 1080)
```drawlib
import utils

utils.draw_chapter_divider(
    chapter_num=1,
    title="The Incident Onset",
    subtitle="From 10 Years of VPS Peace to Serverless Cloud Run Bill Shock",
    topics=[
        "10-Year Legacy VPS vs. Public Serverless Cloud Run Exposure",
        "Cache-Busting TTS Synthesis Flood & 4-5x Weekly Bill Spike",
        "Initial Triage: Why Origin Clamping Fails vs. Edge Drop",
    ],
    total_chapters=4,
)
```
:::

::: note
Act 1 covers the initial onset of the incident.
We start by comparing the service's 10-year history on a fixed-cost VPS ($10/month) against its modernized serverless architecture on Google Cloud Run. We then examine how the attacker exploited CPU-intensive speech synthesis using mutated parameters to force 100% cache misses, and why origin-level rate limiting cannot save a serverless deployment without an upstream edge shield.
:::
