::: block (0, 0) (1920, 1080)
```drawlib file:divider.svg
import utils

utils.draw_chapter_divider(
    chapter_num=5,
    title="Multi-Frame Animations",
    subtitle="Programmatic Keyframes, Progressive Reveal & Interactive Slide Controls",
    topics=[
        "Declarative Frame Context Manager (Animation & anim.frame)",
        "Layout-Preserving Element Reveal (.show = False -> True)",
        "Quantitative Chart Growth (.draw_ratio & .draw_direction)",
        "Interactive Slide Playback (anim:click, anim:once, anim:pause)",
    ],
)
```
:::

::: note
- Welcome to Chapter 5: Multi-Frame Animations.
- Static diagrams are great for structure, but distributed systems, network traffic, and phased rollouts are inherently temporal.
- In this chapter, we explore how Drawlib brings diagrams to life using a declarative frame context manager (`Animation` and `with anim.frame():`), layout-preserving element visibility (`.show`), quantitative chart growth (`.draw_ratio`), and interactive slide playback controls.
:::
