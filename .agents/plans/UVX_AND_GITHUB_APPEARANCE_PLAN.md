# Design & Implementation Plan: `uvx drawlib` Zero-Install Workflow & GitHub Repository Appearance

## 1. Objectives

1. **Zero-Install `uvx drawlib` & Polyglot Repository Support**:
   - Allow developers in **any directory or non-Python repository** (Go, Rust, TypeScript, Java, Terraform) as well as Python `uv` repositories without a direct `drawlib` dependency to scaffold and build documentation/diagrams immediately via `uvx drawlib init project ... && ./<target>_src/build.sh`.
   - Fix `DRAWLIB_CMD` resolution across all 16 scaffolded `.sh.template` scripts so `uv.lock` presence verifies `uv run drawlib --version &> /dev/null` before selecting `uv run drawlib`, and falls back automatically to `uvx drawlib` when `uvx` is installed.
   - Update `src/drawlib/_rules/agent_instruction.md` (and sync `.agents/rules/drawlib.md`) so AI coding agents know to invoke `uvx drawlib` in zero-install / polyglot repositories while staying under Windsurf's compact character budget (`< 10,600` chars).
   - Document `uvx drawlib`, `uv tool install drawlib`, and `uv add drawlib` workflows across `docs/docs_src/en/` and `docs/docs_src/ja/` with 100% EN/JA structural parity.

2. **GitHub Repository Appearance & Onboarding (`README.md`, `docs/README_JA.md`, `docs/README_PYPI.md`, `.github/`)**:
   - Upgrade root `README.md` with `<picture>` dark/light transparent brand logos (`docs/logo/logo_dark_transparent.png` / `docs/logo/logo_transparent.png`), status badges (PyPI, Python 3.11–3.13, Apache-2.0 License, Code Quality CI, Official Docs), language switch (`English | 日本語`), quick jump links, and an above-the-fold **"Try in 30 Seconds (`uvx drawlib`)"** section right below the Hero animation.
   - Create `docs/README_JA.md` as the complete Japanese README (preserving clean repository root alongside `docs/README_DEV.md` and `docs/README_PYPI.md`) with verified relative paths.
   - Synchronize `docs/README_PYPI.md` using absolute `https://www.drawlib.com/...` and `https://github.com/yuichi110/drawlib/...` URLs for PyPI rendering.
   - Add lightweight GitHub community files: `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/ISSUE_TEMPLATE/config.yml`, and `.github/CONTRIBUTING.md` (guiding contributors to `docs/README_DEV.md` and `./dcli`).

---

## 2. File-by-File Changes

### 2.1 Scaffolded Shell Templates (`src/drawlib/_templates/project/`)
Update `DRAWLIB_CMD` auto-detection in all 16 leaf shell templates (`images/build_image.sh.template`, `doc/{build_html,build_pdf,build_docx,build_markdown,build_image,serve}.sh.template`, `site/{build_html,build_markdown,build_image,serve}.sh.template`, `slide/{build_html,build_pdf,build_pptx,build_image,serve}.sh.template`):

```bash
if [ -z "${DRAWLIB_CMD:-}" ]; then
    if ( [ -f "uv.lock" ] || [ -f "../uv.lock" ] ) && command -v uv &> /dev/null && uv run drawlib --version &> /dev/null; then
        DRAWLIB_CMD="uv run drawlib"
    elif command -v drawlib &> /dev/null; then
        DRAWLIB_CMD="drawlib"
    elif python3 -m drawlib --version &> /dev/null; then
        DRAWLIB_CMD="python3 -m drawlib"
    elif python -m drawlib --version &> /dev/null; then
        DRAWLIB_CMD="python -m drawlib"
    elif command -v uv &> /dev/null && uv run drawlib --version &> /dev/null; then
        DRAWLIB_CMD="uv run drawlib"
    elif command -v uvx &> /dev/null; then
        DRAWLIB_CMD="uvx drawlib"
    else
        DRAWLIB_CMD="drawlib"
    fi
fi
```

### 2.2 Embedded Agent Instructions & Unit Tests
- `src/drawlib/_rules/agent_instruction.md` & `.agents/rules/drawlib.md`: Add concise CLI invocation guidance (`uv run drawlib` in Python `uv` projects, `uvx drawlib` in zero-install / non-Python repos, or `drawlib` when installed globally).
- `tests/drawlib/cli/test_cli_init.py`: Add unit test verifying `uvx drawlib` fallback and `uv run drawlib --version` guard across all scaffolded project types (`images`, `doc`, `site`, `slide`).

### 2.3 Official Documentation (`docs/docs_src/en/` & `docs/docs_src/ja/`)
- `01_getting_started/installation.md` (EN & JA):
  - Update Hero `ChevronProcess` Step 1 description to `"uvx drawlib\nuv add / pip"` and visually inspect with `-g`.
  - Expand Section 1 (`Using uv & Zero-Install uvx (Recommended)`) to cover `uvx drawlib` (zero-install & polyglot repos), `uv add drawlib` (Python project dependency), and `uv tool install drawlib` (persistent global CLI).
- `01_getting_started/quick_start.md` (EN & JA):
  - Show `uvx drawlib init project images` alongside `uv run drawlib init project images` in the Project-First callout.
- `10_ai_agents_and_advanced/ai_agent_instructions.md` (EN & JA):
  - Note `uvx drawlib init agent ...` for polyglot / non-Python repositories in Section 2.

### 2.4 Repository READMEs & GitHub Community Standards
- `README.md`: Dark/light `<picture>` logo header, badges, `English | 日本語` switcher, quick navigation links, Hero animation, above-the-fold `## Try in 30 Seconds (Zero Install with uvx)`, updated `[seo]` mention, and `uvx` CLI tips.
- `docs/README_JA.md`: Complete Japanese translation of `README.md` with relative links adjusted for `docs/`.
- `docs/README_PYPI.md`: PyPI-ready counterpart using absolute `https://www.drawlib.com/...` and GitHub URLs.
- `.github/ISSUE_TEMPLATE/{bug_report.yml,feature_request.yml,config.yml}` & `.github/CONTRIBUTING.md`: Clean community templates and contributor entry point.

---

## Verification Plan

### Functional, Static Analysis & Visual Checks
- Run `./dcli code-check all` (Ruff lint/format, `ty` type check, docstring check).
- Run `./dcli test target tests/drawlib/cli/test_cli_init.py --no-cov`, `test_cli_init_agent.py`, and `test_cli_rules.py`.
- Visually inspect updated `installation_setup_workflow.png` with `-g` (`view_file`) for text sizing (`>= 10.0pt`) and margin balance.
- Build and check official docs via `./dcli docs build site --no-clean && ./dcli docs serve site --check`.
- Validate all relative file/image links in `README.md`, `docs/README_JA.md`, and `.github/CONTRIBUTING.md`.

### Automated Security Check
- **Security Considerations (Shell Templates, Static HTML/Markdown, Local Server)**:
  - All `.sh.template` commands use hardcoded binary strings (`uv run drawlib`, `drawlib`, `python3 -m drawlib`, `uvx drawlib`) without evaluating untrusted external input, preventing command injection.
  - No secrets, credentials, authentication cookies, databases, or file upload endpoints are introduced (static Markdown/YAML templates and CLI scripts only).
  - Local preview checks (`./dcli docs serve site --check` / `serve.sh`) bind strictly to `localhost` / `127.0.0.1` (`http://localhost:8000`), never `0.0.0.0`.
- **Security Scanner**: Run a scan on all newly created files to identify common vulnerabilities (e.g., XSS, SQL injection) using `run-security-scanner` if the SecureCoder extension API is active. If findings are detected, auto-apply the fix and document the results.
- **Security Audit**: Audit the new files for design-level security issues (command execution safety, link/HTML attribute quoting, absence of secrets). Document findings and remediations using `generate-security-audit-report` when scanner findings apply.
