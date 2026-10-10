::: block (80, 40) (1760, 70)
# Midnight Emergency: Tearing Down GCLB & Choosing a Flat-Rate WAF
:::

::: block (80, 140) (1760, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess, Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=176, height=81)

# Top Section: Midnight Emergency Cutover Pipeline
rectangle((88.0, 63.0), width=172, height=32, style=Styles.Neutral.patch(shape_r=2.5))
text((88.0, 74.0), "Midnight Emergency Cutover Sequence (Stopping the $225/Day Bleeding)", style=Styles.BlackBold.patch(text_size=12.0))

steps = ChevronProcess(
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=9.5),
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
)
steps.add("1. Delete GCLB & Armor", description="Stop $225/day meter immediately", style=Styles.AccentFlat, text_style=Styles.WhiteBold.patch(text_size=10.5), description_style=Styles.White.patch(text_size=9.5))
steps.add("2. Temporary Origin Clamp", description="max-instances=1 safety cap", style=Styles.SecondaryNeutral)
steps.add("3. Evaluate 4 Architectures", description="Reject per-request WAF pricing")
steps.add("4. Cutover to Cloudflare Pro", description="Flat $20/mo unlimited DDoS drop", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=10.5), description_style=Styles.White.patch(text_size=9.5))
steps.draw(xy=(8.0, 51.0), width=160.0, height=17.0)

# Bottom Section: Architectural Comparison Matrix
rectangle((88.0, 23.5), width=172, height=41, style=Styles.Neutral.patch(shape_r=2.5))
text((88.0, 40.0), "Architectural Comparison: Pay-Per-Request Cloud WAFs vs. Flat-Rate Edge Proxy", style=Styles.BlackBold.patch(text_size=12.0))

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=9.5),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.0),
    border_style=Styles.MutedThin,
)
table.set_style_cell_evenodd(
    even_color=(248, 250, 252),
    even_text_style=Styles.Dark.patch(text_size=9.5),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=9.5),
)
table.set_style_cell(
    background_color=(230, 244, 234),
    text_style=Styles.PrimaryBold.patch(text_size=9.5),
    rows=[4],
    columns=[0, 1, 2, 3, 4],
)

matrix = [
    ["Defense Option", "Base Fee", "Per-Request WAF Fee", "Cost @ 300M Req/Day", "Verdict"],
    ["Google Cloud Armor (Standard)", "$5 / mo + GCLB", "$0.75 / 1M evaluated", "~$6,750 / mo", "REJECT: EDoS Bankruptcy"],
    ["AWS WAF / Azure WAF", "$5–10 / mo + ALB", "$0.60 / 1M evaluated", "~$5,400 / mo", "REJECT: Per-Req Trap"],
    ["Self-Hosted Nginx VPS", "$10 / mo fixed", "$0 (Fixed Bandwidth)", "$10 / mo", "REJECT: 1 NIC Saturates"],
    ["Cloudflare Pro (Unmetered L7)", "$20 / mo FLAT", "$0.00 (Unmetered Drop)", "$20 / mo FLAT", "SELECTED: Zero EDoS Risk"],
]
table.draw_flexible(xy=(6.0, 36.5), column_widths=[42.0, 26.0, 34.0, 30.0, 32.0], row_heights=[6.2, 6.2, 6.2, 6.2, 6.2], data=matrix)
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Realizing that Cloud Armor was accruing **$225 every 24 hours**, we executed an emergency midnight cutover:
1. **Immediate Teardown of GCLB & Cloud Armor**: You cannot simply "pause" an External Application Load Balancer while attack traffic is hitting its Anycast IP. We deleted the GCLB forwarding rules and Cloud Armor security policies outright to stop the per-request billing meter, temporarily clamping Cloud Run back to `max-instances = 1`.
2. **Evaluating 4 Architectural Candidates**:
   - **Google Cloud Armor**: $0.75/M requests evaluated ($\sim\$6,750$/mo at 300M req/day).
   - **AWS WAF / Azure WAF**: Identical hyperscaler billing model ($\sim\$0.60$/M requests evaluated $\rightarrow \$5,400$/mo).
   - **Self-Hosted Reverse Proxy VPS**: Caps cost at $10/mo, but a single VPS network interface immediately saturates under 300M req/day, causing 100% downtime.
   - **Cloudflare Pro ($20/month Flat Rate)**: Absorbs and drops L7 DDoS floods across its global Anycast edge with **zero per-request evaluation overage fees**.
:::
