# Drawlib Documentation Build Guidelines

Drawlib provides a built-in document builder engine that compiles Markdown documents containing embedded `drawlib` code blocks into responsive HTML documentation sites, GitHub-flavored Markdown, and headless vector PDFs.

---

## 1. Project Scaffolding (`drawlib init`)

> **Important**: Do **NOT** create documentation projects from scratch manually.  
> Always use `drawlib init` to scaffold the project structure, configuration, and build scripts.

```bash
# List available starter templates:
drawlib init --list

# Scaffold a multi-page documentation site directly in current project/repository:
drawlib init site --here

# Scaffold a multi-page documentation site in a new directory:
drawlib init site my_site/

# Scaffold a single-page document project:
drawlib init simple my_doc/

# Scaffold a multi-chapter PDF report project:
drawlib init pdf my_report/
```

Options:
- `--here`: Initialize directly into the current working directory without creating a subfolder.
- `--force`: Overwrite existing files if directory is not empty.

---

## 2. Directory Structure & Lifecycle Rules

A standard Drawlib documentation project (`site` template) follows this directory layout:

```text
my_project/
├── docs_src/                  # [SOURCE OF TRUTH] Edit ONLY files here!
│   ├── index.md               # [MANDATORY] Root landing page
│   ├── navbar.md              # [MANDATORY] Sidebar navigation menu definition
│   ├── architecture/          # Topic / chapter subdirectories
│   │   └── index.md
│   └── workflow/
│       └── index.md
├── docs_config.py             # Global drawing configuration script
├── docs_build.sh              # Unified build automation script
├── docs/                      # [GENERATED] Markdown site for GitHub browsing (NEVER EDIT DIRECTLY!)
└── docs_html/                 # [GENERATED] Static HTML site with sidebar (NEVER EDIT DIRECTLY!)
```

### Golden Rule of Documentation
- **Edit exclusively under `docs_src/`**: Never manually modify generated files in `docs/` or `docs_html/`.
- **Root requirements for directory HTML builds**:
  - `docs_src/index.md` is **mandatory**.
  - `docs_src/navbar.md` is **mandatory**.
  - Subdirectories (e.g. `architecture/`, `workflow/`) do not require their own `navbar.md`.

---

## 3. Navigation Bar (`navbar.md`) Authoring Rules

The sidebar menu for multi-page sites is defined by `docs_src/navbar.md`:

```markdown
# My Documentation Site

- [Welcome](index.md)

## System Architecture
- [Component Overview](architecture/index.md)
- [Execution Lifecycle](workflow/index.md)

## External Resources
- [GitHub Repository](https://github.com/example/repo)
```

### Syntax & Behavior:
1. **Site Title (Brand Name)**:
   - The first `# Heading 1` (e.g. `# My Documentation Site`) is extracted as the site title and rendered in the top-left sidebar brand header.
2. **Category Headings**:
   - `## Heading 2` defines grouped category headers (e.g. `## System Architecture`).
   - Bullets placed before any `##` heading become top-level ungrouped navigation items.
3. **Links**:
   - Bullet items `- [Title](path/to/file.md)` link to documentation files relative to `navbar.md`.
   - Anchors are supported: `- [Section](path.md#section-id)`.
   - External URLs (`http://`, `https://`) automatically open in a new tab with `target="_blank"`.
4. **Strict Build Validation**:
   - Every local Markdown link in `navbar.md` is validated at build time.
   - If any target file does not exist, the build immediately aborts with an informative error message indicating the file path and line number.
5. **Active Page Tracking**:
   - The current page is automatically detected, highlighted (`.nav-item.active`), and relative paths are dynamically computed for nested subdirectories.

---

## 4. Build Commands (`drawlib build`, `docs_build.sh`)

### Automated Build Script:
```bash
./docs_build.sh
```
This executes both Markdown and HTML compilations using the detected Python / drawlib runtime.

### Direct CLI Commands:
```bash
# 1. Compile entire directory to static HTML site with sidebar:
drawlib build html docs_src/ -o docs_html/ -c docs_config.py --css google

# 2. Compile directory to rendered Markdown for GitHub:
drawlib build markdown docs_src/ -o docs/ -c docs_config.py

# 3. Compile single document to vector PDF:
drawlib build pdf docs_src/index.md -o output.pdf -c docs_config.py --css google
```

Key Options:
- `-o`, `--output <path>`: Destination directory or file path.
- `-c`, `--config <path>`: Python configuration script executed before drawing code blocks (e.g. `docs_config.py`).
- `--css <name|path>`: Built-in CSS theme (`google`, `google-dark`, `google-auto`, `default`, `default-dark`, `default-auto`, `github`, `minimal`, `monochrome`) or custom CSS path.
- `--no-cache`: Force clean diagram generation ignoring the SQLite cache.

---

## 5. Local Preview & Link Verification (`drawlib serve`)

Preview the generated static HTML site with built-in asset and broken-link checking:

```bash
# Start local development server (default port 8000, opens browser):
drawlib serve docs_html/

# Start server on custom port without opening browser:
drawlib serve docs_html/ -p 8080 --no-browser

# Run link and image asset verification only and exit immediately:
drawlib serve docs_html/ --check

# Start server skipping pre-flight checks:
drawlib serve docs_html/ --skip-check
```

---

## 6. Embedded Drawing Blocks (````drawlib````)

Embed Python drawing code inside Markdown using the ````drawlib```` code fence:

````markdown
```drawlib 600px center caption:"System Architecture"
config(width=100, height=50)

rectangle((25, 25), width=30, height=20, style=styles.blue_flat, text="Client", textstyle=styles.white_bold)
rectangle((75, 25), width=30, height=20, style=styles.green_flat, text="Server", textstyle=styles.white_bold)
line((40, 25), (60, 25), arrowhead="->", style=styles.bold)
```
````

### Header Options:
- **Code Visibility**:
  - `hide-code` *(default)*: Renders illustration only.
  - `show-code`: Displays Python source followed by the rendered image.
  - `fold-code`: Displays image followed by a collapsed `<details>` dropdown with code.
- **Dimensions**: `500px`, `100%`, `w:600px`, `h:300px`.
- **Alignment**: `center`, `left`, `right`.
- **Caption**: `caption:"Description"` (displayed in `<figcaption>`).
- **Filename**: `file:custom_name.png` (explicit image filename).

### Global Namespace & Isolation:
- Authors do not need boilerplate imports. `canvas`, `shapes`, `lines`, `text`, `icons`, `smartarts`, `charts`, `colors` are pre-injected into globals.
- The canvas is automatically cleared and reset between code blocks.

---

## 7. Recommended Agent Development Workflow

When modifying or authoring documentation:
1. **Never rebuild the full site for single diagram adjustments**:
   - Export and verify individual diagrams rapidly without browser/GUI popups:
     ```bash
     drawlib export docs_src/architecture/index.md 1 -o scratch/test.png
     ```
   - Check with coordinate grid overlay if alignment needs tuning:
     ```bash
     drawlib export docs_src/architecture/index.md 1 -g -o scratch/test_grid.png
     ```
2. **Once illustration code is verified**:
   - Run the full site build:
     ```bash
     ./docs_build.sh
     ```
3. **Verify links and site health**:
   - Run:
     ```bash
     drawlib serve docs_html/ --check
     ```
