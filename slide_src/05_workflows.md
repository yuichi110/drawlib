::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Workflows & Pipelines
:::

::: block (80, 140) (740, 840)
## Automated CI/CD & Caching

Technical diagrams shouldn't slow down your deployment cycles:

- **Git-Triggered Pipeline**: Build runs automatically on pull requests
- **Change Detection**: Analyzes document diffs and Python dependencies
- **SQLite Hash Caching**:
  - Unchanged blocks are restored in **< 1ms**
  - Only modified diagram code triggers full Python execution
- **Dynamic Animations**: Render looping animated WebP diagrams natively using `Animation`
:::

::: block (880, 140) (960, 840)
```drawlib file:workflow_pipeline.webp
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles


def draw_pipeline_state(active_step: str) -> None:
    flow = FlowDiagram(
        node_style=Styles.MutedFlat,
        edge_style=Styles.Primary,
        title="Illustration & Slide CI/CD Pipeline (Live)",
    )
    s_start = Styles.AccentFlat if active_step == "push" else Styles.PrimaryFlat
    s_detect = Styles.AccentFlat if active_step == "detect" else Styles.PrimaryFlat
    s_check = Styles.AccentFlat if active_step == "check" else Styles.PrimaryFlat
    s_cache = Styles.AccentFlat if active_step == "cache" else Styles.PrimaryFlat
    s_build = Styles.AccentFlat if active_step == "build" else Styles.PrimaryFlat
    s_deploy = Styles.AccentFlat if active_step == "deploy" else Styles.PrimaryFlat

    start = flow.add(Start("Git Push", style=s_start), xy=(11.0, 46.0))
    detect = flow.add(Process("Detect Changed", style=s_detect), xy=(35.0, 46.0))
    cache_check = flow.add(Decision("In Cache?", style=s_check), xy=(62.0, 46.0))
    render = flow.add(Process("Drawlib Python", style=Styles.PrimaryFlat), xy=(62.0, 22.0))
    fetch_cache = flow.add(Process("Read SQLite", style=s_cache), xy=(62.0, 68.0))
    build_deck = flow.add(Process("Build Slide/HTML", style=s_build), xy=(94.0, 46.0))
    end = flow.add(End("Deploy Slide", style=s_deploy), xy=(122.0, 46.0))

    start.connect(detect)
    detect.connect(cache_check)
    cache_check.connect(fetch_cache, label="Hit", start_side="top", end_side="bottom")
    cache_check.connect(render, label="Miss", start_side="bottom", end_side="top")
    fetch_cache.connect(build_deck, start_side="right", end_side="top")
    render.connect(build_deck, start_side="right", end_side="bottom")
    build_deck.connect(end)

    flow.draw(xy=(2.0, -8.0))


clear()
setup(width=138, height=70)
anim = Animation(fps=1.0, loop=0)
for step, dur in zip(["push", "detect", "check", "cache", "build", "deploy"], [0.8, 0.8, 0.8, 1.0, 0.8, 1.5]):
    with anim.frame(duration=dur):
        draw_pipeline_state(step)
save()
```
:::
::: block (80, 1010) (820, 30) font:14px
*Drawlib: Illustration as Code*
:::
