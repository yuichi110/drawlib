# 3. Recommended Remediation Roadmap

This chapter translates the diagnostic findings into **10 prioritized engineering actions** (`1 P0` urgent security fix, `5 P1` container hardening, maintainability, and air-gapped verification actions, and `4 P2` architectural and governance refinements), mapping exact target files, implementation steps, expected impact, and rule/CVE traceability.

```drawlib align=center code=hide file=ch03_remediation_roadmap.png caption="Phased Engineering Remediation Timeline (P0 Urgent -> P1 Hardening & Air-Gapped CI -> P2 Polish)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import KpiCards, Panel, Roadmap
from drawlib.styles import Colors, Styles

setup(width=166, height=88)

# 1. Top Target Outcome KPI Strip (3 calm neutral/tinted-neutral cards)
kpis = KpiCards(
    style=Styles.Neutral,
    metric_style=Styles.DarkBold.patch(text_size=13.5),
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    accent_style=Styles.PrimaryFlat,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.33,
    spacing=3.5,
)
kpis.add(
    "0 CVEs",
    "P0 Security Target",
    "Clears all 41 Pillow CVEs",
    style=Styles.DangerNeutral,
    metric_style=Styles.DangerBold.patch(text_size=13.0),
    accent_style=Styles.DangerFlat,
)
kpis.add(
    "100%",
    "P1 Offline Test Pass",
    "UID 10001 + pkg.files + PPTX",
    style=Styles.PrimaryNeutral,
    metric_style=Styles.PrimaryBold.patch(text_size=13.5),
    accent_style=Styles.PrimaryFlat,
)
kpis.add(
    "0 Cycles",
    "P2 Pure Library DAG",
    "Acyclic DAG + SECURITY.md",
    style=Styles.Neutral,
    metric_style=Styles.DarkBold.patch(text_size=12.5),
    accent_style=Styles.SecondaryFlat,
)
kpis.draw(xy=(5.0, 66.5), width=156.0, height=16.5, columns=3, align="bottom_left")

# 2. Main Phased Execution Roadmap Panel
roadmap_panel = Panel(
    "Phased Remediation Execution Timeline (P0 -> P1 -> P2)",
    "10 Pre-Sorted Actions",
    style=Styles.White.patch(shape_line_color=Colors.Gray3, shape_line_width=1.0),
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.5),
    description_style=Styles.White.patch(text_size=10.0),
    icon=phosphor.rocket_launch,
    icon_style=Styles.White,
    header_variant="filled",
    header_height=8.5,
)
roadmap_panel.draw((5.0, 5.0), width=156.0, height=58.0, align="bottom_left")
inner_xy, inner_w, inner_h = roadmap_panel.get_content_box(
    (5.0, 5.0),
    width=156.0,
    height=58.0,
    padding=(4.0, 2.2),
    align="bottom_left",
)

rm = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Dark.patch(text_size=10.0),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.0,
    card_shape="rounded_rect",
    spacing=2.2,
)
rm.add(
    "P0: Upgrade Pillow >=13.0.0 (Clears 41 CVEs)",
    "Bump pillow in uv.lock & pyproject.toml; run ./dcli test drawlib to verify pixel baselines (#1)",
    badge_text="P0 · 1",
    icon=phosphor.shield_warning,
    style=Styles.PrimaryNeutral,
    badge_style=Styles.DangerFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
    icon_style=Styles.DangerBold,
)
rm.add(
    "P1: Hardening & Air-Gapped Tests (Actions #2–#6)",
    "Non-root Docker USER 10001, _download.py pkg.files check, DOCX complexity <=15 & offline PPTX",
    badge_text="P1 · 5",
    icon=phosphor.wrench,
    style=Styles.Neutral,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
)
rm.add(
    "P2: Architectural & Governance Polish (Actions #7–#10)",
    "Resolve 2 sibling diagram cycles, library exceptions vs sys.exit(1), Dependabot & SECURITY.md",
    badge_text="P2 · 4",
    icon=phosphor.git_merge,
    style=Styles.Neutral,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.SecondaryBold,
)
rm.draw(xy=inner_xy, width=inner_w, height=inner_h, align="bottom_left")

save()
```

---

## 3.1 Remediation Strategy & Priority Horizons

Drawlib v0.3.5 already operates from a strong **90/100 (Grade S)** baseline with **100.0% callable type coverage**, **99.3% docstring and import hygiene**, **0 SQL/shell/XSS injection flaws**, and **0 OS container CVEs**. The remaining audit deductions cluster into three tightly scoped execution horizons that can be landed incrementally without disrupting public APIs:

1. **`P0` — Urgent Supply-Chain Vulnerability Closure (Action `#1`)**: All **41 application CVEs** (`5 CRITICAL`, `23 HIGH`, `13 MEDIUM`) originate from a single locked package (`pillow@12.3.0` in `uv.lock`) while the other 12 direct runtime dependencies report **0 CVEs**. Upgrading to `pillow>=13.0.0` and re-verifying golden pixel baselines clears 100% of application CVEs in one atomic change.
2. **`P1` — Container Least Privilege, Compiler Complexity & Air-Gapped Verification (Actions `#2`–`#6`)**: Addresses the two offline `--network=none` assumptions uncovered by containerized runtime testing (`pkg.files` membership checks before HTTPS downloads in `_download.py`, plus pre-baked Chromium and pure-Python `_pptx_writer.py` unit tests), adds non-root `USER drawlib` (`UID 10001`) across Dockerfiles, and decomposes high-complexity DOCX/HTML AST walkers (`cognitive <= 15`).
3. **`P2` — Architectural Acyclicity, Library Exception Hygiene & Governance Polish (Actions `#7`–`#10`)**: Eliminates the final 2 intra-package `_edge <-> _junction` sibling cycles, replaces library-level `sys.exit(1)` calls with typed exceptions caught at the CLI boundary, publishes `SECURITY.md` + `.github/dependabot.yml`, and aligns `test_api_docs_completeness.py` with clean-room Docker test contexts.

---

## 3.2 Action Plan Traceability Matrix (`P0 -> P1 -> P2`)

The visual matrix below maps all **10 pre-sorted remediation items** (`P0 -> P1 -> P2`) across target modules, expected engineering outcomes, and governing audit rules or CVE advisories.

```drawlib align=center code=hide file=ch03_action_plan_matrix.png caption="Action Plan Traceability Matrix Across All 10 Prioritized Engineering Items (P0 -> P2)"
from drawlib.canvas import save, setup
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=168, height=96)

text(
    (84.0, 91.2),
    "Action Plan Traceability Matrix — 10 Prioritized Engineering Actions (P0 -> P2)",
    style=Styles.DarkBold.patch(text_size=12.5),
)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.5),
    border_style=Styles.MutedThin,
    has_header=True,
)

# 1. Alternating neutral row fills first
table.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Dark.patch(text_size=10.0),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.0),
)

# 2. Priority column semantic neutral badges (rows 1..10)
table.set_style_cell(
    background_color=Colors.Danger,
    text_style=Styles.WhiteBold.patch(text_size=10.0),
    rows=[1],
    columns=[0],
)
table.set_style_cell(
    background_color=Colors.PrimaryNeutral,
    text_style=Styles.PrimaryBold.patch(text_size=10.0),
    rows=[2, 3, 4, 5, 6],
    columns=[0],
)
table.set_style_cell(
    background_color=Colors.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
    rows=[7, 8, 9, 10],
    columns=[0],
)

# 3. Re-apply header row style AFTER set_style_cell_evenodd so row 0 stays PrimaryFlat
table.set_style_cell_header(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

table.set_style_border(
    top=Styles.Dark.patch(line_width=1.4),
    top2=Styles.Dark.patch(line_width=1.1),
    bottom=Styles.Dark.patch(line_width=1.4),
    left=Styles.MutedThin,
    left2=Styles.MutedThin,
    right=Styles.MutedThin,
    between_columns=Styles.MutedThin,
    between_rows=Styles.MutedThin,
)

matrix_data = [
    ["Priority", "Action Title", "Target Files", "Expected Impact", "Related Rules / CVEs"],
    [
        "P0 · #1",
        "Upgrade Pillow >=13.0.0 &\nverify raster baselines",
        "pyproject.toml,\nuv.lock",
        "Clears all 41 app CVEs\n(5 CRIT, 23 HIGH -> 0)",
        "security_vulnerability,\n5 CRIT CVEs + GHSA",
    ],
    [
        "P1 · #2",
        "Decompose high-complexity\nDOCX & fence parsers",
        "exporter_docx.py,\noptions.py, merger.py",
        "Cognitive complexity <=15;\nlowers compiler risk",
        "common/maintainability",
    ],
    [
        "P1 · #3",
        "Non-root Docker USER +\nSECURITY.md & Dependabot",
        "Dockerfile.{prod,\ntest_local,test_pypi}",
        "Fixes 3 HIGH DS-0002;\nautomates CVE PRs & OIDC",
        "security_vulnerability,\nsupply_chain, DS-0002",
    ],
    [
        "P1 · #4",
        "Run production Docker image\nas non-root UID 10001",
        "tools/docker/\nDockerfile.prod",
        "Enforces least privilege\nin Docker PDF/exec runs",
        "common/supply_chain,\ncommon/security",
    ],
    [
        "P1 · #5",
        "Bake Chromium & assets +\n_pptx_writer unit tests",
        "_pptx_writer.py, pdf.py,\ntest_pptx.py",
        "100% offline pass rate;\n>80% PPTX writer cov",
        "common/\nruntime_verification",
    ],
    [
        "P1 · #6",
        "Validate pkg.files before\nHTTPS asset downloads",
        "_download.py,\n_release_assets.py",
        "Fast-fails invalid icons;\nfixes 12 offline tests",
        "common/\nruntime_verification",
    ],
    [
        "P2 · #7",
        "Eliminate 2 intra-diagram\nsibling import cycles",
        "architecture & flow\n_edge.py / _junction.py",
        "0 runtime circular deps\nacross all 424 modules",
        "common/architecture",
    ],
    [
        "P2 · #8",
        "Replace library sys.exit(1)\nwith typed exceptions",
        "_settings.py, viewer.py,\n_cli/_drawlib.py",
        "Prevents host termination\nfor library callers",
        "common/\nlibrary_guidelines",
    ],
    [
        "P2 · #9",
        "Publish SECURITY.md &\nconfigure Dependabot",
        "pyproject.toml,\nquality.yml",
        "Closes OpenSSF disclosure\n& supply-chain gaps",
        "common/supply_chain",
    ],
    [
        "P2 · #10",
        "Include docs_src/api or\nguard with pytest.skip",
        "test_api_docs_*.py,\n.dockerignore, Dockerfile",
        "Keeps dcli docker test\ngreen (local & PyPI)",
        "python/testing",
    ],
]

table.draw_flexible(
    xy=(5.0, 86.3),
    column_widths=[14.0, 43.0, 34.0, 37.0, 30.0],
    row_heights=[7.3] + [7.4] * 10,
    data=matrix_data,
    align="top_left",
)

save()
```

### Summary Table of All 10 Pre-Sorted Action Items

| # | Priority | Category | Action Title | Target Files | Related Rules / Advisories | Expected Impact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **`P0`** | `security` | **Upgrade locked Pillow dependency to >=13.0.0 and re-verify raster baselines** | `pyproject.toml`, `uv.lock` | `common/security_vulnerability`, `CVE-2026-112393`, `CVE-2026-112398`, `CVE-2026-112403`, `CVE-2026-112900`, `CVE-2026-96639`, `GHSA-78g4-xqwv-q3g8` | Eliminates all 41 Trivy application CVEs (`5 CRITICAL`, `23 HIGH`, `13 MEDIUM`), bringing `app_vuln_counts` to `0`. |
| **2** | **`P1`** | `code_quality` | **Decompose High-Complexity DOCX & Fence Parser Routines** | `src/drawlib/_builder/doc_builder/exporter_docx.py`, `src/drawlib/_builder/doc_builder/processor/options.py`, `src/drawlib/_builder/doc_builder/merger.py` | `common/maintainability` | Substantially lowers maintenance risk and unit test surface in the document compiler pipeline (`cognitive <= 15`). |
| **3** | **`P1`** | `security` | **Add non-root USER to Dockerfiles and publish SECURITY.md + Dependabot config** | `tools/docker/Dockerfile.prod`, `tools/docker/Dockerfile.test_local`, `tools/docker/Dockerfile.test_pypi` | `common/security_vulnerability`, `common/supply_chain`, `DS-0002` | Resolves all `HIGH` container misconfigurations (`DS-0002`), automates future CVE detection, and hardens release credential hygiene. |
| **4** | **`P1`** | `security` | **Run Production Docker Image as Non-Root User** | `tools/docker/Dockerfile.prod` | `common/supply_chain`, `common/security` | Enforces container least privilege when rendering diagrams or PDFs inside Docker (`UID 10001`). |
| **5** | **`P1`** | `testing` | **Bake Chromium shell & asset cache into .pni/dockerfiles/Dockerfile and add unit tests for _pptx_writer.py** | `src/drawlib/_slide/_pptx_writer.py`, `src/drawlib/_builder/doc_builder/compiler/pdf.py`, `tests/drawlib/slide/test_pptx.py` | `common/runtime_verification` | Achieves 100% offline `--network=none` test pass rate and lifts `_pptx_writer.py` and `_pptx_dom.py` coverage above 80%. |
| **6** | **`P1`** | `testing` | **Validate asset filename membership in pkg.files before network downloads** | `src/drawlib/_core/l3_external/_download.py`, `src/drawlib/_release_assets.py` | `common/runtime_verification` | Eliminates unnecessary GitHub Release archive downloads on invalid icon names and fixes 12 offline `--network=none` unit test failures. |
| **7** | **`P2`** | `architecture` | **Eliminate Remaining 2 Intra-Diagram Sibling Import Cycles** | `src/drawlib/_diagrams/architecture/_edge.py`, `src/drawlib/_diagrams/architecture/_junction.py`, `src/drawlib/_diagrams/flow/_edge.py`, `src/drawlib/_diagrams/flow/_junction.py` | `common/architecture` | Achieves `0` runtime circular dependencies across all 424 modules. |
| **8** | **`P2`** | `code_quality` | **Replace Library-Level sys.exit(1) Calls with Typed Exceptions** | `src/drawlib/_core/l1_core/_settings.py`, `src/drawlib/_builder/doc_builder/processor/viewer.py`, `src/drawlib/_cli/_drawlib.py` | `common/library_guidelines` | Prevents unexpected interpreter termination for programmatic Python library callers. |
| **9** | **`P2`** | `security` | **Publish SECURITY.md and Configure Dependabot Updates** | `pyproject.toml`, `.github/workflows/quality.yml` | `common/supply_chain` | Closes OpenSSF Scorecard governance gaps for vulnerability disclosure and automated supply-chain maintenance. |
| **10** | **`P2`** | `testing` | **Include docs_src/api in Clean-Room Docker Test Context or Guard with pytest.skip** | `tests/drawlib/doc_builder/test_api_docs_completeness.py`, `.dockerignore`, `tools/docker/Dockerfile.test_local` | `python/testing` | Keeps `./dcli docker test` green across both local source and PyPI clean-room modes. |

---

## 3.3 Detailed Engineering Specifications by Priority Tier

### Phase `P0` — Urgent Security Remediation

#### Action #1 (`[P0]` · `security`): Upgrade locked Pillow dependency to `>=13.0.0` and re-verify raster baselines
- **Target Files**: `pyproject.toml`, `uv.lock`
- **Related Rules & Advisories**: `common/security_vulnerability`, `CVE-2026-112393`, `CVE-2026-112398`, `CVE-2026-112403`, `CVE-2026-112900`, `CVE-2026-96639`, `GHSA-78g4-xqwv-q3g8`
- **Implementation Guidance**: Upgrade `pillow` in `uv.lock` (`uv lock --upgrade-package pillow`) and bump the runtime lower bound in `pyproject.toml` to `pillow>=13.0.0` after verifying wheel availability across Python 3.11, 3.12, and 3.13. Run `./dcli test drawlib` to verify pixel-exact golden PNG comparisons under `tests/**/test_*_answers/` and refresh any raster baselines affected by upstream libjpeg/libtiff/libopenjp2 decoder updates.
- **Expected Impact**: Eliminates all **41 Trivy application CVEs** (`5 CRITICAL` CVSS 9.8, `23 HIGH`, `13 MEDIUM`), reducing `app_vuln_counts` to `0` and turning `common/security_vulnerability` SCA gates green.

---

### Phase `P1` — High-Value Hardening, Maintainability & Air-Gapped Testing

#### Action #2 (`[P1]` · `code_quality`): Decompose High-Complexity DOCX & Fence Parser Routines
- **Target Files**: `src/drawlib/_builder/doc_builder/exporter_docx.py`, `src/drawlib/_builder/doc_builder/processor/options.py`, `src/drawlib/_builder/doc_builder/merger.py`
- **Related Rules**: `common/maintainability`
- **Implementation Guidance**: Refactor `render_chapter` (`cognitive=174`, 283 LOC) and `_render_inline` (`cognitive=102`) in `exporter_docx.py` into per-token dispatch handlers (headings, code fences, callouts, lists, tables). Extract per-attribute validators from `parse_block_info` (`cognitive=106`) in `options.py`, and split TOC assembly, asset path rewriting, and heading normalization out of `build_merged_html` (`cognitive=87`) in `merger.py` so each helper maintains SIG cognitive complexity `<= 15`.
- **Expected Impact**: Substantially lowers maintenance risk, cyclomatic branch density, and isolated unit-testing effort across the HTML and OpenXML `.docx` compilation pipelines.

#### Action #3 (`[P1]` · `security`): Add non-root `USER` to Dockerfiles and publish `SECURITY.md` + Dependabot config
- **Target Files**: `tools/docker/Dockerfile.prod`, `tools/docker/Dockerfile.test_local`, `tools/docker/Dockerfile.test_pypi`
- **Related Rules & Advisories**: `common/security_vulnerability`, `common/supply_chain`, `DS-0002`
- **Implementation Guidance**: Add a dedicated non-root `USER drawlib` (`UID 10001`) across `tools/docker/Dockerfile.*` before `ENTRYPOINT`/`CMD`, author `SECURITY.md` documenting vulnerability disclosure and the `CWE-94` `exec()` trust boundary for untrusted Markdown/Python inputs, configure `.github/dependabot.yml` for `uv`/`pip` and `github-actions`, and migrate PyPI publishing from local `.env` API tokens to GitHub Actions OIDC Trusted Publishing.
- **Expected Impact**: Resolves all 3 `HIGH` Trivy container misconfigurations (`DS-0002`), automates upstream CVE pull requests, and eliminates local release token exposure.

#### Action #4 (`[P1]` · `security`): Run Production Docker Image as Non-Root User
- **Target Files**: `tools/docker/Dockerfile.prod`
- **Related Rules**: `common/supply_chain`, `common/security`
- **Implementation Guidance**: Create an unprivileged `drawlib` user and group (`UID/GID 10001`), relocate shared `DRAWLIB_CACHE_DIR` and `PLAYWRIGHT_BROWSERS_PATH` (`/opt/ms-playwright`) with world-readable/executable permissions, and switch to `USER drawlib` prior to `WORKDIR /workspace` in `tools/docker/Dockerfile.prod`.
- **Expected Impact**: Enforces strict container least privilege whenever rendering `drawlib` scripts or headless Chromium PDFs inside production containers.

#### Action #5 (`[P1]` · `testing`): Bake Chromium shell & asset cache into `.pni/dockerfiles/Dockerfile` and add unit tests for `_pptx_writer.py`
- **Target Files**: `src/drawlib/_slide/_pptx_writer.py`, `src/drawlib/_builder/doc_builder/compiler/pdf.py`, `tests/drawlib/slide/test_pptx.py`
- **Related Rules**: `common/runtime_verification`
- **Implementation Guidance**: Pre-install `chromium-headless-shell` (with OS shared libraries) and pre-populate `drawlib cache download --all` inside `.pni/dockerfiles/Dockerfile`, add a graceful offline skip guard when Chromium binaries are intentionally absent, and add pure-Python unit tests feeding synthetic `PptxSlide` dataclasses directly into `src/drawlib/_slide/_pptx_writer.py` without invoking Playwright.
- **Expected Impact**: Achieves a **100% offline `--network=none` test pass rate** (resolving the 6 Playwright CDN failures and 1 CJK font download failure) while lifting `_pptx_writer.py` (currently `11.1%`) and `_pptx_dom.py` (`58.6%`) coverage above `80%`.

#### Action #6 (`[P1]` · `testing`): Validate asset filename membership in `pkg.files` before network downloads
- **Target Files**: `src/drawlib/_core/l3_external/_download.py`, `src/drawlib/_release_assets.py`
- **Related Rules**: `common/runtime_verification`
- **Implementation Guidance**: Update `download_if_not_exist()` and `find_package_for_resource_path()` (and `find_package_for_icon_path()`) to verify that the requested relative asset path is listed in `pkg.files` (and check `pkg.is_downloaded()`) before calling `pkg.download_and_extract()`, immediately raising `FileNotFoundError` for bogus icon or font filenames without performing network I/O.
- **Expected Impact**: Eliminates redundant GitHub Release archive downloads on invalid icon lookups and immediately fixes **12 of the 19 offline `--network=none` unit test failures** (`test_nonexistent_*_icon_error`).

---

### Phase `P2` — Architectural, Library & Governance Polish

#### Action #7 (`[P2]` · `architecture`): Eliminate Remaining 2 Intra-Diagram Sibling Import Cycles
- **Target Files**: `src/drawlib/_diagrams/architecture/_edge.py`, `src/drawlib/_diagrams/architecture/_junction.py`, `src/drawlib/_diagrams/flow/_edge.py`, `src/drawlib/_diagrams/flow/_junction.py`
- **Related Rules**: `common/architecture`
- **Implementation Guidance**: Extract a lightweight connectable node/endpoint `Protocol` or base class into `_types.py` within `_diagrams/architecture/` and `_diagrams/flow/`, and guard concrete `_edge <-> _junction` cross-imports behind `if TYPE_CHECKING:` blocks.
- **Expected Impact**: Achieves **0 runtime circular dependencies** across all 424 Python source modules.

#### Action #8 (`[P2]` · `code_quality`): Replace Library-Level `sys.exit(1)` Calls with Typed Exceptions
- **Target Files**: `src/drawlib/_core/l1_core/_settings.py`, `src/drawlib/_builder/doc_builder/processor/viewer.py`, `src/drawlib/_cli/_drawlib.py`
- **Related Rules**: `common/library_guidelines`
- **Implementation Guidance**: Replace direct `sys.exit(1)` calls in `DrawlibSettings` (`_settings.py:123,297,304,313`) and `viewer.py` (`lines 189,193,245`) with `ValueError` or a typed `DrawlibError` exception, translating those exceptions to exit code `1` exclusively inside `src/drawlib/_cli/_drawlib.py:call_command()`.
- **Expected Impact**: Prevents unexpected host Python interpreter termination when `drawlib` is embedded programmatically inside notebooks, web backends, or automation services.

#### Action #9 (`[P2]` · `security`): Publish `SECURITY.md` and Configure Dependabot Updates
- **Target Files**: `pyproject.toml`, `.github/workflows/quality.yml`
- **Related Rules**: `common/supply_chain`
- **Implementation Guidance**: Publish a root `SECURITY.md` policy enabling GitHub Private Vulnerability Reporting and documenting supported versions, add `.github/dependabot.yml` covering `pip`/`uv` and `github-actions`, and pin third-party GitHub Actions (`actions/checkout`, `astral-sh/setup-uv`, `actions/setup-python`) to full 40-character commit SHAs.
- **Expected Impact**: Closes OpenSSF Scorecard supply-chain governance gaps for coordinated vulnerability disclosure and automated dependency maintenance.

#### Action #10 (`[P2]` · `testing`): Include `docs_src/api` in Clean-Room Docker Test Context or Guard with `pytest.skip`
- **Target Files**: `tests/drawlib/doc_builder/test_api_docs_completeness.py`, `.dockerignore`, `tools/docker/Dockerfile.test_local`
- **Related Rules**: `python/testing`
- **Implementation Guidance**: Unignore `docs_src/api/` in `.dockerignore` and copy it into `tools/docker/Dockerfile.test_local` for local source container verification, while adding a `pytest.skip("docs_src/api not present in packaged test environment")` guard in `test_api_docs_completeness.py` when testing standalone PyPI wheels via `Dockerfile.test_pypi`.
- **Expected Impact**: Ensures `./dcli docker test` remains consistently green across both local source and published PyPI clean-room container modes.
