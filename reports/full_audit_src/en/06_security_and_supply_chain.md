# 6. Deep Dive: Security, Supply Chain & API Surface

First-party Drawlib source code exhibits strong security fundamentals—zero SQL/command/XSS injection flaws, zero hardcoded source secrets, SHA-256 verified external asset downloads, and least-privilege `contents: read` CI workflows—while Trivy scanning (`76/100, Grade B`) isolated all `41` dependency CVEs to a single locked package (`pillow@12.3.0 -> 13.0.0`) alongside `3` root-user `Dockerfile` misconfigurations (`DS-0002`).

```drawlib align=center code=hide file=ch06_supply_chain_vuln_breakdown.png caption="Figure 6.1 — Trivy SCA, Container OS, IaC Misconfiguration, and Secret Scan Breakdown isolating all 41 dependency CVEs to pillow@12.3.0."
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.icons import phosphor
from drawlib.smartarts import KpiCards, Panel
from drawlib.styles import Styles

setup(width=170, height=84)

bar = BarChart(
    axis_line_style=Styles.Muted,
    categories=[
        "Source AST Secrets\n(424 Files)",
        "Container OS Layers\n(python:3.12-slim)",
        "Other 12 Direct Deps\n(pyproject.toml)",
        "Dockerfiles IaC\n(3x Dockerfile.*)",
        "pillow@12.3.0\n(uv.lock -> 13.0.0)",
    ],
    width=80.0,
    height=58.0,
    orientation="horizontal",
    bar_mode="stack",
    bar_width_ratio=0.62,
    bar_r=0.8,
    title="Trivy Security Findings by Target & Severity",
    title_style=Styles.DarkBold.patch(text_size=12.0),
    axis_text_style=Styles.Dark.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=9.8),
    value_format="{:.0f}",
)
bar.add_series("Critical (CVSS 9.8)", [0.0, 0.0, 0.0, 0.0, 5.0], style=Styles.DangerFlat)
bar.add_series("High", [0.0, 0.0, 0.0, 3.0, 23.0], style=Styles.WarningFlat)
bar.add_series("Medium / Low", [0.0, 0.0, 0.0, 3.0, 13.0], style=Styles.SecondaryNeutral)
bar.configure_x_axis(min_value=0.0, max_value=45.0, tick_step=10.0)
bar.draw(xy=(21.0, 7.0))
bar.draw_legend(
    xy=(23.0, 68.5),
    text_style=Styles.Dark.patch(text_size=10.0),
    orientation="horizontal",
    item_gap=5.5,
)

panel = Panel(
    "Supply-Chain & Secret Posture",
    style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.shield_check,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=8.8,
)
panel.draw((104.0, 6.0), width=61.0, height=72.0, align="bottom_left")
p_xy, p_w, p_h = panel.get_content_box((104.0, 6.0), width=61.0, height=72.0, padding=(2.6, 2.8))

kpis = KpiCards(
    style=Styles.White,
    metric_style=Styles.PrimaryBold.patch(text_size=12.8),
    text_style=Styles.DarkBold.patch(text_size=10.3),
    description_style=Styles.Muted.patch(text_size=9.6),
    accent_style=Styles.PrimaryFlat,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.30,
    spacing=2.5,
)
kpis.add(
    "41 -> 0",
    "Pillow 13.0.0 Upgrade",
    "5 Crit, 23 High, 13 Med (uv.lock)",
    metric_style=Styles.DangerBold.patch(text_size=12.8),
    accent_style=Styles.DangerFlat,
)
kpis.add(
    "0 CVEs",
    "12 Other Deps & OS",
    "SemVer floors + 0 OS layer CVEs",
    metric_style=Styles.SuccessBold.patch(text_size=12.8),
    accent_style=Styles.SuccessFlat,
)
kpis.add(
    "3 HIGH",
    "IaC DS-0002 Root User",
    "+ 3 LOW DS-0026 Dockerfile checks",
    metric_style=Styles.WarningBold.patch(text_size=12.8),
    accent_style=Styles.WarningFlat,
)
kpis.add(
    "0 in Git",
    "Source Secret Hygiene",
    "1 gitignored .env PyPI token",
    metric_style=Styles.PrimaryBold.patch(text_size=12.5),
    accent_style=Styles.PrimaryFlat,
)
kpis.draw(p_xy, width=p_w, height=p_h, columns=1)

save()
```

---

## 6.1 Dependency Vulnerability Analysis (`SEC-01`: `pillow@12.3.0 -> 13.0.0`)

Trivy v0.69.3 Software Composition Analysis (`SEC-01`) evaluated `pyproject.toml`, `uv.lock`, and container OS package metadata:
- **Single-Package Concentration (`41` App CVEs -> `0` after `pillow>=13.0.0`)**: Every single reported application vulnerability (`5 CRITICAL`, `23 HIGH`, `13 MEDIUM`, `0 LOW` in `app_vuln_counts`; `40` unique deduplicated advisory IDs) resides in **`pillow@12.3.0`** resolved in `uv.lock` (`pillow>=10.2` in `pyproject.toml`). All `41` findings share the exact same upstream remediation target: **`pillow 13.0.0`**.
- **Clean Adjacent Ecosystem (`0` CVEs Across 12 Sibling Packages & OS Layers)**: The remaining `12` direct runtime dependencies (`matplotlib>=3.8`, `numpy>=1.26`, `pydantic>=2.8`, `pygments>=2.18`, `markdown-it-py>=3.0`, `jinja2>=3.1`, `markupsafe>=2.1`, `typer>=0.12.0`, `rich>=13.0.0`, `playwright>=1.49.0`, `python-docx>=1.2.0`, `python-pptx>=1.0.2`) and container OS layers (`os_vuln_counts = 0`) recorded **zero vulnerabilities** and **zero unpinned range specifiers** (`app_vuln_unpinned_range_matches = 0`).
- **Practical Reachability in Drawlib**: Drawlib wraps `PIL.Image.open()` inside `Dimage` (`src/drawlib/_core/l3_images/_dimage.py`) and rasterizes Matplotlib figures to PNG/WEBP/PDF buffers. While trusted first-party SVG/PNG icons and Matplotlib RGBA buffers do not exercise exotic decoders (FlashPix, MSP, SPIDER, Ghostscript EPS), passing untrusted external raster files into `image()` or `Dimage()` could reach vulnerable native JPEG, TIFF, or bundled `libopenjp2 2.5.4` (`GHSA-78g4-xqwv-q3g8`) code paths. Running `uv lock --upgrade-package pillow` and bumping `pyproject.toml` to `pillow>=13.0.0` (`P0`) eliminates the entire CVE surface in one atomic change.

### Deduplicated Critical & High `pillow@12.3.0` Advisories (`uv.lock`, Fixed in `13.0.0`)

| Advisory ID | Severity | CVSS | Installed -> Fixed | Affected Native Subsystem & Vulnerability Summary |
| :--- | :---: | :---: | :---: | :--- |
| `CVE-2026-112393` | **CRITICAL** | `9.8` | `12.3.0 -> 13.0.0` | Heap buffer overflow in `_tiffWriteProc` when saving TIFF streams to `BytesIO`. |
| `CVE-2026-112398` | **CRITICAL** | `9.8` | `12.3.0 -> 13.0.0` | Heap buffer overflow in FlashPix (FPX) JPEG decoding leading to arbitrary code execution. |
| `CVE-2026-112403` | **CRITICAL** | `9.8` | `12.3.0 -> 13.0.0` | Heap buffer overflow in `ImagingJpegDecode` native JPEG decoder. |
| `CVE-2026-112900` | **CRITICAL** | `9.8` | `12.3.0 -> 13.0.0` | Argument injection in Ghostscript invocation, potentially leading to remote code execution. |
| `CVE-2026-96639` | **CRITICAL** | `9.8` | `12.3.0 -> 13.0.0` | Multi-frame image loaders can reuse stale native storage pointers across mode transitions. |
| `CVE-2026-96778` | **HIGH** | `8.8` | `12.3.0 -> 13.0.0` | Arbitrary code execution via buffer overflow in native JPEG encoder. |
| `CVE-2026-112404` | **HIGH** | `8.2` | `12.3.0 -> 13.0.0` | Denial of service via out-of-bounds read during TIFF decoding. |
| `CVE-2026-112896` | **HIGH** | `8.2` | `12.3.0 -> 13.0.0` | Denial of service via out-of-bounds read in native TIFF encoder. |
| `CVE-2026-96644` | **HIGH** | `8.1` | `12.3.0 -> 13.0.0` | Denial of service via out-of-bounds read in Windows metafile parser. |
| `GHSA-78g4-xqwv-q3g8` | **HIGH** | `8.1` | `12.3.0 -> 13.0.0` | Bundled `libopenjp2 2.5.4` in wheels carries `OSV-2025-219` heap-buffer-overflow write via `Image.open().load()`. |
| `CVE-2026-112390` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via infinite loop when parsing crafted MIC images. |
| `CVE-2026-112392` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via zero-size images passed to rank filters. |
| `CVE-2026-112397` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via out-of-bounds memory access on zero-width images. |
| `CVE-2026-112399` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via crafted APNG multi-frame image streams. |
| `CVE-2026-112400` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via unbounded memory exhaustion from crafted GIF frames. |
| `CVE-2026-112402` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via double free during native image transformation. |
| `CVE-2026-112405` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via null pointer dereference in `Image.merge()`. |
| `CVE-2026-112406` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via infinite loop during PDF page rewriting. |
| `CVE-2026-112892` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via unbounded memory expansion in MSP decoder. |
| `CVE-2026-112893` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via invalid pointer free during TrueType font rendering. |
| `CVE-2026-112894` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via crafted multi-frame mode conversion. |
| `CVE-2026-112895` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via crafted PDF stream during append operations. |
| `CVE-2026-112897` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Information disclosure via uninitialized heap buffer in TIFF decoding. |
| `CVE-2026-96640` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via duplicate page references in PDF output/input files. |
| `CVE-2026-96643` | **HIGH** | `7.5` | `12.3.0 -> 13.0.0` | Denial of service via repeated malformed EXIF headers. |
| `CVE-2026-112902` | **HIGH** | `7.1` | `12.3.0 -> 13.0.0` | Memory disclosure and segmentation fault in `libtiff` encoder via crafted TIFF tags. |
| `CVE-2026-96637` | **HIGH** | `6.5` | `12.3.0 -> 13.0.0` | Denial of service via decompression-bomb check bypass in SPIDER images. |
| `CVE-2026-96642` | **HIGH** | `6.5` | `12.3.0 -> 13.0.0` | Denial of service via negative archive member size in `TarIO`. |

*(Twelve additional deduplicated `MEDIUM` advisories—`CVE-2026-112394`, `CVE-2026-112395`, `CVE-2026-112391`, `CVE-2026-112396`, `CVE-2026-112401`, `CVE-2026-112891`, `CVE-2026-112899`, `CVE-2026-112901`, `CVE-2026-96636`, `CVE-2026-96638`, `CVE-2026-96641`, and `CVE-2026-112898`—are likewise resolved simultaneously by upgrading to `pillow>=13.0.0`.)*

---

## 6.2 Container IaC Hardening (`SEC-02`) & Secret Hygiene (`SEC-03`)

### Dockerfile Misconfigurations (`DS-0002` & `DS-0026`)

Trivy IaC scanning flagged `6` findings across Drawlib's three container definitions under `tools/docker/`:

| Check ID | Severity | Affected Files (`tools/docker/`) | Trivy Finding Message | Engineering Remediation |
| :--- | :---: | :--- | :--- | :--- |
| **`DS-0002`** | **HIGH** (`×3`) | `Dockerfile.prod`, `Dockerfile.test_local`, `Dockerfile.test_pypi` | `Specify at least 1 USER command in Dockerfile with non-root user as argument` | Create unprivileged `drawlib` user (`UID 10001`), store Playwright browsers and pre-downloaded assets under world-readable `/opt/` paths, and set `USER drawlib` before `WORKDIR /workspace`. |
| **`DS-0026`** | **LOW** (`×3`) | `Dockerfile.prod`, `Dockerfile.test_local`, `Dockerfile.test_pypi` | `Add HEALTHCHECK instruction in your Dockerfile` | Informational for ephemeral batch CLI/test containers (`CMD ["drawlib", "--help"]`), which exit upon completion rather than running a long-lived network daemon; document Trivy ignore or add `HEALTHCHECK NONE`. |

Running `Dockerfile.prod` as non-root (`USER drawlib`) is particularly impactful for Drawlib because both embedded Python diagram `exec()` blocks and Playwright's headless Chromium browser execute inside the container process tree.

### Secret Scanning & `.dockerignore` Isolation (`SEC-03`)

- **Zero Hardcoded Source Secrets (`PASS`)**: Both AST literal entropy analysis (`AstFacts.hardcoded_secrets = []`) and Trivy repository scanning confirmed **zero API keys, credentials, or tokens** across all `424` tracked source files and `150` test files.
- **Default-Deny `.dockerignore` (`PASS`)**: Root `.dockerignore` begins with `*` (deny all) and explicitly allowlists only `!pyproject.toml`, `!src/`, and `!tests/`, guaranteeing local developer files can never leak into built Docker layers.
- **Untracked Local `.env` PyPI Token (`1` Redacted Workspace Finding)**: Trivy's local filesystem scan detected `pypi-upload-token` at `.env:1` (`PYPI_TOKEN=***`). Verification confirmed `.env` is excluded by `.gitignore:159` and `git ls-files .env` is empty (never committed to Git history). Migrating release publishing in `tools/dcli/pypi/` to **GitHub Actions OIDC Trusted Publishing** (`id-token: write`) eliminates the need to store static PyPI tokens on developer workstations.

---

## 6.3 AST Dangerous Code Sinks (`CWE-94`) & API Attack Surface

```drawlib align=center code=hide file=ch06_cwe_sinks_and_trust_boundary.png caption="Figure 6.2 — Complete CWE-94 exec() sink inventory, zero injection/API surface verification, and recommended container sandbox boundary for untrusted Markdown."
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, Panel, Table
from drawlib.styles import Colors, Styles

setup(width=170, height=88)

left_panel = Panel(
    "AST Code Sinks & Surface Audit (SEC-04..06)",
    style=Styles.Neutral,
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.code,
    icon_style=Styles.DarkBold,
    header_variant="filled",
    header_height=8.8,
)
left_panel.draw((5.0, 6.0), width=95.0, height=76.0, align="bottom_left")

tbl = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=9.8),
    header_cell_style=Styles.PrimaryNeutral,
    header_text_style=Styles.DarkBold.patch(text_size=10.0),
    border_style=Styles.MutedThin,
)
tbl.set_style_cell_evenodd(
    even_color=Colors.Neutral,
    even_text_style=Styles.Dark.patch(text_size=9.8),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=9.8),
)
tbl.set_style_cell_header(
    background_color=Colors.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
tbl.set_style_cell(
    background_color=Colors.SuccessNeutral,
    text_style=Styles.SuccessBold.patch(text_size=9.8),
    rows=[6, 7],
    columns=[1],
)

sink_rows = [
    ["Location / Audit Scope", "Class", "Runtime Purpose / Verification"],
    ["styles_loader.py:78", "CWE-94", "exec(styles.py) theme tokens"],
    ["styles_loader.py:158", "CWE-94", "exec(utils.py) shared helpers"],
    ["processor.py:121", "CWE-94", "exec(fence) quiet stdout mode"],
    ["processor.py:123", "CWE-94", "exec(fence) verbose/dev mode"],
    ["_image_code.py:54", "CWE-94", "Subprocess get_dimage_from_code"],
    ["CWE-89 / 78 / 79 / 502", "0 Flaws", "Param SQL, shell=False, Jinja2"],
    ["HTTP API Surface (SEC-05)", "0 Routes", "N/A — pure CLI & Python library"],
]
tbl.draw_flexible(
    xy=(8.0, 69.5),
    column_widths=[30.5, 14.5, 44.0],
    row_heights=[7.6, 7.4, 7.4, 7.4, 7.4, 7.4, 7.6, 7.6],
    data=sink_rows,
    align="top_left",
)

right_panel = Panel(
    "Untrusted Markdown Sandbox",
    style=Styles.PrimaryNeutral,
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    icon=phosphor.lock_key,
    icon_style=Styles.WhiteBold,
    header_variant="filled",
    header_height=8.8,
)
right_panel.draw((104.0, 6.0), width=61.0, height=76.0, align="bottom_left")
r_xy, r_w, r_h = right_panel.get_content_box((104.0, 6.0), width=61.0, height=76.0, padding=(3.0, 3.0))

sandbox = CardList(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=10.3),
    description_style=Styles.Dark.patch(text_size=9.7),
    badge_shape="rounded_rect",
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=9.8),
    direction="vertical",
    show_arrows=True,
    arrow_style=Styles.DarkBold,
    spacing=3.4,
)
sandbox.add(
    "1. Classify Source Trust",
    "Trusted Git repo: local CLI OK\nUntrusted Markdown: isolate",
    badge_text="IN",
)
sandbox.add(
    "2. Non-Root Container",
    "USER drawlib (UID 10001) +\n--read-only & CPU/memory caps",
    badge_text="OS",
)
sandbox.add(
    "3. Offline --network=none",
    "Pre-baked assets & Chromium;\nblocks SSRF & exfiltration",
    badge_text="NET",
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=9.8),
)
sandbox.draw(r_xy, width=r_w, height=r_h)

save()
```

### Detailed Assessment of `CWE-94` Sites, Injection Classes & API Endpoints

1. **Five Intentional `CWE-94` (`exec`) Sinks (`SEC-04 WARN`)**:
   - `src/drawlib/_builder/_common/styles_loader.py:78` (`load_styles`) and `styles_loader.py:158` (`load_utils`) compile and execute project-level `styles.py` and `utils.py` files so documentation projects can customize `Styles`/`Colors` and register reusable drawing macros.
   - `src/drawlib/_builder/doc_builder/processor/processor.py:121` (quiet stdout-redirected mode) and `processor.py:123` (`verbose`/`developer` mode) execute ```` ```drawlib ```` fenced Python blocks inside Markdown files while temporarily monkey-patching `save()` as a controlled no-op.
   - `src/drawlib/_core/l4_canvas/_image_code.py:54` (`_worker_render_code`) executes nested drawing scripts inside an isolated `multiprocessing` child process for `get_dimage_from_code(code, timeout=...)`.
   - **Architectural Verdict**: Just like Jupyter notebooks, Quarto, or Sphinx code-execution directives, executing Python code is the core value proposition of Drawlib (*"Illustration as Code"*). Python-level `ast` allowlisting or `__builtins__` restriction is notoriously bypassable via object-graph traversal and should **not** be relied upon as a security boundary. Instead, Drawlib should explicitly document this trust boundary in `SECURITY.md` and CLI help: run `drawlib build` / `drawlib show` directly only on trusted sources, and wrap untrusted third-party Markdown rendering inside an ephemeral container (`--user 10001:10001 --network=none --read-only --pids-limit=128 --memory=1g`) built with `--full` pre-cached assets.
2. **Zero Injection or Deserialization Vulnerabilities (`PASS`)**:
   - **`CWE-89` (SQL Injection = `0`)**: `BuildImageCache` and `CliImageCache` in `src/drawlib/_builder/_common/cache.py` use strictly parameterized `?` SQLite queries on static table schemas.
   - **`CWE-78` (OS Command Injection = `0`)**: Subprocess execution in `src/drawlib/_builder/_common/browser.py:210` passes explicit argument arrays (`[str(exec_path), str(cli_path), *_INSTALL_ARGS]`) without `shell=True`.
   - **`CWE-79` / `CWE-502` (XSS / Unsafe Deserialization = `0`)**: HTML templates rely on `Jinja2` + `MarkupSafe` escaping, manifests parse via stdlib `tomllib`, and caches store raw PNG/SVG bytes plus SHA-256 digests (zero `pickle` or `yaml.load` usage).
3. **API Endpoint Surface (`SEC-05` / `SEC-06`: `api_endpoints = []`, `not_applicable`)**:
   - Drawlib's runtime archetype is `["cli", "library"]` with **zero production HTTP/gRPC service endpoints**. The `drawlib serve` subcommand launches a strictly local static preview server bound to `127.0.0.1` by default for interactive authoring and `--check` link validation.

---

## 6.4 OpenSSF Supply-Chain Posture & Governance Checklist

Drawlib scored **86/100 (Grade A)** on `supply_chain_audit` and **89/100 (Grade A)** on `repo_structure_audit`, combining strong cryptographic asset integrity and least-privilege CI workflows with straightforward governance additions (`SECURITY.md`, Dependabot, and commit-SHA Action pins):

| Supply-Chain Control | Current Repository State | Evidence Location | Recommended Hardening |
| :--- | :---: | :--- | :--- |
| **CI Workflow Token Permissions** | **PASS** | `.github/workflows/{quality,ut_github,ut_pypi,ut_template}.yml` | All `4` workflows declare explicit top-level `permissions: contents: read`; retain least-privilege defaults when adding OIDC release jobs. |
| **External Binary Asset Integrity** | **PASS** | `src/drawlib/_core/l3_external/_package.py` & `src/drawlib/_release_assets.py` | Every lazy-downloaded font, icon, and GeoJSON archive embeds a compiled-in **SHA-256 digest** verified before zip extraction alongside `timeout=60` HTTPS fetches. |
| **Runtime Dependency Specifiers** | **PASS** | `pyproject.toml` (`dependencies`, `13` packages) | `100%` of runtime dependencies specify explicit SemVer lower bounds (`unpinned_dependencies = []`), cleanly separated from `[dependency-groups].dev`. |
| **Lockfile Strategy (`uv.lock`)** | **INFO** | `uv.lock` & `.gitignore:182` | `uv.lock` is generated locally for reproducible audits while `.gitignore` excludes it so CI tests flexible library resolution across Python `3.11–3.13`; document this intentional library policy or commit `uv.lock` alongside a separate `--resolution=lowest-direct` CI job. |
| **GitHub Actions Pinning** | **WARN** (`P2`) | `.github/workflows/quality.yml:20,23,28` | Steps currently reference mutable major tags (`actions/checkout@v4`, `astral-sh/setup-uv@v5`, `actions/setup-python@v5`); pin to full 40-char commit SHAs with version comments. |
| **Vulnerability Disclosure Policy** | **MISSING** (`P1/P2`) | Repository root (`SECURITY.md` absent) | Add `SECURITY.md` enabling GitHub Private Vulnerability Reporting, supported version policy (`0.3.x`), and the `CWE-94` `exec()` container-sandbox guidance. |
| **Automated Dependency Updates** | **MISSING** (`P1/P2`) | `.github/dependabot.yml` absent | Configure weekly `.github/dependabot.yml` updates for `uv`/`pip` and `github-actions` so future `pillow` or Action advisories open automated PRs immediately. |
