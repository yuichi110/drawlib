::: block xy=(80, 40) width=1760 height=70
# Threat Actor Profile: Anatomy of an AI-Assisted Adversary
:::

::: block xy=(80, 140) width=680 height=810
## Why Their Cycle Ran So Fast

- **LLM-Speed JS Cracking (<3 Hours)**
  De-obfuscated our custom frontend JS bundle and replicated HMAC signing in under 180 minutes.
- **Automated A/B Threshold Probing**
  Binary-searched our WAF rate rule and tuned 5,000+ nodes to `6–8 req/10s` (just below `10 req/10s`).
- **Adversarial Training Sandbox**
  Used our low-stakes hobby service as a live proving ground to train automated WAF-evasion agents.
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles

setup(width=115, height=90)

panel = Panel(
    "Forensic Evidence: Manual Script vs. AI-Assisted Botnet",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=15.5),
    header_variant="underline",
    header_height=9.5,
    header_align="center",
)
panel.draw(xy=(2.0, 2.0), width=111.0, height=86.0)
c_xy, c_w, c_h = panel.get_content_box(xy=(2.0, 2.0), width=111.0, height=86.0, padding=(4.0, 3.5))

cl = CardList(
    style=Styles.White,
    text_style=Styles.BlackBold.patch(text_size=14.0),
    description_style=Styles.Dark.patch(text_size=12.5),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=11.5),
    icon_style=Styles.White,
    direction="vertical",
    spacing=3.5,
)
cl.add(
    "1. Client JS Signature Reverse-Engineering",
    "Manual: Days of DevTools debugging\nObserved AI Bot: Parsed AST & cloned HMAC in < 3h",
    badge_text="01",
    icon=phosphor.robot,
    style=Styles.PrimaryNeutral,
    badge_style=Styles.PrimaryFlat,
)
cl.add(
    "2. WAF Rule & Rate-Limit Inference (Step 3 -> 4)",
    "Manual: Static flood until blocked (429)\nObserved AI Bot: A/B probe -> tuned 5k IPs to 6-8 req/10s",
    badge_text="02",
    icon=phosphor.gauge,
    style=Styles.SecondaryNeutral,
    badge_style=Styles.AccentFlat,
)
cl.add(
    "3. Strategic Motivation on a $10/mo Hobby Site",
    "Manual: Demands ransom or steals user PII\nObserved AI Bot: Zero data theft — live WAF evasion benchmark",
    badge_text="03",
    icon=phosphor.cpu,
    style=Styles.White,
    badge_style=Styles.DarkFlat,
)
cl.draw(c_xy, width=c_w, height=c_h)
```
:::

::: block xy=(1720, 995) width=140 height=30
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
