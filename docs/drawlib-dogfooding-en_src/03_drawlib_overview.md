# Chapter 3: Drawlib Architecture and Capabilities

Drawlib is an integrated platform for Illustrated Documentation as Code. In addition to its document compilation pipeline, it provides a 6-layer architecture spanning geometric primitives, system topology design, and presentation/animation generation.

## 3.1 Drawing & Documentation Component Layers

| Layer | Primary Modules | Description & Use Cases |
| :--- | :--- | :--- |
| **1. Primitives** | `drawlib.shapes`, `lines`, `text`, `icons`, `images` | **43** geometric shapes, polyline/curved/block arrows, rich typography, and Phosphor / FontAwesome / official GCP icons |
| **2. SmartArts** | `drawlib.smartarts` | Process chevrons, data tables (`Table`), offline world & Japan maps (`GeoMap`), syntax-highlighted code cards (`SourceCode`), mindmaps (`MindMapNode`), hierarchy trees (`TreeNode`), cycles (`Cycle`), pyramids, and grids |
| **3. Charts** | `drawlib.charts` | Gantt schedules, bar charts, line & area charts, pie & donut charts, radar charts, and scatter/bubble plots (with shared axes, log scale, and legends) |
| **4. Diagrams & Graphs** | `drawlib.diagrams`, `drawlib.graph` | Cloud architectures, flowcharts, sequence diagrams, ER diagrams, UML class diagrams, state machines, and 5 pure-Python auto-layout solvers (`get_layout()`) |
| **5. Presentation & Animation** | `drawlib.slide`, `drawlib.anim` | 16:9 presentation stages (`::: block` / `::: note`, Presenter View), multi-frame APNG & Animated WebP generation |
| **6. Builder, CLI & Tools** | `drawlib.tools` (CLI: `drawlib`) | Multi-target HTML / PDF / Slide / Markdown / Image compilation, SQLite incremental build cache (`.drawlib/cache.db`), asset cache management (`drawlib cache`), and local verification server (`drawlib serve --check`) |

## 3.2 Unified Design System and Semantic Colors

With Drawlib, you never need to guess raw RGB values. It provides a cohesive **6-role semantic color palette**, **neutral baseline tokens**, and consistent naming conventions out of the box:

- **`Styles.Neutral` / `Styles.PrimaryNeutral` / `Styles.SecondaryNeutral`**: Calm neutral cards that form the structural foundation of diagrams (soft gray, blue-gray, and slate tones)
- **`Styles.Primary`**: Core system nodes and primary paths (Blue)
- **`Styles.Secondary`**: External systems, clients, and actors (Slate / Indigo)
- **`Styles.Accent`**: Highlighted services and focal callouts (Amber / Teal)
- **`Styles.Muted`**: Boundary containers, structural grids, and subtle annotations (Light Gray)
- **`Styles.Success` / `Styles.Danger`**: Healthy statuses (Green) and warnings, alerts, or error paths (Red)

Every color role includes standardized PascalCase design tokens such as `PrimaryFlat` (solid fill), `PrimaryOutline` (bordered), `PrimaryBold` (thick stroke), and `PrimaryDashed` (dashed border).

### The 50%+ Neutral Baseline Rule (Preventing Rainbow Diagrams)

Assigning saturated fills (`PrimaryFlat`, `AccentFlat`, `SuccessFlat`, etc.) to every box creates visually noisy "rainbow diagrams" where nothing stands out. To establish clear visual hierarchy, Drawlib enforces two core color principles:

- **Ground 50%+ of Nodes in Neutral Cards**: Use **`Styles.Neutral`**, **`Styles.PrimaryNeutral`**, and **`Styles.SecondaryNeutral`** for at least 50% of nodes to create a calm, readable structural baseline.
- **Reserve Saturated Fills for 1–2 Focal Points**: Use high-saturation fills like **`Styles.PrimaryFlat`** or **`Styles.AccentFlat`** strictly for 1–2 primary focal elements per diagram.

### Principles of Neutral Typography and Connectors

To maintain high contrast and clean readability across all diagrams:
- **Neutral Typography**: On light backgrounds and neutral cards, text defaults to **`Styles.Dark`** or **`Styles.DarkBold`**. Inside dark-filled shapes (`PrimaryFlat`), use **`Styles.WhiteBold`** or **`Styles.Light`**. Avoid coloring text (`Primary`, `Secondary`) without explicit semantic intent.
- **Neutral Connectors**: Standard workflow transitions and connectors should use **`Styles.DarkBold`**. Reserve colored arrows (`Styles.Primary`, `Styles.Danger`) for critical paths or error rollback loops that require deliberate emphasis.

## 3.3 Multilingual Typography and Full CJK Support

Drawlib provides first-class multilingual and CJK (Japanese, Chinese, Korean) typography out of the box. Initializing a project with `--lang ja` (or other language flags) automatically configures:
- **HTML / PDF Output**: Curated web and system font stacks (e.g., Inter, Roboto, Noto Sans JP, Hiragino Sans).
- **Canvas Rendering**: Automatic configuration of bundled open-source fonts (such as `drawlib.fonts.FontJapanese`) to prevent missing glyphs, tofu boxes, or cross-platform layout shifts.
