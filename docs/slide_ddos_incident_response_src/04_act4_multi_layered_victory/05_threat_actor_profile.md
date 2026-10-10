::: block (80, 40) (1760, 70)
# Threat Actor Profile: Anatomy of an AI-Assisted Adversary
:::

::: block (80, 140) (680, 810)
## Why Their Cycle Ran So Fast

- **LLM-Speed JS Cracking (<3 Hours)**
  De-obfuscated our custom frontend JS bundle and replicated HMAC signing in under 180 minutes.
- **Automated A/B Threshold Probing**
  Binary-searched our WAF rate rule and tuned 5,000+ nodes to `6–8 req/10s` (just below `10 req/10s`).
- **Adversarial Training Sandbox**
  Used our low-stakes hobby service as a live proving ground to train automated WAF-evasion agents.
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=115, height=90)

rectangle((57.5, 45.0), width=111, height=86, style=Styles.Neutral.patch(shape_r=2.5))
text((57.5, 82.5), "Forensic Evidence: Manual Script vs. AI-Assisted Botnet", style=Styles.BlackBold.patch(text_size=14.5))

cards = [
    (
        63.0,
        "1. Client JS Signature Reverse-Engineering",
        "Manual Attacker: Days of DevTools debugging",
        "Observed AI Bot: Parsed AST & cloned HMAC in < 3 hours",
        phosphor. robot,
        Styles.PrimaryFlat,
        Styles.PrimaryNeutral,
    ),
    (
        39.5,
        "2. WAF Rule & Rate-Limit Inference (Step 3 -> 4)",
        "Manual Attacker: Static flood until blocked (429)",
        "Observed AI Bot: Parallel A/B probe -> tuned 5k IPs to 6-8 req/10s",
        phosphor.gauge,
        Styles.AccentFlat,
        Styles.SecondaryNeutral,
    ),
    (
        16.0,
        "3. Strategic Motivation on a $10/mo Hobby Site",
        "Manual Attacker: Demands ransom or steals user PII",
        "Observed AI Bot: Zero data theft — live WAF evasion benchmark!",
        phosphor.cpu,
        Styles.DarkFlat,
        Styles.White,
    ),
]

for cy, title_str, manual_str, ai_str, icon_fn, badge_style, card_style in cards:
    rectangle((57.5, cy), width=101.0, height=19.5, style=card_style.patch(shape_r=2.0, shape_line_width=1.4))
    rectangle((16.5, cy), width=13.0, height=13.5, style=badge_style.patch(shape_r=1.8))
    icon_fn((16.5, cy), width=7.5, style=Styles.White)

    text((26.0, cy + 5.2), title_str, style=Styles.BlackBold.patch(text_size=13.5, halign="left"))
    text((26.0, cy - 0.5), manual_str, style=Styles.Dark.patch(text_size=12.0, halign="left"))
    text((26.0, cy - 5.6), ai_str, style=Styles.AccentBold.patch(text_size=12.5, halign="left"))
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
In Act 2, we saw the attacker's 5-step adaptation cycle. Why did that cycle execute at superhuman speed against a $10/month hobby speech synthesis service with zero monetizable user data?
- **AI-Assisted Reverse Engineering**: The 3-hour turnaround between deploying our obfuscated JS signature and the botnet replicating the exact signing algorithm strongly points to an **LLM-assisted coding workflow** (feeding minified JS bundles into an LLM to generate Python/Go request signers).
- **Automated Rate-Limit Probing**: Whenever we adjusted per-IP rate limits, the swarm automatically binary-searched the exact threshold via parallel A/B probes and dialed per-node request rates just underneath it.
- **Production as an Adversarial Sandbox**: Modern botnet operators and AI security researchers routinely use real-world public APIs as live proving grounds to benchmark residential proxy rotation and WAF evasion frameworks before attacking high-value commercial targets.
:::
