# Chapter 3: Drawlib Architecture and Capabilities

Drawlib is an integrated platform for Illustrated Documentation as Code. It unifies document building with a 4-layer drawing architecture, ranging from geometric primitives to full system topologies.

## 3.1 Four Component Layers

| Layer | Primary Modules | Description & Use Cases |
| :--- | :--- | :--- |
| **1. Primitives** | `drawlib.shapes`, `lines`, `text`, `icons` | Rectangles, circles, wedges, polygons, arrows, text, and Phosphor/GCP vector icons |
| **2. SmartArts** | `drawlib.smartarts` | Sequential chevrons, comparison tables, radial mindmaps, organizational trees, and callouts |
| **3. Charts** | `drawlib.charts` | Gantt schedules, bar charts, time-series line/area plots, pie charts, and radar charts |
| **4. Diagrams** | `drawlib.diagrams` | Cloud VPC architectures, workflow flowcharts, sequence diagrams, ER diagrams, and UML classes |

## 3.2 Unified Design System and Semantic Colors

With Drawlib, you never waste time tweaking arbitrary RGB hex codes. It provides a cohesive **6-role semantic color palette**:

- **`Styles.primary`**: Core system nodes and primary paths (Blue)
- **`Styles.secondary`**: External entities, user actors, and clients (Slate / Indigo)
- **`Styles.accent`**: Highlighted features and auxiliary components (Amber / Teal)
- **`Styles.muted`**: Boundary containers, structural grids, and subtle annotations (Light Gray)
- **`Styles.success` / `Styles.warning` / `Styles.danger`**: Operational statuses, alerts, and errors

Every color role includes variants such as `_flat` (solid fill), `_outline` (bordered), `_bold` (thick line), and `_dashed` (dashed border).

## 3.3 Typography and Multilingual Support

Drawlib provides first-class typography out of the box:
- **HTML / PDF Output**: Automatic font stacks featuring Google Sans, Inter, Roboto, and Noto Sans.
- **Canvas Rendering**: Universal font loaders prevent missing glyphs and broken character boxes across platforms.
