# Drawlib TreeNode SmartArt Guidelines (`lib-smartarts-tree`)

`TreeNode` renders hierarchical file-tree and directory-like listings with orthogonal connector lines, cascading text/line styles, and optional prepended or appended icons.

---

## 1. Architecture & Geometry

- **Anchor**: Fixed Top-Left coordinate `xy=(x, y)`. The root label is drawn at `xy`, and descendant branches step downward (`child_y = current_y - line_vertical_margin`).
- **Root Node Requirement**: The root `TreeNode` must define all five layout/style settings for downward propagation:
  - `text_style`
  - `line_style`
  - `line_horizontal_margin`
  - `line_horizontal_length`
  - `line_vertical_margin`
  Child nodes inherit these settings automatically via cascading unless individually overridden. Calling `draw()` on a root node missing any of the five raises a `ValueError`.

---

## 2. Constructor, Properties & Node Methods

```python
TreeNode(
    text: str,
    *,
    text_style: Style | None = None,
    line_style: Style | None = None,
    line_horizontal_margin: float | None = None,
    line_horizontal_length: float | None = None,
    line_vertical_margin: float | None = None,
    children: list[TreeNode] | None = None,
    show: bool = True,
)
```

### Properties & Mutation Attributes

- `node.text: str`: Get or mutate the node text label.
- `node.text_style: Style | None`: Get or mutate the node text style.
- `node.line_style: Style | None`: Get or mutate the connector line style.
- `node.children: list[TreeNode]`: Access the list of child `TreeNode` instances.
- `node.show: bool`: Visibility flag (`True` by default). Setting `child.show = False` hides that node and its connector tick while preserving vertical row spacing for all sibling and following nodes.

### Adding Children (`node.add` vs. `children=[...]`)

```python
child = node.add(
    text: str,
    *,
    text_style: Style | None = None,
    line_style: Style | None = None,
    line_horizontal_margin: float | None = None,
    line_horizontal_length: float | None = None,
    line_vertical_margin: float | None = None,
    show: bool = True,
) -> TreeNode
```

> **Important — `node.add(text: str, ...)` Signature**:
> `node.add()` accepts **`text: str`** (not `child: TreeNode | str`), creates a new child `TreeNode`, appends it to `node.children`, and returns the newly created child `TreeNode` instance.
> If you construct child `TreeNode(...)` objects directly, pass them via the constructor's `children=[TreeNode(...), ...]` parameter (or append to `node.children`).

### Drawing Method

```python
node.draw(
    xy: tuple[float, float],
    scale: float = 1.0,
) -> Self
```

Renders the tree hierarchy starting at top-left `xy` with optional proportional `scale` around `xy`, returning `self`.

---

## 3. Custom Drawing Items (Icons & Badges)

Register reusable icon or shape callables (e.g. `drawlib.icons.phosphor`) on `TreeNode` and attach them to specific nodes:

```python
TreeNode.register_drawing_item(
    name: str,
    location: Literal["before", "after"],
    padding_width: float,
    function: Callable[..., Any],
    style: Style,
    args: dict[str, Any],
) -> None

node.set_drawing_item(name: str) -> Self
```

- `location`: `"before"` (draws icon at node `x` and shifts text rightward by `padding_width`) or `"after"` (draws text at node `x` and places icon at `x + padding_width`).
- `padding_width`: Horizontal offset in canvas units between icon and text.
- `function`: Drawing callable accepting `xy` and `style` (e.g. `phosphor.folder`, `phosphor.file_py`, `phosphor.file_code`).
- `style`: `Style` passed to `function` (automatically patched with `halign="left", valign="center"`).
- `args`: Additional keyword arguments dictionary passed to `function` (e.g. `{"width": 3.0}`).
- `set_drawing_item(name)`: Associates the node with the registered item name and returns `self` for fluent chaining.

---

## 4. Production Example: Monorepo Project Structure

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.preset_colors import CssColors
from drawlib.smartarts import TreeNode
from drawlib.styles import Colors, Styles

setup(width=110, height=70)

TreeNode.register_drawing_item(
    name="dir_icon",
    location="before",
    padding_width=4.5,
    function=phosphor.folder,
    style=Styles.Primary.patch(icon_color=Colors.Primary),
    args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="py_icon",
    location="before",
    padding_width=4.5,
    function=phosphor.file_py,
    style=Styles.Primary.patch(icon_color=CssColors.ForestGreen),
    args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="yaml_icon",
    location="before",
    padding_width=4.5,
    function=phosphor.file_code,
    style=Styles.Primary.patch(icon_color=Colors.Dark),
    args={"width": 3.0},
)

tree_root = TreeNode(
    "monorepo-root/",
    text_style=Styles.Dark.patch(text_size=11.0),
    line_style=Styles.Muted.patch(line_width=1.0),
    line_horizontal_margin=3.0,
    line_horizontal_length=3.0,
    line_vertical_margin=6.0,
    children=[
        TreeNode(
            "services/",
            children=[
                TreeNode(
                    "auth_api/",
                    children=[
                        TreeNode("main.py").set_drawing_item("py_icon"),
                        TreeNode("config.py").set_drawing_item("py_icon"),
                    ],
                ).set_drawing_item("dir_icon"),
                TreeNode(
                    "payment_api/",
                    children=[TreeNode("worker.py").set_drawing_item("py_icon")],
                ).set_drawing_item("dir_icon"),
            ],
        ).set_drawing_item("dir_icon"),
        TreeNode(
            "deploy/",
            children=[
                TreeNode("k8s-prod.yaml").set_drawing_item("yaml_icon"),
                TreeNode("docker-compose.yaml").set_drawing_item("yaml_icon"),
            ],
        ).set_drawing_item("dir_icon"),
    ],
).set_drawing_item("dir_icon")

# Or append children dynamically via .add(text: str, ...)
tree_root.add("pyproject.toml").set_drawing_item("yaml_icon")

tree_root.draw(xy=(10, 62))
save()
```
