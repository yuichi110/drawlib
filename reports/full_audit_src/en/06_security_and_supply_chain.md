# 6. Deep Dive: Security, Supply Chain & API Surface

First-party Drawlib source code and container packaging achieve a **96/100 (Grade S)** score on `security_vulnerability_audit` (`status="passed"`) and **94/100** on the overall Security axis—combining zero SQL/command/XSS injection flaws, zero hardcoded secrets, SHA-256 verified external asset downloads, and least-privilege `contents: read` CI workflows with **zero application CVEs** (`pillow@13.0.0` in `uv.lock`) and **zero active Dockerfile misconfigurations** (`USER drawlib`, `UID 10001`).

```drawlib align=center code=hide file=ch06_supply_chain_vuln_breakdown.png caption="Figure 6.1 — Post-Remediation Trivy SCA, Container OS, IaC Misconfiguration, and Secret Scan Posture (0 Active CVEs, 0 IaC Failures, 0 Secrets)."
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.icons import phosphor
from drawlib.smartarts import KpiCards, Panel
from drawlib.styles import Styles

setup(width=170, height=84)

bar = BarChart(
    axis_line_style=Styles.Muted,
    categories=[
        "Source & .env Secrets\n(424 Files + pni.toml)",
        "Container OS Layers\n(python:3.12-slim)",
        "12 Sibling Runtime Deps\n(pyproject.toml)",
        "Dockerfiles IaC (After)\n(USER drawlib UID 10001)",
        "pillow@13.0.0 (After)\n(Upgraded from 12.3.0)",
        "pillow@12.3.0 (Before)\n(Initial Baseline)",
    ],
    width=80.0,
    height=58.0,
    orientation="horizontal",
    bar_mode="stack",
    bar_width_ratio=0.62,
    bar_r=0.8,
    title="Trivy Security Findings: Initial Baseline vs. Post-Remediation",
    title_style=Styles.DarkBold.patch(text_size=11.5),
    axis_text_style=Styles.Dark.patch(text_size=9.8),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=9.8),
    value_format="{:.0f}",
)
bar.add_series("Critical (CVSS 9.8)", [0.0, 0.0, 0.0, 0.0, 0.0, 5.0], style=Styles.DangerFlat)
bar.add_series("High", [0.0, 0.0, 0.0, 0.0, 0.0, 23.0], style=Styles.WarningFlat)
bar.add_series("Medium / Low", [0.0, 0.0, 0.0, 0.0, 0.0, 13.0], style=Styles.SecondaryNeutral)
bar.configure_x_axis(min_value=0.0, max_value=45.0, tick_step=10.0)
bar.draw(xy=(21.0, 7.0))
bar.draw_legend(
    xy=(23.0, 68.5),
    text_style=Styles.Dark.patch(text_size=10.0),
    orientation="horizontal",
    item_gap=5.5,
)

panel = Panel(
    "Verified Security Posture",
    style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.shield_check,
    icon_style=Styles.SuccessBold,
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
    "Pillow 13.0.0 Upgraded",
    "0 CVEs in uv.lock & pyproject.toml",
    metric_style=Styles.SuccessBold.patch(text_size=12.8),
    accent_style=Styles.SuccessFlat,
)
kpis.add(
    "0 CVEs",
    "All 13 Deps & OS Layers",
    "SemVer floors + 0 OS layer CVEs",
    metric_style=Styles.SuccessBold.patch(text_size=12.8),
    accent_style=Styles.SuccessFlat,
)
kpis.add(
    "3 -> 0",
    "IaC DS-0002 Cleared",
    "UID 10001 + DS-0026 waived",
    metric_style=Styles.PrimaryBold.patch(text_size=12.8),
    accent_style=Styles.PrimaryFlat,
)
kpis.add(
    "0 Secrets",
    "Source & Scan Hygiene",
    ".env excluded in git & pni.toml",
    metric_style=Styles.PrimaryBold.patch(text_size=12.0),
    accent_style=Styles.PrimaryFlat,
)
kpis.draw(p_xy, width=p_w, height=p_h, columns=1)

save()
```

---

## 6.1 Dependency Vulnerability Remediation (`SEC-01`: `pillow@12.3.0 -> 13.0.0`, `0` CVEs)

Trivy v0.69.3 Software Composition Analysis (`SEC-01`) evaluated `pyproject.toml`, `uv.lock`, and container OS package metadata before and after the in-tree `pillow>=13.0.0` upgrade:
- **Complete Closure of All 41 Application CVEs (`41 -> 0`)**: In the initial baseline scan, all `41` reported application vulnerabilities (`5 CRITICAL`, `23 HIGH`, `13 MEDIUM` in `app_vuln_counts`) resided in **`pillow@12.3.0`** in `uv.lock`. Upgrading `pyproject.toml` to `pillow>=13.0.0` and `uv.lock` to **`pillow@13.0.0`** resolved **100% of application CVEs (`app_vuln_counts = 0`)**, verified by re-running `run_security_scan` (`trivy_fs.json` & `security_facts.json`: `status = "passed"`, `vulnerabilities = []`).
- **Clean Ecosystem Across All 13 Direct Dependencies & OS Layers (`0` CVEs)**: All `13` direct runtime dependencies (`matplotlib>=3.8`, `pillow>=13.0.0`, `numpy>=1.26`, `pydantic>=2.8`, `pygments>=2.18`, `markdown-it-py>=3.0`, `jinja2>=3.1`, `markupsafe>=2.1`, `typer>=0.12.0`, `rich>=13.0.0`, `playwright>=1.49.0`, `python-docx>=1.2.0`, `python-pptx>=1.0.2`) and container OS layers (`os_vuln_counts = 0`) now report **zero vulnerabilities** and **zero unpinned range specifiers**.

### Historical Reference: 28 Critical & High `pillow@12.3.0` Advisories Cleared by `pillow>=13.0.0`

| Advisory ID | Severity | CVSS | Resolution (`uv.lock`) | Affected Native Subsystem & Vulnerability Summary |
| :--- | :---: | :---: | :---: | :--- |
| `CVE-2026-112393` | **CRITICAL** | `9.8` | **Fixed (`13.0.0`)** | Heap buffer overflow in `_tiffWriteProc` when saving TIFF streams to `BytesIO`. |
| `CVE-2026-112398` | **CRITICAL** | `9.8` | **Fixed (`13.0.0`)** | Heap buffer overflow in FlashPix (FPX) JPEG decoding leading to arbitrary code execution. |
| `CVE-2026-112403` | **CRITICAL** | `9.8` | **Fixed (`13.0.0`)** | Heap buffer overflow in `ImagingJpegDecode` native JPEG decoder. |
| `CVE-2026-112900` | **CRITICAL** | `9.8` | **Fixed (`13.0.0`)** | Argument injection in Ghostscript invocation, potentially leading to remote code execution. |
| `CVE-2026-96639` | **CRITICAL** | `9.8` | **Fixed (`13.0.0`)** | Multi-frame image loaders can reuse stale native storage pointers across mode transitions. |
| `CVE-2026-96778` | **HIGH** | `8.8` | **Fixed (`13.0.0`)** | Arbitrary code execution via buffer overflow in native JPEG encoder. |
| `CVE-2026-112404` | **HIGH** | `8.2` | **Fixed (`13.0.0`)** | Denial of service via out-of-bounds read during TIFF decoding. |
| `CVE-2026-112896` | **HIGH** | `8.2` | **Fixed (`13.0.0`)** | Denial of service via out-of-bounds read in native TIFF encoder. |
| `CVE-2026-96644` | **HIGH** | `8.1` | **Fixed (`13.0.0`)** | Denial of service via out-of-bounds read in Windows metafile parser. |
| `GHSA-78g4-xqwv-q3g8` | **HIGH** | `8.1` | **Fixed (`13.0.0`)** | Bundled `libopenjp2 2.5.4` in wheels carries `OSV-2025-219` heap-buffer-overflow write via `Image.open().load()`. |
| `CVE-2026-112390`..`96642` | **HIGH (`×18`)** | `6.5–7.5` | **Fixed (`13.0.0`)** | 18 `HIGH` DoS/memory-safety advisories across MIC, rank filters, APNG, GIF, `Image.merge()`, PDF, MSP, TrueType, EXIF, `libtiff`, SPIDER, and `TarIO` decoders (plus 12 `MEDIUM` advisories). |

---

## 6.2 Container IaC Hardening (`SEC-02`) & Secret Hygiene (`SEC-03`)

### Dockerfile Hardening (`DS-0002` Fixed, `DS-0026` Waived -> `0` Active Misconfigurations)

Trivy IaC scanning (`trivy_fs.json` / `security_facts.json`) verified all three container definitions under `tools/docker/` plus `.pni/dockerfiles/root/Dockerfile`:

| Check ID | Initial Sev | Affected Files (`tools/docker/`) | Resolution Status | Engineering Implementation & Verification |
| :--- | :---: | :--- | :---: | :--- |
| **`DS-0002`** | **HIGH** (`×3`) | `Dockerfile.prod`, `Dockerfile.test_local`, `Dockerfile.test_pypi` | **`FIXED` (`0` Failures)** | Added unprivileged `drawlib` user and group (`UID/GID 10001`), relocated Playwright browsers (`/opt/ms-playwright`) and asset caches (`/opt/drawlib-cache`) with `chmod -R a+rX`, and switched to `USER drawlib` before `WORKDIR` / `CMD`. Trivy reports `26` passed checks and `0` `DS-0002` failures. |
| **`DS-0026`** | **LOW** (`×3`) | `Dockerfile.prod`, `Dockerfile.test_local`, `Dockerfile.test_pypi` | **`WAIVED` (`.pni/pni.toml`)** | Ephemeral batch CLI and `pytest` containers exit immediately after command completion rather than running a long-lived daemon; waived via `[[opt_out]] id = "DS-0026"` (`opt_out_counts = {"DS-0026": 3}`). |

### Secret Scanning & `.dockerignore` Isolation (`SEC-03`: `0` Secrets)

- **Zero Hardcoded Source Secrets (`PASS`)**: Both AST literal entropy analysis (`AstFacts.hardcoded_secrets = []`) and Trivy repository scanning (`security_facts.secrets = []`) confirmed **zero API keys, credentials, or tokens** across all `424` tracked source files and `150` test files.
- **Default-Deny `.dockerignore` & `.pni/pni.toml` Scope (`PASS`)**: Root `.dockerignore` begins with `*` (deny all) and explicitly allowlists only `!pyproject.toml`, `!src/`, and `!tests/`, while `.gitignore` and `.pni/pni.toml` (`skip_files = [".env", ".env.*", "**/.env"]`) exclude untracked local developer `.env` files from Git, Docker build contexts, and filesystem scans.

---

## 6.3 AST Dangerous Code Sinks (`CWE-94`) & API Attack Surface

```drawlib align=center code=hide file=ch06_cwe_sinks_and_trust_boundary.png caption="Figure 6.2 — Complete CWE-94 exec() sink inventory (waived in .pni/pni.toml), zero injection/API surface verification, and container sandbox boundary for untrusted Markdown."
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
    ["Location / Audit Scope", "Policy", "Runtime Purpose / Verification"],
    ["styles_loader.py:78", "Waived", "exec(styles.py) theme tokens"],
    ["styles_loader.py:158", "Waived", "exec(utils.py) shared helpers"],
    ["processor.py:121", "Waived", "exec(fence) quiet stdout mode"],
    ["processor.py:123", "Waived", "exec(fence) verbose/dev mode"],
    ["_image_code.py:54", "Waived", "Subprocess get_dimage_from_code"],
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

1. **Five Intentional `CWE-94` (`exec`) Sinks (`Waived in .pni/pni.toml`)**:
   - `src/drawlib/_builder/_common/styles_loader.py:78` (`load_styles`) and `styles_loader.py:158` (`load_utils`) compile and execute project-level `styles.py` and `utils.py` files so documentation projects can customize `Styles`/`Colors` and register reusable drawing macros.
   - `src/drawlib/_builder/doc_builder/processor/processor.py:121` (quiet stdout-redirected mode) and `processor.py:123` (`verbose`/`developer` mode) execute ```` ```drawlib ```` fenced Python blocks inside Markdown files while temporarily monkey-patching `save()` as a controlled no-op.
   - `src/drawlib/_core/l4_canvas/_image_code.py:54` (`_worker_render_code`) executes nested drawing scripts inside an isolated `multiprocessing` child process for `get_dimage_from_code(code, timeout=...)`.
   - **Architectural Verdict**: Just like Jupyter notebooks, Quarto, or Sphinx code-execution directives, executing Python code is the core value proposition of Drawlib (*"Illustration as Code"*). This intentional design is recorded under `[[opt_out]] id = "CWE-94"` in `.pni/pni.toml`, and untrusted third-party Markdown should be rendered inside an ephemeral container (`--user 10001:10001 --network=none --read-only --pids-limit=128 --memory=1g`) built with `./dcli docker build --full`.
2. **Zero Injection or Deserialization Vulnerabilities (`PASS`)**:
   - **`CWE-89` (SQL Injection = `0`)**: `BuildImageCache` and `CliImageCache` in `src/drawlib/_builder/_common/cache.py` use strictly parameterized `?` SQLite queries on static table schemas.
   - **`CWE-78` (OS Command Injection = `0`)**: Subprocess execution in `src/drawlib/_builder/_common/browser.py:210` passes explicit argument arrays (`[str(exec_path), str(cli_path), *_INSTALL_ARGS]`) without `shell=True`.
   - **`CWE-79` / `CWE-502` (XSS / Unsafe Deserialization = `0`)**: HTML templates rely on `Jinja2` + `MarkupSafe` escaping, manifests parse via stdlib `tomllib`, and caches store raw PNG/SVG bytes plus SHA-256 digests (zero `pickle` or `yaml.load` usage).
3. **API Endpoint Surface (`SEC-05` / `SEC-06`: `api_endpoints = []`, `not_applicable`)**:
   - Drawlib's runtime archetype is `["cli", "library"]` with **zero production HTTP/gRPC service endpoints**. The `drawlib serve` subcommand launches a strictly local static preview server bound to `127.0.0.1` by default for interactive authoring and `--check` link validation.

---

## 6.4 OpenSSF Supply-Chain Posture & Governance Checklist

Drawlib scored **92/100 (Grade S)** on `supply_chain_audit` and **91/100 (Grade S)** on `repo_structure_audit`, combining cryptographic asset integrity, non-root Docker images (`UID 10001`), and least-privilege CI workflows with straightforward governance additions (`SECURITY.md`, Dependabot, and commit-SHA Action pins):

| Supply-Chain Control | Current Repository State | Evidence Location | Recommended Hardening |
| :--- | :---: | :--- | :--- |
| **CI Workflow Token Permissions** | **PASS** | `.github/workflows/{quality,ut_github,ut_pypi,ut_template}.yml` | All `4` workflows declare explicit top-level `permissions: contents: read`; retain least-privilege defaults when adding OIDC release jobs. |
| **External Binary Asset Integrity** | **PASS** | `src/drawlib/_core/l3_external/_package.py` & `src/drawlib/_release_assets.py` | Every lazy-downloaded font, icon, and GeoJSON archive embeds a compiled-in **SHA-256 digest** verified before zip extraction alongside `pkg.files` membership checks and `timeout=60` HTTPS fetches. |
| **Container Least Privilege (`USER`)** | **PASS** | `tools/docker/Dockerfile.{prod,test_local,test_pypi}` | All production and test Dockerfiles create and switch to an unprivileged `USER drawlib` (`UID 10001`) with `0` Trivy `DS-0002` findings. |
| **Runtime Dependency Specifiers** | **PASS** | `pyproject.toml` (`dependencies`, `13` packages) | `100%` of runtime dependencies specify explicit SemVer lower bounds (`pillow>=13.0.0`, `unpinned_dependencies = []`, `0` CVEs), cleanly separated from `[dependency-groups].dev`. |
| **Lockfile Strategy (`uv.lock`)** | **WAIVED** (`.pni/pni.toml`) | `uv.lock`, `.gitignore:182` & `.pni/pni.toml` | `uv.lock` is generated locally for reproducible SCA while `.gitignore` excludes it so CI tests flexible library resolution across Python `3.11–3.13` (`python/lockfile_committed` waived in `.pni/pni.toml`). |
| **GitHub Actions Pinning** | **WARN** (`P2`) | `.github/workflows/quality.yml:20,23,28` | Steps currently reference mutable major tags (`actions/checkout@v4`, `astral-sh/setup-uv@v5`, `actions/setup-python@v5`); pin to full 40-char commit SHAs with version comments. |
| **Vulnerability Disclosure Policy** | **OPEN** (`P2`) | Repository root (`SECURITY.md` absent) | Add `SECURITY.md` enabling GitHub Private Vulnerability Reporting, supported version policy (`0.3.x`), and the `CWE-94` `exec()` container-sandbox guidance. |
| **Automated Dependency Updates** | **OPEN** (`P2`) | `.github/dependabot.yml` absent | Configure weekly `.github/dependabot.yml` updates for `uv`/`pip` and `github-actions` so future dependency or Action advisories open automated PRs immediately. |
