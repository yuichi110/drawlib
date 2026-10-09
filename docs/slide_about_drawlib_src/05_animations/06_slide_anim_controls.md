::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Interactive Slide Animation Controls (`click`, `once`, `pause`)
:::

::: block (80, 140) (760, 840) font:20px
## Presenter-Driven Keyframe Stepping

In slide decks, you control `<canvas>` animation playback directly from the ```` ```drawlib ```` code fence header—turning multi-frame APNGs into interactive slide builds:

````markdown
```drawlib file:step_click_demo.png anim:click loop:once pause:1,2
# 4-frame architectural walkthrough (Frames 0, 1, 2, 3)
```
````

| Fence Option | Shorthand / Alias | Behavior in `slide.js` |
| :--- | :--- | :--- |
| `anim-trigger:auto` | `anim:auto` | Starts playing automatically when entering the slide. |
| `anim-trigger:click` | `anim:click` | Holds on **Frame 0 (`READY`)** until clicked or **`A`** is pressed. |
| `anim-loop:infinite` | `loop:infinite` | Loops continuously back to Frame 0 after the last frame. |
| `anim-loop:once` | `loop:once` | Stops on the final frame (**`ENDED`** badge; click to reset). |
| `anim-pause:1,2` | `pause:1,2` | Pauses at 0-based frame indices (`PAUSED` badge) until the next trigger. |

### Synchronized Dual-Window Control
- **Keyboard & Click**: Click the diagram, press **`A`**, or click **`▶ Play / Resume Animation`** in Presenter View (`P`) to step through pause points in real time across both screens.
:::

::: block (880, 140) (960, 840)
```drawlib file:step_click_demo.png anim:click anim-loop:once anim-pause:1,2
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=96, height=84)
anim = Animation(fps=1.2, loop=0)

steps = [
    (
        "Step 1 / 4 — Frame 0 (READY: Initial State on Slide Entry)",
        "1. Client TLS Handshake",
        "Edge Router terminates TLS 1.3 & validates client certificate",
        "READY (Hold on Frame 0)",
    ),
    (
        "Step 2 / 4 — Frame 1 (PAUSED at pause:1,2 — Click or Press 'A')",
        "2. Policy & Auth Check",
        "OPA Engine verifies RBAC claims & injects identity headers",
        "PAUSED (Frame 1)",
    ),
    (
        "Step 3 / 4 — Frame 2 (PAUSED at pause:1,2 — Click or Press 'A')",
        "3. Primary Execution",
        "Payment Service executes idempotent ledger transaction",
        "PAUSED (Frame 2)",
    ),
    (
        "Step 4 / 4 — Frame 3 (ENDED via loop:once — Click to Reset)",
        "4. Audit & Response",
        "Immutable event logged to Kafka & 200 OK returned to client",
        "ENDED (Frame 3)",
    ),
]

for active_step in range(4):
    with anim.frame(duration=0.8):
        rectangle((48, 42), width=92, height=78, style=Styles.Neutral.patch(shape_r=2.5))
        text(
            (48, 74.5),
            "Interactive Click-Through Demo  (Click Diagram or Press 'A')",
            style=Styles.DarkBold.patch(text_size=11.5),
        )

        # State machine indicator bar
        state_labels = ["READY (F0)", "PAUSED (F1)", "PAUSED (F2)", "ENDED (F3)"]
        for idx, s_lbl in enumerate(state_labels):
            sx = 16.5 + idx * 21.0
            is_cur = idx == active_step
            st = Styles.AccentFlat if is_cur else (Styles.PrimaryNeutral if idx < active_step else Styles.White)
            ts = Styles.WhiteBold.patch(text_size=8.0) if is_cur else Styles.DarkBold.patch(text_size=8.0)
            rectangle((sx, 65.0), width=18.0, height=6.5, style=st.patch(shape_r=1.2), text=s_lbl, text_style=ts)
            if idx < 3:
                line((sx + 9.0, 65.0), (sx + 12.0, 65.0), arrow_head="->", style=Styles.DarkBold)

        # 4 vertical architecture step cards
        for i in range(4):
            cy = 51.0 - i * 11.5
            if i > active_step:
                # Reserved ghost slot
                rectangle(
                    (48, cy),
                    width=82,
                    height=8.8,
                    style=Styles.MutedDashed.patch(shape_r=1.5),
                    text=f"Step {i + 1} — Waiting for presenter trigger...",
                    text_style=Styles.Muted.patch(text_size=8.8),
                )
            else:
                is_active = i == active_step
                c_style = Styles.PrimaryFlat if is_active else Styles.White
                t_title = Styles.WhiteBold.patch(text_size=9.5, halign="left") if is_active else Styles.DarkBold.patch(text_size=9.5, halign="left")
                t_desc = Styles.White.patch(text_size=8.2, halign="left") if is_active else Styles.Muted.patch(text_size=8.2, halign="left")
                badge_st = Styles.AccentFlat if is_active else Styles.SecondaryFlat

                rectangle((48, cy), width=82, height=8.8, style=c_style.patch(shape_r=1.5))
                circle((12.5, cy), radius=2.6, style=badge_st, text=str(i + 1), text_style=Styles.WhiteBold.patch(text_size=8.5))
                text((17.5, cy + 1.6), steps[i][1], style=t_title)
                text((17.5, cy - 1.8), steps[i][2], style=t_desc)

        # Bottom banner
        rectangle(
            (48, 8.5),
            width=82,
            height=6.0,
            style=Styles.PrimaryNeutral.patch(shape_r=1.2),
            text=steps[active_step][0],
            text_style=Styles.PrimaryBold.patch(text_size=8.8),
        )

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 5: Multi-Frame Animations — Interactive Slide Playback Controls*
:::

::: note
- Try clicking the diagram on the right or pressing `A` on your keyboard!
- Because the fence specifies `anim:click anim-loop:once anim-pause:1,2`, the slide opens in `READY` state on Frame 0 (Step 1).
- Clicking once advances to Frame 1 and pauses (`PAUSED`). Clicking again advances to Frame 2 (`PAUSED`). Clicking a third time advances to Frame 3 and stops in `ENDED` state. One more click resets back to Frame 0!
:::
