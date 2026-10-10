::: block (80, 40) (1760, 70)
# The Cloud Armor Trap: 99.9% Blocked, $6,750/mo Bill
:::

::: block (80, 140) (680, 810)
```drawlib
from drawlib.canvas import setup
import utils

setup(width=70, height=84)
utils.draw_kpi_cards(
    [
        ("99.9%", "Cloud Armor Block Rate", "Origin CPU stayed calm & 100% healthy"),
        ("$1/day", "Cloud Run Origin Cost", "Container compute completely protected"),
        ("$225/d", "Cloud Armor + GCLB Fee", "$0.75 per 1M evaluated requests at edge"),
        ("$6,750", "Projected Monthly Bill", "675x over our $10/mo hobby budget!"),
    ],
    width=70,
    height=84,
)
```
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart
from drawlib.shapes import rectangle
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=115, height=90)

# Top Card: Daily Cost Comparison BarChart
rectangle((57.5, 62.0), width=111, height=50, style=Styles.Neutral.patch(shape_r=2.5))

chart = BarChart(
    axis_line_style=Styles.Primary,
    categories=["Normal Baseline\n(Pre-Attack)", "Protected Origin\n(Cloud Run CPU)", "Edge WAF Evaluation\n(Cloud Armor + GCLB)"],
    width=96.0,
    height=38.0,
    title="Daily Cost Paradox During 300M Req/Day Flood ($ USD / Day)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
    bar_width_ratio=0.5,
    bar_r=1.0,
    axis_text_style=Styles.DarkBold.patch(text_size=9.5),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.BlackBold.patch(text_size=10.0),
    value_format="${:g} / day",
)
chart.add_series("Daily Cost ($ USD)", [0.35, 1.00, 225.00], style=Styles.AccentFlat)
chart.configure_y_axis(min_value=0.0, max_value=260.0, tick_step=50.0, format="${:.0f}")
chart.draw(xy=(9.0, 40.0))

# Bottom Card: Billing Breakdown Table
rectangle((57.5, 18.0), width=111, height=30, style=Styles.Neutral.patch(shape_r=2.5))
text((57.5, 29.5), "Why Blocking Traffic at the Edge Still Cost $225/Day", style=Styles.BlackBold.patch(text_size=11.0))

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=9.5),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=9.5),
    border_style=Styles.MutedThin,
)
table.set_style_cell(
    background_color=(252, 232, 230),
    text_style=Styles.AccentBold.patch(text_size=9.5),
    rows=[1, 2],
    columns=[3],
)
data = [
    ["Billing Component", "Unit Pricing Model", "300M Req/Day Volume", "Daily Cost"],
    ["Cloud Armor Standard", "$0.75 per 1M requests evaluated", "300M blocked at edge", "$225.00 / day"],
    ["GCLB Forwarding & L7", "Hourly rule + L7 processing", "300M TLS terminations", "+$18.00 / day"],
]
table.draw_flexible(xy=(6.5, 26.0), column_widths=[30.0, 31.0, 24.0, 17.0], row_heights=[6.5, 6.5, 6.5], data=data)
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Here lies the most painful lesson of the entire incident—**the Cloud WAF Pricing Trap**:
- **Technical Success vs. Financial Disaster**: Technically, Google Cloud Armor worked exactly as advertised. Its rate-limiting rules dropped **99.9%** of the 300M daily attack requests at Google's edge POPs. Our Cloud Run origin stayed completely healthy, and origin compute cost only **$1.00/day**.
- **The $0.75 / Million Evaluation Fee**: However, Cloud Armor Standard charges **$0.75 per 1 million requests evaluated** against a security policy—*even when the request is immediately blocked with a 403 at the edge!*
- **The Math of EDoS**:
  $$\text{300M requests/day} \times \frac{\$0.75}{\text{1M requests}} = \$225\text{/day} \approx \$6,750\text{/month}$$
  Meanwhile, upgrading to Cloud Armor Managed Protection Plus costs **$3,000/month** base fee. For an enterprise, $3,000/month is pocket change; for a $10/month solo service, **the shield itself became the weapon of bankruptcy**.
:::
