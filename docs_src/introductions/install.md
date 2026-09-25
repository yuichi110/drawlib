# Install

Drawlib can be installed using `uv` (recommended) or `pip`.


## Using uv (Recommended)

Add Drawlib to your project:

```bash
$ uv add drawlib
```

To install with optional PDF export support (`drawlib build pdf`):

```bash
$ uv add "drawlib[pdf]"
$ uv run playwright install chromium
```


## Using pip

Install Drawlib into your Python environment:

```bash
$ pip install drawlib
```

To install with optional PDF export support (`drawlib build pdf`):

```bash
$ pip install "drawlib[pdf]"
$ playwright install chromium
```

---

## Verifying Installation

After installation, verify that the `drawlib` CLI and library are installed:

```bash
# When using uv:
$ uv run drawlib --version

# When using pip / global environment:
$ drawlib --version
# or: $ python -m drawlib --version
```

The CLI manages document compilation (`drawlib build`), local preview servers (`drawlib serve`), project scaffolding (`drawlib init`), and diagram export. For more details, see the **[CLI Reference](../cli/index.md)**.

---

## Troubleshooting

Drawlib depends on `matplotlib`, which requires `msvc-runtime` on Windows. If it is not automatically installed on Windows systems, you may encounter the following error:

```text
ImportError: DLL load failed while importing _cext: The specified module could not be found
```

In this case, manually install `msvc-runtime`:

```bash
# Using uv:
$ uv pip install msvc-runtime

# Using pip:
$ pip install msvc-runtime
```

---

## Release Policy

Drawlib follows semantic versioning (`<major>.<minor>.<patch>`):

- **Major Version**: Significant architectural or API changes
- **Minor Version**: New features and minor API additions
- **Patch Version**: Bug fixes and minor maintenance

During development cycles, pre-release packages (`dev<n>`) are published for testing:

```bash
# Using uv:
$ uv add "drawlib==0.3.0.dev1"

# Using pip:
$ pip install "drawlib==0.3.0.dev1"
```

Once a feature cycle stabilizes, an official release (e.g. `0.3.1`) is published.


```drawlib fold-code 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.shapes import arrow, chevron
from drawlib.text import text
from drawlib.types import Style


def draw_versions(x: float, y: float, versions: list[str]):
    width = 6
    height = 5
    corner_angle = 60
    padding = 1

    s1 = "blue_flat"
    s2 = Style(line_style="dashed", fill_color=Colors.Transparent, line_color=Colors.Blue)
    st1 = Style(text_size=11, text_color=Colors.White, text_font=FontRoboto.ROBOTO_REGULAR)
    st2 = Style(text_size=11, text_color=Colors.Blue, text_font=FontRoboto.ROBOTO_REGULAR)
    for i, version in enumerate(versions):
        if len(versions) == 5 and i in [0, 1]:
            chevron(
                (x + (width + padding) * i, y),
                width=width,
                height=height,
                corner_angle=corner_angle,
                style=s2,
                text=version,
                textstyle=st2,
            )
        else:
            chevron(
                (x + (width + padding) * i, y),
                width=width,
                height=height,
                corner_angle=corner_angle,
                style=s1,
                text=version,
                textstyle=st1,
            )


config(width=115, height=72)

ts = Style(text_size=16, text_font=FontRoboto.ROBOTO_REGULAR)
text((7, 6), "private\nα\nrelease", style=ts)
text((7, 18), "public\nβ\nrelease", style=ts)
text((7, 30), "public\nreleases", style=ts)
text((7, 51), "matured\npublic\nreleases", style=ts)

# v0.1
draw_versions(15, 3, ["0.1.1", "...", "0.1.n"])
line((32, 9), (32, 13.5), arrowhead="->")

# v0.2
draw_versions(29, 15, ["0.2.1", "...", "0.2.n"])
line((46, 21), (46, 25.5), arrowhead="->")

text((50, 34), "dev only", style=Style(text_size=14, text_font=FontRoboto.ROBOTO_REGULAR))
draw_versions(43, 27, ["0.3.0\ndev1", "...", "0.3.1", "...", "0.3.n"])
line((74, 33), (74, 37.5), arrowhead="->")
text((74, 39.5), 'keep "0.n.m" till library matures', style=Style(text_font=FontRoboto.ROBOTO_REGULAR))
line((74, 43), (74, 46.5), arrowhead="->")

text((78, 55), "dev only", style=Style(text_size=14, text_font=FontRoboto.ROBOTO_REGULAR))
draw_versions(71, 48, ["1.0.0\ndev1", "...", "1.0.1", "...", "1.0.n"])
line((102, 54), (102, 58.5), arrowhead="->")
text((102, 62), "...", style=Style(text_size=16, text_font=FontRoboto.ROBOTO_REGULAR))

arrow(
    (15, 67),
    (113, 67),
    tail_width=3,
    head_width=7,
    head_length=5,
    style="blue_flat",
    text="Time",
    textstyle=Style(text_color=Colors.White, text_size=14, text_font=FontRoboto.ROBOTO_REGULAR),
)
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
