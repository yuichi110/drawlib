# Drawlib Documentation Site Project

This is a multi-page documentation website project created with [Drawlib](https://github.com/yuichi110/drawlib).

## 1. Project Structure

- `docs_src/`: Source Markdown files with embedded Drawlib illustrations (**Source of Truth**).
  - `index.md`: Mandatory root landing page.
  - `navbar.md`: Mandatory sidebar navigation menu definition.
  - `architecture/index.md`: Architecture chapter.
  - `workflow/index.md`: Workflow chapter.
- `docs_config.py`: Global configuration script for Drawlib illustrations (themes, canvas defaults, fonts).
- `docs_build.sh`: Shell script to compile all documents into Markdown and a responsive static HTML site.
- `docs/`: Generated Markdown site for repository browsing (**Never edit directly!**).
- `docs_html/`: Generated static HTML website with sidebar navigation (**Never edit directly!**).

## 2. Navigation Bar (`navbar.md`) Rules & Syntax

The sidebar navigation for the HTML site is defined by `docs_src/navbar.md`.

### Syntax Conventions:

1. **Site Brand Name (`# H1`)**:
   The first `# Heading 1` sets the site title displayed at the top of the sidebar.
   ```markdown
   # Documentation Site
   ```

2. **Categorized Sections (`## H2`)**:
   `## Heading 2` defines prominent section group headings (e.g. `## Topics`, `## System Design`).
   Bullet items placed before any `##` heading become top-level ungrouped navigation links.

3. **Page Links (`- [Title](path)`)**:
   Use standard Markdown bullet links relative to `navbar.md`:
   ```markdown
   # Documentation Site

   - [Overview](index.md)

   ## Topics
   - [Architecture](architecture/index.md)
   - [Workflow](workflow/index.md)
   ```

4. **Anchor & External Links**:
   - In-page anchors: `- [Component Details](architecture/index.md#components)`
   - External links: `- [GitHub](https://github.com/example/repo)` (automatically opens in a new tab with `target="_blank"`).

5. **Build-Time Link Validation**:
   Drawlib validates every local link in `navbar.md` during the build.
   If a linked file does not exist, the build immediately aborts with an informative error detailing the exact file path and line number, preventing broken navigation links.

### How to Add a New Page:
1. Create your Markdown document under `docs_src/` (e.g. `docs_src/guides/deployment.md`).
2. Add a corresponding link under the desired section in `docs_src/navbar.md`:
   ```markdown
   ## Guides
   - [Deployment](guides/deployment.md)
   ```
3. Run `./docs_build.sh` to compile the updated site.

## 3. Building the Site

Run the automated build script:

```bash
./docs_build.sh
```

Or build manually via the CLI:

```bash
# Build rendered Markdown for GitHub browsing:
drawlib build markdown docs_src/ -o docs/ -c docs_config.py

# Build responsive static HTML website with sidebar:
drawlib build html docs_src/ -o docs_html/ -c docs_config.py --css google
```

## 4. Previewing & Link Verification Locally

Start a local development server with built-in asset and broken-link checking:

```bash
drawlib serve docs_html/
```

To run link and asset verification only without launching the web server:

```bash
drawlib serve docs_html/ --check
```

## 5. Rapid Illustration Development

When tweaking an individual illustration, avoid rebuilding the entire site. Use `drawlib export` to verify the specific diagram rapidly:

```bash
# Export block 1 with coordinate grid overlay:
drawlib export docs_src/architecture/index.md 1 -g -o scratch/test.png
```

For more documentation and CLI guidelines, run:
```bash
drawlib rules show docs_build
```
