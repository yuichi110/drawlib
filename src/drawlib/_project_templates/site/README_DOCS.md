# Drawlib Documentation Site Project

This is a multi-page documentation website project created with Drawlib.

## Project Structure

- `docs_src/`: Source Markdown files with embedded Drawlib illustrations.
  - `index.md`: Main landing page.
  - `architecture.md`: Architecture chapter.
  - `workflow.md`: Workflow chapter.
- `docs_config.py`: Global configuration script for Drawlib illustrations.
- `docs_build.sh`: Shell script to compile all documents into Markdown and a responsive static HTML site.
- `docs/`: Generated Markdown site for repository browsing.
- `docs_html/`: Generated static HTML website with sidebar navigation.

## Building the Site

Run the build script:

```bash
./docs_build.sh
```

Or build manually via the CLI:

```bash
drawlib build markdown docs_src/ -o docs/ -c docs_config.py
drawlib build html docs_src/ -o docs_html/ -c docs_config.py
```

## Previewing Locally

You can preview the built HTML website using `drawlib serve`:

```bash
drawlib serve docs_html/
```
