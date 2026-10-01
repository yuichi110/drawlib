# Site Project Guide (`drawlib init site`)

The `site` starter template builds a responsive multi-page technical documentation website with hierarchical sidebar navigation, mobile-responsive layout, syntax highlighting, and dual publishing to static HTML and GitHub-ready Markdown.

---

## 1. Project Initialization

Scaffold a documentation website using `drawlib init`:

```bash
# Create in a new subdirectory:
drawlib init site my_docs/

# With custom theme and language:
drawlib init site my_docs/ --style google --lang en
```

---

## 2. Directory Layout & Architecture

```text
my_docs/
├── docs_src/                  # [SOURCE OF TRUTH] Author Markdown content here
│   ├── index.md               # [MANDATORY] Root site landing page
│   ├── navbar.md              # [MANDATORY] Sidebar categories and navigation menu
│   ├── template.html          # [MANDATORY] Responsive HTML layout template
│   ├── style.css              # [MANDATORY] Site stylesheet
│   ├── config.py              # Global drawing settings
│   ├── build.sh               # Executable build script
│   ├── README.md              # Authoring instructions
│   ├── 01_architecture/       # Section directory
│   │   └── vpc.md
│   └── 02_services/           # Section directory
│       └── auth.md
├── docs/                      # [GENERATED] Markdown site for GitHub browsing
└── docs_html/                 # [GENERATED] Static HTML site ready for web hosting
```

---

## 3. Sidebar Navigation (`navbar.md`)

The sidebar navigation structure is governed entirely by `docs_src/navbar.md`:

```markdown
# Drawlib Documentation

- [Home](index.md)

## Core Infrastructure
- [VPC Architecture](01_architecture/vpc.md)
- [Storage Tier](01_architecture/storage.md)

## Microservices
- [Authentication Gateway](02_services/auth.md)
- [Payment Service](02_services/payments.md)

## External Resources
- [GitHub Repository](https://github.com/example/repo)
```

### Authoring Rules:
1. **Brand Header (`# Title`)**: The top level `# Heading 1` sets the brand title in the sidebar header.
2. **Category Groupings (`## Category`)**: Each `## Heading 2` defines a collapsible navigation category section.
3. **Internal Document Links**: Relative paths must point to existing Markdown files within `docs_src/`.
4. **External Links**: URLs beginning with `http://` or `https://` automatically open in a new tab (`target="_blank"`) with an external link indicator.
5. **Strict Build-Time Validation**: If any linked document does not exist, the build immediately aborts with an error indicating the file and line number.
6. **Active Page Tracking**: The currently viewed page is automatically highlighted (`.nav-item.active`) with dynamic relative path resolution.

---

## 4. Static Asset Synchronization

Any static assets placed in `docs_src/` (such as custom logos, sample data files, or images in `_assets/`) are recursively mirrored to `docs_html/` and `docs/`, preserving folder hierarchies.

---

## 5. Building & Local Preview

### Compile Site
```bash
./docs_src/build.sh
```

### Local Preview Server & Link Audit
Start the local development server to preview pages:

```bash
uv run drawlib serve docs_html/
```

Before deploying to production, run a headless pre-flight audit:

```bash
uv run drawlib serve docs_html/ --check
```
