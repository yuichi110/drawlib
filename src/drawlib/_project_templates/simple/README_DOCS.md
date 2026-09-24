# Drawlib Simple Project

This is a single-document Drawlib project.

## Project Structure

- `docs_src/doc.md`: Source Markdown file containing embedded Drawlib code blocks.
- `docs_config.py`: Global configuration script for Drawlib illustrations.
- `docs_build.sh`: Shell script to compile Markdown and HTML documents.
- `docs/`: Generated Markdown and image assets (created on build).
- `docs_html/`: Generated HTML and image assets (created on build).

## Building Documents

Run the build script:

```bash
./docs_build.sh
```

Or build manually via the CLI:

```bash
drawlib build markdown docs_src/doc.md -o docs/doc.md -c docs_config.py
drawlib build html docs_src/doc.md -o docs_html/doc.html -c docs_config.py
```
