# Drawlib Slide Architecture Plan 2.0 (SLIDE_PLAN2.md)

**A Pure Canvas-Based 1920×1080 Stage Architecture with Coordinated Design Tokens**

---

## 1. Executive Summary & Design Philosophy

### 1.1. The Evolution from HTML Layouts to Canvas Architecture
In the initial exploration ([SLIDE_PLAN.md](SLIDE_PLAN.md)), slide layouts borrowed concepts from traditional web slide frameworks (Marp, Slidev), dividing slides into rigid Flexbox/Grid slots such as `slot: left` and `slot: right`.

However, `drawlib`'s core philosophy is **"Illustration as Code"** — built on mathematically precise, deterministic Cartesian coordinates. Rigid CSS slots directly conflicted with this philosophy:
- Placing multiple diagrams on one slide required hacking CSS grids or awkward sub-containers.
- Adjusting a diagram's position by 20px or shifting a text block to avoid overlap was frustrating.
- Users were forced to fight against HTML layout abstractions instead of leveraging Drawlib's spatial precision.

**Slide Architecture 2.0** discards rigid slot divisions and adopts a **Pure Canvas-Based 1920×1080 Stage Model**:
1. **The Slide is a 1920×1080 Canvas**: Every slide is rendered onto a fixed 1920×1080 virtual stage scaled responsively by CSS `transform: scale()`.
2. **Master Frame for Consistency**: Header, footer, typography, and color tokens are defined globally in `slide.css` and `styles.py` to ensure visual unity across all slides.
3. **Absolute Freedom for Content Blocks**: Text containers, Drawlib diagrams, SmartArts, and animations can all be positioned freely on stage using `(x, y)` and `(w, h)` bounding boxes.
4. **Container Syntax & Frontmatter**: Scoped text containers (`::: box (x, y) (w, h) ... :::`) and slide frontmatter (`offset_y`, `font_size`, `compact`) provide fine-tuning without intercepting HTML comments, which remain unencumbered for user notes.
5. **Project-Local `slide.css`**: Scaffolding deploys `slide_src/slide.css` directly into the user's project, matching the customization model of `docs_src/style.css` in HTML/PDF projects.

---

## 2. The Balance: Master Frame + Free Canvas Blocks

```text
┌────────────────────────────────────────────────────────────────────────────┐ 1920 x 1080
│ [Master Frame: Consistency] Header Bar (Title, Category, Breadcrumb)       │ Y: 0 ~ 120
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│ [Canvas Working Stage: Freedom (X: 80~1840, Y: 140~1000)]                  │
│                                                                            │
│  ┌─────────────────────────┐   ┌────────────────────────────────────────┐  │
│  │ Text Block              │   │ Drawlib Diagram 1                      │  │
│  │ (80, 140) (740, 840)    │   │ (880, 140) (960, 480)                  │  │
│  │                         │   │                                        │  │
│  │ # Heading               │   ├───────────────────┬────────────────────┤  │
│  │ - **Point 1**: Body text│   │ SmartArt 2        │ Animated WebP 3    │  │
│  │ - **Point 2**: Body text│   │ (880, 660)        │ (1380, 660)        │  │
│  │                         │   │ (460, 320)        │ (460, 320)         │  │
│  └─────────────────────────┘   └───────────────────┴────────────────────┘  │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ [Master Frame: Consistency] Footer Bar (Confidentiality, Page Number)      │ Y: 1020 ~ 1080
└────────────────────────────────────────────────────────────────────────────┘
```

### 2.1. Layer 1: Master Frame (Ensuring Uniformity & Brand Identity)
Defined and synchronized across two files:
- **`slide_src/styles.py`**: Python design tokens (`GoogleColors`, `GoogleStyles`, custom palettes).
- **`slide_src/slide.css`**: HTML design tokens (root CSS variables, header/footer styling, typography hierarchy).

| Attribute | Default Google Theme Specification |
| :--- | :--- |
| **Stage Geometry** | Fixed aspect ratio `16:9` (`1920px × 1080px`) |
| **Typography** | `Google Sans` (Titles), `Inter` / `Roboto` (Body), `JetBrains Mono` (Code) |
| **Color Tokens** | `--slide-primary: #1a73e8;`, `--slide-bg: #ffffff;`, `--slide-text: #202124;` |
| **Header Area** | Height 50px, top margin 60px, left margin 90px |
| **Footer Area** | Height 40px, bottom margin 40px, page counter format: `current / total` |

### 2.2. Layer 2: Canvas Working Stage (Delivering Total Spatial Freedom)
Within the working area (or across the entire 1920×1080 stage):
- Multiple diagrams can coexist side-by-side or stacked vertically.
- Drawlib vector graphics, SmartArts, and animated WebPs are placed at deterministic coordinates.
- Overlapping, layering, and precise alignment are fully supported.

---

## 3. Syntax & Directive Specification

### 3.1. Block Coordinate Specification (`drawlib` and `smartart`)
Drawlib blocks and SmartArts support concise, readable bounding box coordinates:

```text
```drawlib (x, y) (width, height) file:<name>.<ext> [options]
```

#### Syntax Examples:
```markdown
<!-- Standard explicit coordinates -->
```drawlib (880, 140) (960, 480) file:arch.svg
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node
...
```

<!-- Multi-panel layout on a single slide -->
```smartart:custom_kpi (880, 660) (460, 320) file:kpi.svg
99.99% | System Availability | Tier-1 SLA
```

```drawlib (1380, 660) (460, 320) file:pipeline.webp
anim = Animation(fps=1.0)
...
```
```

#### Smart Defaults (Zero-Config Fallback):
If coordinates `(x, y) (w, h)` are omitted:
- **First Drawlib block**: Automatically defaults to right stage area `(880, 140) (960, 840)`.
- **Text content**: Automatically occupies left stage area `(80, 140) (740, 840)`.
- This ensures simple 1-text + 1-image slides require zero coordinate math.

---

### 3.2. Container Syntax (`::: box ... :::`) & Slide-Level Frontmatter
Instead of intercepting HTML comments (which remain reserved for standard user notes and draft memos: `<!-- TODO: update this -->`), Drawlib uses structured **Container Syntax (`::: box ... :::`)** for scoped block positioning, paired with **Frontmatter** for slide-wide defaults.

#### 1. Slide-Level Frontmatter (Whole-Slide Defaults)
When the entire slide needs adjustments (font scaling, vertical nudge, or compact layout):
```yaml
---
header: "Cloud Architecture"
footer: "Drawlib Technical Presentation"
offset_y: -20px      # Shifts slide content vertically by -20px
font_size: 21px      # Base font size override for slide body
compact: true        # Compact preset (85% font size, tighter line-height)
---
```

#### 2. Container Syntax for Text Blocks (`::: box ... :::`)
When dividing a slide into multiple text blocks or positioning text at exact coordinates on the 1920×1080 stage:

```text
::: box (x, y) (width, height) [options]
... markdown content ...
:::
```

| Parameter / Option | Syntax | Effect |
| :--- | :--- | :--- |
| **Stage Coordinates** | `(x, y)` | Top-left stage coordinates in pixels (e.g. `(80, 140)`). |
| **Dimensions** | `(w, h)` | Width and height bounding box in pixels (e.g. `(740, 840)`). |
| **Font Size** | `font: 22px` or `font-size: 22px` | Overrides font size within this specific container. |
| **Compact Mode** | `compact` | Enables tighter line-height and margin density. |
| **Alignment** | `center`, `left`, `right` | Text alignment within the box. |
| **Custom Style** | `style: "..."` | Inline CSS properties (e.g. `style: "background: rgba(0,0,0,0.03); border-radius: 8px;"`). |

#### Multi-Box Slide Example:
```markdown
---
header: "Microservices Architecture"
---

::: box (80, 140) (740, 480) font:21px
# Ingress & Service Mesh
- **API Gateway**: TLS termination and OAuth2 validation
- **K8s Pods**: Multi-zone auto-scaled worker nodes
:::

::: box (80, 660) (740, 320) compact
> **Operational Note**:
> Regional failover is orchestrated automatically by DNS routing.
:::

```drawlib (860, 140) (980, 840) file:arch.svg
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node
...
```
```

#### 3. Preservation of HTML Comments (`<!-- ... -->`)
HTML comments `<!-- ... -->` remain 100% standard HTML/Markdown comments:
- Drawlib does NOT parse or repurpose them.
- Users and developers can freely write `<!-- TODO: verify SLA numbers -->` or `<!-- Draft note -->` without any side effects on rendering.

---

### 3.3. Canvas Mode & Overlapping Layouts

#### 1. Full Canvas Mode (`layout: canvas` - Header/Footer なしの一枚絵)
スライド全体を 1920×1080 の純粋なキャンバスとして使用し、インフォグラフィックや巨大な構成図、タイトルヒーローを描画するモードです。
Header, Footer, Padding がすべて自動的にゼロとなり、全画面がコードによる描画エリアになります。

```markdown
---
layout: canvas
---

```drawlib (0, 0) (1920, 1080) file:full_hero_diagram.svg
from drawlib.canvas import clear, setup, save
...
```
```

#### 2. Partial Overlap & Bleed (右側だけのはみ出し・オーバーラップ)
通常のスライド枠（Header / Footer あり）を維持しながらも、特定のダイアグラムだけを右端・上端までブリード（はみ出し）させたり、テキストボックスと重ね合わせることができます。

- 座標系は常に **スライド原点 (0, 0) を基準とした 1920×1080**。
- `(1000, 0) (920, 1080)` と指定すれば、ヘッダーの高さ制限を突き抜けて右半分の上端から下端まで一面にダイアグラムを配置可能。
- `z: N` (または `z-index: N`) を指定することで、レイヤーの前後関係（背景・前面・オーバーラップ）を完全に制御できます。

```markdown
---
header: "High Availability Architecture"
---

::: box (80, 200) (760, 600) z:10
# Active-Active Multi-Region
- 99.999% SLA across 3 regions
- Synchronous replication
:::

<!-- 右半分の上端(0)から下端(1080)まで突き抜けるブリード配置 -->
```drawlib (960, 0) (960, 1080) z:5 file:multi_region_map.svg
from drawlib.canvas import clear, setup, save
...
```
```

#### 3. Granular Header / Footer Control
通常スライドでも、必要に応じて個別に Header や Footer を消去して領域を拡張できます：
- `header: none` (または `header: false`): ヘッダーバーを非表示
- `footer: none` (または `paginate: false`): フッターバー・ページ番号を非表示

---

## 4. Design System & Project Scaffolding (`drawlib init slide`)

### 4.1. File Layout in User Project (`slide_src/`)
Following the proven pattern of `site`, `simple`, and `pdf` projects, `drawlib init slide` scaffolds a local, fully customizable `slide.css`:

```text
slide_src/
├── slide.css                        # ★ Project Presentation Stylesheet (Editable!)
├── styles.py                        # ★ Project Drawlib Drawing Styles (Editable!)
├── utils.py                         # Shared Python helper functions
├── _slide_templates/                # Project Custom SmartArt Components
│   └── custom_kpi.py                # Example custom component
├── 01_title.md                      # Slide 1 (Cover)
├── 02_agenda.md                     # Slide 2 (Curved Agenda SmartArt)
├── 03_architecture.md               # Slide 3 (Cloud Architecture Diagram)
├── build.sh                         # ./slide_src/build.sh
└── serve.sh                         # ./slide_src/serve.sh
```

### 4.2. Role Separation Between `slide.css` and `styles.py`

| Concern | Configured in `slide.css` | Configured in `styles.py` |
| :--- | :--- | :--- |
| **Typography** | Font families for headers, lists, code blocks | Font enums (`FontRoboto`, `FontSansSerif`) |
| **Colors** | `--slide-bg`, `--slide-text`, `--slide-header` | `Colors.Blue6`, `Colors.Gray1`, `Colors.White` |
| **Layout & Stage** | 1920×1080 dimensions, header/footer spacing | Canvas `setup(width=..., height=...)` |
| **Theme Presets** | Google Slides, Default Dark, Monochrome | `GoogleStyles`, `DefaultStyles`, `MonochromeStyles` |

---

## 5. Rendering Engine & Searchability Implementation

### 5.1. Inline SVG Vector Integration
- **Zero Opaque Boundaries**: In contrast to `<img src="*.svg">` which isolates content inside an opaque image sandbox, the slide compiler inlines SVG code directly:
  ```html
  <figure class="drawlib-image" data-slot="right">
    <svg class="slide-vector-graphic" viewBox="0 0 720 469" ...>
      <text x="256" y="230">API Gateway</text>
    </svg>
  </figure>
  ```
- **Browser DOM Integration**:
  - `Cmd + F` (Mac) and `Ctrl + F` (Windows/Linux) seamlessly find and highlight diagram text.
  - Text selection and copy/paste work natively.
  - Typography inherits system fonts without font loading latency.
- **Zero Drop-Shadows**:
  - Removed artificial `filter: drop-shadow(...)` from slide images so vector drawings integrate seamlessly with slide backgrounds.

### 5.2. Keyboard Handler Modifier Safety in `slide.js`
Keyboard navigation listeners must never intercept browser shortcuts:
```javascript
window.addEventListener('keydown', (e) => {
  // Never intercept browser commands (Cmd+F, Cmd+R, Ctrl+F, Ctrl+R, etc.)
  if (e.metaKey || e.ctrlKey || e.altKey) {
    return;
  }
  // Never intercept keys when typing inside input / textarea
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
    return;
  }
  ...
});
```

### 5.3. Icon Stability (No Font Tofu)
- Phosphor font icons require local TTF files that can display as tofu (`□`) on client machines lacking the font.
- For cloud architectures and system diagrams, **Google Cloud PNG Icons (`GcpIcon`)** or embedded vector paths are preferred:
  - Icons are embedded as self-contained base64 rasters inside the SVG.
  - 100% portable across macOS, Windows, Linux, iOS, and Android with zero missing glyphs.

---

## 6. Implementation Plan & Milestones

### Phase 1: Project Scaffolding & Theme File Deployment
- [ ] **`_builder/project_init.py`**: Update `_deploy_stylesheet()` to deploy `slide_src/slide.css` when `selected_type == "slide"`.
- [ ] **`_slide/compiler.py`**: Update `_deploy_slide_assets()` to prioritize `slide_src/slide.css` (and fallback to built-in template).
- [ ] Verify `uv run drawlib init slide -s google` deploys `slide_src/slide.css` and `slide_src/styles.py`.

### Phase 2: Compiler Support for `(x, y) (w, h)`, `z: N` & Container Syntax
- [ ] **`_builder/doc_builder/processor/options.py`**:
  - Enhance `parse_block_info()` to parse tuple shorthand `(x, y) (w, h)` in addition to `xy:(...)` and `size:(...)`.
  - Add `z_index` (`z: N` / `z-index: N`) option parsing to `DrawlibBlockOptions`.
- [ ] **`_slide/compiler.py`**:
  - Implement `_parse_container_blocks(markdown_text: str)` extracting `::: box (x, y) (w, h) [options] ... :::` into positioned `<div class="slide-text-box" style="position: absolute; left: ...px; top: ...px; width: ...px; height: ...px; z-index: ...;">`.
  - Implement frontmatter handlers for `offset_y`, `font_size`, `compact`.
  - Support multiple positioned `drawlib` and `smartart` blocks on a single slide without slot collision.
  - Implement `layout: canvas` (zero padding, no header/footer for full 1920×1080 canvas) and granular header/footer suppression (`header: none`, `footer: none`).

### Phase 3: Project Template Refactoring
- [ ] Update `src/drawlib/_project_templates/slide/`:
  - Include starter `slide.css` in template assets.
  - Update starter slides (`01_title.md`, `02_agenda.md`, `03_architecture.md`) to showcase `(x, y) (w, h)` positioning and `GcpIcon`.

### Phase 4: Quality & Test Suite Verification
- [ ] Add unit and integration tests in `tests/test_slide.py`:
  - Test `(x, y) (w, h)` parsing and absolute positioning HTML generation.
  - Test container syntax (`::: box (x, y) (w, h) [options] ... :::`) and slide-level frontmatter (`offset_y`, `font_size`, `compact`).
  - Test project-local `slide.css` discovery and deployment.
- [ ] Execute `./dcli check all` (Ruff, Ty type checker, docstrings).
- [ ] Execute `./dcli test all` (all 962+ pytest tests).

---

## 7. Architectural Decisions Log (ADR)

| Decision | Rationale | Alternatives Considered |
| :--- | :--- | :--- |
| **Pure Canvas Stage over Split Slots** | Unifies slide authoring with Drawlib's core Cartesian coordinate model; enables arbitrary multi-image placement. | Preserving `split-right` / `split-left` slots (too rigid for multi-panel diagrams). |
| **Container Syntax (`::: box ... :::`) over HTML Comments** | Clear scoping with balanced delimiters prevents unclosed tag bugs and AI hallucination; preserves `<!-- ... -->` exclusively for developer notes and draft memos. | HTML comments `<!-- box: ... -->` (prone to scope leakage and conflicts with normal notes), Raw HTML `<div style="...">` (cluttered). |
| **Project-local `slide.css`** | Matches `site` and `pdf` projects (`docs_src/style.css`); empowers developers to tweak typography and design tokens. | Global library-only CSS (rigid, requires hacking library source). |
| **Inline SVG for Searchability** | Enables native browser `Cmd + F` / `Ctrl + F` searching and mouse dragging inside diagrams. | `<img src="*.svg">` (isolated sandbox, unsearchable), `<object>` (separate frame). |
| **GcpIcon for Google Theme** | Embedded self-contained PNG icons avoid font missing / tofu boxes on external devices. | PhosphorIcon TTF (relies on client font installation or heavy TTF base64). |

