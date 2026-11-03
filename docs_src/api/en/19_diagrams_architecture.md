# drawlib.diagrams.architecture

Declarative cloud, infrastructure, and distributed systems architecture diagrams featuring icon-centric service cards, nested boundary groups, and orthogonal bus routing. Canonical import: `from drawlib.diagrams.architecture import ArchitectureDiagram, Edge, GcpIcon, Junction, Node, NodeGroup, PhosphorIcon`.

```drawlib align=center code=fold file=19_diagrams_architecture_hero.png caption="Cloud VPC Architecture with Nested NodeGroup and Orthogonal Bus Routing"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Colors, Styles

setup(width=120, height=64)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

client = d.add(
    Node("Client", width=18, height=16, icon=PhosphorIcon.LAPTOP, icon_size=7.0),
    xy=(9.0, 25.0),
)

vpc = d.add(
    NodeGroup(
        title="VPC Network",
        width=56,
        height=54,
        padding=5.0,
        style=Styles.PrimaryNeutral.patch(line_style="dashed"),
        text_style=Styles.PrimaryBold.patch(text_size=11.0, halign="left"),
    ),
    xy=(30.0, 0.0),
)
gateway = vpc.add(
    Node(
        "API Gateway",
        width=20,
        height=16,
        icon=PhosphorIcon.CLOUD_CHECK,
        icon_size=6.5,
        style=Styles.White,
        text_style=Styles.WhiteBold.patch(text_color=Colors.White, text_size=10.5),
        card_style=Styles.PrimaryFlat,
    ),
    xy=(13.5, 25.0),
)
auth_pod = vpc.add(
    Node("Auth Pod", width=19, height=15, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=6.5),
    xy=(43.0, 36.5),
)
order_pod = vpc.add(
    Node(
        "Order Pod",
        width=19,
        height=15,
        icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE,
        icon_size=6.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(43.0, 13.5),
)

db = d.add(
    Node("Cloud SQL", width=20, height=16, icon=GcpIcon.CLOUD_SQL, icon_size=7.0, card_style=Styles.SecondaryNeutral),
    xy=(102.0, 25.0),
)

d.connect(client, gateway, label="HTTPS", padding=1.0)
gateway.fork([auth_pod, order_pod], at_x=58.0, padding=1.0)
d.connect(auth_pod, db, padding=1.0)
d.connect(order_pod, db, padding=1.0)

d.draw(xy=(60.0, 32.0), align="center")
save()
```

---

## `class` ArchitectureDiagram

Top-level container for architecture diagrams managing service nodes, nested boundary groups, junctions, and edge routing.

```python
ArchitectureDiagram(
    *,
    node_style: Style,
    node_text_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    node_card_style: Style | None = None,
    title: str = "",
    title_style: Style | None = None,
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
) -> None
```

- **Coordinate Anchor**: `draw(xy=(0.0, 0.0), align="bottom_left")` places the diagram's local `(0.0, 0.0)` bottom-left origin at canvas coordinate `xy` (or centers the diagram bounding box at `xy` when `align="center"`). For automatic topology coordinate solving, see [`ArchitectureGraph.get_layout()`](25_graph.md#architecturegraph).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base style applied to node vector icons and fallback visual elements (keyword-only). |
| `node_text_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base typography style applied to node labels and group header titles (keyword-only). |
| `edge_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base stroke and arrowhead style applied to connection edges (keyword-only). |
| `edge_text_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base typography style applied to edge labels (keyword-only). |
| `node_card_style` | `Style \| None` | `None` | Optional default background fill and border style for [`Node`](#node) cards (`None` renders transparent cards). |
| `title` | `str` | `""` | Optional diagram title rendered centered above the top boundary. |
| `title_style` | `Style \| None` | `None` | Optional typography style override for `title`. |
| `width` | `float \| None` | `None` | Optional fixed diagram width in local units (auto-computed from items when `None`). |
| `height` | `float \| None` | `None` | Optional fixed diagram height in local units (auto-computed from items when `None`). |
| `style` | `Style \| None` | `None` | Optional outer container card background and border style. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, item: ItemT, xy: tuple[float, float], *, show: bool \| None = None) -> ItemT` | Add a [`Node`](#node) (center `xy`), [`NodeGroup`](#nodegroup) (bottom-left `xy`), or [`Junction`](#junction) at diagram-local coordinate `xy`. |
| `add_edge` | `method` | `(self, edge: Edge, *, show: bool \| None = None) -> Edge` | Register a pre-constructed [`Edge`](#edge) instance with this diagram. |
| `connect` | `method` | `(self, start: Connectable, end: Connectable, label: str = "", arrow: ArrowType = "->", routing: RoutingType = "orthogonal", style: Style \| None = None, text_style: Style \| None = None, padding: PaddingType = 0.0, show: bool = True) -> Edge` | Create and register an [`Edge`](#edge) between any two connectable items (`Node`, `NodeGroup`, or `Junction`). |
| `draw` | `method` | `(self, xy: tuple[float, float] = (0.0, 0.0), *, align: Literal["bottom_left", "center"] = "bottom_left", scale: PosFloat = 1.0) -> None` | Render the complete architecture diagram onto the active canvas anchored at `xy`. |
| `edges` | `property` | `-> list[Edge]` | Return the list of registered [`Edge`](#edge) connections in declaration order. |
| `get_size` | `method` | `(self) -> tuple[float, float]` | Return the overall `(width, height)` of the diagram in unscaled local units. |
| `items` | `property` | `-> list[Node \| NodeGroup \| Junction]` | Return the list of top-level items registered directly on the diagram. |
| `junction` | `method` | `(self, xy: tuple[float, float], *, show: bool = True) -> Junction` | Create and register a zero-size [`Junction`](#junction) waypoint/branch point at local coordinate `xy`. |

---

## `class` Node

Vertex component representing a service, actor, compute instance, or managed resource card in an architecture diagram.

```python
Node(
    text: str = "",
    width: float = 20.0,
    height: float = 16.0,
    icon: IconType = None,
    icon_size: float = 8.0,
    style: Style | None = None,
    text_style: Style | None = None,
    card_style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: **Center `(cx, cy)`** when registered via `d.add(node, xy=(cx, cy))` or `group.add(node, xy=(lx, ly))` (where `(lx, ly)` is relative to the parent [`NodeGroup`](#nodegroup)'s bottom-left `(0, 0)`).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | `""` | Display label rendered inside the lower portion of the card (supports `\n` line breaks). |
| `width` | `float` | `20.0` | Card bounding box width in local units. |
| `height` | `float` | `16.0` | Card bounding box height in local units. |
| `icon` | `IconType` | `None` | Any of the [34 icon enums](#icon-enums), icon function (`drawlib.icons.*`), [`CustomIcon`](#customicon), [`Dimage`](04_images_and_math.md#dimage), `PIL.Image.Image`, or image path (`str \| Path`). |
| `icon_size` | `float` | `8.0` | Rendered icon width/height in local coordinate units. |
| `style` | `Style \| None` | `None` | Optional style override for vector icon tinting (falls back to `diagram.node_style`). |
| `text_style` | `Style \| None` | `None` | Optional typography style override for `text` (falls back to `diagram.node_text_style`). |
| `card_style` | `Style \| None` | `None` | Optional card background fill and border style override (falls back to `diagram.node_card_style`). |
| `show` | `bool` | `True` | Visibility flag (`False` hides the node and its incident edges while keeping layout geometry). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `bottom` | `property` | `-> tuple[float, float]` | Bottom boundary anchor coordinate in diagram-root coordinates. |
| `center` | `property` | `-> tuple[float, float]` | Center coordinate of the node card in diagram-root coordinates. |
| `connect` | `method` | `(self, target: Connectable, label: str = "", arrow: ArrowType = "->", routing: RoutingType = "orthogonal", style: Style \| None = None, padding: PaddingType = 0.0, show: bool = True) -> Edge` | Connect this node to `target` and register the resulting [`Edge`](#edge) on the parent diagram. |
| `fork` | `method` | `(self, targets: list[Connectable], at_x: float \| None = None, at_y: float \| None = None, style: Style \| None = None, padding: PaddingType = 0.0, show: bool = True) -> list[Edge]` | Fan out from this node to multiple `targets` via an intermediate orthogonal [`Junction`](#junction) placed at `at_x` or `at_y`. |
| `get_absolute_xy` | `method` | `(self) -> tuple[float, float]` | Compute the node center `(x, y)` relative to the diagram root across any nested [`NodeGroup`](#nodegroup) ancestors. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(-width/2, -height/2, width/2, height/2)` relative to node center `(0, 0)`. |
| `get_size` | `method` | `(self) -> tuple[float, float]` | Return the card `(width, height)`. |
| `left` | `property` | `-> tuple[float, float]` | Left boundary anchor coordinate in diagram-root coordinates. |
| `right` | `property` | `-> tuple[float, float]` | Right boundary anchor coordinate in diagram-root coordinates. |
| `top` | `property` | `-> tuple[float, float]` | Top boundary anchor coordinate in diagram-root coordinates. |
| `xy` | `property` | `-> tuple[float, float]` | Relative center coordinate `(x, y)` passed when adding this node to its parent container. |

---

## `class` NodeGroup

Hierarchical boundary container grouping [`Node`](#node) cards, [`Junction`](#junction) points, and nested sub-groups (e.g., Cloud Regions, VPCs, Subnets, and Kubernetes clusters).

```python
NodeGroup(
    title: str = "",
    width: float | None = None,
    height: float | None = None,
    padding: float = 5.0,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: **Bottom-Left `(x0, y0)`** when added to `ArchitectureDiagram` or a parent `NodeGroup`. Calling `group.add(child, xy=(lx, ly))` positions `child` in **group-local coordinates** relative to `group`'s own bottom-left `(0, 0)` corner (`(lx, ly)` is the child's center for `Node` and bottom-left for a nested `NodeGroup`).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | `""` | Group banner label rendered near the top-left inside the boundary box. |
| `width` | `float \| None` | `None` | Optional fixed boundary width (`None` auto-sizes around enclosed children plus `padding`). |
| `height` | `float \| None` | `None` | Optional fixed boundary height (`None` auto-sizes around enclosed children plus `padding`). |
| `padding` | `float` | `5.0` | Inner clearance margin around child items when auto-sizing. |
| `style` | `Style \| None` | `None` | Optional boundary rectangle fill and stroke style (defaults to a dashed border when `None`). |
| `text_style` | `Style \| None` | `None` | Optional typography style override for `title` (falls back to `diagram.node_text_style`). |
| `show` | `bool` | `True` | Visibility flag for the group boundary and title (child items remain controlled by their own `show` flags). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, item: ItemT, xy: tuple[float, float], *, show: bool \| None = None) -> ItemT` | Add a child [`Node`](#node), nested [`NodeGroup`](#nodegroup), or [`Junction`](#junction) at group-relative coordinate `xy`. |
| `bottom` | `property` | `-> tuple[float, float]` | Bottom midpoint anchor on the group boundary in diagram-root coordinates. |
| `center` | `property` | `-> tuple[float, float]` | Center coordinate of the group boundary in diagram-root coordinates. |
| `connect` | `method` | `(self, target: Connectable, label: str = "", arrow: ArrowType = "->", routing: RoutingType = "orthogonal", style: Style \| None = None, padding: PaddingType = 0.0, show: bool = True) -> Edge` | Connect this group's outer boundary to `target` and register the [`Edge`](#edge). |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(min_x, min_y, max_x, max_y)` relative to the group's bottom-left `(0, 0)`. |
| `get_size` | `method` | `(self) -> tuple[float, float]` | Return the visual `(width, height)` of the group boundary. |
| `items` | `property` | `-> list[Node \| NodeGroup \| Junction]` | Return the list of direct child items registered inside this group. |
| `left` | `property` | `-> tuple[float, float]` | Left midpoint anchor on the group boundary in diagram-root coordinates. |
| `right` | `property` | `-> tuple[float, float]` | Right midpoint anchor on the group boundary in diagram-root coordinates. |
| `top` | `property` | `-> tuple[float, float]` | Top midpoint anchor on the group boundary in diagram-root coordinates. |
| `xy` | `property` | `-> tuple[float, float]` | Group bottom-left coordinate `(x, y)` relative to its immediate parent container. |

---

## `class` Edge

Directed, bidirectional, or undirected connection line linking two connectable elements (`Node`, `NodeGroup`, or `Junction`).

```python
Edge(
    start: Connectable,
    end: Connectable,
    label: str = "",
    arrow: ArrowType = "->",
    routing: RoutingType = "orthogonal",
    style: Style | None = None,
    text_style: Style | None = None,
    padding: PaddingType = 0.0,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: Automatically attaches to boundary anchors of `start` and `end`; intermediate waypoints passed to `.points()`, `.via()`, or `.add_point()` use diagram-root `(x, y)` coordinates.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `start` | `Node \| NodeGroup \| Junction` | *(Required)* | Source connectable element. |
| `end` | `Node \| NodeGroup \| Junction` | *(Required)* | Target connectable element. |
| `label` | `str` | `""` | Protocol or description label rendered along the edge path. |
| `arrow` | `Literal["->", "<-", "<->", "-"]` | `"->"` | Arrowhead direction marker. |
| `routing` | `Literal["orthogonal", "direct", "curved"]` | `"orthogonal"` | Path routing mode (`"orthogonal"` right-angled bends, `"direct"` straight segment, or `"curved"` spline). |
| `style` | `Style \| None` | `None` | Optional stroke style override (falls back to `diagram.edge_style`). |
| `text_style` | `Style \| None` | `None` | Optional label typography style override (falls back to `diagram.edge_text_style`). |
| `padding` | `float \| tuple[float, float]` | `0.0` | Symmetric or `(start_pad, end_pad)` clearance gap between element boundaries and line endpoints. |
| `show` | `bool` | `True` | Whether to render this edge. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add_point` | `method` | `(self, xy: tuple[float, float]) -> Junction` | Append intermediate waypoint `xy` and return a registered [`Junction`](#junction) at `xy` for tapping/branching. |
| `points` | `method` | `(self, waypoints: list[tuple[float, float]]) -> Edge` | Set explicit intermediate `(x, y)` routing waypoints and return `self`. |
| `set_arrow` | `method` | `(self, arrow: ArrowType) -> Edge` | Update arrowhead direction (`"->"`, `"<-"`, `"<->"`, `"-"`) and return `self`. |
| `set_label` | `method` | `(self, text: str, pos: float = 0.5) -> Edge` | Set edge label `text` and normalized path position `pos` (`0.0`–`1.0`) and return `self`. |
| `set_padding` | `method` | `(self, padding: PaddingType) -> Edge` | Update endpoint clearance gap padding and return `self`. |
| `set_style` | `method` | `(self, style: Style) -> Edge` | Override line stroke [`Style`](05_styles_and_types.md#style) and return `self`. |
| `set_text_style` | `method` | `(self, text_style: Style) -> Edge` | Override edge label [`Style`](05_styles_and_types.md#style) and return `self`. |
| `via` | `method` | `(self, *waypoints: tuple[float, float]) -> Edge` | Unpacked variadic shorthand for `.points(list(waypoints))`; returns `self`. |
| `waypoints` | `property` | `-> list[tuple[float, float]]` | Return a copy of intermediate `(x, y)` waypoints configured on this edge. |

---

## `class` Junction

Zero-size connectable waypoint and multi-edge merge/branch point in an architecture diagram.

```python
Junction(
    xy: tuple[float, float],
    *,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: Exact point `(x, y)` in its parent container (`ArchitectureDiagram` or [`NodeGroup`](#nodegroup)). Prefer creating junctions via `d.junction(xy)` or `edge.add_point(xy)`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *(Required)* | Local `(x, y)` coordinate of the junction point. |
| `show` | `bool` | `True` | Whether edges routed through this junction are visible (keyword-only). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `bottom` | `property` | `-> tuple[float, float]` | Bottom anchor coordinate (equal to the junction's absolute `(x, y)`). |
| `center` | `property` | `-> tuple[float, float]` | Center coordinate (equal to the junction's absolute `(x, y)`). |
| `connect` | `method` | `(self, target: Connectable, label: str = "", arrow: ArrowType = "->", routing: RoutingType = "orthogonal", style: Style \| None = None, padding: PaddingType = 0.0, show: bool = True) -> Edge` | Connect this junction to `target` and register the [`Edge`](#edge) on the parent diagram. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return zero-area local bounding box `(0.0, 0.0, 0.0, 0.0)`. |
| `get_size` | `method` | `(self) -> tuple[float, float]` | Return zero visual dimensions `(0.0, 0.0)`. |
| `left` | `property` | `-> tuple[float, float]` | Left anchor coordinate (equal to the junction's absolute `(x, y)`). |
| `right` | `property` | `-> tuple[float, float]` | Right anchor coordinate (equal to the junction's absolute `(x, y)`). |
| `top` | `property` | `-> tuple[float, float]` | Top anchor coordinate (equal to the junction's absolute `(x, y)`). |
| `xy` | `property` | `-> tuple[float, float]` | Local `(x, y)` coordinate of this junction relative to its parent. |

---

## `class` CustomIcon

Adapter wrapping raster image files, [`Dimage`](04_images_and_math.md#dimage) objects, or `PIL.Image.Image` instances for use as `Node(..., icon=CustomIcon(...))`.

```python
CustomIcon(
    image: str | Path | Dimage | Image | CustomIcon,
) -> None
```

- **Coordinate Anchor**: Centered automatically inside the host [`Node`](#node) card's icon slot at `icon_size`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `image` | `str \| Path \| Dimage \| Image \| CustomIcon` | *(Required)* | Path to a PNG/JPEG file, a [`Dimage`](04_images_and_math.md#dimage) instance, a `PIL.Image.Image` object, or another `CustomIcon`. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `copy` | `method` | `(self) -> CustomIcon` | Return an independent deep copy of this `CustomIcon`. |
| `dimage` | `property` | `-> Dimage` | Return the underlying [`Dimage`](04_images_and_math.md#dimage) instance wrapping the image buffer. |

---

## `type` icons

Re-exported icon namespace submodule (`drawlib.diagrams.architecture.icons`) providing grouped access to [`CustomIcon`](#customicon), `IconType`, and all 34 diagram icon enums without importing individual enum classes at top level.

```python
from drawlib.diagrams.architecture import icons

# Equivalent access via submodule namespace:
node = Node("Gateway", icon=icons.GcpIcon.API_GATEWAY)
```

- **Coordinate Anchor**: Not applicable (namespace module re-exporting 40 icon types and helpers).

| Export Group | Exported Symbols | Description |
| :--- | :--- | :--- |
| **Icon Enums (34)** | `icons.AiIcon` .. `icons.WorkspaceIcon` | All 34 `StrEnum` icon catalogs listed in [`Icon Enums (34 Suites)`](#icon-enums). |
| **Custom Wrapper** | `icons.CustomIcon` | Alias of [`CustomIcon`](#customicon) for custom raster/nested diagram icons. |
| **Type Aliases & Helpers** | `icons.IconType`, `icons.draw_node_icon` | Union type alias accepted by `Node(icon=...)` and internal icon renderer helper. |

---

## `enum` Icon Enums (34 Suites)

All 34 standardized icon `StrEnum` classes re-exported directly from `drawlib.diagrams.architecture` (and `drawlib.diagrams.architecture.icons`) for declarative `Node(..., icon=<Enum>.<MEMBER>)` configuration. `PhosphorIcon` glyphs are monochrome vector font icons tinted by `node.style` / `diagram.node_style`; the remaining 33 suites render multi-color or pastel PNG assets from [`drawlib.icons`](08_icons.md).

| Icon Enum | Corresponding `drawlib.icons` Suite | Category & Asset Style |
| :--- | :--- | :--- |
| `AiIcon` | [`drawlib.icons.ai`](08_icons.md#ai) | Official AI, LLM, and ML platform icons |
| `AwsIcon` | [`drawlib.icons.aws`](08_icons.md#aws) | Official Amazon Web Services architecture icons |
| `AzureIcon` | [`drawlib.icons.azure`](08_icons.md#azure) | Official Microsoft Azure architecture icons |
| `BusinessIcon` | [`drawlib.icons.business`](08_icons.md#business) | Enterprise SaaS, ERP, CRM, and FinTech brand icons |
| `ClientIcon` | [`drawlib.icons.client`](08_icons.md#client) | Browsers, mobile/desktop OS, and client device icons |
| `CloudIcon` | [`drawlib.icons.cloud`](08_icons.md#cloud) | Cloud, PaaS, CDN, and hosting provider brand icons |
| `CnativeIcon` | [`drawlib.icons.cnative`](08_icons.md#cnative) | Kubernetes and CNCF cloud-native ecosystem icons |
| `CodeIcon` | [`drawlib.icons.code`](08_icons.md#code) | Programming languages, frameworks, and runtime icons |
| `DataIcon` | [`drawlib.icons.data`](08_icons.md#data) | Relational/NoSQL databases, caches, and streaming icons |
| `DevopsIcon` | [`drawlib.icons.devops`](08_icons.md#devops) | CI/CD, IaC, containers, and observability tool icons |
| `FacilityIcon` | [`drawlib.icons.facility`](08_icons.md#facility) | Datacenter, racks, telecom carriers, and hardware icons |
| `GcpIcon` | [`drawlib.icons.gcp`](08_icons.md#gcp) | Official Google Cloud Platform architecture icons |
| `ItserviceIcon` | [`drawlib.icons.itservice`](08_icons.md#itservice) | IT service management, consulting, and enterprise vendor icons |
| `NetworkIcon` | [`drawlib.icons.network`](08_icons.md#network) | Routers, switches, firewalls, DNS, and network topology icons |
| `OriginalAiIcon` | [`drawlib.icons.original_ai`](08_icons.md#original-ai) | Drawlib vendor-neutral flat AI & ML icons |
| `OriginalBusinessIcon` | [`drawlib.icons.original_business`](08_icons.md#original-business) | Drawlib vendor-neutral flat business & office icons |
| `OriginalClientIcon` | [`drawlib.icons.original_client`](08_icons.md#original-client) | Drawlib vendor-neutral flat client & device icons |
| `OriginalCloudIcon` | [`drawlib.icons.original_cloud`](08_icons.md#original-cloud) | Drawlib vendor-neutral flat cloud service icons |
| `OriginalCnativeIcon` | [`drawlib.icons.original_cnative`](08_icons.md#original-cnative) | Drawlib vendor-neutral flat cloud-native & container icons |
| `OriginalCodeIcon` | [`drawlib.icons.original_code`](08_icons.md#original-code) | Drawlib vendor-neutral flat code & SDK icons |
| `OriginalDataIcon` | [`drawlib.icons.original_data`](08_icons.md#original-data) | Drawlib vendor-neutral flat database & storage icons |
| `OriginalDevopsIcon` | [`drawlib.icons.original_devops`](08_icons.md#original-devops) | Drawlib vendor-neutral flat DevOps & pipeline icons |
| `OriginalFacilityIcon` | [`drawlib.icons.original_facility`](08_icons.md#original-facility) | Drawlib vendor-neutral flat building & facility icons |
| `OriginalItserviceIcon` | [`drawlib.icons.original_itservice`](08_icons.md#original-itservice) | Drawlib vendor-neutral flat IT operations & support icons |
| `OriginalNetworkIcon` | [`drawlib.icons.original_network`](08_icons.md#original-network) | Drawlib vendor-neutral flat network appliance icons |
| `OriginalSecurityIcon` | [`drawlib.icons.original_security`](08_icons.md#original-security) | Drawlib vendor-neutral flat security & IAM icons |
| `OriginalServerIcon` | [`drawlib.icons.original_server`](08_icons.md#original-server) | Drawlib vendor-neutral flat server & compute icons |
| `OriginalSocialIcon` | [`drawlib.icons.original_social`](08_icons.md#original-social) | Drawlib vendor-neutral flat social & messaging icons |
| `OriginalWorkspaceIcon` | [`drawlib.icons.original_workspace`](08_icons.md#original-workspace) | Drawlib vendor-neutral flat workspace & collaboration icons |
| `PhosphorIcon` | [`drawlib.icons.phosphor`](08_icons.md#phosphor) | 1,530+ tintable monochrome Phosphor UI vector font icons |
| `SecurityIcon` | [`drawlib.icons.security`](08_icons.md#security) | Official cybersecurity, IAM, and compliance brand icons |
| `ServerIcon` | [`drawlib.icons.server`](08_icons.md#server) | Linux/Windows OS, hypervisors, and server hardware icons |
| `SocialIcon` | [`drawlib.icons.social`](08_icons.md#social) | Social platforms, developer communities, and messaging icons |
| `WorkspaceIcon` | [`drawlib.icons.workspace`](08_icons.md#workspace) | Productivity suites, docs, and team collaboration SaaS icons |
