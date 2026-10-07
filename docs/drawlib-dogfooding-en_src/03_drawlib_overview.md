# Chapter 3: Drawlib Architecture and Capabilities

Drawlib is an integrated platform for Illustrated Documentation as Code. It unifies document building with a 4-layer drawing architecture, ranging from geometric primitives to full system topologies.

## 3.1 Drawing & Documentation Component Layers

| Layer | Primary Modules | Description & Use Cases |
| :--- | :--- | :--- |
| **1. Primitives** | `drawlib.shapes`, `lines`, `text`, `icons`, `images` | 23 geometric shapes, orthogonal & curved connectors, rich typography, and Phosphor/FontAwesome/GCP icons |
| **2. SmartArts** | `drawlib.smartarts` | Sequential chevrons, comparison tables, radial mindmaps, organizational trees, and circular cycle loops |
| **3. Charts** | `drawlib.charts` | Gantt schedules, bar charts, time-series line/area plots, pie charts, scatter plots, and radar charts |
| **4. Diagrams & Graphs** | `drawlib.diagrams`, `drawlib.graph` | Cloud VPC architectures, workflow flowcharts, sequence diagrams, ER diagrams, UML classes, and Pure-Python auto-layout solvers |
| **5. Presentation & Animation** | `drawlib.slide`, `drawlib.anim` | 16:9 presentation slide decks, native APNG & Animated WebP generation |
| **6. Builder & CLI** | `drawlib._builder`, `drawlib._cli` | HTML / PDF / Markdown multi-target compilation, live-reload preview server |

## 3.2 Unified Design System and Semantic Colors

With Drawlib, you never waste time tweaking arbitrary RGB hex codes. It provides a cohesive **6-role semantic color palette**:

- **`Styles.Primary`**: Core system nodes and primary paths (Blue)
- **`Styles.Secondary`**: External entities, user actors, and clients (Slate / Indigo)
- **`Styles.Accent`**: Highlighted features and auxiliary components (Amber / Teal)
- **`Styles.Muted`**: Boundary containers, structural grids, and subtle annotations (Light Gray)
- **`Styles.Success` / `Styles.Danger`**: Operational statuses, health checks, alerts, and errors

Every color role includes standardized PascalCase design tokens such as `PrimaryFlat` (solid fill), `PrimaryOutline` (bordered), `PrimaryBold` (thick line), and `PrimaryDashed` (dashed border).

### Principles of Neutral Typography and Connectors

To maintain high contrast, professional aesthetics, and visual clarity:
- **Neutral Typography**: On light backgrounds, text MUST default to `Styles.Dark` or `Styles.DarkBold`. Inside dark-filled shapes, use `Styles.WhiteBold` or `Styles.Light`. Never apply colors (`Primary`, `Secondary`, `Accent`) to text without explicit semantic necessity.
- **Neutral Connectors**: Standard workflow lines, arrows, and sequential transitions default to `Styles.DarkBold`. Reserve accent and status colors (`Styles.Primary`, `Styles.Accent`, `Styles.Danger`) strictly for critical flow paths, active connections, or error loops.

## 3.3 Typography and Multilingual Support

Drawlib provides first-class typography out of the box:
- **HTML / PDF Output**: Automatic font stacks featuring Google Sans, Inter, Roboto, and Noto Sans.
- **Canvas Rendering**: Universal font loaders prevent missing glyphs and broken character boxes across platforms.
