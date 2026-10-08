::: block (80, 50) (1760, 120)
# Design Token Discipline & The 50%+ Neutral Rule (`drawlib.styles`)
How systematic PascalCase tokens and neutral grounding prevent "rainbow chaos" in technical diagrams.
:::

::: block (80, 190) (780, 770) compact
### 1. Systematic `Styles.<Color><Variant>` Matrix

```python
from drawlib.styles import Colors, Styles, get_intermediate_colors

# Always import PascalCase Styles & Colors!
hero = Styles.PrimaryFlat              # Saturated focal point
card = Styles.PrimaryNeutral           # Soft tinted-neutral card
base = Styles.Neutral                  # Calm slate/white baseline
zone = Styles.MutedDashed              # Container boundary

# Immutable overrides via .patch()
custom = Styles.PrimaryBold.patch(line_width=3.0, text_size=12)

# Smooth color interpolation for gradients & heatmaps
ramp = get_intermediate_colors(Colors.Primary, Colors.Secondary,
                               num=3, include_ends=True)
```

### 2. The 50%+ Neutral Baseline Rule
- **Avoid Rainbow Chaos**: Never fill every node with competing saturated colors (`PrimaryFlat`, `WarningFlat`, `DangerFlat`, `PurpleFlat`).
- **Ground 50%+ in Calm Neutrals**: Use `Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.BlueNeutral` for standard components, reserving `Styles.PrimaryFlat` / `Styles.AccentFlat` (`text_style=Styles.WhiteBold`) strictly for **1–2 focal hero nodes**.
:::

::: block (900, 180) (940, 780)
```drawlib file:style_tokens.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles, get_intermediate_colors
from drawlib.text import text

clear()
setup(width=100, height=82)

# Section 1: Anti-Pattern vs Best Practice (50%+ Neutral Rule)
rectangle((50, 66), width=90, height=26, r=2.5, style=Styles.LightFlat)
text((9, 75), "1. Anti-Pattern (Rainbow Chaos) vs. 50%+ Neutral Discipline", style=Styles.DarkBold.patch(text_size=9.0, halign="left"))

# Left: Rainbow Chaos (Anti-Pattern)
text((27, 69.5), "✗ Anti-Pattern: All Saturated Fills", style=Styles.DangerBold.patch(text_size=8.0))
rectangle((15, 61), width=11, height=9, r=1.5, style=Styles.DangerFlat, text="UI", text_style=Styles.WhiteBold.patch(text_size=7.5))
rectangle((27, 61), width=11, height=9, r=1.5, style=Styles.WarningFlat, text="API", text_style=Styles.WhiteBold.patch(text_size=7.5))
rectangle((39, 61), width=11, height=9, r=1.5, style=Styles.PurpleFlat, text="DB", text_style=Styles.WhiteBold.patch(text_size=7.5))

# Right: 50%+ Neutral Grounded (Best Practice)
text((73, 69.5), "✓ Best Practice: 1 Hero + Calm Neutrals", style=Styles.SecondaryBold.patch(text_size=8.0))
rectangle((61, 61), width=11, height=9, r=1.5, style=Styles.Neutral, text="UI", text_style=Styles.DarkBold.patch(text_size=7.5))
rectangle((73, 61), width=11, height=9, r=1.5, style=Styles.PrimaryFlat, text="API", text_style=Styles.WhiteBold.patch(text_size=7.5))
rectangle((85, 61), width=11, height=9, r=1.5, style=Styles.SecondaryNeutral, text="DB", text_style=Styles.DarkBold.patch(text_size=7.5))

# Section 2: Structural Variants Matrix
rectangle((50, 38), width=90, height=22, r=2.5, style=Styles.LightFlat)
text((9, 45.5), "2. Orthogonal Style Variants (Styles.<Role><Variant>)", style=Styles.DarkBold.patch(text_size=9.0, halign="left"))

variants = [
    (18, Styles.PrimaryFlat, Styles.WhiteBold.patch(text_size=7.5), "PrimaryFlat"),
    (39, Styles.PrimaryNeutral, Styles.DarkBold.patch(text_size=7.5), "PrimaryNeutral"),
    (61, Styles.SecondaryNeutral, Styles.DarkBold.patch(text_size=7.5), "SecondaryNeutral"),
    (82, Styles.MutedDashed, Styles.DarkBold.patch(text_size=7.5), "MutedDashed"),
]
for cx, st, tst, lbl in variants:
    rectangle((cx, 36), width=18, height=10, r=2.0, style=st, text=lbl, text_style=tst)

# Section 3: Color Interpolation (get_intermediate_colors)
rectangle((50, 13), width=90, height=20, r=2.5, style=Styles.LightFlat)
text((9, 19.5), "3. Color Interpolation: get_intermediate_colors(Primary, Secondary)", style=Styles.DarkBold.patch(text_size=9.0, halign="left"))

ramp = get_intermediate_colors(Colors.Primary, Colors.Secondary, num=4, include_ends=True)
for i, col in enumerate(ramp):
    cx = 16 + i * 13.6
    st = Styles.WhiteFlat.patch(shape_fill_color=col)
    rectangle((cx, 10.5), width=11.5, height=8.5, r=1.5, style=st, text=f"Step {i}", text_style=Styles.WhiteBold.patch(text_size=7.5))

save()
```
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- Design token discipline is what separates amateur diagrams from executive-ready architecture blueprints.
- Always import `Colors` and `Styles` in PascalCase from `drawlib.styles`.
- Follow the 50%+ Neutral Baseline rule: ground at least half of your shapes in calm neutrals (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`), and reserve saturated fills (`Styles.PrimaryFlat`) for 1 or 2 hero focal nodes.
:::
