# 4. Preset Styles & Themes

Instead of manually configuring RGB tuples or custom `Style(...)` models for every shape, Drawlib includes a comprehensive **Preset Styles** system accessed via `from drawlib.styles import styles`. Every drawing function accepts a preset style such as `style=styles.primary` or `style=styles.danger_flat`.

## Official Style Themes

Drawlib ships with three curated preset themes:
- **`"default"`**: Balanced, clean palette designed for architectural blueprints and engineering diagrams.
- **`"google"`**: Modern, vibrant palette adhering to Google Cloud / Material design standards.
- **`"monochrome"`**: Crisp grayscale palette tailored for print books and academic publications.

## Semantic Roles & Style Matrix

Drawlib defines 6 core semantic roles across all themes:
- **`primary`**: Main application logic, core services, and primary actions.
- **`secondary`**: Data stores, caches, queues, and auxiliary services.
- **`accent`**: Entry points, clients, gateways, and focal callouts.
- **`muted`**: Group containers, boundaries, subnets, and structural lines.
- **`danger`**: Errors, alerts, security vulnerabilities, and failures.
- **`success`**: Healthy status, completed milestones, and verified checks.

Each semantic role (and color) provides 10 orthogonal variants:
`bordered` (default), `flat`, `outline`, `dashed`, `bold`, `light`, `outline_bold`, `outline_light`, `dashed_bold`, and `dashed_light`.

```python
from drawlib.styles import styles

circle((20, 25), radius=10, style=styles.primary)        # Primary bordered
circle((45, 25), radius=10, style=styles.secondary_flat) # Secondary flat
circle((70, 25), radius=10, style=styles.danger_outline) # Danger outline
```

```drawlib 620px center caption:"Figure 4.1: Core Semantic Styles Applied to Lines, Shapes, and Text"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.styles import styles
from drawlib.text import text

setup(width=120, height=45)
line_y = 36
text_y = 9

items = [
    (12, "primary", styles.primary),
    (31, "secondary", styles.secondary),
    (50, "accent", styles.accent),
    (69, "muted", styles.muted),
    (88, "danger", styles.danger),
    (107, "success", styles.success),
]

for x, label, st in items:
    line((x - 7, line_y), (x + 7, line_y), style=st)
    circle((x, 23), radius=7, style=st)
    text((x, text_y), text=label, style=st, size=9)
```
