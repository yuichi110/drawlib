---
layout: split-right
ratio: "4:6"
header: "Modular SmartArts"
footer: "Drawlib: Illustration as Code"
paginate: true
---

# Extensible Presentation Components

Drawlib bridges the gap between pure diagrams and structured presentation components:

- **Built-in SmartArts**:
  - `curved_agenda`: Visual agenda with curved arc and numbered topic pills
  - `timeline`: Linear chronological milestones and event sequences
  - `chevron_process`: Multi-stage execution flows
- **Custom Project Components**:
  - Place Python classes into `_slide_templates/*.py`
  - Subclass `SmartArtComponent` and implement `render(box, content, output_file)`
  - Call directly from Markdown with ````smartart:<name> slot:<slot> file:<out.svg>````

```smartart:custom_kpi slot:right file:kpi_metrics.svg
99.99% | System Availability | Tier-1 SLA production target
1.2s | Fast Build Time | Sub-second SQLite cache hit
100% | Verified Coverage | 962 / 962 unit and integration tests passing
```
