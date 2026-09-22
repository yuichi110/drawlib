# Charts Overview

`drawlib.charts` provides declarative, vector-grade charting capabilities for illustration and technical presentation.
Built completely on pure-Python drawing primitives, charts integrate seamlessly into documents, slides, and diagrams without external dependencies like matplotlib or seaborn.

---

## Available Chart Types

| Chart Type | Class | Description |
|---|---|---|
| **Bar Chart** | [`BarChart`](./bar.md) | Vertical and horizontal column/bar charts with grouped and stacked modes, customizable grid/ticks, and logarithmic scales. |

---

## Design Philosophy

1. **Object-Oriented Builder Pattern**: Create a chart object, add series, configure axes, and draw onto the canvas.
2. **Seamless Canvas Composition**: Place charts anywhere alongside other shapes, annotations, text, or architecture diagrams.
3. **Smart Automatic Layout**: Automatic legend placement, nice numbers tick generation, and category spacing.
4. **Fine-grained Customization**: Full control over axis ticks, gridlines, formatting, logarithmic scales, and color styling.
